import argparse

from . import temp_anomalies


def temp_anomalies_graz():
    """Entry point for the temp_anomalies"""
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
        help="Month for which the mean values are calculated (0 to 11, Default 0: January)",
    )
    parser.add_argument(
        "--comp",
        required=False,
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

    args = parser.parse_args()

    anomalies, years = temp_anomalies.calc_mean(
        args.start, args.end, args.month, args.comp
    )
    if args.fig:
        temp_anomalies.figure(years, anomalies, args.comp, args.start, args.end)
