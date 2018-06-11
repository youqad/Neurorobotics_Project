---
presentation:

  width: 1700
  height: 1150

  margin: 0.05

  # Display controls in the bottom right corner
  controls: true

  # Display a presentation progress bar
  progress: true

  # Display the page number of the current slide
  slideNumber: true

  # Push each slide change to the browser history
  history: false

  # Enable keyboard shortcuts for navigation
  keyboard: true

  # Enable the slide overview mode
  overview: true

  # Vertical centering of slides
  center: false

  # Enables touch navigation on devices with touch input
  touch: true

  # Loop the presentation
  loop: false

  # Change the presentation direction to be RTL
  rtl: false

  # Randomizes the order of slides each time the presentation loads
  shuffle: false

  # Turns fragments on and off globally
  fragments: true

  # Flags if the presentation is running in an embedded mode,
  # i.e. contained within a limited portion of the screen
  embedded: false

  # Flags if we should show a help overlay when the questionmark
  # key is pressed
  help: true

  # Flags if speaker notes should be visible to all viewers
  showNotes: false

  # Number of milliseconds between automatically proceeding to the
  # next slide, disabled when set to 0, this value can be overwritten
  # by using a data-autoslide attribute on your slides
  autoSlide: 0

  # Stop auto-sliding after user input
  autoSlideStoppable: true

  # Enable slide navigation via mouse wheel
  mouseWheel: false

  # Hides the address bar on mobile devices
  hideAddressBar: true

  # Opens links in an iframe preview overlay
  previewLinks: false

  # Transition style
  transition: 'default' # none/fade/slide/convex/concave/zoom

  # Transition speed
  transitionSpeed: 'default' # default/fast/slow

  # Transition style for full page slide backgrounds
  #backgroundTransition: '' # none/fade/slide/convex/concave/zoom

  # Number of slides away from the current that are visible
  viewDistance: 3

  # Parallax background image
  parallaxBackgroundImage: 'https://i.gyazo.com/b0ccddff134624a2d2dc0bdaa917e393.png'

  # Parallax background size
  # parallaxBackgroundSize: "5100px 2800px"


  # Number of pixels to move the parallax background per slide
  # - Calculated automatically unless specified
  # - Set to 0 to disable movement along an axis
  parallaxBackgroundHorizontal: 200
  parallaxBackgroundVertical: 200
---

