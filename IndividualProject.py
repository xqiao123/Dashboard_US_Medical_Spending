'''
Individual GitHub Project

https://sylwiamielnicka.com/blog/advanced-plotly-sliders-and-dropdown-menus/
'''

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas

pd.set_option('display.max_columns', 1000) 
pd.set_option('display.max_rows', 1000) 
pd.set_option('display.width', 1000)


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


### pandas data frame to html table
def generate_table(dataframe, max_rows=7):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)


##Preparation
med=pd.read_pickle('medical.pkl')
noContLst=['Alaska','Hawaii','District of Columbia','American Samoa','Guam','Commonwealth of the Northern Mariana Islands','Puerto Rico','U.S. Virgin Islands']
med2=med[~med.State.isin(noContLst)] #48 rows
states=geopandas.read_file('states/states.shp')


##Map
geo_df=pd.merge(states, med2, how='right',left_on='STATE_NAME',right_on='State') #geopandas
geo_df.index=geo_df.State
geo_df.MSPB=geo_df.MSPB.astype(int)
geo_df.Obamacare=np.where(geo_df.Obamacare==0,'No','Yes')

fig = px.choropleth(geo_df,
                    geojson=geo_df.geometry,
                    locations=geo_df.index,
                    color='MSPB',
                    height=800,
                    width=1000,
                    color_continuous_scale='Blues')


fig2=px.box(geo_df, x="Obamacare", y="MSPB",
            color_discrete_sequence=['steelblue'],
            height=400, width=550)
fig3=px.scatter(geo_df, x='Unemployment_Rate',y='MSPB', trendline='ols',
                trendline_color_override='steelblue', 
                color_discrete_sequence=['silver'],
                height=400, width=550)
fig4=px.scatter(geo_df, x='Smoking_Rate',y='MSPB', trendline='ols', 
                trendline_color_override='steelblue', 
                color_discrete_sequence=['silver'],
                height=400, width=550)


