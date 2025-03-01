# CS50AI | Lecture 0 - Search | Project 0A - `degrees`

This project is a mandatory assignment from **CS50AI – Lecture 0: "Search"**.

### 📌 Usage

To run the project locally, follow these steps:

1. **Clone the repository** to your local machine.
2. **Navigate to the project directory**:  
   ```sh
   cd path/to/degrees
   ```
3. **Run the script in the terminal** 
   ```sh
   python3 degrees.py [optional: large/small]
   ```
3. **Enter the names** of the source / target actors when prompted. 

3. **Wait for results** – the shortest connection path will be displayed. 

<br>


## Table of Contents

1. **[Introduction](#introduction)**

2. **[Terminology](#terminology)**
    - [Agent](#agent)
    - [State](#state)
    - [Transition Model](#transition-model)
    - [Actions](#actions)
    - [State Space](#state-space)
    - [Goal Test](#goal-test)
    - [Path Cost](#path-cost)
    - [Optimal Solution](#optimal-solution)

3. **[Technical Overview](#technical-overview)**
    - [`util.py`](#utilpy)
    - [`degrees.py`](#degreespy)

4. **[Algorithm Logic and Agent Perception](#algorithm-logic-and-agent-perception)**


<br>

## Introduction
This project is a practical implementation of depth-first search (DFS) and breadth-first search (BFS) algorithms, aiming to explore the fundamental components of artificial intelligence (AI) programs, including the environment, agents, frontier, nodes, actions, and goal-testing mechanisms. The goal is to demonstrate how AI can be used to solve search problems, focusing on determining the degrees of separation between two actors in a movie database.

In this project, the agent's task is to find the shortest path (in terms of movie collaborations) between two actors. The agent does so by searching for movies they have co-starred in, and by using search algorithms like BFS and DFS, it explores different connections between actors. The search process aims to uncover the fewest number of steps, or "degrees," needed to link one actor to another through their shared movie roles.

The movie database is structured around three key entities: actors, movies, and the relationships between them (which actors starred in which movies). Users can search for actors by name, load the movie database, and find the shortest path between two actors. By leveraging BFS and DFS algorithms, the program demonstrates how search can be applied to real-world datasets.

<br>

## Terminology

#### **Agent** 
Definition: An agent is an entity that perceives its environment and acts upon that environment to achieve a goal. 

    E.g. In a navigator app, the agent would be a representation of a car that needs to decide on which actions to take to arrive at the destination. 
    
    In this project, the agent represents an actor (the current actor currently being explored) searching for a connection to another actor (our target). It explores movies they’ve starred in and chooses co-stars as possible paths, aiming to reach the target actor in the shortest way. If Actor Alpha starred in a movie with Actor Beta, and Actor Beta starred in a different movie with Actor Gamma, the path from Actor Alpha to Actor Gamma goes through Actor Beta.

To understand what an agent is, we should understand what an agent is NOT:

__An agent is NOT the entire algorithm.__
- The entire algorithm is the search process (e.g., BFS or DFS), which systematically explores different paths to find the shortest connection between two actors.
- The agent only makes local decisions at each step (e.g., choosing which actor to explore next).
- An agent perceives its environment by gathering information about the current state of the world. In your project, this happens through data structures and function calls that allow the agent to "see" the actors and movies around it.

__An agent is NOT the environment (the world it operates in).__
- The environment in this project is the network of actors and movies, where actors are connected if they have starred in the same movie.
- The agent navigates this environment by selecting connections (movies) that lead to other actors.

__An agent is NOT the goal.__
- The goal is to find the shortest path between two actors.
- The agent works toward achieving this goal by making decisions about which actor to explore next.

<br>

#### **State** 
A state represents the **current condition or configuration** of an agent in its environment at a specific moment. It's essentially a snapshot of the agent's position or situation, based on the information it has perceived up to that point.

    E.g. In a 15 puzzle game, a state is any arrangement of the numbered tiles on the puzzle board. 
    
    In the context of this project, where the agent is an actor searching for a connection to another actor, the state is the current actor (represented by their person_id). Each actor is part of the search process, and their state tells the agent where it is in the movie network.

- **Initial State:** The state from which the search algorithm starts. In a navigator app, that would be the current location. The initial state in this project is the actor where the search begins, typically the source actor (the actor you want to find the connection from).

#### **Transition Model**

The transition model tells us **what happens** when the agent performs an action in a certain state. It defines the next state the agent will be in, based on the current state and the action it took.

More formally, a transition model describes the relationship between states and actions —specifically, how performing an action in a given state leads to a new state. It helps us understand how the agent moves from one state to another based on the actions it takes.

The transition model is often represented as a function:

`Results(state, action) -> new_state`

    E.g. In this project, the transition model is implicitly defined by how the agent transitions from one actor (state) to another via movies (actions). It can be described as a function that takes the current actor (state) and a movie (action), and outputs the next actor (new state).


#### **Actions**

Actions are the possible choices or moves that an agent can make when it's in a particular state. In other words, actions define **the agent's options** at any given moment based on its current state.

More precisely, actions can be modeled as a function:

`ACTIONS(state)`: This function takes a state as input (e.g., a specific actor) and returns a set of actions that can be executed in that state. The actions represent all the valid moves the agent can make from that state.

    E.g. In this project, the state is the current actor (person_id), and the actions are the movies that the actor starred in. For each actor, the set of valid actions consists of all the movies they were part of. By choosing one of these movies, the agent moves to another actor.



#### **State Space** 

The state space is the **set of all possible states** that can be reached from the initial state through any sequence of actions. It represents all the potential configurations the agent can encounter as it navigates its environment, starting from the initial state and taking different actions along the way.

For this project, the state space consists of all the actors (represented by person_ids) that can be reached from the initial actor by following a sequence of movies (actions). Each actor can be thought of as a state, and the movies (actions) connecting actors form the paths between the states.

The state space can be visualized as a directed graph, where:
- States (nodes) represent the actors.
- Actions (arrows) represent the movies that connect actors.



#### **Goal Test**

The goal test is the condition that determines whether the agent has reached its desired state or not. It checks if the agent’s current state meets the criteria for success.

In this project, the goal test would be whether the agent (actor) has successfully connected with the target actor. 

    E.g. The goal is to connect two actors. So, the goal test checks if the current actor in the agent’s state is the target actor. If the agent's current actor is the same as the target actor, the search is complete and the agent has found the connection.
    
    If the agent has not reached the target actor, the agent continues searching by exploring other possible actors connected by movies until the goal test is met.



#### **Path Cost**
Path cost refers to the numerical value or cost associated with a sequence of actions (in this case, the movies the agent selects). The agent tries to find **the least costly path to the goal**, which may be based on criteria like the number of actions (movies) taken or any other defined measure of cost.

In thid project, the path cost could be defined as the number of movies the agent follows to connect two actors. The goal is to minimize this number to find the shortest path from the initial actor to the target actor.

**Optimal Solution**:
An optimal solution is the best possible solution to a problem, according to a defined criterion or measure, such as the lowest cost, shortest path, or quickest time. In the context of search algorithms, an optimal solution means finding the path or series of actions that best satisfies the goal while minimizing the associated cost or maximizing the desired outcome.

**Example from This Project**

Suppose you are trying to connect Demi Moore to Tom Hanks.

- **Path 1 (non-optimal)**: Demi Moore → Whoopi Goldberg → Tom Hanks (2 movies)
- **Path 2 (optimal)**: Demi Moore → Tom Hanks (1 movie)

In this case, Path 2 would be the optimal solution because it takes fewer steps (1 movie) to connect Demi Moore and Tom Hanks, compared to Path 1, which involves 2 movies.

<br>
<br>

## Technical Overview

### `util.py`

The `util.py` file contains essential **utility classes** used for implementing the search algorithms in this project. It defines key data structures that help represent the search space and manage the exploration process efficiently.

<br>

#### Class `Node()`:
The `Node` class is used to represent a single actor in the search space. It holds the details of the current state (actor's database id), the parent node (previous actor's node), and the action (movie) that links the current actor to the parent actor.

If we think about the structure of the `Node` class:

```Python
class Node:
    def __init__(self, state, parent, action):
        self.state = state        # The actor (person_id)
        self.parent = parent      # The previous node (actor)
        self.action = action      # The movie that connects them
```

* `state` is an actor (person_id).
* `parent` is the previous actor (person_id).
* `action` is the movie_id that connects the parent and child actors.


In classical search algorithms, action typically represents the action taken to move from one state to another (e.g., "move left," "move up," etc.).

In this problem:

- States = Actors (people in the dataset, represented by person_id).
- Actions = The movies that connect two actors. 
    - _Since an actor transitions to another actor through a movie, the movie is the action that caused the transition._

<br>


#### Class `StackFrontier()`:
The StackFrontier class is a data structure that represents the frontier of a search algorithm (specifically a stack-based frontier). It follows the LIFO (Last In, First Out) principle, where the most recently added node is processed first.

```Python
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
```

- add(node): Adds a node to the frontier.
- contains_state(state): Checks if the frontier contains a node with a given state.

    The method `contains_state(self, state)` checks whether the frontier (the list of nodes in the search algorithm) contains a node whose state matches the given state. Here’s a breakdown of what’s happening:

    - `state`: This is the value we are looking for in the frontier. It's an identifier for an actor (person_id) in the search algorithm.

    - `self.frontier`: This is the list that stores the nodes. Each node represents an actor, and the frontier is a collection of nodes that have been discovered but not yet explored.

    - `any(...)`: The any() function returns True if at least one element in the iterable evaluates to True. In this case, the iterable is the expression inside the parentheses, which is a generator expression that checks each node in the frontier.

    - `node.state == state`: This checks whether the state (actor's ID) of the current node in the frontier matches the state we're searching for.

    - __The result__: The `any()` function will return `True` if there is any node in the frontier whose state matches the given state, and `False` otherwise.

    In Simple Terms
    - This method checks if a specific actor (identified by state) is already present in the frontier.
    - It does this by looping through all the nodes in the frontier and checking if the actor (the state) of any node matches the one we’re looking for.

- empty(): Checks if the frontier is empty.
- remove(): Removes the most recent node added (i.e., the last node) and returns it.

The `StackFrontier` is used for __depth-first search (DFS)__, where nodes are explored by going as deep as possible before backtracking.

#### Example

Suppose the frontier contains the following nodes:

```Python
frontier = [
    Node(state="1", parent=None, action=None),
    Node(state="2", parent=None, action=None),
    Node(state="3", parent=None, action=None),
]
```

And we call:

```Python
contains_state("2")
```

This will return `True` because there is a node with `state == "2"` in the frontier.

<br>

#### Class `QueueFrontier()` (Subclass of `StackFrontier`)

The `QueueFrontier` class is a variation of `StackFrontier`, but it follows the **FIFO** (First In, First Out) principle, meaning that nodes are processed in the order they are added, making it suitable for breadth-first search (BFS).

```Python
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
```
* `remove()`: Removes the first node added to the frontier (i.e., the earliest node) and returns it.

This class enables breadth-first search (BFS), where the first node added is explored first.

<br>
<br>

### `Degrees.py`

Technical Overview of `degrees.py`

#### 1. `main()` Function:
This is the beginning of our program. That's the first function that is called.

- The program first checks the command-line arguments. If there are more than two arguments, it exits with an error message. If there's one argument, it uses it as the directory to load data from CSV files; otherwise, it defaults to the "large" directory.
- It prints "Loading data..." and then calls `load_data(directory)` to load data from CSV files into memory. After the data is loaded, it prints "Data loaded."
- The program then prompts the user to input two names. It attempts to find the corresponding person IDs using `person_id_for_name(name)`. If any of the names can't be found, the program exits.
- Once both IDs are found, it calls `shortest_path(source, target)` to find the shortest path between the two people in terms of movie collaborations.
- If a path is found, it prints the number of degrees of separation and details of each step in the path (which movie two people starred in). If no path is found, it prints "Not connected."

#### 2. `load_data(directory)` Function:
The function populates the `people`, `movies`, and `names` dictionaries by reading from the respective CSV files.

- `people`: Maps person IDs to a dictionary containing the person’s name, birth year, and the set of movies they starred in.

    ```Python
    people = {
        "1": {
            "name": "Leonardo DiCaprio",
            "birth": "1974",
            "movies": {"10456", "11456"}
        },
        "2": {
            "name": "Kate Winslet",
            "birth": "1975",
            "movies": {"10456"}
        },
        "3": {
            "name": "Joseph Gordon-Levitt",
            "birth": "1981",
            "movies": {"11456"}
        }
    }
    ```

- `movies`: Maps movie IDs to a dictionary containing the movie title, year, and the set of person IDs (stars).

    ```Python
    movies = {
        "10456": {
            "title": "Titanic",
            "year": "1997",
            "stars": {"1", "2"}
        },
        "11456": {
            "title": "Inception",
            "year": "2010",
            "stars": {"1", "3"}
        }
    }
    ```

- `names`: Maps a person's name (lowercased) to a set of person IDs, allowing quick lookups.

    ```Python
    names = {
    "leonardo dicaprio": {"1"},
    "kate winslet": {"2"},
    "joseph gordon-levitt": {"3"}
    } 
    ```

#### 3. `shortest_path(source, target)` Function:

This is the search algorithm of our program.

- This function finds the shortest path between two people using breadth-first search (BFS).
- If the source and target are the same, it returns an empty list.
- It initializes the BFS frontier with the source person and starts exploring neighbors (people who starred with the current person).
- For each neighbor, it checks if it is the target. If it is, it calls `construct_path(node, movie_id, target)` to reconstruct and return the path.
- If a neighbor hasn't been explored yet, it adds it to the frontier to explore further.
- If no path is found, it returns `None`.

<br> 

**UTIL FUNCTIONS:**

#### 4. `construct_path(node, movie_id, target)` Function:
This is a (custom) util function that is used inside the `shortest_path(source, target)` Function.

- Constructs the shortest path from the source to the target by backtracking from the target through the parent nodes.
- It starts with the target and backtracks, collecting the movie ID and person ID pairs.
- Once the entire path is backtracked, it reverses the path (since it was built in reverse order) and returns it.

#### 5. `person_id_for_name(name)` Function:
- Resolves a person's name to their corresponding IMDB ID.
- It handles ambiguities by listing all matching people if there are multiple entries for the same name.
- If there are multiple people with the same name, it asks the user to choose the correct one.

#### 6. `neighbors_for_person(person_id)` Function:
- Returns all (movie_id, person_id) pairs for people who starred in the same movies as the given person.
- It looks up the movies the person has starred in and gathers all other actors from those movies, creating a set of (movie_id, person_id) pairs.

#### Execution Flow:
- When the script is run, it starts with `main()`.
- `main()` loads the data, takes input for two people, and calls `shortest_path` to find the shortest connection.
- The `shortest_path` function uses BFS (or DFS if configured) to explore co-actors and find the shortest path between the two people.
- If a path is found, `construct_path` is used to trace the path back from the target to the source, and the path is printed.

<br>
<br>
<br>


## Algorithm Logic and Agent Perception

### How Does the Agent Perceive Its Environment?

An agent perceives its environment by gathering information about the current state of the world. In our project, this happens through data structures and function calls that allow the agent to "see" the actors and movies around it.

#### 1. The Agent's "Vision" (What It Can See)

At any point in the search, the agent is focused on a specific actor (`person_id`). It perceives its environment by:

- Looking at the movies that the current actor has starred in (`people[actor]["movies"]`).
- Looking at other actors who have also starred in those movies (`movies[movie]["stars"]`).

#### 2. The Perception Process (How It Gathers Information)

When the agent is at a specific actor, it calls:

`neighbors_for_person(person_id)`

While there isn't a single function named "transition model" in your code, the transition happens within the process of exploring actors and movies.  The relevant function that captures the transition behavior is `neighbors_for_person(person_id)`.

This function tells the agent:

- Which **movies** the current actor has appeared in.
- Which **other actors** starred in those same movies.

So, if the agent is at Actor X, it can "see" all other actors who have shared a movie with Actor X.

This function essentially models the transitions between states (actors) based on the movies they starred in together.


#### 3. What the Agent Does With This Information

The agent processes this information and decides which actor to explore next.

- If an actor has already been explored, it ignores them.
- If an actor is the target, the search stops.
- Otherwise, the agent moves forward by adding new actors to the search frontier.

**Transition Model in Your Project**

The transition model is described by which actor (state) the agent can move to, based on which movie (action) the agent chooses to explore.

- State: The current actor (e.g., "Demi Moore").
- Action: A movie (e.g., "A Few Good Men").
- New State: The new actor that co-starred in the chosen movie (e.g., "Tom Hanks").

In this sense, the transition from one actor to another is controlled by the movie the agent picks from the list of movies that the current actor starred in.
