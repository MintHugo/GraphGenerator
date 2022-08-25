
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import webbrowser
from threading import Timer
from sqlalchemy import create_engine
#import MySQLdb
import warnings
import math
import datetime




"""This code is related to a dashboard and uses data from the database. Therefore, when launching the dashboard, it could take like 1-2 minutes
before it pops up on your screen.

The Dashboard is a grapg generator which can make a graph based on a date range, based on the inputs in the dashboard.

The graph generator can create a Mint Tower Fund, combined with up to 3 different indices based on a selection in the dashboard.

Also, there are statistics added in a table below the actual graph plot which should give statistics of the securities related to the selected time period"""

warnings.filterwarnings("ignore")

global df_sql, df_indices
#db = MySQLdb.connect(host="192.168.31.12",    
#                         user="mint_guest",        
#                         passwd="B3ursplein5!",
#                         db="HistoricalData")  
engine = create_engine('mysql://mint_guest:B3ursplein5!@192.168.31.12:3306/HistoricalData')


myQuery4 = '''SELECT distinct BloombergTicker FROM HistoricalData.Product_Static where HistoricalType="Index" or HistoricalType="Rate Index" or HistoricalType="Volatility Index" or HistoricalType="Index Future"  '''
compare_tickers = pd.read_sql_query(myQuery4, con = engine)
compare_tickers = compare_tickers.BloombergTicker.tolist()


myQuery5 = '''SELECT * FROM DailyData2 WHERE Ticker IN %(compare_tickers)s'''
df_indices = pd.read_sql_query(myQuery5, params= {'compare_tickers': compare_tickers}, con =engine)



df_sql = pd.read_sql('SELECT * FROM HistoricalData.MintFundClasses_NAV', con=engine)
#df_indices = pd.read_sql('SELECT * FROM HistoricalData.DailyData2 where Ticker = , con=engine)


app = dash.Dash(__name__,external_stylesheets = [dbc.themes.SANDSTONE])

#from datetime import date

inputrow1 = dcc.DatePickerSingle(id = 'bid',
    initial_visible_month= datetime.datetime(2011,1,1),
    date='2011-01-01',
    display_format='YYYY-MM-DD'
)



inputrow1_1 = dcc.DatePickerSingle(id = 'ask',
    initial_visible_month= datetime.datetime(2022,1,1),
    date='2022-01-01',
    display_format='YYYY-MM-DD'
)


inputrow1_2 = dbc.Row(
    [dbc.Col(
        dbc.FormGroup([
            dbc.Label('Select class'),
            dcc.Dropdown(
            id='checklistclassPLOT',
            options=[
                    {"label": "Lead - EUR", "value": "Lead - EUR"},
                    {"label": "I-Class - EUR", "value": "I-Class - EUR"},
                    {"label": "G-Class - EUR", "value": "G-Class - EUR"},
                    {"label": "Lead - USD", "value": "Lead - USD"},
                    {"label": "I-Class - USD", "value": "I-Class - USD"},
                    {"label": "G-Class - USD", "value": "G-Class - USD"},
                    #{"label": "G-Class - GBP", "value": "G-Class - GBP"},
                    {"label": "I-Class - CHF", "value": "I-Class - CHF"},
                    {"label": "G-Class - CHF", "value": "G-Class - CHF"},
                    {"label": "Lead - GBP", "value": "Lead - GBP"},
                    {"label": "I-Class - GBP", "value": "I-Class - GBP"},
                    {"label": "Lead - ILS", "value": "Lead - ILS"}
                ],
            value='Index'
            )])
            ),
    ])


inputrow3_1 = dbc.Row(
    [dbc.Col(
        dbc.FormGroup([
            dbc.Label('Select Index'),
            dcc.Dropdown(
            id='checklistindexPLOT',
            options=[
                    {"label": "Lead - EUR", "value": "Lead - EUR"},
                    {"label": "I-Class - EUR", "value": "I-Class - EUR"},
                    {"label": "G-Class - EUR", "value": "G-Class - EUR"},
                    {"label": "Lead - USD", "value": "Lead - USD"},
                    {"label": "I-Class - USD", "value": "I-Class - USD"},
                    {"label": "G-Class - USD", "value": "G-Class - USD"},
                    #{"label": "G-Class - GBP", "value": "G-Class - GBP"},
                    {"label": "I-Class - CHF", "value": "I-Class - CHF"},
                    {"label": "G-Class - CHF", "value": "G-Class - CHF"},
                    {"label": "Lead - GBP", "value": "Lead - GBP"},
                    {"label": "I-Class - GBP", "value": "I-Class - GBP"},
                    {"label": "Lead - ILS", "value": "Lead - ILS"},
                    {"label": "None", "value": ""},   
                    {"label": "AEX Index", "value": "AEX Index"},
                    {"label": "CAC Index", "value": "CAC Index"},
                    {"label": "DAX Index", "value": "DAX Index"},
                    {"label": "EUR001M Index", "value": "EUR001M Index"},
                    {"label": "EUR003M Index", "value": "EUR003M Index"},
                    {"label": "EUR006M Index", "value": "EUR006M Index"},
                    {"label": "FTSEMIB Index", "value": "FTSEMIB Index"},
                    {"label": "HFRXGL Index", "value": "HFRXGL Index"},
                    {"label": "HSCEI Index", "value": "HSCEI Index"},
                    {"label": "HSI Index", "value": "HSI Index"},
                    {"label": "IBOXHY Index", "value": "IBOXHY Index"},
                    {"label": "INDU Index", "value": "INDU Index"},
                    {"label": "LEGATREU Index", "value": "LEGATREU Index"},
                    {"label": "LEGATRUU Index", "value": "LEGATRUU Index"},
                    {"label": "LHVLTRUU Index", "value": "LHVLTRUU Index"},
                    {"label": "LUATTRUU Index", "value": "LUATTRUU Index"},
                    {"label": "MIGSEBI LX Index", "value": "MIGSEBI LX Index"},
                    {"label": "MXEU0RE Index", "value": "MXEU0RE Index"},
                    {"label": "MXWO Index", "value": "MXWO Index"},
                    {"label": "NDX Index", "value": "NDX Index"},
                    {"label": "NEIXCTA Index", "value": "NEIXCTA Index"},
                    {"label": "NKY Index", "value": "NKY Index"},
                    {"label": "RTY Index", "value": "RTY Index"},
                    {"label": "SGIXVR3U Index", "value": "SGIXVR3U Index"},
                    {"label": "SMI Index", "value": "SMI Index"},
                    {"label": "SPX Index", "value": "SPX Index"},
                    {"label": "SX5E Index", "value": "SX5E Index"},
                    {"label": "SX5T Index", "value": "SX5T Index"},
                    {"label": "SX7E Index", "value": "SX7E Index"},
                    {"label": "SXAP Index", "value": "SXAP Index"},
                    {"label": "SXEP Index", "value": "SXEP Index"},
                    {"label": "UKX Index", "value": "UKX Index"},
                    {"label": "US0001M Index", "value": "US0001M Index"},
                    {"label": "US0003M Index", "value": "US0003M Index"},
                    {"label": "US0006M Index", "value": "US0006M Index"},
                    {"label": "V2X Index", "value": "V2X Index"},
                    {"label": "VIX Index", "value": "VIX Index"},
                    {"label": "VSTX12M Index", "value": "VSTX12M Index"}
                ],
            value= 'Index'
            )])
            ),
    ])

