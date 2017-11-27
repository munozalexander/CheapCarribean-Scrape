from bs4 import BeautifulSoup
import requests
import datetime
import itertools

class Crawler():
    def __init__(self, earliestDeparture, latestArrival, minNights, maxPrice):
        '''
        earliestDeparture : string, "MM/DD/YYYY"
        latestArrival : string, "MM/DD/YYYY"
        minNights : int, minimum nights to stay
        maxPrice : int, print filtered results below this price
        '''
        self.__minNights = minNights
        self.__maxPrice = maxPrice
        self.__locDict = {274:"Antigua",275:"Aruba",379:"Bahamas, Abaco",305:"Bahamas, Grand Bahama",\
                          306:"Bahamas, Nassau",377:"Bahamas, Nassau & Paradise Island",307:"Bahamas: Paradise Island",\
                          277:"Barbados",345:"Belize",308:"Bermuda",279:"Bonaire",313:"BVI Tortola",281:"Cayman Islands",\
                          366:"Costa Rica, Arenal",363:"Costa Rica, Guanacaste",353:"Costa Rica, Puntarenas",367:"Costa Rica, San Jose",\
                          369:"Costa Rica, Tambor",282:"Curacao",317:"DR, Romana",284:"DR, Puerto Plata",362:"DR, Puerto Plata/Santiago",\
                          316:"DR, Punta Cana",350:"DR, Samana",318:"DR, Santo Domingo",285:"Grenada",373:"Haiti",309:"Jamaica",\
                          321:"Mexico, Cancun",374:"Mexico, Cancun & Riviera Maya",322:"Mexico, Cozumel",\
                          349:"Mexico, Huatulco",323:"Mexico, Ixtapa",342:"Mexico, Los Cabos",341:"Mexico, Manzanillo",\
                          324:"Mexico, Mazatlan",326:"Mexico, Puerto Vallarta",375:"Mexico, Puerto Vallarta & Riviera Nayarit",\
                          327:"Mexico, Riviera Maya",325:"Mexico, Riviera Nayarit",290:"Nevis",359:"Nicaragua",344:"Panama",291:"Puerto Rico",\
                          358:"Roatan",297:"St Kitts",303:"St Lucia",298:"St Martin",301:"Turks & Caicos",294:"USVI St Croix",\
                          296:"USVI St John",376:"USVI St John & St Thomas",304:"USVI St Thomas"}
        depart_date = [int(a) for a in earliestDeparture.split('/')]
        self.__earliestDeparture = datetime.date(depart_date[2], depart_date[0], depart_date[1])
        arrival_date = [int(a) for a in latestArrival.split('/')]
        self.__latestArrival = datetime.date(arrival_date[2], arrival_date[0], arrival_date[1])
        self.__possDates = [] #determine possible date-ranges
        for delta1 in range((self.__latestArrival-self.__earliestDeparture).days-self.__minNights+1):
            d0 = self.__earliestDeparture+datetime.timedelta(days=delta1)
            self.__possDates += list(itertools.product([d0],[d0+datetime.timedelta(days=i) \
                                for i in range(self.__minNights,(self.__latestArrival-d0).days+1)]))

    def __generateURL(self, loc_id, depart_date, return_date, num_people=2, num_rooms=1):
        ''' generate urls '''
        base = "https://www.cheapcaribbean.com/search/vacation-packages.html?"
        people = "".join(["searchParameters.rooms%5B0%5D.persons%5B"+str(i)+"%5D=25&" for i in range(num_people)])
        constant = "searchParameters.bookingType=P&searchParameters.maxPrice=&searchParameters.nonStop=false&searchParameters.departureAirport=BOS&"
        location = "searchParameters.localeId="+str(loc_id)+"&"
        departing = "searchParameters.leaveDate="+str(depart_date.month)+"%2F"+str(depart_date.day)+"%2F"+str(depart_date.year)+"&"
        returning = "searchParameters.returnDate="+str(return_date.month)+"%2F"+str(return_date.day)+"%2F"+str(depart_date.year)+"&"
        rooms = "searchParameters.noOfRooms="+str(num_rooms)+"&"
        all_inclusive = "searchParameters.allInclusive=true&_searchParameters.allInclusive=on"
        url = base+people+constant+location+departing+returning+rooms+all_inclusive
        return url

    def __parse(self, url):
        ''' parse html from a given url '''
        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content, 'html.parser')
        block = str(soup.body.findAll('script')[1].get_text())
        elements = [elt.split(':') for elt in block.split(',')]
        return elements

    def __extractPrices(self, url):
        ''' extract prices from url '''
        elements = self.__parse(url)
        prices = []
        for elt in elements:
            if elt[0]=='\"price\"':
                price = int(elt[1].split('.')[0][1:])
                prices.append(price)
        return prices

    def crawl(self):
        ''' crawl and scrape '''
        for loc_id in self.__locDict.keys():
            for depart_date, return_date in self.__possDates:
                url = self.__generateURL(loc_id, depart_date, return_date)
                prices = self.__extractPrices(url)
                prices = filter(lambda y:y<self.__maxPrice, prices)
                if len(prices)>0:
                    print self.__locDict[loc_id], ':', depart_date, '->', return_date, '('+str((return_date-depart_date).days)+')'
                    print 'Prices:', prices, '\n\n'

if __name__ == '__main__':
    crawler = Crawler(earliestDeparture = '3/10/2018', \
                      latestArrival = '3/18/2018', \
                      minNights = 4, \
                      maxPrice = 850)
    crawler.crawl()
