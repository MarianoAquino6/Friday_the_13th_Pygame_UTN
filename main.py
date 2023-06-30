import pygame
from pygame.locals import *
from config import *
import graphic_user_interface
import auxiliar

pygame.init()
pygame.font.init()
pygame.display.set_caption("Friday the 13th")

# graphic_user_interface.draw_menu()

#TESTING:
# graphic_user_interface.show_next_level(1, "testing")
# graphic_user_interface.show_next_level(2, "testing")
graphic_user_interface.show_next_level(3, "testing")