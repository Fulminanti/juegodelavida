import pygame
import numpy as np
import sys

# Inicializar Pygame
pygame.init()

# Configuración
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Configurar la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Juego de la Vida de Conway')

# Fuente para texto
font = pygame.font.SysFont('Arial', 16)

# Crear grid
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))

# Variables de control
running = True
playing = False
clock = pygame.time.Clock()
fps = 10

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_buttons():
    # Botón de inicio/pausa
    button_text = "Pausar" if playing else "Iniciar"
    button_color = RED if playing else GREEN
    start_button = pygame.Rect(10, HEIGHT - 40, 100, 30)
    pygame.draw.rect(screen, button_color, start_button)
    text = font.render(button_text, True, WHITE)
    screen.blit(text, (start_button.x + 10, start_button.y + 5))
    
    # Botón de limpiar
    clear_button = pygame.Rect(120, HEIGHT - 40, 100, 30)
    pygame.draw.rect(screen, BLUE, clear_button)
    text = font.render("Limpiar", True, WHITE)
    screen.blit(text, (clear_button.x + 10, clear_button.y + 5))
    
    # Control de velocidad
    speed_text = font.render(f"Velocidad: {fps} FPS", True, BLACK)
    screen.blit(speed_text, (230, HEIGHT - 35))
    
    # Botones de velocidad
    speed_up = pygame.Rect(370, HEIGHT - 40, 30, 30)
    pygame.draw.rect(screen, GREEN, speed_up)
    text = font.render("+", True, WHITE)
    screen.blit(text, (speed_up.x + 10, speed_up.y + 5))
    
    speed_down = pygame.Rect(410, HEIGHT - 40, 30, 30)
    pygame.draw.rect(screen, RED, speed_down)
    text = font.render("-", True, WHITE)
    screen.blit(text, (speed_down.x + 10, speed_down.y + 5))
    
    # Instrucciones
    instructions = font.render("Click: Dibujar células | Botones: Controlar simulación", True, BLACK)
    screen.blit(instructions, (10, HEIGHT - 70))
    
    return start_button, clear_button, speed_up, speed_down

def update_grid():
    # Copiar la grid actual
    new_grid = grid.copy()
    
    # Aplicar las reglas del Juego de la Vida
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            # Contar vecinos vivos
            neighbors = count_neighbors(x, y)
            
            # Reglas del Juego de la Vida
            if grid[y][x] == 1:  # Célula viva
                if neighbors < 2 or neighbors > 3:
                    new_grid[y][x] = 0  # Muere por soledad o sobrepoblación
            else:  # Célula muerta
                if neighbors == 3:
                    new_grid[y][x] = 1  # Nace por reproducción
    
    return new_grid

def count_neighbors(x, y):
    # Cuenta los vecinos vivos alrededor de la célula (x, y)
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Saltar la propia célula
            
            nx, ny = (x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT  # Hacer que los bordes se conecten
            count += grid[ny][nx]
            
    return count

def draw_glider(x, y):
    # Dibuja un "glider" en la posición (x, y)
    if x < GRID_WIDTH - 3 and y < GRID_HEIGHT - 3:
        grid[y+1][x] = 1
        grid[y+2][x+1] = 1
        grid[y][x+2] = 1
        grid[y+1][x+2] = 1
        grid[y+2][x+2] = 1

# Dibujar algunos patrones iniciales
draw_glider(10, 10)
draw_glider(30, 15)

# Bucle principal
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo
                x, y = event.pos
                
                # Verificar si se hizo clic en los botones
                start_button, clear_button, speed_up, speed_down = draw_buttons()
                
                if start_button.collidepoint(x, y):
                    playing = not playing
                elif clear_button.collidepoint(x, y):
                    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))
                elif speed_up.collidepoint(x, y):
                    fps = min(60, fps + 5)
                elif speed_down.collidepoint(x, y):
                    fps = max(1, fps - 5)
                else:
                    # Convertir coordenadas de píxeles a coordenadas de grid
                    grid_x = x // CELL_SIZE
                    grid_y = y // CELL_SIZE
                    
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        # Alternar estado de la célula
                        grid[grid_y][grid_x] = 1 - grid[grid_y][grid_x]
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playing = not playing
            elif event.key == pygame.K_c:
                grid = np.zeros((GRID_HEIGHT, GRID_WIDTH))
            elif event.key == pygame.K_g:
                # Crear un glider donde el mouse está posicionado
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                draw_glider(grid_x, grid_y)
    
    # Actualizar el grid si la simulación está en marcha
    if playing:
        grid = update_grid()
    
    # Dibujar el grid
    draw_grid()
    
    # Dibujar botones e interfaz
    draw_buttons()
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()