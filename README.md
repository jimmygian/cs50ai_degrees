# SEARCH ALGORITHMS and degrees.py exercise

## Introduction
Search problems involve an agent that is given an initial state and a goal state, and it returns a solution of how to get from the former to the latter. This project explores this concept.

The goal of this project is to use an agent to determine the degrees of separation between two actors by finding the movies they have co-starred in. The project uses search algorithms such as BFS (Breadth-First Search) and DFS (Depth-First Search) to find the shortest(?) path connecting two actors through a series of movies.

The database consists of three main entities: actors (people), movies, and their associations (which actors starred in which movies). The project allows users to search for actors by name, load a movie database, and find the shortest path connecting two actors.


## Terminology

#### **Agent:** 
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

<br>

#### **State Space** 

The state space is the **set of all possible states** that can be reached from the initial state through any sequence of actions. It represents all the potential configurations the agent can encounter as it navigates its environment, starting from the initial state and taking different actions along the way.

For this project, the state space consists of all the actors (represented by person_ids) that can be reached from the initial actor by following a sequence of movies (actions). Each actor can be thought of as a state, and the movies (actions) connecting actors form the paths between the states.

The state space can be visualized as a directed graph, where:
- States (nodes) represent the actors.
- Actions (arrows) represent the movies that connect actors.


<br>

#### **Goal Test**

The goal test is the condition that determines whether the agent has reached its desired state or not. It checks if the agent’s current state meets the criteria for success.

In this project, the goal test would be whether the agent (actor) has successfully connected with the target actor. 

    E.g. The goal is to connect two actors. So, the goal test checks if the current actor in the agent’s state is the target actor. If the agent's current actor is the same as the target actor, the search is complete and the agent has found the connection.
    
    If the agent has not reached the target actor, the agent continues searching by exploring other possible actors connected by movies until the goal test is met.

<br>
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


## `util.py`

The `util.py` file contains essential **utility classes** used for implementing the search algorithms in this project. It defines key data structures that help represent the search space and manage the exploration process efficiently.

### Class `Node()`:
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


### Class `StackFrontier()`:
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

### Example

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

## Class `QueueFrontier()` (Subclass of `StackFrontier`)

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


## Explaining the algorithm's logic

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

**Transition Model in Your Project**
The transition model is described by which actor (state) the agent can move to, based on which movie (action) the agent chooses to explore.

- State: The current actor (e.g., "Demi Moore").
- Action: A movie (e.g., "A Few Good Men").
- New State: The new actor that co-starred in the chosen movie (e.g., "Tom Hanks").

In this sense, the transition from one actor to another is controlled by the movie the agent picks from the list of movies that the current actor starred in.

#### 3. What the Agent Does With This Information

The agent processes this information and decides which actor to explore next.

- If an actor has already been explored, it ignores them.
- If an actor is the target, the search stops.
- Otherwise, the agent moves forward by adding new actors to the search frontier.