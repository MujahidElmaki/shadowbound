import pygame, sys
from settings import *
from debug import debug
from level import Level

 
class Game:
    def __init__(self):
          
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        Icon = pygame.image.load('images/Icon.png')
        pygame.display.set_caption('ShadowBound')
        pygame.display.set_icon(Icon)
        self.clock = pygame.time.Clock()

        self.level = Level()
    
    def run(self):
        while True:
            for event in pygame.event.get(): # Loops to check if we want to quit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
 
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
 
if __name__ == '__main__':
    game = Game()
    game.run()