inputrow3_2 = dbc.Row(
    [dbc.Col(
        dbc.FormGroup([
            dbc.Label('Select Index'),
            dcc.Dropdown(
            id='checklistindexPLOT2',
            options=[
                    {"label": "None", "value": ""},   
                    {"label": "AEX Index", "value": "AEX Index"},
                    {"label": "CAC Index", "value": "CAC Index"},
                    {"label": "DAX Index", "value": "DAX Index"},
                    {"label": "EUR001M Index", "value": "EUR001M Index"},
                    {"label": "EUR003M Index", "value": "EUR003M Index"},
                    {"label": "EUR006M Index", "value": "EUR006M Index"},
                    {"label": "FTSEMIB Index", "value": "FTSEMIB Index"},
                    {"label": "HFRXGL Index", "value": "HFRXGL Index"},
                    {"label": "HSCEI Index", "value": "HSCEI Index"},
                    {"label": "HSI Index", "value": "HSI Index"},
                    {"label": "IBOXHY Index", "value": "IBOXHY Index"},
                    {"label": "INDU Index", "value": "INDU Index"},
                    {"label": "LEGATREU Index", "value": "LEGATREU Index"},
                    {"label": "LEGATRUU Index", "value": "LEGATRUU Index"},
                    {"label": "LHVLTRUU Index", "value": "LHVLTRUU Index"},
                    {"label": "LUATTRUU Index", "value": "LUATTRUU Index"},
                    {"label": "MIGSEBI LX Index", "value": "MIGSEBI LX Index"},
                    {"label": "MXEU0RE Index", "value": "MXEU0RE Index"},
                    {"label": "MXWO Index", "value": "MXWO Index"},
                    {"label": "NDX Index", "value": "NDX Index"},
                    {"label": "NEIXCTA Index", "value": "NEIXCTA Index"},
                    {"label": "NKY Index", "value": "NKY Index"},
                    {"label": "RTY Index", "value": "RTY Index"},
                    {"label": "SGIXVR3U Index", "value": "SGIXVR3U Index"},
                    {"label": "SMI Index", "value": "SMI Index"},
                    {"label": "SPX Index", "value": "SPX Index"},
                    {"label": "SX5E Index", "value": "SX5E Index"},
                    {"label": "SX5T Index", "value": "SX5T Index"},
                    {"label": "SX7E Index", "value": "SX7E Index"},
                    {"label": "SXAP Index", "value": "SXAP Index"},
                    {"label": "SXEP Index", "value": "SXEP Index"},
                    {"label": "UKX Index", "value": "UKX Index"},
                    {"label": "US0001M Index", "value": "US0001M Index"},
                    {"label": "US0003M Index", "value": "US0003M Index"},
                    {"label": "US0006M Index", "value": "US0006M Index"},
                    {"label": "V2X Index", "value": "V2X Index"},
                    {"label": "VIX Index", "value": "VIX Index"},
                    {"label": "VSTX12M Index", "value": "VSTX12M Index"}
                ],
            value=""
            )])
            ),
    ])

