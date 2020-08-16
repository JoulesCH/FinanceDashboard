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
saldo_actual, saldo_previo,df_month, df, df_payments, df_deposits,fig_deposits,fig_month = organizer(df,df_month,fechas_month,colors) #,fig_payments
################################################## App dash build
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
                    ################# Menu
                    # html.Div(children='Opciones de visualización', 
                    #         style={
                    #                 'color': colors['h4'],
                    #                 'margin-left': 40
                    #                 }
                    #         ),
                    html.Div(
                        dcc.Dropdown(id = 'table_size',options = [ {'label':'Ver todos', 
                                                                    'value':2**100},
                                                                    {'label':'Ver últimos 10', 
                                                                    'value':10},
                                                                    {'label':'Ver últimos 5 ',
                                                                     'value': 5}], 
                                                        value = 5, 
                                                        searchable = False,
                                                        clearable = False
                                    ),
                    
                        style = {
                            'margin': 40,
                            'margin-top':10,
                            'width': 150
                            }
                         ),
                    ################# Table
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
                    ################# Menu
                    html.Div(
                        dcc.Dropdown(id = 'graphic_p_range',options = [ {'label':'Ver todos', 
                                                                    'value':2**100},
                                                                    {'label':'Ver últimos 3 meses',
                                                                     'value': 3},
                                                                     {'label':'Ver último mes', 
                                                                    'value':1}], 
                                                        value = 3, 
                                                        searchable = False,
                                                        clearable = False
                                    ),
                    
                        style = {
                            'margin': 40,
                            'margin-top':10,
                            'margin-bottom':0,
                            'width': 150
                            }
                         ),

                    dcc.Graph(
                        id='df_Payments'
                        #figure=fig_payments
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
                    ################# Menu
                    html.Div(
                        dcc.Dropdown(id = 'graphic_d_range',options = [ {'label':'Ver todos', 
                                                                    'value':2**100},
                                                                    {'label':'Ver últimos 3',
                                                                     'value': 3},
                                                                     {'label':'Ver mes actual', 
                                                                    'value':1}], 
                                                        value = 5, 
                                                        searchable = False,
                                                        clearable = False
                                    ),
                    
                        style = {
                            'margin': 40,
                            'margin-top':10,
                            'margin-bottom':0,
                            'width': 150
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
@app.callback(Output('df_Payments','figure'),[Input('graphic_p_range', 'value')] )
def generate_payments_graph( max_months ):
    df_payments = df[df['Cargo']>0]
    df_payments['Fecha'] = df[df['Cargo']>0].index

    max_months = df_month.shape[0] - min(df_month.shape[0] , max_months) 

    if max_months !=0 and max_months != (df_month.shape[0] - 1): # Si no es igual a eso entonces no hace filtro porque es todo el dataframe
        df_payments = df_payments[df_payments['Fecha'] > df_month.index[max_months ]]
    
    elif max_months == (df_month.shape[0] - 1): # Para el mes actual
         df_payments = df_payments[df_payments['Fecha'] > df_month.index[max_months - 1]]
    
    fig_payments = px.bar(df_payments, x = 'Fecha', y="Cargo", color="Descripcion", barmode="relative", title = 'Cargos')
    return fig_payments.update_layout(
        #plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

################################################## Entry
if __name__ == '__main__':
    app.run_server(debug=True)