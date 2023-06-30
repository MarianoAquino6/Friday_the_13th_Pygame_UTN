import pygame
from music import play_music
from config import *
from NPCs import Cop, AlienQueen, Taxi, UFO

def set_final_battle(jason_voorhees, level, invisible_rects, npc_list):
    jason_voorhees.movement_amount += level["final_battle"]["jason_voorhees"]["movement_amount"]
    jason_voorhees.movements_speed -= level["final_battle"]["jason_voorhees"]["movements_speed"]
    jason_voorhees.life += level["final_battle"]["jason_voorhees"]["life"]

    jason_voorhees.movement_amount += 6
    jason_voorhees.movements_speed -= 4
    jason_voorhees.life += 500

    if level["level"] == 1:
        invisible_rects.pop(-1)
        boss = Cop(starting_x=SCREEN_WIDTH+level["final_battle"]["boss"]["starting_x"],
                    starting_y=level["final_battle"]["boss"]["starting_y"],
                    movement_amount=level["final_battle"]["boss"]["movement_amount"],
                    movements_speed=level["final_battle"]["boss"]["movements_speed"],
                    animation_speed=level["final_battle"]["boss"]["animation_speed"],
                    boss=level["final_battle"]["boss"]["boss"], 
                    subfolder=level["final_battle"]["boss"]["subfolder"])
    elif level["level"] == 2:
        boss = AlienQueen(starting_x=SCREEN_WIDTH+level["final_battle"]["boss"]["starting_x"],
                    starting_y=level["final_battle"]["boss"]["starting_y"],
                    movement_amount=level["final_battle"]["boss"]["movement_amount"],
                    movements_speed=level["final_battle"]["boss"]["movements_speed"],
                    animation_speed=level["final_battle"]["boss"]["animation_speed"],
                    subfolder=level["final_battle"]["boss"]["subfolder"], alien_queen=True)
    else:
        boss = AlienQueen(starting_x=SCREEN_WIDTH+level["final_battle"]["boss"]["starting_x"],
                    starting_y=level["final_battle"]["boss"]["starting_y"],
                    movement_amount=level["final_battle"]["boss"]["movement_amount"],
                    movements_speed=level["final_battle"]["boss"]["movements_speed"],
                    animation_speed=level["final_battle"]["boss"]["animation_speed"],
                    subfolder=level["final_battle"]["boss"]["subfolder"], michael_myers=True)
        for npc in npc_list:
            if type(npc) == Taxi:
                npc.boss = True
    npc_list.append(boss)

    play_music(level=level["level"], boss=True)

def create_UFO(jason_voorhees, npc_list):
    ufo = UFO(jason_voorhees.rect.x-250, -100, 8, 80)
    npc_list.append(ufo)
    return ufo
