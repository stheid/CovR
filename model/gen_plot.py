import pandas as pd
from operator import mul
from itertools import repeat
import requests
import io
import matplotlib.pyplot as plt
from matplotlib.dates import WeekdayLocator, DateFormatter, DayLocator, MO
from datetime import date

from matplotlib.ticker import MultipleLocator

DPI = 90


def gen_plot():
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/Nowcasting_Zahlen.xlsx?__blob=publicationFile"
    r = requests.get(url, stream=True)
    df_src = pd.read_excel(io.BytesIO(r.content), sheet_name='Nowcast_R')
    dfdeltacase = df_src.iloc[:, [0, 4]].dropna().reset_index(drop=True)
    dfdeltacase.columns = ['date', 'deltacase']
    df = df_src.iloc[:, [0, 7, 8, 9]].dropna().reset_index(drop=True)
    df.columns = ['date', 'R', 'low', 'up']
    df7 = df_src.iloc[:, [0, 10, 11, 12]].dropna().reset_index(drop=True)
    df7.columns = ['date', 'R', 'low', 'up']

    today = date.today()

    fig, ax = plt.subplots()
    ax.fill_between(df7.date, df7.low, df7.up, alpha=.5)
    ax.plot(df7.date, df7.R, marker='o', markersize=2, label="7-day R", alpha=1)
    ax.plot(df.date, df.R, c='gray', label='daily R', alpha=.4)
    fig.legend(loc=(.7, .85))
    ax.set_ylim((0, None))
    ax2 = ax.twinx()
    ax2.fill_between(dfdeltacase.date, 0, dfdeltacase.deltacase, label="daily cases", alpha=.15)
    ax2.set_ylim(tuple(map(mul,ax.get_ylim(),repeat(3000))))

    # zero line
    ax.plot((df.date.iloc[[0, -1]][0], today), (1, 1), c='r')
    # today
    ax.plot((today, today), ax.get_ylim(), c='.5', linestyle='--')
    ax.annotate('Today', (today, 2.5), xytext=(.85, .75), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', width=.5),
                fontsize=12,
                horizontalalignment='left', verticalalignment='top')

    ax.tick_params(which='minor', length=1)

    ax.yaxis.set_minor_locator(MultipleLocator(.1))
    ax.xaxis.set_major_formatter(DateFormatter('%d. %h \'%y'))
    ax.xaxis.set_major_locator(DayLocator([1, 15]))
    ax.xaxis.set_minor_locator(WeekdayLocator(MO))
    fig.autofmt_xdate(rotation=20)
    ax.grid(which="major")
    ax.grid(which="minor", ls=':', alpha=.5)
    ax.set_xlabel('date')
    ax.set_ylabel('Reproduction rate $R$')
    ax2.set_ylabel('new daily cases')

    img = io.BytesIO()
    fig.set_size_inches(960 / DPI, 960 / 1.618 / DPI)
    fig.tight_layout()
    fig.savefig(img, format='svg', bbox='tight', dpi=DPI)
    img.seek(0)
    return img
