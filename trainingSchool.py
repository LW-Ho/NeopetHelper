
from bs4 import BeautifulSoup
import re, web, Constants

class TrainingSchool():
    def __init__(self, session):
        self.session = session
        self.codestones = []

    def checkStone(self, htmlText, petName):
        soup = BeautifulSoup(htmlText , "html.parser")
        div = soup.findAll("td", {"class": "content"})
        rows = div[0].findAll('td', {'width': 250} )

        for row in rows:
            if(row.text.find("Codestone") > -1) and (row.find('a', {'href':re.compile(petName)})) :
                result = row.findAll('b')
                for codestone in result:
                    if(codestone.text.find("Codestone") > -1):
                        self.codestones.append(codestone.text)

        return self.codestones
