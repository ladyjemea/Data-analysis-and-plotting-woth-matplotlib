#pylint: disable=all
#pylint: disable=no-member
import pandas as pd
import numpy as np
from pandas import read_csv
from csv import reader
import datetime as dtm
from datetime import timedelta
import seaborn as sns
sns.set()
import time
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.dates as mdates
import os
np.warnings.filterwarnings('ignore')
from PIL import Image


yr = dtm.datetime.utcnow().year
mo = dtm.datetime.utcnow().month
today =dtm.datetime.utcnow().day
next_day = (dtm.datetime.utcnow() + dtm.timedelta(days=1)).day
time = dtm.datetime.utcnow().replace(microsecond=0)
hour = time.hour
minute = time.minute
date = dtm.datetime(year=yr, month=mo, day=today, hour=hour, minute=minute)


start_time = dtm.datetime(year=yr, month=mo, day=today, hour=0, minute=0)
end_time = start_time + dtm.timedelta(days=1)

start_time_24 = time - dtm.timedelta(days=1)
end_time_24 = time

start_time_48 = time - dtm.timedelta(days=2)
end_time_48 = time

sns.set_style("whitegrid")




'''Magnetometer H_component data'''

#H COMPONENT TROMSØ REALTIME
dfTro = pd.read_csv('../Combined_data/data/magnetometer_tro.csv', sep = " ") #read csv data
dfTro = dfTro.drop_duplicates(subset=['timestamp']) #drop duplicates

dfTro['timestamp'] = pd.to_datetime(dfTro['timestamp']) # convert column to datetime
dfTro.set_index('timestamp', inplace=True) #set column as index

dfTro['year'] = dfTro.index.year
dfTro['month'] = dfTro.index.month
dfTro['day'] = dfTro.index.day
dfTro['hour'] = dfTro.index.hour
dfTro['minute'] = dfTro.index.minute 
dfTro['diff_hour'] = dfTro['hour'].diff() #hour difference between rows
dfTro['diff_day'] = dfTro['day'].diff() #day difference between rows
dfTro['diff_hour'].fillna(0, inplace = True) #replace missing values with zeros
dfTro['diff_day'].fillna(0, inplace = True)

length = len(dfTro.index)-1 #number of rows in the dataframe
for i in range(length):
    if (dfTro.index[i+1]-dfTro.index[i]).seconds >= 300:
        dfTro.loc[dfTro.index[i]+dtm.timedelta(minutes=5)] = float("nan") #insert null values if there are rows where the time difference is above 5 minutes
dfTro.sort_index(inplace=True)

realtime = (dfTro.index >= start_time) & (dfTro.index <= time) #create a new dataframe based on dates
df_real = dfTro.loc[realtime]


#Tromsø H component current plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_real.index, df_real.Horiz_tro)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time, right=end_time)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Tromsø magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/tromso_Hcom_realtime_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/tromso_Hcom_realtime_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/tromso_Hcom_realtime.png')


#ACTIVITY INDEX TROMSØ REALTIME
new_df = pd.read_csv('../Combined_data/data/aiTro.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiTro']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

realtime = (new_df.index >= start_time) & (new_df.index <= time)
df_real = new_df.loc[realtime]

#Tromsø Activity Index current plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_real.index, df_real.aiTro.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time, right= end_time)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Tromsø hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_real['aiTro'].to_list()

