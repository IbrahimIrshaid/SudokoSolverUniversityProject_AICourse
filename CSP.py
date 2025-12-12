import time
import copy
from typing import List, Tuple, Optional, Set


class CSP:
    def __init__(self, board):
        """
        Initialize CSP solver
        Receives a normal partial-filled Sudoku grid (integers 0-9)
        """
        # Store original board (convert to integer grid if needed)
        self.original_board = []
        for row in board:
            new_row = []
            for cell in row:
                if isinstance(cell, str):
                    val = 0 if cell in ['.', '0'] else int(cell)
                else:
                    val = int(cell)
                new_row.append(val)
            self.original_board.append(new_row)

        # Working board (will be modified during solving)
        self.board = [row[:] for row in self.original_board]

        # Domain tracking - stores possible values for each cell
        # Format: domains[row][col] = set of possible values {1,2,...,9}
        self.domains = [[set() for _ in range(9)] for _ in range(9)]

        self.heuristic_type = None
        self.nodes_explored = 0
        self.backtracks = 0

        # Initialize domains
        self._initialize_domains()

    def _initialize_domains(self):
        """Initialize domain for each cell based on constraints"""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    # Empty cell - calculate possible values
                    self.domains[row][col] = self._get_possible_values(row, col)
                else:
                    # Fixed cell - no domain (already assigned)
                    self.domains[row][col] = set()

    def _get_neighbors(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """Get all neighbors (row, column, and 3x3 box) of a cell"""
        neighbors = set()

        # Same row
        for c in range(9):
            if c != col:
                neighbors.add((row, c))

        # Same column
        for r in range(9):
            if r != row:
                neighbors.add((r, col))

        # Same 3x3 box
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))

        return neighbors

    def _get_possible_values(self, row: int, col: int) -> Set[int]:
        """Get all valid values for a cell based on current board state"""
        if self.board[row][col] != 0:
            return set()

        possible = set(range(1, 10))

        # Remove values in same row
        for c in range(9):
            val = self.board[row][c]
            if val != 0:
                possible.discard(val)

        # Remove values in same column
        for r in range(9):
            val = self.board[r][col]
            if val != 0:
                possible.discard(val)

        # Remove values in same 3x3 box
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                val = self.board[r][c]
                if val != 0:
                    possible.discard(val)

        return possible

    def _update_domains_after_assignment(self, row: int, col: int, value: int):
        """Update domains of all neighbors after assigning a value"""
        # Clear domain of assigned cell
        self.domains[row][col] = set()

        # Update all neighbors
        neighbors = self._get_neighbors(row, col)
        for r, c in neighbors:
            if self.board[r][c] == 0:
                # Remove the assigned value from neighbor's domain
                self.domains[r][c].discard(value)

    def _select_unassigned_cell_MRV(self) -> Optional[Tuple[int, int]]:
        """
        Minimum Remaining Values (MRV) heuristic
        Select cell with smallest domain (fewest possible values)
        """
        min_values = 10
        best_cell = None

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    domain_size = len(self.domains[row][col])

                    if domain_size == 0:
                        return None  # Contradiction found

                    if domain_size < min_values:
                        min_values = domain_size
                        best_cell = (row, col)

        return best_cell

    def _select_unassigned_cell_MCV(self) -> Optional[Tuple[int, int]]:
        """
        Most Constraining Variable (MCV) heuristic
        Select cell that affects most unassigned neighbors
        """
        max_constraints = -1
        best_cell = None

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    # Count unassigned neighbors
                    neighbors = self._get_neighbors(row, col)
                    unassigned_neighbors = sum(1 for r, c in neighbors
                                               if self.board[r][c] == 0)

                    if unassigned_neighbors > max_constraints:
                        max_constraints = unassigned_neighbors
                        best_cell = (row, col)

        return best_cell

    def _order_values_LCV(self, row: int, col: int, possible: Set[int]) -> List[int]:
        """
        Least Constraining Value (LCV) heuristic
        Order values by how many choices they eliminate for neighbors
        """
        value_impacts = []

        for value in possible:
            # Count how many neighbor possibilities this value eliminates
            impact = 0
            neighbors = self._get_neighbors(row, col)

            for r, c in neighbors:
                if self.board[r][c] == 0:
                    # Check if this value is in neighbor's domain
                    if value in self.domains[r][c]:
                        impact += 1

            value_impacts.append((impact, value))

        # Sort by impact (ascending - least constraining first)
        value_impacts.sort()
        return [val for _, val in value_impacts]

    def _backtrack(self, heuristic: str) -> bool:
        """Backtracking search with specified heuristic"""
        self.nodes_explored += 1

        # Select unassigned cell based on heuristic
        if heuristic == 'MRV':
            cell = self._select_unassigned_cell_MRV()
        elif heuristic == 'MCV':
            cell = self._select_unassigned_cell_MCV()
        else:  # LCV - use MRV for selection, LCV for ordering
            cell = self._select_unassigned_cell_MRV()

        if cell is None:
            # Check if puzzle is complete
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:
                        return False  # Contradiction
            return True  # Puzzle complete

        row, col = cell
        possible_values = self.domains[row][col].copy()

        if not possible_values:
            return False

        # Order values based on heuristic
        if heuristic == 'LCV':
            ordered_values = self._order_values_LCV(row, col, possible_values)
        else:
            ordered_values = list(possible_values)

        for value in ordered_values:
            # Save current state
            saved_board = [row[:] for row in self.board]
            saved_domains = [row[:] for row in self.domains]

            # Try this value
            self.board[row][col] = value
            self._update_domains_after_assignment(row, col, value)

            # Recursively solve
            if self._backtrack(heuristic):
                return True

            # Backtrack
            self.backtracks += 1
            self.board = saved_board
            self.domains = saved_domains

        return False

    def solve(self, heuristic: str = 'MRV', visual: bool = False) -> Tuple[List[List], dict]:
        """
        Solve the Sudoku puzzle using CSP with specified heuristic

        Args:
            heuristic: 'MRV', 'MCV', or 'LCV'
            visual: Whether to show solving progress (not implemented yet)

        Returns:
            Tuple of (solved_board, statistics)
        """
        self.nodes_explored = 0
        self.backtracks = 0
        start_time = time.time()

        # Solve using backtracking
        success = self._backtrack(heuristic)

        end_time = time.time()
        elapsed_time = end_time - start_time

        stats = {
            'heuristic': heuristic,
            'success': success,
            'time': elapsed_time,
            'nodes_explored': self.nodes_explored,
            'backtracks': self.backtracks
        }

        return self.board if success else None, stats


