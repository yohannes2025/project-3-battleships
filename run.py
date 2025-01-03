# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Ultimate Battleships Game

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

