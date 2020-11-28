import threading
import time

import feedparser
import requests
import base64
import io

from flask import Flask
from  bs4 import BeautifulSoup
from flask import render_template
from wordcloud import WordCloud

app = Flask(__name__)

categoryList= []
categoryTitleList=[]
categoryListInThreadOrder=[]
categoryTitleListInThreadOrder=[]
cloudListInThreadOrder=[]
categorydict={}
cloudDict ={}
texts = []
wordClouds = []

BBC_FEED = "http://feeds.bbci.co.uk/news/world/rss.xml"
LIMIT = 10

def get_wordcloud(text,url):
    if(text!= ''):
      print(' Turning into word cloud')
      pil_img = WordCloud()
      wordCloud=pil_img.generate(text=text).to_image()
      img= io.BytesIO()
      wordCloud.save(img,"PNG")
      img.seek(0)
      img_b64=base64.b64encode(img.getvalue()).decode()
      cloudDict[url] = img_b64
      wordClouds.append(img_b64)
    else:
        print('Passing this text')

def parse_article(url):
    categoryListInThreadOrder.append(url)
    print("Downloading {}".format(url))
    soup= getContentOfSite(url)
    ps=soup.find_all('p')
    text= "\n".join(p.get_text() for p in ps)
    texts.append(text)
    get_wordcloud(text,url)

def getContentOfSite(url):
    response = requests.get(url= url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Get all categories of news
def getCategoryAndTitleList(categoriesSoup, id):
    allCategories = categoriesSoup.find(id=id).find_all("a")
    for category in allCategories:
        if (category['href'] != "#orb-footer"):
            categoryTitleList.append(category.string)
            categoryList.append(category['href'])
            categorydict[category['href']]= category.string
    return categoryList, categoryTitleList


@app.route('/')
def home():
    categoriesSoup = getContentOfSite("https://www.bbc.com/")
    categoryList, categoryTitleList = getCategoryAndTitleList(categoriesSoup,"orb-nav-links")

    start = time.time()
    threads = [threading.Thread(target=parse_article, args=(url,)) for url in categoryList]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for categoryLink in categoryListInThreadOrder:
      try:
           categoryTitle = list(categorydict.values())[list(categorydict.keys()).index(categoryLink)]
           cloud = list(cloudDict.values())[list(cloudDict.keys()).index(categoryLink)]
           categoryTitleListInThreadOrder.append(categoryTitle)
           cloudListInThreadOrder.append(cloud)
      except:
          print(categoryLink, " is not in List.")

    print("Elapsed Time: %s" % (time.time() - start))

    return render_template('home.html', clouds=cloudListInThreadOrder, categoryList=categoryListInThreadOrder, categoryTitleList=categoryTitleListInThreadOrder)

@app.route('/breakingNews.html')
def getBreakingNews():
    feed = feedparser.parse(BBC_FEED)
    clouds = []

    for article in feed['entries'][:LIMIT]:
        text = parse_article(article['link'])
        cloud = get_wordcloud(text)
        clouds.append(cloud)
    return render_template('breakingNews.html', breakingNews=clouds)


if __name__ == '__main__':
    app.run('0.0.0.0')
