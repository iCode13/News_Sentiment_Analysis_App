# Setup dependencies
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import json
import copy

path = "static/data/choropleth_locations3_all_sentiment.csv"
df = pd.read_csv(path)
df = df.rename(columns = {'article_score':'article_sentiment'})


def choropleth_global_overtime():
    
    # Extract year-month from date to groupby over time
    df_country_time = df[['country', 'country_ISO_code', 'article_sentiment', 'pub_date']].copy()
    df_country_time['year_month'] = " "    # Extract only month and year from date
    df_country_time = df_country_time[['country', 'country_ISO_code', 'article_sentiment', 'pub_date', 'year_month']]

    for i in range(len(df_country_time)):
        pub_date = df_country_time.iloc[i,3]
        df_country_time.iloc[i,4] = pub_date[:7]
        
    # Get mean sentiment scores for each country by year-month
    group_by_time = df_country_time.groupby(['year_month', 'country', 'country_ISO_code'], as_index=False)['article_sentiment'].mean()
    df_country_time = pd.DataFrame({
        'country':group_by_time.country, 
        'country_ISO_code':group_by_time.country_ISO_code, 
        'article_sentiment':group_by_time.article_sentiment, 
        'year_month':group_by_time.year_month
    })

    for i in range(len(df_country_time)):
        df_country_time['article_sentiment'][i] = "{:.4f}".format(df_country_time['article_sentiment'][i])

    # Create animation
    fig1_time = px.choropleth(df_country_time,               
        locations = "country_ISO_code",               
        color = "article_sentiment",
        animation_frame = "year_month",
        hover_name = "country",
        hover_data={
            "article_sentiment": True,
            "year_month": True,                  
            "country_ISO_code": False,
        },
        color_continuous_scale = 'RdBu',
        range_color=(-0.8,0.8),
        color_continuous_midpoint=0,
        title = 'Global News Sentiment Over Time (2015-2017)',
        height = 800             
    )
    fig1_time_json = json.dumps(fig1_time, cls=plotly.utils.PlotlyJSONEncoder)
    return fig1_time_json
    

