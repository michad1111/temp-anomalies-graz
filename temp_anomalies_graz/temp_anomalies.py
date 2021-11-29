import numpy as np
import matplotlib.pyplot as plt
import os
from pkg_resources import resource_filename

file_path = resource_filename(__name__, os.path.join("data", "klima-daily_Graz.csv"))

data_date = np.genfromtxt(
    file_path, skip_header=1, usecols=1, delimiter=",", dtype=np.datetime64
)
data_temp = np.genfromtxt(file_path, skip_header=1, usecols=(2, 3, 4), delimiter=",")

# check for equal length of data sets
if np.shape(data_date)[0] != np.shape(data_temp)[0]:
    raise Warning("length of date and temp data does not match")

month_dict = {0: 'all months',
              1: 'January',
              2: 'February',
              3: 'March',
              4: 'April',
              5: 'May',
              6: 'June',
              7: 'July',
              8: 'August',
              9: 'September',
              10: 'October',
              11: 'November',
              12: 'December',}


def calc_mean(year_start, year_end, month=None, year_comp=None):
    if year_comp is None:
        year_comp = [year_start, year_end + 1]
    if month is None:
        month = int(0)
        month_shift = int(1)
    else:
        month_shift = month

    if np.datetime64(f"{year_start}") < min(data_date):
        raise Warning(f"start date to early! earliest date: {min(data_date)}")
    if np.datetime64(f"{year_end}") > max(data_date):
        raise Warning(f"end date to late! maximum date: {max(data_date)}")

    years = range(get_year(min(data_date)), get_year(max(data_date)) + 1)

    mean_years = [[0, 0, 0]]
    for year in years:
        timestamp = [
            np.datetime64(f"{year}") + np.timedelta64(month_shift - 1, "M"),
            np.datetime64(f"{year}") + np.timedelta64(month_shift, "M"),
        ]
        if month == int(0): timestamp[1] += np.timedelta64(11, "M")
        filter_date = (data_date >= timestamp[0]) & (data_date < timestamp[1])
        mean_new = np.nanmean(data_temp[filter_date], axis=0)
        mean_years = np.append(mean_years, [mean_new], axis=0)
    mean_years = mean_years[1:]

    mean_timeframe = np.nanmean(
        mean_years[year_start - years[0] : year_end - years[-1] - 1], axis=0
    )
    anomalies = mean_years - mean_timeframe

    anomalies_comp = anomalies[year_comp[0] - years[0] : year_comp[1] - years[0] + 1]
    print(f"Anomalies for {month_dict[month]} from {year_comp[0]} to {year_comp[1]}: ", anomalies_comp)

    return anomalies, years


def trend(anomalies, years):
    fit_valid_points = np.isfinite(anomalies[:, 0])
    trend = np.polyfit(np.array(years)[fit_valid_points], anomalies[:, 0][fit_valid_points], 1)
    return trend

def get_year(data_obj):
    return data_obj.astype("datetime64[Y]").astype(int) + 1970


def figure(years, anomalies, year_comp, year_start, year_end, month=None, trend=None):
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
    if trend is not None:
        t_trend = np.polyval(trend, years)
        ax.plot(years[year_comp[0] - years[0] : year_comp[1] - years[0] + 1],
                t_trend[year_comp[0] - years[0] : year_comp[1] - years[0] + 1],
                label="trend")
    ax.set_xlabel("year")
    ax.set_ylabel(r"$\Delta$ T / °C")
    ax.set_title(
        f"temperature anomalies for {month_dict[month]} in Graz (compaired to {year_start}-{year_end})"
    )
    ax.legend()
    ax.grid()
    plt.show()

    fig.savefig("anomalies.png")