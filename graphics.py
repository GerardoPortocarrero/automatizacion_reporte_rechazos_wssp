import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# Reporte de barras horizontal
def horizontal_bar_graphic(
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
        #plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches='tight')
        plt.show()

    except Exception as e:
        print(f'Cantidad de datos: {len(df)}')
        print('❌ Error en la generación del gráfico:', e)

# Utilidad: asegurar Serie agregada (acepta DataFrame o Serie)
def _ensure_series(data, group_by, indicator, ascending=False):
    """
    Si 'data' es Serie, la devuelve ordenada.
    Si es DataFrame, agrupa por 'group_by' y suma 'indicator'.
    """
    if isinstance(data, pd.Series):
        s = data.astype(float).sort_values(ascending=ascending)
    elif isinstance(data, pd.DataFrame):
        s = (
            data.groupby(group_by)[indicator]
            .sum()
            .sort_values(ascending=ascending)
            .astype(float)
        )
    else:
        raise ValueError("data debe ser un pd.Series o pd.DataFrame.")
    return s

# ==============================
# GRÁFICO PARETO (barras + %)
# ==============================
def pareto_graphic(
        project_address,
        data,          # Serie agregada (ideal) o DataFrame
        date,
        group_by,      # string para títulos/archivo
        indicator,     # "Venta Perdida CF"
        width=10,
        height=7,
        label_size=16,  # tamaño de ticks
        fontsize=18,    # tamaño etiquetas de valor
        bar_color="#D32F2F",
        line_color="#FFC107"
    ):
    try:
        # Serie descendente (Pareto)
        s = _ensure_series(data, group_by, indicator, ascending=False)
        if s.empty:
            raise ValueError("Serie de datos vacía para pareto_graphic().")

        total = float(s.sum())
        cumperc = 100 * s.cumsum() / total
        x = range(len(s))

        fig, ax = plt.subplots(figsize=(width, height))

        # Barras verticales con borde sutil
        bars = ax.bar(x, s.values, color=bar_color, edgecolor="#333333", linewidth=0.5)

        # Etiquetas de valor sobre barras
        for bar in bars:
            h = bar.get_height()
            ax.annotate(
                f"{h:,.1f} CF",
                xy=(bar.get_x() + bar.get_width()/2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=fontsize, color="black"
            )

        # Línea acumulada (%)
        ax2 = ax.twinx()
        ax2.plot(list(x), cumperc.values, color=line_color, marker="o", linewidth=2)
        ax2.set_ylim(0, 110)
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))

        # Estética general
        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)
        ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.3)

        ax.tick_params(axis='x', labelsize=label_size)
        ax.tick_params(axis='y', labelsize=label_size)
        ax2.tick_params(axis='y', labelsize=label_size)

        # Nombres de categorías en X
        ax.set_xticks(list(x))
        ax.set_xticklabels([str(k) for k in s.index], rotation=35, ha='right')

        # Formato eje Y (CF)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))

        # Cuadro resumen
        ax.text(
            0.80, 0.20,
            f"{date}\n\nTotal: {total:,.1f} CF",
            transform=ax.transAxes,
            fontsize=label_size,
            va='top', ha='left',
            bbox=dict(facecolor='#f9f9f9', edgecolor='gray', boxstyle='round,pad=0.4', alpha=0.95)
        )

        # Limpieza de títulos (sin labels innecesarios)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax2.set_ylabel("")

        plt.tight_layout(rect=[0, 0, 0.95, 0.93], pad=2)

        filename = f"pareto_{group_by}_{indicator}.png"
        #plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches='tight')
        #plt.close(fig)
        plt.show()

    except Exception as e:
        print(f"❌ Error en pareto_graphic(): {e}")

