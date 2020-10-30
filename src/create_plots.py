import pandas as pd
import numpy as np
from matplotlib import pyplot
import seaborn as sns


def make_bar_plots(dataframe):
    region_data = dataframe["region"]

    regions, counts = np.unique(region_data, return_counts=True)

    pyplot.bar(regions, counts)
    pyplot.title("Data points per region")
    pyplot.xlabel("Region ID")
    pyplot.ylabel("Data points")

    pyplot.savefig("../plots/Observations_for_region.png")

    pyplot.clf()

    ###
    # Incidents per region
    ###

    incidents_per_region = []

    for region_id in regions:
        data_for_region = dataframe[dataframe["region"] == region_id]
        incidents_per_region.append(data_for_region.sum()["avalanche"])

    pyplot.bar(regions, incidents_per_region)
    pyplot.title("Registered incidents per region Dec 2017 - now")
    pyplot.xlabel("Region ID")
    pyplot.ylabel("Registered incidents")

    pyplot.savefig("../plots/incidents_per_region.png")

    pyplot.clf()

    ###
    # Incidents per weekday
    ###

    incidents_per_weekday = []
    weekdays = [1, 2, 3, 4, 5, 6, 7]
    weekday_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    for weekday in weekdays:
        data_for_weekday = dataframe[dataframe["weekday"] == weekday]
        incidents_per_weekday.append(data_for_weekday.sum()["avalanche"])

    pyplot.bar(weekday_names, incidents_per_weekday)
    pyplot.title("Registered incidents per weekday Dec 2017 - now")
    pyplot.xlabel("Weekday")
    pyplot.ylabel("Registered incidents")

    pyplot.savefig("../plots/incidents_per_weekday.png")

    pyplot.clf()

    ###
    # Incidents per month
    ###

    incidents_per_month = []
    months = [12, 1, 2, 3, 4, 5, 6]
    month_names = ["december", "january", "february", "march", "april", "may", "june"]

    dataframe['date'] = pd.to_datetime(dataframe['date'], errors='coerce')
    for month in months:
        data_for_month = dataframe[dataframe["date"].dt.month == month]
        incidents_per_month.append(data_for_month.sum()["avalanche"])

    pyplot.bar(month_names, incidents_per_month)
    pyplot.title("Registered incidents per month Dec 2017 - now")
    pyplot.xlabel("month")
    pyplot.ylabel("Registered incidents")

    pyplot.savefig("../plots/incidents_per_month.png")

    pyplot.clf()

    ###
    # Incidents per month every year
    ###
    incidents_per_month = []
    months = [1, 2, 3, 4, 5, 6, 12]
    years = [2017, 2018, 2019, 2020]
    month_names = ["1.17", "2.17", "3.17", "4.17", "5.17", "6.17", "12.17",
                   "1.18", "2.18", "3.18", "4.18", "5.18", "6.18", "12.18",
                   "1.19", "2.19", "3.19", "4.19", "5.19", "6.19", "12.19",
                   "1.20", "2.20", "3.20", "4.20", "5.20", "6.20", "12.20"]
    dataframe['date'] = pd.to_datetime(dataframe['date'], errors='coerce')
    for year in years:
        for month in months:
            data_for_month = dataframe[(dataframe["date"].dt.month == month) & (dataframe["date"].dt.year == year)]
            incidents_per_month.append(data_for_month.sum()["avalanche"])

    pyplot.bar(month_names, incidents_per_month)
    pyplot.title("Registered incidents per month Jan 2017 - now")
    pyplot.xlabel("year and month")
    pyplot.ylabel("Registered incidents")
    pyplot.xticks(rotation=50)

    pyplot.savefig("../plots/incidents_per_month_and_year.png")

    pyplot.clf()
    ###
    # Incidents for danger level
    ###

    incidents_per_danger_level = []
    danger_levels = [1, 2, 3, 4, 5]

    for danger_level in danger_levels:
        data_for_danger_level = dataframe[dataframe["DangerLevel"] == danger_level]
        incidents_per_danger_level.append(data_for_danger_level.sum()["avalanche"])

    pyplot.bar(danger_levels, incidents_per_danger_level)
    pyplot.title("Registered incidents per danger level Dec 2017 - now")
    pyplot.xlabel("danger level")
    pyplot.ylabel("Registered incidents")

    pyplot.savefig("../plots/incidents_per_danger_level.png")

    pyplot.clf()

    ###
    # Incidents per minimum temperature
    ###

    incidents_per_min_temperature = []
    min_temperatures = [x for x in range(-30, 30)]

    for min_temperature in min_temperatures:
        data_for_min_temperature = dataframe[dataframe["Temperatur_min"] == min_temperature]
        incidents_per_min_temperature.append(data_for_min_temperature.sum()["avalanche"])

    pyplot.bar(min_temperatures, incidents_per_min_temperature)
    pyplot.title("Registered incidents per min temperature Dec 2017 - now")
    pyplot.xlabel("Temperatures")
    pyplot.ylabel("Registered incidents")

    pyplot.savefig("../plots/incidents_per_min_temperature.png")

    pyplot.clf()

    ###
    # Incidents per maximum temperature
    ###

    incidents_per_max_temperature = []
    max_temperatures = [x for x in range(-30, 30)]

    for max_temperature in max_temperatures:
        data_for_max_temperature = dataframe[dataframe["Temperatur_max"] == max_temperature]
        incidents_per_max_temperature.append(data_for_max_temperature.sum()["avalanche"])

    pyplot.bar(max_temperatures, incidents_per_max_temperature)
    pyplot.title("Registered incidents per max temperature Dec 2017 - now")
    pyplot.xlabel("Temperatures")
    pyplot.ylabel("Registered incidents")

    pyplot.savefig("../plots/incidents_per_max_temperature.png")

    pyplot.clf()

    ###
    # Incidents for cloud cover
    ###

    incidents_for_cloud_cover = []
    cloud_covers = [0, 10, 20, 30]
    cloud_cover_names = ["Ikke gitt", "Klarvær", "Delvis skyet", "Skyet"]

    for cloud_cover in cloud_covers:
        data_for_cloud_cover = dataframe[dataframe["CloudCoverId"] == cloud_cover]

        incidents_for_cloud_cover.append(data_for_cloud_cover.sum()["avalanche"])

    pyplot.bar(cloud_cover_names, incidents_for_cloud_cover)
    pyplot.title("Registered incidents for type of cloud cover Dec 2017 - now")
    pyplot.xlabel("cloud covers")
    pyplot.ylabel("Registered incidents")

    pyplot.savefig("../plots/incidents_per_cloud_cover.png")

    pyplot.clf()

    ###
    # Incidents for wind_strength
    ###

    incidents_for_wind_strength = []
    wind_strengths = ['Frisk bris', 'Bris', 'Sterk kuling', 'Storm', 'Liten storm', 'Stiv kuling', 'Stille/svak vind', 'Liten kuling']

    for wind_strength in wind_strengths:
        data_for_wind_strength = dataframe[dataframe["Vindstyrke"] == wind_strength]

        incidents_for_wind_strength.append(data_for_wind_strength.sum()["avalanche"])

    pyplot.bar(wind_strengths, incidents_for_wind_strength)
    pyplot.title("Registered incidents per wind strength Dec 2017 - now")
    pyplot.xlabel("wind strengts")
    pyplot.ylabel("Registered incidents")
    pyplot.xticks(rotation=20)

    pyplot.savefig("../plots/incidents_per_wind_strength.png")

    pyplot.clf()

    ###
    # Incidents for rainfall
    ###

    incidents_for_rainfall = []
    rainfalls = [x for x in range(50)]

    dataframe["Nedbor"] = dataframe["Nedbor"].astype(np.float64)

    for rainfall in rainfalls:
        data_for_rainfall = dataframe[dataframe["Nedbor"] == rainfall]

        incidents_for_rainfall.append(data_for_rainfall.sum()["avalanche"])

    pyplot.bar(rainfalls, incidents_for_rainfall)
    pyplot.title("Registered incidents per rainfall Dec 2017 - now")
    pyplot.xlabel("Rainfalls")
    pyplot.ylabel("Registered incidents")

    pyplot.savefig("../plots/incidents_per_rainfall.png")

    pyplot.clf()

    ###############################################################################
    #                            General distributions                            #
    ###############################################################################

    ###
    # Distribution for danger level
    ###

    distribution_of_danger_levels = []
    danger_levels = [1, 2, 3, 4, 5]

    for danger_level in danger_levels:
        data_for_danger_level = dataframe[dataframe["DangerLevel"] == danger_level]
        distribution_of_danger_levels.append(len(data_for_danger_level.index))

    pyplot.bar(danger_levels, distribution_of_danger_levels)
    pyplot.title("Distribution for danger level Dec 2017 - now")
    pyplot.xlabel("Danger level")
    pyplot.ylabel("Data points")

    pyplot.savefig("../plots/distributions_of_danger_levels.png")

    pyplot.clf()

    ###
    # Distribution for minimum temperature
    ###

    distribution_of_min_temperature = []
    min_temperatures = [x for x in range(-30, 30)]

    for min_temperature in min_temperatures:
        data_for_min_temperatures = dataframe[dataframe["Temperatur_min"] == min_temperature]
        distribution_of_min_temperature.append(len(data_for_min_temperatures.index))

    pyplot.bar(min_temperatures, distribution_of_min_temperature)
    pyplot.title("Distribution of min temperatures Dec 2017 - now")
    pyplot.xlabel("Temperatures")
    pyplot.ylabel("Data points")

    pyplot.savefig("../plots/distributions_of_min_temperatures.png")

    pyplot.clf()

    ###
    # Distribustion for maximum temperature
    ###

    distribution_of_max_temperature = []
    max_temperatures = [x for x in range(-30, 30)]

    for max_temperature in max_temperatures:
        data_for_max_temperatures = dataframe[dataframe["Temperatur_max"] == max_temperature]
        distribution_of_max_temperature.append(len(data_for_max_temperatures.index))

    pyplot.bar(max_temperatures, distribution_of_max_temperature)
    pyplot.title("Distribution of max temperature Dec 2017 - now")
    pyplot.xlabel("Temperatures")
    pyplot.ylabel("Data points")

    pyplot.savefig("../plots/distributions_of_max_temperature.png")

    pyplot.clf()

    ###
    # Incidents for cloud cover
    ###

    distribution_of_cloud_cover = []
    cloud_covers = [0, 10, 20, 30]
    cloud_cover_names = ["Ikke gitt", "Klarvær", "Delvis skyet", "Skyet"]

    for cloud_cover in cloud_covers:
        data_for_cloud_cover = dataframe[dataframe["CloudCoverId"] == cloud_cover]

        distribution_of_cloud_cover.append(len(data_for_cloud_cover.index))

    pyplot.bar(cloud_cover_names, distribution_of_cloud_cover)
    pyplot.title("Distribution of cloud covers Dec 2017 - now")
    pyplot.xlabel("cloud covers")
    pyplot.ylabel("Data points")

    pyplot.savefig("../plots/distributions_of_cloud_cover.png")

    pyplot.clf()

    ###
    # Incidents for wind_strength
    ###

    distributions_for_wind_strength = []
    wind_strengths = ['Frisk bris', 'Bris', 'Sterk kuling', 'Storm', 'Liten storm', 'Stiv kuling', 'Stille/svak vind', 'Liten kuling']

    for wind_strength in wind_strengths:
        data_for_wind_strength = dataframe[dataframe["Vindstyrke"] == wind_strength]

        distributions_for_wind_strength.append(len(data_for_wind_strength.index))

    pyplot.bar(wind_strengths, distributions_for_wind_strength)
    pyplot.title("Distribution of wind strength Dec 2017 - now")
    pyplot.xlabel("Wind strengths")
    pyplot.ylabel("Data points")
    pyplot.xticks(rotation=20)

    pyplot.savefig("../plots/distributions_of_wind_strength.png")

    pyplot.clf()

    ###
    # Incidents for rainfall
    ###

    distributions_of_rainfalls = []
    rainfalls = [x for x in range(50)]

    for rainfall in rainfalls:
        data_for_rainfall = dataframe[dataframe["Nedbor"] == rainfall]

        distributions_of_rainfalls.append(len(data_for_rainfall))

    pyplot.bar(rainfalls, distributions_of_rainfalls)
    pyplot.title("Distribution of rainfall Dec 2017 - now")
    pyplot.xlabel("Rainfalls")
    pyplot.ylabel("Data points")

    pyplot.savefig("../plots/distributions_of_rainfall.png")

    pyplot.clf()
    pyplot.close()


def create_correlation_plot(dataframe, filename):
    corr = dataframe.corr()
    sns.set(rc={'figure.figsize': (15.0, 15.0)})
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns_heatmap = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                              square=True, linewidths=.5, cbar_kws={"shrink": .5})
    figure = sns_heatmap.get_figure()
    figure.savefig(filename, dpi=200)
    pyplot.clf()


def main():
    dataframe = pd.read_csv("../data/dataset.csv")

    dataframe_without_problems = dataframe[['region', 'date', 'weekday', 'weekend', 'red_day', 'avalanche', 'DangerLevel', 'CloudCoverId', 'Nedbor', 'Vindstyrke', 'Temperatur_min', 'Temperatur_max']]

    make_bar_plots(dataframe)
    create_correlation_plot(dataframe_without_problems, "../plots/seaborn_heatmap_without_problems.png")
    create_correlation_plot(dataframe, "../plots/seaborn_heatmap.png")

    dataframe_processed_data = pd.read_csv("../data/processed_data.csv")
    create_correlation_plot(dataframe_processed_data, "../plots/seaborn_heatmap_processed_data.png")


if __name__ == "__main__":
    main()
