# BFS and Cutset Algorithm Project

## Overview

This project implements Breadth-First Search (BFS) traversal and a k-cutset detection algorithm for undirected graphs. It includes visualization tools to demonstrate how removing certain nodes can disconnect a graph.

## Files

- **`Graph.py`**: Custom graph implementation using adjacency lists with deque (doubly-linked list)
- **`cutset.py`**: Implementation of the k-cutset algorithm
- **`visualize.py`**: Graph visualization tool using matplotlib and NetworkX

## Key Questions and Answers

### 1. How much memory will the queue need, in general, for input graph with n nodes?

**Answer: O(n) memory**

In the worst case, the BFS queue will need to store **all n nodes** of the graph. This occurs when:
- The graph has a structure where one level of BFS contains most/all nodes
- Example: A star graph where the center node connects to all other nodes

The implementation uses a Python list with an index pointer to avoid the O(n) cost of `list.pop(0)`. While this approach uses O(n) space for the queue, it provides O(1) access time for dequeuing operations.

**Memory breakdown:**
- Queue list: O(n) - can store up to n nodes
- Visited set: O(n) - tracks all visited nodes
- **Total: O(n) space**

### 2. Does there exist a set of k nodes such that removing them disconnects G?

**Answer: It depends on the graph structure and the value of k**

This is exactly the question that the **k-cutset algorithm** answers. The algorithm:
- Tries all possible combinations of k nodes: C(n,k) = n!/(k!(n-k)!)
- For each combination, removes those nodes and checks if the graph becomes disconnected
- Returns **YES** if any combination disconnects the graph, **NO** otherwise

**For the example graph in this project (A-B-C-D-E-F):**
- k=1: **YES** - Removing node A disconnects the graph into 3 components
- k=2: **YES** - Removing nodes {A, B} disconnects the graph
- k=3: **YES** - Removing nodes {A, B, D} disconnects the graph

**Graph properties affecting the answer:**
- **Vertex connectivity**: The minimum number of nodes needed to disconnect the graph
- **Highly connected graphs**: Require larger k values to disconnect
- **Tree structures**: Can be disconnected by removing any single internal node (k=1)
- **Complete graphs K_n**: Require k=n-1 nodes to disconnect

### 3. How large of a graph can be reasonably run with your algorithm?

**Answer: Small to medium graphs (n ≤ 20-30 nodes) with small k values (k ≤ 3-4)**

The cutset algorithm has **exponential time complexity** due to trying all C(n,k) combinations.

**Practical limits:**

| Graph Size (n) | k | Combinations C(n,k) | Est. Runtime |
|----------------|---|---------------------|--------------|
| 10 nodes       | 2 | 45                  | < 1 second   |
| 10 nodes       | 3 | 120                 | < 1 second   |
| 15 nodes       | 3 | 455                 | < 1 second   |
| 20 nodes       | 3 | 1,140               | ~1 second    |
| 20 nodes       | 4 | 4,845               | ~5 seconds   |
| 30 nodes       | 3 | 4,060               | ~5 seconds   |
| 30 nodes       | 5 | 142,506             | ~2-3 minutes |
| 50 nodes       | 5 | 2,118,760           | ~30+ minutes |

**Factors affecting performance:**
- **Number of nodes (n)**: Affects both combinations and BFS runtime
- **k value**: Higher k = exponentially more combinations
- **Graph density (m edges)**: Denser graphs take longer in BFS
- **Early termination**: Algorithm stops after finding first cutset (helps in practice)
---

## Algorithm Analysis

### BFS Algorithm

**Purpose:** Traverse a graph starting from a given node, visiting all reachable nodes level by level.

**Implementation Details:**
- Uses a list-based queue with an index pointer (avoids O(n) pop operations)
- Tracks visited nodes using a set for O(1) lookup
- Processes each node exactly once

