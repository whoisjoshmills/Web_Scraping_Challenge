# Dependencies
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_mars():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Define and vist html
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Parse
    html = browser.html
    soup = bs(html, 'html.parser')

    # Capture first news title
    titles = soup.find_all('div', class_ = "content_title")
    news_title = titles[0].text

    #Capture news title paragraph
    paragraphs = soup.find_all('div', class_= "article_teaser_body")
    news_p = paragraphs[0].text

    # Quit browser
    browser.quit()

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Define and vist html
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # Parse
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find source path
    img = soup.find('img', class_='headerimage')
    source = img['src']

    # Combine html and source to get url of image file
    featured_image_url = f'{url}{source}'

    # Quit browser
    browser.quit()

    return_dict = {}
    return_dict['news_title'] = news_title
    return_dict['news_p'] = news_p
    return_dict['featured_image_url'] = featured_image_url
    #return_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return return_dict



def hemispheres():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Define and vist html
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Parse
    html = browser.html
    soup = bs(html, 'html.parser')

    # Create blank list of products
    products_lst = []

    # Find h3 tags
    products = soup.find('div', class_='collapsible results')
    h3 = products.find_all('h3')

    # Append h3 text to products list
    for item in h3:
        products_lst.append(item.text)
    products_lst


    # Create list of urls we will need to add to original url and visit
    url_lst = []

    # Condense text to code we need
    url_text = products.find_all('a')

    # Iterate through to click into final page
    for products in products_lst:
        
        # Parse
        html = browser.html
        soup = bs(html, 'html.parser')
        
        #print(products)
        browser.links.find_by_partial_text(products).click()
        
        # Parse second layer
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # Find link tag
        lis = soup.find('li')
        href = lis.find('a')['href']
        new_url = f'{url}{href}'
        
        # Append new url to list
        url_lst.append(new_url)
        
        browser.visit(url)
       
    # Create dictionary of title and image url
    hemisphere_image_urls = []

    # Add hemisphere and image link to dictionary
    for x in range(0,len(products_lst)):
        my_dict = {'title': products_lst[x], 'img_url': url_lst[x]}
        hemisphere_image_urls.append(my_dict)

    browser.quit()

    return hemisphere_image_urls


def mars_html():

    # Define url
    url = "https://galaxyfacts-mars.com/"

    # Read url into tables
    tables = pd.read_html(url)
    mars_df = tables[0]

    # Clean DataFrame
    # Create new row to add to top of dataframe
    new_row = pd.DataFrame({0:"Description", 1:"", 2:""}, index=[0])

    # Concat new row to mars_df
    mars_df = pd.concat([new_row, mars_df])

    # Extract first column and save for index
    index_series = mars_df.loc[:,0].tolist()

    # Rename column headers
    mars_df = mars_df.rename(columns={1:"Mars",2:"Earth"})

    # Set index first column
    mars_df = mars_df.set_index(0)

    # Rename column headers
    mars_df.index.name = None

    # Render to html
    mars_html = mars_df.to_html()

    # Eliminate \n
    mars_html = mars_html.replace('\n', '')

    # Save table
    mars_df.to_html('comparison.html')
    
    return mars_html
