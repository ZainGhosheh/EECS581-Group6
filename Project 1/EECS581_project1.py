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
BOARD_SIZE = 10  # Set the board size to 10x10 grid
MAX_SHIP = 5  # Define the maximum number of ships allowed for each player

# Declare ASCII character 'A', used to generate column labels
A_CHAR = 65  # ASCII value for character 'A' used to label the columns

# Generate row labels and column labels
ROWS = [str(i) for i in range(1, BOARD_SIZE + 1)]  # Create a list of row labels from 1 to 10
COLS = [chr(i) for i in range(A_CHAR, BOARD_SIZE + A_CHAR)]  # Create a list of column labels from 'A' to 'J'

# Use characters to describe empty space and a ship on the board
EMPTY = '.'  # Character to represent an empty space on the board
SHIP = 'S'  # Character to represent a ship's location on the board

# Utility function to display a board
def display(board):
    # Print the column headers, joining the COLS list with spaces
    print("  " + " ".join(COLS))  
    # Print the row labels and each corresponding row of the board
    for i, row in enumerate(board):
        print(ROWS[i] + " " + " ".join(row))  

# Create an empty 10x10 board
def create_board():
    # Use list comprehension to create a 10x10 grid filled with EMPTY characters
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  

# Convert letter and number to board coordinates
def get_coordinates(pos):
    # Extract row number from the input position (e.g., A1 -> 0) by converting to 0-based index
    row = int(pos[1:]) - 1  
    # Convert the column letter (e.g., 'A') to its corresponding index (0 for 'A', 1 for 'B', etc.)
    col = ord(pos[0].upper()) - A_CHAR  
    return row, col  # Return the calculated row and column indices

# Place a ship on the board and return its positions
def place_ship(board, size, orientation, direction, start):
    # Get the starting row and column coordinates
    row, col = get_coordinates(start)  
    positions = []  # List to store the positions of the placed ship
    if orientation == 'H':  # If the ship is placed horizontally
        if direction == 'H':  # If the direction is towards the right
            for i in range(size): 
                board[row][col + i] = SHIP  # Place ship at each successive column
                positions.append((row, col + i))  # Store the position in the list
        elif direction == 'L':  # If the direction is towards the left
            for i in range(size):
                board[row][col - i] = SHIP  # Place ship at each successive column in reverse
                positions.append((row, col - i))
    else:  # If the ship is placed vertically
        if direction == 'D':  # If the direction is downwards
            for i in range(size):
                board[row + i][col] = SHIP  # Place ship at each successive row
                positions.append((row + i, col))
        elif direction == 'U':  # If the direction is upwards
            for i in range(size):
                board[row - i][col] = SHIP  # Place ship at each successive row in reverse
                positions.append((row - i, col))
    return positions  # Return the list of ship's positions

# Check if a given position is valid for placing a ship
def is_valid_position(pos):
    if len(pos) < 2 or len(pos) > 3:  # Position should be of the form A1 or B10 (length of 2 or 3)
        return False
    if pos[0].upper() not in COLS:  # Column letter should be valid (A-J)
        return False
    try:
        row = int(pos[1:])  # Convert the row part to an integer
        if row < 1 or row > BOARD_SIZE:  # Row should be within valid range (1 to BOARD_SIZE)
            return False
    except ValueError:
        return False
    finally:
        return True  # If all checks pass, return True

# Check if placing a ship is valid
def valid_ship_placement(board, size, orientation, direction, start):
    # Get the starting coordinates of the ship
    row, col = get_coordinates(start)
    if orientation == 'H':  # If the orientation is horizontal
        if direction == 'R':  # If the direction is to the right
            if col + size > BOARD_SIZE:  # Check if the ship will fit within the board horizontally
                return False  
            return all(board[row][col + i] == EMPTY for i in range(size))  # Ensure all spaces are empty
        elif direction == 'L':  # If the direction is to the left
            if col - size + 1 < 0:  # Check if the ship will fit within the board going left
                return False  
            return all(board[row][col - i] == EMPTY for i in range(size))  # Ensure all spaces are empty
    else:  # If the orientation is vertical
        if direction == 'D':  # If the direction is downwards
            if row + size > BOARD_SIZE:  # Check if the ship will fit within the board vertically
                return False 
            return all(board[row + i][col] == EMPTY for i in range(size))  # Ensure all spaces are empty
        elif direction == 'U':  # If the direction is upwards
            if row - size + 1 < 0:  # Check if the ship will fit within the board going upwards
                return False 
            return all(board[row - i][col] == EMPTY for i in range(size))  # Ensure all spaces are empty

# Fire at opponent's board
def fire(board, pos, ships):
    # Get the target coordinates to fire at
    row, col = get_coordinates(pos)  
    if board[row][col] == SHIP:  # If the position contains a ship
        board[row][col] = "X"  # Mark the hit with an 'X'
        for ship in ships:  # Iterate through each ship
            if (row, col) in ship['positions']:  # Check if the fired position belongs to the ship
                ship['positions'].remove((row, col))  # Remove the position from the ship
                if not ship['positions']:  # If the ship has no more positions, it is sunk
                    return "hit_and_sunk", ship['size']  # Return hit and sunk status
        return "hit", None  # Return hit status if not sunk
    elif board[row][col] == EMPTY:  # If the position is empty (miss)
        board[row][col] = "O"  # Mark the miss with an 'O'
        return "miss", None  
    else:
        return "already", None  # If the position has already been fired at

# Check if all ships are sunk
def all_ships_sunk(ships):
    # Return True if all ships have no remaining positions (i.e., all are sunk)
    return all(not ship['positions'] for ship in ships)

# Ship configuration
def ship_sizes(num_ships):
    # Return a list of ship sizes from 1 to the number of ships
    return list(range(1, num_ships + 1))

# Place ships on the board
def place_ships(board, ship_list):
    ships = []  # List to store ships
    for ship_size in ship_list:  # For each ship size
        while True:
            print(f"\nPlacing ship of size {ship_size}")
            display(board)  # Display the current board state
            start = input("Enter start position (e.g., A1): ")  # Get starting position input
            if ship_size <= 1:  # If the ship size is 1, automatically set orientation and direction
                orientation = 'H'
                direction = 'R'
            else:
                orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
                direction = input("Enter direction (R for right, L for left, D for down, U for up): ").upper()
            if not is_valid_position(start) or orientation not in ['H', 'V'] or direction not in ['R', 'L', 'D', 'U']:
                print("Invalid input. Try again.")  # Handle invalid input
                continue
            if valid_ship_placement(board, ship_size, orientation, direction, start):
                ship_positions = place_ship(board, ship_size, orientation, direction, start)  # Place the ship
                ships.append({'size': ship_size, 'positions': ship_positions})  # Add the ship to the list
                break
            else:
                print("Invalid placement. Try again.")  # Handle invalid placement
    return ships  # Return the list of ships

# Get the number of ships for each player
def get_num_ships():
    while True:
        try:
            # Ask for a number of ships between 1 and MAX_SHIP
            num_ships = int(input(f"Enter number of ships per player (1 to {MAX_SHIP}): "))
            if 1 <= num_ships <=
