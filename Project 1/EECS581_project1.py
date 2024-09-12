BOARD_SIZE = 10
MAX_SHIP = 5

A_CHAR = 65

ROWS = [str(i) for i in range(1, BOARD_SIZE+1)]  # Row labels: 1-10
COLS = [chr(i) for i in range(A_CHAR, BOARD_SIZE + A_CHAR)]  # Column labels: A-J

EMPTY = '.'

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
    col = ord(pos[0].upper()) - 65
    return row, col


# Place ships
def place_ship(board, size, orientation, start):
    row, col = get_coordinates(start)
    if orientation == 'H':  # Horizontal
        for i in range(size):
            board[row][col + i] = "S"
    else:  # Vertical
        for i in range(size):
            board[row + i][col] = "S"


# Check if placing ship is valid
def valid_ship_placement(board, size, orientation, start):
    row, col = get_coordinates(start)
    if orientation == 'H':
        if col + size > BOARD_SIZE:
            return False
        return all(board[row][col + i] == EMPTY for i in range(size))
    else:
        if row + size > BOARD_SIZE:
            return False
        return all(board[row + i][col] == EMPTY for i in range(size))


# Fire at opponent's board
def fire(board, pos):
    row, col = get_coordinates(pos)
    if board[row][col] == "S":
        board[row][col] = "X"  # Hit
        return True
    elif board[row][col] == EMPTY:
        board[row][col] = "O"  # Miss
        return False
    return False  # Already fired at this position


# Check if all ships are sunk
def all_ships_sunk(board):
    for row in board:
        if "S" in row:
            return False
    return True


# Ship configuration
def ship_sizes(num_ships):
    return list(range(1, num_ships + 1))

def place_ships(board, ship_list):
    for ship in ship_list:
        while True:
            print(f"Placing ship of size {ship}")
            display(board)
            start = input("Enter start position (e.g., A1): ")
            orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
            if valid_ship_placement(board, ship, orientation, start):
                place_ship(board, ship, orientation, start)
                break
            else:
                print("Invalid placement. Try again.")   

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
    num_ships = int(input(f"Enter number of ships per player (1 to {MAX_SHIP}): "))
    while num_ships < 1 or num_ships > MAX_SHIP:
        num_ships = int(input(f"Please enter a valid number (1 to {MAX_SHIP}): "))

    ship_list = ship_sizes(num_ships)

    # Player 1's turn
    print("\nPlayer 1, place your ships.")
    place_ships(player1_board, ship_list)

    # Player 2's turn
    print("\nPlayer 2, place your ships.")
    place_ships(player2_board, ship_list)

    player_turn = 1
    while True:
        if player_turn == 1:
            print("\nPlayer 1's turn!")
            display(player1_view)
            pos = input("Enter position to fire (e.g., A1): ")
            if fire(player2_board, pos):
                print("Hit!")
                player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
            else:
                print("Miss!")
                player1_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O"
            if all_ships_sunk(player2_board):
                print("Player 1 wins! All ships sunk.")
                break
            player_turn = 2
        else:
            print("\nPlayer 2's turn!")
            display(player2_view)
            pos = input("Enter position to fire (e.g., A1): ")
            if fire(player1_board, pos):
                print("Hit!")
                player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "X"
            else:
                print("Miss!")
                player2_view[get_coordinates(pos)[0]][get_coordinates(pos)[1]] = "O"
            if all_ships_sunk(player1_board):
                print("Player 2 wins! All ships sunk.")
                break
            player_turn = 1


battleship_game()