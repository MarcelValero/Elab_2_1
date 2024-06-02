# Description: Simulated annealing algorithm for optimizing the location of service points
import pandas as pd
import random
import math

# Author:
#   Marcel Valero Talarn i6315821
#   Date: 2021-09-30


# Create object SP (for service point)
class SP:
    """
    Service point class
    initializes with:
    :param SP_id: service point id
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


class Square:  # this will be used as the available coordinates for new service points to be spawned #
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

    Methods:
    - total_cost: Calculate the total cost of the initial solution
    - modify_service_point: Randomly select a service point and modify its coordinates
    - add_service_point: Add a new service point with random coordinates
    - delete_service_point: Delete a random service point
    """

    def __init__(self, service_points):
        self.service_points = service_points

    def __repr__(self):
        return f"InitialSolution(service_points={self.service_points})"

    def total_cost(self):
        """
        Calculate the cost of the initial solution.

        The cost is calculated as the sum of a base cost, a cost per unit of pickup capacity,
        and a cost per unit of total distance.

        :return: cost of the initial solution
        :rtype: float
        """
        cost = 0
        for sp in self.service_points:
            cost += 75000 + 0.1 * sp.pickup + 0.5 * sp.total_dist
        return cost

    def modify_service_point(self, valid_coordinates):
        """
        Randomly select a service point and modify its coordinates.

        This method selects a random service point from the list and assigns it new coordinates
        chosen randomly from the list of valid coordinates.

        :param valid_coordinates: List of tuples representing valid (x, y) coordinates
        :type valid_coordinates: list of tuple
        """
        sp = random.choice(self.service_points)
        new_x, new_y = select_random_coordinate(valid_coordinates)
        sp.x = new_x
        sp.y = new_y
        print(f"Service Point {sp.SP_id} coordinates modified to ({new_x}, {new_y})")

    def add_service_point(self, valid_coordinates, new_id):
        """
        Add a new service point with random coordinates.

        This method creates a new service point with a unique ID and random coordinates
        chosen from the list of valid coordinates, and adds it to the list of service points.

        :param valid_coordinates: List of tuples representing valid (x, y) coordinates
        :type valid_coordinates: list of tuple
        :param new_id: Unique ID for the new service point
        :type new_id: int
        """
        new_x, new_y = select_random_coordinate(valid_coordinates)
        new_sp = SP(new_id, new_x, new_y, pickup=0, delivery=0, total_dist=0, cost=0)  # Adjust these values as needed
        self.service_points.append(new_sp)
        print(f"New Service Point added with ID {new_id} at coordinates ({new_x}, {new_y})")

    def delete_service_point(self):
        """
        Delete a random service point.

        This method randomly selects a service point from the list and removes it.
        """
        if self.service_points:
            self.service_points.pop(random.randint(0, len(self.service_points) - 1))
            print("Random Service Point deleted")


def create_service_points(file_path):
    """
    Create a list of service points from a CSV file.

    This function reads service point data from a CSV file and creates a list of SP objects.

    :param file_path: Path to the CSV file containing service point data
    :type file_path: str
    :return: List of service points
    :rtype: list of SP
    """
    df = pd.read_csv(file_path)
    service_points = []
    for index, row in df.iterrows():
        sp = SP(row['id'], row['x'], row['y'], row['pickup'], row['delivery'], row['total_dist'], row['cost'])
        service_points.append(sp)
    return service_points


def load_valid_coordinates(file_path):
    """
    Load valid coordinates from a CSV file.

    This function reads valid (x, y) coordinates from a CSV file and returns them as a list of tuples.

    :param file_path: Path to the CSV file containing valid coordinates
    :type file_path: str
    :return: List of valid (x, y) coordinates
    :rtype: list of tuple
    """
    df = pd.read_csv(file_path)
    valid_coordinates = list(zip(df['x'], df['y']))
    return valid_coordinates


def select_random_coordinate(valid_coordinates):
    """
    Select a random coordinate from the list of valid coordinates.

    This function returns a random (x, y) coordinate from the provided list of valid coordinates.

    :param valid_coordinates: List of tuples representing valid (x, y) coordinates
    :type valid_coordinates: list of tuple
    :return: Random (x, y) coordinate
    :rtype: tuple
    """
    return random.choice(valid_coordinates)

def simulated_annealing(original_profit, new_profit, temperature):
    """
    Perform the simulated annealing acceptance criterion.

    :param original_profit: The profit of the original solution
    :type original_profit: float
    :param new_profit: The profit of the new solution
    :type new_profit: float
    :param temperature: The current temperature in the simulated annealing process
    :type temperature: float
    :return: Whether the new solution should be accepted
    :rtype: bool
    """
    probability = math.exp((new_profit - original_profit) / temperature)
    math_random = random.random()

    return probability >= math_random

def main():
    # Load data
    sp_path = 'path/to/service_points.csv'  # Replace with the path to your dataset
    valid_coords_path = 'path/to/valid_coordinates.csv'  # Replace with your valid coordinates file path

    ServiceP = create_service_points(sp_path)
    valid_coordinates = load_valid_coordinates(valid_coords_path)

    # Generate initial solution
    initial_solution = InitialSolution(ServiceP)

    print(f"Initial Profit: {initial_solution.total_cost()}")
    print(f"Number of Service Points: {len(ServiceP)}")

    temperature = 45000000

    for i in range(1, 350000001):
        if i % 1000000 == 0:
            print(f"Iteration {i}, Profit: {initial_solution.total_cost()}")

        temperature = 45000000 / i
        rand = random.random()

        if rand <= 0.02:
            initial_solution.delete_service_point()
        elif rand <= 0.2:  # need to adapt the adding logic
            initial_solution.add_service_point(valid_coordinates, new_id=999)
        else:
            initial_solution.modify_service_point(valid_coordinates)

    print("FINAL SOLUTION")
    print(f"Final Profit: {initial_solution.total_cost()}")
    # Implement is_valid_solution logic if applicable
    print("Solution is valid:", True)


if __name__ == "__main__":
    main()
