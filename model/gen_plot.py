import pandas as pd
import requests
import io
import matplotlib.pyplot as plt
from datetime import date

from matplotlib.ticker import MultipleLocator

DPI = 90


def gen_plot():
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/Nowcasting_Zahlen.xlsx?__blob=publicationFile"
    r = requests.get(url, stream=True)
    df_src = pd.read_excel(io.BytesIO(r.content), sheet_name='Nowcast_R')

    df = df_src.iloc[:, [0, 7, 8, 9]].dropna().reset_index(drop=True)
    df.columns = ['date', 'R', 'low', 'up']
    df7 = df_src.iloc[:, [0, 10, 11, 12]].dropna().reset_index(drop=True)
    df7.columns = ['date', 'R', 'low', 'up']

    today = date.today()

    fig, ax = plt.subplots()
    ax.fill_between(df7.date, df7.low, df7.up, alpha=.5)
    ax.plot(df7.date, df7.R, marker='o', markersize=2, label="7-day R", alpha=1)
    ax.plot(df.date, df.R, c='gray', label='daily R', alpha=.4)
    ax.legend()
    ax.set_ylim((0, None))
    # zero line
    ax.plot((df.date.iloc[[0, -1]][0], today), (1, 1), c='r')
    # today
    ax.plot((today, today), ax.get_ylim(), c='.5', linestyle='--')
    ax.annotate('Today', (today, 2.5), xytext=(.85, .75), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', width=.5),
                fontsize=12,
                horizontalalignment='left', verticalalignment='top')

    ax.tick_params(which='minor', length=1)

    ax.xaxis.set_minor_locator(MultipleLocator(7))
    ax.grid(which="major")
    ax.grid(which="minor", ls=':')
    ax.set_xlabel('date')
    plt.xticks(rotation=45)
    ax.set_ylabel('R')

    img = io.BytesIO()
    fig.set_size_inches(960 / DPI, 960 / 1.618 / DPI)
    fig.tight_layout()
    fig.savefig(img, format='svg', bbox='tight', dpi=DPI)
    img.seek(0)
    return img
