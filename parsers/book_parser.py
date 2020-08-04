import re

from bs4 import Beautifulparent

from locators.book_locators import BookLocators


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
        self.parent = parent

    @property
    def name(self):
        locator = BookLocators.NAME_LOCATOR
        item_name = self.parent.select_one(locator).attrs["title"]
        return item_name

    @property
    def link(self):
        locator = BookLocators.LINK_LOCATOR
        item_url = self.parent.select_one(locator).attrs["href"]
        return item_url

    @property
    def price(self):
        locator = BookLocators.PRICE_LOCATOR
        item_price = self.parent.select_one(locator).string

        pattern = "£([0-9]+\.[0-9]+)"
        matcher = re.search(pattern, item_price)
        return float(matcher.group(1))  # 51.77

    @property
    def rating(self):
        locator = BookLocators.RATING_LOCATOR
        star_rating_element = self.parent.select_one(locator)
        # ['star-rating', 'Three']
        classes = star_rating_element.attrs["class"]
        rating_classes = filter(lambda x: x != "star-rating", classes)
        rating_number = BookParser.RATINGS.get(
            rating_classes[0])  # None if not found
        return next(rating_classes)
