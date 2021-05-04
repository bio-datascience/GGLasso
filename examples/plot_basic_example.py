"""
Basic example
=================================

We demonstrate how to use ``GGLasso`` for a SGL problem. 
First, we generate a sparse powerlaw network of 20 nodes. We generate an according precision matrix and sample from it. Here, we use a very large 
number of samples (N=5000) to demonstrate that it is possible to recover (approximately) the original graph if sufficiently many samples are available.

In many practical applications however, we face the situation of p>N.

"""

from gglasso.helper.data_generation import group_power_network, sample_covariance_matrix
from gglasso.problem import glasso_problem
from gglasso.helper.basic_linalg import adjacency_matrix

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

p = 20
N = 5000

Sigma, Theta = group_power_network(p, K = 1, M = 1, nxseed = 1235)
S, sample = sample_covariance_matrix(Sigma, N)
# remove redundant dimension
Theta = Theta[0]; S = S[0]; sample= sample[0]

print("Shape of empirical covariance matrix: ", S.shape)
print("Shape of the sample array: ", sample.shape)


#%%

# Draw the graph of the true precision matrix.
A = adjacency_matrix(Theta)
np.fill_diagonal(A,1)

G = nx.from_numpy_array(A)
pos = nx.drawing.layout.spring_layout(G)

plt.figure()
nx.draw_networkx(G, pos = pos, node_color = "darkblue", edge_color = "darkblue", font_color = 'white', with_labels = True)

#%%
# We now create an instance of ``glasso_problem``. The problem formulation is derived automatically from the input shape of ``S``.
#

P = glasso_problem(S, N, reg_params = {'lambda1': 0.05}, latent = False, do_scaling = False)
print(P)

#%%
# Next, do model selection by solving the problem on a range of :math:`\lambda_1` values.
#

lambda1_range = np.logspace(0, -3, 25)
modelselect_params = {'lambda1_range': lambda1_range}

P.model_selection(modelselect_params = modelselect_params, method = 'eBIC', gamma = 1.0)

# regularization parameters are set to the best ones found during model selection
print(P.reg_params)

#%%
# access the solution and draw the corresponding graph
#

#tmp = P.modelselect_stats
sol = P.solution.precision_
P.solution.calc_adjacency()


fig, axs = plt.subplots(2,2, figsize=(10,8))
node_size = 100
font_size = 9

nx.draw_networkx(G, pos = pos, node_size = node_size, node_color = "darkblue", edge_color = "darkblue", \
                 font_size = font_size, font_color = 'white', with_labels = True, ax = axs[0,0])
axs[0,0].axis('off')
axs[0,0].set_title("True graph")

G1 = nx.from_numpy_array(P.solution.adjacency_)
nx.draw_networkx(G1, pos = pos, node_size = node_size, node_color = "peru", edge_color = "peru", \
               font_size = font_size, font_color = 'white', with_labels = True, ax = axs[0,1])
axs[0,1].axis('off')
axs[0,1].set_title("Recovered graph")

sns.heatmap(Theta, cmap = "coolwarm", vmin = -0.5, vmax = 0.5, linewidth = .5, square = True, cbar = False, \
            xticklabels = [], yticklabels = [], ax = axs[1,0])
axs[1,0].set_title("True precision matrix")
    
sns.heatmap(sol, cmap = "coolwarm", vmin = -0.5, vmax = 0.5, linewidth = .5, square = True, cbar = False, \
            xticklabels = [], yticklabels = [], ax = axs[1,1])
axs[1,1].set_title("Recovered precision matrix")
   
    