import requests
from  bs4 import BeautifulSoup
from wordcloud import WordCloud
import base64
import io
from flask import Flask, render_template
import time

app = Flask(__name__)

def getContentOfSite(url):
    response = requests.get(url= url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def getCategoryAndTitleList(categoriesSoup, id):
    categoryList = []
    categoryTitleList = []
    allCategories = categoriesSoup.find('div', id=id).find_all('a')

    for category in allCategories:
        if '#' not in category['href'] and category.string not in [None, 'None']:
            categoryTitleList.append(category.string)
            categoryList.append(category['href'])
    return categoryList, categoryTitleList

def parseArticle(article_url):
    print(f"Downloading {article_url}")
    soup = getContentOfSite(article_url)
    ps = soup.find_all('p')
    text = "\n".join(p.get_text() for p in ps)
    return text

def getWordCloud(text):
    pil_img = WordCloud()
    wordCloud = pil_img.generate(text=text).to_image()
    img = io.BytesIO()
    wordCloud.save(img,"PNG")
    img.seek(0)
    img_b64=base64.b64encode(img.getvalue()).decode()
    return img_b64


@app.route('/')
def home():
    start = time.time()

    clouds = []
    categoriesSoup = getContentOfSite("https://www.bbc.com/")
    categoryList, categoryTitleList = getCategoryAndTitleList(categoriesSoup, 'orb-header')

    newCategoryList = []
    newCategoryTitleList = []

    for categoryLink, categoryTitle in zip(categoryList, categoryTitleList):
        if '#' not in categoryLink and categoryTitle not in [None, 'None']:
            text = parseArticle(categoryLink)
            if text not in ['', None]:
                newCategoryList.append(categoryLink)
                newCategoryTitleList.append(categoryTitle)
                cloud = getWordCloud(text)
                clouds.append(cloud)

    print("Elapsed Threading Time: %s" % (time.time() - start))                
    return render_template('home.html', clouds=clouds, categoryList=newCategoryList, categoryTitleList=newCategoryTitleList)