import pandas as pd
import datetime as dt
import requests
import json
import plotly.express as px
import os
from django.conf import settings
import plotly.offline as py


def get_df():
    csv_path = os.path.join(settings.BASE_DIR, 'energy_data/utils/solar_electric_data.csv')
    df=pd.read_csv(csv_path,skiprows=13,header=0,sep=',', parse_dates=['Date'])
    df['DateTime']=pd.to_datetime(df['Date'].astype(str) +' ' + df['Start Time'].astype(str), format="mixed", errors='ignore')
    df.set_index('DateTime',inplace=True)
    return df


def getClimateData(stn_id, start=None, end=None):
    url='https://data.rcc-acis.org/StnData/'
    now=dt.datetime.now()
    if start or end:
        sd=start.strftime('%Y-%m-%d')
        ed=end.strftime('%Y-%m-%d')
    else:
        sd="{}-01-01".format(now.year)
        ed="{}".format(now.strftime("%Y-%m-%d"))
    params={"sid":"{}".format(stn_id),"sdate":sd,"edate":ed,"elems":
            [{"name":"maxt"},
             {"name":"maxt","normal":"1"},
             {"name":"mint"},
             {"name":"mint","normal":"1"},
             {"name":"pcpn"},
             {"name":"pcpn","normal":"1"},
             {"name":"avgt"},
             {"name":"avgt","normal":"1"}]
             }
    r=requests.post(url,data=json.dumps(params),headers={'content-type': 'application/json'}, timeout=60)
    if r.status_code==200:
        return r.json()
    else:
        return []
    
# sample the data daily
def get_daily_df():
    df = get_df()
    dly_df=df[['Consumption','Generation']].resample('D').mean()
    clim_data=getClimateData('KMYF',start=dly_df.index[0], end=dly_df.index[-1])
    #print(clim_data)
    max_temp_data=[i[1] for i in clim_data['data']]
    min_temp_data = [i[3] for i in clim_data['data']]
    avg_temp_data=[i[7] for i in clim_data['data']]
    avgt = pd.to_numeric(pd.Series(avg_temp_data),errors='ignore')
    avgt.index = dly_df.index

    maxt=pd.to_numeric(pd.Series(max_temp_data),errors='ignore')
    maxt.index=dly_df.index

    mint = pd.to_numeric(pd.Series(min_temp_data),errors='ignore')
    mint.index = dly_df.index

    dly_df['maxt']=maxt
    dly_df['avgt']=avgt
    dly_df['mint']=mint

    return dly_df

def getCorr(var1, var2):
    return var1.corr(var2, method='kendall'), var1.corr(var2, method='pearson'), var1.corr(var2, method='spearman')

def number_one():
    dly_df = get_daily_df()
    winter_df = dly_df[(dly_df.index>='2022-12-01') & (dly_df.index<'2023-03-01')]
    winter_corr = getCorr(winter_df['Generation'], winter_df['avgt'])
    return winter_corr

def number_two():
    dly_df = get_daily_df()
    fa_win_spr_df = dly_df[(dly_df.index>='2022-09-01') & (dly_df.index<='2023-05-31')]
    fa_win_spr_corr = getCorr(fa_win_spr_df['Generation'], fa_win_spr_df['avgt'])
    return fa_win_spr_corr

def get_hly_df():
    df = get_df()
    hly_df=df[['Consumption','Generation']].resample('H').mean()
    hly_df['Date'] = hly_df.index.date
    hly_df['Time'] = hly_df.index.time
    return hly_df

def number_three():
    hly_df = get_hly_df()
    aug_hly_df = hly_df[(hly_df.index>='2023-08-01') & (hly_df.index<='2023-08-31')]
    heatmap_data = aug_hly_df.pivot_table(index='Time', columns='Date', values='Consumption')
    fig = px.imshow(heatmap_data, labels=dict(x="Date", y="Time", color="Consumption"),
                x=heatmap_data.columns,
                y=heatmap_data.index,
                aspect="auto")
    fig.update_layout(
        title="Heatmap of Consumption by Day and Hour",
        xaxis_nticks=36
    )
    div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return div

def number_four():
    hly_df = get_hly_df()
    fa_wi_sp_hly_df = hly_df[(hly_df.index >= '2022-09-01') & (hly_df.index <= '2023-05-31')]
    new_df = fa_wi_sp_hly_df.groupby(["Time"])['Consumption'].mean()
    fig = px.box(new_df, y="Consumption")
    div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return div

def get_weekly_df():
    df = get_df()
    weekly_df=df[['Consumption','Generation']].resample('W').mean()
    return weekly_df

def number_five():
    weekly_df = get_weekly_df()
    fa_wi_sp_weekly_df = weekly_df[(weekly_df.index >= '2022-09-01') & (weekly_df.index <= '2023-05-31')]
    fig = px.box(fa_wi_sp_weekly_df, y="Consumption")
    div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return div


def get_monthly_df():
    df = get_df()
    monthly_df = df[['Consumption', 'Generation']].resample('M').mean()
    return monthly_df

def number_six():
    monthly_df = get_monthly_df()
    mthly_rnge_df = monthly_df[(monthly_df.index >= '2022-09-01') & (monthly_df.index <= '2023-08-31')]
    fig = px.box(mthly_rnge_df, y='Consumption')
    div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return div

def number_seven():
    monthly_df = get_monthly_df()
    mthly_rnge_df = monthly_df[(monthly_df.index >= '2022-09-01') & (monthly_df.index <= '2023-08-31')]
    fig = px.box(mthly_rnge_df, y='Generation')
    div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return div


