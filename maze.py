import heapq


class Node:

    def __init__(self, position, parent=None, cost=0):
        self.position = position
        self.cost = cost
        self.parent = parent

    def __lt__(self, node):
        return node

    def __eq__(self, node):
        return node == self.position

    def __hash__(self):
        return hash(self.position)


class Maze():

    def __init__(self, maze):
        self.maze = maze
        self.begin = self.findStart(maze)
        self.end = self.findEnd(maze)
        self.height = len(maze)
        self.width = len(maze[0])

    def findStart(self, maze):
        for y, arr in enumerate(maze):
            for x, ch in enumerate(arr):
                if ch == "S":
                    return Node((x, y))

    def findEnd(self, maze):
        for y, arr in enumerate(maze):
            for x, ch in enumerate(arr):
                if ch == "E":
                    return Node((x, y))

    def solve(self):
        open = []
        visited = set()

        heapq.heappush(open, (self.begin.cost, self.begin))

        while open:
            cost, node = heapq.heappop(open)

            if node.position == self.end.position:
                path = []
                while node:
                    path.append(node.position)
                    node = node.parent

                return (path[::1], visited)

            visited.add(node)

            for neighbor in self.getNeighbors(node):
                if neighbor in visited:
                    continue

                newCost = node.cost + 1

                if neighbor not in open:
                    heapq.heappush(open, (newCost + self.h(neighbor), neighbor))

                elif newCost < neighbor.cost:
                    neighbor.cost = newCost
                    neighbor.parent = node
        raise Exception("No Solution Found")

    def h(self, node: Node):
        x, y = node.position
        x2, y2 = self.end.position
        return abs(x - x2) + abs(y - y2)

    def getNeighbors(self, node):
        x, y = node.position
        neighbors = []
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            newX, newY = x + dx, y + dy
            if self.height > newY and self.width > newX:
                if not (self.maze[newY][newX] == "#"):
                    n = Node((newX, newY), parent=node, cost=node.cost + 1)
                    neighbors.append(n)
        return neighbors


def replace(s, newStr, index):
    s = s[:index] + newStr + s[index + 1:]
    return s


def main():
    m = []
    m.append("##########E#")
    m.append("#          #")
    m.append("#   ########")
    m.append("#          #")
    m.append("#          #")
    m.append("#          #")
    m.append("#          #")
    m.append("#          #")
    m.append("########   #")
    m.append("#          #")
    m.append("#     #### #")
    m.append("#          #")
    m.append("#          #")
    m.append("#          #")
    m.append("#S##########")

    maze = Maze(m)
    path, visited = maze.solve()

    for x, y in path:
        m[y] = replace(m[y], "*", x)
    steps = len(path)
    print("Steps: " + str(steps))
    print("Total Steps: " + str(len(visited)))
    for arr in m:
        print(arr)


if __name__ == "__main__":
    main()
