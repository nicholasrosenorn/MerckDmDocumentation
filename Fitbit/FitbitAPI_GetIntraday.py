#Returns info like:
#'activities-heart-intraday': {
#'dataset': [
#    {'time': '00:00:00', 'value': 66},
#    {'time': '00:00:10', 'value': 67},
#    {'time': '00:00:25', 'value': 67},
#    {'time': '00:00:40', 'value': 67},
#    {'time': '23:57:40', 'value': 84},
#    {'time': '23:58:40', 'value': 85},
#    {'time': '23:58:50', 'value': 80}
#],
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

dummydata = {
    "activities-heart": [
        {
            "customHeartRateZones": [],
            "dateTime": "today",
            "heartRateZones": [
                {
                    "caloriesOut": 2.3246,
                    "max": 94,
                    "min": 30,
                    "minutes": 2,
                    "name": "Out of Range"
                },
                {
                    "caloriesOut": 0,
                    "max": 132,
                    "min": 94,
                    "minutes": 0,
                    "name": "Fat Burn"
                },
                {
                    "caloriesOut": 0,
                    "max": 160,
                    "min": 132,
                    "minutes": 0,
                    "name": "Cardio"
                },
                {
                    "caloriesOut": 0,
                    "max": 220,
                    "min": 160,
                    "minutes": 0,
                    "name": "Peak"
                }
            ],
            "value": "64.2"
        }
    ],
    "activities-heart-intraday": {
        "dataset": [
            {
                "time": "00:00:00",
                "value": 64
            },
            {
                "time": "00:00:10",
                "value": 63
            },
            {
                "time": "00:00:20",
                "value": 64
            },
            {
                "time": "00:00:30",
                "value": 65
            },
            {
                "time": "00:00:45",
                "value": 65
            },
            {
                "time": "00:01:00",
                "value": 64
            },
            {
                "time": "00:01:15",
                "value": 66
            },
            {
                "time": "00:01:30",
                "value": 65
            },
            {
                "time": "00:01:45",
                "value": 63
            },
            {
                "time": "00:02:00",
                "value": 63
            },
            {
                "time": "00:02:15",
                "value": 64
            },
            {
                "time": "00:02:30",
                "value": 65
            },
            {
                "time": "00:02:45",
                "value": 65
            },
            {
                "time": "00:03:00",
                "value": 63
            }
        ],
        "datasetInterval": 1,
        "datasetType": "second"
    }
}
an_array = np.empty(len(dummydata["activities-heart-intraday"]["dataset"]) * 2, dtype=object)
offset = 0

for i in range(0,len(dummydata["activities-heart-intraday"]["dataset"])):
    data = list(dummydata["activities-heart-intraday"]["dataset"][i].values())
    an_array[i + offset] = np.array(data)[0]
    an_array[i + 1 + offset] = np.array(data)[1]
    offset = offset + 1



an_array = np.reshape(an_array, (-1, 2))
myDF = pd.DataFrame(data=an_array, columns=["time", "heart rate"])

myDF['time'] = pd.to_datetime(myDF["time"], format='%H:%M:%S')
myDF['heart rate'] = myDF['heart rate'].astype(int)

plt.close()
plt.plot(myDF["time"], myDF["heart rate"])
plt.autoscale()
plt.title("Intraday Heart Rate")
plt.xlabel("timestamp")
plt.ylabel("heart rate")
plt.show()
