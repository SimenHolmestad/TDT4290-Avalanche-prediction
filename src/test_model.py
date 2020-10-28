import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras


def test_model_on_dataset(model):
    df = pd.read_csv("../data/balanced_dataset.csv")

    # Get rows on right format
    rows = list(df.loc[:, df.columns != "avalanche"].to_numpy())
    for i in range(len(rows)):
        rows[i] = [float(value) for value in rows[i]]

    # Get labels (true values)
    labels = df["avalanche"]

    prediction_values_for_avalanche = []
    prediction_values_for_not_avalanche = []

    for i in range(len(rows)):
        prediction = model.predict([rows[i]])[0]

        # Round numbers
        prediction = [round(prediction[0], 2), round(prediction[1], 2)]
        prediction_value = prediction[0]

        print("True avalanche value: ", labels[i], "- prediction =", prediction, end="")

        failed_value = round(abs(labels[i] - prediction[0]), 2)

        print(", failed by", failed_value)

        if (labels[i] == 1.0):
            prediction_values_for_avalanche.append(prediction_value)
        else:
            prediction_values_for_not_avalanche.append(prediction_value)

    mean_prediction_value_for_avalanche = sum(prediction_values_for_avalanche) / len(prediction_values_for_avalanche)
    mean_prediction_value_for_not_avalanche = sum(prediction_values_for_not_avalanche) / len(prediction_values_for_not_avalanche)

    print("Mean prediction value for avalanche:", mean_prediction_value_for_avalanche)
    print("Mean prediction value for not avalanche:", mean_prediction_value_for_not_avalanche)

    # Plot prediction values for avalanche
    prediction_values_for_avalanche = [round(x, 2) for x in prediction_values_for_avalanche]
    unique, counts = np.unique(prediction_values_for_avalanche, return_counts=True)

    plt.plot(unique, counts)
    plt.title("Distribution of probabilities for forecast where avalanche happened")
    plt.xlabel("Probabilities")
    plt.ylabel("Number of forecasts")
    plt.xlim(0, 1)
    plt.savefig("../plots/probabilities_where_avalanche.png", dpi=300)
    plt.clf()

    # Plot prediction values for not avalanche
    prediction_values_for_not_avalanche = [round(x, 2) for x in prediction_values_for_not_avalanche]
    unique, counts = np.unique(prediction_values_for_not_avalanche, return_counts=True)

    plt.plot(unique, counts)
    plt.title("Distribution of probabilities for forecast where avalanches did not happen")
    plt.xlabel("Probabilities")
    plt.ylabel("Number of forecasts")
    plt.xlim(0, 1)
    plt.savefig("../plots/probabilities_where_not_avalanche.png", dpi=300)
    plt.clf()
    print("Plots were saved to the plot folder")


def main():
    print("Loading model...")
    model = keras.models.load_model('../resources/model.tf')
    print("Testing_model:")
    test_model_on_dataset(model)


if __name__ == "__main__":
    main()
