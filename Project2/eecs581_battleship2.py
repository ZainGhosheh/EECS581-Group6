"""
Authors: Zain Ghosheh, Abdulahi Mohamed, Olufewa Alonge, Mahgoub Husien
Date: 09-29-2024
Assignment: EECS 581 Project 2
Description: Updated Battleship game with AI player
Inputs: Difficulty
Output: AI player moves
Sources: ChatGpt, StackOverflow, GeeksforGeeks
"""





import random # Import random for random number generation
import re # Import re for regular expressions
import time # Import time for sleep function
import os  # Import os for clearing the terminal

# Constants
BOARD_SIZE = 10 # 10x10 board
MAX_SHIP = 5 # Maximum number of ships
A_CHAR = 65# ASCII value of 'A'
EMPTY = "." # Empty cell
SHIP = "S" # Ship cell
HIT = "X" # Hit cell
MISS = "O" # Miss cell
SPECIAL_SHOT_SIZE = 3 # Size of the special shot

ROWS = [str(i) for i in range(1, BOARD_SIZE + 1)] # Row labels
COLS = [chr(i) for i in range(A_CHAR, BOARD_SIZE + A_CHAR)] # Column labels

# Exception class for validation errors
class ValidationError(Exception): 
    pass

# Utility function to display a board
def display(board):
    print("  " + " ".join(COLS)) # Column labels
    for i, row in enumerate(board): # Display each row
        print(ROWS[i] + " " + " ".join(row)) # Row label and row values

# Create an empty board
def create_board(): 
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)] # Create a 10x10 board with empty cells

# Convert letter and number to board coordinates
def get_coordinates(pos):
    pos = pos.upper() # Convert to uppercase
    row = int(pos[1:]) - 1 # Get the row number
    col = ord(pos[0]) - A_CHAR # Get the column number
    return row, col # Return the row and column

# Place a ship on the board and return its positions
def place_ship(board, size, orientation, direction, start): 
    row, col = get_coordinates(start) # Get the starting position
    positions = [] # List to store ship positions
    if orientation == "H": # Horizontal placement
        if direction == "R": # Right
            for i in range(size): # Place the ship
                board[row][col + i] = SHIP # Mark the cell as a ship
                positions.append((row, col + i)) # Add the position to the list
        elif direction == "L":# Left
            for i in range(size): # Place the ship
                board[row][col - i] = SHIP # Mark the cell as a ship
                positions.append((row, col - i)) # Add the position to the list
    else: # Vertical placement
        if direction == "D": # Down
            for i in range(size): # Place the ship
                board[row + i][col] = SHIP # Mark the cell as a ship
                positions.append((row + i, col)) # Add the position to the list
        elif direction == "U": # Up
            for i in range(size): # Place the ship
                board[row - i][col] = SHIP # Mark the cell as a ship
                positions.append((row - i, col)) # Add the position to the list
    return positions # Return the list of ship positions

# Check if a position is valid for placing a ship
def is_valid_position(pos):
    pos = pos.upper() # Convert to uppercase
    if len(pos) < 2 or len(pos) > 3: # Check the length
        return False # Return False if the length is invalid
    if pos[0] not in COLS: # Check the column
        return False # Return False if the column is invalid
    try: # Check the row
        row = int(pos[1:]) # Convert the row to an integer
        if row < 1 or row > BOARD_SIZE: # Check the row range
            return False  # Return False if the row is out of range
    except ValueError: # Handle invalid row values
        return False # Return False if the row is invalid
    return True # Return True if the position is valid

# Check if placing a ship is valid
def valid_ship_placement(board, size, orientation, direction, start):
    row, col = get_coordinates(start) # Get the starting position
    if orientation == "H": # Horizontal placement
        if direction == "R": # Right
            if col + size > BOARD_SIZE: # Check if the ship goes out of bounds
                return False # Return False if the ship goes out of bounds
            return all(board[row][col + i] == EMPTY for i in range(size)) # Check if the cells are empty
        elif direction == "L": # Left
            if col - size + 1 < 0: # Check if the ship goes out of bounds
                return False # Return False if the ship goes out of bounds
            return all(board[row][col - i] == EMPTY for i in range(size)) # Check if the cells are empty
    else: # Vertical placement
        if direction == "D": # Down
            if row + size > BOARD_SIZE: # Check if the ship goes out of bounds
                return False # Return False if the ship goes out of bounds
            return all(board[row + i][col] == EMPTY for i in range(size))   # Check if the cells are empty
        elif direction == "U": # Up
            if row - size + 1 < 0: # Check if the ship goes out of bounds
                return False # Return False if the ship goes out of bounds
            return all(board[row - i][col] == EMPTY for i in range(size))   # Check if the cells are empty

