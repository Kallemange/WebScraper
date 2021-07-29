# import scraper as sc
import requests
from bs4 import BeautifulSoup
import string
import os

articleTitles = []

def makeArticleList():
    articlePrint = "["
    for article in articleTitles:
        articlePrint += "'"+article+"', "
    articlePrint += "]"
    articlePrint = articlePrint.replace(", ]", "]")
    return articlePrint

def beautifyTitle(title):
    title = str.strip(title)
    translator = str.maketrans(string.punctuation, '#'*len(string.punctuation))
    title = title.translate(translator)
    title = title.replace("#", "")
    return str.replace(title, " ", "_").strip()

def getArticleContent(article, page):
    try:
        soup = BeautifulSoup(article.content, 'html.parser')
        body = soup.find('div', class_=["c-article-body", "article-item__body"])
        # title = soup.find('head').find('title')
        title = soup.find('h1', itemprop="headline").string
        title = beautifyTitle(title)
        if body.text:
            f = open("Page_" + str(page) + "/" + title + ".txt", 'wb')
            f.write(body.text.encode())
        f.close()
        articleTitles.append(title)
    except Exception as e:
        print("Error3: " + str(e))

    return articleTitles

def getArticle(title, page):
    try:
        link = title.find('a', {"data-track-action": "view article"})
        article = requests.get("https://www.nature.com" + link['href'])
        getArticleContent(article, page)
    except Exception as e:
        print("Error2: " + str(e))

def createFolders(no):
    my_dir = os.getcwd()
    for i in range(no):
        if not os.path.isdir(my_dir+'/Page_'+str(i+1)):
            os.mkdir(my_dir+'/Page_'+str(i+1))


def getNature():
    baseURL = "https://www.nature.com/nature/articles"
    # noPages = int(4)
    # articleType = "News"
    noPages = int(input())
    articleType = input()
    searchURL = "/nature/articles?searchType=journalSearch&sort=PubDate&page="

    createFolders(noPages)
    try:
        for page in range(1,noPages+1):
            url = baseURL+searchURL+str(page)
            r = requests.get(url)
            if r:
                soup = BeautifulSoup(r.content, 'html.parser')
                titles = soup.find_all('article')
                for title in titles:
                    article = title.find('span', {"data-test": "article.type"})
                    if article.text.strip() == articleType:
                        getArticle(title, page)

            else:
                raise
    except Exception as e:
        print("Error1: " + str(e))
        return
    print("Saved articles:")
    print(makeArticleList())

def main():
    # print("Input the URL:")
    getNature()
    return

if __name__ == "__main__":
    main()

