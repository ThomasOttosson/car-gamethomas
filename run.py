import random
from random import randrange

import colorama
from colorama import Fore, Back, Style
colorama.init()


def check_ok(boat, taken):
    """
    Check if a boat's positions are valid and do not
    overlap with existing taken positions.
    """
    boat.sort()  # Ensure positions are in ascending order for validation
    for i in range(len(boat)):
        num = boat[i]
        if num in taken:  # Boat invalid if position is taken
            boat = [-1]
            break
        elif num < 0 or num > 99:  # Check if position is out of board range
            boat = [-1]
            break
        elif num % 10 == 9 and i < len(boat) - 1:
            # Stops wrapping to next row
            if boat[i + 1] % 10 == 0:
                boat = [-1]
                break
        if i != 0:
            if boat[i] != boat[i - 1] + 1 and boat[i] != boat[i - 1] + 10:
                # Rule
                boat = [-1]
                break

    return boat


def get_ship(long, taken):
    """
    Prompt the user to input a valid ship of the
    specified length and update the taken list.
    """
    while True:
        ship = []
        print(Fore.GREEN + Back.BLACK + "Welcome to Battleships Game")
        print("")
        print("GUIDELINES AND RULES:")
        print("The board consists of the numbers 0-99")
        print("You can place your ships as a row (for example 1,2,3,4,5)")
        print("Or you can place the ships vertical (for example 10,20,30,40)")
        print("")
        print("Enter your ship of length", long)
        input_valid = True  # Flag to track if all inputs are valid
        for i in range(long):
            boat_num = input("please enter a number: ")
            try:
                num = int(boat_num)
            except ValueError:
                print("Error: Please enter a valid number.")
                input_valid = False
                break
            ship.append(num)
        if not input_valid:
            continue  # Restart the loop without printing an additional error

        ship = check_ok(ship, taken)  # Validate the ship positions
        if ship[0] != -1:
            taken = taken + ship  # Add valid ship positions to the taken list
            return ship, taken
        else:
            print("error - please try again")


def create_ships(taken, boats):
    """Generate all ships for the player based
    on specified boat lengths, updating taken positions."""
    ships = []
    for boat in boats:
        ship, taken = get_ship(boat, taken)  # Get each ship's positions
        ships.append(ship)  # Append each created ship
    return ships, taken


def check_boat(b, start, dirn, taken):
    """
    Generate a boat's positions based on starting
    position and direction and validate them.
    """
    boat = []
    if dirn == 1:  # Direction: Up
        for i in range(b):
            boat.append(start - i * 10)
    elif dirn == 2:  # Direction: Right
        for i in range(b):
            boat.append(start + i)
    elif dirn == 3:  # Direction: Down
        for i in range(b):
            boat.append(start + i * 10)
    elif dirn == 4:  # Direction: Left
        for i in range(b):
            boat.append(start - i)
    boat = check_ok(boat, taken)  # Validate boat positions against taken list
    return boat


def create_boats(taken, boats):
    """
    Generate all computer ships by randomly
    selecting starting positions and directions.
    """
    ships = []
    for b in boats:
        boat = [-1]
        while boat[0] == -1:  # Retry until a valid boat configuration is made
            boat_start = randrange(99)
            boat_direction = randrange(1, 5)
            boat = check_boat(b, boat_start, boat_direction, taken)
        ships.append(boat)  # Append each valid boat to the ship list
        taken = taken + boat  # Update taken positions
    return ships, taken


def show_board_c(taken):
    """
    Display the user's board layout, marking ships'
    positions on the grid.
    """
    print("     Battleships (Your Ships on Your Board)")
    print("Your board appears at the bottom after first shot")
    print("     0  1  2  3  4  5  6  7  8  9")
    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            ch = " _ "
            if place in taken:  # Mark positions with ships
                ch = " o "
            row = row + ch
            place = place + 1
        print(x, " ", row)


def get_shot_comp(guesses, tactics):
    """
    Generate a computer shot based on
    remaining tactics or randomly if none left.
    """
    ok = "n"
    while ok == "n":
        try:
            if tactics:
                shot = tactics[0]  # Take next tactic shot if available
            else:
                shot = randrange(99)  # Generate random shot otherwise
            if shot not in guesses:  # Ensure shot hasn't been guessed already
                ok = "y"
                guesses.append(shot)  # Add shot to guesses list
                break
        except Exception:
            print("incorrect entry - please enter again")
    return shot, guesses


def show_board(hit, miss, comp):
    """
    Display the current state of the board
    with hit, miss, and computer's completed ships.
    """
    print("            Battleships")
    print("     0  1  2  3  4  5  6  7  8  9")
    place = 0
    for x in range(10):
        row = ""
        for y in range(10):
            ch = " _ "
            if place in miss:
                ch = " x "  # Mark missed shot
            elif place in hit:
                ch = " o "  # Mark hit
            elif place in comp:
                ch = " O "  # Mark fully destroyed ship
            row = row + ch
            place = place + 1
        print(x, " ", row)


