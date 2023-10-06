import pygame
import sys

from const import *
from game import Game
from dragger import Dragger


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( size=(WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()
        

    def mainloop(self):

        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        
        while True:
            self.game.show_bg(self.screen)
            self.game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                #Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    #if clicker square has piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)


                #Mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        dragger.update_blit(screen)
                        

                #Click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                #Quit app 
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            
            pygame.display.update()


main = Main()
main.mainloop()
