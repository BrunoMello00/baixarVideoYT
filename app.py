from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import yt_dlp
import re
from pathlib import Path

app = Flask(__name__)

# Função para validar URLs do YouTube
def validate_youtube_url(url):
    regex = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+'
    return re.match(regex, url) is not None

# Função para obter o caminho de downloads padrão do sistema
def get_default_download_path():
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:  # Linux, macOS e outros
        return str(Path.home() / 'Downloads')

# Função para garantir que a pasta de downloads exista e tenha permissões
def ensure_download_folder(download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.access(download_path, os.W_OK):
        try:
            os.chmod(download_path, 0o777)  # Torna a pasta gravável (Linux/macOS)
        except:
            pass  # Ignora erros no Windows

# Classe para capturar logs do yt_dlp
class MyLogger:
    def __init__(self):
        self.logs = []

    def debug(self, msg):
        if msg.startswith("ERROR:"):
            self.logs.append(msg)

    def warning(self, msg):
        self.logs.append(msg)

    def error(self, msg):
        self.logs.append(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Obtém as URLs, o destino, o formato e a resolução do formulário
        youtube_urls = request.form.get('youtubeUrl').split(',')
        download_destination = request.form.get('downloadDestination')  # 'server' ou 'pc'
        
        # Define o caminho de download com base no destino
        download_path = 'downloads' if download_destination == 'server' else get_default_download_path()
        ensure_download_folder(download_path)

        results = []  # Lista para armazenar o status de cada vídeo

        for url in youtube_urls:
            url = url.strip()  # Remove espaços extras
            if not validate_youtube_url(url):
                results.append({'url': url, 'status': 'error', 'message': 'URL inválido'})
                continue

            logger = MyLogger()  # Logger para capturar mensagens

            # Configura o filtro de formato com base na resolução e no formato
            format = request.form.get('format', 'mp4')  # Padrão para MP4
            resolution = request.form.get('resolution', 'best')  # Padrão para melhor qualidade
            format_filter = f'bestvideo[height<={resolution[:-1]}]+bestaudio/best' if resolution != 'best' else 'best'
            if format == 'mp3':
                format_filter = 'bestaudio/best'

            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'logger': logger,
                'noplaylist': True,  # Baixa apenas o vídeo, não a playlist inteira
                'format': format_filter,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if format == 'mp3' else []
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                results.append({'url': url, 'status': 'success', 'message': 'Vídeo baixado com sucesso!'})
            except Exception as e:
                # Captura erros específicos do yt_dlp
                error_message = logger.logs[-1] if logger.logs else str(e)
                results.append({'url': url, 'status': 'error', 'message': error_message})
        
        print(f"Download path: {download_path}")
        print(f"Results: {results}")
        return jsonify(results), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


# Rota para servir arquivos baixados no servidor
@app.route('/downloads/<path:filename>')
def serve_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))