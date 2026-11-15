"""Estilo único dos gráficos da EDA (saidas/eda/).

Paleta categórica validada (azul, laranja, verde-água, amarelo), texto em tons neutros,
grade discreta e rótulos diretos. Usada pelo notebooks/eda_vitaliza.ipynb.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "saidas" / "eda"

FUNDO = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
GRADE = "#e4e3df"
NEUTRO = "#a3a29c"
AZUL, LARANJA, AQUA, AMARELO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
FICOU, SAIU = AZUL, LARANJA
CORES_SEGMENTO = {1: AZUL, 2: LARANJA, 3: AQUA, 4: AMARELO}
DIVERGENTE = ["#1c5cab", "#6da7ec", "#f0efec", "#f3a07c", "#c4481a"]  # azul ← cinza → laranja


def estilo() -> None:
    plt.rcParams.update({
        "figure.facecolor": FUNDO, "axes.facecolor": FUNDO, "savefig.facecolor": FUNDO,
        "font.family": "DejaVu Sans", "font.size": 10,
        "text.color": TEXTO, "axes.labelcolor": TEXTO_2, "xtick.color": TEXTO_2, "ytick.color": TEXTO_2,
        "axes.edgecolor": GRADE, "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlepad": 10,
        "legend.frameon": False, "lines.linewidth": 2, "figure.dpi": 110,
    })


def pct(casas: int = 0) -> FuncFormatter:
    return FuncFormatter(lambda v, _: f"{100 * v:.{casas}f}%".replace(".", ","))


def br(v: float, casas: int = 1) -> str:
    """Número no formato brasileiro (vírgula decimal, ponto de milhar)."""
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


MESES_PT = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def titulo(fig, texto: str, sub: str | None = None) -> None:
    """Título e subtítulo no topo, em polegadas fixas (não dependem da altura da figura)."""
    h = fig.get_figheight()
    fig.suptitle(texto, x=0.01, y=1 - 0.1 / h, ha="left", va="top", fontsize=13, fontweight="bold", color=TEXTO)
    if sub:
        fig.text(0.01, 1 - 0.42 / h, sub, ha="left", va="top", fontsize=9.5, color=TEXTO_2)
    fig._topo = 1 - (0.75 if sub else 0.5) / h


def fonte(fig, texto: str) -> None:
    fig.text(0.01, 0.06 / fig.get_figheight(), texto, ha="left", va="bottom", fontsize=8, color=TEXTO_2)


def ajustar(fig) -> None:
    """tight_layout deixando espaço para o título, o subtítulo e a fonte."""
    fig.tight_layout(rect=(0, 0.3 / fig.get_figheight(), 1, getattr(fig, "_topo", 0.96)))


def eixo_meses(ax) -> None:
    """Rótulos de mês em português (jan/25, mar/25...)."""
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 3, 5, 7, 9, 11]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: (lambda d: f"{MESES_PT[d.month - 1]}/{d:%y}")(mdates.num2date(v))))


def salvar(fig, nome: str) -> Path:
    PASTA.mkdir(parents=True, exist_ok=True)
    destino = PASTA / nome
    fig.savefig(destino, dpi=160, bbox_inches="tight")
    return destino