**Time Complexity: O(n + m)**
- n = number of nodes (vertices)
- m = number of edges
- Each node is visited once: O(n)
- Each edge is examined once (undirected graph): O(m)
- **Total: O(n + m)**

**Space Complexity: O(n)**
- Queue storage: O(n) - worst case all nodes in queue
- Visited set: O(n) - tracks all visited nodes
- Traversal order list: O(n) - stores result
- **Total: O(n)**

**Best Case:** O(n + m) - must visit all reachable nodes
**Worst Case:** O(n + m) - same as best case
**Average Case:** O(n + m)

---

### K-Cutset Algorithm

**Purpose:** Determine if there exists a set of k nodes whose removal disconnects the graph.

**Algorithm Steps:**
1. Generate all combinations of k nodes from n total nodes
2. For each combination:
   - Temporarily remove those k nodes
   - Run BFS to check if remaining graph is connected
   - If disconnected, return True (cutset found)
3. If no combination disconnects the graph, return False

**Time Complexity: O(C(n,k) × (n + m))**
- C(n,k) = n!/(k!(n-k)!) combinations to try
- Each combination requires:
  - BFS traversal: O(n + m)
  - Set operations: O(k)
- **Total: O(C(n,k) × (n + m))**

**Detailed breakdown:**
```
For k=1: O(n × (n + m)) = O(n² + nm)
For k=2: O(n²/2 × (n + m)) = O(n³ + n²m)
For k=3: O(n³/6 × (n + m)) = O(n⁴ + n³m)
```

**Space Complexity: O(n + m)**
- Graph storage: O(n + m) - adjacency lists
- BFS visited set: O(n)
- BFS queue: O(n)
- Current combination: O(k)
- **Total: O(n + m)** (dominated by graph storage)

**Best Case:** O(n + m) - first combination tried is a valid cutset
**Worst Case:** O(C(n,k) × (n + m)) - must try all combinations
**Average Case:** O(C(n,k)/2 × (n + m)) - cutset found midway

---

### Graph Visualization Algorithm

**Purpose:** Create visual representations of graphs before and after cutset removal.

**Time Complexity: O(n + m)**
- Converting to NetworkX graph: O(n + m)
- Spring layout calculation: O(n² × iterations) ≈ O(n²)
- Drawing nodes/edges: O(n + m)
- **Total: O(n²)** for layout calculation

**Space Complexity: O(n + m)**
- NetworkX graph copy: O(n + m)
- Position dictionary: O(n)
- Image buffer: O(width × height) for rendering
- **Total: O(n + m + image_size)**

---

## Complexity Summary Table

| Algorithm | Time Complexity | Space Complexity | Practical Limit |
|-----------|----------------|------------------|-----------------|
| **BFS** | O(n + m) | O(n) | Very large (n > 10,000) |
| **K-Cutset** | O(C(n,k) × (n + m)) | O(n + m) | Small (n ≤ 30, k ≤ 4) |
| **Visualization** | O(n²) | O(n + m) | Medium (n ≤ 100) |

---

## Usage

### Run BFS

```bash
python Graph.py
```

### Find Cutsets

```bash
python cutset.py
```

### Visualize Graphs

```bash
python visualize.py
```

Visualizations are saved in the `visualizations/` directory.

---

## Dependencies

- Python 3.x
- matplotlib
- networkx

Install dependencies:
```bash
pip install matplotlib networkx
```

---

## Graph Structure (Example)

The default graph has 6 nodes with the following connections:
```
    E
    |
F - D - A - B
        |
        C
```

**Edges:**
- A-B, A-C, A-D
- D-E, D-F

**Key observation:** Node A is a critical **bottleneck**. Removing it alone disconnects the graph, making it a 1-cutset.

---

## References

- Graph Theory: Diestel, R. (2017). Graph Theory. Springer.
- BFS Algorithm: Cormen et al. Introduction to Algorithms (CLRS)
- Vertex Connectivity: Graph connectivity theory and applications
