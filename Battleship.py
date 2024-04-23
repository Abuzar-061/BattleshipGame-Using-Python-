import random

# Constants
EMPTY = ' ' # Represents an empty cell on the board
SHIP = 'S'  # Represents a ship on the board
HIT = 'X' # Represents a hit on a ship
MISS = 'O' # Represents a miss on the board
BOARD_SIZE = 10 # Size of the game board (4x4)
SHIP_TYPES = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}

def create_board():
    return [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def display_board(board):
    print("  ", " ".join(str(i) for i in range(BOARD_SIZE)))
    for i in range(BOARD_SIZE):
        print(i, " ".join(board[i]))

def place_ship(board, ship, start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos

    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if board[x1][y] != EMPTY:
                return False
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if board[x][y1] != EMPTY:
                return False
    else:
        return False

    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            board[x1][y] = SHIP
    else:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            board[x][y1] = SHIP
    return True

def valid_coordinates(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def register_shot(board, x, y):
    if not valid_coordinates(x, y):
        return False, "Out of range"
    elif board[x][y] == HIT or board[x][y] == MISS:
        return False, "Already fired at this position"
    elif board[x][y] == SHIP:
        board[x][y] = HIT
        return True, "Hit!"
    else:
        board[x][y] = MISS
        return True, "Miss"

def place_all_ships(board):
    for ship, length in SHIP_TYPES.items():
        placed = False
        while not placed:
            start_x = random.randint(0, BOARD_SIZE - 1)
            start_y = random.randint(0, BOARD_SIZE - 1)
            orientation = random.choice(['horizontal', 'vertical'])
            end_x, end_y = start_x, start_y
            if orientation == 'horizontal':
                end_y += length - 1
            else:
                end_x += length - 1
            
            if valid_coordinates(end_x, end_y) and place_ship(board, ship, (start_x, start_y), (end_x, end_y)):
                placed = True

def check_win_condition(board):
    for row in board:
        if SHIP in row:
            return False
    return True

def run_game():
    player_boards = [create_board(), create_board()]
    for i in range(2):
        print(f"Player {i+1}, prepare to place your fleet.")
        display_board(player_boards[i])
        place_all_ships(player_boards[i])
    print("Game begins!")
    current_player = 0
    while True:
        print(f"Player {current_player + 1}'s turn:")
        display_board(player_boards[current_player])
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        success, message = register_shot(player_boards[1 - current_player], x, y)
        print(message)
        if check_win_condition(player_boards[1 - current_player]):
            print(f"Player {current_player + 1} wins!")
            break
        current_player = 1 - current_player

if __name__ == '__main__':
    run_game()