<style>
.xypic-block {
border: 2px solid #a1a1a1;
padding: 10px 40px;
border-radius: 25px;
background: #ADA996;
background: -webkit-linear-gradient(to right, #EAEAEA, #DBDBDB, #F2F2F2, #ADA996);
background: linear-gradient(to right, #EAEAEA, #DBDBDB, #F2F2F2, #ADA996);
float: center;
position: relative;
}
</style>


$$
\newcommand{\rec}{\mathop{\rm rec}\nolimits}
\newcommand{\ind}{\mathop{\rm ind}\nolimits}
\newcommand{\inl}{\mathop{\rm inl}\nolimits}
\newcommand{\inr}{\mathop{\rm inr}\nolimits}
\newcommand{\Hom}{\mathop{\rm Hom}\nolimits}
\newcommand{\Ty}{\mathop{\rm Ty}\nolimits}
\newcommand{\Tm}{\mathop{\rm Tm}\nolimits}
\newcommand{\op}{\mathop{\rm op}\nolimits}
\newcommand{\Set}{\mathop{\rm Set}\nolimits}
\newcommand{\CwF}{\mathop{\rm CwF}\nolimits}
\newcommand{\CwFB}{\mathop{\rm CwFB}\nolimits}
\newcommand{\CwFId}{\mathop{\rm CwFId}\nolimits}
\newcommand{\Cat}{\mathop{\rm Cat}\nolimits}
\newcommand{\bu}{\bullet}
\newcommand{\isContr}{\mathop{\rm isContr}\nolimits}
\newcommand{\coh}{\mathop{\bf coh}\nolimits}
\newcommand{\id}{\mathop{\rm id}\nolimits}
\newcommand{\Id}{\mathop{\rm Id}\nolimits}
\newcommand{\refl}{\mathop{\rm refl}\nolimits}
\newcommand{\J}{\mathop{\rm J}\nolimits}
\newcommand{\scol}{\mathop{\,;\,}\nolimits}
$$

<!-- slide -->
<div style="text-align:center">

## Is there something out there?

### Inferring Space from Sensorimotor Dependencies

##### Kexin Ren & Younesse Kaddar

##### *Based on* D. Philipona, J. O’Regan, and J. Nadal's 2003 article

[Documentation](https://neurorobotics-project.readthedocs.io) / [Associated Jupyter Notebook](/ipynb/neurorobotics/Inferring_Space_from_Sensorimotor_Dependencies.ipynb.html)


</div>

____

<div style="text-align:left">

### Introduction: you said "space"?

____

### I. Exteroception & Compensation

### II. Mathematical formulation

### III. Algorithm

### V. Simulations and Beyond

</div>


<!-- slide data-transition="convex" data-transition-speed="slow" -->

### Introduction: you said "space"?

<span class="fragment fade-down highlight-red" data-fragment-index="1">high-dimensional sensory input vector</span><span class="fragment fade-down highlight-green" data-fragment-index="2">$\qquad \overset{\text{Brain}}{\rightsquigarrow} \qquad \underbrace{\textit{space, attributes, ...}}_{\text{easier to visualize}}$</span>

<img src="intro_drawing.png" alt="Problem statement" style="max-height: 900px; border:none" class="fragment fade-in" data-fragment-index="3"/>

<!-- slide data-transition="zoom" data-transition-speed="slow" vertical=true -->

All the brain can do:

:   1. issue <strong class="fragment fade-down highlight-blue" data-fragment-index="1">motor commands</strong>

    2. observe the resulting <strong class="fragment fade-down highlight-green" data-fragment-index="2">environmental changes</strong>

    ⟹ *then* collect <strong class="fragment fade-down highlight-red" data-fragment-index="3">sensory inputs</strong>

<img src="motor_env_sensory.png" alt="Problem statement" style="max-height: 900px; border:none" class="fragment fade-down" data-fragment-index="4"/>


<!-- slide data-transition="concave" data-transition-speed="slow" -->

## I. - Exteroception & Compensation

### I.A Exteroception vs. Proprioception

<br>

|Sensory input|Definition|
-|-
<span class="fragment highlight-blue">*Proprioceptive*</span>|<span class="fragment highlight-blue">independent</span> of the environment
<span class="fragment highlight-green">*Exteroceptive*</span>|<span class="fragment highlight-green">dependent</span> of the environment

<br>

________________

### Example

<img src="Haunter_sensory_inputs.png" style="max-height: 500px; border:none" class="fragment fade-down"/>

<!-- slide data-transition="convex" data-transition-speed="slow" -->

### I.B - Compensated movements

<br>

>Compensated movements:
>
>: Variations of the motor command and the environment that compensate one another.

<img src="compensated_movements_step1.png" style="max-height: 900px; border:none" class="fragment fade-down"/>



<!-- slide data-transition="zoom" data-transition-speed="slow" vertical=true -->

<img src="compensated_movements_step2.png" style="max-height: 460px; border:none" class="fragment fade-down"/>
<img src="compensated_movements_step3.png" style="max-height: 460px; border:none" class="fragment fade-down"/>

> **Relative distance between them** is the same at steps 1 & 3

<!-- slide data-transition="concave" data-transition-speed="slow" data-background-image="./background_paved.png"  -->

### Organism 1

<img src="organisms/org1.png"/>

<!-- slide data-transition="concave" data-transition-speed="slow" data-background-image="background_paved.png"  -->

<img src="organisms/org2.png" style="max-height: 500px; border:none" class="fragment fade-down"/>

<img src="organisms/org3.png" style="max-height: 500px; border:none" class="fragment fade-down"/>

<img src="organisms/org4.png" style="max-height: 500px; border:none" class="fragment fade-down"/>


<!-- slide data-transition="concave" data-transition-speed="slow" -->

### II. Mathematical formulation

<br>

$$
\begin{align*}
\mathcal{E} &≝ \lbrace E ∈ \text{environmental states}\rbrace\\
\mathcal{M} &≝ \lbrace M ∈ \text{motor commands}\rbrace\\
\mathcal{S} &≝ \lbrace S ∈ \text{sensory inputs}\rbrace
\end{align*}
$$

are **manifolds** of dimension $e, m$ and $s$ respectively such that:

<br>

>$$\mathcal{S} = ψ(\mathcal{M} × \mathcal{E})$$

<br><br>

________________

<br>

**NB**: We are only considering **exteroceptive inputs**, *i.e.* points $S^e ∈ \mathcal{S}$ s.t.:

$$∃ \mathcal{M}' ⊆ \mathcal{M}; \; ψ^{-1}(S^e) = \mathcal{M}' × \mathcal{E}$$


<!-- slide data-transition="convex" data-transition-speed="slow" vertical=true -->

Pushforward of $(M_0, E_0)$ by $ψ$

⟹ Tangent space at $S_0 ≝ ψ(M_0, E_0)$:

> $$\lbrace dS \rbrace =  \lbrace dS \rbrace_{dE=0} + \lbrace dS \rbrace_{dM=0}$$

Moreover:

- $\lbrace dS \rbrace_{dE=0}$ is the tangent space of $ψ(E_0, \mathcal{M})$ at $S_0$
- $\lbrace dS \rbrace_{dM=0}$ is the tangent space of $ψ(\mathcal{E}, M_0)$ at $S_0$

<br>

<img src="tangent_space.png" style="max-height: 500px; border:none" class="fragment fade-down"/>

<!-- slide data-transition="convex" data-transition-speed="slow" vertical=true -->

$$\mathcal{C}(M_0, E_0) ≝ ψ(\mathcal{E}, M_0) ∩ ψ(\mathcal{E}, M_0)$$

<br>

**Along $\mathcal{C}(M_0, E_0)$:** exteroceptive changes obtained by adding

- either $dE$
- or $dM$.

<br>

________________

<br>

Compensated (infinitesimal) movements:

: when infinitesimal changes along $\lbrace dS \rbrace_{dE=0}$ and $\lbrace dS \rbrace_{dM=0}$ compensate one another

<br> <br>

Dimension of the space of compensated movements:

: $$d ≝ \dim \underbrace{\lbrace dS_{dM=0} \mid ∃ dS_{dE=0}; dS_{dM=0} + dS_{dE=0} = 0 \rbrace}_{= \; \lbrace dS \rbrace_{dE=0} ∩ \lbrace dS \rbrace_{dM=0}} = \dim \mathcal{C}(M_0, E_0)$$


<!-- slide data-transition="convex" data-transition-speed="slow" vertical=true -->

<br><br>

So **by Grassmann formula:**

<br>

>$$\begin{align*}
d \quad &≝ \quad \dim \lbrace dS \rbrace_{dE=0} ∩ \lbrace dS \rbrace_{dM=0}\\
\quad &= \quad \dim \lbrace dS \rbrace_{dE=0} + \dim \lbrace dS \rbrace_{dM=0} \\
\quad & \qquad - \dim \Big( \underbrace{\lbrace dS \rbrace_{dE=0} +\lbrace dS \rbrace_{dM=0}}_{= \lbrace dS \rbrace} \Big)\\ \\
\quad &= \quad \dim \lbrace dS \rbrace_{dE=0} + \dim \lbrace dS \rbrace_{dM=0} - \dim (\lbrace dS \rbrace)
\end{align*}$$


<!-- slide data-transition="convex" data-transition-speed="slow" -->

## t-Distributed Stochastic Neighbor Embedding (t-SNE)

<div>
<span class="fragment fade-down highlight-blue" data-fragment-index="1">the relation "being neighbors"</span><span class="fragment fade-down highlight-red" data-fragment-index="2">$\qquad \rightsquigarrow \qquad \underbrace{\textit{"continuous range of neighborness"}}_{\text{probability distribution}}$</span>
</div>

________________

Map points are:

- attracted to points that are near them in the data set
- repelled by points that are far from them in the data set

<br/>

<img src="tSNE_step0.png" alt="t-SNE" style="max-height: 500px; border:none" class="fragment fade-in" data-fragment-index="2"/>

<em class="fragment fade-in" data-fragment-index="2">Image courtesy of <a src="https://statquest.org/2017/09/18/statquest-t-sne-clearly-explained/">statquest.org</a></em>

<!-- slide data-transition="convex" data-transition-speed="slow" vertical=true data-background-image=dark-background.jpg -->


### Step 1

<div style="text-align:left; margin-left:10%">Compute conditional probabilities</div>

$$p_{j\mid i} ≝ \frac{\exp(-\vert\vert x_i-x_j\vert\vert^2/2\sigma^2)}{\sum_{k\neq i}\exp(-\vert\vert x_i-x_k\vert\vert^2/2\sigma^2)}$$

> probability that $x_i$ has $x_j$ as its neighbor if neighbors were chosen according to a Gaussian distribution centered at $x_i$

<br />

<div style="text-align:left; margin-left:10%">⟶ "similarity" between data points</div>


<img src="tSNE_step1.png" alt="t-SNE" style="max-height: 500px; border:none" class="fragment fade-in" data-fragment-index="1"/>

<!-- slide data-transition="convex" data-transition-speed="slow" vertical=true data-background-image=dark-background.jpg -->

### Step 2

<div style="text-align:left; margin-left:10%">Then symmetrize the conditional probabilities:</div>

$$p_{i,j} ≝ \frac{p_{j\mid i} + p_{i\mid j}}{2n}$$

<img src="tSNE_step2.png" alt="t-SNE" style="margin-left: 15%; border:none; float: left" class="fragment fade-in" data-fragment-index="1"/>

<img src="tSNE_step3.png" alt="t-SNE" style="margin-right: 15%; border:none; float: right" class="fragment fade-in" data-fragment-index="2"/>

<!-- slide data-transition="convex" data-transition-speed="slow" vertical=true data-background-image=dark-background.jpg -->

### Step 3

- $y_i$'s initialized at random

- Similarities between visualization points:

    $$q_{i,j} ≝ \frac{(1+\vert\vert y_i-y_j\vert\vert^2)^{-1}}{\sum_{k\neq l}(1+\vert\vert y_i-y_l\vert\vert^2)^{-1}}$$

    ⟶ computed with resort to a Student-$t$ distribution


<br>

<img src="student_vs_gaussian.png" alt="t-SNE" style="border:none;" class="fragment fade-in" data-fragment-index="2"/>

<br>

<img src="tSNE_step3bis.png" alt="t-SNE" style="border:none;" class="fragment fade-in" data-fragment-index="3"/>


<!-- slide data-transition="convex" data-transition-speed="slow" vertical=true data-background-image=dark-background.jpg -->

### Step 4

- Minimize the Kullback–Leibler divergence: $C ≝ \sum_{i≠ j}p_{ij}\log {\frac {p_{i,j}}{q_{i,j}}}$, by modifying the $y_i$'s with gradient descent

- Recompute the $q_{i,j}$'s at each step (until convergence is reached)

<img src="tSNE_step4.png" alt="t-SNE" style="border:none" class="fragment fade-in" data-fragment-index="1"/>


<!-- slide data-transition="concave" data-transition-speed="slow" -->

## Dimensionality reduction to visualize high-dimensional representations

*In a neural network:*

- **input data** ⟶ shape changed from a layer to another: a *representation* is the reshaped data at a given layer.

<img src="NN_transform.png" alt="t-SNE" style="max-height: 500px; border:none" class="fragment fade-in" data-fragment-index="1"/>


> Since representations are high-dimensional ⟹ DR methods to visualize them


<!-- slide data-transition="concave" data-transition-speed="slow" -->

### meta-SNE to visualize the space of representations


1. Build matrices of pairwise distances: $$D_X ≝ \left(d_X(x_i, x_j)\right)_{i,j}$$ ⟹ vectorize representations

2. *Step up the ladder of abstraction*: visualize vectorized representations with t-SNE


> Regarding neural networks: meta-SNE enables us no longer to confine ourselves to comparing their outcome only, but also how they operate internally.

<!-- slide data-transition="convex" data-transition-speed="slow" data-background-image=dark-background.jpg vertical=true -->

### Sigmoid

<img src="meta-SNE_1.png" alt="meta-SNE" class="fragment fade-in" data-fragment-index="1"/>

### ReLU

<img src="meta-SNE_2.png" alt="meta-SNE" style="max-height: 500px; border:none" class="fragment fade-in" data-fragment-index="2"/>

<!-- slide data-transition="convex" data-transition-speed="slow" data-background-image=dark-background.jpg vertical=true -->

### CNN

<img src="meta-SNE_3.png" alt="meta-SNE" style="max-height: 500px; border:none" class="fragment fade-in" data-fragment-index="3"/>


<!-- slide  data-transition="convex" data-transition-speed="slow" -->

# IV. Conclusion
