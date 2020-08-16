import pandas as pd
import datetime
import plotly.express as px

def organizer(df,df_month,fechas_month,colors):
    ################################################## Ajuste de saldo
    saldo_actual = df.iloc[0,3]
    saldo_previo = df.iloc[-1,[1,3]]
    saldo_previo = saldo_previo['Cargo'] + saldo_previo['Saldo']
    saldo_previo = float('{:.2f}'.format(saldo_previo))
    
    ################################################## df_month
    df_month['Mes'] = [df_month.index[x] +' '+ str(fechas_month.year[x]) for x in range(len(fechas_month))] 
    df_month['Cargos'] = df_month['Cargo'] *-1
    df_month['Abonos'] = df_month['Abono']
    diferencias = df_month['Abonos'] - df_month['Cargos']
    diferencias = diferencias.apply(lambda x : float("{:.2f}".format(x)) )
    df_month['Balance mensual'] = diferencias
    df_month.drop(columns=['Cargo','Abono'] , inplace = True) 
    saldos = [saldo_previo]
    for x in range(len(df_month['Cargos'])):
        saldom = saldos[x] + df_month.iloc[x,3]
        saldos.append(float('{:.2f}'.format(saldom)))
        #print( df_month.iloc[x,3])
    df_month['Saldo'] = saldos[1:]
    df_month['Fecha'] = fechas_month
    df_month.set_index('Fecha', inplace = True)
    fig_month = px.bar(df_month, x="Mes",y="Saldo", barmode="group", title = 'Resumen mensual',
                        color= 'Mes')

    fig_month.update_layout(
        #plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
   
    ################################################## df
    df ['Fecha'] = [str(x)[:10] for x in df.index]

    ################################################## df_payments
    df_payments = df[df['Cargo']>0]
    df_payments['Fecha'] = df[df['Cargo']>0].index
    #print(df_payments[df_payments['Fecha'] > df_month.index[1]])
    #print(df_month.index)
    # fig_payments = px.bar(df_payments,x = 'Fecha', y="Cargo", color="Descripcion", barmode="relative", title = 'Cargos')
    # fig_payments.update_layout(
    #     #plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
    ################################################## df_deposits
    df_deposits = df[df['Abono']>0]
    df_deposits['Fecha'] = df[df['Abono']>0].index
    fig_deposits = px.bar(df_deposits,x = 'Fecha',  y="Abono", color="Descripcion", barmode="group", title = 'Abonos')
    fig_deposits.update_layout(
        #plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return saldo_actual, saldo_previo,df_month, df, df_payments, df_deposits, fig_deposits,fig_month#,fig_payments
