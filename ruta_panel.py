# ANALISIS PARA VENTAS PERDIDAS

import pandas as pd
import graphics as myg
import importlib

# ==========================
# PARSEAR LA FECHA
# ==========================
def parse_date(document, df):
    df[document['date']] = pd.to_datetime(
        df[document['date']], format='%Y-%m-%d', errors='coerce'
    )
    return df

# ==========================
# REPORTES ESPECIALIZADOS
# ==========================

# --- MOTIVO DE ANULACIÓN ---
# Muchos motivos → Pareto
def report_motivo(project_address, df, date, group_by):
    indicator = "Venta Perdida CF"
    data = (
        df.groupby(group_by)[indicator]
        .sum()
        .sort_values(ascending=False)
    )

    # Top 10 + "Otros"
    top_n = 10
    top_data = data.head(top_n)
    otros = pd.Series({"Otros": data.iloc[top_n:].sum()})
    final_data = pd.concat([top_data, otros])

    myg.pareto_graphic(
        project_address,
        final_data,
        date,
        group_by,
        indicator,
        width=10,
        height=7,
        label_size=16,
        fontsize=18,
    )

# --- TRANSPORTISTA ---
# Número limitado (≤10) → Donut
def report_transportista(project_address, df, date, group_by):
    indicator = "Venta Perdida CF"
    data = (
        df.groupby(group_by)[indicator]
        .sum()
        .sort_values(ascending=False)
    )

    myg.donut_graphic(
        project_address,
        data,
        date,
        group_by,
        indicator,
        width=7,
        height=7,
        fontsize=16,
        colors=["#F57C00", "#FF9800", "#FFB74D", "#FFE0B2"]  # Gama cálida
    )

# --- RUTA TRONCAL DINÁMICO ---
# Entre 10–15 categorías → Lollipop
def report_ruta(project_address, df, date, group_by):
    indicator = "Venta Perdida CF"
    data = (
        df.groupby(group_by)[indicator]
        .sum()
        .sort_values(ascending=False)
    )

    myg.lollipop_graphic(
        project_address,
        data,
        date,
        group_by,
        indicator,
        width=12,
        height=7,
        fontsize=16,
        color="#B71C1C"  # Rojo oscuro fuerte
    )

# --- CLIENTE ---
# Demasiados clientes → Top N + "Otros" en barras horizontales
def report_cliente(project_address, df, date, group_by, top_n=10):
    # CONFIGURACIÓN
    bar_width = 12
    bar_height = 7
    bar_label = 14
    bar_fontsize = 14
    bar_color = "#1976D2"  # azul para clientes

    indicator = "Venta Perdida CF"

    # --- calcular top N clientes con mayor rechazo ---
    top_clientes = (
        df.groupby(group_by)[indicator]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )

    # --- filtrar df solo con esos clientes ---
    df_top = df[df[group_by].isin(top_clientes)]

    # --- llamada a la función de gráfico ---
    myg.horizontal_bar_graphic(
        project_address,
        df_top,
        date,
        group_by,
        indicator,
        bar_width,
        bar_height,
        bar_label,
        bar_fontsize,
        bar_color
    )

# ==========================
# FUNCIÓN PRINCIPAL
# ==========================
def main(project_address, df, document, date):
    importlib.reload(myg)

    # if "Motivo de anulación" in document["group_by"]:
    #     report_motivo(project_address, df, date, "Motivo de anulación")

    if "Código Transportista" in document["group_by"]:
        report_transportista(project_address, df, date, "Código Transportista")

    # if "Ruta Troncal Dinámico" in document["group_by"]:
    #     report_ruta(project_address, df, date, "Ruta Troncal Dinámico")

    # if "Cliente" in document["group_by"]:
    #     report_cliente(project_address, df, date, "Cliente")