import json
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import sqlite3
import os


from django.http import HttpResponse
from django.shortcuts import render
from .models import Car

pageNumber = 0

def index(request):
    cars = Car.objects.all()[:10]
    return render(request, "cars/homePage.html", {'cars': cars})

def load(request):
        if request.method == 'GET':
            _id = int(request.GET['_id'])
            n = _id + 10
            cars = Car.objects.all()[_id:n]
            return render(request, "cars/reload.html", {'cars': cars})
        else:
            return HttpResponse("Request method is not a GET")

def add(request):
    return render(request, "cars/addNew.html")

def search(request):
    global pageNumber
    pageNumber = 1
    Car.objects.all().delete()
    if request.method == 'GET':
        zapravka = request.GET['fuels']
        kpp = request.GET['kpp']
        categories = request.GET['categories']
        year = request.GET['year']
        scanning(year,zapravka,kpp,categories)
        return HttpResponse(len(Car.objects.all()))
    else:
        return HttpResponse("Request method is not a GET")

def scanning(year,zapravka,kpp,categories):
    date = year
    fuel = zapravka
    trans = kpp
    categorie = categories

    def saveDB(title,descriptions,producer,model,year,price,img):
        Car.objects.create(title=title,descriptions=descriptions,producer=producer,model=model,year=year,price=price,img=img)
        
        # c = Car(title=title,descriptions=descriptions,producer=producer,model=model,year=year,price=price,img=img)
        # c.save(force_insert=True)

    def getUrl(pageN):
        #Задаємо посилання на сайт магазину та на апі сайта з курсом валют
        cours = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20180726&json"
        url = "https://suchen.mobile.de/fahrzeuge/search.html?categories=%s&damageUnrepaired=NO_DAMAGE_UNREPAIRED&fuels=%s&isSearchRequest=true&makeModelVariant1.makeId=1900&makeModelVariant1.modelId=31&minFirstRegistrationDate=%d&pageNumber=%d&scopeId=C&transmissions=%s" % (categorie,fuel,int(date),pageN,trans)
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
            try:
                descriptions = t.find('div', {"class":"vehicle-data--ad-with-price-rating-label"}).text
            except:
                descriptions = t.find('div', {"class":"g-col-12"}).text

            producer = title[0:4]
            model = title[5:7]
            year = descriptions[0:10]
            try:
                img = 'https:%s' % (t.find('div', {'class': 'image-block'}).find('img').get('src'))
            except:
                img = 'https://www.namepros.com/a/2018/05/106343_82907bfea9fe97e84861e2ee7c5b4f5b.png'

            prices = t.find('span', {"class":"h3 u-block"})
            price = str(round(round(float(prices.text[:-2])*1000)*jstr,2)) + ' UAH'

            saveDB(title,descriptions,producer,model,year,price,img)
      
        global pageNumber
        while pageNumber <= int(pages):
            pageNumber += 1
            getUrl(pageNumber)
            if pageNumber == int(pages):
                exit()

    getUrl(pageNumber)