import sqlite3
import requests
from bs4 import BeautifulSoup


# Git tutorial
# install git
# create repsitory in github

# go to git bash
# git config --global user.name "Prabesh Sunuwar"
# git config --global user.email "prabeshjr1234567890@gmail.com"

# git init
# git status => if you want to check what are the status of the files
# git diff . => if you want to check what are the changes
# git add . 
# git commit -m "Finished Project"
# copy paste git code from github


#####################################
# 1. change the code 
# 2. git add .
# 3. git commit -m "Your message"
# 4. git push origin
#####################################

def create_database():
  conn = sqlite3.connect("books.sqlite3")
  cursor = conn.cursor()
  cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT,
      price REAL,
      currency TEXT 
    )
    """
  )
  conn.commit()
  conn.close()

def insert_book(title, price, currency):
  conn = sqlite3.connect("books.sqlite3")
  cursor = conn.cursor()
  cursor.execute(
    """
      INSERT INTO books (title, price, currency) VALUES (?, ?, ?)
    """,
    (title, price, currency),
  )
  conn.commit()
  conn.close()




def scrape_book(url):
  response = requests.get(url)
  if response.status_code != 200:
    return
  
  #Set encoding explicitly to handle special characters
  response.encoding = response.apparent_encoding

  soup = BeautifulSoup(response.text, "html.parser")
  books = soup.find_all("article", class_="product_pod")
  for book in books:
    title = book.h3.a["title"]
    price_text = book.find("p", class_="price_color").text
    currency = price_text[0]
    price = price_text[1:]
    insert_book(title, price, currency)
  
create_database()
scrape_book("https://books.toscrape.com/")