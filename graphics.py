import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as mticker

# Reporte de barras (sumatoria)
def bar_graphic_v_1(
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
        plt.savefig(f'bar_{group_by}_{indicator}.png')
        plt.show()
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos)')

def bar_graphic_v_2(
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
        plt.savefig(filename, dpi=300)
        plt.show()

    except Exception as e:
        print(f'Cantidad de datos: {len(df)}')
        print('❌ Error en la generación del gráfico:', e)

# Reporte circular (porcentual)
def circle_graphic(
        df,
        date,
        group_by,
        indicator,
        circle_width,
        circle_height,
        circle_fontsize,
        circle_legend_fontsize,
        circle_legend_nro_columns
    ):
    try:
        # Agrupar y ordenar por venta perdida
        group_by_indicator = df.groupby(group_by)[indicator].sum().sort_values(ascending=False)

        # (Opcional) Limitar a los 10 principales si el analisis es anual
        # group_by_indicator = group_by_indicator.head(10)

        # Crear gráfico circular
        fig, ax = plt.subplots(figsize=(circle_width, circle_height))

        # Colores suaves y explosion del sector más grande
        colors = cm.get_cmap('tab20')(np.linspace(0, 1, len(group_by_indicator)))
        explode = [0.05 if i == 0 else 0 for i in range(len(group_by_indicator))]
        
        # Crear pie chart sin etiquetas directamente en el gráfico
        wedges, texts, autotexts = ax.pie(
            group_by_indicator,
            labels=None,              # Sin etiquetas en el gráfico
            autopct=lambda p: f'{p:.1f}%' if p > 2 else '',
            startangle=145,
            counterclock=False,
            textprops={'fontsize': circle_fontsize}, # Tamaño de texto
            explode=explode,
            colors=colors
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # Agregar leyenda con los nombres de los motivos de anulación
        ax.legend(
            wedges,
            group_by_indicator.index,
            loc='center left',
            bbox_to_anchor=(0.95, 0.5),  # a la derecha del gráfico, centrado verticalmente
            fontsize=circle_legend_fontsize,
            ncol=circle_legend_nro_columns,
            frameon=False  # sin borde
        )

        # Ajuste manual del layout sin usar tight_layout
        plt.subplots_adjust(left=0.05, right=0.75, top=0.95, bottom=0.1)
        
        #plt.tight_layout()
        plt.savefig(f'circle_{group_by}_{indicator}.png', bbox_inches='tight')
        plt.show()
    except:
        print(f'Cantidad de datos: {len(df)}')
        print('No hay datos (Probablemente un domingo o festivo o no hubo rechazos)')
