from sys import argv
import binance
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import telebot
from telebot import types


try:
    script, coin, bank, fiat, amount  = argv
except:
    print("Invalid args!")
    exit()


print(fiat)

TOKEN = ''
CHANNEL_ID =
bot = telebot.TeleBot(TOKEN)

def GetConnInfo(link):
    return link.status_code

def getLink(pair, exchange):
    if(exchange == "Binance"):
        return f"https://www.binance.com/uk-UA/trade/{pair}?_from=markets&theme=dark&type=spot"


def PriceDiff(sell_1, buy_2, sell_2, buy_1):
    dif1 = (buy_2/sell_1-1)*100
    dif2 = (buy_1/sell_2-1)*100
    return [dif1, dif2]

async def parseData(data):
    soup = BeautifulSoup(data, 'lxml')
    prices_soup = soup.findAll('div', {"class": "css-1m1f8hn"})
    limits_soup = soup.findAll('div', {"class": "css-4cffwv"})
    return [prices_soup, limits_soup]

async def evaluateCall(page):
    await page.waitFor(10000)
    #await page.waitForNavigation()
    data = await page.evaluate("() => document.querySelector('*').outerHTML");
    return data

async def NextPage(page):
    print("Waiting to click Next button")
    #await page.waitForNavigation()
    #await page.waitFor(10000)
    print("Waiting for selector")
    await page.waitForSelector("main > div.css-15owl46 > div.css-94s69v > div > div.css-kwfbf > div > button[aria-label='Next page']:not([disabled])")
    print("Clicking button")
    await page.click("main > div.css-15owl46 > div.css-94s69v > div > div.css-kwfbf > div > button[aria-label='Next page']:not([disabled])")
    print("Button pressed")
    await page.waitFor(10000)

async def main_p2p(link):
    global result_prices

    print(link)

    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 3000})
    await page.goto(link, {"timeout": 60000})

    #await page.screenshot({"path": '/Users/ivan/Desktop/p2p_arbi/screenshot.jpg'})

    print("Wait for close selector")
    await page.waitFor(20000)
    #await page.screenshot({"path": '/Users/ivan/Desktop/p2p_arbitrage/screenshot.jpg'})
    try:
        await page.waitForSelector("body > div.css-1u2pn8e > div.css-ebuj64 > svg[class='css-1pcqseb']")
        print("Clicking close button")
        await page.click("body > div.css-1u2pn8e > div.css-ebuj64 > svg[class='css-1pcqseb']")
        print("Waiting for close")
        await page.waitFor(10000)
    except:
        print("Nothing to close")
    print("Taking screenshot")
    #await page.screenshot({"path": '/Users/ivan/Desktop/p2p_arbitrage/screenshot.jpg'})
    await page.waitFor(1000)
    await page.type('input[id=C2Csearchamount_searchbox_amount]', amount)#, {delay: 20})
    await page.waitFor(2000)
    #await page.screenshot({"path": '/Users/ivan/Desktop/p2p_arbitrage/screenshot_type.jpg'})
    print("Waiting for Search selector")
    await page.waitForSelector("button[id='C2Csearchamount_btn_search']")
    print("Clicking Search button")
    await page.click("button[id='C2Csearchamount_btn_search']")
    print("Waiting for screenshot")
    await page.waitFor(20000)
    #await page.screenshot({"path": '/Users/ivan/Desktop/p2p_arbitrage/screenshot_search.jpg'})
    print("Screen done")


    #pages = await page.JJ("main > div.css-15owl46 > div.css-94s69v > div > div.css-kwfbf > div > button[aria-label='Next page']:not([disabled])")
    pages_cntr = 0
    pages_cntr2 = 0
    result_page = []
    while pages_cntr < 1: #while True: #pages_cntr < 15:
        try:
            print(f"Taking screen page {pages_cntr}")
            #await page.screenshot({"path": '/Users/ivan/Desktop/p2p_arbitrage/screenshot2.jpg'})
            result_page.append(await evaluateCall(page))
            #await NextPage(page)
            pages_cntr += 1
        except:
            print("Otval while True")
            break
    await browser.close()

    res = []
    for res_page in result_page:
        res.append(await parseData(res_page))

    for result in res:
        prices_soup = result[0]
        limits_soup = result[1]

        prices = []
        limits = []

        for price in prices_soup:
            prices.append(price.text)

        for limit in limits_soup:
            limits.append(limit.text)

        i=0
        while i<10:
            lim_cntr = 0
            for lim in limits:
                if lim.find("₴") == -1:
                    limits.remove(lim)
                lim_cntr += 1
            i += 1

        i = 0
        #result_prices.append(f"Page {pages_cntr2}\n")
        while i < len(prices):
            result_prices.append([prices[i], [limits[i], limits[i+1]]])
            #print(f"Price: {prices[i]} Limits: {limits[i]}, {limits[i+1]}")
            i += 1
        pages_cntr2 += 1
        print(f"End of page {pages_cntr2}   len {len(prices)}")


