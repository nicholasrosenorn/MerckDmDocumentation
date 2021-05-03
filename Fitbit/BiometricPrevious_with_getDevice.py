#!/usr/bin/env python
# coding: utf-8


#Import the necessary packages
import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import json

#Both the Client ID and Client Secret come from when Fitbit site after registering an app
CLIENT_ID = '22BT9R' #Mine:'22BKP3'
CLIENT_SECRET = '05b4118998f3230a2963eb11ee081bb6' #Mine:'1a42e97b6b4cc640572ae5cf10a7d0b0'

#Authorization Process
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
refresh_token=REFRESH_TOKEN)


#enter dae you want to get data for
today = str(datetime.datetime.now().strftime("%Y-%m-%d")) #todays date

class FitbitModel1():
    def __init__(self, authClient):
        self.auth2_client = authClient

    #gets all Activities Data
    def getActivities(myDate, myDevice): 
        activities = auth2_client.activities(date = myDate)['summary']

        if(myDevice == 'Versa Lite' or myDevice == 'Ionic'):
            totalDistance = activities['distances'][0]['distance']
            veryActiveDistance = activities['distances'][3]['distance']
            moderatleyActiveDistance = activities['distances'][4]['distance']
            lightlyActiveDistance = activities['distances'][5]['distance']
            veryActiveMinutes = activities['veryActiveMinutes']
            fairlyActiveMinutes = activities['fairlyActiveMinutes']
            lightlyActiveMinutes = activities['lightlyActiveMinutes']
            sedentaryMinutes = activities['sedentaryMinutes']
            floorsClimbed = 'None'
            daySteps = activities['steps']
        if(myDevice == 'Charge 3'):
            totalDistance = activities['distances'][0]['distance']
            veryActiveDistance =  'None'
            moderatleyActiveDistance =  'None'
            lightlyActiveDistance =  'None'
            veryActiveMinutes =  'None'
            fairlyActiveMinutes =  'None'
            lightlyActiveMinutes =  'None'
            sedentaryMinutes = 'None'
            floorsClimbed = 'None'
            try: 
                floorsClimbed = activities['floors']
            except:
                floorsClimbed = 'None'
            daySteps =activities['steps']
        if(myDevice == 'Inspire' or myDevice == 'Inspire HR'):
            totalDistance = activities['distances'][0]['distance']
            veryActiveDistance =  'None'
            moderatleyActiveDistance =  'None'
            lightlyActiveDistance =  'None'
            veryActiveMinutes =  'None'
            fairlyActiveMinutes =  'None'
            lightlyActiveMinutes =  'None'
            sedentaryMinutes =  'None'
            floorsClimbed = 'None'
            daySteps = activities['steps']
        if(myDevice == 'None'):
            totalDistance = 'None'
            veryActiveDistance = 'None'
            moderatleyActiveDistance = 'None'
            lightlyActiveDistance = 'None'
            veryActiveMinutes = 'None'
            fairlyActiveMinutes = 'None'
            lightlyActiveMinutes = 'None'
            sedentaryMinutes = 'None'
            floorsClimbed = 'None'
            daySteps = 'None'
        else:
            totalDistance = activities['distances'][0]['distance']
            veryActiveDistance = activities['distances'][3]['distance']
            moderatleyActiveDistance = activities['distances'][4]['distance']
            lightlyActiveDistance = activities['distances'][5]['distance']
            veryActiveMinutes = activities['veryActiveMinutes']
            fairlyActiveMinutes = activities['fairlyActiveMinutes']
            lightlyActiveMinutes = activities['lightlyActiveMinutes']
            sedentaryMinutes = activities['sedentaryMinutes']
            try: 
                floorsClimbed = activities['floors']
            except:
                floorsClimbed = 'None'
            daySteps =activities['steps']
    
        return totalDistance, veryActiveDistance, moderatleyActiveDistance, lightlyActiveDistance, veryActiveMinutes, fairlyActiveMinutes, lightlyActiveMinutes, sedentaryMinutes, floorsClimbed, daySteps


    #gets all Sleep data
    def getSleep(myDate): 
        nightSleep = auth2_client.sleep(date = myDate)['sleep']
    
        sleepEfficiency = 'None'
        minutesAsleep = 'None'
    
        if len(nightSleep) != 0:
            sleepEfficiency = nightSleep[0]['efficiency']
            minutesAsleep = nightSleep[0]['minutesAsleep']
        
        return sleepEfficiency, minutesAsleep


    #gets all Heart Data
    def getHeart(myDate): 
            heartRates = auth2_client.intraday_time_series('activities/heart', base_date=myDate, 
                                                           detail_level='1sec')['activities-heart'][0]['value']

            HRrange30to100 = 'None'
            HRrange100to140 = 'None'
            HRrange140to170 = 'None'
            HRrange170to220 = 'None'
            avgRestingHR = 'None'
        
            if len(heartRates) == 3:
                HRrange30to100 = heartRates['heartRateZones'][0]['minutes']
                HRrange100to140 = heartRates['heartRateZones'][1]['minutes']
                HRrange140to170 = heartRates['heartRateZones'][2]['minutes']
                HRrange170to220 = heartRates['heartRateZones'][3]['minutes']
                avgRestingHR = heartRates['restingHeartRate']
            
            return HRrange30to100, HRrange100to140, HRrange140to170, HRrange170to220, avgRestingHR


    #gets all Weight Data
    def getWeight(myDate):
        grabWeight = auth2_client.get_bodyweight(base_date = myDate)['weight']
        weight = 'None'
        BMI = 'None'
        if len(grabWeight) > 0:
            weight = grabWeight[0]['weight']
            BMI = grabWeight[0]['bmi']
        
        return weight, BMI

    #adds data to data frame
    def getBiometricData(myDF, myDevice, myDate):
        totalDistance, veryActiveDistance, moderatleyActiveDistance, lightlyActiveDistance, veryActiveMinutes, fairlyActiveMinutes, lightlyActiveMinutes, sedentaryMinutes, floorsClimbed, daySteps = FitbitModel1.getActivities(myDate, myDevice)
        sleepEfficiency, minutesAsleep = FitbitModel1.getSleep(myDate)
        HRrange30to100, HRrange100to140, HRrange140to170, HRrange170to220, avgRestingHR = FitbitModel1.getHeart(myDate)
        weight, BMI = FitbitModel1.getWeight(myDate)
    
        todaysData = {"Date" : myDate, "Steps" : daySteps, "Floors Climbed" : floorsClimbed, "Total Miles": totalDistance, 
                        "Lightly Active Miles": lightlyActiveDistance, "Moderately Active Miles" : moderatleyActiveDistance,
                        "Very Active Miles" : veryActiveDistance, "Sedentary Minutes": sedentaryMinutes, 
                        "Lightly Active Minutes": lightlyActiveMinutes, "Fairly Active Minutes" : fairlyActiveMinutes,
                        "Very Active Minutes" : veryActiveMinutes,"HR 30-100 Minutes" : HRrange30to100, 
                        "HR 100-140 Minutes": HRrange100to140, "HR 140-170 Minutes" : HRrange140to170, 
                        "HR 170-220 Minutes" : HRrange170to220, "Average Resting HR": avgRestingHR, "Sleep Efficiency" : sleepEfficiency,
		        "Weight" : weight, "Minutes Alseep" : minutesAsleep, "BMI" : BMI}

        biometricDF = myDF.append(todaysData, ignore_index=True)

        return biometricDF

    #gets device type/name
    def getDevice():
        devices = auth2_client.get_devices()
        if(len(devices) == 0):
            deviceVersion = 'None'
        else:
            deviceVersion = devices[0]['deviceVersion']    
        return deviceVersion

#creates data frame
biometricDF = pd.DataFrame(columns=["Date", "Steps", "Floors Climbed", "Total Miles", "Lightly Active Miles", 
                                    "Moderately Active Miles", "Very Active Miles", "Sedentary Minutes", 
                                    "Lightly Active Minutes", "Fairly Active Minutes", "Very Active Minutes", 
                                    "HR 30-100 Minutes", "HR 100-140 Minutes", "HR 140-170 Minutes", 
                                    "HR 170-220 Minutes", "Average Resting HR"])

deviceName = FitbitModel1.getDevice()

biometricDF = FitbitModel1.getBiometricData(biometricDF, deviceName, today) #append to data frame

#send data in csv format to Merck Directory
biometricDF.to_csv('C:/Users/Allison/Desktop/School/S7/DATA190/python-fitbit-master' + today + '.csv')

#prints confirmation
print("Python Script Executed")