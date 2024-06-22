import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# MCP and MTS crystal data from CSV files
MCP = pd.read_csv('data/MCP.csv', encoding='ANSI')
MTS = pd.read_csv('data/MTS.csv', encoding='ANSI')

# Define crystal names for plot
crystal_names = ['MCP', 'MTS']

# Define mAs values and associated linestyles
mAs = [5, 10, 20, 50, 100]
ls = [(0, (2, 4)), '-.', ':', '--', '-']

# Create a figure with two subplots sharing the same x-axis
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# Iterate through crystals
for i, crystal in enumerate([MCP, MTS]):

    # Define time range and crystal count parameters based on crystal index
    time_params = (0, 31.4, 315) if i == 0 else (0, 57.4, 575)
    count_params = (13, 328) if i == 0 else (13, 588)

    # Extract time data
    time = np.linspace(*time_params)

    # Extract temperature data
    temp = pd.Series(crystal.iloc[[2], slice(*count_params)].squeeze().values)

    # Initialise lists to store means and standard deviations
    index = 0
    means = []
    stdevs = []

    # Iterate through mAs values
    for ctp in mAs:

        # Extract count data for the current mAs range
        all_count = pd.DataFrame([crystal.iloc[[i], slice(*count_params)].squeeze().values for i in range(0, 89, 3)])
        count = all_count.iloc[index+3:index+6]

        # Compute mean and standard deviation of counts
        mean_cnt = count.mean()
        st_dev = count.std(axis=0)

        # Append results to lists
        means.append(mean_cnt)
        stdevs.append(st_dev)

        index += 6

    # Choose the appropriate axis for the current crystal
    ax = ax1 if i == 0 else ax2

    # Plot mean counts against time
    for j in range(5):
        ax.plot(time, means[j], color='#0554f2' if i == 0 else 'darkorange', label=f'{mAs[j]} mAs', linestyle=ls[j])
        ax.fill_between(time, means[j] - stdevs[j], means[j] + stdevs[j], color='#07bdfa' if i == 0 else 'orange', alpha=0.2)

    # Configure axis labels, limits, ticks, and formatting
    ax.legend(loc='upper left', title='Current-time', fontsize=8.5, bbox_to_anchor=(0.001, 0.925))
    ax.set_ylabel('Count rate [cps]')
    ax.set_xlim(time_params[:2])  # Set x-axis limits based on time parameters
    ax.set_ylim(0)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(4, 4), useOffset=True)

    # Create a twin y-axis to plot temperature against time
    ax_twin = ax.twinx()
    ax_twin.set_ylabel(r'Temperature [$^{\circ}$C]')
    ax_twin.plot(time, temp, color='red', linestyle='-', linewidth=0.5, alpha=0.5)

    # Adjust limits and set maximum temperature to red
    max_T = 240 if i == 0 else 300
    default_ticks = [tick for tick in ax_twin.get_yticks() if tick != 300] if i == 1 else [tick for tick in ax_twin.get_yticks()]
    ax_twin.set_yticks(default_ticks + [max_T])
    ax_twin.set_ylim(0, 249 if i == 0 else 320)
    ax_twin.get_yticklabels()[list(ax_twin.get_yticks()).index(max_T)].set_color('red')
    ax_twin.tick_params(axis='y')

    # Set title
    ax.set_title(crystal_names[i], weight='bold', x=0.04, y=0.895, fontsize=14)

# Set the common x-axis label
ax2.set_xlabel(r'Time [s]')

# Adjust layout and save figure
fig.subplots_adjust(top=0.98, bottom=0.03, left=0.07, right=0.99, hspace=0.17, wspace=0.1)
plt.savefig(f'results/glowcurves.pdf', bbox_inches='tight')
