#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:18:57 2020

@author: joshuak
"""

#Import the necessary packages
import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import json

#Both the Client ID and Client Secret come from when Fitbit site after registering an app
CLIENT_ID = '22BH28' #Mine:'22BKP3'
CLIENT_SECRET = '78a4838804c1ff0983591e69196b1c46' #Mine:'1a42e97b6b4cc640572ae5cf10a7d0b0'

#Authorization Process
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
refresh_token=REFRESH_TOKEN)


#enter dae you want to get data for
today = str(datetime.datetime.now().strftime("%Y-%m-%d")) #todays date


#gets all Activities Data
def getActivities(myDate): 
    activities = auth2_client.activities(date = myDate)['summary']

    totalDistance = activities['distances'][0]['distance']
    veryActiveDistance = activities['distances'][3]['distance']
    moderatleyActiveDistance = activities['distances'][4]['distance']
    lightlyActiveDistance = activities['distances'][5]['distance']
    veryActiveMinutes = activities['veryActiveMinutes']
    fairlyActiveMinutes = activities['fairlyActiveMinutes']
    lightlyActiveMinutes = activities['lightlyActiveMinutes']
    sedentaryMinutes = activities['sedentaryMinutes']
    floorsClimbed = 0 #activities['floors']
    daySteps =activities['steps']
    
    return totalDistance, veryActiveDistance, moderatleyActiveDistance, lightlyActiveDistance, veryActiveMinutes, fairlyActiveMinutes, lightlyActiveMinutes, sedentaryMinutes, floorsClimbed, daySteps


#gets all Sleep data
def getSleep(myDate): 
    nightSleep = auth2_client.sleep(date = myDate)['sleep']
    
    sleepEfficiency = None
    minutesAsleep = None
    
    if len(nightSleep) != 0:
        sleepEfficiency = nightSleep[0]['efficiency']
        minutesAsleep = nightSleep[0]['minutesAsleep']
        
    return sleepEfficiency, minutesAsleep


#gets all Heart Data
def getHeart(myDate): 
        heartRates = auth2_client.intraday_time_series('activities/heart', base_date=myDate, 
                                                       detail_level='1sec')['activities-heart'][0]['value']

        HRrange30to100 = None
        HRrange100to140 = None
        HRrange140to170 = None
        HRrange170to220 = None
        avgRestingHR = None
        
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
    weight = None
    BMI = None
    if len(grabWeight) > 0:
        weight = grabWeight[0]['weight']
        BMI = grabWeight[0]['bmi']
        
    return weight, BMI


#creates data frame
biometricDF = pd.DataFrame(columns=["Date", "Steps", "Floors Climbed", "Total Miles", "Lightly Active Miles", 
                                    "Moderately Active Miles", "Very Active Miles", "Sedentary Minutes", 
                                    "Lightly Active Minutes", "Fairly Active Minutes", "Very Active Minutes", 
                                    "HR 30-100 Minutes", "HR 100-140 Minutes", "HR 140-170 Minutes", 
                                    "HR 170-220 Minutes", "Average Resting HR"])


#adds data to data frame
def getBiometricData(myDF, myDate):
    totalDistance, veryActiveDistance, moderatleyActiveDistance, lightlyActiveDistance, veryActiveMinutes, fairlyActiveMinutes, lightlyActiveMinutes, sedentaryMinutes, floorsClimbed, daySteps = getActivities(myDate)
    sleepEfficiency, minutesAsleep = getSleep(myDate)
    HRrange30to100, HRrange100to140, HRrange140to170, HRrange170to220, avgRestingHR = getHeart(myDate)
    weight, BMI = getWeight(myDate)
    
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


biometricDF = getBiometricData(biometricDF, today) #append to data frame

#send data in csv format to Merck Directory
biometricDF.to_csv('./' + today + '.csv')

#prints confirmation
print("Python Script Executed")