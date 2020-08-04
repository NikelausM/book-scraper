import requests

from pages.all_books_page import AllBooksPage

URL = "http://books.toscrape.com"

page_content = requests.get(URL).content
page = AllBooksPage(page_content)

books = page.books