# Fire at opponent's board
def fire(board, pos, ships): 
    row, col = get_coordinates(pos) # Get the position
    if board[row][col] == SHIP: # Check if the cell is a ship
        board[row][col] = HIT # Mark the cell as hit
        for ship in ships: # Check each ship
            if (row, col) in ship["positions"]: # Check if the position is in the ship
                ship["positions"].remove((row, col)) # Remove the position from the ship
                if not ship["positions"]: # Check if the ship is sunk
                    return "hit_and_sunk", ship["size"] # Return hit and sunk
        return "hit", None # Return hit
    elif board[row][col] == EMPTY: # Check if the cell is empty
        board[row][col] = MISS # Mark the cell as miss
        return "miss", None # Return miss
    else: # Invalid cell
        return "already", None # Return already hit

# Check if all ships are sunk
def all_ships_sunk(ships): 
    return all(not ship["positions"] for ship in ships) # Return True if all ships are sunk

# Ship configuration
def ship_sizes(num_ships):
    return list(range(1, num_ships + 1)) # Return a list of ship sizes

# Place ships on the board
def place_ships(board, ship_list):
    ships = [] # List to store ship information
    for ship_size in ship_list: # Place each ship
        print(f"\nPlacing ship of size {ship_size}")    
        display(board) # Display the board
        while True: # Loop until a valid placement is made
            start = block_till_valid("Enter start position (e.g., A1): ", "Please enter a valid value", POS_RE) # Get the start position
            if ship_size > 1: # Check if the ship size is greater than 1
                orientation = block_till_valid("Enter orientation (H for horizontal, V for vertical): ", "Invalid orientation. Please enter 'H' or 'V'.", r"^H|h|v|V$").upper() # Get the orientation
                if orientation == "H": # Horizontal placement
                    direction = block_till_valid("Enter direction (R for right, L for left): ", "Invalid direction. Please enter 'R' or 'L'.", r"^R|r|L|l$").upper() # Get the direction
                else: # Vertical placement
                    direction = block_till_valid("Enter direction (D for down, U for up): ", "Invalid direction. Please enter 'D' or 'U'.", r"^D|d|U|u$").upper() # Get the direction
            else: # Single cell ship
                orientation = "H" # Default orientation
                direction = "R" # Default direction
            if is_valid_position(start) and valid_ship_placement(board, ship_size, orientation, direction, start): # Check if the placement is valid
                ship_positions = place_ship(board, ship_size, orientation, direction, start) # Place the ship on the board
                ships.append({"size": ship_size, "positions": ship_positions}) # Add the ship information to the list
                break   # Break the loop if the placement is valid
            else:
                print("Invalid input or placement. Try again.") # Display an error message
    return ships # Return the list of ships

# Get the number of ships for each player
def get_num_ships():
    while True: # Loop until a valid number is entered
        try: # Handle invalid input
            num_ships = int(input(f"Enter number of ships per player (1 to {MAX_SHIP}): ")) # Get the number of ships
            if 1 <= num_ships <= MAX_SHIP: 
                return num_ships # Return the number of ships
            else: 
                print(f"Please enter a number between 1 and {MAX_SHIP}.") # Display an error message
        except ValueError:
            print("Invalid input. Please enter a valid number.")   # Display an error message



