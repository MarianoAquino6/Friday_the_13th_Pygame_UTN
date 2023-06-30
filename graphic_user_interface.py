import pygame
import sys
from config import *
from music import play_music
import level_1
import level_2
import level_3
import pygame_gui
import auxiliar

pygame.init()

MANAGER = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2+130), (300,50)), manager=MANAGER, 
                                                 object_id="#main_text_entry")

def draw_menu():
    play_music(level="MAIN MENU", boss=False)
    start_game_button = pygame.Rect(100, 400, 300, 50)
    controls_button = pygame.Rect(100, 500, 300, 50)
    info_button = pygame.Rect(100, 600, 300, 50)
    ranking_button = pygame.Rect(800, 600, 300, 50)
    background_image = pygame.image.load("BACKGROUND IMAGES/GUI/MENU BACKGROUND.png")

    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.collidepoint(event.pos):
                    offer_user_input()
                elif controls_button.collidepoint(event.pos):
                    draw_controls()
                elif info_button.collidepoint(event.pos):
                    draw_info()
                elif ranking_button.collidepoint(event.pos):
                    show_ranking()

        SCREEN.blit(background_image, (0, 0))
        pygame.draw.rect(SCREEN, (255, 30, 30), start_game_button)
        pygame.draw.rect(SCREEN, (255, 30, 30), controls_button)
        pygame.draw.rect(SCREEN, (255, 30, 30), info_button)
        pygame.draw.rect(SCREEN, (255, 30, 30), ranking_button)

        font = pygame.font.Font("corpse.ttf", 36)
        start_text = font.render("START GAME", True, (0, 0, 0))
        controls_text = font.render("CONTROLS", True, (0, 0, 0))
        info_text = font.render("ABOUT", True, (0, 0, 0))
        ranking_text = font.render("SCORE RANKING", True, (0, 0, 0))

        SCREEN.blit(start_text, (start_game_button.x + 50, start_game_button.y + 5))
        SCREEN.blit(controls_text, (controls_button.x + 65, controls_button.y + 5))
        SCREEN.blit(info_text, (info_button.x + 85, info_button.y + 5))
        SCREEN.blit(ranking_text, (ranking_button.x + 35, ranking_button.y + 5))

        pygame.display.flip()

def offer_user_input():
    background_image = pygame.image.load("BACKGROUND IMAGES/GUI/NAME INPUT.png")

    while True:
        UI_REFRESH_RATE = CLOCK.tick(60)/1000
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                player_name_high_score = str(event.text)
                show_next_level(1, player_name_high_score)

            MANAGER.process_events(event)

        MANAGER.update(UI_REFRESH_RATE)
        SCREEN.blit(background_image, (0,0))
        MANAGER.draw_ui(SCREEN)

        pygame.display.update()

def show_pause_screen():
    pause_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    background_image = pygame.image.load("BACKGROUND IMAGES/GUI/PAUSE.png").convert()
    background_image = pygame.transform.scale(background_image, (600,300))

    black_surface = pygame.Surface((700, 400))
    black_surface.fill((0, 0, 0))

    screen_center_x = SCREEN_WIDTH // 2
    screen_center_y = SCREEN_HEIGHT // 2
    
    # BLACK CENTERED SURFACE
    black_surface_rect = black_surface.get_rect(center=(screen_center_x, screen_center_y))
    pause_screen.blit(black_surface, black_surface_rect)

    # BACKGROUND IMAGE ON TOP OF BLACK CENTERED SURFACE
    background_rect = background_image.get_rect(center=(screen_center_x, screen_center_y-50))
    pause_screen.blit(background_image, background_rect)

    resume_button.draw()
    back_to_menu.draw()

    font = pygame.font.Font("Friday13SH.ttf", 48)
    text = font.render("Need a Break?", True, (255,255,255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+150))
    pause_screen.blit(text, text_rect)
    
    SCREEN.blit(pause_screen, (0, 0))
    pygame.display.flip()

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(font, 24)

    def draw(self):
        pygame.draw.rect(SCREEN, (255, 30, 30), self.rect)
        pygame.draw.rect(SCREEN, (0,0,0), self.rect, 2)
        text = self.font.render(self.text, True, (0,0,0))
        text_rect = text.get_rect(center=self.rect.center)
        SCREEN.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

pause_button = Button(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 50, 100, 40, "PAUSE", "corpse.ttf")
resume_button = Button(450, 600, 100, 40, "RESUME", "corpse.ttf")
return_button_menu = Button(50, 30, 170, 40, "RETURN", "corpse.ttf")
try_again_button = Button(420, 600, 130, 40, "TRY AGAIN", "corpse.ttf")
back_to_menu = Button(630, 600, 200, 40, "BACK TO MENU", "corpse.ttf")
paused = False

