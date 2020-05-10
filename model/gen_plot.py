import pandas as pd
import requests
import io
import matplotlib.pyplot as plt

DPI = 90


def gen_plot():
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/Nowcasting_Zahlen.xlsx?__blob=publicationFile"
    r = requests.get(url, stream=True)
    df = pd.read_excel(io.BytesIO(r.content))

    df = df.iloc[:, [0, 7, 8, 9]].dropna().reset_index(drop=True)
    df.columns = ['date', 'R', 'low', 'up']

    fig, ax = plt.subplots()
    ax.plot(df.date.iloc[[0, -1]], (1, 1), c='r')
    ax.fill_between(df.date, df.low, df.up, alpha=.5)
    ax.plot(df.date, df.R)
    ax.grid(which="both")
    ax.set_ylim((0, None))
    ax.set_xlabel('date')
    plt.xticks(rotation=45)
    ax.set_ylabel('R')

    img = io.BytesIO()
    fig.set_size_inches(960 / DPI, 960 / 1.618 / DPI)
    fig.tight_layout()
    fig.savefig(img, format='png', bbox='tight', dpi=DPI)
    img.seek(0)
    return img
