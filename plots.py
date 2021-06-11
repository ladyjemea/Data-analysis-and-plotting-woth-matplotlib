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




'''X-ray data'''

dfX = pd.read_csv('../Combined_data/data/xrays.csv', sep = " ")

dfX['timestamp'] = pd.to_datetime(dfX['timestamp'])
dfX.set_index('timestamp', inplace=True)

dfX['year'] = dfX.index.year
dfX['month'] = dfX.index.month
dfX['day'] = dfX.index.day
dfX['hour'] = dfX.index.hour
dfX['minute'] = dfX.index.minute
dfX['diff_hour'] = dfX['hour'].diff()
dfX['diff_day'] = dfX['day'].diff()
dfX['diff_hour'].fillna(0, inplace = True)
dfX['diff_day'].fillna(0, inplace = True)
dfX['diff_minute'] = dfX['minute'].diff()
dfX['diff_minute'].fillna(0, inplace = True)

#dfmax = dfX[dfX.diff_minute > 5]

length = len(dfX.index)-1
for i in range(length):
    if (dfX.index[i+1]-dfX.index[i]).seconds >= 300:
        dfX.loc[dfX.index[i]+dtm.timedelta(minutes=5)] = float("nan")
dfX.sort_index(inplace=True)


#Xray plots
dfX['Xrays'].replace(to_replace= 0, value = np.nan, inplace = True)

#realtime
realtime = (dfX.index >= start_time) & (dfX.index <= time)
df_real = dfX.loc[realtime]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_real.index, df_real.Xrays.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time, right=end_time)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Flux [Wm^-2]', fontsize=14)
ax.set_title('GOES X-ray flux (0.1-0.8 nm)', fontsize=16)

flux_col = df_real['Xrays'].to_list()

for x in flux_col:
    if (x >= 1e-5) and (x < 5e-5):
        plt.axhline(1e-5, color = '#F6EB14')
        plt.text(end_time, 1e-5, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 5e-5) and (x < 1e-4):
        plt.axhline(5e-5, color = '#FFC800')
        plt.text(end_time, 5e-5, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e-4) and (x < 1e-3):
        plt.axhline(1e-4, color = '#FF9600')
        plt.text(end_time, 1e-4, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e-3) and (x < 2e-3):
        plt.axhline(1e-3, color = '#FF0000')
        plt.text(end_time, 1e-3, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2e-3):
        plt.axhline(2e-3, color = '#C80000')
        plt.text(end_time, 2e-3, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Xray_Protons/xrays_realtime_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Xray_Protons/xrays_realtime_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Xray_Protons/xrays_realtime.png')



#24h
past_24 = (dfX.index >= start_time_24) & (dfX.index <= time)
df_24 = dfX.loc[past_24]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_24.index, df_24.Xrays.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time_24, right=end_time_24)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Flux [Wm^-2]', fontsize=14)
ax.set_title('GOES X-ray flux (0.1-0.8 nm)', fontsize=16)

flux_col = df_24['Xrays'].to_list()

for x in flux_col:
    if (x >= 1e-5) and (x < 5e-5):
        plt.axhline(1e-5, color = '#F6EB14')
        plt.text(end_time_24, 1e-5, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 5e-5) and (x < 1e-4):
        plt.axhline(5e-5, color = '#FFC800')
        plt.text(end_time_24, 5e-5, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e-4) and (x < 1e-3):
        plt.axhline(1e-4, color = '#FF9600')
        plt.text(end_time_24, 1e-4, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e-3) and (x < 2e-3):
        plt.axhline(1e-3, color = '#FF0000')
        plt.text(end_time_24, 1e-3, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2e-3):
        plt.axhline(2e-3, color = '#C80000')
        plt.text(end_time_24, 2e-3, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Xray_Protons/xrays_24h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Xray_Protons/xrays_24h_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Xray_Protons/xrays_24h.png')



#48h
past_48 = (dfX.index >= start_time_48) & (dfX.index <= time)
df_48 = dfX.loc[past_48]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_48.index, df_48.Xrays.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time_48, right=end_time_48)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Flux [Wm^-2]', fontsize=14)
ax.set_title('GOES X-ray flux (0.1-0.8 nm)', fontsize=16)

