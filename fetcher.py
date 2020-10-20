import requests
from datetime import date, timedelta
import pandas as pd
from decouple import config
import sqlalchemy as sqla
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import create_engine
import holidays
import time
from io import StringIO


def get_avalanche_problem_data(forecast_df):
    """Creates a dictionary containing data for the avalanche problems
    given in an avalanche forecast.
    """
    avalanche_problem_dict = {}
    valid_problem_ids = [0, 3, 5, 7, 10, 30, 45, 50]
    avalanche_problem_features = ["AvalProbabilityId", "AvalCauseId", "DestructiveSizeId", "AvalTriggerSimpleId"]

    # Create skeleton dictionary
    for problem_id in valid_problem_ids:
        for feature in avalanche_problem_features:
            avalanche_problem_dict[feature + "_" + str(problem_id)] = []

    # Loop through each row of dataframe
    for i in range(len(forecast_df.index)):
        # Create dictionary of zeros for avalanche problems in current row
        # (Same format as avalalanche_problem_dict)
        output_for_row = {}
        for problem_id in valid_problem_ids:
            for feature in avalanche_problem_features:
                output_for_row[feature + "_" + str(problem_id)] = 0

        # Get list of avalalanche problems
        av_problem_list = forecast_df["AvalancheProblems"][i]

        # Add data for each avalanche problem to output_for_row
        for av_problem in av_problem_list:
            av_problem_id = av_problem["AvalancheProblemTypeId"]
            if av_problem_id in valid_problem_ids:
                # Add avalanche problem data to current row
                for feature in avalanche_problem_features:
                    output_for_row[feature + "_" + str(av_problem_id)] = av_problem[feature]

        # Add row data to output dictionary
        for key, value in output_for_row.item():
            avalanche_problem_dict[key].append(value)

    return pd.DataFrame(avalanche_problem_dict)