# ==============================
# GRÁFICO DONUT (participación)
# ==============================
def donut_graphic(
        project_address,
        data,          # Serie agregada (ideal) o DataFrame
        date,
        group_by,
        indicator,
        width=7,
        height=7,
        fontsize=16,
        colors=None
    ):
    try:
        # Serie descendente
        s = _ensure_series(data, group_by, indicator, ascending=False)
        if s.empty:
            raise ValueError("Serie de datos vacía para donut_graphic().")

        total = float(s.sum())
        labels = [str(i) for i in s.index]
        values = s.values

        # Colores por defecto (paleta cálida sobria)
        if not colors or len(colors) < len(values):
            colors = ["#F57C00", "#FF9800", "#FFB74D", "#FFE0B2", "#795548", "#9E9E9E"] * 5

        fig, ax = plt.subplots(figsize=(width, height))

        # Donut
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct=lambda pct: (f"{pct:.1f}%" if pct >= 3 else ""),  # evitar ruido <3%
            startangle=90,
            textprops=dict(color="#111", fontsize=fontsize-2),
            colors=colors[:len(values)],
            wedgeprops=dict(width=0.35, edgecolor="#333333", linewidth=0.5)
        )
        ax.set_aspect('equal')

        # Centro con total
        ax.text(
            0, 0,
            f"Total\n{total:,.1f} CF",
            ha='center', va='center',
            fontsize=fontsize, color="#111", weight="bold"
        )

        # Cuadro resumen (fecha)
        ax.text(
            0.80, 0.20,
            f"{date}",
            transform=ax.transAxes,
            fontsize=fontsize-2,
            va='top', ha='left',
            bbox=dict(facecolor='#f9f9f9', edgecolor='gray', boxstyle='round,pad=0.4', alpha=0.95)
        )

        # Spines off
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.tight_layout(rect=[0, 0, 0.95, 0.93], pad=2)

        filename = f"donut_{group_by}_{indicator}.png"
        #plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches='tight')
        #plt.close(fig)
        plt.show()

    except Exception as e:
        print(f"❌ Error en donut_graphic(): {e}")

# ==============================
# GRÁFICO LOLLIPOP (horizontal)
# ==============================
def lollipop_graphic(
        project_address,
        data,          # Serie agregada (ideal) o DataFrame
        date,
        group_by,
        indicator,
        width=12,
        height=7,
        fontsize=16,
        color="#B71C1C"
    ):
    try:
        # Serie ascendente para lectura de abajo hacia arriba
        s = _ensure_series(data, group_by, indicator, ascending=True)
        if s.empty:
            raise ValueError("Serie de datos vacía para lollipop_graphic().")

        total = float(s.sum())

        fig, ax = plt.subplots(figsize=(width, height))

        # Líneas base + puntos
        ax.hlines(y=s.index, xmin=0, xmax=s.values, color="#9e9e9e", alpha=0.6, linewidth=1.2)
        ax.plot(s.values, s.index, "o", color=color, markersize=8, markeredgecolor="#333333", markeredgewidth=0.5)

        # Etiquetas de valor a la derecha del punto
        for x, y in zip(s.values, s.index):
            ax.annotate(
                f"{x:,.1f} CF",
                xy=(x, y),
                xytext=(6, -2),
                textcoords="offset points",
                ha='left', va='center',
                fontsize=fontsize-2, color='black'
            )

        # Estética general
        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)

        ax.grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.set_xlabel("")
        ax.set_ylabel("")

        # Formato de miles en eje X
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))

        # Ticks tamaño
        ax.tick_params(axis='x', labelsize=fontsize-2)
        ax.tick_params(axis='y', labelsize=fontsize-2)

        # Cuadro resumen
        ax.text(
            0.80, 0.20,
            f"{date}\n\nTotal: {total:,.1f} CF",
            transform=ax.transAxes,
            fontsize=fontsize-2,
            va='top', ha='left',
            bbox=dict(facecolor='#f9f9f9', edgecolor='gray', boxstyle='round,pad=0.4', alpha=0.95)
        )

        plt.tight_layout(rect=[0, 0, 0.95, 0.93], pad=2)

        filename = f"lollipop_{group_by}_{indicator}.png"
        #plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches='tight')
        #plt.close(fig)
        plt.show()

    except Exception as e:
        print(f"❌ Error en lollipop_graphic(): {e}")