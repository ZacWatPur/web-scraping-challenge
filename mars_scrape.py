
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    # Setting up windows browser with chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    mars_data = {}

    #URL to be scraped
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all('div', class_="content_title")

    # A blank list to hold the headlines
    news_titles = []
    # Loop over div elements
    for result in results:
        # Identify the anchor...
        if (result.a):
            # And the anchor has non-blank text...
            if (result.a.text):
                # Append thext to the list
                news_titles.append(result)
    
    finalnewstitles = []
    # Print only the headlines
    for x in range(6):
        var=news_titles[x].text
        newvar = var.strip('\n\n')
        finalnewstitles.append(newvar)

    #Find classification for description paragraph below title
    presults = soup.find_all('div', class_="rollover_description_inner")

    news_p = []
    # Loop through the div results to pull out just the text
    for x in range(6):
        var=presults[x].text
        newvar = var.strip('\n\n')
        news_p.append(newvar)
    
    #add titles and paragraphs to dictionary
    mars_data['news_titles'] = finalnewstitles
    mars_data['news_p'] = news_p



    #Mars Space Image
    # Assigning url for image capture
    urlI = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    response = requests.get(urlI)

    html = response.text

    mars_image = BeautifulSoup(html, 'html.parser')

    # Making html more understandable

    print(mars_image.prettify())

    # locating images
    images = mars_image.find_all('a', class_ = "showimg fancybox-thumbs")
    images

    # assigning image specific path
    pic = "image/featured/mars1.jpg"

    # creating url for image    
    feature_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + pic




	#Mars Facts
    url = 'https://space-facts.com/mars/'
    response3 = requests.get(url)
    soup = BeautifulSoup(response3.text, 'html.parser')

    # Pulling table info
    mars_tables = pd.read_html(url)

    
    # transforming to dataframe for alterations
    mars_df = mars_tables[0]

    
    # renaming columns
    mars_df.columns = ['Statistic', 'Measurement']


    # stripping out the :
    mars_ser = pd.Series(mars_df['Statistic'])
    mars_df['Statistic'] = mars_ser.str.strip(':')


    # setting Statistic as the index
    mars_df = mars_df.set_index('Statistic')

    # putting df back into html table
    html_mars_table = mars_df.to_html()
    
    # saving table
    mars_df.to_html('mars_html_table.html')


    # Setting url for alternate browser
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    nextpage_urls = []
    imgtitles = []
    base_url = 'https://astrogeology.usgs.gov'

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain hemisphere photo info
    divs = soup.find_all('div', class_='description')

    counter = 0
    for div in divs:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        link = div.find('a')
        href=link['href']
        img_title = div.a.find('h3')
        img_title = img_title.text
        imgtitles.append(img_title)
        next_page = base_url + href
        nextpage_urls.append(next_page)
        counter = counter+1
        if (counter == 4):
            break

    # Creating loop for high resolution photo on next page
    the_images=[]
    for nextpage_url in nextpage_urls:
        url = nextpage_url
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        link2 = soup.find('img', class_="wide-image")
        forfinal = link2['src']
        full_img = base_url + forfinal
        the_images.append(full_img)
        nextpage_urls = []
    
    # Creating final list of dictionaries
    hemisphere_image_urls = []

    cerberus = {'title':imgtitles[0], 'img_url': the_images[0]}
    schiaparelli = {'title':imgtitles[1], 'img_url': the_images[1]}
    syrtis = {'title':imgtitles[2], 'img_url': the_images[2]}
    valles = {'title':imgtitles[3], 'img_url': the_images[3]}

    hemisphere_image_urls = [cerberus, schiaparelli, syrtis, valles]

    #adding to dict
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data

if __name__ == "__main__":
    scrape()
