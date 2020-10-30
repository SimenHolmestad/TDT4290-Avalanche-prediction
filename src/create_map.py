import json
from shapely.geometry import shape
import matplotlib.pyplot as plt
from colour import Color
import pandas as pd
from tensorflow import keras


region_name_dict = {
    3003: "Nordenskiöld Land",
    3006: "Finnmarkskysten",
    3007: "Vest-Finnmark",
    3009: "Nord-Troms",
    3010: "Lyngen",
    3011: "Tromsø",
    3012: "Sør-Troms",
    3013: "Indre Troms",
    3014: "Lofoten og Vesterålen",
    3015: "Ofoten",
    3016: "Salten",
    3017: "Svartisen",
    3022: "Trollheimen",
    3023: "Romsdal",
    3024: "Sunnmøre",
    3027: "Indre Fjordane",
    3028: "Jotunheimen",
    3029: "Indre Sogn",
    3031: "Voss",
    3032: "Hallingdal",
    3034: "Hardanger",
    3035: "Vest-Telemark",
    3037: "Heiane",
    3001: "Svalbard øst",
    3002: "Svalbard vest",
    3004: "Svalbard sør",
    3005: "Øst-Finnmark",
    3008: "Finnmarksvidda",
    3018: "Helgeland",
    3019: "Nord-Trøndelag",
    3020: "Sør-Trøndelag",
    3021: "Ytre Nordmøre",
    3025: "Nord-Gudbrandsdalen",
    3026: "Ytre Fjordane",
    3030: "Ytre Sogn",
    3033: "Hordalandskysten",
    3036: "Rogalandskysten",
    3038: "Agder sør",
    3039: "Telemark sør",
    3040: "Vestfold",
    3041: "Buskerud sør",
    3042: "Oppland sør",
    3043: "Hedmark",
    3044: "Akershus",
    3045: "Oslo",
    3046: "Østfold"
}


def create_map(forecast_map, number_of_values, plot_filename):
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

    plt.savefig("../plots/" + plot_filename, dpi=300)
    plt.clf()
    print("Map plot saved to plot folder")


def create_map_and_statistics_for_mock_data_file(filename, model):
    file_path = "../resources/" + filename
    dummy_df = pd.read_csv(file_path)

    region_data_df = dummy_df.copy()
    region_data_df.drop("avalanche", axis=1, inplace=True)
    region_data_df.drop("region", axis=1, inplace=True)
    region_data_list = list(region_data_df.to_numpy())

    for i in range(len(region_data_list)):
        region_data_list[i] = [float(value) for value in region_data_list[i]]
    model_predictions = []
    for region_data in region_data_list:
        prediction = model.predict([region_data])[0][0]
        model_predictions.append(round(prediction, 2))

    region_ids = dummy_df["region"]

    # Create map plot
    percentage_model_predictions = [int(prediction * 100) for prediction in model_predictions]
    lowest_value = min(percentage_model_predictions)
    highest_value = max(percentage_model_predictions)

    number_of_values = highest_value - lowest_value
    relative_predictions = [x - lowest_value for x in percentage_model_predictions]
    forecast_map = dict(zip(region_ids, relative_predictions))

    # Create dataframe containing model predictions for regions
    region_name_list = []
    for region_id in region_ids:
        region_name = region_name_dict[region_id]
        region_name_list.append(region_name)

    df = pd.DataFrame({
        "region_id": region_ids,
        "region_name": region_name_list,
        "model_prediction": model_predictions
    })

    print("Predictions for file {}:".format(file_path))
    print(df)

    plt.title("Relative values for model predictions\n" + "for file \"{}\"".format(filename))
    plot_filename = "map_for_" + filename.split(".")[0] + ".png"
    print("Saving map to plots/" + plot_filename)
    create_map(forecast_map, number_of_values + 1, plot_filename)


def main():
    model = keras.models.load_model('../resources/model.tf')
    filenames = ["input_mock_data_1_of_march.csv",
                 "input_mock_data_16_of_january.csv"]

    for filename in filenames:
        create_map_and_statistics_for_mock_data_file(filename, model)


if __name__ == "__main__":
    main()
