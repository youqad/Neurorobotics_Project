---
title: "Final Project: Inferring Space from Sensorimotor Dependencies"
author:
- 'Kexin Ren'
- 'Younesse Kaddar'
date: 2018-06-02
tags:
  - project
  - tutorial
  - exercise
  - robotics
  - neuroscience
  - neuro-robotique
  - neurorobotics
  - Khamassi
abstract: 'Final Project: Inferring Space from Sensorimotor Dependencies'
---

# Final Project: Inferring Space from Sensorimotor Dependencies

### Kexin Ren & Younesse Kaddar (**Lecturer**: Nicolas Perrin)

#### Original article: « Is There Something Out There? Inferring Space from Sensorimotor Dependencies » (D. Philipona, J.K. O'Regan, J.-P. Nadal)

- [Jupyter Notebook](http://bit.ly/2kJwH5w)
- [Online Version](http://younesse.net/Neuro-robotique/Project.md)

$$
\newcommand{\T}{ {\raise{0.7ex}{\intercal}}}
$$


## The Algorithm

1. Proprioceptive input is separated from exteroceptive input by noting that proprioceptive input remains silent when no motor commands are given, whereas exteroceptive input changes because of environmental change.

2. Estimation of the number of parameters needed to describe the variation in the exteroceptive inputs when only the environment changes. The algorithm issues no motor commands and calculates the covariance matrix of the observed environment-induced variations in sensory inputs. The dimension estimation is done by considering the eigenvalues of this covariance matrix. The eigenvalues $λ_i$ should fall into two classes: a class with values all equal to zero and a class with nonzero values. The two classes are separated by a clustering method (e.g. PCA). The number of nonzero eigenvalues is taken as the number of dimensions.

3. Estimation of the number of parameters needed to describe the variation in the exteroceptive inputs when only the body moved. The environment is kept fixed, and the algorithm gives random motor commands. The covariance matrix of the resulting changes is observed and the dimension is estimated from the number of nonzero eigenvalues in the same way as before.

4. Estimation of the number of parameters needed to describe the changes in exteroceptive inputs when both the body and the environment change. The environment is changed at random, and the organism gives random motor commands. The number of nonzero eigenvalues of the covariance matrix is obtained as before.

## Simulation

### Notations

Notation|Meaning
-|-
$$Q ≝ (Q_1, \ldots, Q_q)$$|positions of the joints
$$P ≝ (P_1, \ldots, P_p)$$|positions of the eyes
$$a^θ_i, a^φ_i, a^ψ_i$$|Euler angles for the orientation of eye i
$$Rot(a^θ_i, a^φ_i, a^ψ_i)$$|rotation matrix for eye i
$$C_{i,k}$$|relative position of photosensor $k$ within eye $i$
$$d ≝ (d_1, \ldots,d_q)$$|apertures of diaphragms
$$L ≝ (L_1,\ldots,L_p)$$|positions of the lights
$$θ ≝ (θ_1, \ldots, θ_p)$$|luminances of the lights
$$S^e{i,k}$$|sensory input from exteroceptive sensor $k$ of eye $i$
$$S^i_p$$|sensory input from proprioceptive sensor $i$
$$M, E$$|motor command and environmental control vector

### Computing the motor commands


$$
\begin{align*}
(Q,P,a) &≝ σ(W_1 · σ(W_2 · M − μ_2)−μ_1)\\
L &≝ σ(V_1 ·σ(V_2 · E − ν_2) − ν_1)\\
S^e_{i,k} &≝ d_i \sum\limits_{ j } \frac{θ_j}{\Vert P_i + Rot(a_i^θ, a_i^φ, a_i^ψ) \cdot C_{i,k} - L_j \Vert^2}\\
S^p_i &≝ σ(U_1 · σ(U_2 · M − τ_2) − τ_1)
\end{align*}
$$

where

- $W_1, W_2, V_1, V_2, U_1, U_2$ are matrices with coefficients drawn randomly from a uniform distribution between $−1$ and $1$
- the vectors $μ_1, μ_2, ν_1, ν_2, τ_1, τ_2$ too
- $σ$ is an arbitrary nonlinearity (e.g. the hyperbolic tangent function)
- the $C_{i,k}$ are drawn from a centered normal distribution whose variance (which can be understood as the size of the retina) is so that the sensory changes resulting from a rotation of the eye are of the same order of magnitude as the ones resulting from a translation of the eye
- $θ$ and $d$ are constants drawn at random in the interval $[0.5, 1]$
