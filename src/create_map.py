import json
from shapely.geometry import shape
import matplotlib.pyplot as plt
from colour import Color
import pandas as pd
from tensorflow import keras


def create_map(forecast_map, number_of_values):
    """Creates a map plot containing all avalanche regions with a redness
    scale representing danger.

    Input is a dictionary containing region_ids as keys and
    danger_values as values. If there are some regions that are not
    presented in the dictionary, these will have the lowest
    danger_value (white).

    Args:
        forecaset_map (dict[int, int]): Dictionary with values of the form {forecast_region_id: danger_value}
        number_of_values (int): The maximum possible value for danger_value in the dictionary
    """

    with open('../resources/forecast_areas.json') as f:
        json_map_data = json.load(f)

    forecast_region_shapes = {}

    for feature in json_map_data['features']:
        forecast_region_shape = shape(feature['geometry'])
        forecast_region_id = feature["properties"]["omradeID"]
        forecast_region_shapes[forecast_region_id] = forecast_region_shape

    # Create color values
    start_color = Color("white")
    end_color = Color("red")
    colors = list(start_color.range_to(end_color, number_of_values))

    for region_id, region_shape in forecast_region_shapes.items():
        if (region_id in forecast_map):
            forecast = forecast_map[region_id]
            color = colors[forecast]
        else:
            color = colors[0]

        x, y = region_shape.exterior.xy

        # Fill region with correct color
        plt.fill(x, y, color.get_hex())

        # Print outline of region
        plt.plot(x, y, "k")

    plt.savefig("../plots/map.png", dpi=300)


def main():
    dummy_df = pd.read_csv("../resources/input_mock_data.csv")

    region_data_df = dummy_df.copy()
    region_data_df.drop("avalanche", axis=1, inplace=True)
    region_data_df.drop("region", axis=1, inplace=True)
    region_data_list = list(region_data_df.to_numpy())

    for i in range(len(region_data_list)):
        region_data_list[i] = [float(value) for value in region_data_list[i]]

    model = keras.models.load_model('../resources/model.tf')
    model_predictions = []
    for region_data in region_data_list:
        prediction = model.predict([region_data])[0][0]
        model_predictions.append(int(prediction * 100))

    region_ids = dummy_df["region"]

    # Create map plot
    lowest_value = min(model_predictions)
    highest_value = max(model_predictions)

    number_of_values = highest_value - lowest_value
    model_predictions = [x - lowest_value for x in model_predictions]
    forecast_map = dict(zip(region_ids, model_predictions))

    plt.title("Relative values for model predictions")

    create_map(forecast_map, number_of_values + 1)


if __name__ == "__main__":
    main()
