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


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # print("\n")
    # print(names, "\n")
    # print(people, "\n")
    # print(movies, "\n")
    # print("\n")


    # TODO

    # Complete the implementation of the shortest_path function such that 
    # it returns the shortest path from the person with id source to the person with the id target.

    # Assuming there is a path from the source to the target, your function should return a list, 
    # where each list item is the next (movie_id, person_id) pair in the path from the source to the target. 
    # Each pair should be a tuple of two strings.
        # For example, if the return value of shortest_path were [(1, 2), (3, 4)], 
        # that would mean that the source starred in movie 1 with person 2, person 2 
        # starred in movie 3 with person 4, and person 4 is the target.

    # If there are multiple paths of minimum length from the source to the target, your function can return any of them.

    # If there is no possible path between two actors, your function should return None.

    # You may call the neighbors_for_person function, which accepts a person’s id as input, 
    # and returns a set of (movie_id, person_id) pairs for all people who starred in a movie with a given person.


    # raise NotImplementedError
    return


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