inputrow3_3 = dbc.Row(
    [dbc.Col(
        dbc.FormGroup([
            dbc.Label('Select Index'),
            dcc.Dropdown(
            id='checklistindexPLOT3',
            options=[
                    {"label": "None", "value": ""},   
                    {"label": "AEX Index", "value": "AEX Index"},
                    {"label": "CAC Index", "value": "CAC Index"},
                    {"label": "DAX Index", "value": "DAX Index"},
                    {"label": "EUR001M Index", "value": "EUR001M Index"},
                    {"label": "EUR003M Index", "value": "EUR003M Index"},
                    {"label": "EUR006M Index", "value": "EUR006M Index"},
                    {"label": "FTSEMIB Index", "value": "FTSEMIB Index"},
                    {"label": "HFRXGL Index", "value": "HFRXGL Index"},
                    {"label": "HSCEI Index", "value": "HSCEI Index"},
                    {"label": "HSI Index", "value": "HSI Index"},
                    {"label": "IBOXHY Index", "value": "IBOXHY Index"},
                    {"label": "INDU Index", "value": "INDU Index"},
                    {"label": "LEGATREU Index", "value": "LEGATREU Index"},
                    {"label": "LEGATRUU Index", "value": "LEGATRUU Index"},
                    {"label": "LHVLTRUU Index", "value": "LHVLTRUU Index"},
                    {"label": "LUATTRUU Index", "value": "LUATTRUU Index"},
                    {"label": "MIGSEBI LX Index", "value": "MIGSEBI LX Index"},
                    {"label": "MXEU0RE Index", "value": "MXEU0RE Index"},
                    {"label": "MXWO Index", "value": "MXWO Index"},
                    {"label": "NDX Index", "value": "NDX Index"},
                    {"label": "NEIXCTA Index", "value": "NEIXCTA Index"},
                    {"label": "NKY Index", "value": "NKY Index"},
                    {"label": "RTY Index", "value": "RTY Index"},
                    {"label": "SGIXVR3U Index", "value": "SGIXVR3U Index"},
                    {"label": "SMI Index", "value": "SMI Index"},
                    {"label": "SPX Index", "value": "SPX Index"},
                    {"label": "SX5E Index", "value": "SX5E Index"},
                    {"label": "SX5T Index", "value": "SX5T Index"},
                    {"label": "SX7E Index", "value": "SX7E Index"},
                    {"label": "SXAP Index", "value": "SXAP Index"},
                    {"label": "SXEP Index", "value": "SXEP Index"},
                    {"label": "UKX Index", "value": "UKX Index"},
                    {"label": "US0001M Index", "value": "US0001M Index"},
                    {"label": "US0003M Index", "value": "US0003M Index"},
                    {"label": "US0006M Index", "value": "US0006M Index"},
                    {"label": "V2X Index", "value": "V2X Index"},
                    {"label": "VIX Index", "value": "VIX Index"},
                    {"label": "VSTX12M Index", "value": "VSTX12M Index"}
                ],
            value=""
            )])
            ),
    ])

# =============================================================================
inputrow3_4 = dbc.Row(
    [dbc.Col(
        dbc.FormGroup([
            dbc.Label('Title or No Title'),
            dcc.Dropdown(
            id='checklistindexPLOT4',
            options=[
                    {"label": "None", "value": ""},
                    {"label": "ENG TITLE", "value": "ENG TITLE"},
                    {"label": "DUTCH TITLE", "value": "DUTCH TITLE"},
                    {"label": "NO TITLE", "value": "NO TITLE"}
                    
                ],
            value=""
            )])
            ),
    ])
# =============================================================================

inputrow3_5 = dbc.Row(
    [dbc.Col(
        dbc.FormGroup([
            dbc.Label('Legend or No Legend'),
            dcc.Dropdown(
            id='checklistindexPLOT5',
            options=[
                    {"label": "None", "value": ""},
                    {"label": "WITH LEGEND", "value": "WITH LEGEND"},
                    {"label": "NO LEGEND", "value": "NO LEGEND"}                   

                ],
            value=""
            )])
            ),
    ])

inputrow3_6 = dbc.Row(
    [dbc.Col(
        dbc.FormGroup([
            dbc.Label('Axis color'),
            dcc.Dropdown(
            id='checklistindexPLOT6',
            options=[
                    {"label": "None", "value": ""},
                    {"label": "Gold color", "value": "Gold color"},
                    {"label": "White color", "value": "White color"}
                    
                ],
            value=""
            )])
            ),
    ])


returnmtaf = dbc.Row(
    [dbc.Col(
    html.Div('Mint Tower Fund return:')
            ),
     dbc.Col(
    html.Div(id='returnmtaf')
            )
    ])

returnindex = dbc.Row(
    [dbc.Col(
    html.Div('Index 1 return:')
            ),
     dbc.Col(
    html.Div(id='returnindex')
            )
    ])

returnindex2 = dbc.Row(
    [dbc.Col(
    html.Div('Index 2 return:')
            ),
     dbc.Col(
    html.Div(id='returnindex2')
            )
    ])

returnindex3 = dbc.Row(
    [dbc.Col(
    html.Div('Index 3 return')
            ),
     dbc.Col(
    html.Div(id='returnindex3')
            )
    ])

volatilitymtaf = dbc.Row(
    [dbc.Col(
    html.Div('Volatility Mint Tower Fund:')
            ),
     dbc.Col(
    html.Div(id='volatilitymtaf')
            )
    ])

volatilityindex = dbc.Row(
    [dbc.Col(
    html.Div('Volatility Index 1:')
            ),
     dbc.Col(
    html.Div(id='volatilityindex')
            )
    ])

volatilityindex2 = dbc.Row(
    [dbc.Col(
    html.Div('Volatility Index 2:')
            ),
     dbc.Col(
    html.Div(id='volatilityindex2')
            )
    ])

volatilityindex3 = dbc.Row(
    [dbc.Col(
    html.Div('Volatility Index 3:')
            ),
     dbc.Col(
    html.Div(id='volatilityindex3')
            )
    ])

correlation1 = dbc.Row(
    [dbc.Col(
    html.Div('Correlation Mint Tower Fund - Index 1:')
            ),
     dbc.Col(
    html.Div(id='correlation1')
            )
    ])

correlation2 = dbc.Row(
    [dbc.Col(
    html.Div('Correlation Mint Tower Fund - Index 2:')
            ),
     dbc.Col(
    html.Div(id='correlation2')
            )
    ])

correlation3 = dbc.Row(
    [dbc.Col(
    html.Div('Correlation Mint Tower Fund - Index 3:')
            ),
     dbc.Col(
    html.Div(id='correlation3')
            )
    ])


