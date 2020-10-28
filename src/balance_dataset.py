import pandas as pd


def main():
    df = pd.read_csv("../data/processed_data.csv")

    # Get rows with an avalanche

    avalanches = df.loc[df["avalanche"] == 1]
    not_avalanches = df.loc[df["avalanche"] == 0]

    number_of_avalanches = len(avalanches.index)
    number_of_not_avalanches = len(not_avalanches.index)

    print("Number of days with avalanches:", number_of_avalanches)
    print("Number of days without avalanches:", number_of_not_avalanches)
    print("Ratio of days with avalanches:", number_of_avalanches / len(not_avalanches))
    print()

    print("Sampling {} rows with no avalanches".format(number_of_avalanches))
    sample_of_not_avalanches = not_avalanches.sample(n=number_of_avalanches)

    new_dataset = pd.concat([avalanches, sample_of_not_avalanches])

    filename = "../data/balanced_dataset.csv"

    new_dataset.to_csv(filename, index=False)
    print("Wrote {} rows to {}".format(len(new_dataset.index), filename))


if __name__ == "__main__":
    main()
