import bs4 as bs
import requests
import datetime
from matplotlib import pyplot as plt
import numpy as np

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
        pages = soup.find('span',{'itemprop' : 'numberOfPages'}).text
        author = soup.find('span',{'itemprop' : 'name'}).text
        title = soup.find('h1',{'id' : 'bookTitle'}).text[7:-1]
#Here it just scrapes the information about the book that I want to log

        return [title,author,pages]
        
    except(NameError,AttributeError):
        return (False)

def add(title, datefinished = 'Today'):
    if datefinished == 'Today':
        datefinished = str(datetime.datetime.now())[:10]
    with open('log.txt', 'a', encoding = 'utf-8') as log: 
        try:
            for prop in search(title):
                log.write(prop+'*')
            log.write(datefinished)   
            log.write('\n')
        except(TypeError):
            print('couldnt find a book with that name sorry brah')
    print('done')
#writes the data the search function returns into a txt file

def remove():
    with open('log.txt','r', encoding = 'utf-8')as file:
        bookdata = file.read().splitlines()
        for index,book in enumerate(bookdata):
            print((index,book.split('*')[0] + ' by ' +book.split('*')[1]))
        done = False
        while not done:
            inp = input('Which book would you like to remove?(Index)')
            try:
                inp = int(inp)
                done = True
            except(ValueError):
                print('Please enter a number.')
        
        for index,book in enumerate(bookdata[:]):
            if inp == index:
                bookdata.remove(book)
    
    with open('log.txt','w', encoding = 'utf-8') as file:
        for line in bookdata:
            file.write(line + '\n')
#reads in the bookdata, takes an input of a book index, overwrites the bookdata, without the book of the inputted index
            
def booksread():
    with open('log.txt','r', encoding = 'utf-8') as file:
        bookdata = file.read().splitlines()
        for book in bookdata:
            print('{} by {}, {} pages long, finished on {}'.format(book.split('*')[0],book.split('*')[1],book.split('*')[2],book.split('*')[3]))
    
def plotmonthly():
    with open('log.txt','r', encoding = 'utf-8') as file:
        bookdata = file.read().splitlines()
        splitdata = [[int(book.split('*')[2].split(' ')[0]),book.split('*')[3]] for book in bookdata]
#reads in the log file and makes a list out of the lists that contains the pages and the dates finished
        monthly = []
        
        for book in splitdata:
            book[1] = book[1][:-3]
            if len(monthly) > 0:
                done = False
                for i in monthly:
                    if i[1] == book[1]:
                        i[0] += book[0]
                        done = True
                        break
                if not done:
                    monthly.append(book)
            else:
                monthly.append(book)
#using the list that it constructed above sums up the total pages read each month
        monthly.sort(key = lambda x : x[1])
        pos = np.arange(len([x[0] for x in monthly]))
        plt.style.use('seaborn-colorblind')
        plt.bar(pos, [x[0] for x in monthly])
        plt.xticks(pos, [x[1] for x in monthly])
        plt.title('Number of pages read each month')
        plt.xlabel('Month')
        plt.ylabel('Pages read')
        plt.show()
#plots the data

def plotyearly(year = 'This year'):
    if year == 'This year':
        now = datetime.datetime.now()
        year = now.year
        
    with open('log.txt','r', encoding = 'utf-8') as file:
            bookdata = file.read().splitlines()
            splitdata = [[int(book.split('*')[2].split(' ')[0]),book.split('*')[3]] for book in bookdata]

            pages_read = 0
            month = ['01','02','03','04','05','06','07','08','09','10','11','12']
            
            up_to_month = [['{}-{}'.format(year,month[index]),0] for index in range(0,12)]
            for index in range(0,12):
                if index > 0:
                    up_to_month[index][1] += up_to_month[index-1][1]
                for book in splitdata[:]:
                    if book[1][:-3] == up_to_month[index][0]:
                        up_to_month[index][1] += book[0]
                        splitdata.remove(book)

            month_name =['January','February','March','April','May','June','July','August','September','October','November','December']
            plt.style.use('seaborn-colorblind')
            plt.title('Total number of pages read throughout the year {}'.format(year))
            plt.xlabel('Month')
            plt.ylabel('Pages read')
            plt.plot(month_name,[x[1] for x in up_to_month])
            plt.show()
#this function works almost the same way as the previous one, the only difference is that it takes the previous months pagessum and adds it to the current month, this way we can track our progress throughout the year
