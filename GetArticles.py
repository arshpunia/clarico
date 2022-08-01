import requests
from bs4 import BeautifulSoup
import lxml
import urllib.request
import json
from datetime import datetime 
import os
import time
"""

Make request -> get articles --> parse articles

"""

"""
Makes the request to the XML endpoint and obtains a list of the articles
"""
def makeRequest(url):
    
    response = requests.get(url)
    ##print(response)
    soup = BeautifulSoup(response.text,'xml')
    items = soup.find_all('item')
    ##print(items)
    return items
    
        ##print(firstPara)
    
        
        
        ##print(articleText[1])
        ##print(sample_response['appGip'])
        #fp = urllib.request.urlopen(latestLink)
        #mybytes = fp.read()
        #mystr = mybytes.decode("utf8")
        #fp.close()
        
        #print(mystr)

"""
This method gets the article links
"""
def getLinks(rssFeedItems, cutoffDate): 
    relevantLinks = []
    ##print(rssFeedItems)
    for articles in rssFeedItems:
        ##print(articles.find('pubdate'))
        publicationDate = articles.find('pubDate').contents[0]
        formattedPubDate = datetime.strptime(publicationDate[5:16],"%d %b %Y")
        
        if formattedPubDate >= datetime.strptime(cutoffDate, "%Y-%m-%d"):
            ##print(articles.contents)
            print(articles.find('link').contents[0])
            relevantLinks.append(articles.find('link').contents[0])
            ##relevantLinks.append(articles.contents[4].strip())
            
        
    print("Obtained article links. "+str(len(relevantLinks))+" articles were found!")
    
    return relevantLinks

"""
This method gets all the XML links from the config file
"""

def getXmlLinks(cfgFileName):
    return 0

"""
Accepts articlesList, formats all the articles in the list and compiles them to bookName.epub/mobi

"""
def convertArticles(articlesList, bookName):
    return 0


def parseArticles(articlesList, bookName): 
    count = 1
    firstPara = ""
    for articleLink in articlesList:
        print("Now parsing "+articleLink)
        articleResponse = requests.get(articleLink).text
        text_soup = BeautifulSoup(articleResponse,'html.parser')
        articleItems = text_soup.find('script',type='application/json').contents
            
        json_rep = json.loads(articleItems[0])
            
        """
        How to mine the  thing 
        for children in articleText[0]['children']:
            if children['type'] == "tag":
                for gcs in children['children']:
                    if gcs['type'] == "text":
                        firstPara+=gcs['data']
            elif children['type'] == "text":
                firstPara+=children['data']
        """
            
        publishedDate = json_rep['props']['pageProps']['content'][0]['datePublished']
        articleHeadline = json_rep['props']['pageProps']['content'][0]['headline']
        articleDecription = json_rep['props']['pageProps']['content'][0]['description']
            
        
                
        articleHeading = "## Article"+str(count)+" - "+articleHeadline+"\n"
        firstPara+=articleHeading
        subHeading = "### "+articleDecription+"\n\n"
        firstPara+=subHeading
            
        articleText = json_rep['props']['pageProps']['content'][0]['text']
                
                
        dummyCounter = 0
        for paragraphs in articleText:    
            if paragraphs['type'] == "tag":
                dummyCounter+=1
                ##print(paragraphs['name'])
            for children in paragraphs['children']:
                if children['type'] == "tag":
                    ##print(children['name'])
                    for gcs in children['children']:
                        if gcs['type'] == "text":
                                
                            firstPara+=gcs['data']
                                    
                   
                elif children['type'] == "text":
                    firstPara+=children['data']
                    dummyCounter+=1
                        
            firstPara+="\n\n"
                
        print("Successfully parsed article!\n")
        count+=1
        time.sleep(1)
            
        
    with open(bookName,"w",encoding="utf-8") as f:
        f.write(firstPara)
        print("Generated Markdown file!")
            ##print("Approached the end of the file")
           
    os.system("ebook-convert "+ bookName +" defi.mobi")
    print("Generated Mobi file!")

def obtainArticles(rssItems, cutoffDate):

    count = 1
    firstPara = ""
    for relevantArticles in rssItems:
        
        latestLink = relevantArticles.contents[4].strip()
        print(latestLink)
        articleResponse = requests.get(latestLink).text
        text_soup = BeautifulSoup(articleResponse,'html.parser')
        articleItems = text_soup.find('script',type='application/json').contents
        
        json_rep = json.loads(articleItems[0])
        
        """
        How to mine the  thing 
        for children in articleText[0]['children']:
            if children['type'] == "tag":
                for gcs in children['children']:
                    if gcs['type'] == "text":
                        firstPara+=gcs['data']
            elif children['type'] == "text":
                firstPara+=children['data']
        """
        
        publishedDate = json_rep['props']['pageProps']['content'][0]['datePublished']
        articleHeadline = json_rep['props']['pageProps']['content'][0]['headline']
        articleDecription = json_rep['props']['pageProps']['content'][0]['description']
        
        if datetime.strptime(publishedDate[:10],"%Y-%m-%d") >= datetime.strptime(cutoffDate,"%Y-%m-%d"):
            
            articleHeading = "## Article"+str(count)+" - "+articleHeadline+"\n"
            firstPara+=articleHeading
            subHeading = "### "+articleDecription+"\n\n"
            firstPara+=subHeading
        
            articleText = json_rep['props']['pageProps']['content'][0]['text']
            
            
            dummyCounter = 0
            for paragraphs in articleText:    
                if paragraphs['type'] == "tag":
                    dummyCounter+=1
                    ##print(paragraphs['name'])
                for children in paragraphs['children']:
                    if children['type'] == "tag":
                        ##print(children['name'])
                        for gcs in children['children']:
                            if gcs['type'] == "text":
                            
                                firstPara+=gcs['data']
                                
               
                    elif children['type'] == "text":
                        firstPara+=children['data']
                        dummyCounter+=1
                    
                firstPara+="\n\n"
            
            print(firstPara)
            count+=1
        
        else:
            with open("samplebook.md","w",encoding="utf-8") as f:
                f.write(firstPara)
            print("Generated Markdown file!")
            ##print("Approached the end of the file")
            break
    
def main():
    ##rssLinks = ["https://www.economist.com/china/rss.xml","https://www.economist.com/briefing/rss.xml","https://www.economist.com/finance-and-economics/rss.xml"]
    rssLinks = ["https://www.economist.com/finance-and-economics/rss.xml"]
    
    finArticles = []
    for link in rssLinks:
        finArticles = makeRequest(link)
        
        relevant_articles = getLinks(finArticles,'2022-07-20')
        parseArticles(relevant_articles,"Fin_Aug1.md")

    ##For getting the rss names
    """
    for link in rssLinks:
        tag = link[26:-8]
        formatted = ""
        for kw in tag.split("-"):
            formatted+=kw+" "
        print(formatted)
    """
    
    ##economistLinks = ["https://www.economist.com/business/2022/07/31/apple-already-sold-everyone-an-iphone-now-what"]
    
    ##parseArticles(economistLinks, "Economist_Aug1.md")
    
   
    
    """
    The ideal design would be something like this: 
    - make the request
    - get the links
    - parse the articles, put them under a heading (can be done using a lookup table)
    - append it to the existing document
    - convert it to an ebook once all the links are done
    
    - Arsh, 9/23
    """
if __name__=="__main__":
    main()