import logging

logger = logging.getLogger("scraping.menu")


class Menu:
    """A class that creates a console menu for scraping a website.

    Parameters
    ----------
    MENU_PROMPT : str
        The string to be displayed as the console menu prompt.
    books : List[Books]
        List of books of the website.
    books_generator : Generator
        The generator that returns the books in the book list.
    """

    MENU_PROMPT = """
    Enter one of the following

    - 'b' to look at highest rated books
    - 'c' to look at the cheapest books
    - 'n' to just get the next available book on the catalogue
    - 'q' to exit

    Enter your choice: """

    def __init__(self, books):
        """
        Parameters
        ----------
        books : List[Book]
            A list of the books of the website.
        """
        self.books = books
        self.books_generator = (x for x in self.books)

    def print_best_books(self):
        """Print the highest rated books."""

        logger.info("Finding best books by rating...")
        best_books = sorted(self.books, key=lambda x: (
            x.rating * -1, x.price))[:10]
        for book in best_books:
            print(book)

    def print_cheapest_books(self):
        """Print the cheapest books."""

        logger.info("Finding cheapest books by price...")
        best_books = sorted(self.books, key=lambda x: x.price)[:10]
        for book in best_books:
            print(book)

    def get_next_book(self):
        """Get next book in catalogue."""

        logger.info("Getting next book from generator of all books...")
        print(next(self.books_generator))

    @property
    def user_choices(self):
        """Returns a dictionary of the functions that correspond to user choices.

        Returns
        -------
        Dict[Callable[]]
            The dictionary of the functions that correspond to user choices.
        """

        USER_CHOICES = {
            'b': self.print_best_books,
            'c': self.print_cheapest_books,
            'n': self.get_next_book
        }
        return USER_CHOICES

    def prompt(self):
        """Creates a console menu with a prompt for viewing books."""

        user_input = input(self.MENU_PROMPT)
        while user_input != 'q':
            if user_input in ('b', 'c', 'n'):
                self.user_choices[user_input]()
            else:
                print("Please choose a valid command")
            user_input = input(self.MENU_PROMPT)
        logger.debug("Terminating program...")