#this function ceates an empty plot in the dashboard which will be filled in with the code
def blank_fig():
    fig1 = go.Figure(go.Scatter(x=[], y = []))
    fig1.update_layout(template = None)
    fig1.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig1.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig1

graph1 = dbc.Row([dbc.Col([dbc.Spinner([
   dcc.Graph(id='casegraph', figure=blank_fig(), )
                ]          
                )])
        ])

app.layout =dbc.Container([
                html.H1('Graph Generator Dasboard'),
                html.Hr(),
                dbc.Row(
                    [dbc.Col(
                        [html.P('Through this dashboard you can create graphs for a specific range based on a Mint Tower fund and an index. Left date is the START, Right date is the END'),

                         inputrow1,
                         inputrow1_1,
                         html.Hr(),
                         inputrow1_2,
                         inputrow3_1,
                         inputrow3_2,
                         inputrow3_3,
                         inputrow3_4,
                         inputrow3_5,
                         inputrow3_6,
                         html.Hr(),
                         dbc.Row([
                         dbc.Button('Plot Graph', id='button1', n_clicks=int(0))]),                        
                         ]                             
                            ,width=4
                         )
                         ,
                    dbc.Col(
                        [graph1,
                         html.Hr(),
                         returnmtaf,
                         returnindex,
                         returnindex2,
                         returnindex3,
                         html.Hr(),
                         volatilitymtaf,
                         volatilityindex,
                         volatilityindex2,
                         volatilityindex3,
                         html.Hr(),
                         correlation1,
                         correlation2,
                         correlation3,
                         html.Hr(),

                         ]
                         ,width=8
                         )]
                                      
               ,)])

@app.callback( 
    [Output('casegraph','figure'),
     Output('returnmtaf', 'children'),
     Output('returnindex','children'),
     Output('returnindex2','children'),
     Output('returnindex3','children'),
     Output('volatilitymtaf','children'),
     Output('volatilityindex','children'),
     Output('volatilityindex2','children'),
     Output('volatilityindex3','children'),
     Output('correlation1','children'),
     Output('correlation2','children'),
     Output('correlation3','children')],
    [Input('button1','n_clicks')],
    [State('bid','date'),
     State('ask','date'),
     State('checklistclassPLOT','value'),
     State('checklistindexPLOT','value'),
     State('checklistindexPLOT2','value'),
     State('checklistindexPLOT3','value'),
     State('checklistindexPLOT4','value'),
     State('checklistindexPLOT5','value'),
     State('checklistindexPLOT6','value'),
     ]
                )


