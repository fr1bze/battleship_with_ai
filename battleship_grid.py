from engine import Game

import pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("Battleship")
myfont = pygame.font.SysFont("fresansttf", 100)

#glabal variables
SQ_SIZE = 45
H_MARGIN = SQ_SIZE * 4
V_MARGIN = SQ_SIZE
WIDTH = SQ_SIZE * 10 * 2 + H_MARGIN
HEIGHT = SQ_SIZE * 10 * 2 + V_MARGIN
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
INDENT = 10
HUMAN1 = True
HUMAN2 = False

GREY = (40,40,50)
WHITE = (255, 250, 250)
GREEN = (60,240,120)
BLUE = (50,50,200)
ORANGE = (250,140,40)
RED = (250,50,100)
COLORS = {"U":GREY,"M": BLUE,"H": ORANGE, "S": RED}

#function to draw a grid

def draw_grid(player, left = 0, top = 0, search = False):
    for i in range(100):
        x = i % 10 * SQ_SIZE + left 
        y = i // 10 * SQ_SIZE + top
        square = pygame.Rect(x,y,SQ_SIZE,SQ_SIZE)
        pygame.draw.rect(SCREEN,WHITE,square, width=1)
        if search:
            x += SQ_SIZE // 2
            y += SQ_SIZE // 2
            pygame.draw.circle(SCREEN,COLORS[player.search[i]],(x,y),radius = SQ_SIZE // 4)


#function to draw ships onto the position grids

def draw_ships(player, left = 0, top = 0):
    for ship in player.ships:
        x = ship.col * SQ_SIZE + left + INDENT
        y = ship.row * SQ_SIZE + top + INDENT
        if ship.orientation == "h":
            width = ship.size * SQ_SIZE - 2*INDENT
            height = SQ_SIZE - 2*INDENT
        else: 
            width = SQ_SIZE - 2*INDENT
            height = ship.size * SQ_SIZE - 2*INDENT
        rectangle = pygame.Rect(x,y,width,height)
        pygame.draw.rect(SCREEN,GREEN,rectangle,border_radius= 10)

game = Game(HUMAN1,HUMAN2)


animating = True
pausing = False
while animating:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            animating = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game.over:
            x,y = pygame.mouse.get_pos()
            if game.player1_turn and x < SQ_SIZE * 10 and y < SQ_SIZE * 10:
                row = y // SQ_SIZE
                col = x // SQ_SIZE
                index = row * 10 + col
                game.make_move(index)
            elif not game.player1_turn and x > WIDTH - SQ_SIZE * 10 and y > SQ_SIZE * 10 + V_MARGIN:
                row = (y - SQ_SIZE * 10 - V_MARGIN)  // SQ_SIZE
                col = (x - SQ_SIZE* 10 - H_MARGIN) // SQ_SIZE
                index = row * 10 + col
                game.make_move(index)
                print((row, col))

        if event.type == pygame.KEYDOWN:
            #escape key
            if event.key == pygame.K_ESCAPE:
                animating = False
            #pause and unpause
            if event.key == pygame.K_SPACE:
                pausing = not pausing

            #return Key to restart the game 
            if event.key == pygame.K_r and game.over:
                game = Game(HUMAN1,HUMAN2)
    #execution
    if not pausing:
        SCREEN.fill(GREY)

        #draw search grids
        draw_grid(game.player1,search=True)
        draw_grid(game.player2,search=True, left = (WIDTH - H_MARGIN)//2 + H_MARGIN, top = (HEIGHT - V_MARGIN)//2 + V_MARGIN)
        #draw position grids
        draw_grid(game.player1,top = (HEIGHT - V_MARGIN)//2 + V_MARGIN)
        draw_grid(game.player2,left = (WIDTH - H_MARGIN)//2 + H_MARGIN)

        draw_ships(game.player1,top = (HEIGHT - V_MARGIN)//2 + V_MARGIN)
        draw_ships(game.player2, left = (WIDTH - H_MARGIN)//2 + H_MARGIN)

        #computer moves
        if not game.over and game.computer_turn:
            if game.player1_turn:
                game.random_ai()
            else:
                pygame.time.wait(100)
                game.basic_ai()

        #game over message
        if game.over:
            text = "Player " + str(game.result) + " Won!"
            textbox = myfont.render(text, False,GREY,WHITE)
            SCREEN.blit(textbox, (WIDTH // 2 - 240 , HEIGHT//2 - 50))
        
        pygame.time.wait(100)
        pygame.display.flip()
    
