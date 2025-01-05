# Ultimate Battleships Game

from random import randint

# Global variable to keep track of scores
scores = {"computer": 0, "player": 0}


class Board:
    """Handles game logic, including ships, guesses, and board display."""

    def __init__(self, BOARD_SIZE, num_ships, name, board_type):
        self.BOARD_SIZE = BOARD_SIZE
        self.board = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.num_ships = num_ships
        self.name = name
        self.type = board_type  # "player" or "computer"
        self.guesses = []  # List to track guesses
        self.ships = []  # List to track ships

    def display(self, hide_ships=False):
        """Print the board. Optionally hide ships for the computer's board."""
        for row in self.board:
            row_display = [
                "." if hide_ships and cell == "@" else cell for cell in row
            ]
            print(" ".join(row_display))
        print()

    def process_guess(self, x, y):
        """Process a guess and return whether it's a hit, miss, or repeat."""
        if (x, y) in self.guesses:
            print("You Already guessed! You can not guess the same coordinate more than once")
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
def random_point(BOARD_SIZE):
    """Return a random integer between 0 and BOARD_SIZE-1."""
    return randint(0, BOARD_SIZE - 1)


def valid_coordinates(x, y, board):
    """Check if coordinates are valid and not already occupied."""
    return (
        0 <= x < board.BOARD_SIZE and
        0 <= y < board.BOARD_SIZE and
        (x, y) not in board.ships
    )


def populate_board(board):
    """Place ships randomly on the board."""
    while len(board.ships) < board.num_ships:
        x, y = random_point(board.BOARD_SIZE), random_point(board.BOARD_SIZE)
        if valid_coordinates(x, y, board):
            board.add_ship(x, y)


def get_player_guess(board):
    """Get player's guess input."""
    while True:
        try:
            x, y = map(
                int,
                input("Enter your guess as 'row column' (e.g., 1 2): ").split()
            )

            if 0 <= x < board.BOARD_SIZE and 0 <= y < board.BOARD_SIZE:
                return x, y
            print("Invalid input. Please enter values within the board's range.")

        except ValueError:
            print(f"Invalid input. Plese enter two numbers separated by a space.")


def get_computer_guess(board):
    """Generate a random guess for the computer."""
    while True:
        x, y = random_point(board.BOARD_SIZE), random_point(board.BOARD_SIZE)
        if (x, y) not in board.guesses:
            return x, y


def take_turn(board, guess_func):
    """Handle a single turn for either player or computer."""
    x, y = guess_func(board)
    return board.process_guess(x, y)


def play_game(computer_board, player_board):

    """Alternate turns between player and computer until the game ends."""

    round_num = 0  # Track round number



    while player_board.ships and computer_board.ships:

        round_num += 1

        print(f"\nRound {round_num}")

        print("\nYour Board (with ships):")

        player_board.display()

        print("Computer's Board:")

        computer_board.display(hide_ships=True)



        # Player's turn

        print(f"\n{player_board.name}, it's your turn!")

        while True:

            player_x, player_y = get_player_guess(computer_board)

            player_result = take_turn(computer_board, lambda b: (player_x, player_y))

            if player_result != "Repeat":  # Allow the game to proceed if the guess is valid

                break

            print("Please try again with a new coordinate.")

        if player_result == "Hit":

            computer_board.ships.remove((player_x, player_y))
            scores["player"] += 1  # Increment player score for a hit

        # Check if the game ends after the player's turn

        if not computer_board.ships:

            print("You sank all the computer's ships! You win!")

            scores["player"] += 1

            break


        # Computer's turn

        print("\nComputer's turn!")

        computer_x, computer_y = get_computer_guess(player_board)

        computer_result = take_turn(player_board, lambda b: (computer_x, computer_y))

        if computer_result == "Hit":

            player_board.ships.remove((computer_x, computer_y))
            scores["computer"] += 1  # Increment computer score for a hit



        # Round Summary

        print("\nSummary:")

        print(f"Player guessed: ({player_x}, {player_y})")

        print(f"Player {('hit a ship!' if player_result == 'Hit' else 'missed this time.')}")

        print(f"Computer guessed: ({computer_x}, {computer_y})")

        print(f"Computer {('hit a ship!' if computer_result == 'Hit' else 'missed this time.')}")

        print("_" * 35)



        # Scores after each round

        print(f"After round {round_num}, the scores are:")

        print(f"{player_board.name}: {scores['player']} \tComputer: {scores['computer']}")

        print("_" * 35)



        # Check for end of game

        if not computer_board.ships:

            print("You sank all the computer's ships! You win!")

            scores["player"] += 1

            break



        if not player_board.ships:

            print("The computer sank all your ships! You lose!")

            scores["computer"] += 1

            break



    print("\nFinal Scores:")

    print(f"{player_board.name}: {scores['player']}, Computer: {scores['computer']}")


def new_game():
    """Initialize and start a new game."""
    BOARD_SIZE = int(input("Enter BOARD_SIZE: "))
    # User-defined ship count
    num_ships = int(input("Enter the number of ships: "))
    # Reset scores for a new game
    scores["computer"] = 0
    scores["player"] = 0

    print("_" * 35)
    print()
    print("Welcome to ULTIMATE BATTLESHIPS!!")
    print(f"Board Size: {BOARD_SIZE}. Number of ships: {num_ships}")
    print("Top left corner is row: 0, col: 0")
    print("_" * 35)

    player_name = input("Please enter your name: ")
    print("_" * 35)

    computer_board = Board(BOARD_SIZE, num_ships, "Computer", "computer")
    player_board = Board(BOARD_SIZE, num_ships, player_name, "player")

    populate_board(player_board)
    populate_board(computer_board)

    play_game(computer_board, player_board)


# Run the game
if __name__ == "__main__":
    new_game()
