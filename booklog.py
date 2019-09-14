import bs4 as bs
import requests
import datetime
from matplotlib import pyplot as plt
import numpy as np


book_objects = []


class Books:

    def __init__(self, splitlist):
        self.title = splitlist[0]
        self.author = splitlist[1]
        self.pages = int(splitlist[2])
        self.date = str(splitlist[3])
        book_objects.append(self)


def readmemory():
    with open('log.txt', 'r', encoding = 'UTF-8') as file:
        for line in file.read().splitlines():
            Books(line.split('*'))
try:
    readmemory()
except:
    pass
#reads in the data from the text file and makes them objects of the Books class
        
def search(title):
    try:
        title.replace(' ','+')
        gr = 'https://goodreads.com/'
        url = gr + 'search?q=' + title

        source = requests.get(url)
        source = source.content
        soup = bs.BeautifulSoup(source,'html5lib')
        book_url = soup.find('span', {'itemprop' : 'name'}).find_parent('a').get('href')
        book_source = requests.get(gr + book_url).text
#Here the program searches the title on good reads, then gets the link of the first result, and gets the text of the page the link leads to

        soup = bs.BeautifulSoup(book_source,'html5lib').find('div', {'id' : 'metacol'})
        pages = soup.find('span',{'itemprop' : 'numberOfPages'}).text[:-5]
        author = soup.find('span',{'itemprop' : 'name'}).text
        title = soup.find('h1',{'id' : 'bookTitle'}).text[7:-1]
#Here it just scrapes the information about the book that I want to log

        return [title,author,pages]
        
    except(NameError,AttributeError):
        return (False)

def add(title, datefinished = 'Today'):
    if datefinished == 'Today':
        datefinished = datetime.date.today()
    with open('log.txt', 'a', encoding = 'utf-8') as file: 
        try:
            results = search(title)   
            results.append(datefinished)
            file.write('{}*{}*{}*{}\n'.format(results[0], results[1] ,results[2] , results[3]))
            Books(results)
            
        except(TypeError):
            print('Unable to find a book with that title')
    print('done')
#writes the data the search function returns into a txt file

def remove():
    for book in book_objects:
        print(book_objects.index(book), '{} by {}'.format(book.title, book.author))
    inp = int(input('Please enter the index of the book that you would like to remove '))
    for book in book_objects[:]:
        if book_objects.index(book) == inp:
            book_objects.pop(inp)
            break

    with open('log.txt', 'w', encoding = 'UTF-8') as file:
        for book in book_objects:
            file.write('{}*{}*{}*{}\n'.format(book.title, book.author, book.pages, book.date))
            
#reads in the bookdata, takes an input of a book index, overwrites the bookdata, without the book of the inputted index
            
def booksread():
    for book in book_objects:
        print('{} by {}, {} pages long, finished on {}'.format(book.title, book.author, book.pages, book.date))
    
def plotmonthly():
    monthly = []
    for book in book_objects:
        if book.date[:-3] not in [x[0] for x in monthly]: #I use slicing here because the date includes the exact day too, but we don't need that for a monthly plot
            monthly.append([book.date[:-3], book.pages])
        else:
            for l in monthly:
                if l[0]  == book.date[:-3]:
                    l[1] += book.pages
                    
#sums up the total pages read each month
                    
    monthly.sort(key = lambda x : x[0]) #sorts monthly chronologically
    pos = np.arange(len(monthly))
    plt.style.use('seaborn-colorblind')
    plt.bar(pos, [x[1] for x in monthly])
    plt.xticks(pos, [x[0] for x in monthly])
    plt.title('Number of pages read each month')
    plt.xlabel('Month')
    plt.ylabel('Pages read')
    plt.show()
#plots the data

def plotyearly(year = 'This year'):
    if year == 'This year':
        now = datetime.date.today()
        year = now.year

    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    up_to_month =[['{}-{}'.format(year, month), 0] for month in months]

    for l in up_to_month:
        try:
            l[1] += next_month #adds the previous months pages to the current one, it's in a try block, because the first one obviously can't do that
        except:
            pass
        
        for book in book_objects:
            if book.date[:-3] == l[0]: #slicing again because we dont need the day
                l[1] += book.pages
        next_month = l[1]

    month_name =['January','February','March','April','May','June','July','August','September','October','November','December']
    plt.style.use('seaborn-colorblind')
    plt.title('Total number of pages read throughout the year {}'.format(year))
    plt.xlabel('Month')
    plt.ylabel('Pages read')
    plt.plot(month_name,[x[1] for x in up_to_month])
    plt.show()
#this function works almost the same way as the previous one, the only difference is that it takes the previous months pagessum and adds it to the current month, this way we can track our progress throughout the year
