import argparse

from . import temp_anomalies


def temp_anomalies_graz():
    """Entry point for the temp_anomalies_graz"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start",
        required=True,
        type=int,
        help="Start year of the reference timeframe.",
    )
    parser.add_argument(
        "--end",
        required=True,
        type=int,
        help="End year of the reference timeframe.",
    )
    parser.add_argument(
        "--month",
        required=False,
        type=int,
        default=int(0),
        help="Month for which the mean values are calculated (0 for all months or 1-12 for specific month) Default: 0",
    )
    parser.add_argument(
        "--comp",
        required=True,
        nargs="+",
        type=int,
        help="two integers for the start and end year of timeframe to compare to reference frame",
    )
    parser.add_argument(
        "--fig",
        required=False,
        action="store_true",
        help="Show data in figure.",
    )
    parser.add_argument(
        "--trend",
        required=False,
        action="store_true",
        help="Show trend in figure. Trend will be calculated for the timespan specified in --comp",
    )

    args = parser.parse_args()

    monthly, yearly = temp_anomalies.calc_mean(args.start, args.end)
    if args.trend:
        trend_coef = temp_anomalies.trend(monthly, args.month, args.comp)
    else:
        trend_coef = None
    if args.fig:
        temp_anomalies.figure(
            monthly,
            yearly,
            args.comp,
            args.month,
            trend_coef,
        )
