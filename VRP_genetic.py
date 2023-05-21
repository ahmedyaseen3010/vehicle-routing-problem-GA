import random
import math

# Define the problem parameters
num_customers = 20
num_vehicles = 5
depot = (0, 0)
customer_positions = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_customers)]

# Define the genetic algorithm parameters
population_size = 50
num_generations = 100
mutation_rate = 0.1

# Define the fitness function
def fitness(route):
    """
    Calculates the fitness of a route, which is the total distance traveled.
    Assumes that the route starts and ends at the depot.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        from_index = route[i]
        to_index = route[i + 1]
        dist = distance(customer_positions[from_index], customer_positions[to_index])
        total_distance += dist
    return total_distance

# Define the initial population
def create_individual():
    """
    Creates a random individual, which is a solution to the vehicle routing problem.
    Assumes that the first and last node in the route is the depot.
    """
    individual = [0] # start at the depot
    vehicle_routes = [[] for _ in range(num_vehicles)]
    for customer_index in range(1, num_customers):
        vehicle_index = random.randint(0, num_vehicles - 1)
        if sum(len(route) for route in vehicle_routes) + len(vehicle_routes[vehicle_index]) + 1 <= num_customers:
            vehicle_routes[vehicle_index].append(customer_index)
        else:
            individual += [0] + vehicle_routes[vehicle_index] + [0] # end the route at the depot
            vehicle_routes[vehicle_index] = [customer_index]
    individual += [0] + [c for route in vehicle_routes for c in route] + [0] # end the route at the depot
    return individual

# Define the distance function
def distance(node1, node2):
    """
    Calculates the Euclidean distance between two nodes.
    Assumes that the nodes are represented as (x, y) tuples.
    """
    x1, y1 = node1
    x2, y2 = node2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Create the initial population
population = [create_individual() for _ in range(population_size)]

# Run the genetic algorithm
for generation in range(num_generations):
    # Evaluate the fitness of each individual
    fitnesses = [fitness(individual) for individual in population]

    # Select the fittest individuals to be parents
    parents = [population[i] for i in sorted(range(len(fitnesses)), key=lambda i: fitnesses[i])[:population_size // 2]]

    # Print the best solution of the current generation
    best_solution = min(population, key=fitness)
    print(f"Generation {generation}: {best_solution}, fitness={fitness(best_solution)}")

    # Create the next generation by crossover and mutation
    offspring = []
    for i in range(population_size // 2):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        crossover_point = random.randint(1, len(parent1) - 2)
        child1 = parent1[:crossover_point] + [c for c in parent2 if c not in parent1[:crossover_point]]
        child2 = parent2[:crossover_point] + [c for c in parent1 if c not in parent2[:crossover_point]]
        if random.random() < mutation_rate:
            mutation_point1 = random.randint(1, len(child1) - 2)
            mutation_point2 = random.randint(1, len(child2) - 2)
            child1[mutation_point1], child1[mutation_point2] = child1[mutation_point2], child1[mutation_point1]
            child2[mutation_point1], child2[mutation_point2] = child2[mutation_point2], child2[mutation_point1]
        offspring += [child1, child2]

    # Replace the old population with the new generation
    population = parents + offspring


# Select the fittest individual as the solution to the problem
best_individual = min(population, key=lambda individual: fitness(individual))
solution = best_individual[1:-1] # remove the depot indices from the solution

best_solution = min(population, key=fitness)
print(f"\nbest Solution found at Generation {generation}: {best_solution}, fitness={fitness(best_solution)}")


coordinates = [depot] + [customer_positions[i] for i in solution] + [depot]
print("Coordinates:", coordinates)


