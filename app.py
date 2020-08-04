import requests
import logging
from progress.bar import Bar

from pages.all_books_page import AllBooksPage

import menu

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.INFO,
        filename="logs.txt"
    )

    # creates logger in background
    logger = logging.getLogger("scraping")

    logger.info("Loading books list...")

    # request from website
    BASE_URL = "http://books.toscrape.com"

    page_content = requests.get(BASE_URL).content

    # extract the books page and its books
    page = AllBooksPage(page_content)

    # Get all pages
    with Bar("Scraping web pages", max=page.page_count, suffix='%(percent)d%%') as bar:
        books = []
        for page_num in range(page.page_count):
            url = BASE_URL + f"/catalogue/page-{page_num}.html"
            page_content = requests.get(url).content
            logger.debug("Creating AllBooksPage from page content.")
            page = AllBooksPage(page_content)
            books.extend(page.books)
            bar.next()

    # Create and print out menu
    newMenu = menu.Menu(books)

    newMenu.prompt()
