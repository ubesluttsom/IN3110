#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

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
    # add path to .csv file from 6.0
    path = csv

    # read .csv file, define which columns to read
    df = pd.read_csv(
        path,
        sep=",",
        usecols=["location"] + ["date"] + columns,
        parse_dates=["date"],
        date_parser=lambda col: pd.to_datetime(col, format="%Y-%m-%d"),
    )

    if countries is None:
        # no countries specified, pick 6 countries with the highest case count at end_date
        if end is None:
            # no end date specified, pick latest date available
            end_date = df.date.iloc[-1]
        else:
            end_date = datetime.strptime(end, "%Y-%m-%d")
        df_latest_dates = df[df.date.isin([end_date])]

        # identify the 6 countries with the highest case count
        # on the last included day
        tmp = df.groupby("location")         # group locations, AKA countries
        tmp = tmp["new_cases_per_million"]   # select right column
        tmp = tmp.sum()                      # per 'location', do the sum
        tmp = tmp.sort_values()              # sort by the above sum, ascending
        tmp = tmp.tail(6)                    # choose highest 6 values
        countries = tmp.index                # select index

    # now filter to include only the selected countries
    cases_df = df.loc[df["location"].isin(countries)]

    # apply date filters
    if start is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        # exclude records earlier than start_date
        cases_df = cases_df[cases_df["date"] >= start_date]

    if end is not None:
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if start_date is not None and start_date >= end_date:
            raise ValueError("The start date must be earlier than the end date.")

        # exclude records later than end date
        cases_df = cases_df[cases_df["date"] <= end_date]

    return cases_df


def plot_reported_cases_per_million(countries=None, start=None, end=None):
    """Plots data of reported covid-19 cases per million using altair.
    Calls the function get_data_from_csv to receive a dataframe used for
    plotting.

    Args:
        countries ((list(string), optional): List of countries you want to
            filter.  If none is passed, dataframe will be filtered for the 6
            countries with the highest number of cases per million at the last
            current date available in the timeframe chosen.
        start (string, optional): a string of the start date of the table, none
            of the dates will be older then this on
        end (string, optional): a string of the en date of the table, none of
            the dates will be newer then this one
    Returns:
        altair Chart of number of reported covid-19 cases over time.
    """
    # choose data column to be extracted
    columns = ["new_cases_per_million"]
    # create dataframe
    cases_df = get_data_from_csv(columns,
                                 countries=countries,
                                 start=start,
                                 end=end)

    # Note: when you want to plot all countries simultaneously while enabling
    # checkboxes, you might need to disable altairs max row limit by commenting
    # in the following line alt.data_transformers.disable_max_rows()

    chart = (
        alt.Chart(cases_df,
                  title=f"Reported new COVID-19 cases, {start} to {end}")
        .mark_line()
        .encode(
            x=alt.X(
                "date:T",
                axis=alt.Axis(
                    format="%b, %Y", title="Date", titleFontSize=14, tickCount=20
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
            color=alt.Color("location:N", legend=alt.Legend(title="Country")),
        )
        .interactive()
    )
    return chart


def main():
    """Function called when run as a script

    Creates a chart and display it or save it to a file
    """
    chart = plot_reported_cases_per_million(
        #['Norway', 'Sweden', 'Denmark'],
        #start='2021-11-15',
        #end='2021-11-22',
    )
    # chart.show requires altair_viewer
    # or you could save to a file instead
    chart.show()


if __name__ == "__main__":
    main()