#Обробники telegram

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"Bot started")


#Обробник повідомлень в боті
@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'test': #Тестове повідомлення
            bot.send_message(message.chat.id, "This is test")
        else:
            bot.send_message(message.chat.id, 'Command not found :(')



print(f'\nBinance connection status: {GetConnInfo(binance.r)}')

#bot.send_message(chat_id = CHANNEL_ID, text = "Program p2p just started")

fiat = fiat

print(fiat)

link_buy = f"https://p2p.binance.com/en/trade/{bank}/{coin}?fiat={fiat}"
link_sell = f"https://p2p.binance.com/en/trade/sell/{coin}?fiat={fiat}&payment={bank}"

result_prices = []
asyncio.get_event_loop().run_until_complete((main_p2p(link_buy)))
prices_p2p_buy = list(result_prices)
result_prices = []
asyncio.get_event_loop().run_until_complete((main_p2p(link_sell)))
prices_p2p_sell = list(result_prices)

item = coin+fiat
otvl_cntr = 0
while True:
    try:
        price_market = [[binance.GetOrderbookSell(item)[0][0], binance.GetOrderbookBuy(item)[0][0], binance.GetOrderbookSell(item)[0][1], binance.GetOrderbookBuy(item)[0][1]],[binance.GetOrderbookSell(item)[1][0], binance.GetOrderbookBuy(item)[1][0], binance.GetOrderbookSell(item)[1][1], binance.GetOrderbookBuy(item)[1][1]]]
    except:
        if otvl_cntr >= 10:
            break
        print("Get data from market otval")
        otvl_cntr += 1
    else:
        print("data reached")
        otvl_cntr = 0
        break

diff_check = PriceDiff(price_market[0][0], price_market[1][0], price_market[0][1], price_market[1][1])
price1 = [0,0,0,0]
#price2 = [0,0,0,0]

ALLOW_DIFF = 10

if diff_check[0] > ALLOW_DIFF or diff_check[1] > ALLOW_DIFF:
    price1[0] = price_market[1][0]
    price1[1] = price_market[1][1]
    price1[2] = price_market[1][2]
    price1[3] = price_market[1][3]
else:
    price1[0] = price_market[0][0]
    price1[1] = price_market[0][1]
    price1[2] = price_market[0][2]
    price1[3] = price_market[0][3]


print(f"prices_p2p_buy {len(prices_p2p_buy)}\n{prices_p2p_buy}")
print(f"prices_p2p_sell {len(prices_p2p_sell)}\n{prices_p2p_sell}")
print(f"price_marketn{price1}")

#price1[0].replace(",", "")
prices_p2p_sell[0][0] = prices_p2p_sell[0][0].replace(",", "")
prices_p2p_buy[0][0] = prices_p2p_buy[0][0].replace(",", "")
#price1[1].replace(",", "")

