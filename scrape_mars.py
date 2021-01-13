#!/usr/bin/env python
# coding: utf-8

# Libraries

# In[101]:


#importing libraries to be used
import pandas as pd 
import requests
 #pulling specific library funtions
from splinter import Browser
from bs4 import BeautifulSoup as bs 



# Connecting .exe

# In[127]:

def init_browser():
    #connecting to chrome.exe
    executable_path ={"executable_path" : "chromedriver.exe"}
    return Browser("chrome", **executable_path)


# Nasa Mars News

# In[128]:

def scrape():
    browser = init_browser()
    url_main = "https://mars.nasa.gov/news/"
    response = requests.get(url_main)
    soup= bs(response.text, 'html.parser')


    # In[129]:


    #scrape title and paragraph text
    Title_scrape = soup.find("div", class_ = "content_title").find("a").text
    result = soup.find('div', class_='slide')
    Paragraph_scrape = result.a.text.strip()

    #Display scrape
    #print(Title_scrape)
    #print(Paragraph_scrape)


    # JPL Mars Space Images - Featured Images

    # In[130]:


    #visit site
    url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)


    # In[132]:


    #Html object
    html_Space_image  = browser.html
    soup_space_image = bs(html_Space_image,"html.parser")


    # Find image url ( there is not one )

    # In[133]:


    space_image_featured = soup_space_image.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_webpage_url = "https://www.jpl.nasa.gov"
    featured_image  = main_webpage_url + space_image_featured

    #print(featured_image )


    # Mars Facts

    # In[134]:


    Facts_url = "https://space-facts.com/mars/"
    Facts_table = pd.read_html(Facts_url)


    # In[135]:


    Facts_table_df = Facts_table[0]
    Facts_table_df.columns=['Variables','Mars']
    Facts_table_df


    # In[139]:


    Facts_html =Facts_table_df.to_html(classes='table')
    #print(Facts_html)


    # Mars Hemispheres

    # In[136]:


    Hemipsheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(Hemipsheres_url)


    # In[140]:


    html= browser.html 
    soup = bs(html, "html.parser")


    # In[144]:


    main_hemispheres_url= "https://astrogeology.usgs.gov"
    images = soup.findAll('div',class_='item')
    images_list = []


    # In[149]:


    for x in images:
        title = x.find("h3").text
        image_url = x.find('a',class_="itemLink product-item")["href"]
        browser.visit(main_hemispheres_url + image_url)
        image_html = browser.html
        image_soup = bs(image_html,"html.parser")
        full_url = main_hemispheres_url + image_soup.find("img", class_="wide-image")['src']
        images_list.append({'title': title, 'url': full_url})

        


    # In[150]:
        # create dictionary to hold mars data
    data = {
        'Title_scrape': Title_scrape,
        'Paragraph_scrape': Paragraph_scrape,
        'featured_image': featured_image,
        'Facts_html': Facts_html,
        'image_list': images_list
    }

    browser.quit()

    return data
    #images_list


    # In[ ]:




