import pandas as pd
import random


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
        return f"Square(x={self.x}, y={self.y}, sp_dist={self.sp_dist}, population={self.population})"


class InitialSolution:
    """
    Initial solution class
    initializes with:
    :param service_points: list of service points
    """

    def __init__(self, service_points):
        self.service_points = service_points

    def __repr__(self):
        return f"InitialSolution(service_points={self.service_points})"

    def total_cost(self):
        """
        Calculate the cost of the initial solution
        :return: cost of the initial solution
        """
        cost = 0
        for sp in self.service_points:
            cost += 75000 + 0.1 * sp.pickup + 0.5 * sp.total_dist
        return cost

    def modify_service_point(self, valid_coordinates):
        sp = random.choice(self.service_points)
        new_x, new_y = select_random_coordinate(valid_coordinates)
        sp.x = new_x
        sp.y = new_y

    def add_service_point(self, valid_coordinates, new_id):
        new_x, new_y = select_random_coordinate(valid_coordinates)
        new_sp = SP(new_id, new_x, new_y, pickup=0, delivery=0, total_dist=0, cost=0)  # Adjust these values as needed
        self.service_points.append(new_sp)

    def delete_service_point(self):
        if self.service_points:
            self.service_points.pop(random.randint(0, len(self.service_points) - 1))


def create_service_points(file_path):
    df = pd.read_csv(file_path)
    service_points = []
    for index, row in df.iterrows():
        sp = SP(row['id'], row['x'], row['y'], row['pickup'], row['delivery'], row['total_dist'], row['cost'])
        service_points.append(sp)
    return service_points


def load_valid_coordinates(file_path):
    df = pd.read_csv(file_path)
    valid_coordinates = list(zip(df['x'], df['y']))
    return valid_coordinates


def select_random_coordinate(valid_coordinates):
    return random.choice(valid_coordinates)


# Example usage
valid_coordinates_path = 'path/to/valid_coordinates.csv'  # Replace with your valid coordinates file path
valid_coordinates = load_valid_coordinates(valid_coordinates_path)

service_points_path = 'path/to/service_points.csv'  # Replace with your service points file path
service_points = create_service_points(service_points_path)

initial_solution = InitialSolution(service_points)

# Print the created service points
print("Initial Service Points:")
for sp in service_points:
    print(sp)

# Example simulated annealing iteration (simplified)
initial_solution.modify_service_point(valid_coordinates)
print("\nAfter Modifying a Service Point:")
print(initial_solution)

initial_solution.add_service_point(valid_coordinates, new_id=999)
print("\nAfter Adding a New Service Point:")
print(initial_solution)

initial_solution.delete_service_point()
print("\nAfter Deleting a Service Point:")
print(initial_solution)

print("\nTotal Cost of Initial Solution:", initial_solution.total_cost())
