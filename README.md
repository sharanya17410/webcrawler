# WebCrawler
The project scrapes information about books from the flipkart website - Title , description and ratings and stores in a json file.

Steps to follow :

1. Load the library selenium using pip install -U selenium from your command prompt
2. Load the library beautiful soup using pip install beautifulsoup4
3. Create an empty bookdetails.json file and an empty books.txt file in the folder where you have stored the file webcrawl.py
4. Run the file webcrawl.py - it opens up multiple browsers (here I have used chrome - you could use any web browser of your choice) and starts scraping the information. 
5. Once the project starts running all the links to the books are stored in the file books.txt
6. Each link is picked up and information about each and every book is stored in a json file
7. The empty bookdetails.json file now has all the information about the books that has been scraped.

