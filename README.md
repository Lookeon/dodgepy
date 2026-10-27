# dodgepy

Jogo de queimada em Python com Tkinter, feito com programação orientada a objetos. Desvie das bolas que caem do topo da tela e sobreviva o máximo que puder.

## Como jogar

- Mover para a esquerda: `←`
- Mover para a direita: `→`

Regras:

- Uma nova bola cai do topo da tela a cada 0,9 segundo, em uma posição aleatória.
- Cada bola que passa pelo fundo da tela sem te atingir vale 1 ponto.
- A velocidade das bolas aumenta conforme a pontuação cresce.
- Se uma bola atingir o jogador, o jogo termina. Clique em "Jogar novamente" para recomeçar.

## Como executar

Requisitos: Python 3.8 ou superior com Tkinter (já incluso no Windows e no macOS).

No Linux, se necessário:

```bash
sudo apt install python3-tk
```

Executando o jogo:

```bash
git clone https://github.com/Lookeon/dodgepy.git
cd dodgepy
python queimada_oop.py
```

## Estrutura

O código está em `queimada_oop.py`, com três classes:

- `Ball`: bola que cai, com movimento, detecção de saída da tela e remoção
- `Player`: jogador com visual futurista e movimento horizontal
- `Game`: loop do jogo, colisões, geração de bolas, pontuação e tela de fim de jogo

A colisão entre o jogador e as bolas é calculada entre um retângulo e um círculo.

## Configuração

As constantes no topo do arquivo definem o tamanho da janela:

| Constante | Padrão | Descrição               |
|-----------|--------|-------------------------|
| `LARGURA` | 720    | Largura da área de jogo |
| `ALTURA`  | 520    | Altura da área de jogo  |


<img width="595" height="436" alt="image" src="https://github.com/user-attachments/assets/6ec1126c-c454-4155-91f7-ff99de739ece" />
