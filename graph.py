"""
usage:
python graph.py
description:
An animation of synchronization of sine functions
"""

# TODO
from operator import itemgetter
from typing import Callable, Dict, List, NoReturn, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator

K_CONST = 0.006
X_LIM = 8*np.pi

FuncLine = Dict[str, Union[Line2D, int, List[float]]]


def format_pi(denominator: int) -> Callable:
    """Return a formatting function that uses the denominator provided

    Parameters
    ----------

    denominator : `int`
        The denominator in front of pi in the returned func

    Returns
    -------
    `Callable`
        The function that turns a value into a multiple of (denominator*pi)
    """
    def multiple_of_pi(value: float, _position: float) -> str:
        """Return the multiple that value is of (pi*denominator)

        Parameters
        ----------
        value : `float`
            The value to be turned into a multiple
        \_position : `float`
            The position of the value on the graph
        Returns
        -------
        `str`
            A string with the multiple joined to a pi character
        """
        res = ""
        mult = int(value/(denominator * np.pi))
        if mult == 0:
            res = "0"
        elif mult == 1:
            res = "π"
        else:
            res = f"{mult}π"
        return res
    return multiple_of_pi


def format_plt() -> NoReturn:
    """Change any global style params"""
    mpl.rcParams["font.family"] = "Poppins"
    plt.style.use("ggplot")


def format_axes(axes: Axes) -> NoReturn:
    """Adjust the sizing of the plot's axes.

    Parameters
    ----------
    axes : `Axes`
        The axes object describing the plot's axes
    """
    axes.set_xlim(0, X_LIM)
    axes.set_ylim(-1.05, 1.05)

    axes.set_title("Synchronization of sine functions")

    axes.set_xlabel("X Values")
    axes.set_ylabel("Y Values")

    axes.text(X_LIM - np.pi * 2, 0.9, f"Coupling: K={K_CONST}")

    x_axis = axes.get_xaxis()
    y_axis = axes.get_yaxis()

    x_maj_locator = MultipleLocator(np.pi)
    x_axis.set_major_locator(x_maj_locator)

    x_min_locator = MultipleLocator(np.pi / 3)
    x_axis.set_minor_locator(x_min_locator)

    x_maj_formatter = FuncFormatter(format_pi(1))
    x_axis.set_major_formatter(x_maj_formatter)

    y_maj_locator = MultipleLocator(0.5)
    y_axis.set_major_locator(y_maj_locator)


def sum_of_phase_diffs(target_index: int, lines: List[FuncLine]) -> float:
    """Return the sum of the sines of the differences between
    all other elements and the target element

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
            res += np.sin(line["phase"] - target_value)
    return res


def plot_normal_lines(lines: List[FuncLine], xdata: List[float]) -> NoReturn:
    """Plot the sine funcs as though no phase shifting occured.
    Parameters
    ----------
    lines : `List[FuncLine]`
        The original lines objects
    xdata : `List[float]`
        The x-values to be used to calculate y-values
    """
    for line in lines:
        plt.plot(xdata, np.sin((line["coefficient"] * xdata) + line["phase"]), "o",
                 markersize=0.8, color=line["line"].get_color(), zorder=1)


def init_anim() -> List:
    """Initialize the animation."""
    return []


def animate(frame: float, xdata: List[float], lines: List[FuncLine]) -> List[Line2D]:
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


    Returns
    -------
    `List[Line2D]`
        The line artists needed for blitting
    """
    xdata.append(frame)

    for i, line in enumerate(lines):
        line["phase"] = line["phase"] + K_CONST * \
            sum_of_phase_diffs(i, lines)
        line["data"].append(np.sin((line["coefficient"] * frame) + line["phase"]))
        line["line"].set_data(xdata, line["data"])

    return list(map(itemgetter("line"), lines))


def main() -> NoReturn:
    """Run all executable code"""
    format_plt()

    fig: Figure = plt.figure(figsize=(10.5, 6.4), dpi=225)
    axes: Axes = fig.add_subplot(111)

    format_axes(axes)

    xdata: List[float] = []

    lines: List[FuncLine] = []
    lines.append({"line": plt.plot([], [], lw=2, animated=True, color="r")[0],
                  "phase": 0, "coefficient": 1, "data": []})
    lines.append({"line": plt.plot([], [], lw=2, animated=True, color="g")[0],
                  "phase": 0.5*np.pi, "coefficient": 1, "data": []})
    lines.append({"line": plt.plot([], [], lw=2, animated=True, color="b")[0],
                  "phase": np.pi, "coefficient": 1, "data": []})

    plt.subplots_adjust(top=0.88,
                        bottom=0.11,
                        left=0.125,
                        right=0.9,
                        hspace=0.2,
                        wspace=0.2)

    writer = FFMpegWriter(fps=40, bitrate=250000, extra_args=["-minrate", "650k", "-maxrate", "1M"],
                          metadata=dict(title="/u/ilikeplanes86"))

    frames = np.linspace(0, X_LIM, 512)

    plot_normal_lines(lines, frames)

    anim = FuncAnimation(fig, animate, init_func=init_anim, frames=frames,
                         interval=25, repeat=False, blit=True, fargs=(xdata, lines))

    anim.save(f"recordings/{len(lines)}lines-{K_CONST}.mp4", writer=writer)

    plt.close()


if __name__ == "__main__":
    main()