flux_col = df_48['Xrays'].to_list()

for x in flux_col:
    if (x >= 1e-5) and (x < 5e-5):
        plt.axhline(1e-5, color = '#F6EB14')
        plt.text(end_time_48, 1e-5, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 5e-5) and (x < 1e-4):
        plt.axhline(5e-5, color = '#FFC800')
        plt.text(end_time_48, 5e-5, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e-4) and (x < 1e-3):
        plt.axhline(1e-4, color = '#FF9600')
        plt.text(end_time_48, 1e-4, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e-3) and (x < 2e-3):
        plt.axhline(1e-3, color = '#FF0000')
        plt.text(end_time_48, 1e-3, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 2e-3):
        plt.axhline(2e-3, color = '#C80000')
        plt.text(end_time_48, 2e-3, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Xray_Protons/xrays_48h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Xray_Protons/xrays_48h_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Xray_Protons/xrays_48h.png')




'''Proton data'''

dfP = pd.read_csv('../Combined_data/data/protons.csv',sep= " ")

dfP['timestamp'] = pd.to_datetime(dfP['timestamp'])
dfP.set_index('timestamp', inplace=True)

dfP['year'] = dfP.index.year
dfP['month'] = dfP.index.month
dfP['day'] = dfP.index.day
dfP['hour'] = dfP.index.hour
dfP['minute'] = dfP.index.minute
dfP['diff_hour'] = dfP['hour'].diff()
dfP['diff_day'] = dfP['day'].diff()
dfP['diff_hour'].fillna(0, inplace = True)
dfP['diff_day'].fillna(0, inplace = True)

length = len(dfP.index)-1
for i in range(length):
    if (dfP.index[i+1]-dfP.index[i]).seconds >= 600:
        dfP.loc[dfP.index[i]+dtm.timedelta(minutes=10)] = float("nan")
dfP.sort_index(inplace=True)



#Proton plots
#realtime
realtime = (dfP.index >= start_time) & (dfP.index <= time)
df_real = dfP.loc[realtime]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_real.index, df_real.Protons.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time, right=end_time)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Flux [pfu]', fontsize=14)
ax.set_title('GOES Proton flux (≥10 MeV)', fontsize=16)

flux_col = df_real['Protons'].to_list()

for x in flux_col:
    if (x >= 10) and (x < 1e2):
        plt.axhline(10, color = '#F6EB14')
        plt.text(end_time, 10, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e2) and (x < 1e3):
        plt.axhline(1e2, color = '#FFC800')
        plt.text(end_time, 1e2, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e3) and (x < 1e4):
        plt.axhline(1e3, color = '#FF9600')
        plt.text(end_time, 1e3, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e4) and (x < 1e5):
        plt.axhline(1e4, color = '#FF0000')
        plt.text(end_time, 1e4, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e5):
        plt.axhline(1e5, color = '#C80000')
        plt.text(end_time, 1e5, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Xray_Protons/protons_realtime_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open("../New_AI/plots/Xray_Protons/protons_realtime_old.png")
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save("../New_AI/plots/Xray_Protons/protons_realtime.png")



#24h
past_24 = (dfP.index >= start_time_24) & (dfP.index <= time)
df_24 = dfP.loc[past_24]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_24.index, df_24.Protons.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time_24, right=end_time_24)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Flux [pfu]', fontsize=14)
ax.set_title('GOES Proton flux (≥10 MeV)', fontsize=16)

flux_col = df_24['Protons'].to_list()

