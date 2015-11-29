from suds.client import Client
from datetime import datetime, timedelta



url = 'http://www.wcc.nrcs.usda.gov/awdbWebService/services?WSDL'


class SnotelSoap():

    def __init__(self,stationID):
        self.stationID = stationID
        self.snotel_elems = ['TOBS','SNWD' ,'WTEQ','PREC']
        self.fresh = True
        self.now = datetime.now()

    def connect(self):
        self.client = Client(url)


    def getElements(self):
        self.elem = []
        elements = self.client.service.getStationElements(self.stationID )
        for e in elements:
            self.elem.append(e['elementCd'])

        return self.elem

    def getHourlyData(self,element,days):
        data = []
        times = []

        #the protocol wants a start and end time
        starttime = (self.now-timedelta(days=days)).strftime("%Y-%m-%d")
        endtime = (self.now+timedelta(days=1)).strftime("%Y-%m-%d")

        #total number of hours to expect data for
        hours = days*24 + int(self.now.strftime('%H'))

        #get the data (where all of the real action happens)
        hourlyData = self.client.service.getHourlyData(self.stationID ,element,ordinal=1,beginDate=starttime,endDate=endtime)

        #this flag gets set to false if data actually exists
        flagged = True

        #if there is real data in the return
        if len(hourlyData[0]) > 3:

            #get the first station (I honestly can't remember what the [0][3] is all about except that I got it working empirically
            station_one = hourlyData[0][3]

            #hours always start at 0 for getHourlyData
            curr_hour = 0
            counter = 0
            last_val = 0
            last_time = 0

            for hour in range(hours):
                #roll back the counter
                if curr_hour > 23:
                    curr_hour = 0

                try:
                    #get the data timestamp
                    data_hour = int(station_one[counter]['dateTime'][-5:-3])

                    #see if it matches the time slot
                    if curr_hour == data_hour:
                        data.append(station_one[counter]['value'])
                        times.append(station_one[counter]['dateTime'])
                        last_val = station_one[counter]['value']
                        last_time = station_one[counter]['dateTime']
                        flagged = False
                        counter += 1
                    #if not, append the last val
                    else:
                        data.append(last_val)
                        times.append(last_time)

                #for the end of the data stream
                except:
                    data.append(last_val)
                    times.append(last_time)
                #increment the counter
                curr_hour +=1

        else:
            print('     No ' + element + ' data returned')

        if flagged:
            #if no data exists, clear it out
            data = []

        #The times dict has the time stamps, the data has the data.
        return times,data


    def getAllHourlyData(self,elem_list,days):
        '''fills data and time dicts for every element in list for given days in past'''
        self.data_dict = {}
        self.time_dict = {}

        element_list= [val for val in elem_list if val in self.snotel_elems]
        for elem in element_list:
            self.time_dict[elem],self.data_dict[elem]=self.getHourlyData(elem,days)

        #since there are redundant time dicts for every data element, I just use the temperature one since I know it is always present
        last_update_day = int(self.time_dict['TOBS'][-1][8:10])
        last_update_month = int(self.time_dict['TOBS'][-1][5:7])
        last_update_year = int(self.time_dict['TOBS'][-1][0:4])
        update_dt = datetime(last_update_year,last_update_month, last_update_day)
        delta = self.now - update_dt

        if delta.days > 7:
            self.fresh = False



if __name__ == "__main__":
    import sys
    #Grab data from the Sacajawea Snotel site
    sac = SnotelSoap('929:MT:SNTL')
    sac.connect()

    #see what elements this site supports (not sure why it returns multiples of the same value)
    print(sac.getElements())
    #Most Snotels don't support all of these data, just testing that they fail in a nice way
    data_codes = ['TOBS','SNWD' ,'WTEQ','PREC','WSDV','WSDX','WDIR','NEWS']

    #get 7 days of hourly data
    sac.getAllHourlyData(data_codes,7)

    #look at hoursly snow depth
    print(sac.data_dict['SNWD'])

    #look at new snow over the past day
    print(sac.data_dict['SNWD'][-1]- sac.data_dict['SNWD'][-24])

    #is it current?
    print(sac.fresh)



'''


Element Code


AIR TEMPERATURE AVERAGE: TAVG
AIR TEMPERATURE MAXIMUM: TMAX
AIR TEMPERATURE MINIMUM: TMIN
AIR TEMPERATURE OBSERVED: TOBS

SNOW DEPTH: SNWD
SNOW WATER EQUIVALENT: WTEQ

SNOW DEPTH AVERAGE: SNWDV
SNOW DEPTH MAXIMUM: SNWDX
SNOW DEPTH MINIMUM: SNWDN

SNOW FALL: SNOW

RELATIVE HUMIDITY: RHUM

BAROMETRIC PRESSURE: PRES
'''
