import json
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import sqlite3
import os

# Підключення до бази
conn = sqlite3.connect("cars.db") 
cursor = conn.cursor()

# Створюєм базу
def include(filename):
    if os.path.exists(filename):
        exec(open(filename).read())
include('db.py')

print ("Сканування....")

pageNumber = 1

try:
    # Рік
    minFirstRegistrationDate = [2010,2011,2012,2013,2014,2015,2016,2017,2018]
    date = minFirstRegistrationDate[7]
    # Тип заправлення
    fuels = ["DIESEL","ELECTRICITY","LPG","PETROL"]
    fuel = fuels[0]
    # Коробка передач
    transmissions=["AUTOMATIC_GEAR","MANUAL_GEAR","SEMIAUTOMATIC_GEAR"]
    trans = transmissions[1]
    # Категорія
    categories = ["Cabrio","EstateCar","Limousine","OffRoad","SmallCar","SportsCar","Van"]
    categorie = categories[5]
except:
    print ("Задайте існуючі в списку значення...")
    exit()

allTitle = []
allDisc = []
allPrice = []

# Створюєм ексел файл
workbook = xlsxwriter.Workbook('Cars.xlsx')
worksheet = workbook.add_worksheet()

# from cars.models import Car
# c = Car(title="1",descriptions="1",producer="1",model="1",year="1",price="1",img="1")
# c.save()
# Car.objects.all().delete()

def saveDB(title,descriptions,producer,model,year,price,img):
    cursor.execute("""INSERT INTO cars_car (title,descriptions,producer,model,year,price,img) 
                  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (title,descriptions,producer,model,year,price,img)
               )
    conn.commit()

def getUrl(pageN):
    #Задаємо посилання на сайт магазину та на апі сайта з курсом валют
    cours = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20180726&json"
    url = "https://suchen.mobile.de/fahrzeuge/search.html?categories=%s&damageUnrepaired=NO_DAMAGE_UNREPAIRED&fuels=%s&isSearchRequest=true&makeModelVariant1.makeId=1900&makeModelVariant1.modelId=31&minFirstRegistrationDate=%d&pageNumber=%d&scopeId=C&transmissions=%s" % (categorie,fuel,date,pageN,trans)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    info = requests.get(url, headers = headers)
    course = requests.get(cours)
    # print("Сорінка: ", url)
    func(info.text, course.text)

def func(info,course):
    texts = BeautifulSoup(info, 'lxml')

    boxes = texts.find_all('div', {"class":["cBox-body--resultitem","cBox-body--eyeCatcher"]})
    pag = texts.find('ul', {"class":"pagination"})
    boxN = len(pag)-1
    pages = texts.select_one("ul.pagination > li:nth-of-type(%d) > span" % boxN).text

    jstr = json.loads(course)[0]["rate"]

    for t in boxes:
        title = t.find('span', {"class":"h3 u-text-break-word"}).text
        allTitle.append(title)
        try:
            descriptions = t.find('div', {"class":"vehicle-data--ad-with-price-rating-label"}).text
        except:
            descriptions = t.find('div', {"class":"g-col-12"}).text
        allDisc.append(descriptions)

        producer = title[0:4]
        model = title[5:7]
        year = descriptions[0:10]
        img = 'https:%s' % (t.find('div', {'class': 'image-block'}).find('img').get('src'))

        prices = t.find('span', {"class":"h3 u-block"})
        price = str(round(round(float(prices.text[:-2])*1000)*jstr,2)) + ' UAH'
        allPrice.append(price)

        saveDB(title,descriptions,producer,model,year,price,img)

        #Виводим данні про авто
        # print("Авто - '",title,"'\n Опис - '",descriptions,"'\n Ціна (грн) - '",price,"'")
    print("Знайдених авто : ",len(allTitle),"\n")
    
    global pageNumber
    while pageNumber <= int(pages):
        pageNumber += 1
        getUrl(pageNumber)
        if pageNumber == int(pages):
            exit()

    count = "SELECT COUNT(title) FROM cars_car"
    cursor.execute(count)
    print(cursor.fetchall())

    #Виводимо число знайдених авто та кількість сторінок
    print ('Авто - ',len(allTitle),', Сторінок - ',int(pages)+1)

    # Біжимо по масиву і записуєм дані у файл
    # for i in range(len(allTitle)):
    #     worksheet.write('A'+str(i+1), allTitle[i])
    # for i in range(len(allDisc)):
    #     worksheet.write('B'+str(i+1), allDisc[i])
    # for i in range(len(allPrice)):
    #     worksheet.write('C'+str(i+1), allPrice[i])

    # Закриваєм файл
    workbook.close()
    cursor.close()
    conn.close()
    print ("Кінець... Дані збережено в файлі 'Cars.xlsx'")

getUrl(pageNumber)
