import pygame
import os
from config import *
import graphic_user_interface
import sqlite3

#GETTING SURFACES
def get_surface_list_from_sprite_images_and_scale_them(folder, subfolder, flip_image=False, jason_attacking=False, 
                                                       dead_victim = False, lightning=False, spinning_saw=False, chopper=False, 
                                                       turret=False, diagonal=False, bullet=False, boss=False, button=False, 
                                                       force_field = False, alien=False, drone=False, alien_queen=False, 
                                                       traffic_light=False, taxi=False, gang_member=False, michael_myers=False, 
                                                       ufo=False):
    surfaces_list = []
    path = os.path.join(folder, subfolder)

    for file in os.listdir(path):
        image = pygame.image.load(os.path.join(path, file)).convert_alpha()

        #ROTATION AND FLIPPING
        if diagonal:
            image = pygame.transform.rotate(image, -45)
        if flip_image:
            image = pygame.transform.flip(image,True,False)

        #SCALING IMAGES
        if jason_attacking:
            scaled_image = pygame.transform.scale(image, (100,160))
        elif boss:
            if dead_victim:
                scaled_image = pygame.transform.scale(image, (200,70))
            else:
                scaled_image = pygame.transform.scale(image, (200,200))
        elif dead_victim and not boss and not alien_queen and not michael_myers:
            if alien:
                scaled_image = pygame.transform.scale(image, (160,50))
            else:
                scaled_image = pygame.transform.scale(image, (160,70))
        elif alien_queen and dead_victim:
            scaled_image = pygame.transform.scale(image, (300,70))
        elif michael_myers and dead_victim:
            scaled_image = pygame.transform.scale(image, (280,70))
        elif lightning:
            scaled_image = pygame.transform.scale(image, (50,SCREEN_HEIGHT))
        elif spinning_saw:
            scaled_image = pygame.transform.scale(image, (150,80))
        elif chopper:
            scaled_image = pygame.transform.scale(image, (600,300))
        elif turret:
            scaled_image = pygame.transform.scale(image, (180,150))
        elif bullet:
            scaled_image = pygame.transform.scale(image, (10,7))
        elif button:
            scaled_image = pygame.transform.scale(image, (50,130))
        elif force_field:
            scaled_image = pygame.transform.scale(image, (300,SCREEN_HEIGHT))
        elif alien:
            scaled_image = pygame.transform.scale(image, (150, 150))
        elif drone:
            scaled_image = pygame.transform.scale(image, (100, 100))
        elif alien_queen:
            scaled_image = pygame.transform.scale(image, (320, 200))
        elif traffic_light:
            scaled_image = pygame.transform.scale(image, (50,210))
        elif taxi:
            scaled_image = pygame.transform.scale(image, (300,160))
        elif gang_member:
            scaled_image = pygame.transform.scale(image, (70,160))
        elif michael_myers:
            scaled_image = pygame.transform.scale(image, (80,200))
        elif ufo:
            scaled_image = pygame.transform.scale(image, (600,700))
        else:
            scaled_image = pygame.transform.scale(image, (70,160))
        surfaces_list.append(scaled_image)
    return surfaces_list

#CREATING INVISIBLE RECTS FOR NPCS TO COLLIDE WITH
def create_invisible_rect_for_npcs_collision(invisible_rects):
    invisible_rect_list= []
    x_coordinates = invisible_rects["x_coordinates"]
    for i in range(invisible_rects["amount"]):
        invisible_rect = pygame.Rect(x_coordinates[i], 0, 20, SCREEN_HEIGHT)
        invisible_rect_list.append(invisible_rect)
    return invisible_rect_list

def save_highscore_in_csv(score, name):
    if not os.path.isfile("Highest Score.csv"):
        with open("Highest Score.csv", "w") as file:
            file.write("name,score\n")
    else:
        with open("Highest Score.csv", "a") as file:
            file.write(f"{name},{str(score)}\n")

        print("Score has been saved in CSV file")

def find_highest_score():
    highest_score = 0
    player_name = ""

    if os.path.isfile("Highest Score.csv"):
        with open("Highest Score.csv", "r") as file:
            next(file)  #SKIPPING FIRST LINE

            for line in file:
                line = line.strip().split(",")
                name = line[0]
                score = int(line[1])

                if score > highest_score:
                    highest_score = score
                    player_name = name

    return f"{player_name}......... {highest_score}"

def sort_scores(scores_list):
    flag_swap = True
    while(flag_swap):
        flag_swap = False

        for i in range(len(scores_list) - 1):
                if scores_list[i]["score"] < scores_list[i+1]["score"]:
                    scores_list[i],scores_list[i+1] = scores_list[i+1],scores_list[i]
                    flag_swap = True
    return scores_list

def save_score_in_database(name, score):
    connection = sqlite3.connect('scoresgame.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (str(name), score))

    connection.commit()
    connection.close()

def read_ordered_data():
    connection = sqlite3.connect('scoresgame.db')
    cursor = connection.cursor()

    cursor.execute("SELECT name, score FROM scores ORDER BY score DESC")
    data = cursor.fetchall()

    connection.close()

    return data

def rank_players():
    ordered_data = read_ordered_data()
    ranking_names = []
    ranking_scores = []

    for data in ordered_data:
        nombre = data[0]
        puntuacion = data[1]
        to_save_name_string = f"{nombre}\n"
        to_save_score_string = f"{puntuacion}\n"
        ranking_names.append(to_save_name_string)
        ranking_scores.append(to_save_score_string)

    to_return_name_string = "".join(ranking_names)
    to_return_score_string = "".join(ranking_scores)
    return to_return_name_string, to_return_score_string

def get_highest_score():
    connection = sqlite3.connect('scoresgame.db')
    cursor = connection.cursor()

    cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 1")
    data = cursor.fetchone()

    connection.close()

    name = data[0]
    score = data[1]

    jugador_mas_puntuado = f"{name}......... {score}"

    return jugador_mas_puntuado