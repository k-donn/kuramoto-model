"""
An animation of synchronization of sine functions.

usage: python3.8 graph.py [-h] [-d] K

positional arguments:
  K            Coupling constant for the sine functions

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Show the plot instead of writing to a file

"""

# TODO
# Add legend for current vs. unchanged lines
# Move main() initialization to init_anim()

import argparse
import math
from operator import itemgetter
from typing import Callable, List, TypedDict

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplot_fmt_pi import MultiplePi
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator

X_LIM: float = 8 * math.pi


class FuncLine(TypedDict):
    """A dict representing a line being animated."""

    line: Line2D
    phase: float
    coefficient: float
    data: List[float]


def format_plt() -> None:
    """Change any global style params."""
    mpl.rcParams["font.family"] = "Poppins"
    plt.style.use("ggplot")


def format_axes(axes: Axes, k_const: float) -> None:
    """Adjust the sizing of the plot's axes.

    Parameters
    ----------
    axes : `Axes`
        The axes object describing the plot's axes

    k_const : `float`
        The coupling constant of the sine functions

    """
    axes.set_xlim(0, X_LIM)
    axes.set_ylim(-1.05, 1.05)

    axes.set_title("Synchronization of sine functions")

    axes.set_xlabel("X Values")
    axes.set_ylabel("Y Values")

    axes.text(X_LIM - math.pi * 2, 0.9, f"Coupling: K={k_const}")

    maj_manager = MultiplePi(denominator=1)
    min_manager = MultiplePi(denominator=3)

    x_axis = axes.get_xaxis()
    y_axis = axes.get_yaxis()

    x_axis.set_major_locator(maj_manager.locator())

    x_axis.set_minor_locator(min_manager.locator())

    x_axis.set_major_formatter(maj_manager.formatter())

    y_maj_locator = MultipleLocator(0.5)
    y_axis.set_major_locator(y_maj_locator)


def sum_of_phase_diffs(target_index: int, lines: List[FuncLine]) -> float:
    """Calculate value needed for coupling of sine functions.

    Return the sum of the sines of the differences between all other elements
    and the target element.

    Parameters
    ----------
    target_index : `int`
        The index of the line to be compared against the others

    lines : `List[FuncLine]`
        The list of all lines

    Returns
    -------
    `float`
        The sum of the sines of the differences between
        all other elements and the target element

    """
    res = 0
    target_value = lines[target_index]["phase"]
    for i, line in enumerate(lines):
        if i != target_index:
            res += math.sin(line["phase"] - target_value)
    return res


def copy_lines(lines: List[FuncLine]) -> List[FuncLine]:
    """Create a list of lines that don't change phase.

    Returns
    -------
    `List[FuncLine]`
        The list of non-phase changing lines

    """
    res: List[FuncLine] = []
    for line in lines:
        res.append(
            {"line": plt.plot([], [], "o", markersize=0.8, animated=True,
                              color=line["line"].get_color(), zorder=1)[0],
             "phase": line["phase"], "coefficient": line["coefficient"], "data": []})
    return res


def init_anim() -> List:
    """Initialize the animation."""
    return []


def animate(
        frame: float, xdata: List[float],
        lines: List[FuncLine],
        orig_lines: List[FuncLine],
        k_const: float) -> List[Line2D]:
    """Redraw all artists on the plot.

    Parameters
    ----------
    frame : `float`
        The current frame number

    xdata : `List[float]`
        The current list of all x-values

    lines : `List[FuncLine]`
        The list representing the functions being plotted,
        their past y-values, and line objects describing the artists

    k_const : `float`
        The coupling constant of the sine functions

    Returns
    -------
    `List[Line2D]`
        The line artists needed for blitting

    """
    xdata.append(frame)

    for i, line in enumerate(lines):
        line["phase"] = line["phase"] + k_const * \
            sum_of_phase_diffs(i, lines)
        line["data"].append(
            math.sin((line["coefficient"] * frame) + line["phase"]))
        line["line"].set_data(xdata, line["data"])

    for orig_line in orig_lines:
        orig_line["data"].append(
            math.sin((orig_line["coefficient"] * frame) + orig_line["phase"]))
        orig_line["line"].set_data(xdata, orig_line["data"])

    return list(map(itemgetter("line"), lines)) + \
        list(map(itemgetter("line"), orig_lines))


def main() -> None:
    """Run all executable code."""
    format_plt()

    fig: Figure = plt.figure(figsize=(16, 9), dpi=120)
    axes: Axes = fig.add_subplot(111)
    parser = argparse.ArgumentParser(
        prog="python3.8 graph.py", description="An animation of synchronization of sine functions.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Show the plot instead of writing to a file")
    parser.add_argument("coupling", metavar="K", type=float,
                        help="Coupling constant for the sine functions")

    args = parser.parse_args()

    k_const: float = args.coupling

    format_axes(axes, k_const)

    xdata: List[float] = []

    lines: List[FuncLine] = []
    lines.append({"line": plt.plot([], [], lw=2, animated=True, color="r")[0],
                  "phase": 0, "coefficient": 1, "data": []})
    lines.append({"line": plt.plot([], [], lw=2, animated=True, color="g")[0],
                  "phase": math.pi / 2, "coefficient": 1, "data": []})
    lines.append({"line": plt.plot([], [], lw=2, animated=True, color="b")[0],
                  "phase": 0.75 * math.pi, "coefficient": 1, "data": []})

    writer = FFMpegWriter(fps=40, bitrate=250000,
                          extra_args=["-minrate", "650k", "-maxrate", "1M"])

    frames = np.linspace(0, X_LIM, 512)

    orig_lines = copy_lines(lines)

    anim = FuncAnimation(fig, animate, init_func=init_anim, frames=frames,
                         interval=25, repeat=False, blit=True,
                         fargs=(xdata, lines, orig_lines, k_const))

    if args.debug:
        plt.show()
    else:
        anim.save(f"recordings/kuramoto-model.mp4", writer=writer)


if __name__ == "__main__":
    main()
