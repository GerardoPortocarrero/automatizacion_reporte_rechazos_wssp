# ANALISIS PARA VENTAS PERDIDAS

import pandas as pd
import graphics as myg
import importlib

# Parsear la fecha
def parse_date(file, df):
    df[file['date']] = pd.to_datetime(df[file['date']], errors='coerce', dayfirst=True)
    return df

# REPORTES
def report_configuration(df, report, date):
    # CONFIGURACION GENERAL
    bar_width = 10
    bar_height = 7
    bar_fontsize = 12
    circle_fontsize = 14
    circle_legend_fontsize = 10
    circle_legend_nro_columns = 1
    bar_color_1 = "#c31432"
    bar_color_2 = "#240b36"
    circle_width = 7
    circle_height = 7

    # CONFIGURACION DE GRAFICO
    group_by = report
    indicator = 'Venta Perdida CF'
    title = group_by.upper()
    myg.bar_graphic(
        df,
        date,
        group_by,
        indicator,
        bar_width,
        bar_height,
        bar_fontsize,
        bar_color_1
    )
    # myg.circle_graphic(
    #     df,
    #     date,
    #     group_by,
    #     indicator,
    #     circle_width,
    #     circle_height,
    #     circle_fontsize,
    #     circle_legend_fontsize,
    #     circle_legend_nro_columns
    # )

# Funcion principal
def main(df, document, date):
    importlib.reload(myg)
    
    # Calling graphic generators
    for report in document['reports']:
        report_configuration(df, report, date)