import logging
import asyncio
import aiohttp
import time

import menu

from progress.bar import Bar

from pages.all_books_page import AllBooksPage


async def fetch_page(session, url):
    page_start = time.time()
    # if session.get takes longer than 10 seconds then
    # an exception will be raised
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            # before returning response status it can get suspended
            # until response is received
            print(f"Page took {time.time() - page_start}")
            return response.status


async def get_multiple_pages(loop, *urls):
    tasks = []
    # use same loop as before
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            # Create coroutine and put in tasks list
            tasks.append(fetch_page(session, url))
        # wait for tasks here
        # gather alls tasks in list and treat as single task
        # to execute in loop. Awaits each task and only returns
        # when all complete
        grouped_tasks = asyncio.gather(*tasks)

        # we need to await them (yield from)
        # allows us to suspend execution here and wait
        # until something happens then resume
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

    # Get all pages
    with Bar("Scraping web pages", max=page.page_count,
             suffix='%(percent)d%%') as bar:
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