for x in flux_col:
    if (x >= 10) and (x < 1e2):
        plt.axhline(10, color = '#F6EB14')
        plt.text(end_time_24, 10, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e2) and (x < 1e3):
        plt.axhline(1e2, color = '#FFC800')
        plt.text(end_time_24, 1e2, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e3) and (x < 1e4):
        plt.axhline(1e3, color = '#FF9600')
        plt.text(end_time_24, 1e3, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e4) and (x < 1e5):
        plt.axhline(1e4, color = '#FF0000')
        plt.text(end_time_24, 1e4, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e5):
        plt.axhline(1e5, color = '#C80000')
        plt.text(end_time_24, 1e5, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Xray_Protons/protons_24h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Xray_Protons/protons_24h_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Xray_Protons/protons_24h.png')




#48h
past_48 = (dfP.index >= start_time_48) & (dfP.index <= time)
df_48 = dfP.loc[past_48]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_48.index, df_48.Protons.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time_48, right=end_time_48)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Flux [pfu]', fontsize=14)
ax.set_title('GOES Proton flux (≥10 MeV)', fontsize=16)

flux_col = df_48['Protons'].to_list()

for x in flux_col:
    if (x >= 10) and (x < 1e2):
        plt.axhline(10, color = '#F6EB14')
        plt.text(end_time_48, 10, s = 'Minor', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e2) and (x < 1e3):
        plt.axhline(1e2, color = '#FFC800')
        plt.text(end_time_48, 1e2, s = 'Moderate', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e3) and (x < 1e4):
        plt.axhline(1e3, color = '#FF9600')
        plt.text(end_time_48, 1e3, s = 'Strong', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e4) and (x < 1e5):
        plt.axhline(1e4, color = '#FF0000')
        plt.text(end_time_48, 1e4, s = 'Severe', fontsize = 12, alpha=0.7, color='#000000', zorder=10)
    if (x >= 1e5):
        plt.axhline(1e5, color = '#C80000')
        plt.text(end_time_48, 1e5, s = 'Extreme', fontsize = 12, alpha=0.7, color='#000000', zorder=10)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Xray_Protons/protons_48h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Xray_Protons/protons_48h_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Xray_Protons/protons_48h.png')





'''Solar Wind Speed'''

dfS = pd.read_csv('../Combined_data/data/solar_wind_speed.csv', sep = " ")

dfS['timestamp'] = pd.to_datetime(dfS['timestamp'])
dfS.set_index('timestamp', inplace=True)

dfS['year'] = dfS.index.year
dfS['month'] = dfS.index.month
dfS['day'] = dfS.index.day
dfS['hour'] = dfS.index.hour
dfS['minute'] = dfS.index.minute
dfS['diff_hour'] = dfS['hour'].diff()
dfS['diff_day'] = dfS['day'].diff()
dfS['diff_hour'].fillna(0, inplace = True)
dfS['diff_day'].fillna(0, inplace = True)

length = len(dfS.index)-1
for i in range(length):
    if (dfS.index[i+1]-dfS.index[i]).seconds >= 600:
        dfS.loc[dfS.index[i]+dtm.timedelta(minutes=10)] = float("nan")
dfS.sort_index(inplace=True)



