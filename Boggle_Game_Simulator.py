import random

class Boggle:
    def __init__(self, size=4):
        """
        Initializes the Boggle game with a specified board size.
        """
        self.size = size  # Define the Boggle board size
        self.dice = [
            ['A', 'E', 'A', 'N', 'E', 'G'],
            ['A', 'H', 'S', 'P', 'C', 'O'],
            ['A', 'S', 'P', 'F', 'F', 'K'],
            ['O', 'B', 'J', 'O', 'A', 'B'],
            ['I', 'O', 'T', 'M', 'U', 'C'],
            ['R', 'Y', 'V', 'D', 'E', 'L'],
            ['L', 'R', 'E', 'I', 'X', 'D'],
            ['E', 'I', 'U', 'N', 'E', 'S'],
            ['W', 'N', 'G', 'E', 'E', 'H'],
            ['L', 'N', 'H', 'N', 'R', 'Z'],
            ['T', 'S', 'T', 'I', 'Y', 'D'],
            ['O', 'W', 'T', 'O', 'A', 'T'],
            ['E', 'R', 'T', 'T', 'Y', 'L'],
            ['T', 'O', 'E', 'S', 'S', 'I'],
            ['T', 'E', 'R', 'W', 'H', 'V'],
            ['N', 'U', 'I', 'H', 'M', 'Qu']
        ]
        self.grid = self.generate_grid()
        self.words = []
        self.dictionary = set()  # Initialize dictionary to an empty set
        self.load_dictionary()  # Load dictionary of valid English words

    def generate_grid(self):
        """
        Generates a N*N grid with randomly chosen letters from the dice.
        """
        grid = [random.choice(die) for die in random.sample(self.dice, len(self.dice))]
        random.shuffle(grid)
        return [grid[i * self.size:(i + 1) * self.size] for i in range(self.size)]

    def print_grid(self):
        """
        Prints the Boggle grid.
        """
        for row in self.grid:
            print(' '.join(f"[{letter}]" for letter in row))

    def load_dictionary(self):
        """
        Loads the dictionary file and stores words in a set for quick lookup.
        """
        try:
            with open('words.txt', 'r') as file:
                self.dictionary = set(word.strip().upper() for word in file.readlines())
        except FileNotFoundError:
            print("Dictionary file not found. Please ensure 'words.txt' is present.")
            self.dictionary = set()

    def is_word_constructible(self, word):
        """
        Checks if the given word can be constructed from the Boggle grid.
        """
        def search(x, y, index, visited):
            if index == len(word):
                return True

            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            next_char = word[index]

            if self.grid[x][y] == 'Qu' and word[index:index + 2] == 'QU':
                next_char = 'QU'
                index += 1

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.size and 0 <= new_y < self.size and
                        (new_x, new_y) not in visited and
                        self.grid[new_x][new_y] == next_char and
                        search(new_x, new_y, index + 1, visited | {(new_x, new_y)})):
                    return True
            return False

        word = word.upper()  # Ensure the word is in uppercase to match the grid
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == word[0] or (self.grid[i][j] == 'Qu' and word[:2] == 'QU'):
                    if search(i, j, 1 if self.grid[i][j] != 'Qu' else 2, {(i, j)}):
                        return True
        return False

    def calculate_score(self, word):
        """
        Calculates the score of a word based on its length.
        """
        length = len(word)
        if length in [3, 4]:
            return 1
        elif length == 5:
            return 2
        elif length == 6:
            return 3
        elif length == 7:
            return 5
        elif length >= 8:
            return 11
        return 0

    def is_word_valid(self, word, valid_words):
        """
        Checks if a word is valid based on length, dictionary, grid presence, and uniqueness.
        """
        if len(word) < 3:
            print(f"The word {word} is too short.")
            return False
        if word not in self.dictionary:
            print(f"The word {word} is not a word.")
            return False
        if not self.is_word_constructible(word):
            print(f"The word {word} is not present in the grid.")
            return False
        if word in valid_words:
            print(f"The word {word} has already been used.")
            return False
        return True

    def play(self):
        """
        Main game loop for playing Boggle.
        """
        self.print_grid()
        print("Start typing your words! (press enter after each word and enter 'X' when done):")

        while True:
            word = input("> ").strip().upper()
            if word == 'X':
                break
            if not word.isalpha():
                print(f"The word {word} contains invalid characters.")
                continue
            self.words.append(word)

        valid_words = []

        for word in self.words:
            if self.is_word_valid(word, valid_words):
                valid_words.append(word)
                score = self.calculate_score(word)
                print(f"The word {word} is worth {score} {'point' if score == 1 else 'points'}.")

        total_score = sum(self.calculate_score(word) for word in valid_words)
        print(f"Your total score is {total_score} points!")

def main():
    """
    Entry point for the Boggle game.
    """
    game = Boggle()
    game.play()

if __name__ == "__main__":
    main()
