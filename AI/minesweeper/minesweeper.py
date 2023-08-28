import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return set() if self.cells != self.count else set(self.cells)

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return set(self.cells) if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return 1
        return 0

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            return 1
        return 0


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        counter = 0
        self.mines.add(cell)
        for sentence in self.knowledge:
            counter += sentence.mark_mine(cell)
        return counter

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        counter = 0
        self.safes.add(cell)
        for sentence in self.knowledge:
            counter += sentence.mark_safe(cell)
        return counter

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        i, j = cell
        neig_cells = set()
        for y in range(max(i - 1, 0), min(i + 2, self.height)):
            for x in range(max(j - 1, 0), min(j + 2, self.width)):
                if (i, j) != (y, x):
                    neig_cells.add((y, x))

        self.knowledge.append(Sentence(neig_cells, count))
        self.mark_safe_or_mines()
        inferences = self.inference()

        while inferences:
            for sentence in inferences:
                self.knowledge.append(sentence)
            self.mark_safe_or_mines()
            inferences = self.inference()

    def mark_safe_or_mines(self):
        bound = 1
        while bound:
            bound = 0
            for s in self.knowledge:
                for c in s.known_safes():
                    self.mark_safe(c)
                    bound += 1
                for c in s.known_mines():
                    self.mark_mine(c)
                    bound += 1
            for c in self.safes:
                bound += self.mark_safe(c)
            for c in self.mines:
                bound += self.mark_mine(c)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(0, self.height):
            for j in range(0, self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    return move

        return None

    def inference(self):
        inferences = []
        empty = []

        for s1 in self.knowledge:
            if s1.cells == set():
                empty.append(s1)
                continue
            for s2 in self.knowledge:
                if s2.cells == set():
                    empty.append(s2)
                    continue
                if s1 != s2:
                    if s2.cells.issubset(s1.cells):
                        new_set = s1.cells.difference(s2.cells)
                        new_count = s1.count - s2.count
                        new_sentence = Sentence(new_set, new_count)

                        # Check is new sentence is already in knowledge base
                        if new_sentence not in self.knowledge:
                            inferences.append(new_sentence)

        self.knowledge = [x for x in self.knowledge if x not in empty]

        return inferences