# Blocks till the user has entered a valid coordinate or special command
def block_till_valid(msg, on_fail, validate_by, opponent_board=None, special_move_used=False):
    while True:
        raw = input(msg)
        # Check for special command to display the opponent's or AI's board for 2 seconds
        if raw.strip().lower() == "show opponent board" and opponent_board and not special_move_used: # Check if the special command is valid
            print("\nOpponent's board:") # Display the opponent's board
            display(opponent_board) # Display the opponent's board
            time.sleep(2)  # Display the board for 2 seconds
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
            print("\nTime's up!") # Display a message
            return "special move used"  # Return a flag indicating the special move was used

        elif raw.strip().lower() == "show opponent board" and special_move_used: # Check if the special move has already been used
            print("You have already used the special move. Please enter a position.") # Display an error message
            continue # Continue the loop

        # Check for special command to display the AI's board for 2 seconds
        if raw.strip().lower() == "show ai board" and opponent_board and not special_move_used: # Check if the special command is valid
            print("\nAI's board:") # Display the AI's board
            display(opponent_board) # Display the AI's board
            time.sleep(2)  # Display the board for 2 seconds
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
            print("\nTime's up!") # Display a message
            return "special move used"  # Return a flag indicating the special move was used

        elif raw.strip().lower() == "show ai board" and special_move_used: # Check if the special move has already been used
            print("You have already used the special move. Please enter a position.") # Display an error message
            continue # Continue the loop

        # Validate normal input for position firing
        try:    
            return validate_input(raw, validate_by) # Validate the input
        except ValidationError:
            print(on_fail) # Display an error message
            continue

POS_RE = r"^([A-J]|[a-j])([1-9]|10)$" # Regular expression for position validation

# Validates user input, so that it matches valid coordinates
def validate_input(value: str, validate_by: str):  
    value = value.upper() # Convert to uppercase
    matches = re.search(validate_by, value) # Check if the input matches the regular expression
    if matches is None: # Check if there is no match
        raise ValidationError() # Raise a validation error
    return value # Return the validated input

# Random firing for easy AI 
def random_fire(board):
    available_positions = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] in [EMPTY, SHIP]] # Get all available positions
    
    if not available_positions:  # Check if the list is empty
        return None  # Return None if there are no available positions left
    
    return random.choice(available_positions) # Return a random available 

# Medium AI - modified to fire orthogonally after a hit and consider both empty and ship positions
def medium_ai(board, hit_positions):
    if hit_positions: # Check if there are hit positions
        last_hit = hit_positions[-1] # Get the last hit position
        row, col = last_hit # Get the last hit position
        potential_targets = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)] # Orthogonal positions around the last hit
        valid_targets = [(r, c) for r, c in potential_targets if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] in [EMPTY, SHIP]] # Check if the target is within bounds and is empty or a ship
        
        if valid_targets:  # Check if there are valid targets available
            return random.choice(valid_targets) # Return a random valid target
    
    return random_fire(board)  # Go back to random firing if no adjacent targets


# Hard AI
def hard_ai(board, player_ships):
    for ship in player_ships: # Check each ship
        if ship['positions']: # Check if the ship is not sunk
            return ship['positions'][0] # Return the first position of the ship
    return random_fire(board) # Go back to random firing if all ships are sunk

# AI places ships randomly
def ai_place_ships(board, ship_list): 
    ships = [] # List to store ship information
    for ship_size in ship_list: # Place each ship
        while True: # Loop until a valid placement is made
            start_row = random.randint(0, BOARD_SIZE - 1) # Get a random row
            start_col = random.randint(0, BOARD_SIZE - 1) # Get a random column
            orientation = random.choice(["H", "V"]) # Get a random orientation
            if orientation == "H": # Horizontal placement
                direction = random.choice(["R", "L"]) # Get a random direction
            else:   # Vertical placement
                direction = random.choice(["D", "U"]) # Get a random direction
            
            start = f"{COLS[start_col]}{ROWS[start_row]}" # Get the start position
            
            if is_valid_position(start) and valid_ship_placement(board, ship_size, orientation, direction, start): # Check if the placement is valid
                ship_positions = place_ship(board, ship_size, orientation, direction, start) # Place the ship on the board
                ships.append({"size": ship_size, "positions": ship_positions}) # Add the ship information to the list
                break # Break the loop if the placement is valid
    return ships # Return the list of ships