##Lay out
app.layout = html.Div([
    html.H3('Medical Spending Per Beneficiary (MSPB) By State in 2018',
            style={'textAlign' : 'center'}),
    html.Br(),
    html.Div([html.H6('Background: '),
             html.Article("The State Medicare Spending Per Beneficiary (MSPB) measure can be used to evaluate medical efficiency and the cost of services performed by hospitals and other healthcare providers. According to the report from KFF (Kaiser Family Foundation), Medicare spending was 15 percent of total federal spending in 2018,\
              and is projected to rise to 18 percent by 2029, and was 21% of total health spending in 2018 in the United States.\
             It can be seen from the above that MSPB is a huge cost, and the large number of enrollees (92.9 million) also shows that the importance of the Medicare Plan,\
              so I think it is necessary to compare each state's MSPB in the contiguous US, and explore the features of states may have influence on MSPB based on the dashboard.",
                          style={'width':'100%'})]),
    html.Br(),
    html.Div([html.H6('Instructions: '),
              html.Article("Please single or multi select the 'Obamacare Dropdown' option, and use 'Unemployment Rate Slider' or 'Smoking Rate Slider' to narrow down the states that you're interested in based on the condition you set.\
              Then you'll see the change on the map plot, box plot, two scatter plots and the table below. You can hover your mouse on the state in the map plot to see the state name and MSPB; You can hover the mouse on box-plot to see the median and other values;\
              You can hover the mouse on the straight line in two scatter plots to see the statistical summary and the equation for the model fitted; You can also observe how the detailed information of states change in the table.",
                 style={'width':'100%'})]),
    html.Br(),
    html.Div(dcc.Graph(figure=fig, 
                       id='map_plot'), 
              style={'width' : '58%',
                     'display':'inline-block'}),
    html.Div([html.H6('Detailed Information for Top 7 States based on MSPB'),
             html.Div(id='table_box')],
             style={'width':'40%', 'float':'right'}),
    html.Div(html.Article('-'*240), style={'color':'silver'}),
    html.Div([html.H6('Obamacare Dropdown:'),
              dcc.Dropdown(options=[{'label': 'Yes', 'value': 'Yes'},
                                    {'label': 'No', 'value': 'No'}],
                           multi=True,
                           value=['Yes', 'No'],
                           id = 'obamacare_dropdown')],
              style={'display':'inline-block',
                     'padding':90}),
    html.Div([html.H6('Unemployment Rate Slider:'),
              dcc.RangeSlider(id='my-range-slider',
                              min=2.5,
                              max=5.5,
                              step=0.5,
                              value=[2.5,5.5],
                              tooltip={"placement": "bottom", "always_visible": True})],
               style={'width':'20%', 
                      'display':'inline-block',
                      'padding':80,}),
    html.Div([html.H6('Smoking Rate Slider:'),
              dcc.RangeSlider(id='my-range-slider2',
                              min=9,
                              max=25,
                              step=4,
                              value=[9,25],
                              tooltip={"placement": "bottom", "always_visible": True})],
               style={'width':'20%', 
                      'display':'inline-block',
                      'padding':90}),
    html.Div(dcc.Graph(figure=fig3, 
                       id='scatter_plot2'), 
              style={'width' : '50%', 
                     'display':'inline-block'}),
    html.Div(dcc.Graph(figure=fig4, 
                       id='scatter_plot3'), 
              style={'width' : '50%',
                     'display':'inline-block',
                     }),
     html.Div(dcc.Graph(figure=fig2, 
                       id='scatter_plot'), 
              style={'width' : '100%', 
                     'display':'inline-block'}),
    html.Br(),
    html.Div([html.H6('Summary: '),
          html.Article("When we don't adjust any dropdown or sliders, we can find that Maryland has the highest MSPB ($10,061), and MSPB is relatively high in the Midwest and East of the United States according to the map plot. Based on the 'Obamacare Adopted vs MSPB' plot, the median MSPB for 'No' ($6,378) is lower than that of 'Yes' ($6,709), but the lowest MSPB is in 'Yes' class. \
          In the scatter plot 'Unemployment Rate vs MSPB' we can find the line is going down a little bit with the increase on Unemployment Rate, the equation for the straight line is y_hat=-83*x+7169, which means every one unit increase on the Unemployment Rate, the estimated MSPB value will decrease about $83 on average when other variables keep fixed.\
          In the other scatter plot 'Smoking Rate vs MSPB', we can find the weak upward trend for the straight line, the equation for the model is y_hat=20*x+6526, which means every one unit increase on the Smoking Rate, the estimated MSPB will increase $20 on average when other variables keep fixed. Although we use linear regression models to fit both scatter plots,\
          R-squared are very small for both models. Thus, in the further analysis, I'll use more advanced models to fit datasets. When you use the slider to control those two scatter plots, you can see how does the line change to fit the partial states. When you use the drop-down to control the box plot, you can see how the median values change on two classes. Hope you'll have some interesting findings!",
                       style={'width':'100%'})]),
    html.Br(),
    html.A('Click here to learn more about the Medical Spending in US in 2018',
           href='https://www.kff.org/medicare/issue-brief/the-facts-on-medicare-spending-and-financing/',
           target='_blank',
           style={'float':'left'}),
    html.Br(),
    html.Br(),
    html.Div(html.Article('-'*240), style={'color':'silver'}),
    html.Br(),
    html.Div(html.Article('Copyright ©2021 Xuefei Qiao, All rights reserved.')),
    ])


server = app.server


##CallBack
#map plot
@app.callback(
    dash.dependencies.Output(component_id="map_plot", component_property="figure"),
    [dash.dependencies.Input(component_id="obamacare_dropdown", component_property="value"),
    dash.dependencies.Input(component_id='my-range-slider', component_property='value'),
    dash.dependencies.Input(component_id='my-range-slider2', component_property='value')]
)

def update_plot(obamacare, number_range, number_range2):
    geo_df2 = geo_df[((geo_df.Smoking_Rate<=(max(number_range2))) & (geo_df.Smoking_Rate>=(min(number_range2)))) & (geo_df.Obamacare.isin(obamacare)) & ((geo_df.Unemployment_Rate<=(max(number_range)))&(geo_df.Unemployment_Rate>=(min(number_range))))].sort_values('MSPB', ascending=False)
    fig = px.choropleth(geo_df2,
                    geojson=geo_df2.geometry,
                    locations=geo_df2.index,
                    color='MSPB',
                    height=500,
                    color_continuous_scale='Blues')
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(title_text='Contiguous US Map by MSPB')
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(coloraxis_colorbar={'title':'MSPB ($)'})          
    
    return fig


#Scatter Plot 1
@app.callback(
    dash.dependencies.Output(component_id="scatter_plot", component_property="figure"),
    [dash.dependencies.Input(component_id="obamacare_dropdown", component_property="value"),
    dash.dependencies.Input(component_id='my-range-slider', component_property='value'),
    dash.dependencies.Input(component_id='my-range-slider2', component_property='value')]
)


