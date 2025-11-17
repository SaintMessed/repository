import os
import random

WORDS_FILE = "words.txt"
HANGMAN_DIR = "hangman"


def load_words(filename: str):

    words = []
    if not os.path.exists(filename):
        print(f"Файл со словами '{filename}' не найден!")
        return words

    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ";" not in line:
                continue
            word, hint = line.split(";", 1)
            word = word.strip().upper()
            hint = hint.strip()
            if word:
                words.append((word, hint))
    return words


def load_hangman_stages(directory: str):
    """
    Загружает стадии виселицы из файлов в папке directory.
    Ожидаем файлы вида stage_0.txt, stage_1.txt, ..., пока они существуют.
    """
    stages = []
    i = 0
    while True:
        path = os.path.join(directory, f"stage_{i}.txt")
        if not os.path.exists(path):
            break
        with open(path, encoding="utf-8") as f:
            stages.append(f.read())
        i += 1

    
    if not stages:
        stages = [""]
    return stages


def clear_screen():
    
    print("\n" * 50)


def print_game_state(stages, wrong_guesses, guessed_word, hint, used_letters):
    clear_screen()
    
    stage_index = min(wrong_guesses, len(stages) - 1)
    print(stages[stage_index])
    print()
    print(f"Подсказка: {hint}")
    print(f"Слово: {guessed_word}")
    if used_letters:
        print(f"Использованные буквы: {', '.join(sorted(used_letters))}")
    print(f"Ошибок: {wrong_guesses} из {len(stages) - 1}")
    print()


def get_masked_word(secret_word, opened_letters):
    return "".join(letter if letter in opened_letters else "_" for letter in secret_word)


def play_round(words, stages):
    secret_word, hint = random.choice(words)
    opened_letters = set()
    used_letters = set()
    wrong_guesses = 0
    max_wrong = len(stages) - 1  

    
    guessed_word = get_masked_word(secret_word, opened_letters)

    while True:
        print_game_state(stages, wrong_guesses, guessed_word, hint, used_letters)

        # проверка на победу
        if guessed_word == secret_word:
            print("Поздравляем! Вы отгадали слово!")
            print(f"Слово было: {secret_word}")
            break

        # проверка на проигрыш
        if wrong_guesses >= max_wrong:
            print("Вы проиграли :(")
            print(f"Загаданное слово было: {secret_word}")
            break

        choice = input("Введите букву или попробуйте сразу слово (или '0' для выхода): ").strip().upper()

        if choice == "0":
            print("Выход из раунда.")
            break

        if not choice:
            continue

        # попытка отгадать всё слово
        if len(choice) > 1:
            if choice == secret_word:
                guessed_word = secret_word
                print_game_state(stages, wrong_guesses, guessed_word, hint, used_letters)
                print("Отлично! Вы сразу угадали слово!")
                break
            else:
                print("Неверное слово!")
                wrong_guesses += 1
                continue

        # попытка угадать букву
        letter = choice[0]
        if letter in used_letters:
            print("Эта буква уже была. Попробуйте другую.")
            continue

        used_letters.add(letter)

        if letter in secret_word:
            print("Есть такая буква!")
            opened_letters.add(letter)
            guessed_word = get_masked_word(secret_word, opened_letters)
        else:
            print("Нет такой буквы.")
            wrong_guesses += 1


def main():
    words = load_words(WORDS_FILE)
    if not words:
        print("Список слов пуст или не найден. Заполните файл words.txt.")
        return

    stages = load_hangman_stages(HANGMAN_DIR)
    print("Добро пожаловать в игру 'Виселица на поле чудес'!")
    print(f"Загружено слов: {len(words)}")
    print(f"Стадий виселицы: {len(stages)}")
    input("Нажмите Enter, чтобы начать...")

    while True:
        play_round(words, stages)
        again = input("Сыграть ещё раз? (д/н): ").strip().lower()
        if again != "д":
            print("Спасибо за игру!")
            break


if __name__ == "__main__":
    main()
