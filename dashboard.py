import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import datetime
from dash.dependencies import Input,Output

from main import run
from OrganizeData import organizer


################################################## Constants
colors = {
    'background': '#FFFFFF',#2A2A2A
    'text': '#1866B9', #7FDBFF
    'h4':'#000000'#FFFFFF
}
today = str(datetime.datetime.now())[:10]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

################################################## App dash build
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

################################################## Main CALL
df, df_month, cuenta, fechas_month = run()
################################################## Functions
def generate_monthtable( max_rows, dataframe):
    return [ html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),

        html.Tbody([html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ], style = {'color':'#414242' })
    ]

################################################## OrganizeData CALL
saldo_actual, saldo_previo,df_month, df, df_payments, df_deposits,fig_deposits,fig_month,fig_payments = organizer(df,df_month,fechas_month,colors)

################################################## App layout ##################################################

app.layout = html.Div(
                style = {
                        'backgroundColor': colors['background'], 
                        'margin': 0
                        }, 

                children=[
                    ############################# Title
                    html.H2(children = ' Dashboard de la {} hasta {}'.format(cuenta.lower().replace(':',''),today) ,
                            style = {
                                'textAlign': 'center',
                                'color': colors['text'],
                                'margin': 0,
                                'margin-bottom':20
                            }
                        ),
                    ############################# Subtitle
                    html.H3(children=' Saldo: ${}'.format(saldo_actual),
                            style={
                                'textAlign': 'center',
                                'color': colors['h4'],
                                'margin': 0,
                                'margin-bottom':20
                            }
                        ),
                    ############################# df table 
                    html.H4(children='''
                    Tabla de movimientos
                    ''', style={
                           # 'textAlign': 'center',
                            'color': colors['h4'],
                            'margin-left': 30
                            }
                        ),
                    html.Div(children='''
                    Opciones de visualización
                    ''', style={
                            'color': colors['h4'],
                            'margin-left': 40
                            }
                        ),
                    html.Div(
                        dcc.Dropdown(id = 'table_size',options = [{'label':'Ver todos los movimientos', 'value':2**100},{'label':'Ver últimos 10 movimientos', 'value':10},{'label':'Ver últimos 5 movimientos', 'value': 5}], value = 5),
                        style = {
                            'margin': 40,
                            'margin-top':10
                            }
                         ),

                    html.Table(id = 'First_table',style={'textAlign': 'center',
                                                        #'color': colors['h4'],
                                                        'margin': 80,
                                                        'margin-top': 10,
                                                        'margin-left': 'auto',
                                                        'margin-right': 'auto'
                                                                        }
                                ),
                    ############################# df month table
                    html.H4(children='''
                    Resumen por mes
                    ''', style={
                            #'textAlign': 'center',
                            'color': colors['h4'],
                             'margin-left': 30
                                }
                        ),
                    html.Table(children = generate_monthtable(100, dataframe= df_month),style={
                                                                        'textAlign': 'center',
                                                                        #'color': colors['h4'],
                                                                        'margin': 80,
                                                                        'margin-top': 10,
                                                                        'margin-left': 'auto',
                                                                        'margin-right': 'auto'
                                                                        }),
                    dcc.Graph(
                        id='df_month',
                        figure= fig_month
                    ),
                    ############################# df payments
                    html.H4(children='''
                    Gráfico de cargos
                    ''', style={
                            #'textAlign': 'center',
                            'color': colors['h4'],
                             'margin-left': 30
                            }
                        ), 

                    dcc.Graph(
                        id='df_Payments',
                        figure=fig_payments
                    ),
                    ############################# df deposits
                    html.H4(children='''
                    Gráfico de abonos:
                    ''', style={
                            #'textAlign': 'center',
                            'color': colors['h4'],
                            'margin-left': 30
                            }
                        ),

                    dcc.Graph(
                        id='df_deposits',
                        figure=fig_deposits
                    ),
                    ############################# Footer
                    html.Footer(children= [
                                         html.Div(children = ['Made by Joules CH -  ',
                                                                html.A('GitHub',href = 'https://github.com/JoulesCH') 
                                                        ], 
                                                style = {
                                                    'textAlign': 'center',
                                                    'margin': 10,
                                                    'margin-left': 'auto',
                                                    'margin-right': 'auto'
                                                 }
                                         )
                                    ],
                                style={
                                        'width': 777,
                                        'border-top-style': 'double',
                                        'border-top-color': colors['text'],
                                        'margin-left': 'auto',
                                        'margin-right': 'auto',
                                        'margin-top': 15
                                        
                                }
                    ) 
])
################################################## App Callbacks
@app.callback(Output('First_table','children'),[Input('table_size', 'value')] )
def generate_table( max_rows, dataframe = df):
    return [ html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),

        html.Tbody([html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ], style = {'color':'#414242' })

    ]

################################################## Entry
if __name__ == '__main__':
    app.run_server(debug=True)