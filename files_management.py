import os
import pandas as pd

# Eliminar "comas" por "espacio en blanco" y "punto y coma" por "coma"
def delete_unnecessary_symbols(file_name, output_file_name, project_address):
    # Abrir, leer y modificar el contenido del archivo
    with open(os.path.join(project_address, file_name), "r", encoding="utf-8") as f:
        contenido = f.read()

    # Reemplazos: primero las comas por espacio, luego los puntos y coma por coma
    contenido = contenido.replace(",", " ")
    contenido = contenido.replace(";", ",")

    # Guardar el contenido modificado en un nuevo archivo
    with open(os.path.join(project_address, output_file_name), "w", encoding="utf-8") as f:
        f.write(contenido)

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
def file_processing(file, output_file_name, locaciones, project_address):
    delete_unnecessary_symbols(file['file_name'], output_file_name, project_address)

    df = pd.read_csv(os.path.join(project_address, output_file_name))
    print(df.info())

    df = get_relevant_columns(df, file)
    print(df.info())

    df = get_relevant_locations(df, locaciones)
    print(df.info())

    df = adjust_values(df)
    print(df.info())

    return df

# Filtrar por tiempo
def get_specific_date(df, file, time_option):
    if time_option == 1:
        date = input("año: ")
        started_date = pd.to_datetime('01/01/'+str(date), format='%d/%m/%Y')
        ended_date = pd.to_datetime('31/12/'+str(date), format='%d/%m/%Y')
        df = df[(df[file['date']] >= started_date) & (df[file['date']] <= ended_date)]
    elif time_option == 2:
        date = input("mes/año: ")
        month, year = date.split('/')
        started_date = pd.to_datetime('01/'+str(month)+'/'+str(year), format='%d/%m/%Y')
        ended_date = pd.to_datetime('01/'+str(int(month)+1)+'/'+str(year), format='%d/%m/%Y')
        df = df[(df[file['date']] >= started_date) & (df[file['date']] < ended_date)]
    elif time_option == 3:
        date = input("dia/mes/año: ")
        fecha_corte = pd.to_datetime(str(date), format='%d/%m/%Y')
        df = df[df[file['date']] == fecha_corte]
    elif time_option == 4:
        date = input("dia/mes/año dia/mes/año: ")
        started_date, ended_date = date.split(' ')
        started_date = pd.to_datetime(str(started_date), format='%d/%m/%Y')
        ended_date = pd.to_datetime(str(ended_date), format='%d/%m/%Y')
        df = df[(df[file['date']] >= started_date) & (df['Día'] <= ended_date)]
    elif time_option == 5:
        date = input("dia/mes/año: ")
        fecha_corte = pd.to_datetime(str(date), format='%d/%m/%Y')
        df = df[df[file['date']] >= fecha_corte]

    return df, date

# Filtrar por locacion
def get_specific_location(df, location_option, locaciones):
    if location_option == 1:
        return df
    elif (location_option == 2) | (location_option == 3) | (location_option == 4) | (location_option == 5):
        return df[df['Locación'].isin([locaciones[location_option-2]])]