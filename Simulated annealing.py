import pandas as pd


# create object SP (for service point)
class SP:
    """
    Service point class
    initializes with:
    :param id: service point id
    :param x: x coordinate
    :param y: y coordinate
    :param pickup: service point capacity
    :param delivery: service point delivery
    :param total_dist: distance from this service point to all the people who ordered from it
    :param cost: service point cost
    """

    def __init__(self, SP_id, x, y, pickup, delivery, total_dist, cost):
        self.SP_id = SP_id
        self.x = x
        self.y = y
        self.pickup = pickup
        self.delivery = delivery
        self.total_dist = total_dist
        self.cost = cost

    def __repr__(self):
        return f"SP(id={self.SP_id}, x={self.x}, y={self.y}, pickup={self.pickup}, delivery={self.delivery}, total_dist={self.total_dist} ,cost={self.cost})"


class Square:
    """
    Square class
    initializes with:
    :param x: x coordinate
    :param y: y coordinate
    :param sp_dist: distance from this neighborhood to all the service points
    :param population: population of this neighborhood
    # future extra variables #
    """

    def __init__(self, x, y, sp_dist, population):
        self.x = x
        self.y = y
        self.sp_dist = sp_dist
        self.population = population

    def __repr__(self):
        return f"Square(x={self.x}, y={self.y}, sp_dist={self.sp_dist}), population={self.population})"


class Initial_solution:
    """
    Initial solution class
    initializes with:
    :param service_points: list of service points
    """

    def __init__(self, service_points):
        self.service_points = service_points

    def __repr__(self):
        return f"Initial_solution service_points={self.service_points})"

    def total_cost(self):
        """
        Calculate the cost of the initial solution
        :return: cost of the initial solution
        """
        cost = 0

        for SP in self.service_points:
            cost += 75000 + 0.1 * SP.pickup + 0.5 * SP.total_dist
        return cost


# Read the dataset
def create_service_points(file_path):
    df = pd.read_csv(file_path)

    service_points = []
    for index, row in df.iterrows():
        sp = SP(row['id'], row['x'], row['y'], row['pickup'], row['delivery'], row['cost'])
        service_points.append(sp)

    return service_points


# Example usage:
file_path = 'path/to/your/dataset.csv'  # Replace with the path to your dataset
service_points = create_service_points(file_path)

# Print the created service points
for sp in service_points:
    print(sp)
