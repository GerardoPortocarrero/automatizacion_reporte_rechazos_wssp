# ANALISIS PARA CARGA DIARIA

import pandas as pd
import graphics as myg
import importlib

# Parsear la fecha
def parse_date(file, df):    
    df[file['date']] = pd.to_datetime(df[file['date']], format='%d/%m/%Y')
    return df

# REPORTES
def report_configuration(project_address, df, report, date):
    # CONFIGURACION GENERAL
    bar_width = 10
    bar_height = 7
    bar_label = 16
    bar_fontsize = 19
    bar_color_1 = "#D32F2F"
    bar_color_2 = "#F57C00"
    bar_color_3 = "#B71C1C"
    bar_color_4 = "#FFC107"
    bar_color_5 = "#424242"

    # CONFIGURACION DE GRAFICO
    group_by = report
    indicator = 'Carga Pvta CF'
    title = group_by.upper()
    myg.bar_graphic_v_3(
        project_address,
        df,
        date,
        group_by,
        indicator,
        bar_width,
        bar_height,
        bar_label,
        bar_fontsize,
        bar_color_1
    )

# Funcion principal
def main(project_address, df, document, date):
    importlib.reload(myg)
    
    # Calling graphic generators
    for report in document['reports']:
        report_configuration(project_address, df, report, date)