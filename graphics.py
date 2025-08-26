import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

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
# CONFIGURACIÓN GLOBAL DE ESTILO
# ==============================
STYLE = {
    "title": {"fontsize": 14, "color": "#222", "fontweight": "bold"},
    "axis": {"fontsize": 11, "color": "#333", "fontweight": "normal"},
    "ticks": {"fontsize": 11, "color": "#333"},
    "labels": {"fontsize": 14, "color": "#444", "fontweight": "normal"},
    "totals": {"fontsize": 16, "color": "#111", "fontweight": "bold"},
    "secondary": {"fontsize": 11, "color": "#666", "fontweight": "normal"},
}

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
        bar_color="#E41A1C",
        line_color="#1C1C1C"
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
                ax.annotate(f"{h:,.0f} CF",
                            xy=(bar.get_x() + bar.get_width()/2, h),
                            xytext=(0, 4), textcoords="offset points",
                            ha="center", va="bottom",
                            **STYLE["labels"])

        # --- Línea de Pareto ---
        ax2 = ax.twinx()
        ax2.plot(x, cumperc.values, marker="o", markersize=7,
                 color=line_color, linewidth=2)
        ax2.set_ylim(0, 145)

        key_points = [0, np.argmax(cumperc >= 85), len(cumperc)-1]
        for i in key_points:
            val = cumperc.iloc[i]
            ax2.annotate(f"{val:.1f}%",
                         xy=(x[i], val),
                         xytext=(0, 6), textcoords="offset points",
                         ha="center", va="bottom",
                         fontsize=STYLE["labels"]["fontsize"]+1,
                         color=line_color, fontweight="normal")

        # --- Quitar ejes Y ---
        ax.yaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        for spine in list(ax.spines.values()) + list(ax2.spines.values()):
            spine.set_visible(False)

        # --- Eje X ---
        ax.set_xticks(x)
        ax.set_xticklabels(s.index, rotation=30, ha="right", **STYLE["ticks"])

        # --- Grid discreto ---
        ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.25, color="#aaa")

        # --- Título ---
        ax.set_title(f"{group_by} • {date}", **STYLE["title"], pad=10)

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
        data,
        date,
        group_by,
        indicator,
        colors,
        width=8,
        height=7,
    ):
    try:
        s = _ensure_series(data, group_by, indicator, ascending=False)
        if s.empty:
            raise ValueError("Serie de datos vacía para donut_graphic().")

        total = float(s.sum())
        labels = [str(i).split('.')[0][-4:] for i in s.index]
        values = s.values

        if not colors:
            cmap = plt.cm.get_cmap("tab20")
            colors = [cmap(i/len(values)) for i in range(len(values))]
        elif len(colors) < len(values):
            cmap = plt.cm.get_cmap("tab20")
            extra = [cmap(i/len(values)) for i in range(len(values) - len(colors))]
            colors = colors + extra

        min_frac_for_inside = 0.05
        main_labels, main_values, small_labels, small_values = [], [], [], []
        for lbl, val in zip(labels, values):
            if val / total >= min_frac_for_inside:
                main_labels.append(lbl); main_values.append(val)
            else:
                small_labels.append(lbl); small_values.append(val)

        summary_total = 0
        summary_lines = []
        if small_values:
            summary_total = sum(small_values)
            for l, v in zip(small_labels, small_values):
                summary_lines.append(f"{l}: {v:,.0f} CF")
            main_labels.append("Otros"); main_values.append(summary_total)

        fig, ax = plt.subplots(figsize=(width, height))
        wedges, _ = ax.pie(main_values, labels=None, startangle=90,
                           colors=colors[:len(main_values)],
                           wedgeprops=dict(width=0.38, edgecolor="white", linewidth=1))
        ax.set_aspect('equal')

        # --- Etiquetas dentro/fuera ---
        for i, wedge in enumerate(wedges):
            ang = (wedge.theta2 + wedge.theta1) / 2
            theta = np.deg2rad(ang)
            r = 0.38 / 2 + 0.62
            x, y = np.cos(theta) * r, np.sin(theta) * r

            if main_labels[i] == "Otros":
                ax.annotate("Otros", xy=(x, y),
                            xytext=(1.15*np.cos(theta), 1.15*np.sin(theta)),
                            ha="center", va="center",
                            **STYLE["secondary"],
                            arrowprops=dict(arrowstyle="-", lw=0.6, color="#bbb"))
            else:
                ax.text(x, y, f"{main_labels[i]}", ha="center", va="center", **STYLE["labels"])

        # --- Valores afuera ---
        for i, wedge in enumerate(wedges):
            if main_labels[i] == "Otros": continue
            ang = (wedge.theta2 + wedge.theta1) / 2
            x, y = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
            ax.annotate(f"{main_values[i]:,.0f} CF", xy=(x, y), xytext=(1.25*x, 1.25*y),
                        ha="center", va="center", **STYLE["labels"],
                        arrowprops=dict(arrowstyle="-", lw=0.6, color="#bbb"))

        # --- Centro ---
        ax.text(0, 0.05, f"{total:,.0f}", ha="center", va="center", **STYLE["totals"])
        ax.text(0, -0.05, f"{indicator}", ha="center", va="center", **STYLE["secondary"])

        # --- Título ---
        fig.suptitle(f"{group_by} • {date}", **STYLE["title"], y=0.96)

        # --- Resumen de pequeños ---
        if summary_lines:
            resumen = "Otros:\n" + "\n".join(summary_lines) + f"\nTotal {summary_total:,.0f} CF"
            fig.text(0.95, 0.1, resumen, ha="right", va="bottom",
                     **STYLE["secondary"],
                     bbox=dict(facecolor="white", edgecolor="none", linewidth=0, boxstyle="square,pad=0.3"))

        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.subplots_adjust(top=0.90, bottom=0.12, left=0.08, right=0.85)
        filename = f"donut_{group_by}_{indicator}.png"
        plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches="tight")
        plt.close(fig)
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
        color="#B71C1C"
    ):
    try:
        import matplotlib.pyplot as plt
        import os

        # Serie ascendente para lectura de abajo hacia arriba
        s = _ensure_series(data, group_by, indicator, ascending=True)
        if s.empty:
            raise ValueError("Serie de datos vacía para lollipop_graphic().")

        total = float(s.sum())

        fig, ax = plt.subplots(figsize=(width, height))
        ax.set_facecolor("white")

        ax.hlines(y=s.index, xmin=0, xmax=s.values, color="#b0b0b0", alpha=0.6, linewidth=1.2)
        ax.plot(s.values, s.index, "o", color=color, markersize=9,
                markeredgecolor="white", markeredgewidth=1)

        for x, y in zip(s.values, s.index):
            ax.annotate(f"{x:,.0f} CF", xy=(x, y), xytext=(6, -2),
                        textcoords="offset points", ha="left", va="center", **STYLE["labels"])

        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)

        ax.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.3)
        ax.set_xticks([])
        ax.set_yticklabels([str(lbl) for lbl in s.index], **STYLE["ticks"])
        ax.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)

        # Título estandarizado
        fig.suptitle(f"{group_by} • {date}", y=0.96, **STYLE["title"])

        plt.tight_layout(rect=[0, 0, 0.95, 0.93], pad=2)
        filename = f"lollipop_{group_by}_{indicator}.png"
        plt.savefig(os.path.join(project_address, filename), dpi=300, bbox_inches="tight")
        plt.close(fig)

    except Exception as e:
        print(f"❌ Error en lollipop_graphic(): {e}")

# ==============================
# GRÁFICO BARRAS HORIZONTALES
# ==============================
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