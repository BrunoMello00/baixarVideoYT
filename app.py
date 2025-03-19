from flask import Flask, request, jsonify, render_template
import os
import yt_dlp
import re

app = Flask(__name__)

# Função para validar URLs do YouTube
def validate_youtube_url(url):
    regex = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+'
    return re.match(regex, url) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Obtém as URLs, o caminho de download, o formato e a resolução do formulário
        youtube_urls = request.form.get('youtubeUrl').split(',')
        download_path = request.form.get('downloadPath')
        format = request.form.get('format', 'mp4')  # Padrão para MP4
        resolution = request.form.get('resolution', 'best')  # Padrão para melhor qualidade

        # Garante que o diretório de download exista
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        results = []  # Lista para armazenar o status de cada vídeo

        for url in youtube_urls:
            url = url.strip()  # Remove espaços extras
            if not validate_youtube_url(url):
                results.append({'url': url, 'status': 'error', 'message': 'URL inválido'})
                continue

            logger = MyLogger()  # Logger para capturar mensagens

            # Configura o filtro de formato com base na resolução e no formato
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

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))