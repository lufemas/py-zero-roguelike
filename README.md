# Roguelike Game

Este é um jogo simples de estilo **Roguelike** feito em **Python** usando **Pygame Zero**.

## Como Rodar o Jogo

Para rodar o jogo, você precisa ter o **Python 3.X** instalado no seu sistema.

### Passos para Instalar e Rodar o Jogo:

1. **Instale o Python**: Se ainda não tiver o Python instalado, você pode baixá-lo [aqui](https://www.python.org/downloads/).
   
2. **Clone ou Baixe o Projeto**:
    Você pode clonar o repositório ou baixar os arquivos diretamente.

3. **Instale as Dependências**:
    Na pasta onde você baixou o projeto, abra o terminal (ou prompt de comando) e execute:
    ```bash
    pip install -r requirements.txt
    ```
    Isso irá instalar as dependências necessárias, neste caso é apenas o **Pygame Zero**.

    Alternativamente você ode instalar o **Pygame Zero** de forma global no seu sistema.
    Para isso abra o terminal (ou prompt de comando) e digite o seguinte comando:
    ```bash
    pip install pgzero
    ```

4. **Execute o Jogo**:
    Ainda na pasta do projeto, execute o jogo com o seguinte comando:
    ```bash
    python main.py
    ```

### Como Jogar:
- Use as **setas do teclado** para mover o herói.
- O objetivo do jogo é **encontrar o baú** enquanto **evita os inimigos**.
- O jogo possui um **menu principal** com opções para iniciar o jogo, alternar som e sair.

## Dependências
- As dependências estão listadas no arquivo `requirements.txt`. Elas serão instaladas automaticamente com o comando:
  ```bash
  pip install -r requirements.txt
