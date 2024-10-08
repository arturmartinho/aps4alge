# aps4alge
explicao do codigo:

Neste projeto, implementamos a projeção 3D de um cubo para um espaço 2D utilizando o Pygame. O processo envolve álgebra linear para manipulação de matrizes e projeção de pontos no espaço tridimensional para uma tela bidimensional.

1. Definição dos Vértices e Arestas do Cubo
Começamos definindo os vértices do cubo em coordenadas homogêneas (4D) para facilitar a aplicação de transformações lineares, como rotação e projeção. A quarta coordenada (w = 1) permite usar operações matriciais com mais facilidade:

vertices = np.array([
    [-1, -1, -1, 1],
    [1, -1, -1, 1],
    [1, 1, -1, 1],
    [-1, 1, -1, 1],
    [-1, -1, 1, 1],
    [1, -1, 1, 1],
    [1, 1, 1, 1],
    [-1, 1, 1, 1]
])
O cubo tem 8 vértices e as arestas são definidas como pares de índices desses vértices, conectando os pontos que formam as faces do cubo.

2. Matrizes de Rotação
Para rotacionar o cubo no espaço 3D, utilizamos matrizes de rotação para os três eixos (x, y e z). Cada matriz de rotação é derivada de operações trigonométricas e, em álgebra linear, a rotação é uma transformação linear representada por uma matriz de rotação. Para o eixo X, por exemplo, a matriz é definida como:

def rotation_matrix_x(theta):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(theta), -math.sin(theta), 0],
        [0, math.sin(theta), math.cos(theta), 0],
        [0, 0, 0, 1]
    ])
De forma semelhante, matrizes de rotação para os eixos Y e Z são definidas, e a rotação total é calculada pela multiplicação dessas matrizes (Z * Y * X), aplicando uma rotação em torno de cada eixo:

rotation = rot_z @ rot_y @ rot_x
Essa operação é essencialmente a multiplicação de matrizes que permite a rotação composta no espaço tridimensional.

3. Projeção de Pontos 3D para 2D
Uma vez que os vértices são rotacionados, aplicamos a projeção 3D para 2D. Neste código, utilizamos a técnica de projeção "pinhole", onde os pontos são projetados para um plano com base na distância da câmera. A projeção é realizada pela fórmula:

𝑥𝑝𝑟𝑜𝑗=𝑥⋅𝑑/𝑧+𝑑

xproj= z+d/x⋅d
​
 
𝑦𝑝𝑟𝑜𝑗=𝑦⋅𝑑𝑧+𝑑y 
proj= z+d/y⋅d
​
 
Aqui, 
𝑑
d é a distância da câmera até o plano de projeção, e 
𝑧
z é a profundidade do ponto no espaço 3D. A projeção simplifica os valores tridimensionais para coordenadas bidimensionais que podem ser desenhadas na tela:

def project_point(point, d):
    x, y, z, w = point
    x_proj = (x * d) / (z + d)
    y_proj = (y * d) / (z + d)
    return np.array([x_proj, y_proj])
Essa operação é baseada no conceito de transformação perspectiva, onde objetos mais distantes aparecem menores.

4. Conversão para Coordenadas de Tela
Após projetar os pontos no espaço 2D, eles precisam ser mapeados para a tela. A conversão ajusta as coordenadas projetadas para o sistema de coordenadas da tela (onde o centro da tela é mapeado como a origem):

def to_screen(point_2d):
    screen_x = int(WIDTH / 2 + x * 100)
    screen_y = int(HEIGHT / 2 - y * 100)
    return (screen_x, screen_y)
Esse mapeamento garante que o cubo seja desenhado de forma centralizada e com escala apropriada na tela.

5. Desenho das Arestas
Com os pontos projetados prontos, a última etapa é desenhar as arestas que conectam os vértices do cubo:

for edge in edges:
    start, end = edge
    pygame.draw.line(SCREEN, WHITE, projected_points[start], projected_points[end], 2)
A função pygame.draw.line desenha linhas entre os pontos projetados correspondentes às arestas do cubo, permitindo que o cubo rotacionado seja visualizado na tela.

Conclusão
Este código combina conceitos fundamentais de álgebra linear, como transformações matriciais e projeções, para criar uma visualização em 3D de um cubo. A rotação no espaço tridimensional é implementada por multiplicações de matrizes de rotação, enquanto a projeção é uma aplicação prática de geometria em perspectiva.
