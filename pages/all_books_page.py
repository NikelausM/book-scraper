from bs4 import BeautifulSoup
from typing import List

from locators.all_books_page import AllBooksPageLocators
from parsers.book_parser import BookParser


class AllBooksPage:
    def __init__(self, page_content: bytes):
        """
        Parameters
        ----------
        page_content : bytes
            The content of the webpage.
        """
        self.soup = BeautifulSoup(page_content, "html.parser")

    @property
    def books(self) -> List[BookParser]:
        """Returns the books on the books index page."""

        return [BookParser(e) for e in
                self.soup.select(AllBooksPageLocators.BOOKS)]
