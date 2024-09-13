"""
Name of Program: Battleship!
Description: 2-player, tactical war game that incorporates turn based strategic guessing with intellectual placement for an awesome and fun experience!
Inputs: Opponent's/Player's guesses, Opponent's/Player's ship placements
Outputs: Board w/ Hit and Miss trackers, Sunk ship notification, Current game status and winner
Sources: Group 6 and ChatGPT where marked and explained in the code
Author: Zach Alwin, Kristin Boeckmann, Lisa Phan, Nicholas Hausler, Vinayak Jha
Creation Date: 09/11/2024
"""

BOARD_SIZE = 10
MAX_SHIP = 5

A_CHAR = 65

ROWS = [str(i) for i in range(1, BOARD_SIZE + 1)]  
COLS = [chr(i) for i in range(A_CHAR, BOARD_SIZE + A_CHAR)] 

EMPTY = '.'
SHIP = 'S'

# Utility function to display a board
def display(board):
    print("  " + " ".join(COLS))
    for i, row in enumerate(board):
        print(ROWS[i] + " " + " ".join(row))

# Create an empty 10x10 board
def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Convert letter and number to board coordinates
def get_coordinates(pos):
    row = int(pos[1:]) - 1
    col = ord(pos[0].upper()) - A_CHAR
    return row, col

# Place a ship on the board and return its positions
def place_ship(board, size, orientation, direction, start):
    row, col = get_coordinates(start)
    positions = []
    if orientation == 'H':
        if direction == 'H':
            for i in range(size):
                board[row][col + i] = SHIP
                positions.append((row, col + i))
        elif direction == 'L':
            for i in range(size):
                board[row][col - i] = SHIP
                positions.append((row, col - i))
    else:
        if direction == 'D':
            for i in range(size):
                board[row + i][col] = SHIP
                positions.append((row + i, col))
        elif direction == 'U':
            for i in range(size):
                board[row - i][col] = SHIP
                positions.append((row - i, col))
    return positions

# Check if position is valid for placing the ship
def is_valid_position(pos):
    if len(pos) < 2 or len(pos) > 3:
        return False
    if pos[0].upper() not in COLS:
        return False
    try:
        row = int(pos[1:])
        if row < 1 or row > BOARD_SIZE:
            return False
    except ValueError:
        return False
    finally:
        return True

# Check if placing ship is valid
def valid_ship_placement(board, size, orientation, direction, start):
    row, col = get_coordinates(start)
    if orientation == 'H':
        if direction == 'R':
            if col + size > BOARD_SIZE:
                return False  
            return all(board[row][col + i] == EMPTY for i in range(size))
        elif direction == 'L':
            if col - size + 1 < 0:
                return False  
            return all(board[row][col - i] == EMPTY for i in range(size))
    else:
        if direction == 'D':
            if row + size > BOARD_SIZE:
                return False 
            return all(board[row + i][col] == EMPTY for i in range(size))
        elif direction == 'U':
            if row - size + 1 < 0:
                return False 
            return all(board[row - i][col] == EMPTY for i in range(size))

# Fire at opponent's board
def fire(board, pos, ships):
    row, col = get_coordinates(pos)
    if board[row][col] == SHIP:
        board[row][col] = "X" 
        # We used ChatGPT to help with marking ships as sunk. Here's how it works:
        # We check if (row, col) is in the list of positions for each ship.
        # If it is, we remove that position. If the ship's list of positions becomes empty, it means the ship is sunk.
        # We return "hit_and_sunk" with the size of the ship. If not sunk, we just return "hit".
        for ship in ships:
            if (row, col) in ship['positions']:
                ship['positions'].remove((row, col))
                if not ship['positions']:  # Ship is sunk
                    return "hit_and_sunk", ship['size']
        return "hit", None
    elif board[row][col] == EMPTY:
        board[row][col] = "O" 
        return "miss", None
    else:
        return "already", None  # Already fired at this position

