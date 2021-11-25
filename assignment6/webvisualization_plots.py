#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

import altair as alt
import pandas as pd

def get_data_from_csv(
        columns,
        countries=None,
        start=None,
        end=None,
        csv="owid-covid-data.csv",
    ):
    """Creates pandas dataframe from .csv file.

    Data will be filtered based on data column name, list of countries to be plotted and
    time frame chosen.

    Args:
        columns (list(string)): a list of data columns you want to include
        countries ((list(string), optional): List of countries you want to
            include.  If none is passed, dataframe should be filtered for the 6
            countries with the highest number of cases per million at the last
            current date available in the timeframe chosen.
        start (string, optional): The first date to include in the returned
            dataframe.  If specified, records earlier than this will be
            excluded.
            Default: include earliest date
            Example format: "2021-10-10"
        end (string, optional): The latest date to include in the returned data frame.
            If specified, records later than this will be excluded.
            Example format: "2021-10-10"
    Returns:
        cases_df (dataframe): returns dataframe for the timeframe, columns, and
            countries chosen
    """

    # Read .csv file, define which columns to read.

    df = pd.read_csv(
        csv,
        sep=",",
        usecols=["location"] + ["date"] + columns,
        parse_dates=["date"],
        date_parser=lambda col: pd.to_datetime(col, format="%Y-%m-%d"),
    )

    # If no countries specified, pick 6 countries with the highest case
    # count at end_date.

    if countries is None:

        # If no end date specified, pick latest date available. Else, format
        # date properly.

        if end is None:
            end_date = df.date.iloc[-1]
        else:
            end_date = datetime.strptime(end, "%Y-%m-%d")

        # Based on end date, generate list of all dates in latest week. I'm
        # using `timedelta` from `datetime`, which allows for some basic time
        # arithmetic, in a list comprehension. Then, find all rows in dataframe
        # with `date` in this list.

        df_latest_week = df[df.date.isin(
            [end_date - timedelta(days=i) for i in range(7)]
        )]

        # Identify the 6 locations with the highest case count
        # on the last included day.

        countries = (
            df_latest_week.groupby("location")   # group locations
            ["new_cases_per_million"]            # select right column
            .sum()                               # per 'location', do the sum
            .sort_values()                       # sort by the above sum
            .tail(6)                             # choose highest 6 values
            .index                               # select index
        )

    # Now filter to include only the selected locations/countries.

    cases_df = df.loc[df["location"].isin(countries)]

    # Apply date filters. Make sure to exclude records later than `end_date`,
    # and exclude records earlier than `start_date`.

    if start is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        cases_df = cases_df[cases_df["date"] >= start_date]

    if end is not None:
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if start_date is not None and start_date >= end_date:
            raise ValueError(
                "The start date must be earlier than the end date."
            )
        cases_df = cases_df[cases_df["date"] <= end_date]

    return cases_df


def plot_reported_cases_per_million(
        countries=None,
        start=None,
        end=None,
    ):
    """Plots data of reported COVID-19 cases per million using altair.
    Calls the function `get_data_from_csv` to receive a dataframe used for
    plotting.

    Args:
        countries (list(string), optional): List of countries you want to
            filter.  If none is passed, dataframe will be filtered for the 6
            countries with the highest number of cases per million at the last
            current date available in the timeframe chosen.
        start (string, optional): a string of the start date of the table, none
            of the dates will be older then this on
        end (string, optional): a string of the en date of the table, none of
            the dates will be newer then this one
    Returns:
        altair Chart of number of reported COVID-19 cases over time.
    """

    # Choose data columns to be extracted. I'm choosing some extra ones, for
    # the tool-tip pop-up.

    columns = ['new_cases_per_million',
               'location',
               'new_cases',
               'tests_per_case',
               'total_cases']

    # Create dataframe from CSV file.

    cases_df = get_data_from_csv(columns,
                                 countries=countries,
                                 start=start,
                                 end=end)

    # If no end date specified, pick latest date available.

    if end is None:
        end = cases_df.date.iloc[-1].strftime('%Y-%m-%d')

    # If no start date specified, pick earliest date available.

    if start is None:
        start = cases_df.date.iloc[0].strftime('%Y-%m-%d')

    # Note: when you want to plot all countries simultaneously while enabling
    # checkboxes, you might need to disable altairs max row limit by commenting
    # in the following line

    alt.data_transformers.disable_max_rows()

    # Make our chart, and return it:

    chart = (
        alt.Chart(cases_df,
                  title=f"Reported new COVID-19 cases, {start} to {end}")
        .mark_line(size=3)
        .encode(
            x=alt.X(
                "date:T",
                axis=alt.Axis(
                    format="%b, %Y",
                    title="Date",
                    titleFontSize=14,
                    tickCount=20
                ),
            ),
            y=alt.Y(
                "new_cases_per_million",
                axis=alt.Axis(
                    title="Number of Reported Cases per Million",
                    titleFontSize=14,
                    tickCount=10,
                ),
            ),
            color=alt.Color(
                "location:N",
                legend=alt.Legend(title="Demographic")
            ),
            tooltip=['location', 'new_cases', 'tests_per_case', 'total_cases'],
        )
        .interactive()
    )

    return chart

def get_countries():
    """Extract a sorted list of countries in dataset
    """

    # Get all unique `location` cells in CSV file.

    locations = pd.read_csv(
        "owid-covid-data.csv",
        sep=",",
        usecols=["location"],
    )['location'].unique()

    # Make the locations into sets, and do operations on those. Probably some
    # overhead doing it like this, but it's more intuitive, for me at least.
    # After, convert it back into a list and sort it alphabetically.

    return sorted(list(
        set(locations) - set(get_regions()) - set(get_incomes())
    ))

def get_regions():
    """Return a list of geographical regions
    """
    return [
        'World',
        'Africa',
        'Asia',
        'Europe',
        'Oceania',
        'North America',
        'South America',
    ]

def get_incomes():
    """Return a list of income regions
    """
    return [
        'High income',
        'Upper middle income',
        'Lower middle income',
        'Low income',
    ]

def main():
    """Function called when run as a script

    Creates a chart and display it or save it to a file
    """
    chart = plot_reported_cases_per_million()
    # chart.show requires altair_viewer
    # or you could save to a file instead
    chart.show()


if __name__ == "__main__":
    main()
