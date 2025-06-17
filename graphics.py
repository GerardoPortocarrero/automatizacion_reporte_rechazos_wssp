import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as mticker

# Reporte de barras (sumatoria)
def bar_graphic_v_1(
        project_address,
        df,
        date,
        group_by,
        indicator,
        bar_width,
        bar_height,
        bar_fontsize,
        bar_color
    ):
    try:
        # Agrupar y ordenar
        group_by_indicator = df.groupby(group_by)[indicator].sum().sort_values(ascending=False)

        # Crear figura y eje
        fig, ax = plt.subplots(figsize=(bar_width, bar_height))

        # Dibujar barras
        bars = ax.bar(
            group_by_indicator.index,
            group_by_indicator.values,
            color=bar_color,
            edgecolor='black',
            linewidth=0.5,
        )

        # Etiquetas encima de cada barra
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f'{height:,.1f} CF',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),  # Desplazamiento hacia arriba
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=bar_fontsize,
                color='black'
            )

        # Texto adicional arriba a la derecha
        group_by_indicator_total = group_by_indicator.sum()
        ax.text(
            0.99, 0.98,
            f'Fecha: {date}\n\nTotal: {group_by_indicator_total:,.1f} CF',
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=bar_fontsize,
            color='black',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Estética del gráfico
        ax.set_xlabel("")
        ax.set_ylabel("")  # opcional: puedes poner "CF" si es necesario
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', linestyle='--', alpha=0.4)

        # Ajustar margenes
        ax.margins(y=0.1)

        # Etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=bar_fontsize)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

        plt.tight_layout(pad=2)
        filename = f'barh_{group_by}_{indicator}.png'
        plt.savefig(os.path.join(project_address, filename), dpi=300)
        plt.show()
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos)')

# Reporte de barras horizontal
def bar_graphic_v_2(
        project_address,
        df,
        date,
        group_by,
        indicator,
        bar_width,
        bar_height,
        bar_fontsize,
        bar_color
    ):
    try:
        group_by_indicator = df.groupby(group_by)[indicator].sum().sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(bar_width, bar_height))

        # Dibujar barras
        bars = ax.barh(
            group_by_indicator.index,
            group_by_indicator.values,
            color=bar_color,
            edgecolor='black',
            linewidth=0.6
        )

        # Texto en barras
        for bar in bars:
            width = bar.get_width()
            ax.annotate(
                f'{width:,.1f} CF',
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0),
                textcoords='offset points',
                ha='left', va='center',
                fontsize=bar_fontsize
            )

        # Texto resumen
        total = group_by_indicator.sum()
        ax.text(
            1, 0.15,
            f'Fecha: {date}\n\nTotal: {total:,.1f} CF',
            transform=ax.transAxes,
            ha='right', va='top',
            fontsize=bar_fontsize,
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')
        )

        # Estética
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
        plt.yticks(fontsize=bar_fontsize)
        plt.xticks(fontsize=bar_fontsize)
        plt.tight_layout(pad=2)

        # Guardar
        filename = f'barh_{group_by}_{indicator}.png'
        plt.savefig(os.path.join(project_address, filename), dpi=300)
        #plt.show()

    except Exception as e:
        print(f'Cantidad de datos: {len(df)}')
        print('❌ Error en la generación del gráfico:', e)

# Reporte de barras horizontal
def bar_graphic_v_3(
        project_address,
        df,
        date,
        group_by,
        indicator,
        bar_width,
        bar_height,
        bar_label,
        bar_fontsize,
        bar_color
    ):
    try:
        group_by_indicator = df.groupby(group_by)[indicator].sum().sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(bar_width, bar_height))

        # Elegante color Coca-Cola rojo + borde gris tenue
        bars = ax.barh(
            group_by_indicator.index,
            group_by_indicator.values,
            color=bar_color,  # puede ser "#D52B1E" u otro rojo Coca-Cola
            edgecolor='#333333',
            linewidth=0.5
        )

        # Etiquetas dentro o al lado
        for bar in bars:
            width = bar.get_width()
            ax.annotate(
                f'{width:,.1f} CF',
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0),
                textcoords='offset points',
                ha='left', va='center',
                fontsize=bar_fontsize,
                color='black'
            )

        # Cuadro resumen discreto
        total = group_by_indicator.sum()
        ax.text(
            0.80, 0.20,
            f"{date}\n\nTotal: {total:,.1f} CF",
            transform=ax.transAxes,
            fontsize=bar_label,
            va='top', ha='left',
            bbox=dict(facecolor='#f9f9f9', edgecolor='gray', boxstyle='round,pad=0.4', alpha=0.95)
        )

        # Estética general
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        ax.tick_params(axis='x', labelsize=bar_label)
        ax.tick_params(axis='y', labelsize=bar_label)

        ax.grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.set_xlabel("")  # sin título innecesario
        ax.set_ylabel("")

        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

        # Margen ajustado para WhatsApp (sin cortar texto)
        plt.tight_layout(rect=[0, 0, 0.95, 0.93], pad=2)

        # Guardar con alta calidad
        filename = f'barh_{group_by}_{indicator}.png'
        plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches='tight')
        # plt.show()

    except Exception as e:
        print(f'Cantidad de datos: {len(df)}')
        print('❌ Error en la generación del gráfico:', e)