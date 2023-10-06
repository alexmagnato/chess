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
        self.dragger = Dragger()

    def mainloop(self):

        screen = self.screen
        game = self.game
        dragger = self.dragger
        
        while True:
            self.game.show_bg(self.screen)
            self.game.show_pieces(screen)

            for event in pygame.event.get():

                #Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    print(event.pos)
                    

                #Mouse motion
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

                #Click release
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

                #Quit app 
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            
            pygame.display.update()


main = Main()
main.mainloop()
