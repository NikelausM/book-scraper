import re
import logging

from bs4 import BeautifulSoup
from typing import List

from locators.all_books_page import AllBooksPageLocators
from parsers.book_parser import BookParser

logger = logging.getLogger("scraping.all_books_page")


class AllBooksPage:
    """Class that retreives a web page, its books, and page count."""

    def __init__(self, page_content: bytes):
        """
        Parameters
        ----------
        page_content : bytes
            The content of the webpage.
        """
        logger.debug("Parsing page content with BeautifulSoup HTML parser.")
        self.soup = BeautifulSoup(page_content, "html.parser")

    @property
    def books(self) -> List[BookParser]:
        """Returns the books on the books index page."""

        logger.debug(
            f"Finding all books in the page using" +
            f"`{AllBooksPageLocators.BOOKS}`.")
        return [BookParser(e) for e in
                self.soup.select(AllBooksPageLocators.BOOKS)]

    @property
    def page_count(self):
        """Returns page count of website.

        Returns
        -------
        int
            The number of pages the website has.
        """
        logger.debug("Finding all number of catalogue pages available...")
        content = self.soup.select_one(AllBooksPageLocators.PAGER).string
        logger.info(
            f"Found number of catalogue pages available: `{content}`.")
        pattern = "Page [0-9]+ of ([0-9]+)"
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        logger.debug(f"Extracted nuber of pages as integer: `{pages}`.")
        return pages
