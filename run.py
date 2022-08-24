from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
import requests
import string
import trafilatura
from spacy import displacy
import en_core_web_sm
nlp = en_core_web_sm.load()

lowerCaseAlphabetlist = list(string.ascii_lowercase)

def main():
    # urlOfInitialWebsiteToScrap = input("Enter the URL you wish to scrape: ")
    urlOfInitialWebsiteToScrap = "https://www.independent.co.uk/travel/news-and-advice/eurostar-kent-ashford-ebbsfleet-brexit-b2150948.html"
    listOfUrlsToVisit = getsListOfURLsToVisit(urlOfInitialWebsiteToScrap)
    listOfNameAndSentances = []
    for url in listOfUrlsToVisit:
        plainTextFromURL = getTextFromURL(url,listOfUrlsToVisit[0])
        if plainTextFromURL != None:
            preparedText = preppingText(plainTextFromURL)
            listOfNamesAndSentances = findPeopleAndTheirSentance(preparedText)
            for i in range(len(listOfNamesAndSentances)):
                listOfNameAndSentances.append(listOfNamesAndSentances[i])
    printResults(listOfNameAndSentances)

def getsListOfURLsToVisit(urlOfInitialWebsiteToScrap):
    listOfUrlsToVisit = [urlOfInitialWebsiteToScrap]
    websiteObj = requests.get(urlOfInitialWebsiteToScrap)
    doc = BeautifulSoup(websiteObj.text, "html.parser")
    tags = doc.find_all('a')
    for i in range(len(tags)):
        subURl = (tags[i].get('href'))
        if subURl != None:
            listOfUrlsToVisit.append(subURl)
    return (listOfUrlsToVisit)

def getTextFromURL(url,initalURL):
    try:
        downloaded = trafilatura.fetch_url(url)
        return (trafilatura.extract(downloaded))
    except Exception as e: 
        try:
            url = initalURL +  url
            downloaded = trafilatura.fetch_url(url)
            return (trafilatura.extract(downloaded))
        except Exception as e:
            print("An error occoured whilst trying to acces this url")
            return None
    
def preppingText(text):
    text = text.replace("\n"," ")
    text = sent_tokenize(text)
    for i in range (len(text)):
        text[i] = nltk.word_tokenize(text[i])
    return text

def findPeopleAndTheirSentance(preparredText):
    lowerCaseListOfAllCountries = ['afghanistan', 'aland islands', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia, plurinational state of', 'bonaire, sint eustatius and saba', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean territory', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african republic', 'chad', 'chile', 'china', 'christmas island', 'cocos (keeling) islands', 'colombia', 'comoros', 'congo', 'congo, the democratic republic of the', 'cook islands', 'costa rica', "côte d'ivoire", 'croatia', 'cuba', 'curaçao', 'cyprus', 'czech republic', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands (malvinas)', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard island and mcdonald islands', 'holy see (vatican city state)', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran, islamic republic of', 'iraq', 'ireland', 'isle of man', 'israel', 'italy', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', "korea, democratic people's republic of", 'korea, republic of', 'kuwait', 'kyrgyzstan', "lao people's democratic republic", 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia, republic of', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia, federated states of', 'moldova, republic of', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands', 'norway', 'oman', 'pakistan', 'palau', 'palestinian territory, occupied', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'réunion', 'romania', 'russian federation', 'rwanda', 'saint barthélemy', 'saint helena, ascension and tristan da cunha', 'saint kitts and nevis', 'saint lucia', 'saint martin (french part)', 'saint pierre and miquelon', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten (dutch part)', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia and the south sandwich islands', 'spain', 'sri lanka', 'sudan', 'suriname', 'south sudan', 'svalbard and jan mayen', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan, province of china', 'tajikistan', 'tanzania, united republic of', 'thailand', 'timor-leste', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks and caicos islands', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'united states minor outlying islands', 'uruguay', 'uzbekistan', 'vanuatu', 'venezuela, bolivarian republic of', 'viet nam', 'virgin islands, british', 'virgin islands, u.s.', 'wallis and futuna', 'yemen', 'zambia', 'zimbabwe']
    blackListOfNonNames = ['agobookmark_bordersharemore_vert','incognito','this privacy policy','gmail','maps','keyboard input','recipes','blogger','bbc','bcc','cc', 'gb','metro','norwich','blu-ray','malawi','mouse','locomotive']
    blackListOfNonNames = blackListOfNonNames + lowerCaseListOfAllCountries
    listOfNamesAndSentances = []
    for i in range(len(preparredText)):
        sentanceList = []
        for j in range(len(preparredText[i])):
            sentanceList.append(preparredText[i][j])    
        sentance = ' '.join(sentanceList)
        doc = nlp(sentance)
        entsList = []
        for ents in doc.ents:
            entsList.append(ents.label_)
        for i in range(len(entsList)):
            if entsList[i] == "PERSON" and doc.ents[i].text.lower() not in blackListOfNonNames:
                listOfNamesAndSentances.append((doc.ents[i],sentance))
    return(listOfNamesAndSentances)

def printResults(listOfNameAndSentances):
    for i in range(len(listOfNameAndSentances)):
        print(listOfNameAndSentances[i])

if __name__ == '__main__':
    main()