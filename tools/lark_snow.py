# -*- coding: utf-8 -*-

import snotel_soap
# import data_scrape
import datetime
import logging
import pickle



#*********************************************************************************************************

class LARK_SNOW():
    def __init__(self):

        self.verbose = False
        alpine_url =  'http://bridgerbowl.com/weather_api/table/alpine'
        alpine_dict  = {'TOBS':1,'SNWD':6,'WSDV':3,'WSDX':2,"HUMI":4,"NEWS":5}

        andesite_url = 'http://www.mtavalanche.com/weather/yellowstoneclub/andesite'
        andesite_dict  = {'TOBS':3,'SNWD':8,'WDIR':6,'WSDV':4,'WSDX':5}

        self.areas = [ "Bridger Bowl","Big Sky","Red Lodge","Showdown","Discovery","Whitefish"]
        #Andesite would be better for Big Sky but too unreliable?  Need to add the 'refresh' URL to scrape?
        self.site_dict = {"Big Sky":["Lone Mtn"],
                     "Red Lodge":['Cole Creek'],"Bridger Bowl":['Alpine'],
                    "Showdown":['Spur'],"Discovery":['Warmsprings'],
                     "Great Divide":['Nevada'],"Whitefish":['Stahl']
                     }


        self.site_objs ={
                    'Cole Creek':snotel_soap.SnotelSoap('407:MT:SNTL'),
                    #'Andesite':data_scrape.DataScrape(andesite_url,andesite_dict,source='Club',header_len=0,cols=9,time_col=1),
                    'Lone Mtn':snotel_soap.SnotelSoap('590:MT:SNTL'),
                    #'Alpine':data_scrape.DataScrape(alpine_url,alpine_dict,source='Bridger',header_len=10,cols=7),
                    'Spur':snotel_soap.SnotelSoap('781:MT:SNTL'),'Warmsprings':snotel_soap.SnotelSoap('850:MT:SNTL'),
                    'Nevada':snotel_soap.SnotelSoap('903:MT:SNTL'),'Stahl':snotel_soap.SnotelSoap('787:MT:SNTL')
                    }


        #non site-specific stuff
        self.data_codes = ['TOBS','SNWD','PREC','NEWS']  #Observed Temp, Snow Depth, Water Eq., Precipitation  ,'WSDV','WSDX'
        #data_codes = ['SNWD']
        self.code_names = {'TOBS':'Temperature','SNWD':'Snow Depth','PREC':'Precip To Date',
                      'NEWS':'New Snow'}
        self.units = {'TOBS':'deg F','SNWD':'inches','PREC':'inches','NEWS':'inches'}

    def depth_transfer(self,value):
        pwm_val = 255*value/120.0
        if pwm_val > 255:
            pwm_val = 255
        if pwm_val < 0:
            pwm_val = 0
        return int(pwm_val)

    def new_transfer(self,value):
        pwm_val = 255*value/12.0
        if pwm_val > 255:
            pwm_val = 255
        if pwm_val < 0:
            pwm_val = 0
        return int(pwm_val)

    def temp_transfer(self,value):
        pwm_val = 255*(value+20)/70.0
        if pwm_val > 255:
            pwm_val = 255
        if pwm_val < 0:
            pwm_val = 0
        return int(pwm_val)

    def empty_snow(self):
        sd = {}
        ns = {}
        tp = {}
        for area in self.areas:
            print area
            sd[area]=0
            ns[area]=0
            tp[area]=0
        return sd,ns,tp


    def update_snow(self,snowdepth,newsnow,temper):
        now = datetime.datetime.now()
        if now.minute <10:
            minute = '0'+str(now.minute)
        else:
            minute = str(now.minute)
        time = str(now.month) + '-' + str(now.day) + '-' + str(now.year) + '  ' + str(now.hour) + ':' + minute
        logstr = 'Updating Snow at: ' + str(time)
        logging.info(logstr)
        print logstr

        #baro = baro.baro('http://w1.weather.gov/obhistory/KBZN.html')
        #data is in baro.data

        for area in self.areas:
            print area
            if self.verbose:
                logging.warning("Starting " + area)

            for num,site in enumerate(self.site_dict[area]):
                print '  ' +site
                if self.verbose:
                    logging.info("  Collecting " + site)

                #get the data
                site_obj = self.site_objs[site]
                try:

                    site_obj.connect()
                    site_obj.getAllHourlyData(self.data_codes,1)
                except:
                    logging.error("   Error connecting to " + site)

                #only continue if data is fresh
                if site_obj.fresh:

                    for elem in self.data_codes:
                        try: #this catches sites that don't have the given elem
                            if site_obj.data_dict[elem] != []:
                                if self.verbose:
                                    logging.info("   Data received from " + site + ': ' + elem)

                            else:
                                print '     Error collecting data from: ' + str(site)
                                logging.error("   Error collecting data from " + site + ': ' + elem)
                        except:
                            pass


                    try:
                        depth = site_obj.data_dict['SNWD'][-1]
                        snowdepth[area] = self.depth_transfer(depth)
                        print '     Snow Depth: ' + str(depth)
                        print '     Snow Depth PWM: ' + str(snowdepth[area])
                    except:
                        logging.error('No SNWD at: '+site)
                        print '     No SNWD'

                    try:
                        new_snow = site_obj.data_dict['NEWS'][-1]
                        if new_snow < 0:
                            new_snow = 0

                        newsnow[area]=self.new_transfer(new_snow)
                        print '     New Snow: '+ str(new_snow)
                        print '     New Snow PWM: '+ str(newsnow[area])

                    except:
                        try:
                            new_snow = site_obj.data_dict['SNWD'][-1] - site_obj.data_dict['SNWD'][-24]  #changed to -24 since BB only goes back that far
                            if new_snow < 0:
                                new_snow = 0

                            newsnow[area]=self.new_transfer(new_snow)
                            print '     New Snow: '+ str(new_snow)
                            print '     New Snow PWM: '+ str(newsnow[area])

                        except:
                            logging.error('No Snow Report at: '+site)
                            print '     No Snow report'

                    try:
                        temp = site_obj.data_dict['TOBS'][-1]
                        temper[area]=self.temp_transfer(temp)
                        print '     Temp: ' + str(temp)
                        print '     Temp PWM: ' + str(temper[area])


                    except:
                        logging.error('No Temperature at: '+site)
                        print '     No Temperature Reported'
                    #this is where the pickle saving happened

                else:
                    logging.error(str(site)+ " has old data. Zeroing!")
                    #zero the data out so that in the spring things get zeroed!
                    snowdepth[area] = 0
                    newsnow[area] = 0
                    temper[area] = 0

        snow_pickle = open(r'snow.pkl','w')
        pickle.dump(snowdepth, snow_pickle)
        pickle.dump(newsnow, snow_pickle)
        pickle.dump(temper, snow_pickle)
        snow_pickle.close()

        #for generating fake data for debugging
        if False:
            for count,area in enumerate(self.areas):
                snowdepth[area]=250-count*40
                temper[area]=250-count*40
                newsnow[area]=250-count*40


        print 'Finished Updating Snow!'
        return






#************************************************************************************************************

if __name__ == "__main__":

    '''
    snowdepth = {"Big Sky":0,"Red Lodge":0,"Bridger Bowl":0,"Showdown":0,"Discovery":0,"Whitefish":0}
    newsnow = {"Big Sky":0,"Red Lodge":0,"Bridger Bowl":0,"Showdown":0,"Discovery":0,"Whitefish":0}
    temper = {"Big Sky":0,"Red Lodge":0,"Bridger Bowl":0,"Showdown":0,"Discovery":0,"Whitefish":0}
    '''

    logging.basicConfig(filename='snow.log',level=logging.WARNING)

    f = open(r'snow.pkl')
    snowdepth = pickle.load(f)
    newsnow = pickle.load(f)
    temper = pickle.load(f)
    f.close()

    ls = LARK_SNOW()
    ls.update_snow(snowdepth,newsnow,temper)

    f = open(r'snow.pkl')
    snowdepth = pickle.load(f)
    newsnow = pickle.load(f)
    temper = pickle.load(f)
    f.close()

    print snowdepth
    print newsnow
    print temper


    '''
    ls = LARK_SNOW()
    snowdepth,newsnow,temper = ls.empty_snow()
    print snowdepth
    print newsnow
    print temper
    '''