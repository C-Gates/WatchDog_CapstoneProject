
from newsapi.const import TOP_HEADLINES_URL
from newsapi.newsapi_client import NewsApiClient
from classes.article import Article
import numpy as np

key = '3cfe9505094247e6b1348b3a5533a667'
old_key = '5ef9014fad2647608a531d1971e6e816'
class News():
    def __init__(self):
        self.artiList = []

    def top_headline(self, country_code):
        newsapi = NewsApiClient(api_key=key)
        top_headlines = newsapi.get_top_headlines(country=country_code, category='technology', page_size=5) 
        articles = top_headlines['articles']
        news = []
        i = 0
        #some articles do not have an image and therefore must be skipped
        while (articles[i]['urlToImage'] is None):
            i += 1

        try:
            a = Article(articles[i]["title"], articles[i]["description"], articles[i]["urlToImage"], 
            articles[i]["content"], articles[i]["url"])
        except Exception as E:
            print('no news available')
        self.artiList.append(a)
        news.append(a.get_title())
        news.append(a.get_desc())
        news.append(a.get_url())
        news.append(a.get_id())
        return news

    def news_list(self, country_code='us', categories=['business']):
        #back-up key: 5ef9014fad2647608a531d1971e6e816
        #ee94fab6f9e743ecb0ae7094cabbaf35
        #80b6df1cb3594fadbc6dc481c3cbf334
        #0115244f4ddb4a8291c046b4f09f9601
        #free keys can only be used to call 100 times in 24 hours
        newsapi = NewsApiClient(api_key=key)

        #if no preferences are seleced just select business
        category_len = len(categories)
        if category_len == 0:
            categories = ['business']
            category_len = 1

        ps = int(24/category_len)
        top_headlines = []

        news = []
        desc = []
        img = []
        id = []
        link = []
        cat = []

        for category in categories:
            top_headlines.append(newsapi.get_top_headlines(country=country_code, category=category, page_size=ps))

        index = 0
        for top_headline in top_headlines:
            articles = top_headline['articles']
            num_articles = 12 # starts from 2nd article eg. 6 = article 2 to article 7
            max_num_articles = len(articles) 
            if(num_articles > max_num_articles):
                num_articles = max_num_articles
            num_articles+=1
            i=1
            first_skip = False
            while i <= num_articles and i < max_num_articles:
                my_articles = articles[i]
                i+=1
                if my_articles['urlToImage'] is None or my_articles['content'] is None:
                    num_articles+=1
                    continue

                if not first_skip:
                    first_skip = True
                    continue

                a = Article(my_articles["title"], my_articles["description"], my_articles["urlToImage"],
                my_articles["content"], my_articles["url"])
                self.artiList.append(a)

                id.append(a.get_id())
                news.append(a.get_title())
                desc.append(a.get_desc())
                img.append(a.get_url())
                link.append(a.get_link())
                cat_index = int(np.floor(index/ps))
                cat.append(categories[cat_index])

                index+=1

        news_list = [news, desc, img, id, link, cat]
        news_array = np.asarray(news_list)
        news_array = np.rot90(news_array)
        #shuffle the array in numpy array format in order to randomize the category order
        #otherwise it would be all business then all technology which would look worse
        np.random.shuffle(news_array)
        news_list = news_array.tolist()
        
        return news_list

    #top headline for specific search
    def top_search(self, stock):
        newsapi = NewsApiClient(api_key=key)
        top_headlines = newsapi.get_everything(language='en', q=stock, sort_by='relevancy') 
        articles = top_headlines['articles']
        news = []
        i = 0
        while (articles[i]['urlToImage'] is None):
            i+=1

        try:
            a = Article(articles[i]["title"], articles[i]["description"], articles[i]["urlToImage"], 
            articles[i]["content"], articles[i]["url"])
        except Exception as E:
            print('no news available')
        self.artiList.append(a)
        news.append(a.get_title())
        news.append(a.get_desc())
        news.append(a.get_url())
        news.append(a.get_id())
        return news

    #method for searching the API, similar to the previous but without the need for a category filter
    def stock_news_list(self, stock):
        newsapi = NewsApiClient(api_key=key)
        top_headlines = newsapi.get_everything(language='en', q=stock, sort_by='relevancy')
        articles = top_headlines['articles']
        news = []
        desc = []
        img = []
        id = []
        link = []
        num_articles = 12 # starts from 2nd article eg. 6 = article 2 to article 7
        max_num_articles = len(articles)
        if(num_articles > max_num_articles):
            num_articles = max_num_articles
        num_articles+=1
        i=1
        first_skip = False
        while i <= num_articles and i < max_num_articles:
            my_articles = articles[i]
            i+=1
            if my_articles['urlToImage'] is None or my_articles['content'] is None:
                num_articles+=1
                continue

            if not first_skip:
                first_skip = True
                continue

            a = Article(my_articles["title"], my_articles["description"], my_articles["urlToImage"],
            my_articles["content"], my_articles["url"])
            self.artiList.append(a)
            id.append(a.get_id())
            news.append(a.get_title())
            desc.append(a.get_desc())
            img.append(a.get_url())
            link.append(a.get_link())

        return zip(news, desc, img, id)

        
    def get_artiList(self):
        return self.artiList

    def find_article(self, id):
        found = None
        
        for art in self.artiList:
            
            curr_id = art.get_id()
            if (curr_id == int(id)):
                found = art
        try:
            found.get_title()
            return found
        except Exception as E:
            print("Article does not exist")
