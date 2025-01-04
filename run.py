# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Ultimate Battleships Game

from random import randint

# Global variable to keep track of scores
scores = {"computer": 0, "player": 0}

class Board:
    """Handles game logic, including ships, guesses, and board display."""

    def __init__(self, size, num_ships, name, board_type):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.num_ships = num_ships
        self.name = name
        self.type = board_type  # "player" or "computer"
        self.guesses = []  # List to track guesses
        self.ships = []  # List to track ships

    def display(self, hide_ships=False):
        """Print the board. Optionally hide ships for the computer's board."""
        for row in self.board:
            row_display = ["." if hide_ships and cell == "@" else cell for cell in row]
            print(" ".join(row_display))
        print()

    def process_guess(self, x, y):
        """Process a guess and return whether it's a hit, miss, or repeat."""
        if (x, y) in self.guesses:
            print("Already guessed!")
            return "Repeat"

        self.guesses.append((x, y))

        if (x, y) in self.ships:
            self.board[x][y] = "X"  # Mark as hit
            print("It's a HIT!")
            return "Hit"

        self.board[x][y] = "O"  # Mark as miss
        print("It's a MISS!")
        return "Miss"

    def add_ship(self, x, y):
        """Add a ship to the board at the specified coordinates."""
        if len(self.ships) >= self.num_ships:
            raise ValueError("Cannot add more ships!")
        if (x, y) in self.ships:
            raise ValueError("Ship already placed at this location!")

        self.ships.append((x, y))
        if self.type == "player":  # Display ships on player's board
            self.board[x][y] = "@"

# Helper functions
def random_point(size):
    """Return a random integer between 0 and size-1."""
    return randint(0, size - 1)

def valid_coordinates(x, y, board):
    """Check if coordinates are valid and not already occupied."""
    return 0 <= x < board.size and 0 <= y < board.size and (x, y) not in board.ships

def populate_board(board):
    """Place ships randomly on the board."""
    while len(board.ships) < board.num_ships:
        x, y = random_point(board.size), random_point(board.size)
        if valid_coordinates(x, y, board):
            board.add_ship(x, y)

def get_player_guess(board):
    """Get player's guess input."""
    while True:
        try:
            x, y = map(int, input("Enter your guess (row and column): ").split())
            if 0 <= x < board.size and 0 <= y < board.size:
                return x, y
            print("Invalid input. Please enter values within the board's range.")
        except ValueError:
            print("Invalid input. Enter two numbers separated by a space.")

def get_computer_guess(board):
    """Generate a random guess for the computer."""
    while True:
        x, y = random_point(board.size), random_point(board.size)
        if (x, y) not in board.guesses:
            return x, y

def take_turn(board, guess_func):
    """Handle a single turn for either player or computer."""
    x, y = guess_func(board)
    return board.process_guess(x, y)

def play_game(computer_board, player_board):
    """Alternate turns between player and computer until the game ends."""
    while player_board.ships and computer_board.ships:
        # Player's turn
        print("\nYour Board:")
        player_board.display()
        print("Computer's Board:")
        computer_board.display(hide_ships=True)
        print(f"\n{player_board.name}, it's your turn!")
        x, y = get_player_guess(computer_board) 
        if take_turn(computer_board, get_player_guess) == "Hit":
            computer_board.ships.remove((x, y))

        if not computer_board.ships:
            print("You sank all the computer's ships! You win!")
            scores["player"] += 1
            break

        # Computer's turn
        print("\nComputer's turn!")
        if take_turn(player_board, get_computer_guess) == "Hit":
            player_board.ships.pop()

        if not player_board.ships:
            print("The computer sank all your ships! You lose!")
            scores["computer"] += 1
            break

    print("\nFinal Scores:")
    print(f"Player: {scores['player']}, Computer: {scores['computer']}")

def new_game():
    """Initialize and start a new game."""
    size = 5
    num_ships = 4
    scores["computer"] = 0
    scores["player"] = 0

    print("_" * 35)
    print()
    print("Welcome to ULTIMATE BATTLESHIPS!!")
    print(f"Board Size: {size}. Number of ships: {num_ships}")
    print("Top left corner is row: 0, col: 0")
    print("_" * 35)

    player_name = input("Please enter your name: ")
    print("_" * 35)

    computer_board = Board(size, num_ships, "Computer", "computer")
    player_board = Board(size, num_ships, player_name, "player")

    populate_board(player_board)
    populate_board(computer_board)

    play_game(computer_board, player_board)

# Run the game
if __name__ == "__main__":
    new_game()
