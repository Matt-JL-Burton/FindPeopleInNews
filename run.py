from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import requests
import string
import trafilatura
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

lowerCaseAlphabetlist = list(string.ascii_lowercase)

def main():
    # urlOfInitialWebsiteToScrap = input("Enter the URL you wish to scrape: ")
    urlOfInitialWebsiteToScrap = "https://www.theguardian.com/commentisfree/2022/aug/06/davina-maccall-reality-tv-tules-will-you-be-rewatching-big-brother"
    listOfUrlsToVisit = getsListOfURLsToVisit(urlOfInitialWebsiteToScrap)
    listOfNameAndSentances = []
    for url in listOfUrlsToVisit:
        plainTextFromURL = getTextFromURL(url)
        if plainTextFromURL != None:
            textPrepparedForPOSTagging = preparingTextForPOSTagging(plainTextFromURL)
            taggedText = POSTaggingText(textPrepparedForPOSTagging)
            listOfProperNounsAndSentances = getProperNounsAndTheirSentances(taggedText)
            for i in range(len(listOfProperNounsAndSentances)):
                listOfNameAndSentances.append(listOfProperNounsAndSentances[i])
    printResults(listOfNameAndSentances)

def getsListOfURLsToVisit(urlOfInitialWebsiteToScrap):
    listOfUrlsToVisit = [urlOfInitialWebsiteToScrap]
    websiteObj = requests.get(urlOfInitialWebsiteToScrap)
    doc = BeautifulSoup(websiteObj.text, "html.parser")
    tags = doc.find_all('a')
    for i in range(len(tags)):
        subURl = (tags[i].get('href'))
        if subURl[0:4] ==  "http":
            listOfUrlsToVisit.append(subURl)
    return (listOfUrlsToVisit)

def getTextFromURL(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        return (trafilatura.extract(downloaded))
    except Exception as e:
        return None
    
def preparingTextForPOSTagging(text):
    text = text.replace("\n"," ")
    text = sent_tokenize(text)
    for i in range (len(text)):
        text[i] = nltk.word_tokenize(text[i])
    return text

def POSTaggingText(text):
    for i in range (len(text)):
        text[i] = nltk.pos_tag(text[i])
    return text

def getProperNounsAndTheirSentances(taggedText):
    listOfProperNounsAndSentances = []
    for i in range(len(taggedText)):
        sentanceList = []
        proNoun = None
        containsProNoun = False
        containsName = False
        for j in range(len(taggedText[i])):
            if taggedText[i][j][1] ==  "NNP" or taggedText[i][j][1] == "NNPS":
                proNoun = taggedText[i][j][0]
                containsProNoun = True
            sentanceList.append(taggedText[i][j][0])    
        sentance = ' '.join(sentanceList)
        if containsProNoun == True:
            doc = nlp(sentance)
            for ents in doc.ents:
                if ents.label_ == "PERSON":
                    containsName = True
        if containsProNoun == True and containsName == True:
            listOfProperNounsAndSentances.append((proNoun,sentance))
    return(listOfProperNounsAndSentances)

def printResults(listOfNameAndSentances):
    for i in range(len(listOfNameAndSentances)):
        print(listOfNameAndSentances[i])

if __name__ == '__main__':
    main()