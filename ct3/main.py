def get_books(filename: str):
    """
    Задание 1.
    Читает файл CSV (разделитель '|') и возвращает список списков:
    [isbn, title, author, quantity:int, price:float]
    """
    with open(filename, encoding="utf-8") as f:
        # читаем все строки
        lines = f.read().strip().splitlines()

    # отфильтруем заголовки (строки, которые начинаются с 'isbn|')
    data_lines = list(
        filter(lambda line: not line.lower().startswith("isbn|"), lines)
    )

    # парсер одной строки
    def parse_line(line: str):
        isbn, title, author, quantity, price = line.split("|")
        return [isbn, title, author, int(quantity), float(price)]

    # применяем parse_line ко всем строкам
    return list(map(parse_line, data_lines))


def filtered_books(books, substr: str):
    """
    Задание 2.
    Принимает список из get_books().
    Возвращает список списков вида:
    [isbn, "title, author", quantity, price]
    только для книг, где в title есть substr (без учета регистра).
    """
    needle = substr.casefold()

    # фильтр по подстроке в названии
    def has_substring(book):
        # book = [isbn, title, author, quantity, price]
        return needle in book[1].casefold()

    # преобразование одной книги к нужному виду
    def transform(book):
        isbn, title, author, quantity, price = book
        return [isbn, f"{title}, {author}", quantity, price]

    return list(map(transform, filter(has_substring, books)))


def totals_by_isbn(books_filtered):
    """
    Задание 3.
    Принимает результат filtered_books().
    Возвращает список кортежей: (isbn, quantity * price)
    """
    def to_tuple(book):
        isbn, title_author, quantity, price = book
        return (isbn, quantity * price)

    return list(map(to_tuple, books_filtered))


# Пример использования (можешь оставить или убрать):
if __name__ == "__main__":
    books = get_books("books.csv")
    python_books = filtered_books(books, "python")
    totals = totals_by_isbn(python_books)

    print(books)         # Задание 1
    print(python_books)  # Задание 2
    print(totals)        # Задание 3
