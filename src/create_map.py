import json
from shapely.geometry import shape
import matplotlib.pyplot as plt
import random
from colour import Color


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
    number_of_values = 3
    forecast_region_ids = [3038, 3044, 3041, 3006, 3008, 3032, 3034, 3043, 3037, 3018, 3033, 3027, 3029, 3013, 3028, 3014, 3010, 3025, 3009, 3019, 3015, 3042, 3045, 3005, 3046, 3036, 3023, 3016, 3012, 3020, 3024, 3017, 3039, 3022, 3011, 3007, 3035, 3040, 3031, 3026, 3021, 3030]

    # Create dummy forecast map
    forecast_map = {}
    for region_id in forecast_region_ids:
        forecast_map[region_id] = random.randint(0, number_of_values - 1)

    # Create map plot
    create_map(forecast_map, 3)


if __name__ == "__main__":
    main()
