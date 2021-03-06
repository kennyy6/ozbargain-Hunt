from bs4 import BeautifulSoup
import requests
import telegram
from telegram.ext import Updater, CommandHandler,CallbackQueryHandler,MessageHandler, Filters
import credentials


def topPage(update,context):
    """
    Sends all the products within the top page
    :return:
    """
    page = requests.get("https://www.ozbargain.com.au")

    parser = BeautifulSoup(page.text,"html.parser")
    items = parser.find_all(class_ = "node node-ozbdeal node-teaser")

    products = ""

    for i in range(len(items)):
        contain = items[i].find("div","n-right")
        #print(contain.h2["data-title"])
        products += (contain.h2["data-title"] + "\n +\n")
    bot.send_message(chat_id=credentials.chat_acutal_id, text=products)
    #     print(i)

def searchitem(update,conext):
    """
    If user wants to search for item then parses it and finds it
    :param item:
    :return:
    """
    itemSearch = update.message.text
    itemSearch = itemSearch.replace(" ","%20")
    base_url = "https://www.ozbargain.com.au" +"/search/node/"+itemSearch
    page = requests.get(base_url)

    parser = BeautifulSoup(page.text, "html.parser")
    items = parser.find_all("dt","title")

    # print(items[1]
    check = items[0]
    test=check.find("span","tagger expired")

    products = ""
    for i in range(len(items)):
        #print(items[i])
        try:
            itemTitle = items[i].a.img["alt"]
            booleanExpiry = items[i].find("span", "tagger expired")
            if (booleanExpiry == None): # if its None then there is no span class that says its expired
                                                #booleanExpiry.text != "expired"
                products += itemTitle + "\n +\n"
        except: # due to fact that some are discussion we can use try and except to get rid of them
            continue
    if products == "":
        products = "There is not a sale available"
    bot.send_message(chat_id=credentials.chat_acutal_id, text=products)
    #print(itemTitle)

if __name__ == "__main__":
    #topPage()
    bot = telegram.Bot(token=credentials.api_id)
    #searchitem("airpods 1")
    response = Updater(credentials.api_id,use_context= True)
    response.dispatcher.add_handler(CommandHandler("top10",topPage))
    response.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, searchitem))

    response.start_polling()
    response.idle()

