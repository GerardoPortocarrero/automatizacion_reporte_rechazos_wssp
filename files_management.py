import os
import pandas as pd

# Eliminar todas las columnas excepto las relevantes
def get_relevant_columns(df, file):
    return df[file['relevant_columns']]

# Conservar las filas que contenga las siguientes Locaciones
def get_relevant_locations(df, locaciones):
    return df[df['Locación'].isin(locaciones)]

# Ajustar valores
def adjust_values(df):
    df = df.fillna(0)

    try:
        return df[df['Venta Perdida CF'] != 0]
    except:
        return df
    
# Preparar archivo para analizar
def file_processing(file, locaciones, root_address):
    df = pd.read_csv(os.path.join(root_address, file['file_name']), sep=';')
    #print(df.info())

    df = get_relevant_columns(df, file)
    #print(df.info())

    df = get_relevant_locations(df, locaciones)
    #print(df.info())

    df = adjust_values(df)
    #print(df.info())

    return df

# Filtrar por tiempo
def get_specific_date(df, file, time_option):
    if time_option == 1:
        date = input("\n>> Año (yyyy): ")
        started_date = pd.to_datetime(str(date)+'-01-01', format='%Y-%m-%d')
        ended_date = pd.to_datetime(str(date)+'-12/31/', format='%Y-%m-%d')
        df = df[(df[file['date']] >= started_date) & (df[file['date']] <= ended_date)]
    elif time_option == 2:
        date = input("\n>> Mes/Año (m/yyyy): ")
        month, year = date.split('/')
        started_date = pd.to_datetime(str(year)+'-'+str(month)+'-01', format='%Y-%m-%d')
        ended_date = pd.to_datetime(str(year)+'-'+str(int(month)+1)+'-01', format='%Y-%m-%d')
        df = df[(df[file['date']] >= started_date) & (df[file['date']] < ended_date)]
    elif time_option == 3:
        date = input("\n>> Año-Mes-Dia (yyyy-m-d): ")
        fecha_corte = pd.to_datetime(str(date), format='%Y-%m-%d')
        df = df[df[file['date']] == fecha_corte]
    elif time_option == 4:
        date = input("\n>> (yyyy-m-d yyyy-m-d): ")
        started_date, ended_date = date.split(' ')
        started_date = pd.to_datetime(str(started_date), format='%Y-%m-%d')
        ended_date = pd.to_datetime(str(ended_date), format='%Y-%m-%d')
        df = df[(df[file['date']] >= started_date) & (df['Día'] <= ended_date)]
    elif time_option == 5:
        date = input("\n>> Año-Mes-Dia (yyyy-m-d): ")
        fecha_corte = pd.to_datetime(str(date), format='%Y-%m-%d')
        df = df[df[file['date']] >= fecha_corte]

    return df, date

# Filtrar por locacion
def get_specific_location(df, location_option, locaciones):
    if location_option == 1:
        return df
    elif (location_option == 2) | (location_option == 3) | (location_option == 4) | (location_option == 5):
        return df[df['Locación'].isin([locaciones[location_option-2]])]