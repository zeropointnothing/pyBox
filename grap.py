"""
Make le graph
"""

# class pyGraph:
#     def __init__(self, h, w) -> None:
#         self.height = h
#         self.width = w

#     def plot_point(self, y, x, graph: list | None = None):
#         """
#         Plot a single point on a new graph or an existing one.
#         """
#         graph = [] if not graph else graph

#         for vline in range(self.height):
#             graph.append({"line": vline, "data": []})
#             for wline in range(self.width):
#                 if vline == y-1 and wline == x-1:
#                     graph[vline]["data"].append("X")
#                 else:
#                     graph[vline]["data"].append("-")

#         return graph

#     def plot_line(self, m: float, b: int):
#         """
#         Creates a (simple) graph with the given slope and y-intercept.
#         """
#         # Force the two args into their correct forms.
#         m = float(eval(m))
#         b = int(b)

#         graph = []
#         points = []

#         for  _ in range(self.height):
#             # Make a blank graph.
#             graph.append({"line": _, "data": []})

#         # Use the y=mx+b formula to calculate all even points the line crosses.
#         for x in range(self.width):
#             y = -m * x + -b

#             if round(y) == y:
#                 points.append({"y": round(y), "x": x})

#         # Creates forth quadrant of graph.
#         for i, line in enumerate(graph):
#             for wline in range(self.width):
#                 new = True
#                 for point in points:
#                     if point["x"] == wline-1 and point["y"] == i-1:
#                         line["data"].append("X ")
#                         new = False
#                 if new:
#                     line["data"].append("- ")

#         graph[0]["data"][0] = "* "
        
#         return graph




# gr = pyGraph(40, 40)

# minp = input("Enter Slope (m): ")
# binp = input("Enter Y-Intercept (b): ")

# grph = gr.plot_line(minp, binp)

# output = ""

# for _ in grph:
#     output += f"{''.join(_['data'])}\n"

# print(output)


# # m = 1/4
# # b = 4

# # x = 4

# # y = m*x+b

# # print(y)

class Graph:
    """
    Background class. Don't touch.
    """
    def __init__(self, height: int, width: int) -> None:
        self.grp = []
        oy = round((height-1)/2) + 1
        ox = round((width-1)/2) + 1

        self.origin = (ox, oy)

        # output = ""

        if width%2 == 0 or height%2 == 0:
            raise ValueError("Width and height must be odd!")

        self.height = height
        self.width = width

        for i in range(self.height):
            # Make a blank graph.
            self.grp.append({"line": i, "data": []})
            for _ in range(self.width):
                self.grp[i]["data"].append("- ")

        # for _ in self.grp:
        #     output += f"{''.join(_['data'])}\n"
        # print(output)

    def add_point(self, x: int, y: int, text: str):
        """
        Add a point, calculating its position based on the origin.
        """
        orix, oriy = self.origin

        try:
            if self.grp[oriy-1-y]["data"][orix-1+x] != "- ":
                text = "# "

            self.grp[oriy-1-y]["data"][orix-1+x] = text
        except IndexError:
            # This point can't be shown on the graph.
            return


class GraphiPy:
    """
    grap

    i can make the graphs lets go.
    """
    def __init__(self, height: int, width: int) -> None:
        self.graph = Graph(height, width)

    def plot_point(self, x, y):
        """
        Create a (basic) graph and/or add a single point to it.
        """
        self.graph.add_point(x, y, "X ")

        return self.graph.grp

    def plot_line(self, slope: str, yintercept: int):
        """
        Create a (basic) graph and/or plot a line using y=mx+b.
        """
        tmpwidth = int((self.graph.width-1)/2)
        points = []
        slope = float(eval(slope))
        yintercept = int(yintercept)

        for x in range(-tmpwidth, tmpwidth+1):
            y = slope * x + yintercept
            # Make sure we are only trying to plot numbers that we can even see.
            if round(y) == y and y < self.graph.height/2:
                points.append({"y": round(y), "x": x})

        print(points)

        for point in points:
            self.graph.add_point(point["x"], point["y"], "X ")

        # Add the origin.
        self.graph.add_point(0, 0, "* ")

        return self.graph.grp

grapher = GraphiPy(21, 21)

while True:
    uslope = input("Enter slope (m): ")
    uinter = input("Enter y-intercept (b): ")

    print(grapher.graph.origin)
    result = grapher.plot_line(uslope, uinter)

    output = ""
    for _ in result:
        output += f"{''.join(_['data'])}\n"
    print(output)

# m = 2/1
# b = 0

# points = []

# width = 11

# tmpwidth = int((width-1)/2)

# for x in range(-tmpwidth, tmpwidth):
#     y = -m * x + -b

#     if round(y) == y:
#         points.append({"y": round(y), "x": x})


# print(points)