# Function for playing against AI
def battleship_game_with_ai(ai_difficulty):
    # Initialize boards
    player1_board = create_board()
    ai_board = create_board()

    # Initialize tracking boards 
    player1_view = create_board()

    num_ships = get_num_ships() # Get the number of ships for the game

    # Track special move usage for the player
    player_special_move_used = False

    # Player 1 ship placement
    print("\nPlayer 1, place your ships.") 
    player1_ships = place_ships(player1_board, ship_sizes(num_ships)) 

    # AI ship placement
    print("\nAI is placing its ships...")
    ai_ships = ai_place_ships(ai_board, ship_sizes(num_ships))

    player_turn = 1  # Start with player 1
    ai_hit_positions = []  # To keep track of AI's hits (useful for medium/hard AI)

    while True:
        if player_turn == 1:
            # Player 1's turn
            print("\n\nPlayer 1's turn!")
            print("\nYour board:")
            display(player1_board)
            print("\nOpponent's board:")
            display(player1_view)

            # Allow special move (viewing the AI's board) only once
            pos = block_till_valid("Enter position to fire (e.g., A1) or type 'show ai board' to view the board for 2 seconds (you lose a turn): ",
                                   "Invalid value, please try again.",
                                   POS_RE,
                                   opponent_board=ai_board,
                                   special_move_used=player_special_move_used)
            
            if pos == "special move used": # Check if the special move was used
                player_special_move_used = True # Set the special move flag to True
            else: # Normal firing
                result, sunk_ship_size = fire(ai_board, pos, ai_ships) # Fire at the AI's board
                if result == "hit": # Check if the result is a hit
                    print("Hit!")   
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X" # Mark the cell as hit
                elif result == "hit_and_sunk": # Check if the result is a hit and sunk
                    print(f"Hit! You sunk a ship of size {sunk_ship_size}!") 
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"   # Mark the cell as hit
                elif result == "miss": # Check if the result is a miss
                    print("Miss!")
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O"  # Mark the cell as miss

            # Check if all AI ships are sunk
            if all_ships_sunk(ai_ships):
                print("Player 1 wins! All AI ships are sunk.")
                break

            input("Press Enter to switch to AI's turn...")
            player_turn = 2  # Switch to AI's turn

        else:
            # AI's turn
            print("\n\nAI's turn!")
            
            # AI difficulty-based firing strategy
            if ai_difficulty == 1:
                row, col = random_fire(player1_board)  # Easy AI just fires randomly
            elif ai_difficulty == 2:
                row, col = medium_ai(player1_board, ai_hit_positions)  # Medium AI has some strategy
            elif ai_difficulty == 3:
                row, col = hard_ai(player1_board, player1_ships)  # Hard AI targets remaining ships directly

            pos = f"{COLS[col]}{ROWS[row]}" # Convert row and column to position
            result, sunk_ship_size = fire(player1_board, pos, player1_ships) # Fire at Player 1's board
            if result == "hit": # Check if the result is a hit
                print(f"AI hit at {pos}!") 
                ai_hit_positions.append((row, col)) # Add the hit position to the list
                player1_board[row][col] = "X" # Mark the cell as hit
            elif result == "hit_and_sunk": # Check if the result is a hit and sunk
                print(f"AI hit and sunk a ship of size {sunk_ship_size} at {pos}!") 
                player1_board[row][col] = "X" # Mark the cell as hit
                ai_hit_positions = []  # Clear hit positions after sinking a ship
            elif result == "miss": # Check if the result is a miss
                print(f"AI missed at {pos}.") 
                player1_board[row][col] = "O" # Mark the cell as miss
 
            # Check if all Player 1 ships are sunk
            if all_ships_sunk(player1_ships): 
                print("AI wins! All Player 1 ships are sunk.") 
                break

            input("Press Enter to switch to Player 1's turn...")
            player_turn = 1  # Switch back to Player 1's turn

