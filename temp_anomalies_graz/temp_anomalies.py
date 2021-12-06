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
    if year_start < min(data["year"]):
        raise Warning(f"start date to early! earliest date: {min(data['time_copy'])}")
    if year_end > max(data["year"]):
        raise Warning(f"end date to late! maximum date: {max(data['time_copy'])}")

    monthly_av = data.groupby([data.index.year, data.index.month]).mean().dropna()

    timeframe = monthly_av[
        (monthly_av.year >= year_start) & (monthly_av.year <= year_end)
    ]
    timeframe_av = timeframe.groupby(timeframe.month).mean()

    for col in ["t", "tmax", "tmin"]:
        for i in range(1, 13):
            monthly_av.loc[monthly_av.month == i, f"{col}_anom"] = (
                monthly_av.loc[monthly_av.month == i, f"{col}"]
                - timeframe_av.loc[i, f"{col}"]
            )

    yearly_av = monthly_av.groupby(monthly_av.year).mean()

    return monthly_av, yearly_av


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


def figure(
    monthly_av, yearly_av, year_comp, year_start, year_end, month, trend_coef=None
):
    if year_comp is None:
        year_comp = [year_start, year_end]

    years = monthly_av.index.get_level_values(0).astype(str)
    months = monthly_av.index.get_level_values(1).astype(str)
    dates = pd.to_datetime(years + "-" + months + "-01")
    monthly_av = monthly_av.set_index(dates)

    fig, axs = plt.subplots(3, sharex=True, sharey=True)
    axs[0].plot(dates, monthly_av["t_anom"], label="t", color="g")
    axs[1].plot(dates, monthly_av["tmax_anom"], label="tmax", color="r")
    axs[2].plot(dates, monthly_av["tmin_anom"], label="tmin", color="b")
    plt.xlim(pd.to_datetime([year_comp[0], year_comp[1] + 1], format="%Y"))
    # TODO: option to change time resolution in yearly case
    # if trend_coef is not None:
    #     temp_trend = np.polyval(trend_coef, years)
    #     ax.plot(
    #         years[year_comp[0] - years[0] : year_comp[1] - years[0] + 1],
    #         temp_trend[year_comp[0] - years[0] : year_comp[1] - years[0] + 1],
    #         label=f"t-trend {np.round(trend_coef[0]*10, 2)} °C/dec",
    #     )
    axs[2].set_xlabel("year")
    for i in range(3):
        axs[i].set_ylabel(r"$\Delta$ T / °C")
        axs[i].legend()
        axs[i].grid()
    fig.suptitle(
        f"temperature anomalies for {month_dict[month]} in Graz (compaired to {year_start}-{year_end})"
    )

    fig.savefig("anomalies.png")


mon, yea = calc_mean(1995, 2000)
figure(mon, yea, [1985, 2020], 1995, 2020, int(0))
