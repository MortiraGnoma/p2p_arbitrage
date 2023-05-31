import asyncio
from pyppeteer import launch

link = "https://p2p.binance.com/en"

async def main_p2p(link):
    print(link)
    print("launching browser")
    browser = await launch()
    print("browser started")
    page = await browser.newPage()
    print("page created")
    await page.setViewport({'width': 1920, 'height': 3000})
    print("size set")
    await page.goto(link)
    print("page goto")
    print("Wait for close selector")
    await page.waitFor(10000)
    print("DONE")
    exit()
    
#asyncio.run(main_p2p(link))
asyncio.get_event_loop().run_until_complete((main_p2p(link)))