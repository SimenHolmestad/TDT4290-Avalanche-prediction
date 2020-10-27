import time
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt


def test_model_on_dataset(model):
    df = pd.read_csv("../data/balanced_dataset.csv")

    rows = list(df.loc[:, df.columns != "avalanche"].to_numpy())

    for i in range(len(rows)):
        rows[i] = [float(value) for value in rows[i]]

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

    print("Unique values for avalanche:", unique)
    print("Count values for avalanche:", counts)

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

    print("Unique values for not avalanche:", unique)
    print("Count values for not avalanche:", counts)

    plt.plot(unique, counts)
    plt.title("Distribution of probabilities for forecast where avalanches did not happen")
    plt.xlabel("Probabilities")
    plt.ylabel("Number of forecasts")
    plt.xlim(0, 1)
    plt.savefig("../plots/probabilities_where_not_avalanche.png", dpi=300)
    plt.clf()


print("Reading dataset")

# Read and shuffle dataset
df = pd.read_csv("../data/balanced_dataset.csv").sample(frac=1)


# Initialize hyperparameters
NUMBER_OF_FEATURES = len(df.columns) - 1
HIDDEN_LAYER_SIZE = 25
OUTPUT_NODES = 2
NUMBER_OF_EPOCHS = 10


# Start timer (for measuring total running time)
start_time = time.time()


# Split data into train set and test set
train_df, test_df = train_test_split(df, test_size=0.2)
train_df, validation_df = train_test_split(train_df, test_size=0.1)


# Convert training and test-data to normal lists
train_rows = list(train_df.loc[:, df.columns != "avalanche"].to_numpy())

for i in range(len(train_rows)):
    train_rows[i] = [float(value) for value in train_rows[i]]

test_rows = list(test_df.loc[:, df.columns != "avalanche"].to_numpy())

for i in range(len(test_rows)):
    test_rows[i] = [float(value) for value in test_rows[i]]

validation_rows = list(validation_df.loc[:, df.columns != "avalanche"].to_numpy())

for i in range(len(validation_rows)):
    validation_rows[i] = [float(value) for value in validation_rows[i]]

x_training_data = train_rows
y_training_data = [(x, abs(x - 1)) for x in train_df["avalanche"]]
x_testing_data = test_rows
y_testing_data = [(x, abs(x - 1)) for x in test_df["avalanche"]]
x_validation_data = validation_rows
y_validation_data = [(x, abs(x - 1)) for x in validation_df["avalanche"]]
model = tf.keras.Sequential([
    # tf.keras.layers.Dense is basically implementing: output = activation(dot(input, weight) + bias)
    # it takes several arguments, but the most important ones for us are the hidden_layer_size and the activation function
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 1st hidden layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 2nd hidden layer
    tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 3nd hidden layer
    # the final layer is no different, we just make sure to activate it with softmax
    tf.keras.layers.Dense(OUTPUT_NODES, activation='softmax')  # output layer
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# loss function is chosen to consider the target output 0/1 as one-hot encoding.
batch_size = 100
max_epochs = 100


# set an early stopping mechanism
# let's set patience=2, to be a bit tolerant against random validation loss increases
early_stopping = tf.keras.callbacks.EarlyStopping(patience=4)


# fit the model
# note that this time the train, validation and test data are not iterable
model.fit(x_training_data,  # train inputs
          y_training_data,  # train targets
          batch_size=batch_size,  # batch size
          epochs=max_epochs,  # epochs that we will train for (assuming early stopping doesn't kick in)

          # callbacks are functions called by a task when a task is completed
          # task here is to check if val_loss is increasing
          callbacks=[early_stopping],  # early stopping
          validation_data=(x_validation_data, y_validation_data),  # validation data
          verbose=2  # making sure we get enough information about the training process
          )
print(model.summary())

results = model.evaluate(x_testing_data, y_testing_data)

print('test loss, test acc:', results)


# Print total running time
end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed_time: " + str(round(elapsed_time, 2)) + " seconds")
print("Testing_model:")

test_model_on_dataset(model)
