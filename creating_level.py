import pygame
import json
from config import JSON_PATH
import items
from platforms import *
from NPCs import *

def read_json(level):
    with open(JSON_PATH,"r", encoding="utf-8") as game_info:
        data = json.load(game_info)
        selected_level = data[level]
    return selected_level

def create_platforms(lava_or_spikes, towers, floatings, platform_objects_list):
    for i in range(lava_or_spikes["amount"]):
        platform = get_lava_floor_spikes_or_street(folder=lava_or_spikes["folder"], mode=lava_or_spikes["mode"][i], starting_x=lava_or_spikes["starting_x"][i], starting_y=lava_or_spikes["starting_y"][i], width=lava_or_spikes["width"][i])
        for j in platform:
            platform_objects_list.append(j)

    for i in range(towers["amount"]):
        platform = get_tower(folder=towers["folder"], starting_x=towers["starting_x"][i], starting_y=towers["starting_y"][i], width=towers["width"][i], height=towers["height"][i])
        for j in platform:
            platform_objects_list.append(j)

    for i in range(floatings["amount"]):
        platform = get_floating_platform(folder=floatings["folder"], starting_x=floatings["starting_x"][i], starting_y=floatings["starting_y"][i], small=floatings["small"][i], moving=floatings["moving"][i], movement_speed=floatings["movement_speed"][i])
        for j in platform:
            platform_objects_list.append(j)

def create_items(beers, coins, lightnings=None, spinning_saws=None, turrets=None, buttons=None, force_fields=None, traffic_lights=None, item_object_list=None):
    for i in range(beers["amount"]):
        item = items.get_beer(folder=beers["folder"], x=beers["x"], y=beers["y"])
        item_object_list.append(item)
    
    for i in range(coins["amount"]):
        item = items.get_coin(path=coins["path"], x=coins["x"][i], y=coins["y"][i])
        item_object_list.append(item)

    if spinning_saws != None:
        for i in range(spinning_saws["amount"]):
            item = items.get_spinning_saw(folder=spinning_saws["folder"] ,x=spinning_saws["x"][i], y=spinning_saws["y"][i])
            item_object_list.append(item)

    if lightnings != None:
        for i in range(lightnings["amount"]):
            item = items.get_lightning(x=lightnings["x"][i], y=lightnings["y"][i])
            item_object_list.append(item)
    
    if turrets != None:
        for i in range(turrets["amount"]):
            item = items.get_turret(x=turrets["x"][i], y=turrets["y"][i])
            item_object_list.append(item)
    
    if buttons != None:
        for i in range(buttons["amount"]):
            item = items.get_button(x=buttons["x"], y=buttons["y"])
            item_object_list.append(item)
    
    if force_fields != None:
        for i in range(force_fields["amount"]):
            item = items.get_force_field(x=force_fields["x"], y=force_fields["y"])
            item_object_list.append(item)

    if traffic_lights != None:
        for i in range(traffic_lights["amount"]):
            item = items.get_traffic_light(x=traffic_lights["x"][i], y=traffic_lights["y"][i])
            item_object_list.append(item)

def create_npc(cops=None, choppers=None, stinks=None, aliens=None, drones=None, taxi=None, gang_members=None, npc_list=None):
    if cops:
        for i in range(cops["amount"]):
            npc = Cop(starting_x=cops["starting_x"][i], starting_y=cops["starting_y"][i], movement_amount=cops["movement_amount"][i], 
                    movements_speed=cops["movements_speed"][i], animation_speed=cops["animation_speed"][i], 
                    boss=cops["boss"][i], subfolder=cops["subfolder"][i])
            npc_list.append(npc)

    if aliens:
        for i in range(aliens["amount"]):
            npc = Cop(starting_x=aliens["starting_x"][i], starting_y=aliens["starting_y"][i], movement_amount=aliens["movement_amount"][i], 
                    movements_speed=aliens["movements_speed"][i], animation_speed=aliens["animation_speed"][i], 
                    boss=aliens["boss"][i], subfolder=aliens["subfolder"][i], alien=True)
            npc_list.append(npc)
    
    if choppers:
        for i in range(choppers["amount"]):
            npc = Chopper(starting_x=choppers["starting_x"][i], starting_y=choppers["starting_y"][i], 
                        movement_amount=choppers["movement_amount"][i], folder="CHOPPER")
            npc_list.append(npc)
    
    if drones:
        for i in range(drones["amount"]):
            npc = Drone(starting_x=drones["starting_x"][i], starting_y=drones["starting_y"][i], 
                        movement_amount=drones["movement_amount"][i], animation_speed=drones["animation_speed"][i], folder="DRONE")
            npc_list.append(npc)

    if stinks:
        for i in range(stinks["amount"]):
            npc = Stink(starting_x=stinks["starting_x"][i], starting_y=stinks["starting_y"][i], 
                        movement_amount=stinks["movement_amount"][i], movements_speed=stinks["movements_speed"][i],
                        animation_speed=stinks["animation_speed"][i])
            npc_list.append(npc)
    
    if taxi:
        for i in range(taxi["amount"]):
            npc = Taxi(starting_x=taxi["starting_x"][i], starting_y=taxi["starting_y"][i], movement_amount=taxi["movement_amount"][i], 
                    movements_speed=taxi["movements_speed"][i], animation_speed=taxi["animation_speed"][i])
            npc_list.append(npc)
    
    if gang_members:
        for i in range(gang_members["amount"]):
            npc = Cop(starting_x=gang_members["starting_x"][i], starting_y=gang_members["starting_y"][i], movement_amount=gang_members["movement_amount"][i], 
                    movements_speed=gang_members["movements_speed"][i], animation_speed=gang_members["animation_speed"][i], 
                    boss=gang_members["boss"][i], subfolder=gang_members["subfolder"][i], gang_member=True)
            npc_list.append(npc)