from selenium import webdriver      
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from lxml import html
import time
import random
import datetime
import json

#Right now only works with fox news but is easily changed

data = []
with open('sample.json') as sj:
    data = json.load(sj)



def switchDateToDateTime(strDate):
    splitDate = strDate.split()

    splitDate[1]=splitDate[1].replace(',','')
    switchr = {
        "Jan":1,
        "Feb":2,
        "Mar":3,
        "Apr":4,
        "May":5,
        "Jun":6,
        "Jul":7,
        "Aug":8,
        "Sep":9,
        "Oct":10,
        "Nov":11,
        "Dec":12,
        }

    date = (datetime.datetime(int(splitDate[2]),switchr[splitDate[0]],int(splitDate[1])))

    return date


def getCnnTitles(start,end):     #loads a full webpage based on start and end date Might not work for larger ranges
    TITLE_PARSER = '//*[@class="cnn-search__result-headline"]/a/text()'
    DATE_PARSER = '//*[@class="cnn-search__result-publish-date"]/span[2]/text()'
    BUTTON = '//*[@class="pagination-arrow pagination-arrow-right cnnSearchPageLink text-active"]'

    SITE = "https://www.cnn.com/search?size=10&q=politics&type=article&sort=newest&category=politics"
   


    driver = webdriver.Chrome('C:/Users/Alexb/Downloads/chromedriver_win32/chromedriver.exe')
    driver.get(SITE)
    time.sleep(5)
    
    
    totalTitles = []
    totalDates = []
    


    
    doWeBreakNow = True
    count = 0
    while (doWeBreakNow):
        try:
            print("Made it to button click")
            

            r = driver.page_source
            tree = html.fromstring(r)
            titlesXpath = tree.xpath(TITLE_PARSER)
            dateXPath = tree.xpath(DATE_PARSER)

            for x in dateXPath:

                if(switchDateToDateTime(x)==start):
                    doWeBreakNow = False
                    break;
                
                totalDates.append(switchDateToDateTime(x))
                
                
            loadMoreButton = driver.find_element_by_xpath(BUTTON)
            loadMoreButton.click()

            
            totalTitles+=titlesXpath
            
            time.sleep(random.randrange(1,2))
            count+=1
        except Exception as e:
            print (e)
            count+=1
            break
    print ("Complete")
    time.sleep(3)
    
    
    driver.quit()
    totalDatesStrings = []
    
    titlesAndDates = []
   

    for y in range(len(totalDates)-1):
        doWeBreak = False
        if(len(titlesAndDates)!=0):
            for h in titlesAndDates:
                print(h)
                try:
                    if (totalDates[y].strftime("%Y:%m:%d")==h["date"]):
                        print("It workedasdsafasf")
                        doWeBreak = True
                        break
                except (RuntimeError, TypeError, NameError,Exception):
                        print('rip')
                        pass

        if(doWeBreak):
            continue

        tempTitleList = []

        for j in range(len(totalDates)-1):
            
            if(totalDates[y] == totalDates[j]):
                
                tempTitleList.append(totalTitles[j])
                
                
            
            try:
                tempDict = {
                "date":totalDates[y].strftime("%Y:%m:%d"),
                "titles":tempTitleList,
                "site":"CNN"
                }
            except (RuntimeError, TypeError, NameError):
                print('rip')
                pass
        
        titlesAndDates.append(tempDict)
        print("Done")
        




    return(titlesAndDates)




















def getFoxTitles(start,end):     #loads a full webpage based on start and end date Might not work for larger ranges
    PARSER = '//*[@class="title"]/a[1]/text()'
    BUTTON = '//*[@id="wrapper"]/div[2]/div[2]/div/div[3]/div[2]/a'
    SITE = "https://www.foxnews.com/search-results/search?q=politics"
    print(start.strftime("%d/%m/%y"))
    if(start == datetime.datetime(2020,2,29)):
        return


    driver = webdriver.Chrome('C:/Users/Alexb/Downloads/chromedriver_win32/chromedriver.exe')
    driver.get(SITE)




    time.sleep(5)
    def selections(startdate,enddate):
        letter = ''
        for x in range(2):
            if(x==0):
                letter = "%m"
            if(x==1):
                letter = "%d"  
            timeout = 3
            try:
                element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div[1]/div['+str(1+x)+']/button'))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
            clickedButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div[1]/div['+str(1+x)+']/button')
            clickedButton.click()
            selectionButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div[1]/div['+str(1+x)+']/ul/li['+startdate.strftime(letter)+']')
            selectionButton.click()                         
        for y in range(2):
            if(y==0):
                letter = "%m"
            if(y==1):
                letter = "%d"
            clickedButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div['+str(1+y)+']/button')
            clickedButton.click()
            selectionButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div['+str(1+y)+']/ul/li['+startdate.strftime(letter)+']')
            selectionButton.click()                        
        for j in range(2):
            clickedButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div['+str(1+j)+']/div[3]/button')
            clickedButton.click()
            selectionButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div['+str(1+j)+']/div[3]/ul/li['+str(2021-int(startdate.strftime("%Y")))+']')
            selectionButton.click()
    
    
    
    
    PerPageXPath= '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div[1]/span[1]/text()'
    ResultsXPath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div[1]/span[2]/span/text()'
    
    selections(start,end)
    contentType = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/button')
    contentType.click()
    selectionType = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/ul/li[1]/label')
    selectionType.click()
    searchButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div[2]/div')
    searchButton.click()

    time.sleep(5)
    t = driver.page_source
    treee = html.fromstring(t)
    
    results = (int(str("".join(map(str,treee.xpath(ResultsXPath))).replace(',',''))))
    perpage = (int(str("".join(map(str,treee.xpath(ResultsXPath))).replace(',',''))))

    if(results==0):
        driver.quit()
        return

    amountofClicks = int(results/perpage)
    print("results "+str(results))
    print("Perpage "+str(perpage))
    print(amountofClicks)
    for x in range(amountofClicks):
        try:
            loadMoreButton = driver.find_element_by_xpath(BUTTON)
     
            
            loadMoreButton.click()
            time.sleep(random.randrange(1,3))
        except Exception as e:
            print (e)
            break
    print ("Complete")
    time.sleep(4)
    
    r = driver.page_source
    tree = html.fromstring(r)
    titlesXpath = tree.xpath(PARSER)
    print(PARSER)
    print(titlesXpath)
    driver.quit()
    return(titlesXpath)






