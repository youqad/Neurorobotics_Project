# /!\ We're using Python 3
import plotly
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

import matplotlib.pyplot as plt
from scipy.spatial import distance

from sklearn import preprocessing

from mpl_toolkits.mplot3d import Axes3D

plotly.offline.init_notebook_mode(connected=True)
from IPython.core.display import display, HTML, Markdown
# The polling here is to ensure that plotly.js has already been loaded before
# setting display alignment in order to avoid a race condition.
display(HTML(
    '<script>'
        'var waitForPlotly = setInterval( function() {'
            'if( typeof(window.Plotly) !== "undefined" ){'
                'MathJax.Hub.Config({ SVG: { font: "STIX-Web" }, displayAlign: "center" });'
                'MathJax.Hub.Queue(["setRenderer", MathJax.Hub, "SVG"]);'
                'clearInterval(waitForPlotly);'
            '}}, 250 );'
    '</script>'
))

# Colorscales
def colorscale_list(cmap, number_colors, return_rgb_only=False):
    cm = plt.get_cmap(cmap)
    colors = [np.array(cm(i/number_colors)) for i in range(1, number_colors+1)]
    rgb_colors_plotly = []
    rgb_colors_only = []
    for i, c in enumerate(colors):
        col = 'rgb{}'.format(tuple(255*c[:-1]))
        rgb_colors_only.append(col)
        rgb_colors_plotly.append([i/number_colors, col])
        rgb_colors_plotly.append([(i+1)/number_colors, col])
    return rgb_colors_only if return_rgb_only else rgb_colors_plotly

from scipy.io import loadmat, whosmat
from numpy.random import randint

def formatted(f): 
    return format(f, '.2f').rstrip('0').rstrip('.')


from sensorimotor_dependencies import organisms

##########################################################################
# Plot Figure 3a

## add "from mpl_toolkits.mplot3d import Axes3D" in the beginning

## dim 1: trial index
## dim 2: sensor number (ext + pro)
## dim 3: normalized sensory input

def plot_envchange(xs,ys,zs):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xs,ys,zs)
    plt.show()

O = organisms.Organism1()
z = O.get_proprioception(return_trials=True)
#x = np.array(range(0,z.shape[0]+1))
#y = np.array(range(0,z.shape[1]+1) )
z = preprocessing.scale(z, axis=0, with_mean=True, with_std=True, copy=True)


plotly.offline.iplot([go.Surface(z=z)])


##########################################################################
### EIGNEVALUES AND THEIR RATIOS

O = organisms.Organism1()
eig, ratios = O.get_dimensions(return_eigenvalues=True)[4]

traces_eig, traces_rat = [], []
names = ['Body', 'Environment', 'Body and Environment']

for e, name in zip(eig, names):
    traces_eig.append(go.Scatter(
    y=e[-20::-1],
    name='Moving {}'.format(name)
    ))

for e, name in zip(ratios, names):
    traces_rat.append(go.Scatter(
    y=e,
    name='Moving {}'.format(name)
    ))
    
layout = go.Layout(
    yaxis=dict(
        type='log',
        autorange=True
    )
)

plotly.offline.iplot(
    go.Figure(
        data=[traces_eig], 
        layout=layout)
)

plotly.offline.iplot(
    go.Figure(
        data=[traces_eig])
)