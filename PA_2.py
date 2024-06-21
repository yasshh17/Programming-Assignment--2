import heapq
import sys

class Edge:
    def __init__(self, destination, weight):
        self.destination = destination
        self.weight = weight

class Vertex:
    def __init__(self):
        self.edges = []

def shortest_cycle_length(graph):
    shortest_cycle = float('inf')

    for source in graph:
        distance = {vertex: float('inf') for vertex in graph}
        distance[source] = 0
        queue = [(0, source)]

        while queue:
            current_distance, current = heapq.heappop(queue)

            for edge in graph[current].edges:
                next_vertex = edge.destination
                new_distance = current_distance + edge.weight

                if next_vertex == source and current != source and new_distance < shortest_cycle:
                    shortest_cycle = new_distance
                elif new_distance < distance[next_vertex]:
                    distance[next_vertex] = new_distance
                    heapq.heappush(queue, (new_distance, next_vertex))

    return 0 if shortest_cycle == float('inf') else shortest_cycle

def main(input_file):
    graph = {}

    try:
        with open(input_file, 'r') as file:
            # Check if the file is empty
            if file.read().strip() == '':
                print("Error: Input file is empty")
                return
            # Reset file pointer to beginning
            file.seek(0)

            for line_num, line in enumerate(file, start=1):
                parts = line.strip().split(":")
                if len(parts) != 2:
                    print(f"Error: Invalid input format at line {line_num}")
                    return
                source = int(parts[0])

                vertex = graph.setdefault(source, Vertex())

                edges = parts[1].strip().split()
                if len(edges) % 2 != 0:
                    print(f"Error: Invalid input format at line {line_num}")
                    return
                for i in range(0, len(edges), 2):
                    try:
                        destination = int(edges[i])
                        weight = int(edges[i + 1])

                        # Error handling for negative edge weights
                        if weight < 0:
                            print(f"Error: Negative edge weights are not allowed at line {line_num}")
                            return

                        # Error handling for self-loops
                        if destination == source:
                            print(f"Error: Self-loops are not allowed at line {line_num}")
                            return

                        # Add destination vertex if not already present in the graph
                        graph.setdefault(destination, Vertex())

                    except (IndexError, ValueError):
                        print(f"Error: Invalid input format at line {line_num}")
                        return

                    vertex.edges.append(Edge(destination, weight))
    except FileNotFoundError:
        print("Error: Input file not found")
        return

    shortest_cycle_length1 = shortest_cycle_length(graph)

    if shortest_cycle_length1 == 0:
        print("The length of the shortest cycle is: 0, since the graph is acyclic.")
    else:
        print(f"The length of the shortest cycle is: {shortest_cycle_length1}")
if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--input':
        print("Usage: script.py --input <input_file>")
        sys.exit(1)

    input_file = sys.argv[2]
    main(input_file)
