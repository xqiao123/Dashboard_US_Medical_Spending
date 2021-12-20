'''
Individual GitHub Project

'''

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
#import geopandas


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


### pandas data frame to html table
def generate_table(dataframe, max_rows=6):
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
geo_df=pd.read_csv('medical.csv')
'''
med=pd.read_csv('medical.csv')
noContLst=['Alaska','Hawaii','District of Columbia','American Samoa','Guam','Commonwealth of the Northern Mariana Islands','Puerto Rico','U.S. Virgin Islands']
med2=med[~med.State.isin(noContLst)] #48 rows
states=geopandas.read_file('states/states.shp')
'''

##Map
#geo_df=pd.merge(states, med2, how='right',left_on='STATE_NAME',right_on='State') #geopandas
geo_df.index=geo_df.State
geo_df.MSPB=geo_df.MSPB.astype(int)
geo_df.Obamacare=np.where(geo_df.Obamacare==0,'No','Yes')
'''
fig = px.choropleth(geo_df,
                    geojson=geo_df.geometry,
                    locations=geo_df.index,
                    color='MSPB',
                    height=800,
                    width=1000,
                    color_continuous_scale='Blues')
'''
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
    html.H3('Medical Spending Per Beneficiary By State in 2018',
            style={'textAlign' : 'center',
                   'color':'navy',
                   'font-family':'serif'}),
    html.Div([html.H6('Introduction: ',
                      style={'color':'navy',
                             'font-family':'serif'}),
             html.Article("This is an interactive dashboard for the user to compare each state's Medical Spending Per Beneficiary (MSPB) in the contiguous US,\
              and explore the features of states that may have influence on MSPB based on the dashboard.\
              The user can change the plots (and corresponding legends) or table results according to following options:",
                          style={'width':'100%'})]),
    html.Div(html.Article(" 1) Obamacare Dropdown: it allows the user to filter states that adopt or don't adopt Obamacare.")),
    html.Div(html.Article(" 2) Unemployment Rate Slider: it allows the user to filter states that match the range of 'Unemployment Rate' selected.")),
    html.Div(html.Article(" 3) Smoking Rate Slider: it allows the user to filter states that match the range of 'Smoking Rate' selected.")),
    html.Br(),
    html.Div([html.H6('Instruction: ',
                      style={'color':'navy',
                             'font-family':'serif'}),
              html.Article(" 1) Please single or multi select the 'Obamacare Dropdown' option, and use 'Unemployment Rate Slider' or 'Smoking Rate Slider' to narrow down the states that you're interested in based on the condition you set.\
              Then you'll see the change on the map plot, box plot, two scatter plots and the table below."),
              html.Article(" 2) Please hover your mouse on the state in the map plot to see the state name and MSPB; Please hover the mouse on box-plot to see the median and other values;\
              Please hover the mouse on the straight line in two scatter plots to see the statistical summary and the equation for the model fitted."),
              html.Article(" 3) The result table only shows top 6 states and their information based on the highest MSPB that match your selection, and it also shows the total number of states \
              that match your selection at the bottom of the table.",
                 style={'width':'100%'})]),
    html.Br(),
    html.Br(),
    html.Div([html.H6('Detailed Information for Top 6 States with the Highest MSPB',
                      style={'color':'vavy',
                             'font-family':'serif'}),
             html.Div(id='table_box')],
             style={'width':'40%', 'float':'right'}),
    html.Div(html.Article('-'*200), style={'color':'silver'}),
    html.Div([html.H6('Obamacare Dropdown:',
                      style={'color':'savy',
                             'font-family':'serif'}),
              dcc.Dropdown(options=[{'label': 'Yes', 'value': 'Yes'},
                                    {'label': 'No', 'value': 'No'}],
                           multi=True,
                           value=['Yes', 'No'],
                           id = 'obamacare_dropdown')],
              style={'display':'inline-block',
                     'padding':90,
                     'color':'savy',
                     'font-family':'serif',
                     'width':'15%'}),
    html.Div([html.H6('Unemployment Rate Slider:'),
              dcc.RangeSlider(id='my-range-slider',
                              min=2.5,
                              max=5.5,
                              step=0.5,
                              value=[2.5,5.5],
                              tooltip={"placement": "bottom", "always_visible": True})],
               style={'width':'20%', 
                      'display':'inline-block',
                      'padding':80,
                      'color':'savy',
                     'font-family':'serif'}),
    html.Div([html.H6('Smoking Rate Slider:'),
              dcc.RangeSlider(id='my-range-slider2',
                              min=9,
                              max=25,
                              step=4,
                              value=[9,25],
                              tooltip={"placement": "bottom", "always_visible": True})],
               style={'width':'20%', 
                      'display':'inline-block',
                      'padding':90,
                      'color':'savy',
                      'font-family':'serif'}),
    html.Div(dcc.Graph(figure=fig3, 
                       id='scatter_plot2'), 
              style={'width' : '50%', 
                     'display':'inline-block'}),
    html.Div(dcc.Graph(figure=fig4, 
                       id='scatter_plot3'), 
              style={'width' : '50%',
                     'display':'inline-block'}),
     html.Div(dcc.Graph(figure=fig2, 
                       id='scatter_plot'), 
              style={'width' : '100%',
                     'display':'inline-block' }),
    html.Br(),
    html.Div([html.H6('My Findings: ',
                      style={'color':'navy',
                             'font-family':'serif'}),
          html.Article("When I don't adjust any dropdown or sliders, I have below findings:"),
          html.Article(" 1) Maryland has the highest MSPB ($10,061), and MSPB is relatively high in the Midwest and East of the United States according to the map plot."),
          html.Article(" 2) Based on the 'Obamacare Adopted vs MSPB' plot, the median MSPB for 'No' ($6,378) is lower than that of 'Yes' ($6,709), but the lowest MSPB is in 'Yes' class."),
          html.Article(" 3) In the scatter plot 'Unemployment Rate vs MSPB' we can find the line is going down a little bit with the increase on Unemployment Rate, the equation for the straight line is y_hat=-82*x+7169, which means every one unit increase on the Unemployment Rate, the estimated MSPB value will decrease about $82 on average when other variables keep fixed."),
          html.Article(" 4) In the other scatter plot 'Smoking Rate vs MSPB', we can find the weak upward trend for the straight line, the equation for the model is y_hat=20*x+6525, which means every one unit increase on the Smoking Rate, the estimated MSPB will increase $20 on average when other variables keep fixed. Although we use linear regression models to fit both scatter plots,\
                        R-squared are very small for both models. Thus, in the further analysis, I'll use more advanced models to fit datasets.",
                        style={'width':'100%'})]),
    html.Br(),
    html.Div([html.H6('References: ',
                      style={'color':'navy',
                             'font-family':'serif'}),
          html.Article('Below is a list of data sources and references used for the dashbboard:',
                       style={'width':'100%'})]),
    html.A('The Facts on Medicare Spending and Financing',
           href='https://www.kff.org/medicare/issue-brief/the-facts-on-medicare-spending-and-financing/',
           target='_blank',
           style={'float':'left'}),
    html.Br(),
    html.A('State Health Facts',
           href='https://www.kff.org/state-category/medicare/medicare-enrollment-by-eligibility-category/',
           target='_blank'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(html.Article('-'*200), style={'color':'silver'}),
    html.Div(html.Article('Copyright ©2021 Xuefei Qiao, All rights reserved.',
                          style={'font-style':'italic'})),
    ])


