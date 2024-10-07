import pygame
import numpy as np
import math
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projeção 3D de um Cubo")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definição dos vértices do cubo
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

# Definição das arestas do cubo (pares de índices dos vértices)
edges = [
    (0,1), (1,2), (2,3), (3,0),  # Arestas da face traseira
    (4,5), (5,6), (6,7), (7,4),  # Arestas da face frontal
    (0,4), (1,5), (2,6), (3,7)   # Arestas conectando as faces
]

# Matrizes de rotação
def rotation_matrix_x(theta):
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, cos_theta, -sin_theta, 0],
        [0, sin_theta, cos_theta, 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(theta):
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    return np.array([
        [cos_theta, 0, sin_theta, 0],
        [0, 1, 0, 0],
        [-sin_theta, 0, cos_theta, 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_z(theta):
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    return np.array([
        [cos_theta, -sin_theta, 0, 0],
        [sin_theta, cos_theta, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

# Função de projeção da câmera pinhole
def project_point(point, d):
    """
    Projeta um ponto 3D para 2D usando a técnica da câmera pinhole.

    :param point: Array de coordenadas [x, y, z, w]
    :param d: Distância da câmera ao plano de projeção
    :return: Coordenadas projetadas [x_proj, y_proj]
    """
    x, y, z, w = point
    if z + d != 0:
        x_proj = (x * d) / (z + d)
        y_proj = (y * d) / (z + d)
        return np.array([x_proj, y_proj])
    else:
        return np.array([0, 0])

# Função para converter coordenadas projetadas para a tela
def to_screen(point_2d):
    """
    Converte coordenadas 2D projetadas para coordenadas de tela.

    :param point_2d: Array de coordenadas [x, y]
    :return: Tupla de coordenadas na tela (x, y)
    """
    x, y = point_2d
    screen_x = int(WIDTH / 2 + x * 100)  # Escala para melhor visualização
    screen_y = int(HEIGHT / 2 - y * 100) # Inverte o eixo Y para correspondência com a tela
    return (screen_x, screen_y)

# Parâmetros de projeção
d = 5  # Distância da câmera ao plano de projeção

# Loop principal
def main():
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0  # Ângulos de rotação

    running = True
    while running:
        clock.tick(60)  # Limita a 60 FPS
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualização dos ângulos de rotação
        angle_x += 0.01
        angle_y += 0.01
        angle_z += 0.01

        # Matrizes de rotação atuais
        rot_x = rotation_matrix_x(angle_x)
        rot_y = rotation_matrix_y(angle_y)
        rot_z = rotation_matrix_z(angle_z)

        # Combinação das rotações (ordem Z * Y * X)
        rotation = rot_z @ rot_y @ rot_x

        # Lista para armazenar os pontos projetados
        projected_points = []

        for vertex in vertices:
            # Aplicar a rotação
            rotated = rotation @ vertex

            # Projeção 3D -> 2D
            projected = project_point(rotated, d)

            # Converter para coordenadas de tela
            screen_point = to_screen(projected)
            projected_points.append(screen_point)

        # Desenhar as arestas
        for edge in edges:
            start, end = edge
            pygame.draw.line(SCREEN, WHITE, projected_points[start], projected_points[end], 2)

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()