import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}
"""
names = {
    "leonardo dicaprio": {"1"},
    "kate winslet": {"2"},
    "joseph gordon-levitt": {"3"}
}
"""

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}
"""
people = {
    "1": {
        "name": "Leonardo DiCaprio",
        "birth": "1974",
        "movies": {"10", "11"}
    },
    "2": {
        "name": "Kate Winslet",
        "birth": "1975",
        "movies": {"10"}
    },
    "3": {
        "name": "Joseph Gordon-Levitt",
        "birth": "1981",
        "movies": {"11"}
    }
}
"""

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}
"""
movies = {
    "10": {
        "title": "Titanic",
        "year": "1997",
        "stars": {"1", "2"}
    },
    "11": {
        "title": "Inception",
        "year": "2010",
        "stars": {"1", "3"}
    }
}
"""


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path

        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")



# =============== MY IMPLEMENTATION =============== #

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    If no possible path, returns None.
    """

    # If source and target are the same, return an empty path
    if source == target:
        return []

    # Initialize the BFS/DFS frontier with the source node
    source_node = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(source_node)

    # Track explored states
    explored = set()

    # ==== SEARCH LOOP ==== #
    while not frontier.empty():
        # Remove a node from the frontier (FIFO behavior for BFS, FILO for DFS)
        node = frontier.remove()

        # Mark node as explored
        explored.add(node.state)

        # Expand neighbors (co-actors) — these are the people the current actor starred with
        for movie_id, neighbor_id in neighbors_for_person(node.state):


            # ==== PATH CONSTRUCTION ==== #
            # If found the target, reconstruct and return path
            if neighbor_id == target:
                return construct_path(node, movie_id, target)
            

            # If this neighbor hasn't been explored or is not in frontier, add it
            if neighbor_id not in explored and not frontier.contains_state(neighbor_id):
                child = Node(state=neighbor_id, parent=node, action=movie_id)
                frontier.add(child)

    # If no path is found, return None
    return None
    # ===================== #

def construct_path(node, movie_id, target):
    """
    Constructs and returns the path from the source to the target by backtracking through parent nodes.
    The path consists of (movie_id, person_id) pairs, where each pair represents a movie that connects
    two actors in the path.
    
    Parameters:
    - node (Node): This "final" node represents the actor that has starred with our target actor.
    - movie_id (str): The ID of the movie that connects the target actor to the "node" actor.
    - target (str): The ID of the target actor.

    Returns:
    - path (list): A list of (movie_id, person_id) pairs that represent the shortest path from the source actor
      to the target actor. The list will be in the correct order, from source to target, after the function backtracks
      and reverses the path.

    Explanation:
    - We backtrack from the target actor node to the source actor by following the parent nodes. The path is constructed
      in reverse, so we reverse it at the end before returning it.
    """
    # Initialize the path with the target and the movie that connected the target to the parent node
    path = [(movie_id, target)] # Start with the target actor and the movie that connects them
    
    # Then, backtrack through parent nodes to reconstruct the path from source to target
    while node is not None:
        # If the current node has an action (movie), add it to the path
        if node.action is not None:
            path.append((node.action, node.state)) # Add movie and actor pair to the path

        # Move to the parent node to continue backtracking
        node = node.parent

    # Reverse the path to get the correct order (from source to target)
    path.reverse()
    
    return path

# ================================================= #



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
