"""
usage:
python graph.py
description:
An animation of synchronization of sine functions
"""
# TODO
# Add the kuramoto model effects
# Add type hints and type docstrings
# Refactor data arrays to be iterable
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

plt.style.use("ggplot")

PHASE_0 = 0
PHASE_1 = 0.5*np.pi
PHASE_2 = np.pi
K_CONST = 0.003


def format_axes(axes):
    """Adjust the sizing of the plot's axes.

    Parameters
    ----------
    axes :
        

    Returns
    -------

    """
    axes.set_xlim(0, 4*np.pi)
    axes.set_ylim(-1.05, 1.05)


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

    phases["phase_0"] = phases["phase_0"] + K_CONST * \
        (np.sin(phases["phase_1"] - phases["phase_0"]) +
         np.sin(phases["phase_2"] - phases["phase_0"]))

    phases["phase_1"] = phases["phase_1"] + K_CONST * \
        (np.sin(phases["phase_0"] - phases["phase_1"]) +
         np.sin(phases["phase_2"] - phases["phase_1"]))

    phases["phase_2"] = phases["phase_2"] + K_CONST * \
        (np.sin(phases["phase_0"] - phases["phase_2"]) +
         np.sin(phases["phase_1"] - phases["phase_2"]))

    y_datas["ydata0"].append(np.sin(frame + phases["phase_0"]))
    y_datas["ydata1"].append(np.sin(frame + phases["phase_1"]))
    y_datas["ydata2"].append(np.sin(frame + phases["phase_2"]))

    lines[0].set_data(xdata, y_datas["ydata0"])
    lines[1].set_data(xdata, y_datas["ydata1"])
    lines[2].set_data(xdata, y_datas["ydata2"])

    return lines


def main():
    """Run all executable code"""
    fig = plt.figure(figsize=(8.5, 6.4))
    axes = fig.add_subplot(111)
    format_axes(axes)

    xdata, ydata0, ydata1, ydata2 = [], [], [], []

    lines = []
    lines.append(plt.plot([], [], "o", markersize=1,
                          animated=True, color="r")[0])
    lines.append(plt.plot([], [], lw=2, animated=True, color="g")[0])
    lines.append(plt.plot([], [], lw=2, animated=True, color="b")[0])

    phases = {"phase_0": PHASE_0, "phase_1": PHASE_1, "phase_2": PHASE_2}
    y_datas = {"ydata0": ydata0, "ydata1": ydata1, "ydata2": ydata2}

    amim = FuncAnimation(fig, animate, frames=np.linspace(0, 4*np.pi, 512), interval=25,
                         repeat=False, blit=True, fargs=(lines, xdata, y_datas, phases))

    plt.show()


if __name__ == "__main__":
    main()
