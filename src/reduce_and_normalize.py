from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def Process():
    df = pd.read_csv('../data/dataset.csv')
    data_list = []
    dates = []

    # Adds the dates in a list 'dates'.
    for i in df.index:
        dates.append(df["date"][i])

    # Makes the list into a set so it only is one of each of the dates.
    set_date = set(dates)

    # The date in the dataframe is changed with the month
    for i in set_date:
        df["date"] = df["date"].replace(i, int(i[5:7]))

    df["month"] = df["date"]
    df["month"] = df["month"].replace(12, 0)

    # Change the strings in "Vindstyrke" with numbers.
    df["Vindstyrke"] = df["Vindstyrke"].replace("Stille/svak vind", 0)
    df["Vindstyrke"] = df["Vindstyrke"].replace("Bris", 1)
    df["Vindstyrke"] = df["Vindstyrke"].replace("Frisk bris", 2)
    df["Vindstyrke"] = df["Vindstyrke"].replace("Liten kuling", 3)
    df["Vindstyrke"] = df["Vindstyrke"].replace("Stiv kuling", 4)
    df["Vindstyrke"] = df["Vindstyrke"].replace("Sterk kuling", 5)
    df["Vindstyrke"] = df["Vindstyrke"].replace("Liten storm", 6)
    df["Vindstyrke"] = df["Vindstyrke"].replace("Storm", 7)

    # New columns with average temperature
    temp_mean = df.loc[:, ["Temperatur_min", "Temperatur_max"]]
    df['Temperatur_mean'] = temp_mean.mean(axis=1)

    # Binary encode month-category
    month_1 = []
    month_2 = []
    month_3 = []

    for ind in df.index:
        binary = bin(df["month"][ind]).format(3)

        if df["month"][ind] == 0:
            binary = "000"
        if df["month"][ind] == 1:
            binary = "001"
        if df["month"][ind] == 2:
            binary = "010"
        if df["month"][ind] == 3:
            binary = "011"
        month_1.append(binary[-3])
        month_2.append(binary[-2])
        month_3.append(binary[-1])

    df["month_1"] = month_1
    df["month_2"] = month_2
    df["month_3"] = month_3

    # Add day_off of weekend or red_day
    day_off = []
    for ind in df.index:
        if df["weekend"][ind] == 1 or df["red_day"][ind] == 1:
            day_off.append(1)
        else:
            day_off.append(0)
    df["day_off"] = day_off

    # Loops through the dataframe and the values is appended in a list of lists. Every list is a row.
    for ind in df.index:
        data_list.append(
            [df["month_1"][ind],
             df["month_2"][ind],
             df["month_3"][ind],
             df["day_off"][ind],
             df["avalanche"][ind],
             df["DangerLevel"][ind],
             df["Nedbor"][ind],
             df["Vindstyrke"][ind],
             df["Temperatur_mean"][ind],
             df["AvalProbabilityId_0"][ind],
             df["AvalProbabilityId_3"][ind],
             df["AvalProbabilityId_5"][ind],
             df["AvalProbabilityId_7"][ind],
             df["AvalProbabilityId_10"][ind],
             df["AvalProbabilityId_30"][ind],
             df["AvalProbabilityId_45"][ind],
             df["AvalProbabilityId_50"][ind]])

    # Process the list with data to values between 0-1
    scaler = MinMaxScaler()
    scaler.fit(data_list)
    processed_data = scaler.transform(data_list)

    # Makes the processed data to a dataframe
    df_processed_data = pd.DataFrame(processed_data)

    df_processed_data.columns = ['month_1', 'month_2', 'month_3',
                                 'day_off', 'avalanche', 'danger_level', 'nedbor',
                                 'vind_styrke', 'temperatur_mean', 'aval_probability_id_0',
                                 'aval_probability_id_3', 'aval_probability_id_5',
                                 'aval_probability_id_7', 'aval_probability_id_10',
                                 'aval_probability_id_30', 'aval_probability_id_45',
                                 'aval_probability_id_50']

    # Makes a csv file of the processed data
    df_processed_data.to_csv("../data/processed_data.csv", index=False)


if __name__ == "__main__":
    Process()