#this function activates the code when clicking on "Plot graph" button in the dashboard
def update_sheet(clicks, bid, ask, checklistclassPLOT, checklistindexPLOT, checklistindexPLOT2, checklistindexPLOT3, checklistindexPLOT4, checklistindexPLOT5, checklistindexPLOT6): #checklistindexPLOT4, 
    
    if clicks == 0:
        raise PreventUpdate
            
    else:

        #str(df_sql_52['ValueDate'].iloc[0])[:4] != str(df_sql_52['ValueDate'].iloc[-1])[:4]:        
        print(bid)
        print(ask)
        def create_variables():
            global Datebefore, Datenow, Fund_Name, Index_Name, Index_Name2, Index_Name3, Text, Legend, Axis_color, Title
            Datebefore = bid
            Datenow = ask
            Fund_Name = checklistclassPLOT
            Index_Name = checklistindexPLOT
            Index_Name2 = checklistindexPLOT2
            Index_Name3 = checklistindexPLOT3
            Title = checklistindexPLOT4
            Legend = checklistindexPLOT5
            Axis_color = checklistindexPLOT6
        create_variables()
        
        #this function creates the right dataframe based on the time interval selected in the dashboard
        def mint_fund_data():
            global df_sql_2, df_sql_22, df_sql_32, total_rows_sql2
            df_sql['ValueDate'] = pd.to_datetime(df_sql['ValueDate'])
            Datefilter_NAV = (df_sql['ValueDate'] >= Datebefore) & (df_sql['ValueDate'] <= Datenow)
            df_sql_1 = df_sql.loc[Datefilter_NAV]
            df_sql_2 = df_sql_1.loc[df_sql_1['Fictive'] == 1]       
            df_sql_22 = df_sql_2.loc[df_sql_2['Name'].isin([(Fund_Name)])]
            df_sql_32 = df_sql_22.reset_index(drop=True)
            total_rows_sql2 = len(df_sql_32["NAV"].axes[0])
        mint_fund_data()

        #this function creates a dataframe which sets the relevant Mint Tower NAV to 100 and calculates percentage changes
        def calculate_return_nav():
            global Mint_return, df_sql_52, df_sql_62, b
            
            for i in range(total_rows_sql2):
                if i == 0:
                    df_sql_32["NAV1"] = 100.00000000
                else:
                    df_sql_32["NAV1"][i] = (df_sql_32["NAV"][i]/(df_sql_32["NAV"][(i-1)]))* df_sql_32["NAV1"][(i-1)]
                    
            df_sql_32['%Change'] = ((df_sql_32['NAV1'] -100))
            r2 = pd.date_range(start=df_sql_32.ValueDate.min(), end=df_sql_32.ValueDate.max())
            df_sql_42 = df_sql_32.set_index('ValueDate').reindex(r2).fillna(0.0).rename_axis('ValueDate').reset_index()
            new_2 = df_sql_42['NAV1'].replace(to_replace=0, method='ffill')
            new22 = new_2.tolist()            
            df_sql_52 = df_sql_42.assign(NAV1 = new22)            
            df_sql_62 = df_sql_52        
            df_sql_62['%Change'] = df_sql_62['%Change'].round(6)       
            b = (df_sql_62['%Change'].iloc[-1])/100        
            Mint_return = str(round((b*100),2))
            #Mint_return = str(f'{(b):+.2%}')
        calculate_return_nav()

                    
        
        
        #this function creates the right dataframe based on the time interval selected in the dasboard, for up to three different indices
        def index_data():
            global total_rows_index, total_rows_index2, total_rows_index3, df_indices_3, df_indices_32, df_indices_33, Index_Name_2, Index_Name_22, Index_Name_23
            df_indices1 = df_indices.loc[df_indices['Ticker'].isin([(str(Index_Name))])]
    
            if Index_Name2 != "": 
                df_indices12 = df_indices.loc[df_indices['Ticker'].isin([(Index_Name2)])]
            else:
                df_indices12 = df_indices.loc[df_indices['Ticker'].isin([(Index_Name)])]   
                
            if Index_Name3 != "":    
                df_indices13 = df_indices.loc[df_indices['Ticker'].isin([(Index_Name3)])]
            else: 
                df_indices13 = df_indices.loc[df_indices['Ticker'].isin([(Index_Name)])]  
        
            df_indices1['ValueDate'] = pd.to_datetime(df_indices1['ValueDate'])
            df_indices12['ValueDate'] = pd.to_datetime(df_indices12['ValueDate'])
            df_indices13['ValueDate'] = pd.to_datetime(df_indices13['ValueDate'])
        
            Datefilter_Index = (df_indices1['ValueDate'] >= Datebefore) & (df_indices1['ValueDate'] <= Datenow)
            Datefilter_Index2 = (df_indices12['ValueDate'] >= Datebefore) & (df_indices12['ValueDate'] <= Datenow)
            Datefilter_Index3 = (df_indices13['ValueDate'] >= Datebefore) & (df_indices13['ValueDate'] <= Datenow)
    
            df_indices_2 = df_indices1.loc[Datefilter_Index]
            df_indices_22 = df_indices12.loc[Datefilter_Index2]
            df_indices_23 = df_indices13.loc[Datefilter_Index3]

            df_indices_3 = df_indices_2.reset_index(drop=True)
            df_indices_32 = df_indices_22.reset_index(drop=True)
            df_indices_33 = df_indices_23.reset_index(drop=True)
            
            ##########################ADJUSTED####################################
            print(df_indices1['Ticker'])
            Index_Name_2 = df_indices1['Ticker'].iloc[1]
            
            Index_Name_22 = df_indices12['Ticker'].iloc[1]
            Index_Name_23 = df_indices13['Ticker'].iloc[1]
            
            total_rows_index = len(df_indices_2["Value"].axes[0])
            total_rows_index2 = len(df_indices_22["Value"].axes[0])
            total_rows_index3 = len(df_indices_23["Value"].axes[0])
        index_data()
        
            
        #this function creates a dataframe which sets the relevant Mint Tower NAV to 100 and calculates percentage changes
        def calculate_return_indices():
            global Index_return, Index_return2, Index_return3, df_indices_5, df_indices_52, df_indices_53, a, a2, a3
            
            for i in range(total_rows_index):
                if i == 0:
                    df_indices_3["NAV1"] = 100.00000000
                else:
                    df_indices_3["NAV1"][i] = (df_indices_3["Value"][i]/(df_indices_3["Value"][(i-1)]))* df_indices_3["NAV1"][(i-1)] 
            
            for i in range(total_rows_index2):
                if i == 0:
                    df_indices_32["NAV1"] = 100.00000000
                else:
                    df_indices_32["NAV1"][i] = (df_indices_32["Value"][i]/(df_indices_32["Value"][(i-1)]))* df_indices_32["NAV1"][(i-1)]     
            
            for i in range(total_rows_index3):
                if i == 0:
                    df_indices_33["NAV1"] = 100.00000000
                else:
                    df_indices_33["NAV1"][i] = (df_indices_33["Value"][i]/(df_indices_33["Value"][(i-1)]))* df_indices_33["NAV1"][(i-1)]     
        
        
            df_indices_3["Name"] = df_indices_3["Ticker"]
            df_indices_32["Name"] = df_indices_32["Ticker"]
            df_indices_33["Name"] = df_indices_33["Ticker"]
        
            df_indices_3['%Change'] = ((df_indices_3['NAV1'] -100))
            df_indices_32['%Change'] = ((df_indices_32['NAV1'] -100))
            df_indices_33['%Change'] = ((df_indices_33['NAV1'] -100))
        
            df_indices_4 = df_indices_3
            df_indices_42 = df_indices_32
            df_indices_43 = df_indices_33
        
            df_indices_4['%Change'] = df_indices_4['%Change'].astype(float)
            df_indices_42['%Change'] = df_indices_42['%Change'].astype(float)
            df_indices_43['%Change'] = df_indices_43['%Change'].astype(float)
        
            df_indices_5 = df_indices_4
            df_indices_52 = df_indices_42
            df_indices_53 = df_indices_43
                    
            df_indices_5['%Change'] = df_indices_5['%Change'].round(6)
            df_indices_52['%Change'] = df_indices_52['%Change'].round(6)
            df_indices_53['%Change'] = df_indices_53['%Change'].round(6)
    
            a = (df_indices_5['%Change'].iloc[-1])/100
            a2 = (df_indices_52['%Change'].iloc[-1])/100
            a3 = (df_indices_53['%Change'].iloc[-1])/100
        
            Index_return = str(round((a*100),2))
            Index_return2 = str(round((a2*100),2))
            Index_return3 = str(round((a3*100),2))
            
            #Index_return = str(f'{(a):+.2%}')
            #Index_return2 = str(f'{(a2):+.2%}')
            #Index_return3 = str(f'{(a3):+.2%}')
        calculate_return_indices()
    
        
        #this function creates the lines and notations for the given Mint Fund and selected indices, also there is a legend added to the plot
        #which can be selected within the dashboard
        def create_figure():
            global fig
            
            fig = go.Figure()
            color1 = '#ffa500'
            color2 = '#CD5555'
            color3 = '#CDC8B1'
            #color3 = '#CDB5CD'
            
            #jaar is gelijk
            #if str(df_sql_52['ValueDate'].iloc[0])[:4] != str(df_sql_52['ValueDate'].iloc[-1])[:4]:    
             #   ['Valuedate']


            

            if float(Mint_return) > 0:               
                fig.add_trace(
                            go.Scatter(
                                x=df_sql_52['ValueDate'],
                                y=df_sql_52['NAV1'],
                                mode='lines', 
                                name= df_sql_52['Name'][0],# + ' +' + str((Mint_return)) + '%',
                                line=dict(
                                    color='#0a4be1',
                                    width=3,
                                ),
                                ),
                            )  




            if float(Mint_return) > 0:               
                fig.add_trace(
                            go.Scatter(
                                x=df_sql_52['ValueDate'],
                                y=df_sql_52['NAV1'],
                                mode='lines', 
                                name= df_sql_52['Name'][0],# + ' +' + str((Mint_return)) + '%',
                                line=dict(
                                    color='#0a4be1',
                                    width=3,
                                ),
                                ),
                            )            
            

            elif float(Mint_return) <= 0:                
                fig.add_trace(
                            go.Scatter(
                                x=df_sql_52['ValueDate'],
                                y=df_sql_52['NAV1'],
                                mode='lines', 
                                name= df_sql_52['Name'][0],# + ' ' + str((Mint_return)) + '%',
                                line=dict(
                                    color='#0a4be1',
                                    width=3,
                                ),
                                ),
                            ) 
                
            if float(Index_return) > 0 and Index_Name != "":
                fig.add_trace(
                                go.Scatter(
                                    x=df_indices_3['ValueDate'],
                                    y=df_indices_3['NAV1'],
                                    mode='lines',
    
                                    name= str(df_indices_3['Name'][1]),# + ' +' + str(Index_return) + '%',
                                    line=dict(
                                        color=(color1),
                                        width=3,
                                    ),
                                    ),
                                )

            elif float(Index_return) <= 0 and Index_Name != "":
                fig.add_trace(
                                go.Scatter(
                                    x=df_indices_3['ValueDate'],
                                    y=df_indices_3['NAV1'],
                                    mode='lines',
    
                                    name= str(df_indices_3['Name'][1]),# + ' ' + str(Index_return) + '%',
                                    line=dict(
                                        color=(color1),
                                        width=3,
                                    ),
                                    ),
                                )                
                      
            
            if float(Index_return2) > 0 and Index_Name2 != "":
                fig.add_trace(
                                    go.Scatter(
                                    x=df_indices_32['ValueDate'],
                                    y=df_indices_32['NAV1'],
                                    mode='lines',
    
                                    name=str(df_indices_32['Name'][1]),# + ' +' + str(Index_return2) + '%',
                                    line=dict(
                                        color=(color2),
                                        width=3,
                                    ),
                                    ),
                                )
                
            elif float(Index_return2) <= 0 and Index_Name2 != "":
                fig.add_trace(
                                    go.Scatter(
                                    x=df_indices_32['ValueDate'],
                                    y=df_indices_32['NAV1'],
                                    mode='lines',
    
                                    name=str(df_indices_32['Name'][1]),# + ' ' + str(Index_return2) + '%',
                                    line=dict(
                                        color=(color2),
                                        width=3,
                                    ),
                                    ),
                                )

           
            if float(Index_return3) > 0 and Index_Name3 != "":
                fig.add_trace(
                                go.Scatter(
                                    x=df_indices_33['ValueDate'],
                                    y=df_indices_33['NAV1'],
                                    mode='lines',           
                                    name= str(df_indices_33['Name'][1]),# + ' +' + str(Index_return3) + '%',
                                    line=dict(
                                        color=(color3),
                                        width=3,
                                    ),
                                    ),
                                )
                
            elif float(Index_return3) <= 0 and Index_Name3 != "":
                fig.add_trace(
                                go.Scatter(
                                    x=df_indices_33['ValueDate'],
                                    y=df_indices_33['NAV1'],
                                    mode='lines',           
                                    name= str(df_indices_33['Name'][1]),# + ' ' + str(Index_return3) + '%',
                                    line=dict(
                                        color=(color3),
                                        width=3,
                                    ),
                                    ),
                                )


            #this functoin creates a legend in case this is selected in the dashboard
            if Title == "ENG TITLE":                 
                if Legend == "WITH LEGEND" and Axis_color == "Gold color":
                    fig.update_layout(title={'text': "Net Cumulative Return",'y':0.9,'x':0.5,'xanchor': 'center', 'yanchor':'top'},showlegend=True, font_size=15, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
                elif Legend == "WITH LEGEND" and Axis_color == "White color":
                    fig.update_layout(title={'text': "Net Cumulative Return",'y':0.9,'x':0.5,'xanchor': 'center', 'yanchor':'top'},showlegend=True, font_size=15, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))
                
                elif Legend == "NO LEGEND" and Axis_color == "Gold color":
                    fig.update_layout(title={'text': "Net Cumulative Return",'y':0.9,'x':0.5,'xanchor': 'center', 'yanchor':'top'},showlegend=False, font_size=15, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
                elif Legend == "NO LEGEND" and Axis_color == "White color":
                    fig.update_layout(title={'text': "Net Cumulative Return",'y':0.9,'x':0.5,'xanchor': 'center', 'yanchor':'top'},showlegend=False, font_size=15, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))                
    
            if Title == "DUTCH TITLE":                 
                if Legend == "WITH LEGEND" and Axis_color == "Gold color":
                    fig.update_layout(title={'text': "Netto Rendementsverloop",'y':0.9,'x':0.5,'xanchor': 'center', 'yanchor':'top'},showlegend=True, font_size=15, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
                elif Legend == "WITH LEGEND" and Axis_color == "White color":
                    fig.update_layout(title={'text': "Netto Rendementsverloop",'y':0.9,'x':0.5,'xanchor': 'center', 'yanchor':'top'},showlegend=True, font_size=15, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))
                
                elif Legend == "NO LEGEND" and Axis_color == "Gold color":
                    fig.update_layout(title={'text': "Netto Rendementsverloop",'y':0.9,'x':0.5,'xanchor': 'center', 'yanchor':'top'},showlegend=False, font_size=15, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
                elif Legend == "NO LEGEND" and Axis_color == "White color":
                    fig.update_layout(title={'text': "Netto Rendementsverloop",'y':0.9,'x':0.5,'xanchor': 'center', 'yanchor':'top'},showlegend=False, font_size=15, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))  
                    
            if Title == "NO TITLE":                 
                if Legend == "WITH LEGEND" and Axis_color == "Gold color":
                    fig.update_layout(showlegend=True, font_size=15, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
                elif Legend == "WITH LEGEND" and Axis_color == "White color":
                    fig.update_layout(showlegend=True, font_size=15, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))
                
                elif Legend == "NO LEGEND" and Axis_color == "Gold color":
                    fig.update_layout(showlegend=False, font_size=15, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
                elif Legend == "NO LEGEND" and Axis_color == "White color":
                    fig.update_layout(showlegend=False, font_size=15, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
                                      xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))  
                    
                    
                    
                    
