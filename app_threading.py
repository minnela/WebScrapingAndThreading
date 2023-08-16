import threading
import time
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

LIMIT = 10

def getWordCloud(text,url):
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

def parseArticle(url):
    categoryListInThreadOrder.append(url)
    print("Downloading {}".format(url))
    soup= getContentOfSite(url)
    ps=soup.find_all('p')
    text= "\n".join(p.get_text() for p in ps)
    texts.append(text)
    getWordCloud(text,url)

def getContentOfSite(url):
    response = requests.get(url= url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def getCategoryAndTitleList(categoriesSoup, id):
    allCategories = categoriesSoup.find(id=id).find_all("a")
    for category in allCategories:
        if '#' not in category['href'] and category.string not in [None, 'None']:
            categoryTitleList.append(category.string)
            categoryList.append(category['href'])
            categorydict[category['href']]= category.string
    return categoryList, categoryTitleList


@app.route('/')
def home():
    start = time.time()

    categoriesSoup = getContentOfSite("https://www.bbc.com/")
    categoryList, categoryTitleList = getCategoryAndTitleList(categoriesSoup,"orb-header")
    
    threads = [threading.Thread(target=parseArticle, args=(url,)) for url in categoryList]
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
          print(f"{categoryLink} is not in List.")

    print("Elapsed Threading Time: %s" % (time.time() - start))
    return render_template('home.html', clouds=cloudListInThreadOrder, categoryList=categoryListInThreadOrder, categoryTitleList=categoryTitleListInThreadOrder)