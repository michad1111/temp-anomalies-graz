import numpy as np
import matplotlib.pyplot as plt
import os
from pkg_resources import resource_filename
import pandas as pd

file_path = resource_filename(__name__, os.path.join("data", "klima-daily_Graz.csv"))

data = pd.read_csv(file_path, index_col=1, parse_dates=True)
data = data[(data["t"].notna())]
data["time_copy"] = pd.to_datetime(data.index)
data["month"] = data.time_copy.dt.month
data["year"] = data.time_copy.dt.year

month_dict = {
    0: "all months",
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def calc_mean(year_start, year_end):

    gru = data.groupby("time").groups
    if np.datetime64(f"{year_start}") < min(data["time_copy"]):
        raise Warning(f"start date to early! earliest date: {min(data['time_copy'])}")
    if np.datetime64(f"{year_end}") > max(data['time_copy']):
        raise Warning(f"end date to late! maximum date: {max(data['time_copy'])}")

    monthly_av = data.groupby([data.index.year, data.index.month]).mean().dropna()

    timeframe = monthly_av[(monthly_av.year >= year_start) & (monthly_av.year <= year_end)]
    timeframe_av = timeframe.groupby(timeframe.month).mean()

    for col in ["t", "tmax", "tmin"]:
        for i in range(1,13):
            monthly_av.loc[monthly_av.month == i, f"{col}_anom"] = monthly_av.loc[monthly_av.month == i, f"{col}"] - timeframe_av.loc[i, f"{col}"]

    yearly_av_anom = monthly_av.groupby(monthly_av.year).mean()

    return monthly_av, yearly_av_anom


def trend(anomalies, years, year_comp=None):
    if year_comp is None:
        year_comp = [min(years), max(years)]

    anomalies_timefilter = anomalies[
        year_comp[0] - years[0] : year_comp[1] - years[0] + 1, 0
    ]
    fit_valid_points = ~np.isnan(anomalies_timefilter)
    trend_coef = np.polyfit(
        np.arange(year_comp[0], year_comp[1] + 1)[fit_valid_points],
        anomalies_timefilter[fit_valid_points],
        1,
    )
    print(f"trend: {trend_coef}")
    return trend_coef


def get_year(data_obj):
    return data_obj.astype("datetime64[Y]").astype(int) + 1970


def figure(
    years, anomalies, year_comp, year_start, year_end, month=None, trend_coef=None
):
    if year_comp is None:
        year_comp = [year_start, year_end]
    if month is None:
        month = int(0)

    fig, ax = plt.subplots()
    ax.plot(
        years[year_comp[0] - years[0] : year_comp[1] - years[0] + 1],
        anomalies[year_comp[0] - years[0] : year_comp[1] - years[0] + 1],
        label=["t", "tmax", "tmin"],
    )
    if trend_coef is not None:
        temp_trend = np.polyval(trend_coef, years)
        ax.plot(
            years[year_comp[0] - years[0] : year_comp[1] - years[0] + 1],
            temp_trend[year_comp[0] - years[0] : year_comp[1] - years[0] + 1],
            label=f"t-trend {np.round(trend_coef[0]*10, 2)} °C/dec",
        )
    ax.set_xlabel("year")
    ax.set_ylabel(r"$\Delta$ T / °C")
    ax.set_title(
        f"temperature anomalies for {month_dict[month]} in Graz (compaired to {year_start}-{year_end})"
    )
    ax.legend()
    ax.grid()
    plt.show()

    fig.savefig("anomalies.png")

calc_mean(1995,2000)