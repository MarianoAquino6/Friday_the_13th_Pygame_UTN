import pygame
import pygame_gui
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
gui_manager = pygame_gui.UIManager((800, 600))

background_color = (255, 255, 255)  # Color de fondo del cuadro de entrada de texto
text_color = (0, 0, 0)  # Color del texto del cuadro de entrada de texto

text_entry_line_rect = pygame.Rect(100, 100, 200, 30)
text_entry_line_bg_rect = text_entry_line_rect.inflate(4, 4)  # Rectángulo de fondo ligeramente más grande

container = pygame_gui.elements.UIContainer(
    relative_rect=pygame.Rect((0, 0), (800, 600)),  # Dimensiones del contenedor iguales a las dimensiones de la pantalla
    manager=gui_manager,
)

text_entry_line = pygame_gui.elements.UITextEntryLine(
    relative_rect=text_entry_line_rect,
    manager=gui_manager,
    container=container,
    object_id=pygame_gui.core.ObjectID("text_entry_line"),
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(background_color)  # Rellenar la pantalla con el color de fondo

    pygame.draw.rect(screen, text_color, text_entry_line_bg_rect)  # Dibujar el rectángulo de fondo
    gui_manager.update(0)
    gui_manager.draw_ui(screen)

    pygame.display.update()