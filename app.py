import logging
import requests
import aiohttp
import async_timeout
import asyncio
import time


import menu

from progress.bar import Bar

from pages.all_books_page import AllBooksPage

logger = logging.getLogger("scraping.menu")


async def fetch_page(session, url, bar):
    page_start = time.time()
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            logger.info(f"Page took {time.time() - page_start}")

            # suspend before download has completed
            response_text = await response.text()

            # update progress bar
            bar.next()

            # return html contents
            return response_text


async def get_multiple_pages(loop, *urls):
    # progress bar
    with Bar("Scraping web pages", max=page.page_count,
             suffix='%(percent)d%%') as bar:
        tasks = []
        async with aiohttp.ClientSession(loop=loop) as session:
            for url in urls:
                tasks.append(fetch_page(session, url, bar))

            grouped_tasks = asyncio.gather(*tasks)
            # may not be in order
            return await grouped_tasks

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
    pages = loop.run_until_complete(get_multiple_pages(loop, *urls))

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
