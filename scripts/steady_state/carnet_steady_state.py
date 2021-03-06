""" Generate various steady state data sets."""
from run_steadystate import RunSteadyState
import os
import distutils
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime


inputs = {"P_a": (20, 140), "Pa_CO2": (10, 80), "SaO2sup": (0.2, 1.0)}
title_dict = {"P_a": "Arterial Blood Pressure",
              "Pa_CO2": "Partial Pressure of CO2",
              "SaO2sup": "Arterial Oxygen Saturation"}
outputs = ["CMRO2", "CCO", "HbT", "CBF"]
k_auts = {"Healthy": 1.0,
          "Mild": 0.75,
          "Medium": 0.5,
          "Severe": 0.25}

cbar = sns.color_palette("muted", n_colors=4)
direction = "both"


def add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   x-position of the arrow as a percentile.
                If None, mean of xdata is taken.
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()
    else:
        position = np.percentile(xdata, position)
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == 'right':
        end_ind = start_ind + 1
        arrowstyle = "->"
    else:
        end_ind = start_ind - 1
        arrowstyle = "<-"

    line.axes.annotate('',
                       xytext=(xdata[start_ind], ydata[start_ind]),
                       xy=(xdata[end_ind], ydata[end_ind]),
                       arrowprops=dict(arrowstyle=arrowstyle, color=color),
                       size=size
                       )


for o in outputs:
    print("Running steady state - {}".format(o))
    base_work_dir = os.path.expanduser(os.path.join('~',
                                                    'Dropbox',
                                                    'phd',
                                                    'Conferences',
                                                    'CARnet',
                                                    'Figures',
                                                    o))
    distutils.dir_util.mkpath(base_work_dir)
    for i, r in inputs.items():
        data = {}

        print("\tRunning steady state - {}".format(i))
        for k, v in k_auts.items():
            workdir = os.path.join(base_work_dir, k)
            distutils.dir_util.mkpath(workdir)
            print("\t\tRunning k_aut {}".format(k))
            config = {
                "model_name": "BS",
                "inputs": i,
                "parameters": {
                    "k_aut": v
                },
                "targets": [o],
                "max_val": r[1],
                "min_val": r[0],
                "debug": True,
                "direction": direction
            }

            model = RunSteadyState(conf=config, workdir=workdir)
            output = model.run_steady_state()
            data[k] = output
            with open(os.path.join(workdir,
                                   "{}_{}.json".format(i, direction)),
                      'w') as f:
                json.dump(data, f)

        fig, ax = plt.subplots()

        for idx, k in enumerate(k_auts.keys()):
            ax.set_position([0.1, 0.1, 0.7, 0.8])
            line = ax.plot(data[k][i][:len(data[k][i]) // 2 + 1],
                           data[k][o][:len(data[k][o]) // 2 + 1],
                           label=k, color=cbar[idx])[0]
            add_arrow(line, position=60, size=24)
            line = ax.plot(data[k][i][len(data[k][i]) // 2:],
                           data[k][o][len(data[k][o]) // 2:],
                           color=cbar[idx], linestyle='--')[0]
            add_arrow(line, direction='left', position=25, size=24)

        ax.set_title("Steady state for varying levels\nof "
                     "autoregulation impairment",
                     size=20)
        ax.set_ylabel(o, size=18)
        ax.set_xlabel(title_dict[i], size=16)
        legend = ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
                           prop={'size': 12})

        fig.savefig(os.path.join(base_work_dir, "{}_{}.png".format(i,
                                                                   direction)),
                    bbox_inches="tight")
