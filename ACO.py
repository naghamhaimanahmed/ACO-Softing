import random
import math

# Define the distance matrix
distance_matrix = [
    [0, 2, 3, 4],
    [2, 0, 6, 7],
    [3, 6, 0, 5],
    [4, 7, 5, 0]
]

# Define the parameters
num_ants = 5
num_iterations = 10
alpha = 1.0
beta = 2.0
rho = 0.5
q0 = 0.8

# Initialize pheromone matrix
num_cities = len(distance_matrix)
pheromone_matrix = [[1.0] * num_cities for _ in range(num_cities)]

# Define the ACO algorithm
def ant_colony_optimization():
    best_solution = None
    best_distance = float('inf')

    for iteration in range(num_iterations):
        # Initialize ant paths
        ant_paths = [[] for _ in range(num_ants)]

        # Construct ant paths
        for ant in range(num_ants):
            current_city = random.randint(0, num_cities - 1)
            ant_paths[ant].append(current_city)

            for _ in range(num_cities - 1):
                probabilities = calculate_probabilities(ant_paths[ant], current_city)
                next_city = choose_next_city(probabilities, q0)
                ant_paths[ant].append(next_city)
                current_city = next_city

        # Update pheromone matrix
        update_pheromone(ant_paths)

        # Find the best solution in the current iteration
        iteration_best_solution, iteration_best_distance = find_best_solution(ant_paths)
        if iteration_best_distance < best_distance:
            best_solution = iteration_best_solution
            best_distance = iteration_best_distance

    return best_solution, best_distance

# Calculate the probabilities for the next city selection
def calculate_probabilities(path, current_city):
    probabilities = []
    total = 0.0

    for city in range(num_cities):
        if city not in path:
            pheromone = pheromone_matrix[current_city][city]
            distance = distance_matrix[current_city][city]
            probability = math.pow(pheromone, alpha) * math.pow(1.0 / distance, beta)
            probabilities.append((city, probability))
            total += probability

    probabilities = [(city, probability / total) for city, probability in probabilities]
    return probabilities

# Choose the next city based on probabilities and q0 parameter
def choose_next_city(probabilities, q0):
    if random.uniform(0, 1) <= q0:
        max_probability = max(probabilities, key=lambda x: x[1])
        return max_probability[0]
    else:
        cumulative_probabilities = []
        cumulative_probability = 0.0
        for city, probability in probabilities:
            cumulative_probability += probability
            cumulative_probabilities.append((city, cumulative_probability))

        random_value = random.uniform(0, 1)
        for city, cumulative_probability in cumulative_probabilities:
            if random_value <= cumulative_probability:
                return city

# Update the pheromone matrix
def update_pheromone(ant_paths):
    for i in range(num_cities):
        for j in range(num_cities):
            pheromone_matrix[i][j] *= (1 - rho)

    for ant_path in ant_paths:
        ant_distance = calculate_distance(ant_path)
        for i in range(num_cities - 1):
            current_city = ant_path[i]
            next_city = ant_path[i+1]
            pheromone_matrix[current_city][next_city] += 1.0 / ant_distance

# Calculate the total distance of a path
def calculate_distance(path):
    total_distance = 0.0
    for i in range(len(path) - 1):
        current_city = path[i]
        next_city = path[i+1]
        total_distance += distance_matrix[current_city][next_city]
    return total_distance

# Find the best solution and its distance among all ant paths
def find_best_solution(ant_paths):
    best_solution = None
    best_distance = float('inf')

    for path in ant_paths:
        distance = calculate_distance(path)
        if distance < best_distance:
            best_solution = path
            best_distance = distance

    return best_solution, best_distance

# Run the ACO algorithm
best_solution, best_distance = ant_colony_optimization()

# Print the best solution and its distance
print("Best solution:", best_solution)
print("Best distance:", best_distance)