def choropleth_global_bymonth():
    
    # Get mean sentiment scores by month
    df_country_month = df[['country', 'country_ISO_code', 'article_sentiment', 'month']].copy()
    group_by_month = df_country_month.groupby(['month', 'country', 'country_ISO_code'], as_index=False)['article_sentiment'].mean()
    df_country_month = pd.DataFrame({
        'country':group_by_month.country, 
        'country_ISO_code':group_by_month.country_ISO_code, 
        'article_sentiment':group_by_month.article_sentiment, 
        'month':group_by_month.month
    })

    for i in range(len(df_country_month)):
        df_country_month['article_sentiment'][i] = "{:.4f}".format(df_country_month['article_sentiment'][i])
        
    # Sort data by correct order of months
    df_country_month['month_code'] = " "
    df_country_month = df_country_month[['country', 'country_ISO_code', 'article_sentiment', 'month', 'month_code']]

    months_dict = {
        'month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'month_code': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        }
    df_months = pd.DataFrame(months_dict, columns = ['month', 'month_code'])

    for i in range(len(df_country_month)):
        for j in range(len(df_months)):
            if df_country_month.iloc[i,3] == df_months.iloc[j,0]:
                df_country_month.iloc[i,4] = df_months.iloc[j,1]

    df_country_month = df_country_month.sort_values('month_code', inplace=False)
    df_country_month = df_country_month.reset_index()

    # Create animation
    fig2_month = px.choropleth(df_country_month,               
        locations = "country_ISO_code",               
        color = "article_sentiment",
        hover_name = "country",  
        animation_frame = "month",
        hover_data={
        "article_sentiment": True,
        "month": True,                  
        "country_ISO_code": False,
        },
              color_continuous_scale = 'BrBg', 
              range_color=(-0.8,0.8),
              title = 'Global News Sentiment by Month (2015-2017)',
              height = 800             
    )
    fig2_month_json = json.dumps(fig2_month, cls=plotly.utils.PlotlyJSONEncoder)
    return fig2_month_json


def choropleth_global_byweekday():
    
    # Get mean sentiment scores by day of the week
    df_country_weekday = df[['country', 'country_ISO_code', 'article_sentiment', 'weekday']].copy()
    group_by_weekday = df_country_weekday.groupby(['weekday', 'country', 'country_ISO_code'], as_index=False)['article_sentiment'].mean()
    df_country_weekday = pd.DataFrame({
        'country':group_by_weekday.country, 
        'country_ISO_code':group_by_weekday.country_ISO_code, 
        'article_sentiment':group_by_weekday.article_sentiment, 
        'weekday':group_by_weekday.weekday
    })

    for i in range(len(df_country_weekday)):
        df_country_weekday['article_sentiment'][i] = "{:.4f}".format(df_country_weekday['article_sentiment'][i])
    
    # Sort data by correct order of weekdays
    df_country_weekday['weekday_code'] = " "
    df_country_weekday = df_country_weekday[['country', 'country_ISO_code', 'article_sentiment', 'weekday', 'weekday_code']]

    weekdays_dict = {
        'weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'weekday_code': [1, 2, 3, 4, 5, 6, 7]
        }
    df_weekdays = pd.DataFrame(weekdays_dict, columns = ['weekday', 'weekday_code'])

    for i in range(len(df_country_weekday)):
        for j in range(len(df_weekdays)):
            if df_country_weekday.iloc[i,3] == df_weekdays.iloc[j,0]:
                df_country_weekday.iloc[i,4] = df_weekdays.iloc[j,1]

    df_country_weekday = df_country_weekday.sort_values('weekday_code', inplace=False)
    df_country_weekday = df_country_weekday.reset_index()
    
    # Create animation
    fig3_weekday = px.choropleth(df_country_weekday,               
        locations = "country_ISO_code",               
        color = "article_sentiment",
        animation_frame = "weekday",                
        hover_name = "country",
        hover_data={
            "article_sentiment": True,
            "weekday": True,
            "country_ISO_code": False,
        },            
        color_continuous_scale = 'RdBu',    
        range_color=(-0.8,0.8),
        title = 'Global News Sentiment by Day of the Week (2015-2017)',
        height = 800             
    )
    fig3_weekday_json = json.dumps(fig3_weekday, cls=plotly.utils.PlotlyJSONEncoder)
    return fig3_weekday_json


def choropleth_us_overtime():
   
    # Extract year-month from date to groupby over time
    df_state_time = df[['state', 'US_state_code', 'article_sentiment', 'pub_date']].copy()
    df_state_time['year_month'] = " "    # Extract only month and year from date
    df_state_time = df_state_time[['state', 'US_state_code', 'article_sentiment', 'pub_date', 'year_month']]

    for i in range(len(df_state_time)):
        pub_date = df_state_time.iloc[i,3]
        df_state_time.iloc[i,4] = pub_date[:7]
        df_state_time['article_sentiment'][i] = "{:.4f}".format(df_state_time['article_sentiment'][i])
        
    # Get mean sentiment scores for each state by year-month
    group_by_time = df_state_time.groupby(['year_month', 'state', 'US_state_code'], as_index=False)['article_sentiment'].mean()
    df_state_time = pd.DataFrame({
        'state':group_by_time.state, 
        'US_state_code':group_by_time.US_state_code, 
        'article_sentiment':group_by_time.article_sentiment, 
        'year_month':group_by_time.year_month
    })
    
    # Create animation
    fig4_time = px.choropleth(df_state_time,               
        locations = "US_state_code",               
        color = "article_sentiment",
        hover_name = "state",
        hover_data = {
            "article_sentiment": True,
            "year_month": True,                  
            "US_state_code": False,
        },
        animation_frame = "year_month",   
        color_continuous_scale = 'RdBu',
        range_color = (-0.8,0.8),
        locationmode = 'USA-states',
        scope = "usa",
        title = 'US News Sentiment Over Time (2015-2017)',
        height = 800             
    )
    fig4_time_json = json.dumps(fig4_time, cls=plotly.utils.PlotlyJSONEncoder)
    return fig4_time_json
    

def choropleth_us_bymonth():

    # Get mean sentiment scores by month
    df_state_month = df[['state', 'US_state_code', 'article_sentiment', 'month']].copy()
    group_by_month = df_state_month.groupby(['month', 'state', 'US_state_code'], as_index=False)['article_sentiment'].mean()
    df_state_month = pd.DataFrame({
        'state':group_by_month.state, 
        'US_state_code':group_by_month.US_state_code, 
        'article_sentiment':group_by_month.article_sentiment, 
        'month':group_by_month.month
    })

    for i in range(len(df_state_month)):
        df_state_month['article_sentiment'][i] = "{:.4f}".format(df_state_month['article_sentiment'][i])
        
    # Sort data by correct order of months
    df_state_month['month_code'] = " "
    df_state_month = df_state_month[['state', 'US_state_code', 'article_sentiment', 'month', 'month_code']]

    months_dict = {
        'month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'month_code': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        }
    df_months = pd.DataFrame(months_dict, columns = ['month', 'month_code'])

    for i in range(len(df_state_month)):
        for j in range(len(df_months)):
            if df_state_month.iloc[i,3] == df_months.iloc[j,0]:
                df_state_month.iloc[i,4] = df_months.iloc[j,1]

    df_state_month = df_state_month.sort_values('month_code', inplace=False)
    df_state_month = df_state_month.reset_index()

    # Create animation
    fig5_month = px.choropleth(df_state_month,               
        locations = "US_state_code",               
        color = "article_sentiment",
        animation_frame = "month",               
        hover_name = "state",  
        hover_data = {
            "article_sentiment": True,
            "month": True,
            "US_state_code": False,
        },               
        color_continuous_scale = 'BrBg', 
        range_color = (-0.8,0.8),
        locationmode = 'USA-states',
        scope = "usa",
        title = 'US News Sentiment by Month (2015-2017)',
        height = 800             
    )
    fig5_month_json = json.dumps(fig5_month, cls=plotly.utils.PlotlyJSONEncoder)
    return fig5_month_json


def choropleth_us_byweekday():
    
    # Get mean sentiment scores by state by day of the week
    df_state_weekday = df[['state', 'US_state_code', 'article_sentiment', 'weekday']].copy()
    group_by_weekday = df_state_weekday.groupby(['weekday', 'state', 'US_state_code'], as_index=False)['article_sentiment'].mean()
    df_state_weekday = pd.DataFrame({
        'state':group_by_weekday.state, 
        'US_state_code':group_by_weekday.US_state_code, 
        'article_sentiment':group_by_weekday.article_sentiment, 
        'weekday':group_by_weekday.weekday
    })

    for i in range(len(df_state_weekday)):
        df_state_weekday['article_sentiment'][i] = "{:.4f}".format(df_state_weekday['article_sentiment'][i])
        
    # Sort data by correct order of weekdays
    df_state_weekday['weekday_code'] = " "
    df_state_weekday = df_state_weekday[['state', 'US_state_code', 'article_sentiment', 'weekday', 'weekday_code']]

    weekdays_dict = {
        'weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'weekday_code': [1, 2, 3, 4, 5, 6, 7]
        }
    df_weekdays = pd.DataFrame(weekdays_dict, columns = ['weekday', 'weekday_code'])

    for i in range(len(df_state_weekday)):
        for j in range(len(df_weekdays)):
            if df_state_weekday.iloc[i,3] == df_weekdays.iloc[j,0]:
                df_state_weekday.iloc[i,4] = df_weekdays.iloc[j,1]

    df_state_weekday = df_state_weekday.sort_values('weekday_code', inplace=False)
    df_state_weekday = df_state_weekday.reset_index()
    
    # Create animation
    fig6_weekday = px.choropleth(df_state_weekday,               
        locations = "US_state_code",               
        color = "article_sentiment",
        animation_frame = "weekday",                
        hover_name = "state",  
        hover_data = {
            "article_sentiment": True,
            "weekday": True,
            "US_state_code": False,
        },   
        color_continuous_scale = 'RdBu',
        range_color = (-0.6,0.6),
        locationmode = 'USA-states',
        scope = "usa",
        title = 'US News Sentiment by Day of the Week (2015-2017)',
        height = 800             
    )
    fig6_weekday_json = json.dumps(fig6_weekday, cls=plotly.utils.PlotlyJSONEncoder)
    return fig6_weekday_json

    

