import random
import time
from SA import SA
from CSP import CSP


class Main:
    gameDifficulty = "easy"
    board = None
    original_board = None  # Store the original board for statistics
    statistics = {
        'csp_mrv': None,
        'csp_mcv': None,
        'csp_lcv': None,
        'sa': None
    }

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
        cls.board = [row[:] for row in board]  # Create a copy
        cls.original_board = [row[:] for row in board]  # Store original

        # Reset statistics when new board is generated
        cls.statistics = {
            'csp_mrv': None,
            'csp_mcv': None,
            'csp_lcv': None,
            'sa': None
        }

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
        print("=" * 50)
        print("SUDOKU SOLVER - MAIN MENU")
        print("=" * 50)
        print("1. Generate new board")
        print("2. Show current board")
        print("3. Run CSP algorithm")
        print("4. Run SA algorithm")
        print("5. Show statistics")
        print("-1. Exit program")
        print("=" * 50)
        return "Choice: "

    @staticmethod
    def printCSPMenu():
        print("\n" + "=" * 50)
        print("CSP ALGORITHM MENU")
        print("=" * 50)
        print("1. Run CSP with MRV heuristic")
        print("2. Run CSP with MCV heuristic")
        print("3. Run CSP with LCV heuristic")
        print("4. Show CSP statistics")
        print("5. Back to main menu")
        print("=" * 50)
        return "Choice: "

    @classmethod
    def runCSPWithHeuristic(cls, heuristic_name):
        """Run CSP algorithm with specified heuristic"""
        if cls.board is None:
            print("Please generate a board first!")
            return None

        print(f"\nRunning CSP with {heuristic_name} heuristic...")
        print("Starting board:")
        cls.printBoard(cls.board)

        # Create a copy of the board for solving
        board_copy = [row[:] for row in cls.board]

        # Create CSP solver
        solver = CSP(board_copy)

        # Solve with timing
        start_time = time.time()
        solution, stats = solver.solve(heuristic=heuristic_name, visual=False)
        end_time = time.time()

        # Store statistics
        key = f'csp_{heuristic_name.lower()}'
        cls.statistics[key] = {
            'heuristic': heuristic_name,
            'success': stats['success'],
            'time': stats['time'],
            'nodes_explored': stats['nodes_explored'],
            'backtracks': stats['backtracks']
        }

        if solution:
            print("\n✓ Solution found!")
            cls.printBoard(solution)
        else:
            print("\n✗ No solution found!")

        print(f"\nTime taken: {stats['time']:.4f} seconds")
        print(f"Nodes explored: {stats['nodes_explored']}")
        print(f"Backtracks: {stats['backtracks']}")

        return solution

    @classmethod
    def handleCSPMenu(cls):
        """Handle CSP submenu"""
        csp_choice = ""

        while csp_choice != "5":
            csp_choice = input(cls.printCSPMenu())
            print()

            if csp_choice == "1":
                cls.runCSPWithHeuristic("MRV")
            elif csp_choice == "2":
                cls.runCSPWithHeuristic("MCV")
            elif csp_choice == "3":
                cls.runCSPWithHeuristic("LCV")
            elif csp_choice == "4":
                cls.showCSPStatistics()
            elif csp_choice == "5":
                print("Returning to main menu...")
            else:
                print("Invalid choice!")

            if csp_choice != "5":
                input("\nPress Enter to continue...")

    @classmethod
    def showCSPStatistics(cls):
        """Show statistics for CSP algorithms only"""
        print("\n" + "=" * 70)
        print("CSP STATISTICS")
        print("=" * 70)

        if cls.original_board is None:
            print("No board has been generated yet!")
            return

        print("\nOriginal Board:")
        cls.printBoard(cls.original_board)

        # Check if any CSP algorithm has been run
        has_results = any(cls.statistics[key] is not None
                          for key in ['csp_mrv', 'csp_mcv', 'csp_lcv'])

        if not has_results:
            print("No CSP algorithms have been run yet!")
            return

        print("\nResults:")
        print(f"{'Heuristic':<12} {'Success':<10} {'Time (s)':<12} {'Nodes':<12} {'Backtracks':<12}")
        print("-" * 70)

        for key in ['csp_mrv', 'csp_mcv', 'csp_lcv']:
            stats = cls.statistics[key]
            if stats:
                success_str = "✓" if stats['success'] else "✗"
                print(f"{stats['heuristic']:<12} {success_str:<10} "
                      f"{stats['time']:<12.4f} {stats['nodes_explored']:<12} "
                      f"{stats['backtracks']:<12}")
            else:
                heuristic_name = key.split('_')[1].upper()
                print(f"{heuristic_name:<12} {'Not run':<10}")

    @classmethod
    def showAllStatistics(cls):
        """Show statistics for all algorithms"""
        print("\n" + "=" * 70)
        print("ALL ALGORITHMS STATISTICS")
        print("=" * 70)

        if cls.original_board is None:
            print("No board has been generated yet!")
            return

        print("\nOriginal Board:")
        cls.printBoard(cls.original_board)

        # Check if any algorithm has been run
        has_results = any(v is not None for v in cls.statistics.values())

        if not has_results:
            print("No algorithms have been run yet!")
            return

        print("\nResults:")
        print(f"{'Algorithm':<15} {'Success':<10} {'Time (s)':<12} {'Nodes':<12} {'Backtracks':<12}")
        print("-" * 70)

        # CSP results
        for key in ['csp_mrv', 'csp_mcv', 'csp_lcv']:
            stats = cls.statistics[key]
            if stats:
                success_str = "✓" if stats['success'] else "✗"
                algo_name = f"CSP ({stats['heuristic']})"
                print(f"{algo_name:<15} {success_str:<10} "
                      f"{stats['time']:<12.4f} {stats['nodes_explored']:<12} "
                      f"{stats['backtracks']:<12}")

        # SA results
        if cls.statistics['sa']:
            stats = cls.statistics['sa']
            success_str = "✓" if stats['success'] else "✗"
            print(f"{'SA':<15} {success_str:<10} {stats['time']:<12.4f} "
                  f"{stats.get('iterations', 'N/A'):<12} {'N/A':<12}")