def test_all_heuristics(board):
    """Test all three heuristics and compare performance"""
    print("=" * 60)
    print("TESTING ALL CSP HEURISTICS")
    print("=" * 60)

    results = []

    for heuristic in ['MRV', 'MCV', 'LCV']:
        print(f"\nTesting {heuristic}...")
        solver = CSP(board)
        solution, stats = solver.solve(heuristic=heuristic)
        results.append(stats)

        print(f"  Success: {stats['success']}")
        print(f"  Time: {stats['time']:.4f} seconds")
        print(f"  Nodes explored: {stats['nodes_explored']}")
        print(f"  Backtracks: {stats['backtracks']}")

    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    print(f"{'Heuristic':<10} {'Time (s)':<12} {'Nodes':<12} {'Backtracks':<12}")
    print("-" * 60)

    for stat in results:
        print(f"{stat['heuristic']:<10} {stat['time']:<12.4f} "
              f"{stat['nodes_explored']:<12} {stat['backtracks']:<12}")

    # Find fastest
    fastest = min(results, key=lambda x: x['time'])
    print(f"\nFastest: {fastest['heuristic']} ({fastest['time']:.4f}s)")


# Example usage
if __name__ == '__main__':
    # Example board (0 represents empty cells)
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

    test_all_heuristics(test_board)