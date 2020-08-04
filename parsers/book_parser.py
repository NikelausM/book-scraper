import re
import logging

from locators.book_locators import BookLocators

logger = logging.getLogger("scraping.book_parser")


class BookParser:
    """
    A class to take in an HTML page or content, and find properties of an item
    in it.
    """

    RATINGS = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    def __init__(self, parent):
        """
        Parameters
        ----------
        parent : bs4.element.ResultSet
            The result of tags for Books.
        """

        logger.debug(f"New book parser created from `{parent}`")
        self.parent = parent

    def __repr__(self):
        return f"<Book {self.name}, £{self.price}, ({self.rating} stars)>"

    @property
    def name(self):
        """Returns book name.

        Returns
        -------
        str
            The book name.
        """

        logger.debug("Finding book name...")
        locator = BookLocators.NAME_LOCATOR
        item_name = self.parent.select_one(locator).attrs["title"]
        logger.debug(f"Found book name, `{item_name}`.")
        return item_name

    @property
    def link(self):
        """Returns book link.

        Returns
        -------
        str
            The book link.
        """

        logger.debug("Finding book link...")
        locator = BookLocators.LINK_LOCATOR
        item_url = self.parent.select_one(locator).attrs["href"]
        logger.debug(f"Found book name, `{item_url}`.")
        return item_url

    @property
    def price(self):
        """Returns book price.

        Returns
        -------
        str
            The book price.
        """

        logger.debug("Finding book price...")
        locator = BookLocators.PRICE_LOCATOR
        item_price = self.parent.select_one(locator).string

        pattern = "£([0-9]+\.[0-9]+)"
        matcher = re.search(pattern, item_price)
        float_price = float(matcher.group(1))  # 51.77
        logger.debug(f"Found book price, `{float_price}`.")
        return float_price

    @property
    def rating(self):
        """Returns book rating.

        Returns
        -------
        str
            The book rating.
        """

        logger.debug("Finding book rating...")
        locator = BookLocators.RATING_LOCATOR
        star_rating_element = self.parent.select_one(locator)

        # ['star-rating', 'Three']
        classes = star_rating_element.attrs["class"]
        rating_classes = [r for r in classes if r != "star-rating"]
        rating_number = BookParser.RATINGS.get(
            rating_classes[0])  # None if not found

        logger.debug(
            f"Found book rating, `{rating_number}`.")
        return rating_number
