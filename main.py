import random  # Used to randomly select a word
import datetime  # Used to store date and time for the scoreboard



def load_categories(
        filename="Categories.txt"):  # Loads the categories from the categories txt file and turns it into a list
    categories = []
    try:
        fileobj = open(filename, "r")
        line = fileobj.readline()

        while line != "":
            line = line.strip()
            if len(line) > 0:
                categories.append(line)
            line = fileobj.readline()

        fileobj.close()

    except FileNotFoundError:
        print("Categories file missing - starting with empty list.")

    return categories


def save_categories(categories,
                    filename="Categories.txt"):  # saves the categories entered if new ones are added.                     #for view in voteslist:
    try:
        fileobj = open(filename, "w")
        categoryindex = 0
        while categoryindex < len(categories):
            fileobj.write(categories[categoryindex] + "\n")
            categoryindex = categoryindex + 1
        fileobj.close()
    except Exception as ex:
        print("Error saving categories:", ex)


def load_words(filename="Words.txt"):  # Loads words from the file into a list
    words = []
    try:
        fileobj = open(filename, "r")
        line = fileobj.readline()

        while line != "":
            parts = line.strip().split(",")
            if len(parts) == 3:
                words.append(
                    parts)  # [category, difficulty, word]        Each word is stored as: [category, difficulty, word]
            line = fileobj.readline()

        fileobj.close()

    except FileNotFoundError:
        print("Words file missing - starting empty.")
    return words


def save_words(words, filename="Words.txt"):
    try:
        fileobj = open(filename, "w")
        index = 0

        while index < len(words):
            line = words[index][0] + "," + words[index][1] + "," + words[index][2] + "\n"
            fileobj.write(line)
            index = index + 1
        fileobj.close()
    except Exception as ex:
        print("Error saving words:", ex)


def load_scoreboard(filename="Scoreboard.txt"):  # Loads scoreboard entries from file
    board = []
    try:
        fileobj = open(filename, "r")
        line = fileobj.readline()

        while line != "":
            parts = line.strip().split(",")
            if len(parts) == 3:
                initials = parts[0]
                dtString = parts[1]
                try:
                    score = int(parts[2])
                except:
                    score = 0
                board.append([initials, dtString, score])  # Each entry contains initials, date/time, and score
            line = fileobj.readline()

        fileobj.close()

    except FileNotFoundError:
        print("Scoreboard missing - created new one.")

    return board


def save_scoreboard(board, filename="Scoreboard.txt"):  # Saves the scoreboard list back to the file
    try:
        fileobj = open(filename, "w")
        index = 0

        while index < len(board):
            line = board[index][0] + "," + board[index][1] + "," + str(board[index][2]) + "\n"
            fileobj.write(line)
            index = index + 1

        fileobj.close()
    except Exception as ex:
        print("Error saving scoreboard:", ex)


def getDateTime():  # Gets the current system date and time and returns it as a formatted string
    dt = datetime.datetime.now()

    day = dt.day
    month = dt.month
    year = dt.year
    hrs = dt.hour
    mins = dt.strftime("%M")

    dateStr = str(day) + "/" + str(month) + "/" + str(year)
    timeStr = str(hrs) + ":" + mins

    return dateStr + " " + timeStr


def update_scoreboard(board, initials,
                      points):  # Updates the scoreboard with new points. If the intitals entered by a player already exist points will upate as well as date and time
    found = False
    scoreIndex = 0

    while scoreIndex < len(board):
        if board[scoreIndex][0] == initials:
            board[scoreIndex][2] = board[scoreIndex][2] + points
            board[scoreIndex][1] = getDateTime()
            found = True
        scoreIndex = scoreIndex + 1

    if found == False:
        board.append([initials, getDateTime(), points])


def choose_category(categories):
    print("\nChoose a category:")

    catIndex = 0
    while catIndex < len(categories):
        print(str(catIndex + 1) + ". " + categories[catIndex])
        catIndex = catIndex + 1

    choice = input("Enter number: ")

    if choice.isdigit():
        choiceNum = int(choice)
        if choiceNum >= 1 and choiceNum <= len(categories):
            return categories[choiceNum - 1]

    print("Invalid category.")
    return None


def choose_difficulty():
    diff = input("Enter difficulty (easy/medium/hard): ").strip().lower()
    if diff == "easy" or diff == "medium" or diff == "hard":
        return diff
    print("Invalid difficulty.")
    return None


def pick_word_by_category_and_diff(words, cat, diff):
    shortlist = []
    index = 0

    while index < len(words):
        if words[index][0].lower() == cat.lower() and words[index][1].lower() == diff:
            shortlist.append(words[index][2])
        index = index + 1

    if len(shortlist) == 0:
        return None

    randomIndex = random.randint(0, len(shortlist) - 1)
    return shortlist[randomIndex]