def show_death_screen(level, score, player_name):
    pygame.mixer.stop()
    background_image = pygame.image.load("BACKGROUND IMAGES/GUI/GAME OVER SCREEN.png")
    font = pygame.font.Font("corpse.ttf", 55)
    high_score_text = font.render(f"{score}", True, (255,255,255))

    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_button.rect.collidepoint(event.pos):
                    if level == 1:
                        level_1.level_1(player_name)
                    if level == 2:
                        level_2.level_2(player_name, 0)
                    if level == 3:
                        level_3.level_3(player_name, 0)
                if back_to_menu.rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    draw_menu()

        SCREEN.blit(background_image, (0,0))
        SCREEN.blit(high_score_text, (SCREEN_WIDTH/2-15, SCREEN_HEIGHT/2-68))
        try_again_button.draw()
        back_to_menu.draw()

        pygame.display.flip()

def show_ending_screen(score, highest_score):
    pygame.mixer.stop()
    play_music(level="ENDING", boss=False)
    background_image = pygame.image.load("BACKGROUND IMAGES/GUI/ENDING SCREEN.png")
    font = pygame.font.Font("corpse.ttf", 55)
    high_score_text = font.render(f"{highest_score}", True, (255,255,255))
    score = font.render(f"{score}", True, (255,0,0))

    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_menu.rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    draw_menu()

        SCREEN.blit(background_image, (0,0))
        SCREEN.blit(high_score_text, (300, 310))
        SCREEN.blit(score, (650,430))
        back_to_menu.rect.centerx = SCREEN_WIDTH//2
        back_to_menu.draw()

        pygame.display.flip()

def show_next_level(level, player_name, score=0):
    pygame.mixer.stop()
    pygame.mixer.music.fadeout(3000)
    event_3000ms = pygame.USEREVENT
    pygame.time.set_timer(event_3000ms, 3000)
    level_1_trailer_screen = pygame.image.load("BACKGROUND IMAGES/GUI/LEVEL 1 TRAILER.png")
    level_2_trailer_screen = pygame.image.load("BACKGROUND IMAGES/GUI/LEVEL 2 TRAILER.png")
    level_3_trailer_screen = pygame.image.load("BACKGROUND IMAGES/GUI/LEVEL 3 TRAILER.png")

    while True:
        #-----------------------------------------------------EVENTS----------------------------------------------------
        if level == 1:
            SCREEN.blit(level_1_trailer_screen, (0,0))
        elif level == 2:
            SCREEN.blit(level_2_trailer_screen, (0,0))
        else:
            SCREEN.blit(level_3_trailer_screen, (0,0))
        
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == event_3000ms:
                if level == 1:
                    level_1.level_1(player_name)
                elif level == 2:
                    level_2.level_2(player_name, score)
                else:
                    level_3.level_3(player_name, score)
        pygame.display.flip()

def draw_controls():
    background_image = pygame.image.load("BACKGROUND IMAGES/GUI/CONTROL MENU.png").convert()

    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_menu.rect.collidepoint(event.pos):
                    return  #BACK TO MAIN MENU

        SCREEN.blit(background_image, (0, 0))
        pygame.draw.rect(SCREEN, (255, 30, 30), return_button_menu.rect)

        font = pygame.font.Font("corpse.ttf", 36)
        return_text = font.render("Return", True, (0, 0, 0))
        SCREEN.blit(return_text, (return_button_menu.rect.x + 30, return_button_menu.rect.y))

        pygame.display.flip()

def draw_info():
    background_image = pygame.image.load("BACKGROUND IMAGES/GUI/ABOUT MENU.png").convert()

    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_menu.rect.collidepoint(event.pos):
                    return  #BACK TO MAIN MENU

        SCREEN.blit(background_image, (0, 0))
        return_button_menu.draw()

        pygame.display.flip()

def show_ranking():
    background_image = pygame.image.load("BACKGROUND IMAGES/GUI/RANKING.png").convert()
    font_corpse = pygame.font.Font("corpse.ttf", 40)
    font_friday = pygame.font.Font("Friday13SH.ttf", 49)
    ranking_name_string, ranking_score_string = auxiliar.rank_players()
    ranking_name_text = font_friday.render(ranking_name_string, True, (255, 255, 255))
    ranking_score_text = font_corpse.render(ranking_score_string, True, (255, 255, 255))

    while True:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_menu.rect.collidepoint(event.pos):
                    return  #BACK TO MAIN MENU

        SCREEN.blit(background_image, (0,0))
        SCREEN.blit(ranking_name_text, (220,200))
        SCREEN.blit(ranking_score_text, (840,200))

        return_button_menu.draw()

        pygame.display.flip()