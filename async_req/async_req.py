import logging
import aiohttp
import async_timeout
import asyncio
import time

from progress.bar import Bar
from asyncio import AbstractEventLoop
from typing import List

from pages.all_books_page import AllBooksPage

logger = logging.getLogger("scraping.menu")


async def fetch_page(session: aiohttp.ClientSession, url: str, bar: Bar):
    """Fetches pages of urls.

    Parameters
    ----------
    session : aiohttp.ClientSession
        Encapsulates a connections pool for making HTTP requests.
    url : str
        The url to be requested.
    bar : Bar
        The progress bar.

    Returns
    -------
    str
        The HTML response text from the HTTP request to the url.
    """
    page_start = time.time()
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            logger.info(f"Page took {time.time() - page_start}")

            # wait for response
            response_text = await response.text()

            # update progress bar
            bar.next()

            # return html contents
            return response_text


async def get_multiple_pages(page: AllBooksPage, loop: AbstractEventLoop,
                             *urls: str) -> List[str]:
    """Gets pages from each url given.

    Parameters
    ----------
    page : AllBooksPage
        The class that extractes web page elements and data.
    loop : AbstractEventLoop
        The event loop, by default asyncio is configured to use
        SelectorEventLoop on Unix and ProactorEventLoop on Windows.

    Returns
    -------
    List[str]:
        The list of HTML response text for each web page.
    """
    print("eventloop: ", type(loop))
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
