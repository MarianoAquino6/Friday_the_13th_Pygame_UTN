import pygame
pygame.mixer.init()

def play_music(level, boss):
    if level == "MAIN MENU":
        pygame.mixer.music.load("SOUNDTRACK/Altar Of Sacrifice 8bit.mp3")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    if level == 1: 
        if not boss:
            pygame.mixer.music.load("SOUNDTRACK/The Dark Eternal Night 8bit.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.load("SOUNDTRACK/Culinary Hyperversity 8bit.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)

    if level == 2:
        if not boss:
            pygame.mixer.music.load("SOUNDTRACK/The Ancient Covenant 8bit.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.load("SOUNDTRACK/An Autopsy 8bit.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)

    if level == 3:
        if not boss:
            pygame.mixer.music.load("SOUNDTRACK/Pale Blue Dot 8bit.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.load("SOUNDTRACK/Fermented Offal Discharge 8bit.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)

    if level == "ENDING":
        pygame.mixer.music.load("SOUNDTRACK/Going the Distance 8bit.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)    