# Make le graph

class pyGraph:
    def __init__(self, h, w) -> None:
        self.height = h
        self.width = w

    def plot_point(self, y, x, graph: list | None = None):
        """
        Plot a single point on a new graph or an existing one.
        """
        graph = [] if not graph else graph

        for vline in range(self.height):
            graph.append({"line": vline, "data": []})
            for wline in range(self.width):
                if vline == y-1 and wline == x-1:
                    graph[vline]["data"].append("X")
                else:
                    graph[vline]["data"].append("-")

        return graph

    def plot_line(self, m: float, b: int):
        """
        Creates a (simple) graph with the given slope and y-intercept.
        """
        # Force the two args into their correct forms.
        m = float(eval(m))
        b = int(b)

        graph = []
        points = []

        for  _ in range(self.height):
            # Make a blank graph.
            graph.append({"line": _, "data": []})

        # Use the y=mx+b formula to calculate all even points the line crosses.
        for x in range(self.width):
            y = -m * x + -b

            if round(y) == y:
                points.append({"y": round(y), "x": x})

        # Creates forth quadrant of graph.
        for i, line in enumerate(graph):
            for wline in range(self.width):
                new = True
                for point in points:
                    if point["x"] == wline-1 and point["y"] == i-1:
                        line["data"].append("X ")
                        new = False
                if new:
                    line["data"].append("- ")

        graph[0]["data"][0] = "* "
        
        return graph




gr = pyGraph(20, 20)

minp = input("Enter Slope (m): ")
binp = input("Enter Y-Intercept (b): ")

grph = gr.plot_line(minp, binp)

output = ""

for _ in grph:
    output += f"{''.join(_['data'])}\n"

print(output)


# m = 1/4
# b = 4

# x = 4

# y = m*x+b

# print(y)