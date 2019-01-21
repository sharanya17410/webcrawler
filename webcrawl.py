import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from collections import OrderedDict

driver = webdriver.Chrome(executable_path="C:\\Users\\sharanya\\AppData\\Local\\Programs\\chromedriver.exe")

def getBookLink(link, depth):
    result = []
    if depth >= 1:
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        all_link = [a["href"] for a in soup.find_all('a', href=True)]
        for a in all_link:
            link = 'https://www.flipkart.com' + a
            if 'pid' in link:
                result.append(link)
                result += getBookLink(link, depth - 1)
    return result


def getBook(book_links):
    # "_3eAQiD" - book title
    # " bzeytq _3cTEY2 - book description"
    # "hGSR34 _2beYZw - book rating"
    file = open(r'bookdetails.json', 'w', encoding='utf-8')
    file.write('{"Books":[')
    for book in book_links:
        ordict = OrderedDict()
        driver.get(book)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        ordict["Name"] = ""
        ordict["Description"] = ""
        ordict["Rating"] = ""
        if soup.find_all('h1', class_="_9E25nV"):
            name = str(soup.find_all('h1', class_="_9E25nV")[0].text) #title
            ordict["Name"] = name
            print(name)
        else:
            continue
        if soup.find_all('div', class_="_3la3Fn"):
            description = str(soup.find_all('div', class_="_3la3Fn")[0].text) # description
            ordict["Description"] = description
            print(description)
        if soup.find_all('div', class_="_1i0wk8"):
            rating = str(soup.find_all('div', class_="_1i0wk8")[0].text)  # rating
            ordict["Rating"] = rating
            print(rating)
        json.dump(ordict, file)
        file.write(',\n')

    file.write(']}')
    file.close()


link = "https://www.flipkart.com/books-store"
#For getting book link
# book_links = list(set(getBookLink(link,2)))
# bl = open("books.txt", "w")
# for a in book_links:
#     bl.write(a+"\n")
file = open("books.txt", "r")
links = file.read().split("\n")
getBook(links)








