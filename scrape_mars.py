from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    mars = {}

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Assign the text to variables that you can reference later
    news_title = soup.find('div', class_ = 'content_title').text
    news_p = soup.find('div', class_ = 'rollover_description_inner').text

    # Add to dictionary
    mars['news_title'] = news_title
    mars['news_p'] = news_p

    # Visit the url for JPL Featured Space Image
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    image = soup.find('a', class_ = 'fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov'+ image

    mars['featured_image_url'] = featured_image_url

    # Scrape the latest Mars weather tweet from the page
    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Save the tweet text for the weather report as a variable
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars['mars_weather'] = mars_weather

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
    url_4 = 'https://space-facts.com/mars/'

    mars_data = pd.read_html(url_4)
    mars_df = (mars_data[0])
    mars_df.columns = ['Description', 'Data']
    mars_df = mars_df.set_index('Description')

    # Use Pandas to convert the data to a HTML table string
    mars_html = mars_df.to_html(classes='mars-data')
    mars_html = mars_html.replace('\n', ' ')

    mars['mars_html'] = mars_html

    return mars