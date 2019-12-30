"""
usage:
python graph.py
description:
An animation of synchronization of sine functions
"""
from operator import itemgetter

# TODO
# Add type hints and type docstrings
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.ticker import FuncFormatter, MultipleLocator

K_CONST = 0.1
X_LIM = 8*np.pi


def format_pi(denominator):
    """Return a formatting function that uses the denominator provided

    Parameters
    ----------

    denominator :

    Returns
    -------

    """
    def multiple_of_pi(value, _position):
        """Return the multiple that value is of (pi*denominator)

        Parameters
        ----------
        value :

        _position :

        Returns
        -------

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


def format_plt():
    """Change any global style params"""
    mpl.rcParams["font.family"] = "Poppins"
    plt.style.use("ggplot")


def format_axes(axes):
    """Adjust the sizing of the plot's axes.

    Parameters
    ----------
    axes :


    Returns
    -------

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


def sum_of_phase_diffs(target_index, lines):
    """Return the sum of the sines of the differences between
    all other elements and the target element

    Parameters
    ----------

    target_key :

    target_dict :

    Returns
    -------

    """
    res = 0
    target_value = lines[target_index]["phase"]
    for i, line in enumerate(lines):
        if i != target_index:
            res += np.sin(line["phase"] - target_value)
    return res


def init_anim():
    """Initialize the animation"""
    return []


def animate(frame, xdata, line_props):
    """Redraw all artists on the plot.

    Parameters
    ----------
    frame :

    xdata :

    line_props :


    Returns
    -------

    """
    xdata.append(frame)

    for i, line in enumerate(line_props):
        line["phase"] = line["phase"] + K_CONST * \
            sum_of_phase_diffs(i, line_props)
        line["data"].append(np.sin(frame + line["phase"]))
        line["line"].set_data(xdata, line["data"])

    return list(map(itemgetter("line"), line_props))


def main():
    """Run all executable code"""
    format_plt()

    fig = plt.figure(figsize=(10.5, 6.4), dpi=225)
    axes = fig.add_subplot(111)
    format_axes(axes)

    xdata = []

    phases = [0, 0.5*np.pi, np.pi, -0.5*np.pi]

    lines = []
    lines.append(*plt.plot([], [], lw=2, animated=True, color="r"))
    lines.append(*plt.plot([], [], lw=2, animated=True, color="g"))
    lines.append(*plt.plot([], [], lw=2, animated=True, color="b"))
    lines.append(*plt.plot([], [], lw=2, animated=True, color="c"))

    line_props = []
    for i, line in enumerate(lines):
        line_props.append({"phase": phases[i], "data": [], "line": line})

    plt.subplots_adjust(top=0.88,
                        bottom=0.11,
                        left=0.125,
                        right=0.9,
                        hspace=0.2,
                        wspace=0.2)

    writer = FFMpegWriter(fps=40, bitrate=250000,
                          metadata=dict(author="/u/ilikeplanes86"))

    anim = FuncAnimation(fig, animate, init_func=init_anim, frames=np.linspace(0, X_LIM, 512),
                         interval=25, repeat=False, blit=True, fargs=(xdata, line_props))

    anim.save(f"recordings/{len(lines)}lines-{K_CONST}.mp4", writer=writer)

    # plt.show()


if __name__ == "__main__":
    main()