#Solar Wind Speed
#realtime
realtime = (dfS.index >= start_time) & (dfS.index <= time)
df_real = dfS.loc[realtime]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_real.index, df_real.Speed.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time, right=end_time)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Speed [km/s]', fontsize=14)
ax.set_title('DSCOVR (ACE where missing) Solar wind speed', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Solar_Wind/speed_realtime_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open("../New_AI/plots/Solar_Wind/speed_realtime_old.png")
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save("../New_AI/plots/Solar_Wind/speed_realtime.png")



#24h
past_24 = (dfS.index >= start_time_24) & (dfS.index <= time)
df_24 = dfS.loc[past_24]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_24.index, df_24.Speed.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time_24, right=end_time_24)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Speed [km/s]', fontsize=14)
ax.set_title('DSCOVR (ACE where missing) Solar wind speed', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Solar_Wind/speed_24h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Solar_Wind/speed_24h_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Solar_Wind/speed_24h.png')



#48h
past_48 = (dfS.index >= start_time_48) & (dfS.index <= time)
df_48 = dfS.loc[past_48]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_48.index, df_48.Speed.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time_48, right=end_time_48)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('Speed [km/s]', fontsize=14)
ax.set_title('DSCOVR (ACE where missing) Solar wind speed', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Solar_Wind/speed_48h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Solar_Wind/speed_48h_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Solar_Wind/speed_48h.png')




'''Solar Wind Bz_gsm'''

dfB = pd.read_csv('../Combined_data/data/solar_wind_bz.csv', sep = " ")

dfB['timestamp'] = pd.to_datetime(dfB['timestamp'])
dfB.set_index('timestamp', inplace=True)

dfB['year'] = dfB.index.year
dfB['month'] = dfB.index.month
dfB['day'] = dfB.index.day
dfB['hour'] = dfB.index.hour
dfB['minute'] = dfB.index.minute
dfB['diff_hour'] = dfB['hour'].diff()
dfB['diff_day'] = dfB['day'].diff()
dfB['diff_hour'].fillna(0, inplace = True)
dfB['diff_day'].fillna(0, inplace = True)

length = len(dfB.index)-1
for i in range(length):
    if (dfB.index[i+1]-dfB.index[i]).seconds >= 600:
        dfB.loc[dfB.index[i]+dtm.timedelta(minutes=10)] = float("nan")
dfB.sort_index(inplace=True)



#Solar Wind Bz
#realtime
realtime = (dfB.index >= start_time) & (dfB.index <= time)
df_real = dfB.loc[realtime]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_real.index, df_real.Bz_gsm.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time, right=end_time)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('IMF Bz [nT]', fontsize=14)
ax.set_title('DSCOVR (ACE where missing) IMF Bz component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Solar_Wind/bz_realtime_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open("../New_AI/plots/Solar_Wind/bz_realtime_old.png")
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save("../New_AI/plots/Solar_Wind/bz_realtime.png")



#24h
past_24 = (dfB.index >= start_time_24) & (dfB.index <= time)
df_24 = dfB.loc[past_24]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_24.index, df_24.Bz_gsm.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time_24, right=end_time_24)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('IMF Bz [nT]', fontsize=14)
ax.set_title('DSCOVR (ACE where missing) IMF Bz component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Solar_Wind/bz_24h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Solar_Wind/bz_24h_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Solar_Wind/bz_24h.png')



#48h
past_48 = (dfB.index >= start_time_48) & (dfB.index <= time)
df_48 = dfB.loc[past_48]

fig, ax = plt.subplots(figsize=(15,7))
ax.plot(df_48.index, df_48.Bz_gsm.values, zorder=20)

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
locs, labels = plt.xticks(rotation = 0)
ax.set_xlim(left=start_time_48, right=end_time_48)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax.set_xlabel('UTC', fontsize=14)
ax.set_ylabel('IMF Bz [nT]', fontsize=14)
ax.set_title('DSCOVR (ACE where missing) IMF Bz component', fontsize=16)

fig.text(0.95, 0.03, u"\u00a9" ' 2020 Norwegian Center for Space Weather',
         fontsize=14, color='gray',
         ha='right', va='bottom', alpha=0.5)

plt.savefig('../New_AI/plots/Solar_Wind/bz_48h_old.png', dpi=300)
plt.cla()
plt.close('all')

im = Image.open('../New_AI/plots/Solar_Wind/bz_48h_old.png')
width, height = im.size

left = 270
top = 100
right = 4300
bottom = 2050

imc = im.crop((left, top, right, bottom))
imc.save('../New_AI/plots/Solar_Wind/bz_48h.png')