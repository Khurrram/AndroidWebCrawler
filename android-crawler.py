#Khurram Hanif
#Stony Brook University

from bs4 import BeautifulSoup
import bs4
import requests
import os


url = "https://developer.android.com/reference/android/app/package-summary"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.findAll('td',attrs={'class':'jd-linkcol'})
pages = []

for table in tables:
    links = table.findAll('a')
    for a in links:
        href = a['href']
        pages.append("https://developer.android.com/" + href)

os.mkdir("outFiles")

def caution_(tag):
    return tag.has_attr('data-version-added') and not tag.has_attr('id')

for url in pages:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.select('h1',attrs={'class':'api-title'})[0].text.strip()
    deprecated = soup.findAll(caution_)
    counter = 0
    for divs in deprecated:
        divnote = divs.find('div',attrs={'class':'note'})

        divname = divs.h3
        cautiontext = divs.select('p.caution')
        notetext = divs.select('p.note')

        if (divname != None and cautiontext != []):
            f = open("outFiles/"+title,"a")
            note = ""
            for text in cautiontext:
                note += str(text.text.strip())
            note = note.replace("\n", "")
            f.write(divname.text + ": " + note +'\n')
            f.close()
        elif (divname != None and notetext != []):
            f = open("outFiles/"+title,"a")
            note = ""
            for text in notetext:
                note += str(text.text.strip())
            note = note.replace("\n", "")
            f.write(divname.text + ": " + note + '\n')
            f.close()
        elif(divnote != None and divname != None):
            f = open("outFiles/"+title,"a")
            for notedivs in divnote:
                note = ""
                for notes in notedivs:
                    for elems in notes:
                            note += str(elems)
                if (note.replace("\n","") != ""):
                    note = note.replace("\n"," ")
                    f.write(divname.text + ": " + note + '\n')
            f.close()



