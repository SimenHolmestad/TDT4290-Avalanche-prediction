import pandas as pd

def Reduce(attributes):
    df = pd.read_csv('dataset.csv')
    for a in attributes:
        df.drop(a, inplace=True, axis=1)

    df.to_csv("reduced_data.csv", index = False)