def get_mountain_weather_data(forecast_df):
    possible_measurement_types = ["Nedbør", "Vindstyrke", "Temperatur"]
    output_dict = {}
    for feature in mountain_weather_features:
        output_dict[feature] = []

    # Loop through each row of dataframe
    for i in range(len(forecast_df.index)):
        mountain_weather_dict = forecast_df["MountainWeather"][i]
        if ("CloudCoverId" in mountain_weather_dict.keys):
            output_dict["CloudCoverId"].append(mountain_weather_dict["CloudCoverId"])
        else:
            output_dict["CloudCoverId"].append(0)

        measurement_types = forecast_df["MountainWeather"][i]["MeasurementTypes"]
        for type_dict in measurement_types:
            if type_dict["Name"] == "Nedbør":
                pass
            if type_dict["Name"] == "Temperatur":
                pass



    new_df["date"] = date_list
    cloud_id_list = []
    nedbor_list = []
    vind_list = []
    temp_min_list = []
    temp_max_list = []
    print(len(new_df.index))
    for i in range(len(new_df.index)):
        try:
            cloud_id_list.append(forecast_df["MountainWeather"][i]["CloudCoverId"])
        except TypeError:
            cloud_id_list.append(None)

        try:
            for j in range(len(forecast_df["MountainWeather"][i]["MeasurementTypes"])):
                # Nedbør
                if forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["Name"] == "Nedbør":

                    for k in range(len(forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"])):

                        if forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Name"] == "Gjennomsnitt":
                            try:
                                nedbor_list.append(forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Value"])
                            except TypeError:
                                nedbor_list.append(None)
                # Vind
                if forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["Name"] == "Vind":

                    for k in range(len(forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"])):

                        if forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Name"] == "Styrke":
                            try:
                                vind_list.append(forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Value"])
                            except TypeError:
                                vind_list.append(None)

                # Temperatur
                if forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["Name"] == "Temperatur":

                    for k in range(len(forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"])):

                        if forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Name"] == "Maks":
                            try:
                                temp_max_list.append(forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Value"])
                            except TypeError:
                                temp_max_list.append(None)

                        if forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Name"] == "Min":
                            try:
                                temp_min_list.append(forecast_df["MountainWeather"][i]["MeasurementTypes"][j]["MeasurementSubTypes"][k]["Value"])
                            except TypeError:
                                temp_min_list.append(None)

        except TypeError:
            nedbor_list.append(None)
            vind_list.append(None)
            temp_max_list.append(None)
            temp_min_list.append(None)

    new_df["CloudCoverId"] = cloud_id_list
    new_df["Nedbor"] = nedbor_list
    new_df["Vindstyrke"] = vind_list
    new_df["Temperatur_min"] = temp_min_list
    new_df["Temperatur_max"] = temp_max_list
    av_prob_df = pd.DataFrame.from_dict(new_dict)

    avalanche_forecast_df = new_df.join(av_prob_df)
    return avalanche_forecast_df


def create_avalanche_forecast_url(seasons_to_check):
    url_format_string = 'https://api01.nve.no/hydrology/forecast/avalanche/v5.0.1/api/Archive/Warning/All/1/{}/{}/json'
    first_season = seasons_to_check[0]
    last_season = seasons_to_check[-1]

    # We start from first of december for the first season
    first_date_string = str(first_season) + "-12-01"

    # We end at 15th of june for the last season
    last_date_string = str(last_season + 1) + "-06-15"

    return url_format_string.format(first_date_string, last_date_string)


def get_avalanche_forecast_data(seasons_to_check):
    url = create_avalanche_forecast_url(seasons_to_check)

    # Fetch forecast data
    data = requests.get(url).text

    # Create dataframe
    forecast_df = pd.read_json(StringIO(data))

    # Filter relevant inforrmation
    forecast_df = forecast_df.filter(items=['ValidFrom', 'RegionId', 'DangerLevel', "MountainWeather", "AvalancheProblems"])

    # Convert datetime strings to date values
    forecast_df['date'] = [date.date() for date in pd.to_datetime(forecast_df['ValidFrom'])]
    forecast_df = forecast_df.rename(columns={"RegionId": 'region'})

    base_data_df = forecast_df.filter(items=['date', 'region', 'DangerLevel'])
    mountain_weather_df = get_mountain_weather_data(forecast_df)
    avalanche_problem_df = get_avalanche_problem_data(forecast_df)

    return pd.join([base_data_df, mountain_weather_df, avalanche_problem_df])


def create_db_connection() -> Engine:
    """Creates engine for accessing the database """
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
    """Retrieves data from database and create a list of tuples on the
    form (date, region) where each tuple corresponds to a day and a
    region where an avalanche have happened.

    """
    engine = create_db_connection()
    connection = engine.connect()
    metadata = sqla.MetaData()
    regobs = sqla.Table('regobs_data', metadata,
                        autoload=True, autoload_with=engine)
    query = sqla.select([regobs])
    df = pd.read_sql(query, connection)
    regions = df['forecast_region']
    times = df['time']

    # Convert time-info to date-info
    dates = [date.date() for date in times]
    return [(dates[i], regions[i]) for i in range(len(dates))]


def get_avalanche_data(regions, dates):
    """Takes two lists of the same length containing regions and dates.
    Returns a list of the same length with a 1 if an avalanche
    happened for that region and date combination, otherwise 0.

    This function might be optimized further.
    """
    # Start by creating a list of correct length with just zeros.
    avalanches = [0 for x in range(len(regions))]

    # Get data for where the avalanches have been.
    avalanche_tuples = get_list_of_avalanche_tuples()

    # Check every avalanche incident with all dates and regions in list
    for date_to_check, region in avalanche_tuples:
        for i in range(len(regions)):
            # Check if both date and region corresponds
            if date_to_check == dates[i] and region == regions[i]:
                avalanches[i] = 1
                break

    return avalanches


def create_calendar_and_region_data(years_to_check, list_of_regions):
    """Returns a dictionary containing lists of equal length. The lists
    would have one row for each combination of year and region
    """
    regions = []
    dates = []
    weekends = []
    weekdays = []
    red_days = []

    norwegian_holidays = holidays.Norway()

    for year_to_check in years_to_check:
        # Set current date to 1. of december of the specified year
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

    # Return dectionary with all data
    return {
        'region': regions,
        'date': dates,
        'weekday': weekdays,
        'weekend': weekends,
        'red_day': red_days,
    }


def main():
    # For seasons, 2017 means the season 2017-2018
    seasons_to_check = [2017, 2018, 2019]
    list_of_regions = [3003, 3006, 3007, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017, 3022, 3023, 3024, 3027, 3028, 3029, 3031, 3032, 3034, 3035, 3037]

    # Create dictionary containing calendar an region info
    data_dict = create_calendar_and_region_data(seasons_to_check, list_of_regions)

    # Add avalanche information
    avalanches = get_avalanche_data(data_dict['region'], data_dict['date'])
    data_dict['avalanches'] = avalanches

    # Create dataframe for current data
    region_date_and_avalanche_df = pd.DataFrame(data_dict)

    # Create dataframe for historic avalanche forecast
    avalanche_forecast_df = get_avalanche_forecast_data(seasons_to_check)

    # Merge dataframes
    dataset = pd.merge(region_date_and_avalanche_df, avalanche_forecast_df, how='inner', on=['date', 'region'])

    # Create string containing csv data
    dataset_file_content = dataset.to_csv(index=False)

    # Fix some weird stuff happening in the data
    dataset_file_content = dataset_file_content.replace("--", "-")
    dataset_file_content = dataset_file_content.replace("|", "")

    # Write dataset to file
    f = open("dataset.csv", "w")
    f.write(dataset_file_content)
    f.close()


if __name__ == "__main__":
    main()