def check_shot(shot, ships, hit, miss, comp):
    """
    Check if a shot hit or missed, update board accordingly,
    and remove positions from ships.
    """
    missed = 0
    for i in range(len(ships)):
        if shot in ships[i]:
            ships[i].remove(shot)
            if len(ships[i]) > 0:
                hit.append(shot)  # Add shot to hits if part of ship remains
                missed = 1
            else:
                comp.append(shot)  # Add shot to comp when ship is destroyed
                missed = 2
    if missed == 0:
        miss.append(shot)  # Add to misses if shot missed all ships
    return ships, hit, miss, comp, missed


def calc_tactics(shot, tactics, guesses, hit):
    """
    Calculate new tactics for computer's
    next shot based on previous successful hit location.
    """
    temp = []
    if not tactics:
        temp = [shot - 1, shot + 1, shot - 10, shot + 10]
    else:
        if shot - 1 in hit:
            temp = [shot + 1]
            for num in [2, 3, 4, 5, 6, 7, 8]:
                if shot - num not in hit:
                    temp.append(shot - num)
                    break
        elif shot + 1 in hit:
            temp = [shot - 1]
            for num in [2, 3, 4, 5, 6, 7, 8]:
                if shot + num not in hit:
                    temp.append(shot + num)
                    break
        if shot - 10 in hit:
            temp = [shot + 10]
            for num in [20, 30, 40, 50, 60, 70, 80]:
                if shot - num not in hit:
                    temp.append(shot - num)
                    break
        elif shot + 10 in hit:
            temp = [shot - 10]
            for num in [20, 30, 40, 50, 60, 70, 80]:
                if shot + num not in hit:
                    temp.append(shot + num)
                    break

    cand = []
    for i in range(len(temp)):
        if temp[i] not in guesses and 0 <= temp[i] < 100:
            cand.append(temp[i])
    random.shuffle(cand)
    return cand


def get_shot(guesses):
    """
    Prompt the player to enter a valid guess,
    ensuring it hasn’t been guessed before.
    """
    ok = "n"
    while ok == "n":
        shot_input = input("please enter your guess: ")
        try:
            shot = int(shot_input)
        except ValueError:
            print("Error: Please enter a valid number.")
            continue
        if shot < 0 or shot > 99:
            print("incorrect number, please try again")
        elif shot in guesses:
            print("incorrect number, used before")
        else:
            ok = "y"
            break
    return shot


def check_if_empty_2(list_of_lists):
    """
    Check if all sublists in a list are
    empty, indicating no ships remain.
    """
    return all(not elem for elem in list_of_lists)


# Lists for tracking the hits, misses, and completed ships for player 1
hit1 = []
miss1 = []
comp1 = []
guesses1 = []
missed1 = 0
tactics1 = []

# Initialize lists for tracking the board setup and gameplay for player 2
taken1 = []
taken2 = []
hit2 = []
miss2 = []
comp2 = []
guesses2 = []
missed2 = 0
tactics2 = []

# Define lengths of ships to be placed on the board
battleships = [5, 4, 3, 3, 2, 2]

# Generate player 1's board with ships placed (computer's ships)
ships1, taken1 = create_boats(taken1, battleships)
# Prompt player 2 to set up their board by choosing ship placements(your ships)
ships2, taken2 = create_ships(taken2, battleships)

# Display your board with initial ship placements
show_board_c(taken2)

# Main game loop runs for a set number of turns or until a player wins
for i in range(80):
    # Track all previous guesses made by player 1
    guesses1 = hit1 + miss1 + comp1

    # Prompt player 1 to take a shot at the computer's board
    shot1 = get_shot(guesses1)
    (ships1, hit1, miss1, comp1,
     missed1) = check_shot(shot1, ships1, hit1, miss1, comp1)
    print("\nComputer Board:")
    show_board(hit1, miss1, comp1)

    # Check if computer has no ships remaining; if true, player 1 wins
    if check_if_empty_2(ships1):
        print("End of game - Congratulations, you won!", i)
        break

    # Generate a shot for the computer against your board
    shot2, guesses2 = get_shot_comp(guesses2, tactics2)
    (ships2, hit2, miss2, comp2,
     missed2) = check_shot(shot2, ships2, hit2, miss2, comp2)
    print("\nYour Board:")
    show_board(hit2, miss2, comp2)

    # If computer hits, calculate new tactics for follow-up shots
    if missed2 == 1:
        tactics2 = calc_tactics(shot2, tactics2, guesses2, hit2)
    elif missed2 == 2:
        tactics2 = []
    elif tactics2:
        tactics2.pop(0)

    # Check if your ships are all destroyed; if true, computer wins
    if check_if_empty_2(ships2):
        print("End of game - computer wins", i)
        break
