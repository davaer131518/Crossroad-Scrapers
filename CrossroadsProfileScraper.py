{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup\n",
    "import requests\n",
    "from selenium import webdriver\n",
    "import time\n",
    "import pandas as pd\n",
    "from tqdm.notebook import tqdm\n",
    "import datetime\n",
    "from selenium.webdriver.chrome.options import Options \n",
    "import pymongo\n",
    "from pymongo import MongoClient"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def read_mongoDB(localhost, database, collection):\n",
    "    client = MongoClient(\n",
    "        \"mongodb+srv://davaer:<password>@foodmarket.rrtsu.gcp.mongodb.net/test\"\n",
    "    )\n",
    "    db = client[database]\n",
    "    col = db[collection]\n",
    "    data = pd.DataFrame(list(col.find()))\n",
    "    result = data.drop(\"_id\", axis=1)\n",
    "    return result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def insert_mongoDB(df, localhost, database, collection):\n",
    "    client = MongoClient(\n",
    "        \"mongodb+srv://davaer:<password>@foodmarket.rrtsu.gcp.mongodb.net/test\"\n",
    "    )\n",
    "    db = client[database]\n",
    "    col = db[collection]\n",
    "    col.insert_many(df.to_dict('records'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def contentScraper(pureLinks):\n",
    "    ans_list = []\n",
    "    for link in tqdm(pureLinks):\n",
    "        ans_dict = {}\n",
    "        content = requests.get(link)\n",
    "        soup = BeautifulSoup(content.content, 'html.parser')\n",
    "        # Scrape name\n",
    "        productNameContainer = soup.find('div', class_='infos')\n",
    "        smallProdNameContainer = BeautifulSoup(str(productNameContainer),\n",
    "                                               'html.parser')\n",
    "        filtered_smallName_container = smallProdNameContainer.find(\n",
    "            'h1', {'itemprop': 'name'})\n",
    "        cleanName = filtered_smallName_container.text.strip()\n",
    "        # Scrape sub categories\n",
    "        narrowedSubs = soup.find_all('ul', class_='pathway clear')\n",
    "        btfNarrowedSubs = BeautifulSoup(str(narrowedSubs), 'html.parser')\n",
    "        rawSubs = btfNarrowedSubs.find_all('span', {'itemprop': 'title'})\n",
    "        btfRawSubs = BeautifulSoup(str(rawSubs), 'html.parser')\n",
    "        pureSubs = btfRawSubs.get_text()\n",
    "        resultSub = pureSubs.strip('][').split(', ')\n",
    "        resultSub = ', '.join(resultSub)\n",
    "        # Insert into dict\n",
    "        ans_dict['ProductSub'] = resultSub\n",
    "        ans_dict['ProductLink'] = link\n",
    "        ans_dict['ProductName'] = cleanName\n",
    "        ans_dict['ScrapeDate'] = date\n",
    "        ans_dict['Source'] = motherUrl\n",
    "        # Store dictionary data as list\n",
    "        ans_list.append(ans_dict)\n",
    "    return ans_list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scroller(browser):\n",
    "    lenOfPageOld = browser.execute_script(\n",
    "        \"window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;\"\n",
    "    )\n",
    "    match = 0\n",
    "    while (match <= 10):\n",
    "        time.sleep(2)\n",
    "        lenOfPageNew = browser.execute_script(\n",
    "            \"window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;\"\n",
    "        )\n",
    "        if lenOfPageNew == lenOfPageOld:\n",
    "            match += 1\n",
    "        else:\n",
    "            match = 0\n",
    "        lenOfPageOld = lenOfPageNew"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "flatten = lambda l: [item for sublist in l for item in sublist]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "date = datetime.datetime.now()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Open on ChromeDriver, beautify and store html\n",
    "options = Options()\n",
    "options.add_argument(\"--headless\")\n",
    "browser = webdriver.Chrome(options=options)\n",
    "base_url = 'https://crossroad.com/en/shop/products/'\n",
    "motherUrl = 'https://crossroad.com/'\n",
    "browser.get(base_url)\n",
    "time.sleep(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Take raw html after scrolling\n",
    "source = browser.page_source\n",
    "soup = BeautifulSoup(source, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Get category links\n",
    "subcat_container = soup.find_all('ul', {'class': 'subcategories'})\n",
    "btfSubcat_container = BeautifulSoup(str(subcat_container), 'html.parser')\n",
    "rawLinks = btfSubcat_container.find_all('a', {'href': True})\n",
    "pureLinks = [i['href'] for i in rawLinks]\n",
    "fullPureLinks = [motherUrl + link for link in pureLinks]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Product Links\n",
    "productlinks = []\n",
    "for link in tqdm(fullPureLinks):\n",
    "    browser = webdriver.Chrome(options=options)\n",
    "    browser.get(link)\n",
    "    time.sleep(5)\n",
    "    scroller(browser)\n",
    "    source = browser.page_source\n",
    "    soup = BeautifulSoup(source, 'html.parser')\n",
    "    productLinkContainer = soup.find_all('div', class_='title')\n",
    "    btfProductLinkContainer = BeautifulSoup(str(productLinkContainer),\n",
    "                                            'html.parser')\n",
    "    rawLinks = btfProductLinkContainer.find_all('a', {'href': True})\n",
    "    purelink_extensions = [i['href'] for i in rawLinks]\n",
    "    fullLinks = [motherUrl + i for i in purelink_extensions]\n",
    "    productlinks.append(fullLinks)\n",
    "finalLinks = flatten(productlinks)\n",
    "pureLinks = list(dict.fromkeys(finalLinks))"
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
    "scraped = contentScraper(pureLinks)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Store as dataframe\n",
    "df = pd.DataFrame(scraped)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Store into databse\n",
    "insert_mongoDB(df, '27017', 'ProfileScraper', 'Crossroad')"
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