# =============================================================================
#             #this functoin creates a legend in case this is selected in the dashboard
#             if str(df_sql_52['ValueDate'].iloc[0])[:4] != str(df_sql_52['ValueDate'].iloc[-1])[:4]:
#                 if Legend == "WITH LEGEND" and Axis_color == "Gold color":
#                     fig.update_layout(title = {'text':(str(df_sql_52['ValueDate'].iloc[0])[:4] + '-' + str(df_sql_52['ValueDate'].iloc[-1])[:4]),'x':0.7, 'y':0.815, 'xanchor': 'right', 'yanchor':'middle'}, showlegend=True, font_size=14, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
#                                       xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
#                 elif Legend == "WITH LEGEND" and Axis_color == "White color":
#                     fig.update_layout(title = {'text':(str(df_sql_52['ValueDate'].iloc[0])[:4] + '-' + str(df_sql_52['ValueDate'].iloc[-1])[:4]),'x':0.7, 'y':0.815, 'xanchor': 'right', 'yanchor':'middle'}, showlegend=True, font_size=14, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
#                                       xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))
#                 
#                 elif Legend == "NO LEGEND" and Axis_color == "Gold color":
#                     fig.update_layout(title = {'text':(str(df_sql_52['ValueDate'].iloc[0])[:4] + '-' + str(df_sql_52['ValueDate'].iloc[-1])[:4]),'x':0.7, 'y':0.815, 'xanchor': 'right', 'yanchor':'middle'}, showlegend=False, font_size=14, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
#                                       xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
#                 elif Legend == "NO LEGEND" and Axis_color == "White color":
#                     fig.update_layout(title = {'text':(str(df_sql_52['ValueDate'].iloc[0])[:4] + '-' + str(df_sql_52['ValueDate'].iloc[-1])[:4]),'x':0.7, 'y':0.815, 'xanchor': 'right', 'yanchor':'middle'}, showlegend=False, font_size=14, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
#                                       xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))
#                     
#             elif str(df_sql_52['ValueDate'].iloc[0])[:4] == str(df_sql_52['ValueDate'].iloc[0])[:4]:
#                 if Legend == "WITH LEGEND" and Axis_color == "Gold color":
#                     fig.update_layout(title = {'text':str(df_sql_52['ValueDate'].iloc[0])[:4], 'x':0.7, 'y':0.815, 'xanchor': 'right', 'yanchor':'middle'}, showlegend=True, font_size=14, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
#                                       xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
#                 elif Legend == "WITH LEGEND" and Axis_color == "White color":
#                     fig.update_layout(title = {'text':str(df_sql_52['ValueDate'].iloc[0])[:4], 'x':0.7, 'y':0.815, 'xanchor': 'right', 'yanchor':'middle'}, showlegend=True, font_size=14, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
#                                       xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))
#                 
#                 elif Legend == "NO LEGEND" and Axis_color == "Gold color":
#                     fig.update_layout(title = {'text':str(df_sql_52['ValueDate'].iloc[0])[:4], 'x':0.7, 'y':0.815, 'xanchor': 'right', 'yanchor':'middle'}, showlegend=False, font_size=14, font_color = 'RGB(184, 134, 11)', paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
#                                       xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'RGB(184, 134, 11)'))
#                 elif Legend == "NO LEGEND" and Axis_color == "White color":
#                     fig.update_layout(title = {'text':str(df_sql_52['ValueDate'].iloc[0])[:4], 'x':0.7, 'y':0.815, 'xanchor': 'right', 'yanchor':'middle'}, showlegend=False, font_size=14, font_color = "white", paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', grid_xgap =0, grid_ygap=0,
#                                       xaxis =dict(showgrid = False, tickangle=-45), yaxis=dict(gridcolor = 'rgba(0, 0, 0, 0)'))
# =============================================================================
                
        create_figure()        
       
        #creating general information based on the prior code to make a fundamental basis for the statistics calculations
        def calculating_statistics():
            global returnmtaf, volatilitymtaf, volatilityindex_, volatilityindex2_, volatilityindex3_, correlation1a, correlation1b, correlation1c
            
            returnmtaf = Mint_return
            
            datefilter_alldays = df_sql_52[['ValueDate']]

            #for the mint fund, the dataframe should be a 10 day dataframe with the NAV1's calculted form 100 onwards
            df_fund1 = (df_sql_52.loc[df_sql_52['NAV'] != 0]).reset_index()
            #calculating the return of the mint fund in a specific period based on the calculation below, perform calculation from second row
            df_fund1['Return'] = 0.0000000000
            for i in df_fund1.index:
                if i > 0:
                    df_fund1['Return'][i] = ((df_fund1['NAV1'][i] - df_fund1['NAV1'][i-1]) / df_fund1['NAV1'][i-1]) * 100
                else:
                    df_fund1['Return'][i] = 0
            
            #calculating the return from the indices selected in the dashboard. The dataframe has to match the dataframe of the mint fund
            #but because the weekends are off, the data is moved downwards, so saterday price is actual friday price, sunday price is actual friday price etc.
            df_indices_5['Return'] = 0.0000000000
            df_indices_52['Return'] = 0.0000000000
            df_indices_53['Return'] = 0.0000000000

            df_index1 = pd.merge(datefilter_alldays,df_indices_5, how='outer', on='ValueDate')          
            df_index2 = pd.merge(datefilter_alldays,df_indices_52, how='outer', on='ValueDate')
            df_index3 = pd.merge(datefilter_alldays,df_indices_53, how='outer', on='ValueDate')
            
            df_index1 = df_index1.fillna(0)
            df_index1 = df_index1.replace(to_replace=0, method='ffill')

            df_index2 = df_index2.fillna(0)
            df_index2 = df_index2.replace(to_replace=0, method='ffill')

            df_index3 = df_index3.fillna(0)
            df_index3 = df_index3.replace(to_replace=0, method='ffill')
            
            datefilter_10day = df_fund1[['ValueDate']]
            index1_new = pd.merge(datefilter_10day,df_index1, how='inner', on='ValueDate')
            
            #calculating the return of the indices based on the NAV1 value which is set on 100 for the given period
            for i in index1_new.index:
                if i > 0:
                    index1_new['Return'][i] = ((index1_new['NAV1'][i] - index1_new['NAV1'][i-1]) /index1_new['NAV1'][i-1] * 100)
                else:
                    index1_new['Return'][i] = 0
            
            index1_new['Return'] = index1_new['Return'].replace(to_replace=0, method='ffill')
            
            index2_new = pd.merge(datefilter_10day,df_index2, how='inner', on='ValueDate')
            
            for i in index2_new.index:
                if i > 0:
                    index2_new['Return'][i] = ((index2_new['NAV1'][i] - index2_new['NAV1'][i-1]) /index2_new['NAV1'][i-1] * 100)
                else:
                    index2_new['Return'][i] = 0
            
            
            
            index3_new = pd.merge(datefilter_10day,df_index3, how='inner', on='ValueDate')
            
            for i in index3_new.index:
                if i > 0:
                    index3_new['Return'][i] = ((index3_new['NAV1'][i] - index3_new['NAV1'][i-1]) /index3_new['NAV1'][i-1] * 100)
                else:
                    index3_new['Return'][i] = 0
            
            index3_new['Return'] = index3_new['Return'].replace(to_replace=0, method='ffill')

            #creating the column to do the calculation for the volatility and for the correlation, since we have 10 day data, we use 36 period
            #to annualize the volatility of the period
            column_1 = df_fund1["Return"]
            column_21 = index1_new["Return"]
            column_22 = index2_new["Return"]
            column_23 = index3_new["Return"]

            correlation1a = column_1.corr(column_21)
            correlation1b = column_1.corr(column_22)
            correlation1c = column_1.corr(column_23)

            
            std1 = np.std(column_1)* math.sqrt(36)
            std2 = np.std(column_21)* math.sqrt(36)
            std22 = np.std(column_22)* math.sqrt(36)
            std23 = np.std(column_23)* math.sqrt(36)
    
            volatilitymtaf_ = std1
            volatilityindex_ = std2
            volatilityindex2_ = std22
            volatilityindex3_ = std23
            volatilitymtaf = str(round(volatilitymtaf_,2))
            

        calculating_statistics()
        
        #this function fills in the calculations in the table for the relevant indices and runs the graph
        #the statistics are: return, volatiltiy and correlation
        def add_statistics_table():
            global returnindex, volatilityindex, correlation1, returnindex2, volatilityindex2, correlation2, returnindex3, volatilityindex3, correlation3
            
            
            if Index_Name != "":
                returnindex = Index_return
                volatilityindex = str(round(volatilityindex_,2))
                correlation1 = str(round(correlation1a,2))
    
            else: 
                returnindex = "-"
                volatilityindex = "-"
                correlation1 = '-'
                   
            if Index_Name2 != "":
                returnindex2 = Index_return2          
                volatilityindex2 = str(round(volatilityindex2_,2))
                correlation2 = str(round(correlation1b,2))
    
            else:
                returnindex2 = "-"       
                volatilityindex2 = "-"
                correlation2 = "-"
                    
            if Index_Name3 != "":
                returnindex3 = Index_return3
                volatilityindex3 = str(round(volatilityindex3_,2))           
                correlation3 = str(round(correlation1c,2))
    
            else:
                returnindex3 = "-"
                volatilityindex3 = "-"
                correlation3 = "-"

        add_statistics_table()
        
        
        return fig, returnmtaf, returnindex, returnindex2, returnindex3, volatilitymtaf, volatilityindex, volatilityindex2, volatilityindex3, correlation1, correlation2, correlation3



port = 8085 # or simply open on the default `8050` port

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(port))

if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(host="0.0.0.0", port=port, debug=False)
