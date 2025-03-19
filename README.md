# Baixar Vídeos do YouTube com `yt-dlp`

Este projeto utiliza a biblioteca `yt-dlp` para baixar vídeos do YouTube diretamente para o seu computador. A interface web permite que o usuário insira múltiplos links de vídeos, escolha o formato de saída (MP4 ou MP3) e defina o diretório onde os vídeos serão salvos.

---

## Funcionalidades

- Baixa múltiplos vídeos do YouTube simultaneamente.
- Permite escolher o formato de saída: MP4 (vídeo) ou MP3 (áudio).
- Salva os vídeos em um diretório configurável pelo usuário.
- Interface web simples e intuitiva.
- Utiliza o `yt-dlp`, uma ferramenta poderosa e atualizada para downloads do YouTube.

---

## Pré-requisitos

Antes de executar o projeto, certifique-se de que os seguintes itens estão instalados no seu sistema:

1. **Python 3.7 ou superior**
   - Baixe e instale o Python a partir do site oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/).
   - Durante a instalação, marque a opção **"Add Python to PATH"**.

2. **Biblioteca `yt-dlp`**
   - Instale a biblioteca `yt-dlp` executando o seguinte comando no terminal:
     ```bash
     pip install yt-dlp
     ```

3. **Flask**
   - Instale o Flask para rodar a interface web:
     ```bash
     pip install flask
     ```

4. **FFmpeg (opcional, mas recomendado)**
   - O FFmpeg é necessário para converter vídeos para MP3 ou combinar áudio e vídeo em alguns formatos.
   - **Passos para instalar o FFmpeg no Windows**:
     1. Baixe o arquivo `ffmpeg-n7.1-latest-win64-gpl.zip` a partir do repositório oficial: [https://github.com/BtbN/FFmpeg-Builds/releases](https://github.com/BtbN/FFmpeg-Builds/releases).
     2. Extraia o conteúdo para um diretório, como `C:\ffmpeg`.
     3. Adicione o caminho `C:\ffmpeg\bin` às variáveis de ambiente do sistema:
        - Pressione `Win + S` e procure por **"Editar as variáveis de ambiente do sistema"**.
        - Clique em **Variáveis de Ambiente**.
        - Na seção **Variáveis do Sistema**, edite a variável `Path` e adicione o caminho `C:\ffmpeg\bin`.
     4. Teste a instalação executando o comando `ffmpeg -version` no terminal.

---

## Como Usar

1. **Clone ou baixe este repositório**
   - Clone o repositório usando Git:
     ```bash
     git clone https://github.com/seu-usuario/baixarVideoYT.git
     ```
   - Ou baixe o arquivo ZIP e extraia para um diretório local.

2. **Instale as dependências**
   - No terminal, navegue até o diretório do projeto e instale as dependências:
     ```bash
     pip install -r requirements.txt
     ```

3. **Execute o servidor**
   - Inicie o servidor Flask:
     ```bash
     python app.py
     ```

4. **Acesse a interface web**
   - Abra o navegador e acesse o endereço:
     ```
     http://127.0.0.1:5000/
     ```

5. **Baixe os vídeos**
   - Insira os links dos vídeos do YouTube (separados por vírgulas).
   - Escolha o formato de saída (MP4 ou MP3).
   - Defina o diretório onde os vídeos serão salvos.
   - Escolha a qualidade do video.
   - Clique no botão **"Baixar Vídeos"** e aguarde o download.

---

## Resultado

- Os vídeos serão baixados no diretório configurado pelo usuário.
- O status de cada vídeo será exibido na interface web, indicando se o download foi bem-sucedido ou se ocorreu algum erro.

---

## Melhorias Futuras

- Implementar a aplicação na Azure Cloud 
