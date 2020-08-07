import logging
import requests
import asyncio
import time

import menu

from progress.bar import Bar

from pages.all_books_page import AllBooksPage
from async_req.async_req import fetch_page, get_multiple_pages


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s" +
        " [%(filename)s:%(lineno)d]" +
        " %(message)s",
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

    loop = asyncio.get_event_loop()

    urls = [
        BASE_URL + f"/catalogue/page-{page_num}.html"
        for page_num in range(0, page.page_count)
    ]
    start = time.time()
    pages = loop.run_until_complete(get_multiple_pages(page, loop, *urls))

    print(f"Total page requests took {time.time() - start}")

    # Get all pages
    books = []

    for page_content in pages:
        logger.debug("Creating AllBooksPage from page content.")
        page = AllBooksPage(page_content)
        books.extend(page.books)

    # Create and print out menu
    newMenu = menu.Menu(books)

    newMenu.prompt()
