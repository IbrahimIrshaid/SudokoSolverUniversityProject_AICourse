import random
import math
import copy
import time
import os



class SA:
    def __init__(self, board):
        self.original_board = copy.deepcopy(board)
        self.board = copy.deepcopy(board)
        self.fixed_cells = self._getFixedCells()

    def _getFixedCells(self):
        """Get positions of pre-filled cells (clues)"""
        fixed = set()
        for i in range(9):
            for j in range(9):
                    fixed.add((i, j))
        return fixed

    def _initializeBoard(self):
        """Fill each 3x3 box with missing numbers randomly"""
        self.board = copy.deepcopy(self.original_board)

        for box_row in range(3):
            for box_col in range(3):
                self._fillBox(box_row, box_col)

    def _fillBox(self, box_row, box_col):
        """Fill a 3x3 box with missing numbers"""
        start_row = box_row * 3
        start_col = box_col * 3

        existing = set()
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] != 0:
                    existing.add(self.board[i][j])

        missing = [n for n in range(1, 10) if n not in existing]
        random.shuffle(missing)

        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == 0:
                    self.board[i][j] = missing.pop()

    def _calculateCost(self):
        """Cost = number of duplicates in rows and columns"""
        cost = 0
        for i in range(9):
            row = self.board[i]
            cost += 9 - len(set(row))
        for j in range(9):
            col = [self.board[i][j] for i in range(9)]
            cost += 9 - len(set(col))
        return cost

    def _getNeighbor(self):
        """Generate a neighbor by swapping two non-fixed cells in same box"""
        box_row = random.randint(0, 2)
        box_col = random.randint(0, 2)
        start_row = box_row * 3
        start_col = box_col * 3

        non_fixed = []
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i, j) not in self.fixed_cells:
                    non_fixed.append((i, j))

        if len(non_fixed) < 2:
            return None

        cell1, cell2 = random.sample(non_fixed, 2)
        return (cell1, cell2)

    def _swap(self, cell1, cell2):
        """Swap values of two cells"""
        r1, c1 = cell1
        r2, c2 = cell2
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]

    def _clearScreen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _printBoardWithHighlight(self, swapped_cells=None, iteration=0, cost=0, temp=0, action=""):
        """Print board with highlighted swapped cells"""
        self._clearScreen()

        print("=" * 50)
        print("       SIMULATED ANNEALING - SUDOKU SOLVER")
        print("=" * 50)
        print(f"  Iteration: {iteration:,}")
        print(f"  Current Cost: {cost} (0 = solved)")
        print(f"  Temperature: {temp:.6f}")
        print(f"  Action: {action}")
        print("=" * 50)
        print()

        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("  ------+-------+------")

            row_str = "  "
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "

                val = self.board[i][j]

                # Highlight swapped cells
                if swapped_cells and (i, j) in swapped_cells:
                    row_str += f"\033[92m{val}\033[0m "  # Green color
                elif (i, j) in self.fixed_cells:
                    row_str += f"\033[94m{val}\033[0m "  # Blue for fixed
                else:
                    row_str += f"{val} "

            print(row_str)

        print()
        print("  Legend: \033[94mBlue\033[0m = Fixed clues | \033[92mGreen\033[0m = Just swapped")
        print()

    def _printStep(self, step_num, description):
        """Print algorithm step explanation"""
        print(f"\n  Step {step_num}: {description}")
        print("  " + "-" * 40)

    def solve(self, initial_temp=1.0, cooling_rate=0.99995, max_iterations=500000, visual=True, delay=0.05):
        """
        Main Simulated Annealing algorithm with visualization

        Parameters:
        - initial_temp: Starting temperature
        - cooling_rate: How fast temperature decreases
        - max_iterations: Maximum iterations before stopping
        - visual: Show step-by-step visualization
        - delay: Seconds between visual updates
        """

        if visual:
            self._clearScreen()
            print("=" * 50)
            print("       SIMULATED ANNEALING - EXPLANATION")
            print("=" * 50)
            print("""
  How Simulated Annealing Works:

  1. START: Fill each 3x3 box with numbers 1-9 randomly
     (This ensures boxes are valid, but rows/columns may not be)

  2. COST: Count duplicates in rows + columns
     (Cost = 0 means puzzle is solved!)

  3. NEIGHBOR: Pick two cells in same box and swap them
     (Only swap non-fixed cells)

  4. DECISION:
     - If new cost is BETTER (lower) → Always accept
     - If new cost is WORSE (higher) → Maybe accept
       (Probability = e^(-delta/temperature))

  5. COOLING: Reduce temperature gradually
     (As temp drops, less likely to accept worse solutions)

  6. REPEAT until cost = 0 or max iterations reached
            """)
            print("=" * 50)
            input("\n  Press Enter to start solving...")

        # Step 1: Initialize
        if visual:
            self._clearScreen()
            self._printStep(1, "Initializing board - filling boxes with 1-9")

        self._initializeBoard()
        current_cost = self._calculateCost()
        temperature = initial_temp
        best_cost = current_cost
        best_board = copy.deepcopy(self.board)

        if visual:
            self._printBoardWithHighlight(None, 0, current_cost, temperature, "Board initialized")
            time.sleep(1)

        accepted = 0
        rejected = 0
        improved = 0

        for iteration in range(max_iterations):
            # Check if solved
            if current_cost == 0:
                if visual:
                    self._printBoardWithHighlight(None, iteration, current_cost, temperature, "SOLVED!")
                    print("\n  🎉 PUZZLE SOLVED! 🎉")
                    print(f"  Total iterations: {iteration:,}")
                    print(f"  Moves accepted: {accepted:,}")
                    print(f"  Moves rejected: {rejected:,}")
                    print(f"  Improvements: {improved:,}")
                else:
                    print(f"\nSolved in {iteration:,} iterations!")
                return self.board

            # Step 3: Get neighbor (swap)
            swap_cells = self._getNeighbor()
            if swap_cells is None:
                continue

            cell1, cell2 = swap_cells
            old_val1 = self.board[cell1[0]][cell1[1]]
            old_val2 = self.board[cell2[0]][cell2[1]]

            # Make the swap
            self._swap(cell1, cell2)
            new_cost = self._calculateCost()
            delta = new_cost - current_cost

            # Step 4: Accept or reject
            action = ""
            if delta < 0:
                # Better solution - always accept
                current_cost = new_cost
                accepted += 1
                improved += 1
                action = f"ACCEPTED (improved by {-delta})"

                if current_cost < best_cost:
                    best_cost = current_cost
                    best_board = copy.deepcopy(self.board)

            elif temperature > 0:
                probability = math.exp(-delta / temperature)
                if random.random() < probability:
                    current_cost = new_cost
                    accepted += 1
                    action = f"ACCEPTED (worse, prob={probability:.3f})"
                else:
                    self._swap(cell1, cell2)  # Swap back
                    rejected += 1
                    action = f"REJECTED (prob={probability:.3f})"
            else:
                self._swap(cell1, cell2)  # Swap back
                rejected += 1
                action = "REJECTED (temp=0)"

            # Cool down
            temperature *= cooling_rate

            # Visual update
            if visual and iteration % 500 == 0:
                swap_set = {cell1, cell2}
                self._printBoardWithHighlight(swap_set, iteration, current_cost, temperature, action)
                print(f"  Swapped: ({cell1[0]},{cell1[1]})↔({cell2[0]},{cell2[1]}) | {old_val1}↔{old_val2}")
                print(f"  Accepted: {accepted:,} | Rejected: {rejected:,} | Improved: {improved:,}")
                time.sleep(delay)

            # Non-visual progress
            if not visual and iteration % 50000 == 0:
                print(f"Iteration {iteration:,}, Cost: {current_cost}, Temp: {temperature:.6f}")

        # Max iterations reached - return best found
        if visual:
            self._printBoardWithHighlight(None, max_iterations, best_cost, temperature, "MAX ITERATIONS REACHED")
            print(f"\n  Best cost achieved: {best_cost}")
        else:
            print(f"\nMax iterations reached. Best cost: {best_cost}")

        return best_board

    def getBoard(self):
        return self.board

    @staticmethod
    def printBoard(board):
        """Pretty print the board"""
        print()
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")
            row_str = ""
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                val = board[i][j]
                row_str += (str(val) if val != 0 else ".") + " "
            print(row_str)
        print()


if __name__ == '__main__':
    test_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("Original puzzle:")
    SA.printBoard(test_board)
    input("Press Enter to start SA solver with visualization...")

    solver = SA(test_board)
    solution = solver.solve(visual=True, delay=0.03)

    print("\nFinal Solution:")
    SA.printBoard(solution)