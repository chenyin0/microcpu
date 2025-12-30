import matplotlib.pyplot as plt

def plot_scatter(x, y, fig_path):
    plt.scatter(x, y)
    plt.savefig(fig_path)