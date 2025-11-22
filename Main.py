import random


class Main:
    gameDifficulty = "easy"
    board = None

    @classmethod
    def generateBoard(cls, gameDifficulty):
        # Step 1: Generate a complete solved board using brute force
        board = [[0] * 9 for _ in range(9)]
        cls._bruteForceFill(board)

        # Step 2: Remove numbers based on difficulty
        if gameDifficulty == "easy":
            cells_to_remove = 35  # ~46 clues remain
        elif gameDifficulty == "medium":
            cells_to_remove = 45  # ~36 clues remain
        else:  # hard
            cells_to_remove = 55  # ~26 clues remain

        cls._removeNumbers(board, cells_to_remove)
        cls.board = board
        return board

    @classmethod
    def _bruteForceFill(cls, board):
        """
        Brute force approach:
        1. Find an empty cell
        2. Try numbers 1-9 randomly
        3. If valid, place it and move to next cell
        4. If stuck, backtrack and try different number
        """
        # Find the next empty cell
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    # Try numbers 1-9 in random order
                    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    random.shuffle(numbers)

                    for num in numbers:
                        # Check if this number is valid here
                        if cls._isValidPlacement(board, row, col, num):
                            board[row][col] = num

                            # Recursively try to fill the rest
                            if cls._bruteForceFill(board):
                                return True

                            # If it didn't work, reset and try next number
                            board[row][col] = 0

                    # No number worked, need to backtrack
                    return False

        # No empty cells left, board is complete
        return True

    @classmethod
    def _isValidPlacement(cls, board, row, col, num):
        """Check if placing num at (row, col) is valid"""
        # Check row - no duplicate in same row
        for j in range(9):
            if board[row][j] == num:
                return False

        # Check column - no duplicate in same column
        for i in range(9):
            if board[i][col] == num:
                return False

        # Check 3x3 box - no duplicate in same box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False

        return True

    @classmethod
    def _removeNumbers(cls, board, count):
        """Remove random numbers from the board"""
        # Get all cell positions
        cells = []
        for i in range(9):
            for j in range(9):
                cells.append((i, j))

        # Shuffle to remove randomly
        random.shuffle(cells)

        # Remove cells one by one
        removed = 0
        for row, col in cells:
            if removed >= count:
                break
            board[row][col] = 0
            removed += 1

    @classmethod
    def printBoard(cls, board=None):
        """Pretty print the Sudoku board"""
        if board is None:
            board = cls.board
        if board is None:
            print("No board generated yet!")
            return

        print()
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")

            row_str = ""
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "

                val = board[i][j]
                if val == 0:
                    row_str += ". "
                else:
                    row_str += str(val) + " "

            print(row_str)
        print()

    @classmethod
    def setGameDifficulty(cls, difficulty):
        if difficulty == '1':
            cls.gameDifficulty = "easy"
        elif difficulty == '2':
            cls.gameDifficulty = "medium"
        elif difficulty == '3':
            cls.gameDifficulty = "hard"

    @classmethod
    def getGameDifficulty(cls):
        return cls.gameDifficulty

    @staticmethod
    def printGameDifficulties():
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        return "Choice: "

    @staticmethod
    def printMenu():
        print("Choose an option:")
        print("1. Choose difficulty")
        print("2. Generate new board")
        print("3. Show current board")
        print("4. Run algorithm")
        print("Press -1 to exit the program")
        return "Choice: "

    @staticmethod
    def printAlgorithmChoices():
        print("Choose an algorithm:")
        print("1. CSP (Constraint Satisfaction Problem)")
        print("2. SA (Simulated Annealing)")
        return "Choice: "


if __name__ == '__main__':
    print("Hello to The Sudoku Solver Project")
    print()
    choice = ""

    while choice != "-1":
        choice = input(Main.printMenu())
        print()

        if choice == "1":
            diffChoice = input(Main.printGameDifficulties())
            Main.setGameDifficulty(diffChoice)
            print(f"Difficulty set to: {Main.getGameDifficulty()}")

        elif choice == "2":
            print(f"Generating {Main.getGameDifficulty()} board...")
            Main.generateBoard(Main.getGameDifficulty())
            Main.printBoard()

        elif choice == "3":
            Main.printBoard()

        elif choice == "4":
            if Main.board is None:
                print("Please generate a board first (option 2)")
            else:
                algoChoice = input(Main.printAlgorithmChoices())
                if algoChoice == "1":
                    print("Running CSP algorithm...")

                    # TODO: Call CSP class here
                    # CSP.solve(Main.board)
                elif algoChoice == "2":
                    print("Running SA algorithm...")
                    # TODO: Call SA class here
                    # SA.solve(Main.board)
                else:
                    print("Invalid choice")

        print()