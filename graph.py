"""
usage:
python graph.py
description:
An animation of synchronization of sine functions
"""
# TODO
# Add type hints and type docstrings
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FuncFormatter, MultipleLocator

plt.style.use("ggplot")

PHASE_0 = 0
PHASE_1 = 0.5*np.pi
PHASE_2 = np.pi
K_CONST = 0.004
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
        else:
            res = f"{mult}π"
        return res
    return multiple_of_pi


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

    axes.text(X_LIM - np.pi * 2, 0.9, f"Coupling: K={K_CONST}", zorder=4)

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


def diff_el_dict(target_key, target_dict):
    """Return the difference between all other elements and the target element

    Parameters
    ----------

    target_key :

    target_dict :

    Returns
    -------

    """
    res = 0
    target_value = target_dict[target_key]
    for key, value in target_dict.items():
        if key != target_key:
            res += np.sin(value - target_value)
    return res


def init_anim():
    """Initialize the animation"""
    return []


def animate(frame, lines, xdata, y_datas, phases):
    """Redraw all artists on the plot.

    Parameters
    ----------
    frame :

    lines :

    xdata :

    y_datas :

    phases :


    Returns
    -------

    """
    xdata.append(frame)

    phases["phase_0"] = phases["phase_0"] + \
        K_CONST * diff_el_dict("phase_0", phases)

    phases["phase_1"] = phases["phase_1"] + \
        K_CONST * diff_el_dict("phase_1", phases)

    phases["phase_2"] = phases["phase_2"] + \
        K_CONST * diff_el_dict("phase_2", phases)

    y_datas["ydata0"].append(np.sin(frame + phases["phase_0"]))
    y_datas["ydata1"].append(np.sin(frame + phases["phase_1"]))
    y_datas["ydata2"].append(np.sin(frame + phases["phase_2"]))

    lines[0].set_data(xdata, y_datas["ydata0"])
    lines[1].set_data(xdata, y_datas["ydata1"])
    lines[2].set_data(xdata, y_datas["ydata2"])

    return lines


def main():
    """Run all executable code"""
    fig = plt.figure(figsize=(10.5, 6.4), dpi=180)
    axes = fig.add_subplot(111)
    format_axes(axes)

    xdata, ydata0, ydata1, ydata2 = [], [], [], []

    lines = []
    lines.append(*plt.plot([], [], lw=2, animated=True, color="r"))
    lines.append(*plt.plot([], [], lw=2, animated=True, color="g"))
    lines.append(*plt.plot([], [], lw=2, animated=True, color="b"))

    phases = {"phase_0": PHASE_0, "phase_1": PHASE_1, "phase_2": PHASE_2}
    y_datas = {"ydata0": ydata0, "ydata1": ydata1, "ydata2": ydata2}

    plt.subplots_adjust(top=0.88,
                        bottom=0.11,
                        left=0.125,
                        right=0.9,
                        hspace=0.2,
                        wspace=0.2)

    amim = FuncAnimation(fig, animate, init_func=init_anim, frames=np.linspace(0, X_LIM, 512),
                         interval=25, repeat=False, blit=True, fargs=(lines, xdata, y_datas, phases))

    plt.show()


if __name__ == "__main__":
    main()
