{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup\n",
    "import requests\n",
    "from selenium import webdriver\n",
    "import time\n",
    "import pandas as pd\n",
    "from tqdm.notebook import tqdm\n",
    "import datetime\n",
    "import pickle\n",
    "import numpy as np\n",
    "from selenium.webdriver.chrome.options import Options "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "def scroller(browser):   \n",
    "    lenOfPageOld = browser.execute_script(\"window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;\")\n",
    "    match=0\n",
    "    while(match <= 10):\n",
    "        time.sleep(2)\n",
    "        lenOfPageNew = browser.execute_script(\"window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;\")\n",
    "        if lenOfPageNew == lenOfPageOld:            \n",
    "            match+=1\n",
    "        else:\n",
    "            match = 0\n",
    "        lenOfPageOld = lenOfPageNew"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "def contentScraper(new_links):\n",
    "    ans_list = []\n",
    "    for link in tqdm(new_links):\n",
    "        ans_dict = {}\n",
    "        # Get link raw html, beautify\n",
    "        content = requests.get(link)\n",
    "        soup = BeautifulSoup(content.text, 'html.parser')\n",
    "        # Get container for both name and price\n",
    "        productNameContainer = soup.find('div', class_ = 'infos')\n",
    "        # Beautify previous container raw html\n",
    "        smallProdNameContainer = BeautifulSoup(str(productNameContainer), 'html.parser')\n",
    "        # Get raw name from beautified html\n",
    "        filtered_smallName_container = smallProdNameContainer.find('h1', {'itemprop' : 'name'})\n",
    "        # Clean raw name \n",
    "        cleanName = filtered_smallName_container.text.strip()\n",
    "        # Dictionary with two colums: Name -> Product name; Price -> Product price\n",
    "        ans_dict['ProductLink'] = link\n",
    "        ans_dict['ProductName'] = cleanName\n",
    "        ans_dict['ScrapeDate'] = cleanDate\n",
    "        ans_dict['Source'] = motherUrl\n",
    "        # Store dictionary data as list\n",
    "        ans_list.append(ans_dict)\n",
    "    return ans_list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "flatten = lambda l: [item for sublist in l for item in sublist]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "date = datetime.datetime.now().timestamp()\n",
    "cleanDate = datetime.datetime.fromtimestamp(date)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Run all highlighted after running script once (for base data)\n",
    "# df_previous = pd.read_csv(\"crossroads.csv\", index_col = 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Open on ChromeDriver, beautify and store html\n",
    "options = Options()  \n",
    "options.add_argument(\"--headless\")  \n",
    "browser = webdriver.Chrome(options = options)\n",
    "base_url = 'https://crossroad.com/en/shop/products/'\n",
    "motherUrl = 'https://crossroad.com/'\n",
    "browser.get(base_url)\n",
    "time.sleep(4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "source = browser.page_source\n",
    "soup = BeautifulSoup(source, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "scrolled": false
   },
   "outputs": [],
   "source": [
    "# Get category links\n",
    "subcat_container = soup.find_all('ul', {'class' : 'subcategories'})\n",
    "btfSubcat_container = BeautifulSoup(str(subcat_container), 'html.parser')\n",
    "rawLinks = btfSubcat_container.find_all('a', {'href' : True})\n",
    "pureLinks = [i['href'] for i in rawLinks]\n",
    "fullPureLinks = [motherUrl + link for link in pureLinks]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "e3dee8ac71874380b57b3d67232b1912",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HBox(children=(FloatProgress(value=0.0, max=207.0), HTML(value='')))"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "ename": "KeyboardInterrupt",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mKeyboardInterrupt\u001b[0m                         Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-10-e62a51155538>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      5\u001b[0m     \u001b[0mbrowser\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mget\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mlink\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      6\u001b[0m     \u001b[0mtime\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msleep\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;36m4\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 7\u001b[1;33m     \u001b[0mscroller\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mbrowser\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      8\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      9\u001b[0m     \u001b[0msource\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mbrowser\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mpage_source\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m<ipython-input-2-940e735d5a13>\u001b[0m in \u001b[0;36mscroller\u001b[1;34m(browser)\u001b[0m\n\u001b[0;32m      3\u001b[0m     \u001b[0mmatch\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;36m0\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      4\u001b[0m     \u001b[1;32mwhile\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mmatch\u001b[0m \u001b[1;33m<=\u001b[0m \u001b[1;36m10\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 5\u001b[1;33m         \u001b[0mtime\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msleep\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;36m2\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      6\u001b[0m         \u001b[0mlenOfPageNew\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mbrowser\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mexecute_script\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m\"window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;\"\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      7\u001b[0m         \u001b[1;32mif\u001b[0m \u001b[0mlenOfPageNew\u001b[0m \u001b[1;33m==\u001b[0m \u001b[0mlenOfPageOld\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mKeyboardInterrupt\u001b[0m: "
     ]
    }
   ],
   "source": [
    "productlinks = []\n",
    "productPrices = []\n",
    "for link in tqdm(fullPureLinks):\n",
    "    browser = webdriver.Chrome(options = options)\n",
    "    browser.get(link)\n",
    "    time.sleep(4)\n",
    "    scroller(browser)\n",
    "    \n",
    "    source = browser.page_source\n",
    "    soup = BeautifulSoup(source, 'html.parser')\n",
    "    \n",
    "    productprice = soup.find_all('div', class_ = 'price')\n",
    "    productprice = productprice[1:]\n",
    "    btfproductprice = BeautifulSoup(str(productprice), 'html.parser')\n",
    "    purePrices = btfproductprice.text.replace(' dram', ' ֏').strip()\n",
    "    productPrices.append(purePrices)\n",
    "    \n",
    "    linkContainer = soup.find_all('div', class_ = 'title')\n",
    "    btfLinkContainer = BeautifulSoup(str(linkContainer), 'html.parser')\n",
    "    rawLinks = btfLinkContainer.find_all('a', {'href' : True})\n",
    "    pureLinkExtensions = [i['href'] for i in rawLinks]\n",
    "    pureFullLinks = [motherUrl + i for i in pureLinkExtensions]\n",
    "    productlinks.append(pureFullLinks)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": false
   },
   "outputs": [],
   "source": [
    "df = pd.DataFrame(productPrices, index = productlinks, columns = [cleanDate])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.to_csv('crossroads.csv', encoding = 'utf-8-sig')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# df_combination = df_previous.merge(df, how = \"outer\", on = df.index).drop_duplicates().set_index(\"key_0\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": false
   },
   "outputs": [],
   "source": [
    "# df_combination.to_csv('crossroads.csv', encoding='utf-8')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# new_links = list(df[~df.index.isin(df_previous.index)].index)\n",
    "# repeating_links = list(df[df.index.isin(df_previous.index)].index)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# # Print for logger\n",
    "# print(str(len(new_links)) + ' new links have been found: ' + str(new_links) + ' and ' + str(len(repeating_links)) + ' repeating links.')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# # Update databse if new links exist\n",
    "# if len(new_links) > 0:\n",
    "#     df_profiles = pd.read_csv(\"crossroadsData.csv\", index_col = 0, encoding='utf-8-sig')\n",
    "#     new_profile = contentScraper(new_links)\n",
    "#     profile_df = pd.DataFrame(new_profile)\n",
    "#     df_combined = pd.concat([df_profiles, profile_df], axis = 1)\n",
    "#     df_combined.to_csv('crossroadsData.csv', encoding='utf-8-sig')\n",
    "#     print('New profiles have been added to database.')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  },
  "toc": {
   "base_numbering": 1,
   "nav_menu": {},
   "number_sections": true,
   "sideBar": true,
   "skip_h1_title": false,
   "title_cell": "Table of Contents",
   "title_sidebar": "Contents",
   "toc_cell": false,
   "toc_position": {},
   "toc_section_display": true,
   "toc_window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
