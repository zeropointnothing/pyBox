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

class GraphiPy:
    """
    grap

    i can make the graphs lets go.
    """
    def __init__(self, height: int, width: int) -> None:
        self.graph = self._Graph(height, width)

    class UndefinedSlopeError(BaseException):
        """
        AKA Tried to divide by zero like a stoopid error.
        """
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    class _Graph:
        """
        Internal class.
        """
        def __init__(self, height: int, width: int) -> None:
            self.grp = []
            oriy = round((height-1)/2) + 1
            orix = round((width-1)/2) + 1

            # Get the true origin of our graph by halving both the height and width.

            self.origin = (orix, oriy)

            # output = ""

            # Ensure that both the height and width are odd so that we can have a central origin.
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

        def add_point(self, xcoord: int, ycoord: int, text: str):
            """
            Add a point, calculating its position based on the origin.
            """
            orix, oriy = self.origin

            try:
                # See if we already have something here. If so, use the crossed points symbol.
                if self.grp[oriy-1-ycoord]["data"][orix-1+xcoord] != "- ":
                    text = "# "

                # Get the position by adding/subtracting the origin coords by the specified coords.
                self.grp[oriy-1-ycoord]["data"][orix-1+xcoord] = text
            except IndexError:
                # This point can't be shown on the graph.
                return

    def plot_point(self, xcoord, ycoord):
        """
        Create a (basic) graph and/or add a single point to it.
        """
        self.graph.add_point(xcoord, ycoord, "X ")

        return self.graph.grp

    def plot_slopeinter(self, slope: str, yintercept: int, exp: int = 1):
        """
        Create a (basic) graph and/or plot a line using y=mx+b.

        Exp is an optional value. Even values will always be positive.
        """
        # Split the graph in half so we can calculate negatives as well.
        tmpwidth = int((self.graph.width-1)/2)
        points = []
        # force the args to be the right type.
        try:
            slope = float(int(slope.split("/")[0]) / int(slope.split("/")[1]))
        except IndexError:
            # There was no fraction (division operator) provided. This is probably an integer.
            slope = int(slope)
        except ZeroDivisionError as exc:
            raise self.UndefinedSlopeError(f"Cannot graph an undefined slope! ({slope})") from exc

        yintercept = int(yintercept)
        exp = int(exp)

        # Use y=mx+b to calculate all our (rounded) points.
        for xpoint in range(-tmpwidth, tmpwidth+1):
            ypoint = ((slope * xpoint) ** exp) + yintercept
            # Make sure we are only trying to plot numbers that we can even see.
            if round(ypoint) == ypoint and ypoint < self.graph.height/2:
                points.append({"y": round(ypoint), "x": xpoint})

        print(points)

        # Plot all of our points.
        for point in points:
            self.graph.add_point(point["x"], point["y"], "X ")

        # Add the origin.
        self.graph.add_point(0, 0, "* ")

        return self.graph.grp

grapher = GraphiPy(21, 21)

while True:
    uslope = input("Enter slope (m): ")
    uinter = input("Enter y-intercept (b): ")
    uexp = input("exp (defaults to 1): ")

    uexp = 1 if not uexp else uexp

    print(grapher.graph.origin)
    result = grapher.plot_slopeinter(uslope, uinter, uexp)

    OUTPUT = ""
    for _ in result:
        OUTPUT += f"{''.join(_['data'])}\n"
    print(OUTPUT)

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