server = app.server


##CallBack
#map plot
'''
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
'''

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
    fig3.update_layout(title_text='Unemployment Rate vs MSPB')
    fig3.update(layout = dict(title=dict(x=0.5)))
    if len(geo_df2)>0:
        fig3_results=px.get_trendline_results(fig3).px_fit_results.iloc[0]
        fig3['data'][0]['showlegend']=True
        fig3['data'][0]['name']='State'   
        fig3['data'][1]['showlegend']=True
        fig3['data'][1]['name']='y='+str(int(fig3_results.params[1]))+'*x+'+str(int(fig3_results.params[0]))
                       
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
    fig4.update_layout(title_text='Smoking Rate vs MSPB')
    fig4.update(layout = dict(title=dict(x=0.5)))
    if len(geo_df2)>0:
        fig4_results=px.get_trendline_results(fig4).px_fit_results.iloc[0]
        fig4['data'][0]['showlegend']=True
        fig4['data'][0]['name']='State'   
        fig4['data'][1]['showlegend']=True
        fig4['data'][1]['name']='y='+str(int(fig4_results.params[1]))+'*x+'+str(int(fig4_results.params[0]))
        
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
    geo_df3=geo_df2[['State','MSPB','Obamacare','Unemployment_Rate','Smoking_Rate']]
    geo_df4=geo_df3.rename(columns={'Unemployment_Rate':'Unemployment Rate','Smoking_Rate':'Smoking Rate'})
    return generate_table(geo_df4), '*There are '+str(len(geo_df4))+' states match your selection.'


if __name__ == '__main__':
    app.run_server(debug=True)