# Main function to run Battleship game with mode selection
def battleship_game(): 
    print("Welcome to Battleship!") 
    game_mode = input("Choose game mode: (1) 2-player, (2) vs AI: ") # Get the game mode

    if game_mode == "1": # Check if the game mode is 2 player
        two_player_game()
    elif game_mode == "2": # Check if the game mode is vs AI
        ai_difficulty = int(input("Choose AI difficulty: easy(1), medium(2), hard(3) : "))
        battleship_game_with_ai(ai_difficulty)
    else:
        print("Invalid choice. Please choose 1 or 2.") # Display an error message
        battleship_game()

# Function for 2-player Battleship
def two_player_game():
    # Initialize boards
    player1_board = create_board()
    player2_board = create_board()

    # Initialize tracking boards (what the player can see of the opponent's board)
    player1_view = create_board()
    player2_view = create_board()

    # Get the number of ships for the game
    num_ships = get_num_ships()

    # Track special move usage for each player
    player1_special_move_used = False
    player2_special_move_used = False

    # Player 1 ship placement
    print("\nPlayer 1, place your ships.")
    player1_ships = place_ships(player1_board, ship_sizes(num_ships))

    # Player 2 ship placement
    print("\nPlayer 2, place your ships.")
    player2_ships = place_ships(player2_board, ship_sizes(num_ships))

    player_turn = 1  # Start with player 1

    while True: # Main game loop
        if player_turn == 1: # Player 1's turn
            print("\n\nPlayer 1's turn!") 
            print("\nYour board:")
            display(player1_board) # Display Player 1's board
            print("\nOpponent's board:")
            display(player1_view)
            
            # Allow special move (viewing the opponent's board) only once
            pos = block_till_valid("Enter position to fire (e.g., A1) or type 'show opponent board' to view the board for 2 seconds: ",
                                   "Invalid value, please try again.",
                                   POS_RE,
                                   opponent_board=player2_board,
                                   special_move_used=player1_special_move_used)
            
            if pos == "special move used": # Check if the special move was used
                player1_special_move_used = True # Set the special move flag to True
            else: # Normal firing
                result, sunk_ship_size = fire(player2_board, pos, player2_ships) # Fire at Player 2's board
                if result == "hit": # Check if the result is a hit
                    print("Hit!")
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X" # Mark the cell as hit
                elif result == "hit_and_sunk": # Check if the result is a hit and sunk
                    print(f"Hit! You sunk a ship of size {sunk_ship_size}!") 
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X" # Mark the cell as hit
                elif result == "miss": # Check if the result is a miss
                    print("Miss!")
                    player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O" # Mark the cell as miss

            # Check if all ships are sunk
            if all_ships_sunk(player2_ships): 
                print("Player 1 wins! All ships sunk.") 
                break

            input("Press Enter to switch to Player 2's turn...") 
            player_turn = 2  # Switch to Player 2

        else:
            print("\n\nPlayer 2's turn!") # Player 2's turn
            print("\nYour board:") 
            display(player2_board) # Display Player 2's board
            print("\nOpponent's board:")
            display(player2_view) # Display Player 2's view of Player 1's board
            
            # Allow special move (viewing the opponent's board) only once
            pos = block_till_valid("Enter position to fire (e.g., A1) or type 'show opponent board' to view the board for 2 seconds: ",
                                   "Invalid value, please try again.",
                                   POS_RE,
                                   opponent_board=player1_board,
                                   special_move_used=player2_special_move_used)

            if pos == "special move used": # Check if the special move was used
                player2_special_move_used = True # Set the special move flag to True
            else: 
                result, sunk_ship_size = fire(player1_board, pos, player1_ships) # Fire at Player 1's board
                if result == "hit": # Check if the result is a hit
                    print("Hit!")
                    player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X" # Mark the cell as hit
                elif result == "hit_and_sunk": # Check if the result is a hit and sunk
                    print(f"Hit! You sunk a ship of size {sunk_ship_size}!")
                    player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X" # Mark the cell as hit
                elif result == "miss": # Check if the result is a miss
                    print("Miss!")
                    player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O" # Mark the cell as miss

            # Check if all ships are sunk
            if all_ships_sunk(player1_ships):
                print("Player 2 wins! All ships sunk.")
                break

            input("Press Enter to switch to Player 1's turn...")
            player_turn = 1  # Switch to Player 1's turn


# Run the game
battleship_game()