for x in max_ai:
    if (x >= 100) and (x < 281):
        plt.axhline(100, color = '#CBE90C')
        plt.text(end_time, 100, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 281) and (x < 481):
        plt.axhline(281, color = '#F6EB14')
        plt.text(end_time, 281, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 481) and (x < 801):
        plt.axhline(481, color = '#FFC800')
        plt.text(end_time, 481, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 801) and (x < 1321):
        plt.axhline(801, color = '#FF9600')
        plt.text(end_time, 801, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1321) and (x < 2001):
        plt.axhline(1321, color = '#FF0000')
        plt.text(end_time, 1321, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2001) and (x < 10000):
        plt.axhline(2001, color = '#C80000')
        plt.text(end_time, 2001, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/tromso_deltaH_realtime_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/tromso_deltaH_realtime_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/tromso_deltaH_realtime.png')




#H COMPONENT DOMBÅS REALTIME
dfDob = pd.read_csv('../Combined_data/data/magnetometer_dob.csv', sep = " ")
dfDob = dfDob.drop_duplicates(subset=['timestamp'])

dfDob['timestamp'] = pd.to_datetime(dfDob['timestamp'])
dfDob.set_index('timestamp', inplace=True)

dfDob['year'] = dfDob.index.year
dfDob['month'] = dfDob.index.month
dfDob['day'] = dfDob.index.day
dfDob['hour'] = dfDob.index.hour
dfDob['minute'] = dfDob.index.minute
dfDob['diff_hour'] = dfDob['hour'].diff()
dfDob['diff_day'] = dfDob['day'].diff()
dfDob['diff_hour'].fillna(0, inplace = True)
dfDob['diff_day'].fillna(0, inplace = True)

length = len(dfDob.index)-1
for i in range(length):
    if (dfDob.index[i+1]-dfDob.index[i]).seconds >= 300:
        dfDob.loc[dfDob.index[i]+dtm.timedelta(minutes=5)] = float("nan")
dfDob.sort_index(inplace=True)

realtime = (dfDob.index >= start_time) & (dfDob.index <= time)
df_real = dfDob.loc[realtime]


#Dombås H component current plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_real.index, df_real.Horiz_dob)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time, right=end_time)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Dombås magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/dombas_Hcom_realtime_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/dombas_Hcom_realtime_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/dombas_Hcom_realtime.png')


#ACTIVITY INDEX DOMBÅS REALTIME
new_df = pd.read_csv('../Combined_data/data/aiDob.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiDob']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

realtime = (new_df.index >= start_time) & (new_df.index <= time)
df_real = new_df.loc[realtime]

#Dombås Activity Index current plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_real.index, df_real.aiDob.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time, right= end_time)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Dombås hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_real['aiDob'].to_list()

for x in max_ai:
    if (x >= 50) and (x < 106):
        plt.axhline(50, color = '#CBE90C')
        plt.text(end_time, 50, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 106) and (x < 180):
        plt.axhline(106, color = '#F6EB14')
        plt.text(end_time, 106, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 180) and (x < 300):
        plt.axhline(180, color = '#FFC800')
        plt.text(end_time, 180, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 300) and (x < 495):
        plt.axhline(300, color = '#FF9600')
        plt.text(end_time, 300, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 495) and (x < 750):
        plt.axhline(495, color = '#FF0000')
        plt.text(end_time, 495, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 750) and (x < 10000):
        plt.axhline(750, color = '#C80000')
        plt.text(end_time, 750, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/dombas_deltaH_realtime_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/dombas_deltaH_realtime_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/dombas_deltaH_realtime.png')



#H COMPONENT NY-ÅLESUND REALTIME
dfNal = pd.read_csv('../Combined_data/data/magnetometer_nal.csv', sep = " ")
dfNal = dfNal.drop_duplicates(subset=['timestamp'])

dfNal['timestamp'] = pd.to_datetime(dfNal['timestamp'])
dfNal.set_index('timestamp', inplace=True)

dfNal['year'] = dfNal.index.year
dfNal['month'] = dfNal.index.month
dfNal['day'] = dfNal.index.day
dfNal['hour'] = dfNal.index.hour
dfNal['minute'] = dfNal.index.minute
dfNal['diff_hour'] = dfNal['hour'].diff()
dfNal['diff_day'] = dfNal['day'].diff()
dfNal['diff_hour'].fillna(0, inplace = True)
dfNal['diff_day'].fillna(0, inplace = True)

length = len(dfNal.index)-1
for i in range(length):
    if (dfNal.index[i+1]-dfNal.index[i]).seconds >= 300:
        dfNal.loc[dfNal.index[i]+dtm.timedelta(minutes=5)] = float("nan")
dfNal.sort_index(inplace=True)

realtime = (dfNal.index >= start_time) & (dfNal.index <= time)
df_real = dfNal.loc[realtime]


#Dombås H component current plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_real.index, df_real.Horiz_nal)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time, right=end_time)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Ny-Ålesund magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/nyalesund_Hcom_realtime_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/nyalesund_Hcom_realtime_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/nyalesund_Hcom_realtime.png')


#ACTIVITY INDEX NY-ÅLESUND REALTIME
new_df = pd.read_csv('../Combined_data/data/aiNal.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiNal']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

realtime = (new_df.index >= start_time) & (new_df.index <= time)
df_real = new_df.loc[realtime]

#nY-Ålesund Activity Index current plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_real.index, df_real.aiNal.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time, right= end_time)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Ny-Ålesund hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_real['aiNal'].to_list()

for x in max_ai:
    if (x >= 100) and (x < 281):
        plt.axhline(100, color = '#CBE90C')
        plt.text(end_time, 100, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 281) and (x < 481):
        plt.axhline(281, color = '#F6EB14')
        plt.text(end_time, 281, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 481) and (x < 801):
        plt.axhline(481, color = '#FFC800')
        plt.text(end_time, 481, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 801) and (x < 1321):
        plt.axhline(801, color = '#FF9600')
        plt.text(end_time, 801, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1321) and (x < 2001):
        plt.axhline(1321, color = '#FF0000')
        plt.text(end_time, 1321, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2001) and (x < 10000):
        plt.axhline(2001, color = '#C80000')
        plt.text(end_time, 2001, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/nyalesund_deltaH_realtime_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/nyalesund_deltaH_realtime_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/nyalesund_deltaH_realtime.png')






#H COMPONENT TROMSØ 24H
past_24 = (dfTro.index >= start_time_24) & (dfTro.index <= time)
df_24 = dfTro.loc[past_24]
#df_24 = df.iloc[-1600:]

#Tromsø H component 24h plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_24.index, df_24.Horiz_tro)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time_24, right=end_time_24)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Tromsø magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/tromso_Hcom_24h_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/tromso_Hcom_24h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/tromso_Hcom_24h.png')


#ACTIVITY INDEX TROMSØ 24H
new_df = pd.read_csv('../Combined_data/data/aiTro.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiTro']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

past_24 = (new_df.index >= start_time_24) & (new_df.index <= time)
df_24 = new_df.loc[past_24]

#Tromsø Activity Index 24h plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_24.index, df_24.aiTro.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time_24, right= end_time_24)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Tromsø hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_24['aiTro'].to_list()

for x in max_ai:
    if (x >= 100) and (x < 281):
        plt.axhline(100, color = '#CBE90C')
        plt.text(end_time_24, 100, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 281) and (x < 481):
        plt.axhline(281, color = '#F6EB14')
        plt.text(end_time_24, 281, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 481) and (x < 801):
        plt.axhline(481, color = '#FFC800')
        plt.text(end_time_24, 481, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 801) and (x < 1321):
        plt.axhline(801, color = '#FF9600')
        plt.text(end_time_24, 801, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1321) and (x < 2001):
        plt.axhline(1321, color = '#FF0000')
        plt.text(end_time_24, 1321, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2001) and (x < 10000):
        plt.axhline(2001, color = '#C80000')
        plt.text(end_time_24, 2001, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/tromso_deltaH_24h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/tromso_deltaH_24h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/tromso_deltaH_24h.png')




#H COMPONENT DOMBÅS 24H
past_24 = (dfDob.index >= start_time_24) & (dfDob.index <= time)
df_24 = dfDob.loc[past_24]

#Dombås H component 24h plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_24.index, df_24.Horiz_dob)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time_24, right=end_time_24)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Dombås magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/dombas_Hcom_24h_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/dombas_Hcom_24h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/dombas_Hcom_24h.png')


#ACTIVITY INDEX DOMBÅS 24H
new_df = pd.read_csv('../Combined_data/data/aiDob.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiDob']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

past_24 = (new_df.index >= start_time_24) & (new_df.index <= time)
df_24 = new_df.loc[past_24]

#Dombås Activity Index 24h plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_24.index, df_24.aiDob.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time_24, right= end_time_24)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Dombås hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_24['aiDob'].to_list()

for x in max_ai:
    if (x >= 50) and (x < 106):
        plt.axhline(50, color = '#CBE90C')
        plt.text(end_time_24, 50, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 106) and (x < 180):
        plt.axhline(106, color = '#F6EB14')
        plt.text(end_time_24, 106, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 180) and (x < 300):
        plt.axhline(180, color = '#FFC800')
        plt.text(end_time_24, 180, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 300) and (x < 495):
        plt.axhline(300, color = '#FF9600')
        plt.text(end_time_24, 300, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 495) and (x < 750):
        plt.axhline(495, color = '#FF0000')
        plt.text(end_time_24, 495, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 750) and (x < 10000):
        plt.axhline(750, color = '#C80000')
        plt.text(end_time_24, 750, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/dombas_deltaH_24h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/dombas_deltaH_24h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/dombas_deltaH_24h.png')




#H COMPONENT NY-ÅLESUND 24H
past_24 = (dfNal.index >= start_time_24) & (dfNal.index <= time)
df_24 = dfNal.loc[past_24]

#Ny-Ålesund H component 24h plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_24.index, df_24.Horiz_nal)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time_24, right=end_time_24)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Ny-Ålesund magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/nyalesund_Hcom_24h_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/nyalesund_Hcom_24h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/nyalesund_Hcom_24h.png')


#ACTIVITY INDEX NY-ÅLESUND 24H
new_df = pd.read_csv('../Combined_data/data/aiNal.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiNal']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

past_24 = (new_df.index >= start_time_24) & (new_df.index <= time)
df_24 = new_df.loc[past_24]

#Ny-Ålesund Activity Index 24h plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_24.index, df_24.aiNal.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time_24, right= end_time_24)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Ny-Ålesund hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_24['aiNal'].to_list()

for x in max_ai:
    if (x >= 100) and (x < 281):
        plt.axhline(100, color = '#CBE90C')
        plt.text(end_time_24, 100, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 281) and (x < 481):
        plt.axhline(281, color = '#F6EB14')
        plt.text(end_time_24, 281, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 481) and (x < 801):
        plt.axhline(481, color = '#FFC800')
        plt.text(end_time_24, 481, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 801) and (x < 1321):
        plt.axhline(801, color = '#FF9600')
        plt.text(end_time_24, 801, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1321) and (x < 2001):
        plt.axhline(1321, color = '#FF0000')
        plt.text(end_time_24, 1321, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2001) and (x < 10000):
        plt.axhline(2001, color = '#C80000')
        plt.text(end_time_24, 2001, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/nyalesund_deltaH_24h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/nyalesund_deltaH_24h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/nyalesund_deltaH_24h.png')




#H COMPONENT TROMSØ 48H
past_48 = (dfTro.index >= start_time_48) & (dfTro.index <= time)
df_48 = dfTro.loc[past_48]
#df_48 = df.iloc[-3200:]

#Tromsø H component 48h plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_48.index, df_48.Horiz_tro)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time_48, right=end_time_48)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Tromsø magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/tromso_Hcom_48h_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/tromso_Hcom_48h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/tromso_Hcom_48h.png')


#ACTIVITY INDEX TROMSØ 48H
new_df = pd.read_csv('../Combined_data/data/aiTro.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiTro']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

past_48 = (new_df.index >= start_time_48) & (new_df.index <= time)
df_48 = new_df.loc[past_48]

#Tromsø Activity Index 48h plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_48.index, df_48.aiTro.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time_48, right= end_time_48)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Tromsø hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_48['aiTro'].to_list()

for x in max_ai:
    if (x >= 100) and (x < 281):
        plt.axhline(100, color = '#CBE90C')
        plt.text(end_time_48, 100, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 281) and (x < 481):
        plt.axhline(281, color = '#F6EB14')
        plt.text(end_time_48, 281, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 481) and (x < 801):
        plt.axhline(481, color = '#FFC800')
        plt.text(end_time_48, 481, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 801) and (x < 1321):
        plt.axhline(801, color = '#FF9600')
        plt.text(end_time_48, 801, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1321) and (x < 2001):
        plt.axhline(1321, color = '#FF0000')
        plt.text(end_time_48, 1321, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2001) and (x < 10000):
        plt.axhline(2001, color = '#C80000')
        plt.text(end_time_48, 2001, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/tromso_deltaH_48h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/tromso_deltaH_48h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/tromso_deltaH_48h.png')




#H COMPONENT DOMBÅS 48H
past_48 = (dfDob.index >= start_time_48) & (dfDob.index <= time)
df_48 = dfDob.loc[past_48]
#df_48 = df.iloc[-3200:]

#Dombås H component 48h plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_48.index, df_48.Horiz_dob)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time_48, right=end_time_48)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Dombås magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/dombas_Hcom_48h_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/dombas_Hcom_48h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/dombas_Hcom_48h.png')


#ACTIVITY INDEX DOMBÅS 48H
new_df = pd.read_csv('../Combined_data/data/aiDob.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiDob']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

past_48 = (new_df.index >= start_time_48) & (new_df.index <= time)
df_48 = new_df.loc[past_48]

#Dombås Activity Index 48h plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_48.index, df_48.aiDob.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time_48, right= end_time_48)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Dombås hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_48['aiDob'].to_list()

for x in max_ai:
    if (x >= 50) and (x < 106):
        plt.axhline(50, color = '#CBE90C')
        plt.text(end_time_48, 50, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 106) and (x < 180):
        plt.axhline(106, color = '#F6EB14')
        plt.text(end_time_48, 106, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 180) and (x < 300):
        plt.axhline(180, color = '#FFC800')
        plt.text(end_time_48, 180, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 300) and (x < 495):
        plt.axhline(300, color = '#FF9600')
        plt.text(end_time_48, 300, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 495) and (x < 750):
        plt.axhline(495, color = '#FF0000')
        plt.text(end_time_48, 495, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 750) and (x < 10000):
        plt.axhline(750, color = '#C80000')
        plt.text(end_time_48, 750, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/dombas_deltaH_48h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/dombas_deltaH_48h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/dombas_deltaH_48h.png')




#H COMPONENT NY-ÅLESUND 48H
past_48 = (dfNal.index >= start_time_48) & (dfNal.index <= time)
df_48 = dfNal.loc[past_48]
#df_48 = df.iloc[-3200:]

#Ny-Ålesund H component 48h plot
fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_48.index, df_48.Horiz_nal)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlim(left=start_time_48, right=end_time_48)
ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Magnetic field intensity [nT]', fontsize=14)
ax.set_title('Ny-Ålesund magnetometer H-component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Hcomponent/nyalesund_Hcom_48h_old.png', dpi=300)
plt.cla()
plt.close('all') 

im = Image.open('../New_AI/plots/Hcomponent/nyalesund_Hcom_48h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Hcomponent/nyalesund_Hcom_48h.png')


#ACTIVITY INDEX Ny-Ålesund 48H
new_df = pd.read_csv('../Combined_data/data/aiNal.csv', sep = " ")
new_df.drop(['max', 'min'], axis=1, inplace=True)
new_df.columns = ['timestamp', 'aiNal']
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'])
new_df.set_index('timestamp', inplace=True)

past_48 = (new_df.index >= start_time_48) & (new_df.index <= time)
df_48 = new_df.loc[past_48]

#Ny-Ålesund Activity Index 48h plot
fig, ax = plt.subplots(figsize = (15, 7))
ax.bar(df_48.index, df_48.aiNal.values, width = 0.02, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:00"))

ax.set_xlim(left=start_time_48, right= end_time_48)

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('ΔH [nT]', fontsize=14)
ax.set_title('Ny-Ålesund hourly geomagnetic activity index', fontsize=16)
plt.xticks(rotation = 0)

max_ai = df_48['aiNal'].to_list()

for x in max_ai:
    if (x >= 100) and (x < 281):
        plt.axhline(100, color = '#CBE90C')
        plt.text(end_time_48, 100, s = 'Disturbed', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 281) and (x < 481):
        plt.axhline(281, color = '#F6EB14')
        plt.text(end_time_48, 281, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 481) and (x < 801):
        plt.axhline(481, color = '#FFC800')
        plt.text(end_time_48, 481, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 801) and (x < 1321):
        plt.axhline(801, color = '#FF9600')
        plt.text(end_time_48, 801, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1321) and (x < 2001):
        plt.axhline(1321, color = '#FF0000')
        plt.text(end_time_48, 1321, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2001) and (x < 10000):
        plt.axhline(2001, color = '#C80000')
        plt.text(end_time_48, 2001, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)


fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Activity_index/nyalesund_deltaH_48h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Activity_index/nyalesund_deltaH_48h_old.png')
width, height = im.size

left = 250
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Activity_index/nyalesund_deltaH_48h.png')