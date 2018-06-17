import requests, bs4
import openpyxl
import re
from bs4 import BeautifulSoup
url_pre=('https://www.banggood.com/Wholesale-Smartphones-c-1567-0-1-1-44-0_page')
url_post=('.html')
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'Spam Spam Spam'
iteration=0
#################################################
for i in range (1, 10):
    print('iteracja nr. '+str(i))
    res = requests.get(url_pre+str(i)+url_post)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    exampleSoup = bs4.BeautifulSoup(res.text,'html.parser')
    type(exampleSoup)
    hyper=[0]
    k=0
    elems = exampleSoup.select('div ul li span > a')
    for j in range (1, len(elems)):
        if elems[j-1].attrs['href']!=elems[j].attrs['href'] and j>12:
            if (('reviews') in str(elems[j].attrs['href']))==0:
                hyper.append(elems[j])
                k=k+1
                sheet.cell(row=k+iteration*44, column=1).value = k
                sheet.cell(row=k+iteration*44, column=2).value = hyper[k].attrs['href']
    ##########################################
    for m in range (1, 44):
        res = requests.get(hyper[m].attrs['href'])
        try:
            res.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        exampleSoup = bs4.BeautifulSoup(res.text,'html.parser')
        type(exampleSoup)
            ###########################################################################
        for n in range (1, 4):     
            elems = exampleSoup.select('div meta')
        price =float(elems[5].attrs['content'])
        sheet.cell(row=m+iteration*44, column=3).value = float(price)
        

    ##############################
        links = []
        for link in exampleSoup(text=re.compile(r'([0-9]+mah)',re.IGNORECASE)):
            links.append(link.replace(u'\xa0', u' ').strip())
            aa=re.compile(r'([0-9]+mah)',re.IGNORECASE)
            mo=aa.search(links[0])
            battery=int(re.sub('[^0-9]','',mo.group()))
        sheet.cell(row=m+iteration*44, column=4).value = int(battery)
###########################################################
#for link in exampleSoup(text=re.compile(r'[*]\d{1,2}[.]\d{1,2}mm',re.IGNORECASE)):
   # links.append(link.replace(u'\xa0', u' ').strip())
  #  battery=int(re.sub('[^0-9]','',links[0]))
    #print(battery)
    #s=re.sub('[^0-9*.]','',links[1])[:6]
#################################################
    #sheet.cell(row=i, column=1).value = i
    #sheet.cell(row=i, column=2).value = elems[0].getText()
    iteration=iteration+1
    

wb.save('banggood.xlsx')
    
