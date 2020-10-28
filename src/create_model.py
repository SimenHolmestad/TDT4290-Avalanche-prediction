import time
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np


def main():
    # Read and shuffle dataset
    print("Reading and shuffeling dataset")
    df = pd.read_csv("../data/balanced_dataset.csv").sample(frac=1)

    # Initialize hyperparameters
    HIDDEN_LAYER_SIZE = 25
    OUTPUT_NODES = 2

    # Start timer (for measuring total running time)
    start_time = time.time()

    # Split data into train set, test set and validation set
    train_df, test_df = train_test_split(df, test_size=0.2)
    train_df, validation_df = train_test_split(train_df, test_size=0.1)

    # Convert training-, test- and validation-data to numpy arrays of correct form
    x_training_data = train_df.loc[:, train_df.columns != "avalanche"].to_numpy()
    y_training_data = np.array([(x, abs(x - 1)) for x in train_df["avalanche"]])

    x_testing_data = test_df.loc[:, test_df.columns != "avalanche"].to_numpy()
    y_testing_data = np.array([(x, abs(x - 1)) for x in test_df["avalanche"]])

    x_validation_data = validation_df.loc[:, validation_df.columns != "avalanche"].to_numpy()
    y_validation_data = np.array([(x, abs(x - 1)) for x in validation_df["avalanche"]])

    # Create the model
    model = tf.keras.Sequential([
        # tf.keras.layers.Dense is basically implementing: output = activation(dot(input, weight) + bias)
        # it takes several arguments, but the most important ones for us are the hidden_layer_size and the activation function
        tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 1st hidden layer
        tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 2nd hidden layer
        tf.keras.layers.Dense(HIDDEN_LAYER_SIZE, activation='relu'),  # 3nd hidden layer
        # The final layer is no different, we just make sure to activate it with softmax
        tf.keras.layers.Dense(OUTPUT_NODES, activation='softmax')  # Output layer
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Loss function is chosen to consider the target output 0/1 as one-hot encoding.
    batch_size = 100
    max_epochs = 100

    # Set an early stopping mechanism
    # Let's set patience=2, to be a bit tolerant against random validation loss increases
    early_stopping = tf.keras.callbacks.EarlyStopping(patience=4)

    # Fit the model
    # Note that this time the train, validation and test data are not iterable
    model.fit(x_training_data,  # Train inputs
              y_training_data,  # Train targets
              batch_size=batch_size,  # Batch size
              epochs=max_epochs,  # Epochs that we will train for (assuming early stopping doesn't kick in)

              # Callbacks are functions called by a task when a task is completed
              # Task here is to check if val_loss is increasing
              callbacks=[early_stopping],  # Early stopping
              validation_data=(x_validation_data, y_validation_data),  # Validation data
              verbose=2  # Making sure we get enough information about the training process
              )

    # Print how the model looks
    print(model.summary())

    # Test the model on test set
    results = model.evaluate(x_testing_data, y_testing_data)
    print('test loss, test acc:', results)

    # Print total running time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed_time: " + str(round(elapsed_time, 2)) + " seconds")

    # Save model
    model_filename = "../resources/model.tf"
    print("Saving model to", model_filename)
    model.save(model_filename)


if __name__ == "__main__":
    main()
