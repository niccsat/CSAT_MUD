#!/usr/bin/env python

"""A simple Multi-User Dungeon (MUD) game. Players can talk to each
other, examine their surroundings and move between rooms.

Some ideas for things to try adding:
    * More rooms to explore
    * An 'emote' command e.g. 'emote laughs out loud' -> 'Mark laughs
        out loud'
    * A 'whisper' command for talking to individual players
    * A 'shout' command for yelling to players in all rooms
    * Items to look at in rooms e.g. 'look fireplace' -> 'You see a
        roaring, glowing fire'
    * Items to pick up e.g. 'take rock' -> 'You pick up the rock'
    * Monsters to fight
    * Loot to collect
    * Saving players accounts between sessions
    * A password login
    * A shop from which to buy items

author: Mark Frimston - mfrimston@gmail.com
"""

import time

# import the MUD server class
from mudserver import MudServer

# import rooms from rooms.py
from rooms import rooms

# import items from items.py
from items import items

# import npcs from npcs.py
from npcs import npcs

print(npcs)

# stores the players in the game
players = {}

# start the server
mud = MudServer()

# main game loop. We loop forever (i.e. until the program is terminated)
while True:

    # pause for 1/5 of a second on each loop, so that we don't constantly
    # use 100% CPU time
    time.sleep(0.2)

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()

    # go through any newly connected players
    for id in mud.get_new_players():

        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. We set their room to
        # None initially until they have entered a name
        # Try adding more player stats - level, gold, inventory, etc
        players[id] = {
            "name": None,
            "room": None,
            "credits": 100,
            "inventory": [],
            "npcChosen": "",
        }

        # send the new player a prompt for their name
        mud.send_message(id, "What is your name?")

    # go through any recently disconnected players
    for id in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players:
            continue

        # go through all the players in the game
        for pid, pl in players.items():
            # send each player a message to tell them about the diconnected
            # player
            mud.send_message(pid, "{} quit the game".format(
                                                        players[id]["name"]))

        # remove the player's entry in the player dictionary
        del(players[id])

    # go through any new commands sent from players
    for id, command, params in mud.get_commands():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if id not in players:
            continue

        # if the player hasn't given their name yet, use this first command as
        # their name and move them to the starting room.
        if players[id]["name"] is None:

            players[id]["name"] = command
            players[id]["room"] = "Hub 1 Center"

            # go through all the players in the game
            for pid, pl in players.items():
                # send each player a message to tell them about the new player
                mud.send_message(pid, "{} entered the game".format(
                                                        players[id]["name"]))

            # send the new player a welcome message
            mud.send_message(id, "Welcome to the game, {}. ".format(
                                                           players[id]["name"])
                             + "Type 'help' for a list of commands. Have fun!")

            # send the new player the description of their current room
            mud.send_message(id, rooms[players[id]["room"]]["description"])

        # each of the possible commands is handled below. Try adding new
        # commands to the game!

        # 'help' command
        elif command == "help":

            # send the player back the list of possible commands
            mud.send_message(id, "Commands:")
            mud.send_message(id, "  say <message>  - Says something out loud, "
                                 + "e.g. 'say Hello'")
            mud.send_message(id, "  look           - Examines the "
                                 + "surroundings, e.g. 'look'")
            mud.send_message(id, "  go <exit>      - Moves through the exit "
                                 + "specified, e.g. 'go outside'")

        # 'say' command
        elif command == "say":

            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # send them a message telling them what the player said
                    mud.send_message(pid, "{} says: {}".format(
                                                players[id]["name"], params))

        # 'look' command
        elif command == "look":

            # store the player's current room
            rm = rooms[players[id]["room"]]

            # send the player back the description of their current room
            mud.send_message(id, rm["description"])

            playershere = []
            # go through every player in the game
            for pid, pl in players.items():
                # if they're in the same room as the player
                if players[pid]["room"] == players[id]["room"]:
                    # ... and they have a name to be shown
                    if players[pid]["name"] is not None:
                        # add their name to the list
                        playershere.append(players[pid]["name"])

            # send player a message containing the list of players in the room
            mud.send_message(id, "Players here: {}".format(
                                                    ", ".join(playershere)))
            
                        # send player a message containing the list of npcs in the room
            mud.send_message(id, "NPCs here: {}".format(
                                                    ", ".join(rm["npcs"])))

            # send player a message containing the list of exits from this room
            mud.send_message(id, "Exits are: {}".format(
                                                    ", ".join(rm["exits"])))

        # 'npc' command
        elif command == "npc":
            print("npc")
            
            # store the npc name
            ex = params.lower()
            
            rm = rooms[players[id]["room"]]

            # handles KeyErrors somehow
            if npcs[ex]["type"] in npcs:
                npcType = npcs[ex]["type"]

            try:
                npcType = npcs[ex]["type"]
                players[id]["npcChosen"] = ex

            except KeyError:
                pass

            # if the npc is in the current room's npc list 
            if ex in rm["npcs"]:
                print("npc found")

                # find the type of npc
                if npcType == "shop":
                    print("shop")
                    mud.send_message(id, "Items for sale are:")
                    indexnum = 0

                    # send the player the items for sale 
                    for i in npcs[ex]["items"]:
                        print("for")
                        mud.send_message(id, str(npcs[ex]["items"]))


        # 'buy' command
        elif command == "buy":
            ex =  params.lower()
            rm = rooms[players[id]["room"]]

            # boolean for if npc is in current room
            npcsThere = False

            # checking if npc is in current room; prevents KeyErrors
            if players[id]["npcChosen"] in npcs:
                npcsThere = True

            else:
                npcsThere = False

            # check if the chosen item is in the currently selected npcs inventory
            if npcsThere and ex in npcs[players[id]["npcChosen"]]["items"]:

                # check if the price of the item is credits or an item
                if not(isinstance(npcs[players[id]["npcChosen"]]["items"][ex] ,int)):

                    print(str(npcs[players[id]["npcChosen"]]["items"][ex]))


                    # check if the player has the item in his/her inventory
                    if npcs[players[id]["npcChosen"]]["items"][ex] in players[id]["inventory"]:

                        # take the item from the player
                        players[id]["inventory"].remove(npcs[players[id]["npcChosen"]]["items"][ex])

                        # give the player the purchased item
                        players[id]["inventory"].append(ex)
                        mud.send_message(id, ex + " succesfully purchased!")
                    else:
                        mud.send_message(id, "You do not have enough to purchase this item.")

                else:
                    # check if the player has enough money
                    if npcs[players[id]["npcChosen"]]["items"][ex] < players[id]["credits"]:

                        # take the money from the player
                        players[id]["credits"] = players[id]["credits"] - npcs[players[id]["npcChosen"]]["items"][ex]

                        # give the player the purchased item
                        players[id]["inventory"].append(ex)
                        mud.send_message(id, ex + " succesfully purchased!")
                    else:
                        mud.send_message(id, "You do not have enough to purchase this item.  The item costs: " + str(npcs[players[id]["npcChosen"]]["items"][ex]))
                        print(str(npcs[players[id]["npcChosen"]]["items"][ex]))
            else:
                mud.send_message(id, "Item not found.")
                    

        # 'inventory' command
        elif command == "inventory":
            ex = params.lower()

            # send the player inventory list
            mud.send_message(id, str(players[id]["inventory"]))

            # send the player credits count
            mud.send_message(id, "You have " + str(players[id]["credits"]) + " credits.")


        # 'go' command
        elif command == "go":

            # store the exit name
            ex = params.lower()

            # store the player's current room
            rm = rooms[players[id]["room"]]

            # if the specified exit is found in the room's exits list
            if ex in rm["exits"]:

                # go through all the players in the game
                for pid, pl in players.items():
                    # if player is in the same room and isn't the player
                    # sending the command
                    if players[pid]["room"] == players[id]["room"] \
                            and pid != id:
                        # send them a message telling them that the player
                        # left the room
                        mud.send_message(pid, "{} left via exit '{}'".format(
                                                      players[id]["name"], ex))

                # update the player's current room to the one the exit leads to
                players[id]["room"] = rm["exits"][ex]
                players[id]["npcChosen"] = ""
                rm = rooms[players[id]["room"]]

                # go through all the players in the game
                for pid, pl in players.items():
                    # if player is in the same (new) room and isn't the player
                    # sending the command
                    if players[pid]["room"] == players[id]["room"] \
                            and pid != id:
                        # send them a message telling them that the player
                        # entered the room
                        mud.send_message(pid,
                                         "{} arrived via exit '{}'".format(
                                                      players[id]["name"], ex))

                # send the player a message telling them where they are now
                mud.send_message(id, "You arrive at '{}'".format(
                                                          players[id]["room"]))

            # the specified exit wasn't found in the current room
            else:
                # send back an 'unknown exit' message
                mud.send_message(id, "Unknown exit '{}'".format(ex))

        # some other, unrecognised command
        else:
            # send back an 'unknown command' message
            mud.send_message(id, "Unknown command '{}'".format(command))