def update_plot2(obamacare, number_range, number_range2):
    geo_df2 = geo_df[((geo_df.Smoking_Rate<=(max(number_range2))) & (geo_df.Smoking_Rate>=(min(number_range2)))) & (geo_df.Obamacare.isin(obamacare)) & ((geo_df.Unemployment_Rate<=(max(number_range)))&(geo_df.Unemployment_Rate>=(min(number_range))))].sort_values('MSPB', ascending=False)
    fig2 = px.box(geo_df2, x="Obamacare", y="MSPB", color_discrete_sequence=['steelblue'],
                  labels={'MSPB':'MSPB ($)',
                          'Obamacare':'Obamacare Adopted'})
    fig2.update_layout(title_text='Obamacare Adopted vs MSPB')
    fig2.update(layout = dict(title=dict(x=0.5)))             
    
    return fig2


#Scatter Plot 2
@app.callback(
    dash.dependencies.Output(component_id="scatter_plot2", component_property="figure"),
    [dash.dependencies.Input(component_id="obamacare_dropdown", component_property="value"),
    dash.dependencies.Input(component_id='my-range-slider', component_property='value'),
    dash.dependencies.Input(component_id='my-range-slider2', component_property='value')]
)


def update_plot3(obamacare, number_range, number_range2):
    geo_df2 = geo_df[((geo_df.Smoking_Rate<=(max(number_range2))) & (geo_df.Smoking_Rate>=(min(number_range2)))) & (geo_df.Obamacare.isin(obamacare)) & ((geo_df.Unemployment_Rate<=(max(number_range)))&(geo_df.Unemployment_Rate>=(min(number_range))))].sort_values('MSPB', ascending=False)
    fig3=px.scatter(geo_df2, x='Unemployment_Rate',y='MSPB', trendline='ols',
                    trendline_color_override='steelblue', color_discrete_sequence=['silver'],
                    labels={'MSPB':'MSPB ($)',
                            'Unemployment_Rate':'Unemployment Rate'})
    fig3.update_layout(title_text='Unemployment Rate vs MSPB Per State')
    fig3.update(layout = dict(title=dict(x=0.5)))
                       
    return fig3


#Scatter Plot 3
@app.callback(
    dash.dependencies.Output(component_id="scatter_plot3", component_property="figure"),
    [dash.dependencies.Input(component_id="obamacare_dropdown", component_property="value"),
    dash.dependencies.Input(component_id='my-range-slider', component_property='value'),
    dash.dependencies.Input(component_id='my-range-slider2', component_property='value')]
)


def update_plot4(obamacare, number_range, number_range2):
    geo_df2 = geo_df[((geo_df.Smoking_Rate<=(max(number_range2))) & (geo_df.Smoking_Rate>=(min(number_range2)))) & (geo_df.Obamacare.isin(obamacare)) & ((geo_df.Unemployment_Rate<=(max(number_range)))&(geo_df.Unemployment_Rate>=(min(number_range))))].sort_values('MSPB', ascending=False)
    fig4=px.scatter(geo_df2, x='Smoking_Rate',y='MSPB', trendline='ols',
                    trendline_color_override='steelblue', color_discrete_sequence=['silver'],
                    labels={'MSPB':'MSPB ($)',
                            'Smoking_Rate':'Smoking Rate'})
    fig4.update_layout(title_text='Smoking Rate vs MSPB Per State')
    fig4.update(layout = dict(title=dict(x=0.5)))
    
    return fig4


#Table
@app.callback(
    Output(component_id='table_box', component_property='children'),
    [dash.dependencies.Input(component_id="obamacare_dropdown", component_property="value"),
    dash.dependencies.Input(component_id='my-range-slider', component_property='value'),
    dash.dependencies.Input(component_id='my-range-slider2', component_property='value')]
)

def update_table(obamacare, number_range, number_range2):
    geo_df2 = geo_df[((geo_df.Smoking_Rate<=(max(number_range2))) & (geo_df.Smoking_Rate>=(min(number_range2)))) & (geo_df.Obamacare.isin(obamacare)) & ((geo_df.Unemployment_Rate<=(max(number_range)))&(geo_df.Unemployment_Rate>=(min(number_range))))].sort_values('MSPB', ascending=False)                       
    geo_df3=geo_df2[['State','Obamacare','Unemployment_Rate','Smoking_Rate','MSPB']]
    
    return generate_table(geo_df3)


if __name__ == '__main__':
    app.run_server(debug=True)