#market buy
ADVANTAGE = 0.1
market_buy = float(price1[0]) #buy_1 and buy_2
p2p_sell = float(prices_p2p_sell[0][0]) #sell_1
p2p_sell_order = float(prices_p2p_buy[0][0]) #- ADVANTAGE #sell_2
print(market_buy)
print(p2p_sell)
print(p2p_sell_order)
market_buy_diff = PriceDiff(p2p_sell, market_buy, p2p_sell_order, market_buy)
market_buy_diff[0] *= -1
market_buy_diff[1] *= -1

#p2p buy
ADVANTAGE = 0.1
p2p_buy = float(prices_p2p_buy[0][0]) #buy_1
p2p_buy_order = float(prices_p2p_sell[0][0]) #+ ADVANTAGE #buy_2
market_sell = float(price1[1]) # sell_1 and sell_2
print(p2p_buy)
print(p2p_buy_order)
print(market_sell)
p2p_buy_diff = PriceDiff(market_sell, p2p_buy_order, market_sell, p2p_buy)
p2p_buy_diff[0] *= -1
p2p_buy_diff[1] *= -1


print(f"Buy on market {market_buy} -> Sell on p2p {p2p_sell} ({market_buy_diff[0]}) OR sell on p2p order {p2p_sell_order} ({market_buy_diff[1]})")
print(f"Buy on p2p {p2p_buy} ({p2p_buy_diff[1]}) OR buy order {p2p_buy_order} ({p2p_buy_diff[0]}) -> Sell on market {market_sell}")

LIMIT = 0.5

market_link = getLink(item, "Binance")

if market_buy_diff[0] > LIMIT:
    message = "-----------------p2p/market------------------------\n\n"
    message += f"Prices for amount {amount} {fiat}!\n\n"
    message += f"~~~{bank}  {coin}~~~\n"
    message += f"Buy on market {market_buy} -> Sell on p2p {p2p_sell} ({market_buy_diff[0]})%\n\n"
    message += f"Link p2p: {link_sell}\nLink market: {market_link}"
    bot.send_message(chat_id = CHANNEL_ID, text = message)

if p2p_buy_diff[0] > LIMIT:
    message = "-----------------p2p/market------------------------\n\n"
    message += f"Prices for amount {amount} {fiat}!\n\n"
    message += f"~~~{bank}  {coin}~~~\n"
    message += f"Buy on p2p creating order with price higher {p2p_buy_order} -> Sell on market {market_sell} ({p2p_buy_diff[0]})%\n\n"
    message += f"Link p2p: {link_sell}\nLink market: {market_link}"
    bot.send_message(chat_id = CHANNEL_ID, text = message)

if market_buy_diff[1] > LIMIT:
    message = "-----------------p2p/market------------------------\n\n"
    message += f"Prices for amount {amount} {fiat}!\n\n"
    message += f"~~~{bank}  {coin}~~~\n"
    message += f"Buy on market {market_buy} -> Sell on p2p creating order with price lower {p2p_sell_order} ({market_buy_diff[1]})%\n\n"
    message += f"Link p2p: {link_buy}\nLink market: {market_link}"
    bot.send_message(chat_id = CHANNEL_ID, text = message)

if p2p_buy_diff[1] > LIMIT:
    message = "-----------------p2p/market------------------------\n\n"
    message += f"Prices for amount {amount} {fiat}!\n\n"
    message += f"~~~{bank}  {coin}~~~\n"
    message += f"Buy on p2p {p2p_buy} -> Sell on market {market_sell} ({p2p_buy_diff[1]})%\n\n"
    message += f"Link p2p: {link_buy}\nLink market: {market_link}"
    bot.send_message(chat_id = CHANNEL_ID, text = message)


#message += f"Buy on market {market_buy} -> Sell on p2p {p2p_sell} ({market_buy_diff[0]}) OR sell on p2p order {p2p_sell_order} ({market_buy_diff[1]})\n\n"
#message += f"Buy on p2p {p2p_buy} ({p2p_buy_diff[1]}) OR buy order {p2p_buy_order} ({p2p_buy_diff[0]}) -> Sell on market {market_sell}"