# Check if all ships are sunk
def all_ships_sunk(ships):
    return all(not ship['positions'] for ship in ships)

# Ship configuration
def ship_sizes(num_ships):
    return list(range(1, num_ships + 1))

def place_ships(board, ship_list):
    ships = []
    for ship_size in ship_list:
        while True:
            print(f"\nPlacing ship of size {ship_size}")
            display(board)
            start = input("Enter start position (e.g., A1): ")

            #If the ship size is 1, there's no need to ask for orientation and direction
            if ship_size <= 1:
                orientation = 'H'
                direction = 'R'
            else:
                orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
                direction = input("Enter direction (R for right, L for left, D for down, U for up): ").upper()

            if not is_valid_position(start) or orientation not in ['H', 'V'] or direction not in ['R', 'L', 'D', 'U']:
                print("Invalid input. Try again.")
                continue
            if valid_ship_placement(board, ship_size, orientation, direction, start):
                ship_positions = place_ship(board, ship_size, orientation, direction, start)
                ships.append({'size': ship_size, 'positions': ship_positions})
                break
            else:
                print("Invalid placement. Try again.")
    return ships

def get_num_ships():
    while True:
        try:
            num_ships = int(input(f"Enter number of ships per player (1 to {MAX_SHIP}): "))
            if 1 <= num_ships <= MAX_SHIP:
                return num_ships
            else:
                print(f"Please enter a number between 1 and {MAX_SHIP}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def battleship_game():
    # Initialize player boards
    player1_board = create_board()
    player2_board = create_board()

    # Initialize player tracking boards (for hits/misses)
    player1_view = create_board()
    player2_view = create_board()

    # Ship placement
    print("Welcome to Battleship!")

    # Get the number of ships
    num_ships = get_num_ships()

    ship_list = ship_sizes(num_ships)

    # Player 1's turn
    print("\nPlayer 1, place your ships.")
    player1_ships = place_ships(player1_board, ship_list)

    # Player 2's turn
    print("\nPlayer 2, place your ships.")
    player2_ships = place_ships(player2_board, ship_list)

    player_turn = 1
    while True:
        if player_turn == 1:
            print("\n\n\n\n\nPlayer 1's turn!")
            print("\nYour board:")
            display(player1_board)  # Show Player 1's board with their ships
            print("\nOpponent's board:")
            display(player1_view)  # Show Player 1's view of Player 2's board
            while True:
                pos = input("Enter position to fire (e.g., A1): ")
                result, sunk_ship_size = fire(player2_board, pos, player2_ships)
                if result == "hit":
                    print("Hit!")
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
                    break
                elif result == "hit_and_sunk":
                    print(f"Hit! You sunk a ship of size {sunk_ship_size}!")
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
                    break
                elif result == "miss":
                    print("Miss!")
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O"
                    break
                else:
                    print("You've already fired at that position. Choose a different spot.")
            if all_ships_sunk(player2_ships):
                print("Player 1 wins! All ships sunk.")
                break
            input("Press Enter to switch to Player 2's turn...")
            player_turn = 2
        else:
            print("\n\n\n\n\nPlayer 2's turn!")
            print("\nYour board:")
            display(player2_board)  # Show Player 2's board with their ships
            print("\nOpponent's board:")
            display(player2_view)  # Show Player 2's view of Player 1's board
            while True:
                pos = input("Enter position to fire (e.g., A1): ")
                result, sunk_ship_size = fire(player1_board, pos, player1_ships)
                if result == "hit":
                    print("Hit!")
                    player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
                    break
                elif result == "hit_and_sunk":
                    print(f"Hit! You sunk a ship of size {sunk_ship_size}!")
                    player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
                    break
                elif result == "miss":
                    print("Miss!")
                    player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O"
                    break
                else:
                    print("You've already fired at that position. Choose a different spot.")
            if all_ships_sunk(player1_ships):
                print("Player 2 wins! All ships sunk.")
                break
            input("Press Enter to switch to Player 1's turn...")
            player_turn = 1

battleship_game()
