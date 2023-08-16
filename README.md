# Creating Word Clouds with Flask, BS4, and Threading


## Inspiration

I wanted to play around with threading a bit and I ran across this small project on ![Medium](https://medium.com/analytics-vidhya/web-scraping-using-threading-in-python-flask-aad43edb44a8) by GitHub user ![minnela](https://github.com/minnela) that scrapes news info from the BBC. After some minor fixes (issues with div id's changing on the site) and improvements (errors with some links, not showing running times, not having separate files for threading and original, remove unnecessary files) I was able to get it running again.

## Info 

Basically it is a word cloud generator that takes a URL and returns a word cloud of the most frequently used words on the page using Flask to create a simple web page shows the word cloud. I used BeautifulSoup to scrape the text from the page, and I used threading to speed up the process of scraping the text and generating the word cloud. 

## Running the App

This project uses Python 3.9.17 and the packages listed in the `requirements.txt` file. To install the packages activate your virtual environment and run `pip install -r requirements.txt` in the terminal. Next run `flask --app app run` to start the app that doesn't use threading. Then enter this url in your browser `http://127.0.0.1:5000/`. Then you should see the app running in terminal and the page should load the word clouds. To run the app using threading, simply run `flask --app app_threading run`.


![](/images/result.png)