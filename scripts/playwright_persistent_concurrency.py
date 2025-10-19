import asyncio
import random
from pathlib import Path

from playwright.async_api import BrowserContext, async_playwright

CWD = Path().resolve()

# Example path
user_data_dir = Path.joinpath(CWD, 'playwright/data_dir/chromium')
user_data_dir.mkdir(parents=True, exist_ok=True)


async def open_page(url: str, browser: BrowserContext, sleep: int):
    'Open page in given `BrowserContext`'
    page = await browser.new_page()
    await page.goto(url, wait_until='domcontentloaded')
    # Simulate some job
    await asyncio.sleep(sleep)
    await page.close()


async def main(url: str, tabs: int) -> None:
    'Open multiple `tabs` asynchronous, in same browser.'
    semaphore = asyncio.BoundedSemaphore(5)
    async with semaphore, async_playwright() as playwright:
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless = False,
            )

        tasks = []
        for _ in range(tabs):
            tasks.append(
                asyncio.create_task(
                    open_page(
                        url=url,
                        browser=browser,
                        sleep=random.randint(3, 10)
                        )))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    url = 'https://example.com/'
    tabs = 5
    asyncio.run(main(url, tabs))