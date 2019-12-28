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


def animate(frame, lines, xdata, ydata0, ydata1):
    """Redraw all artists on the plot.

    Parameters
    ----------
    frame :

    lines :

    xdata :

    ydata0 :

    ydata1 :


    Returns
    -------

    """
    xdata.append(frame)
    ydata0.append(np.sin(frame))
    ydata1.append(np.sin(frame + 0.5*np.pi))
    lines[0].set_data(xdata, ydata0)
    lines[1].set_data(xdata, ydata1)
    return lines


def main():
    """Run all executable code"""
    fig = plt.figure(figsize=(8.5, 6.4))
    axes = fig.add_subplot(111)
    format_axes(axes)
    xdata, ydata0, ydata1 = [], [], []
    lines = []
    lines.append(plt.plot([], [], "o", markersize=1,
                          animated=True, color="r")[0])
    lines.append(plt.plot([], [], lw=2, animated=True, color="g")[0])
    amim = FuncAnimation(fig, animate, frames=np.linspace(0, 4*np.pi, 512),
                         interval=25, repeat=False, blit=True, fargs=(lines, xdata, ydata0, ydata1))

    plt.show()


if __name__ == "__main__":
    main()
