from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    marsdata = {}
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape the browser into soup and use soup to find the latest news title and paragraph text
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find headlines and articles inside item, inside slide elements
    element = soup.select_one("ul.item_list li.slide")
    marsdata["headline"] = element.find("div",class_="content_title").get_text()
    marsdata["article"] = element.find("div", class_="article_teaser_body").get_text()
    
    browser.quit()

    # # Retrieve Mars featured image 
    url ="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html" 
    browser.visit(url)

    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find class
    soup.find("img", class_="headerimage fade-in").get("src")

    #browser.find_by_xpath(xpath)
    marsdata["img_url"] = browser.find_by_xpath('//img[@class="headerimage fade-in"]')['src'] 

    # Use the requests library to download and save the image from the `img_url` above
    import requests
    import shutil
    response = requests.get(img_url, stream=True)
    with open('feature_image.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    
    # Display the image with IPython.display
    from IPython.display import Image
    
    browser.quit()

    # # Retrieve Mars Facts
    #Use pandas to scrape the table containing facts about Mars
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    table = tables[2]
    table.columns = ['description', 'fact']
    table

    marsdata["html_table"] = table.to_html()

    # # Retrieve Mars Hemisphere Images

    # Get high resolution images for each of Mars' hemispheres from 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = "https://astrogeology.usgs.gov"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    links = soup.find_all("div", class_="item")

    for link in links:
        img_dict = {}
        title = link.find("h3").text
        next_link = link.find("div", class_="description").a["href"]
        full_next_link = base_url + next_link
        
        browser.visit(full_next_link)
        
        pic_html = browser.html
        pic_soup = BeautifulSoup(pic_html, 'html.parser')
        
        url = pic_soup.find("img", class_="wide-image")["src"]

        img_dict["title"] = title
        img_dict["img_url"] = base_url + url
        
        hemisphere_image_urls.append(img_dict)

    marsdata["hemisphere_image_urls"] = hemisphere_image_urls
    
    return marsdata