def play_game(words, categories, board):
    print("\n Play the Game ")

    cat = choose_category(categories)
    if cat == None:
        print("No category selected.")
        return

    diff = choose_difficulty()
    if diff == None:
        print("No difficulty selected.")
        return

    secretWord = pick_word_by_category_and_diff(words, cat, diff)
    if secretWord == None:
        print("There are no words for that category and difficulty.")
        return

    # scoring by points
    if diff == "easy":
        points = 1
    elif diff == "medium":
        points = 5
    else:
        points = 10

    # mask the secret word by hiding it with undcerscores
    masked = ""
    letterIndex = 0
    while letterIndex < len(secretWord):
        if secretWord[letterIndex].isalpha():
            masked = masked + "_"
        else:
            masked = masked + secretWord[letterIndex]
        letterIndex = letterIndex + 1

    guessedLetters = []
    lives = 5

    print("\n--- Game Start ---")

    while "_" in masked and lives > 0:
        print("Word:", masked)
        print("You have", lives, "lives left:")

        letter = input("Guess a letter: ").lower()
        if len(letter) != 1 or not letter.isalpha():
            print("You can only enter a single letter.")
            continue

        if not letter.isalpha():
            print("Letters only.")
            continue

        if letter in guessedLetters:
            print("You have already guessed the letter.")
            continue

        guessedLetters.append(letter)

        found = False
        maskedList = list(masked)

        position = 0
        while position < len(secretWord):
            if secretWord[position].lower() == letter:
                maskedList[position] = secretWord[position]
                found = True
            position = position + 1

        if found:
            masked = "".join(maskedList)
        else:
            lives = lives - 1
            print("Wrong letter.")

    if "_" not in masked:
        print("\nYou WON! The word was:", secretWord)
        print("You earned", points, "points.")

        initials = input("Enter 3-letter initials: ").upper()
        if len(initials) != 3:
            initials = "ABC"

        update_scoreboard(board, initials, points)
        save_scoreboard(board)
        print("Score saved.")
    else:
        print("\nUnlucky! You lost. The word was:", secretWord)


def sortScore(row):
    return row[2]


def display_scoreboard(board):
    if len(board) == 0:
        print("Scoreboard is empty (There are no entries.")
        return

    board.sort(key=sortScore, reverse=True)

    print("\nTop 5 Scores")
    print("Initials | Score | Date/Time")

    scoreIndex = 0
    while scoreIndex < len(board) and scoreIndex < 5:
        print(board[scoreIndex][0] + " | " + str(board[scoreIndex][2]) + " | " + board[scoreIndex][1])
        scoreIndex = scoreIndex + 1


def manage_game(categories, words):  # Allows admin options such as adding categories and words
    running = True

    while running:
        print("\n--- Manage Game ---")
        print("1. Add Category")
        print("2. Add Word")
        print("3. List Categories")
        print("4. List Words")
        print("5. Back")

        choice = input("Choice: ")

        if choice == "1":
            newcat = input("Enter category: ").strip().lower()
            if newcat != "" and newcat not in categories:
                categories.append(newcat)
                save_categories(categories)
                print("Category added.")
            else:
                print("Invalid or exists already.")

        elif choice == "2":
            word = input("Enter word/phrase: ")
            if word == "":
                print("Cannot be blank.")
                continue

            print("Choose category:")
            catIndex = 0
            while catIndex < len(categories):
                print(str(catIndex + 1) + ". " + categories[catIndex])
                catIndex = catIndex + 1

            num = input("Enter number: ")
            if num.isdigit():
                num = int(num)
                if num >= 1 and num <= len(categories):
                    cat = categories[num - 1]
                else:
                    print("Invalid number.")
                    continue
            else:
                print("Invalid input.")
                continue

            diffic = input("Difficulty (easy/medium/hard): ").lower()
            if diffic != "easy" and diffic != "medium" and diffic != "hard":
                print("Invalid difficulty.")
                continue

            words.append([cat, diffic, word])
            save_words(words)
            print("Word added.")

        elif choice == "3":
            print("Categories:")
            for category in categories:
                print(category)

        elif choice == "4":
            print("Words:")
            for row in words:
                print(row[0] + " - " + row[1] + " - " + row[2])

        elif choice == "5":
            running = False

        else:
            print("Invalid choice.")


def main_menu():  # Displays the main menu and returns the user's choice

    splashscreen = r"""

 .d888b,  88bd88b  d8888b  ?88   d8P  d8P  88bd8b,d88b  d888b8b    88bd88b     
 ?8b,     88P' ?8bd8P' ?88 d88  d8P' d8P'  88P'`?8P'?8bd8P' ?88    88P' ?8b    
   `?8b  d88   88P88b  d88 ?8b ,88b ,88'  d88  d88  88P88b  ,88b  d88   88P    
`?888P' d88'   88b`?8888P' `?888P'888P'  d88' d88'  88b`?88P'`88bd88'   88b    
    """
    print(splashscreen)
    print("")
    print("1. Play the Game")
    print("2. Show Scoreboard")
    print("3. Manage Game")
    print("4. Exit")

    option = input("Enter choice: ")
    return option


def main():
    categories = load_categories()
    words = load_words()
    board = load_scoreboard()

    game_running = True  # Controls the menu from repeating

    while game_running:
        choice = main_menu()

        if choice == "1":
            play_game(words, categories, board)

        elif choice == "2":
            display_scoreboard(board)

        elif choice == "3":
            manage_game(categories, words)

        elif choice == "4":
            print("Saving data...")
            save_categories(categories)
            save_words(words)
            save_scoreboard(board)
            game_running = False
            print("Data saved!")

        else:
            print("Invalid option.")


main()