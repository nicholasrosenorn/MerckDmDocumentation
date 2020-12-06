import schedule
import time
import pandas as pd

def f1():
    df = pd.DataFrame()
    df["Weight (in lbs)"] = ['133', '133', '133','134','134']
    df["Heart Rate (bpm)"] = ['90', '86', '85', '90', '68']

    df["Sleep (hours"] = ['7', '9', '8', '7', '9']
    df["Biometric Data"] = ['70', '90', '80', '70', '90']
    df["Calories"] = ['2333', '1789', '1500', '2430', '1000']

    df.index = ['10/26', '10/27', '10/28', '10/29', '10/30']

    print(df)


def f2():
    print("Current data based:")

    df = pd.DataFrame()


    df["Weight (in lbs)"] = ['130', '131', '131','132','134']
    df["Heart Rate (bpm)"] = ['85', '70', '85', '90', '68']

    df["Sleep (hours"] = ['7', '9', '8', '7', '9']
    df["Biometric Data"] = ['70', '90', '80', '70', '90']
    df["Calories"] = ['2534', '2345', '1800', '1923', '1999']

    df.index = ['10/21', '10/22', '10/23', '10/24', '10/25']

    print(df)

schedule.every(5).seconds.do(f2)
schedule.every(5).seconds.do(f1)



while 1:
    schedule.run_pending()
    time.sleep(1)