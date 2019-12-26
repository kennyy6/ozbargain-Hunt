import telegram
import credentials
import feedparser
bot = telegram.Bot(token=credentials.api_id)

def top20():
    """
    Sends a text to all the users  about the top 20 deals of the day
    :precondition: None
    :postcondition: None
    :complexity: O(N) where n is the length of the feed entries
    :return: None
    """
    feed =feedparser.parse("https://www.ozbargain.com.au/feed")
    products = ""
    for i in range(len(feed.entries)):
        entry = feed.entries[i].title
        products += (entry+"\n")
    #print (link.find(".//title").text)
    print(products)
    bot.send_message(chat_id= credentials.chat_acutal_id ,text=products)
    #print(bot.get_me())

print(top20())
