from app import books

USER_CHOICE = """
Enter one of the following

- 'b' to look at 5-star books
- 'c' to look at the cheapest books
- 'n' to just get the next available book on the catalogue
- 'q' to exit

Enter your choice: """


def print_best_books():
    best_books = sorted(books, key=lambda x: (x.rating * -1, x.price))[:10]
    for book in best_books:
        print(book)


def print_cheapest_books():
    best_books = sorted(books, key=lambda x: x.price)[:10]
    for book in best_books:
        print(book)


books_generator = (x for x in books)


def get_next_book():
    """Get next book in catalogue."""

    print(next(books_generator))


user_choices = {
    'b': print_best_books,
    'c': print_cheapest_books,
    'n': get_next_book
}


def menu():
    """Creates a console menu for viewing books."""

    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input in ('b', 'c', 'n'):
            user_choices[user_input]()
        else:
            print("Please choose a valid command")
        user_input = input(USER_CHOICE)


SCRIPT_MODE = "__main__"
if __name__ == SCRIPT_MODE:
    menu()
