# -*- coding: utf-8 -*-
"""
Snake v1.0

Created on Wed Jun 24 18:49:20 2020

@author: lmunoz
"""
import pygame
import random

# ----------------- Constantes -----------------------
HEIGHT = 560
WIDTH = 480
SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUISH = (80, 80, 255)

# ------------------ Clases -------------------------- 
class Bloc:
    # Bloques graficos
    def __init__(self, x=None, y=None, color=(255, 255, 255), size=10):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        
    def coord(self):
        return (self.x, self.y)
        
    def display(self, screen):
        pygame.draw.rect(screen, self.color, 
                 pygame.Rect(self.x, self.y, self.size, self.size))
        
    def move(self, direction):
        if direction == 'up':
            self.move_up()
        elif direction == 'down':
            self.move_down()
        elif direction == 'left':
            self.move_left()
        elif direction == 'rigth':
            self.move_rigth()
        else:
            pass
        
    def move_up(self):
        head.y = (head.y - (head.size + 1)) % HEIGHT
    
    def move_down(self):
        head.y = (head.y + (head.size + 1)) % HEIGHT
    
    def move_left(self):
        head.x = (head.x - (head.size + 1)) % WIDTH
    
    def move_rigth(self):
        head.x = (head.x + (head.size + 1)) % WIDTH
        
    def __repr__(self):
        return f"Bloc[x={self.x}, y={self.y}]"

class Body:
    # Cuerpo de la serpiente
    def __init__(self):
        self.segs = []
        
    def add_segment(self, bloc):
        self.segs = [bloc] + self.segs
        
    def update(self, head):
        for i in range(0, len(self.segs) - 1):
            self.segs[i].x = self.segs[i+1].x
            self.segs[i].y = self.segs[i+1].y
        self.segs[-1].x = head.x
        self.segs[-1].y = head.y
        
    def coords(self):
        return [bloc.coord() for bloc in self.segs]
    
    def __len__(self):
        return len(self.segs)

# ------------------- Functions ----------------------------
def screen_base(screen):
    global BLACK, HEIGHT, WIDTH, SIZE
    
    screen.fill(BLACK)

    # Dibujamos una grilla de fondo
    for j in range(0, HEIGHT, SIZE):
        pygame.draw.line(screen, WHITE, (0, j), (WIDTH, j))
            
    for i in range(0, HEIGHT, SIZE):
        pygame.draw.line(screen, WHITE, (i, 0), (i, HEIGHT))


# ------------- Pygame Initialization -------------------    
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS', 30)

# Definimos el area de juego (screen)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!")
screen_base(screen)

# Definimos la serpiente (cabeza y cuerpo)
head = Bloc(WIDTH//2 + 1, HEIGHT//2 + 1, BLUE, SIZE - 1)
body = Body()
#head.display(screen)

# ------------------ Game Loop -------------------
game_over = False
direction = None
food_in_game = False

while not game_over:
    pygame.time.delay(5)
    # Se capturan los eventos del juego
    for event in pygame.event.get():
        # Si el evento es salir, se rompe el lazo del juego
        if event.type == pygame.QUIT:
            game_over = True
    
    # Comprobar si la serpiente se ha tocado a si misma
    # para reiniciar el juego
    if len(body) > 1:
        if head.coord() in body.coords():
             text = font.render("You lost", False, RED)
             textRect = text.get_rect()
             textRect.center = (WIDTH // 2, HEIGHT // 2)
             screen.blit(text, textRect)
             pygame.display.flip()
             pygame.time.delay(1000)
             
             direcion = None
             food_in_game = False
             head = Bloc(WIDTH//2 + 1, HEIGHT//2 + 1, BLUE, SIZE - 1)
             body = Body()
             head.display(screen)
             pygame.event.clear()
            
    # Comprobar si se ha presionado una tecla        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        direction = 'up'
    if keys[pygame.K_DOWN]:
        direction = 'down'
    if keys[pygame.K_LEFT]:
        direction = 'left'
    if keys[pygame.K_RIGHT]:
        direction = 'rigth'
 
    # Si la serpiente se esta moviendo, se debe de 
    # colocar la comida en una posicion aleatoria
    if direction != None and not food_in_game:
        food = Bloc(random.randint(0, 23) * SIZE + 1,  
                    random.randint(0, 23) * SIZE + 1,
                    RED, SIZE - 1)
        food_in_game = True
             
    # Si la cabeza esta sobre el comida esta debe de
    # aparecer en otro lado y la serpiente debe de crecer
    if food_in_game and head.coord() == food.coord():
        food_in_game = False
        body.add_segment(Bloc(color=BLUISH, size=SIZE - 1))
   
    # Actualizar la posicion de la serpiente
    if len(body) > 0:
        body.update(head)
        
    head.move(direction)
       
    # Se actualiza la pantalla del juego
    screen_base(screen)
    
    if food_in_game:
        food.display(screen)
    
    head.display(screen)
    
    # Si hay cuerpo, se muestra
    if len(body) > 0:
        for seg in body.segs:
            seg.display(screen)
        
    pygame.display.flip()
    clock.tick(20)
            
pygame.quit()

