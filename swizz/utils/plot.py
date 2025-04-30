import matplotlib as mpl

def apply_legend(ax):
    print(mpl.rcParams)
    return ax.legend(
        loc=mpl.rcParams["legend.loc"],
        frameon=mpl.rcParams["legend.frameon"],
        framealpha=mpl.rcParams["legend.framealpha"],
        edgecolor=mpl.rcParams["legend.edgecolor"],
        handlelength=mpl.rcParams["legend.handlelength"],
        fontsize=mpl.rcParams["legend.fontsize"],
    )
