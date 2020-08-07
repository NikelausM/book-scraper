import logging
import aiohttp
import async_timeout
import asyncio
import time

from progress.bar import Bar

logger = logging.getLogger("scraping.menu")


async def fetch_page(session, url, bar):
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


async def get_multiple_pages(page, loop, *urls):
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
