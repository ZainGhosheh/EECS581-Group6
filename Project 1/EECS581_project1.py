"""
Name of Program: Battleship!
Description: 2-player, tactical war game that incorporates turn based strategic guessing with intellectual placement for an awesome and fun experience!
Inputs: Opponent's/Player's guesses, Opponent's/Player's ship placements
Outputs: Board w/ Hit and Miss trackers, Sunk ship notification, Current game status and winner
Sources: Group 6 and ChatGPT where marked and explained in the code
Author: Zach Alwin, Kristin Boeckmann, Lisa Phan, Nicholas Hausler, Vinayak Jha
Creation Date: 09/11/2024
"""

# Declare size of board and maximum number of ships
BOARD_SIZE = 10 # 10 by 10 sized board
MAX_SHIP = 5 # Max number of ships on the board for a player's side

# Declare ASCII character 'A', used to generate column labels
A_CHAR = 65

# Generate row labels and column labels
ROWS = [str(i) for i in range(1, BOARD_SIZE + 1)]  # 1 to 10
COLS = [chr(i) for i in range(A_CHAR, BOARD_SIZE + A_CHAR)]  # A to J

# Use characters to describe and empty space and a ship on the board
EMPTY = '.'  # Empty space
SHIP = 'S'  # Ship space

# Utility function to display a board
def display(board):
    print("  " + " ".join(COLS))  # Print headers for column
    for i, row in enumerate(board):
        print(ROWS[i] + " " + " ".join(row))  #Print labels for rows

# Create an empty 10x10 board
def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # List comprehension to create a 10x10 grid initialized with EMPTY

# Convert letter and number to board coordinates
def get_coordinates(pos):
    row = int(pos[1:]) - 1  # Extract row and column from the position string
    col = ord(pos[0].upper()) - A_CHAR  # Convert letter to corresponding index
    return row, col

# Place a ship on the board and return its positions
def place_ship(board, size, orientation, direction, start):
    row, col = get_coordinates(start)  # Fetch starting coordinates
    positions = []  # Stores list of ship positions
    if orientation == 'H':  # Horizontal
        if direction == 'H':  # Right Direction
            for i in range(size): 
                board[row][col + i] = SHIP  # Place ship on the board
                positions.append((row, col + i))  # Store position of ship
        elif direction == 'L':  # Left Direction
            for i in range(size):
                board[row][col - i] = SHIP
                positions.append((row, col - i))
    else:  # Vertical 
        if direction == 'D':  # Downwards
            for i in range(size):
                board[row + i][col] = SHIP
                positions.append((row + i, col))
        elif direction == 'U':  # Upwards
            for i in range(size):
                board[row - i][col] = SHIP
                positions.append((row - i, col))
    return positions  # Return the list of ship's positions

# Check if position is valid for placing the ship
def is_valid_position(pos):
    if len(pos) < 2 or len(pos) > 3:  # Valid position string length
        return False
    if pos[0].upper() not in COLS:  # Valid column letter
        return False
    try:
        row = int(pos[1:])  # Convert row to an integer
        if row < 1 or row > BOARD_SIZE:  # Check if row number is within bounds
            return False
    except ValueError:
        return False
    finally:
        return True  # Return true if all checks passed

# Check if placing ship is valid
def valid_ship_placement(board, size, orientation, direction, start):
    row, col = get_coordinates(start)
    if orientation == 'H':  # Horizontal
        if direction == 'R':  # Right direction
            if col + size > BOARD_SIZE:  # Check if ship fits within bounds of board
                return False  
            return all(board[row][col + i] == EMPTY for i in range(size))  # Check if all cells are empty
        elif direction == 'L':  # Left 
            if col - size + 1 < 0:  # Check bounds for left direction placement
                return False  
            return all(board[row][col - i] == EMPTY for i in range(size))
    else:  # Vertical
        if direction == 'D':  # Downwards
            if row + size > BOARD_SIZE:  # Check for downwards placement
                return False 
            return all(board[row + i][col] == EMPTY for i in range(size))
        elif direction == 'U':  # Upwards
            if row - size + 1 < 0:  # Check for upwards placement
                return False 
            return all(board[row - i][col] == EMPTY for i in range(size))

# Fire at opponent's board
def fire(board, pos, ships):
    row, col = get_coordinates(pos)  # Get target coordinates
    if board[row][col] == SHIP:  # Check if target is a ship
        board[row][col] = "X"  # Mark a hit with an X
        # We used ChatGPT to help with marking ships as sunk. Here's how it works:
        # We check if (row, col) is in the list of positions for each ship.
        # If it is, we remove that position. If the ship's list of positions becomes empty, it means the ship is sunk.
        # We return "hit_and_sunk" with the size of the ship. If not sunk, we just return "hit".
        for ship in ships:
            if (row, col) in ship['positions']:
                ship['positions'].remove((row, col))  # Remove hit position from ship
                if not ship['positions']:  # Ship is sunk
                    return "hit_and_sunk", ship['size']  # Return hit_and_sunk message
        return "hit", None  # Return hit, but not sunk message
    elif board[row][col] == EMPTY:  # Missed shot
        board[row][col] = "O"  # Mark miss with O
        return "miss", None  
    else:
        return "already", None  # Already fired at this position

# Check if all ships are sunk
def all_ships_sunk(ships):
    return all(not ship['positions'] for ship in ships)  # Check if all ships have no position left (all sunk)

# Ship configuration
def ship_sizes(num_ships):
    return list(range(1, num_ships + 1))  # Return a list of ships with range of 1 to the number of ships

def place_ships(board, ship_list):
    ships = []  # List that stores all ships
    for ship_size in ship_list:
        while True:
            print(f"\nPlacing ship of size {ship_size}")
            display(board)
            start = input("Enter start position (e.g., A1): ")  # Receive start position from user

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
                ship_positions = place_ship(board, ship_size, orientation, direction, start)  # Place ship
                ships.append({'size': ship_size, 'positions': ship_positions})  # Add ship to list
                break
            else:
                print("Invalid placement. Try again.")
    return ships  # Return list of ships

def get_num_ships():  # Get number of ships for each player
    while True:
        try:
            num_ships = int(input(f"Enter number of ships per player (1 to {MAX_SHIP}): "))
            if 1 <= num_ships <= MAX_SHIP:
                return num_ships  # Return valid number of current ships
            else:
                print(f"Please enter a number between 1 and {MAX_SHIP}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Main function to run battleship game
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
                    print("Hit!")  # Hit feedback 
                    player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
                    break
                elif result == "hit_and_sunk":
                    print(f"Hit! You sunk a ship of size {sunk_ship_size}!")
                    player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
                    break
                elif result == "miss":
                    print("Miss!")  # Miss feedback
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
