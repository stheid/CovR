import cloudscraper
import io
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from itertools import repeat
# import requests
from matplotlib.dates import WeekdayLocator, DateFormatter, DayLocator, MO
from matplotlib.ticker import MultipleLocator
from numbers import Number
from operator import mul

DPI = 90


def english_floats(s):
    if isinstance(s, Number):
        return s
    # convert all . to ,
    return s.replace(',', '.')


def remove_thousends(s):
    if isinstance(s, Number):
        return s
    return s.replace('.', '')


def gen_plot():
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/Nowcasting_Zahlen.xlsx?__blob=publicationFile"
    df = (
        pd.read_excel(
            io.BytesIO(cloudscraper.create_scraper().get(url, stream=True).content),
            sheet_name='Nowcast_R',
            na_values=['.'],
            engine='openpyxl',
            index_col='Datum des Erkrankungsbeginns',
            parse_dates=True,
            date_parser=lambda s: pd.to_datetime(s, format="%d.%m.%Y"),
            converters={4: remove_thousends,
                        7: english_floats,
                        8: english_floats,
                        9: english_floats,
                        10: english_floats,
                        11: english_floats,
                        12: english_floats}
        )
            .rename_axis(index='date')
            .pipe(lambda df_:
                  pd.concat({
                      'daily': df_.iloc[:, 3].rename('delta'),
                      '4-day': df_.iloc[:, [6, 7, 8]].set_axis(['R', 'low', 'high'], axis='columns', inplace=False),
                      '7-day': df_.iloc[:, [9, 10, 11]].set_axis(['R', 'low', 'high'], axis='columns', inplace=False)
                  }, axis='columns')
                  )
    )

    dfdeltacase = df.daily.astype(dict(delta='int')).reset_index()
    df4 = (df['4-day'].dropna()
           .astype(dict(R='float', low='float', high='float'))
           .reset_index())
    df7 = (df['7-day'].dropna()
           .astype(dict(R='float', low='float', high='float'))
           .reset_index())

    today = date.today()

    # plot cases, r and 7-day r
    fig, ax = plt.subplots()
    ax.fill_between(df7.date, df7.low, df7.high, alpha=.5)
    ax.plot(df7.date, df7.R, marker='o', markersize=2, label="7-day R", alpha=1)
    ax.plot(df4.date, df4.R, c='gray', label='daily R', alpha=.4)
    fig.legend(loc=(.7, .85))
    ax.set_ylim((0, None))
    ax2 = ax.twinx()
    ax2.fill_between(dfdeltacase.date, 0, dfdeltacase.delta, label="daily cases", alpha=.15)
    ax2.set_ylim(tuple(map(mul, ax.get_ylim(), repeat(5000))))

    # zero line
    ax.plot((df4.date.iloc[[0, -1]][0], today), (1, 1), c='r')
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
