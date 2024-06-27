# OpenNote by Brrxis

OpenNotePad é um editor de texto Basico desenvolvido em Python com uma interface gráfica utilizando `tkinter` e `ttkbootstrap`. Ele suporta a criação de categorias e cadernos de anotações, bem como formatação de texto (negrito, itálico, sublinhado) e detecção de hyperlinks.

# Funcionalidades

- **Categorias e Cadernos**: Organize suas notas em categorias e cadernos.
- **Formatação de Texto**: Aplique negrito, itálico e sublinhado ao texto.
- **Detecção de Hyperlinks**: URLs no texto são detectadas automaticamente e podem ser clicadas para abrir no navegador.

# Pré-requisitos

- Python 3.12
- Pacotes listados no `requirements.txt` (ou seja, `tkinter`, `ttkbootstrap`, `Pillow`)

# Instalação

## Ambiente de Desenvolvimento

1. Clone o repositório:
    ```bash
    git clone
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # No Windows
    source .venv/bin/activate  # No Linux/Mac
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute o script:
    ```bash
    python main.py
    ```

# Compilando para Executável

Para compilar o projeto em um executável `.exe`, siga os passos abaixo:

1. Instale o PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2. Crie o executável:
    ```bash
    pyinstaller OpenNotePad.spec
    ```

3. O executável será gerado na pasta `dist`. Certifique-se de copiar a pasta `internals` (contendo todos os ícones e recursos) para o mesmo diretório onde o executável está localizado.

# Usando o Executável

Para usar o Advanced Notepad em qualquer pasta contendo o executável `.exe` e a pasta `internals`:

1. Copie o executável gerado (`OpenNotePad.exe`) e a pasta `internals` para o diretório desejado.
2. Certifique-se de que a estrutura de diretórios seja a seguinte:
    ```
    seu-diretorio/
    ├── OpenNotePad.exe
    └── internals/
        ├── icons/
        │   ├── boldico.png
        │   ├── italicico.png
        │   └── underlineico.png
        └── OpenNotesBrrxis.ico
    ```

3. Execute o arquivo `OpenNotePad.exe` para iniciar o Advanced Notepad.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias.

## Agradecimentos

- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) por fornecer um tema moderno para `tkinter`.
- [Pillow](https://python-pillow.org/) por facilitar o processamento de imagens.

