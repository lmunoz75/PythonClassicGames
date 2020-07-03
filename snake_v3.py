# -*- coding: utf-8 -*-
"""
Snake v3.0

Created on Wed Jul 01 12:40:20 2020

@author: lmunoz
"""
import tkinter as tk
from random import choice
from pyfirmata import Arduino, util
from tkinter.messagebox import showerror
from time import sleep

class Square:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        
    def move_to(self, direction, width, height):
        if direction == 'Right':
            self.x = (self.x + self.size) % width
            
        if direction == 'Left':
            self.x = (self.x - self.size) % width
        
        if direction == 'Up':
            self.y = (self.y - self.size) % height
        
        if direction == 'Down':
            self.y = (self.y + self.size) % height
            
    def __eq__(self, other):
        # Use "=="in Square objects
        return self.x == other.x and self.y == other.y
    
    def copy(self):
        return Square(self.x, self.y, self.size)
    
    def __repr__(self):
        return f"Square[x={self.x}, y={self.y}]"
        

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.width = 400
        self.height = 480
        self.size = 16
        self.score = 0
        self.speed = 1000 // 16
        self.direction = "Right"
        self.new_direction = "Right"
        self.COM_PORT = "COM6"
        self.master.focus_force()
        
        self.master.title(f"Snake Game in tkinter! - Score : {self.score}")
        self.master.geometry(f"{self.width+1}x{self.height+1}+50+50")
        self.master.resizable(0, 0)
                
        self.body = [Square(x=choice(range(0, self.width, self.size)), 
                            y=choice(range(0, self.height, self.size)),
                            size=self.size)]
        self.set_food()
        
        self.blocked_moves = {'Left': 'Right', 'Right': 'Left',
                              'Up': 'Down', 'Down': 'Up'}
        


        self.board = tk.Canvas(width=self.width, height=self.height, bg='black')
        self.board.pack()
        
        self.joystick_init()

        self.board.bind_all("<Key>", self.key_press)
        
        self.read_joystick()

        self.game_loop()
        
    def joystick_init(self):
        # Espera a que haya un joysick conectado en el puerto COM
        print(f"Conecting to Joystick in {self.COM_PORT}. Please wait...")
        self.arduino = Arduino(self.COM_PORT)
        it = util.Iterator(self.arduino)
        it.start()
        sleep(1)

        print("Joystick conected")
        self.arduino.analog[1].enable_reporting()
        self.arduino.analog[2].enable_reporting()
        
        self.left_right = self.arduino.get_pin('a:1:i')
        self.up_down = self.arduino.get_pin('a:2:i')


    def read_joystick(self):
        a1_val = self.up_down.read()
        a2_val = self.left_right.read()

        # Control de rangos para deteccion del movimiento
        if a1_val is not None:
            if a1_val < 0.3:
                self.new_direction = 'Down'
            elif a1_val > 0.8:
                self.new_direction = 'Up'

        if a2_val is not None:
            if a2_val < 0.3:
                self.new_direction = 'Left'
            elif a2_val > 0.8:
                self.new_direction = 'Right'
            
        self.master.after(10, self.read_joystick) 
    
    def set_food(self):
        # Genera la posicion de la comida en un sitio aleatorio en el tablero
        # y que no ocupe la posicion de la serpiente
        while True:
            self.food = Square(x=choice(range(0, self.width, self.size)), 
                                y=choice(range(0, self.height, self.size)),
                                size=self.size)
            for sq in self.body:
                # Si la comida esta en un bloque del cuerpo de la serpiente...
                if self.food == sq:
                    # ...volver a generar una posicion
                    continue
            else:
                break
        
    def show_board(self):
        # Se muestra la grilla del tablero
        for i in range(0, self.height, self.size):
            self.board.create_line((0, i), (self.width, i), fill='#eeeeee')

        for i in range(0, self.width, self.size):
            self.board.create_line((i, 0), (i, self.height), fill='#eeeeee')        
        
        # Se muestra la serpiente
        self.board.create_rectangle((self.body[0].x + 1, self.body[0].y + 1), 
                                        (self.body[0].x + self.body[0].size - 1,
                                         self.body[0].y + self.body[0].size - 1), 
                                        fill='#32cd32')
        for sq in self.body[1:]:
            self.board.create_rectangle((sq.x + 1, sq.y + 1), 
                                        (sq.x + sq.size - 1, sq.y + sq.size - 1), 
                                        fill='green')
        
        # Se muestra el cuadrado de la comida        
        if self.food:
            self.board.create_rectangle((self.food.x + 1, self.food.y + 1), 
                                        (self.food.x + self.food.size - 1, 
                                            self.food.y +  self.food.size - 1), 
                                        fill='red')
        
        
    def key_press(self, event):
        #self.new_direction = event.keysym
        
        # Con Esc salimos del juego...
        if event.keysym == 'Escape':
            self.master.destroy()
            

    def game_loop(self):
        # Se limpia el tablero del juego
        self.board.delete(tk.ALL)
        
        # Se muestra la cuadricula del tablero, la serpiente y el alimento
        self.show_board()
        
        # Se establece la direccion del movimiento segun las
        # acciones del joystick, con la restriccion de no retroceder
        if self.blocked_moves.get(self.direction, None) != self.new_direction: 
            self.direction = self.new_direction
        else:
            pass
        
        # Si la cabeza de la serpiente esta sobre el cuerpo, 
        # pierde el juego
        for sq in self.body[1:]:
            if self.body[0] == sq:
                self.board.create_text(self.width // 2, self.height // 2, 
                                       text="GAME OVER", fill='red', 
                                       font='Courier 25 bold')
                return
        
        # Si la cabeza de la serpiente esta sobre la posicion del
        # alimento, el alimento aparece en otra posicion y la serpiente
        # aumenta su tamaño en un bloque
        if self.body[0] == self.food:
            self.score += 10
            self.master.title(f"Snake Game in tkinter! - Score : {self.score}")
            self.set_food()
            self.body.append(self.body[-1].copy())
            
        # Mueve la cabeza de la serpiente y el cuerpo
        for i in range(len(self.body)-1, 0, -1):
            self.body[i] = self.body[i-1].copy()
            self.body[i] = self.body[i-1].copy()
        
        self.body[0].move_to(self.direction, self.width, self.height)
        
        # Sostenimiento del lazo del juego
        self.master.after(self.speed, self.game_loop)
    
        
root = tk.Tk()
app = SnakeGame(root)
root.mainloop()