def testing(start,end):
    PARSER = '//*[@class="title"]/a[1]/text()'
    BUTTON = '//*[@id="wrapper"]/div[2]/div[2]/div/div[3]/div[2]/a'
    SITE = "https://www.foxnews.com/search-results/search?q=politics"
   


    driver = webdriver.Chrome('C:/Users/Alexb/Downloads/chromedriver_win32/chromedriver.exe')
    driver.get(SITE)
    time.sleep(20)
    def selections(startdate,enddate):
        letter = ''
        for x in range(2):
                          
                                                         
            clickedButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div['+str(1+x)+']/div[2]/button')
            clickedButton.click()
            selectionButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div['+str(1+x)+']/div[2]/ul/li[1]')
            selectionButton.click()                         
        for y in range(2):
            if( int(startdate.strftime('%m'))+y== 13):
                yearss = "1"
            else:
                yearss = str(int(startdate.strftime('%m'))+y)


            clickedButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div['+str(1+y)+']/div[1]/button')
            clickedButton.click()
            selectionButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div['+str(1+y)+']/div[1]/ul/li['+yearss+']')
            selectionButton.click()                        
        for j in range(2):
            thisYear =str(2021-int(startdate.strftime("%Y")))
            if(j==1):
                if((2021-int(startdate.strftime("%Y")))==2):
                    thisYear="1"
                
                    
            clickedButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div['+str(1+j)+']/div[3]/button')
            clickedButton.click()
            selectionButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[3]/div['+str(1+j)+']/div[3]/ul/li['+thisYear+']')
            selectionButton.click()
    
    
    
    
    PerPageXPath= '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div[1]/span[1]/text()'
    ResultsXPath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div[1]/span[2]/span/text()'
    
    selections(start,end)
    contentType = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/button')
    contentType.click()
    selectionType = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/ul/li[1]/label')
    selectionType.click()
    searchButton = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div[2]/div')
    searchButton.click()

    time.sleep(10)
    t = driver.page_source
    treee = html.fromstring(t)
    
    results = (int(str("".join(map(str,treee.xpath(ResultsXPath))).replace(',',''))))
    perpage = (int(str("".join(map(str,treee.xpath(ResultsXPath))).replace(',',''))))

    if(results==0):
        driver.quit()
        return

    amountofClicks = int(results/perpage)
    print("results "+str(results))
    print("Perpage "+str(perpage))
    print(amountofClicks)
    for x in range(13):
        try:
            loadMoreButton = driver.find_element_by_xpath(BUTTON)
     
            
            loadMoreButton.click()
            time.sleep(random.randrange(3,7))
        except Exception as e:
            print (e)
            break
    print ("Complete")
    time.sleep(4)
    
    r = driver.page_source
    tree = html.fromstring(r)
    titlesXpath = tree.xpath(PARSER)
    print(PARSER)
    print(titlesXpath)
    driver.quit()
    return(titlesXpath)
















def getTitlesInRange(start,end,site):   #Gets all the data from webpages within a range
    amountofDates = 0;
    startDate = start
    allTitles =[]
    if(start.strftime("%Y")>end.strftime("%Y")):
        print('wrong date')
    elif (start.strftime("%Y")<end.strftime("%Y")):
        amountofDates=(int(end.strftime("%j"))-int(start.strftime("%j")))
        amountofDates+=365*(int(end.strftime("%Y"))-int(start.strftime("%Y")))
    elif (start.strftime("%Y")==end.strftime("%Y")):
        amountofDates=(int(end.strftime("%j"))-int(start.strftime("%j")))
    if(amountofDates!=0):
        for x in range(amountofDates+1):
            if(site=="Fox"):
                getTitle = getFoxTitles(startDate,startDate)



            tempDateAndTime = {"date":startDate.strftime("%Y:%m:%d"),"titles":getTitle,"site":site}
            allTitles.append(tempDateAndTime)
            startDate += datetime.timedelta(days=1)
            
    return allTitles
#CnnTitles = getCnnTitles(datetime.datetime(2019,12,15),datetime.datetime(2020,6,3))
#CnnJson = json.dumps(CnnTitles,indent=3)
#with open("ScrapedDataCnn.json", "w") as outfiles: 
#    outfiles.write(CnnJson) 
FoxTitles = getTitlesInRange(datetime.datetime(2019,12,15),datetime.datetime(2020,6,3),"Fox")

FoxJson = json.dumps(FoxTitles,indent=3)
with open("ScrapedDataFox.json", "w") as outfilee: 
    outfilee.write(FoxJson) 


#AllTitlesSites.append(FoxTitles + CnnTitles)
#json_object = json.dumps(AllTitlesSites,indent=3)
#with open("ScrapedData.json", "w") as outfile: 
#    outfile.write(json_object) 
