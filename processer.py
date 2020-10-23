from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def Process():
    df = pd.read_csv('dataset.csv')
    data_list = []
    dates = []

    # Loops thorough the dataframe and change the strings in "Vindstyrke" with numbers. Adds the dates in a list 'dates'.
    for i in df.index:
        dates.append(df["date"][i])
        df["Vindstyrke"] = df.replace(
            {"Vindstyrke": {"Frisk bris": 0,
                            "Bris": 1,
                            "Sterk kuling": 2,
                            "Storm": 3,
                            "Liten storm": 4,
                            "Stiv kuling": 5,
                            "Stille/svak vind": 6,
                            "Liten kuling": 7}})

    # Makes the list into a set so it only is one of each of the dates.
    set_date = set(dates)

    # The date in the dataframe is changed with the month
    for i in set_date:
        df["date"] = df["date"].replace(i, int(i[5:7]))

    # Loops thourgh the dataframe and the values is appended in a list of lists. Every list is a row.
    for ind in df.index:
        data_list.append([df["date"][ind], df["weekday"][ind], df["weekend"][ind], df["red_day"][ind], df["avalanche"][ind], df["DangerLevel"][ind],
                          df["CloudCoverId"][ind], df["Nedbor"][ind], df["Vindstyrke"][ind], df["Temperatur_min"][ind], df["Temperatur_max"][ind],
                          df["AvalProbabilityId_0"][ind], df["AvalCauseId_0"][ind], df["DestructiveSizeId_0"][ind], df["AvalTriggerSimpleId_0"][ind],
                          df["AvalProbabilityId_3"][ind], df["AvalCauseId_3"][ind], df["DestructiveSizeId_3"][ind], df["AvalTriggerSimpleId_3"][ind],
                          df["AvalProbabilityId_5"][ind], df["AvalCauseId_5"][ind], df["DestructiveSizeId_5"][ind], df["AvalTriggerSimpleId_5"][ind],
                          df["AvalProbabilityId_7"][ind], df["AvalCauseId_7"][ind], df["DestructiveSizeId_7"][ind], df["AvalTriggerSimpleId_7"][ind],
                          df["AvalProbabilityId_10"][ind], df["AvalCauseId_10"][ind], df["DestructiveSizeId_10"][ind], df["AvalTriggerSimpleId_10"][ind],
                          df["AvalProbabilityId_30"][ind], df["AvalCauseId_30"][ind], df["DestructiveSizeId_30"][ind], df["AvalTriggerSimpleId_30"][ind],
                          df["AvalProbabilityId_45"][ind], df["AvalCauseId_45"][ind], df["DestructiveSizeId_45"][ind], df["AvalTriggerSimpleId_45"][ind],
                          df["AvalProbabilityId_50"][ind], df["AvalCauseId_50"][ind], df["DestructiveSizeId_50"][ind], df["AvalTriggerSimpleId_50"][ind]])
    
    # Process the list with data to values between 0-1
    scaler = MinMaxScaler()
    scaler.fit(data_list)
    processed_data = scaler.transform(data_list)

    # Makes the processed data to a dataframe
    df_processed_data = pd.DataFrame(processed_data)
    df_processed_data.columns = ['date', 'weekday', 'weekend', 'red_day', 'avalanche', 'danger_level', 'cloud_cover_id', 'nedbor', 'vind_styrke',
                                 'temperatur_min', 'temperatur_max', 'aval_probability_id_0', 'aval_cause_id_0', 'destructive_size_id_0', 'aval_trigger_simple_id_0',
                                 'aval_probability_id_3', 'aval_cause_id_3', 'destructive_size_id_3', 'aval_trigger_simple_id_3', 'aval_probability_id_5', 'aval_cause_id_5',
                                 'destructive_size_id_5', 'aval_trigger_simple_id_5', 'aval_probability_id_7', 'aval_cause_id_7', 'destructive_size_id_7',
                                 'aval_trigger_simple_id_7', 'aval_probability_id_10', 'aval_cause_id_10', 'destructive_size_id_10', 'aval_trigger_simple_id_10',
                                 'aval_probability_id_30', 'aval_cause_id_30', 'destructive_size_id_30', 'aval_trigger_simple_id_30', 'aval_probability_id_45',
                                 'aval_cause_id_45', 'destructive_size_id_45', 'aval_trigger_simple_id_45', 'aval_probability_id_50', 'aval_cause_id_50',
                                 'destructive_size_id_50', 'aval_trigger_simple_id_50']

    # Makes a csv file of the processed data.
    df_processed_data.to_csv("processed_data.csv", index=False)


if __name__ == "__main__":
    Process()
