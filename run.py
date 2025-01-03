# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Ultimate Battleships Game

from random import randint

class Board:
    """Handles game logic, including ships, guesses, and board display."""

    def __init__(self, size, num_ships, name, board_type):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]  # 2D board
        self.num_ships = num_ships
        self.name = name
        self.type = board_type  # "player" or "computer"
        self.guesses = []  # List to track guesses
        self.ships = []  # List to track ships

    def print(self, hide_ships=False):
        """Print the board. Optionally hide ships for the computer's board."""
        for row in self.board:
            row_display = ["." if hide_ships and cell == "@" else cell for cell in row]
            print(" ".join(row_display))
        print()


    def guess(self, x, y):
        """Process a guess and return whether it's a hit or miss."""
        if (x, y) in self.guesses:
            print("Already guessed!")
            return "Repeat"
        self.guesses.append((x, y))
        if (x, y) in self.ships:
            self.board[x][y] = "X"  # Mark as hit
            print("It's a HIT!")
            return "Hit"
        else:
            self.board[x][y] = "O"  # Mark as miss
            print("It's a MISS!")
            return "Miss"

    def add_ship(self, x, y):
        """Add a ship to the board at the specified coordinates."""
        if len(self.ships) >= self.num_ships:
            print("Error: Cannot add more ships!")
        elif (x, y) in self.ships:
            print("Error: Ship already placed at this location!")
        else:
            self.ships.append((x, y))
            if self.type == "player":  # Only display ships on the player's board
                self.board[x][y] = "@"

def random_point(size):
    """Helper function to return a random integer between 0 and size."""
    return randint(0, size - 1)

def valid_coordinates(x, y, board):
    """Check if coordinates are valid and not already occupied."""
    valid_range = 0 <= x < board.size and 0 <= y < board.size
    return valid_range and (x, y) not in board.ships

def populate_board(board):
    """Place ships randomly on the board."""
    while len(board.ships) < board.num_ships:
        x, y = random_point(board.size), random_point(board.size)
        if valid_coordinates(x, y, board):
            board.add_ship(x, y)


def make_guess(board):
    """Allow a player or computer to make a guess."""
    if board.type == "player":
        while True:
            try:
                x, y = map(int, input("Enter your guess (row and column): ").split())
                if 0 <= x < board.size and 0 <= y < board.size:
                    return x, y
                else:
                    print("Invalid input. Please try again.")
            except ValueError:
                print("Invalid input. Enter two numbers separated by a space.")
    else:
        while True:
            x, y = random_point(board.size), random_point(board.size)
            if (x, y) not in board.guesses:
                return x, y


def play_game(computer_board, player_board):
    """Alternates turns between player and computer."""
    while len(player_board.ships) > 0 and len(computer_board.ships) > 0:
        # Player's turn
        print("\nYour Board:")
        player_board.print()
        print("Computer's Board:")
        computer_board.print(hide_ships=True)
        print(f"\n{player_board.name}, it's your turn!")
        x, y = make_guess(computer_board)
        result = computer_board.guess(x, y)
        if result == "Hit":
            computer_board.ships.remove((x, y))
        if not computer_board.ships:
            print("You sank all the computer's ships!")
            scores["player"] += 1
            break

        # Computer's turn
        print("\nComputer's turn!")
        x, y = make_guess(player_board)
        result = player_board.guess(x, y)
        if result == "Hit":
            player_board.ships.remove((x, y))
        if not player_board.ships:
            print("The computer sank all your ships!")
            scores["computer"] += 1
            break

    print("\nFinal Scores:")
    print(f"Player: {scores['player']}, Computer: {scores['computer']}")


def new_game():
    """Starts a new game by initializing boards and gameplay."""
    size = 5
    num_ships = 4
    scores["computer"] = 0
    scores["player"] = 0
    print("Welcome to ULTIMATE BATTLESHIPS!!")
    print(f"Board Size: {size}. Number of ships: {num_ships}")
    print("Top left corner is row: 0, col: 0")
    print("_" * 35)
    player_name = input("Please enter your name: \n")
    print("_" * 35)
    computer_board = Board(size, num_ships, "Computer", "computer")
    player_board = Board(size, num_ships, player_name, "player")
    populate_board(player_board)
    populate_board(computer_board)
    play_game(computer_board, player_board)  # Start the game