if __name__ == '__main__':
    print("=" * 50)
    print("WELCOME TO THE SUDOKU SOLVER PROJECT")
    print("=" * 50)
    print()

    choice = ""

    while choice != "-1":
        choice = input(Main.printMenu())
        print()

        if choice == "1":
            diffChoice = input(Main.printGameDifficulties())
            Main.setGameDifficulty(diffChoice)
            print(f"\nGenerating {Main.getGameDifficulty()} board...")
            Main.generateBoard(Main.getGameDifficulty())
            Main.printBoard()

        elif choice == "2":
            Main.printBoard()

        elif choice == "3":
            if Main.board is None:
                print("Please generate a board first (option 1)")
            else:
                Main.handleCSPMenu()

        elif choice == "4":
            if Main.board is None:
                print("Please generate a board first (option 1)")
            else:
                print("Running SA algorithm...")
                solver = SA(Main.board)
                start_time = time.time()
                solution = solver.solve(visual=True, delay=0.02)
                end_time = time.time()

                # Store SA statistics
                Main.statistics['sa'] = {
                    'success': solution is not None,
                    'time': end_time - start_time,
                    'iterations': getattr(solver, 'iterations', 0)
                }

                print("\nFinal Solution:")
                Main.printBoard(solution)

        elif choice == "5":
            Main.showAllStatistics()

        elif choice == "-1":
            print("Thank you for using the Sudoku Solver!")
            print("Goodbye!")

        else:
            print("Invalid choice!")

        if choice != "-1":
            print()

    print("\nProgram terminated.")