import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

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
        data,
        date,
        group_by,
        indicator,
        width=11,
        height=6,
        label_size=12,
        fontsize=11,
        bar_color="#2196F3",   # Azul más intenso
        line_color="#FF5722"   # Naranja fuerte para contraste
    ):
    try:
        s = _ensure_series(data, group_by, indicator, ascending=False)
        if s.empty:
            raise ValueError("Serie de datos vacía para pareto_graphic().")

        total = float(s.sum())
        cumperc = 100 * s.cumsum() / total
        x = np.arange(len(s))

        fig, ax = plt.subplots(figsize=(width, height), facecolor="white")

        # --- Barras ---
        bars = ax.bar(x, s.values, color=bar_color, alpha=0.85)
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.annotate(f"{h:,.0f}",
                            xy=(bar.get_x() + bar.get_width()/2, h),
                            xytext=(0, 4),
                            textcoords="offset points",
                            ha="center", va="bottom",
                            fontsize=label_size+4,
                            fontweight="bold",
                            color="#222")

        # --- Línea de Pareto ---
        ax2 = ax.twinx()
        ax2.plot(x, cumperc.values,
                 marker="o", markersize=7,
                 color=line_color, linewidth=2.5)
        ax2.set_ylim(0, 105)

        # % solo en puntos clave
        key_points = [0, np.argmax(cumperc >= 80), len(cumperc)-1]
        for i in key_points:
            val = cumperc.iloc[i]
            ax2.annotate(f"{val:.1f}%",
                         xy=(x[i], val),
                         xytext=(0, 6),
                         textcoords="offset points",
                         ha="center", va="bottom",
                         fontsize=label_size+5,
                         fontweight="bold",
                         color=line_color)

        # --- Quitar ejes Y ---
        ax.yaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for spine in ax2.spines.values():
            spine.set_visible(False)

        # --- Eje X ---
        ax.set_xticks(x)
        ax.set_xticklabels(
            s.index,
            rotation=30,
            ha="right",
            fontsize=label_size+1,
            color="#111"
        )

        # --- Grid discreto ---
        ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.25, color="#aaa")

        # --- Título (menos importante que etiquetas) ---
        ax.set_title(
            f"{group_by} – {date}",
            fontsize=label_size,  # mismo tamaño que etiquetas
            color="#555",
            pad=10,
            fontweight="normal"
        )

        # --- Ajustes de margenes ---
        plt.subplots_adjust(top=0.88, bottom=0.24, left=0.06, right=0.98)

        filename = f'pareto_{group_by}_{indicator}.png'
        plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches='tight')
        plt.close(fig)

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

        # Colores → si no pasan, usamos un degradado cálido (Oranges)
        if not colors or len(colors) < len(values):
            cmap = plt.cm.Oranges
            colors = [cmap(i/len(values)) for i in range(len(values))]

        fig, ax = plt.subplots(figsize=(width, height))

        # Donut
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,  # 🔹 quitamos para usar leyenda aparte
            autopct=lambda pct: (f"{pct:.1f}%" if pct >= 3 else ""), 
            startangle=90,
            textprops=dict(color="black", fontsize=fontsize-3),
            colors=colors[:len(values)],
            wedgeprops=dict(width=0.35, edgecolor="white", linewidth=1)
        )
        ax.set_aspect('equal')

        # Centro con total destacado
        ax.text(
            0, 0.05,
            f"{total:,.0f}",
            ha="center", va="center",
            fontsize=fontsize+6, weight="bold", color="#222"
        )
        ax.text(
            0, -0.15,
            f"{indicator}",
            ha="center", va="center",
            fontsize=fontsize-2, color="#555"
        )

        # Título arriba
        fig.suptitle(
            f"{group_by} - {date}",
            fontsize=fontsize+4,
            weight="bold",
            color="#333",
            y=0.98
        )

        # Leyenda estilizada
        ax.legend(
            wedges,
            [f"{l}  ({v:,.0f})" for l, v in zip(labels, values)],
            title="Detalle",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.3, 1),
            fontsize=fontsize-3,
            title_fontsize=fontsize-2,
            frameon=True,
            facecolor="white",
            edgecolor="gray"
        )

        # Spines off
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.tight_layout(rect=[0, 0, 0.9, 0.93])

        filename = f"donut_{group_by}_{indicator}.png"
        # plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches="tight")
        # plt.close(fig)
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