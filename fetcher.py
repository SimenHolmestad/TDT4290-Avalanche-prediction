import requests
from datetime import date, timedelta
import pandas as pd
from decouple import config
import sqlalchemy as sqla
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import create_engine
import holidays
from io import StringIO

import numpy as np
from matplotlib import pyplot

print(pd.__version__)


def ArchiveFromAPI():
    url = 'https://api01.nve.no/hydrology/forecast/avalanche/v5.0.1/api/Archive/Warning/All/1/2017-12-01/2020-07-15/json'

    r = requests.get(url)
    data = r.text

    df = pd.read_json(StringIO(data))

    df = df.filter(items=['ValidFrom', 'RegionId', 'DangerLevel', "MountainWeather", "AvalancheProblems"])

    df['ValidFrom'] = pd.to_datetime(df['ValidFrom'])
    date_list = [date.date() for date in df['ValidFrom']]
    new_df = df.filter(items=['RegionId', 'DangerLevel'])
    new_df = new_df.rename(columns={"RegionId": 'region'})

    new_df["date"] = date_list
    av_prob_list = []
    cloud_id_list = []
    nedbor_list = []
    vind_list = []
    temp_min_list = []
    temp_max_list = []
    print(int(new_df.size / 3))
    for i in range(int(new_df.size / 3)):
        # column_dict = {
        #     "Nedbør": ["Gjennomsnitt"],
        #     "Vind": ["Styrke"],
        #     "Temperatur": ["Maks", "Min"]
        # }

        try:
            cloud_id_list.append(df["MountainWeather"][i]["CloudCoverId"])
        except TypeError:
            cloud_id_list.append(None)

        # new_df["CloudCoverId"] = cloud_id_list
        '''
        for key in column_dict:
            new_df[key] = fetch_mw(df, key, column_dict, i)

        #cloud_id_list.append(df["MountainWeather"][i]["CloudCoverId"])
        '''
        try:
            for j in range(len(df["MountainWeather"][i]["MeasurementTypes"])):

                # Nedbør
                if df["MountainWeather"][i]["MeasurementTypes"][j]["Name"] == "Nedbør":

                    for k in range(len(df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"])):

                        if df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Name"] == "Gjennomsnitt":
                            try:
                                nedbor_list.append(df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Value"])
                            except TypeError:
                                nedbor_list.append(None)

                # Vind
                if df["MountainWeather"][i]["MeasurementTypes"][j]["Name"] == "Vind":

                    for k in range(len(df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"])):

                        if df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Name"] == "Styrke":
                            try:
                                vind_list.append(df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Value"])
                            except TypeError:
                                vind_list.append(None)

                # Temperatur
                if df["MountainWeather"][i]["MeasurementTypes"][j]["Name"] == "Temperatur":

                    for k in range(len(df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"])):

                        if df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Name"] == "Maks":
                            try:
                                temp_max_list.append(df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Value"])
                            except TypeError:
                                temp_max_list.append(None)

                        if df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Name"] == "Min":
                            try:
                                temp_min_list.append(df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Value"])
                            except TypeError:
                                temp_min_list.append(None)

        except TypeError:
            nedbor_list.append(None)
            vind_list.append(None)
            temp_max_list.append(None)
            temp_min_list.append(None)

        av_prob_dict = {
            0: [0, 0, 0, 0],
            3: [0, 0, 0, 0],
            5: [0, 0, 0, 0],
            7: [0, 0, 0, 0],
            10: [0, 0, 0, 0],
            30: [0, 0, 0, 0],
            45: [0, 0, 0, 0],
            50: [0, 0, 0, 0]
        }

        av_prob_row = df["AvalancheProblems"][i]

        for prob in av_prob_row:
            av_prob_dict[prob["AvalancheProblemTypeId"]] = [int(prob["AvalProbabilityId"]), int(prob["AvalCauseId"]), int(prob["DestructiveSizeId"]), int(prob["AvalTriggerSimpleId"])]

        # print(av_prob_dict)
        av_prob_list.append(av_prob_dict)

    new_dict = {}

    for j, key in enumerate(av_prob_dict):

        new_dict["AvalProbabilityId_" + str(key)] = []
        new_dict["AvalCauseId_" + str(key)] = []
        new_dict["DestructiveSizeId_" + str(key)] = []
        new_dict["AvalTriggerSimpleId_" + str(key)] = []

        for aval_prob_day in av_prob_list:

            av_prob_j = aval_prob_day[key]
            # print("av_prob_j", av_prob_j)

            new_dict["AvalProbabilityId_" + str(key)].append(av_prob_j[0])
            new_dict["AvalCauseId_" + str(key)].append(av_prob_j[1])
            new_dict["DestructiveSizeId_" + str(key)].append(av_prob_j[2])
            new_dict["AvalTriggerSimpleId_" + str(key)].append(av_prob_j[3])

        # print(new_dict)
    new_df["CloudCoverId"] = cloud_id_list
    new_df["Nedbor"] = nedbor_list
    new_df["Vindstyrke"] = vind_list
    new_df["Temperatur_min"] = temp_min_list
    new_df["Temperatur_max"] = temp_max_list
    av_prob_df = pd.DataFrame.from_dict(new_dict)
    # print(av_prob_df)
    # print(av_prob_df.isna().sum())
    # print(new_df)
    # print(new_df.isna().sum())

    avalanche_forecast_df = new_df.join(av_prob_df)
    # print(avalanche_forecast_df)
    return avalanche_forecast_df


def create_db_connection() -> Engine:
    server = 'avalanche-server.database.windows.net,1433'
    database = 'avalanche-db'
    username = config('DBUSERNAME')
    password = config('PASSWORD')
    driver = 'ODBC Driver 17 for SQL Server'

    connection_string = 'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}?Trusted_Connection=yes'.format(
        username=username, password=password, server=server, database=database, driver=driver)
    engine = create_engine(connection_string, connect_args={'timeout': 4000})

    return engine


def get_list_of_avalanche_tuples():
    engine = create_db_connection()
    connection = engine.connect()
    metadata = sqla.MetaData()
    regobs = sqla.Table('regobs_data', metadata,
                        autoload=True, autoload_with=engine)
    query = sqla.select([regobs])
    df = pd.read_sql(query, connection)
    regions = df['forecast_region']
    times = df['time']

    dates = [date.date() for date in times]
    return [(dates[i], regions[i]) for i in range(len(dates))]


def get_avalanche_data(regions, dates):
    avalanches = [0 for x in range(len(regions))]
    avalanche_tuples = get_list_of_avalanche_tuples()

    number_of_ones = 0
    for date_to_check, region in avalanche_tuples:
        for i in range(len(regions)):
            if date_to_check == dates[i] and region == regions[i]:
                if avalanches[i] == 0:
                    number_of_ones += 1
                avalanches[i] = 1
    print("Number of ones:", number_of_ones)
    return avalanches


def main():
    years_to_check = [2017, 2018, 2019]
    list_of_regions = [3003, 3006, 3007, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017, 3022, 3023, 3024, 3027, 3028, 3029, 3031, 3032, 3034, 3035, 3037]

    regions = []
    dates = []
    weekends = []
    weekdays = []
    red_days = []

    norwegian_holidays = holidays.Norway()

    for year_to_check in years_to_check:
        # Set current date to 1. of september the specified year
        current_date = date(year_to_check, 12, 1)

        # Continue until date is 15. of june the following year
        while current_date.month != 6 or current_date.day != 15:
            # Add data for each region
            for region in list_of_regions:
                regions.append(region)
                dates.append(current_date)
                if current_date.weekday() == 5 or current_date.weekday() == 6:
                    weekends.append(1)
                else:
                    weekends.append(0)
                weekdays.append(current_date.weekday() + 1)
                if current_date in norwegian_holidays and current_date.weekday() != 6:
                    red_days.append(1)
                else:
                    red_days.append(0)

            # Go to next day
            current_date = current_date + timedelta(days=1)

    avalanches = get_avalanche_data(regions, dates)

    data_dict = {
        'region': regions,
        'date': dates,
        'weekday': weekdays,
        'weekend': weekends,
        'red_day': red_days,
        'avalanche': avalanches
    }
    df = pd.DataFrame(data_dict)
    # df.to_csv("df.csv", index=False)
    # print(df)
    df_avalanche = ArchiveFromAPI()
    # df_avalanche.to_csv("df_avalanche.csv", index=False)
    print("Fetched Avalanche Forecast")
    # print(df_avalanche)
    result = pd.merge(df, df_avalanche, how='inner', on=['date', 'region'])

    print(result)
    print(result.sum())
    print(result.corr())
    file_content = result.to_csv(index=False)

    # There are some weird stuff in the data that needs to be fixed
    file_content = file_content.replace("--", "-")
    file_content = file_content.replace("|", "")

    f = open("dataset.csv", "w")
    f.write(file_content)
    f.close()


def analyse():
    dataframe = pd.read_csv("df_avalanche.csv")
    region_data = dataframe["region"]

    regions, counts = np.unique(region_data, return_counts=True)

    # print(dataframe.columns)
    # print("antall incidents:", np.sum(dataframe["date"]))

    pyplot.bar(regions, counts)
    pyplot.title("Data points per region")
    pyplot.xlabel("Region ID")
    pyplot.ylabel("Data points")

    pyplot.savefig("Observations_for_region.png")
    pyplot.clf()


if __name__ == "__main__":
    main()
    # analyse()
