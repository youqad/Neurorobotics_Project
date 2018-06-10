from .utils import *

#------------------------------------------------------------
# Parameters

M_size = 40
E_size = 40

# Number of Joints / q
nb_joints = 4

# Number of eyes / p
nb_eyes = 2

# Number of lights / r
nb_lights = 3

# Number of exteroceptive photosensors / p'
extero = 20

# Number of proprioceptive sensors / q'
proprio = 4


# Sensory inputs were generated from...
nb_generating_motor_commands = 50
nb_generating_env_positions = 50

# Neighborhood size of the linear approximation:
# Motor commands/Environmental positions drawn from normal distribution
# with mean zero and standard deviation... 
neighborhood_size = 1e-8
# (Coordinates differing from 0 by more than the std deviation are set equal to 0)

sigma = np.tanh

class Organism1:
  """
  Organism 1:
  
    1. The arm has

      - ``nb_joints`` joints

          - each of which has ``proprio`` **proprioceptive** sensors 
          (whose outputs depend on the position of the joint)
          
      - ``nb_eyes`` eyes (for each of them: 3 spatial and 3 orientation coordinates)

          - on which there are ``extero`` omnidirectional **exteroceptive** photosensors
          
    2. the motor command is ``M_size``-dimensional  

    3. the environment consists of:

        - ``nb_lights`` lights (3 spatial coordinates and ``nb_lights`` luminance values for each of them)
        
    Other parameters:
    
    - Random seed: ``seed``
    
    - Sensory inputs are generated from ``nb_generating_motor_commands`` motor commands
      and ``nb_generating_env_positions`` environment positions
      
    - Neighborhood size of the linear approximation: ``neighborhood_size``
      i.e. Motor commands/Environmental positions drawn from normal distribution
      with mean zero and standard deviation ``neighborhood_size``
      (Coordinates differing from 0 by more than the std deviation are set equal to 0)
      
    - ``retina_size`` size of the retina: variance of the normal distribution from
      which are drawn the ``C[i,k]`` (relative position of photosensor ``k`` within eye ``i``)

    +-----------------------------------+-----------------------------------+
    | **Parameter**                     | **Value**                         |
    +===================================+===================================+
    | Dimension of motor commands       | ``M_size``                        |
    +-----------------------------------+-----------------------------------+
    | Dimension of environmental        | ``E_size``                        |
    | control vector                    |                                   |
    +-----------------------------------+-----------------------------------+
    | Dimension of proprioceptive       | ``proprio*nb_joints``             |
    | inputs                            |                                   |
    +-----------------------------------+-----------------------------------+
    | Dimension of exteroceptive inputs | ``extero*nb_eyes``                |
    +-----------------------------------+-----------------------------------+
    | Number of eyes                    | ``nb_eyes``                       |
    +-----------------------------------+-----------------------------------+
    | Number of joints                  | ``nb_joints``                     |
    +-----------------------------------+-----------------------------------+
    | Diaphragms                        | None                              |
    +-----------------------------------+-----------------------------------+
    | Number of lights                  | ``nb_lights``                     |
    +-----------------------------------+-----------------------------------+
    | Light luminance                   | Fixed                             |
    +-----------------------------------+-----------------------------------+
    
  """
  def __init__(self, seed=1, retina_size=1., M_size=M_size, E_size=E_size,
               nb_joints=nb_joints, nb_eyes=nb_eyes, nb_lights=nb_lights, 
               extero=extero, proprio=proprio, 
               nb_generating_motor_commands=nb_generating_motor_commands,
               nb_generating_env_positions=nb_generating_env_positions,
               neighborhood_size=neighborhood_size, sigma=sigma):

    self.random = np.random.RandomState(seed)

    #------------------------------------------------------------
    # Random initializations

    dim_mu1 = 3*nb_joints+3*nb_eyes+3*nb_eyes
    W_1, mu_1 = 2*self.random.rand(dim_mu1, dim_mu1)-1, 2*self.random.rand(dim_mu1)-1
    W_2, mu_2 = 2*self.random.rand(dim_mu1, M_size)-1, 2*self.random.rand(dim_mu1)-1

    dim_nu1 = 3*nb_lights
    V_1, nu_1 = 2*self.random.rand(dim_nu1, dim_nu1)-1, 2*self.random.rand(dim_nu1)-1
    V_2, nu_2 = 2*self.random.rand(dim_nu1, E_size)-1, 2*self.random.rand(dim_nu1)-1

    dim_tau1 = proprio*nb_joints
    U_1, tau_1 = 2*self.random.rand(dim_tau1, dim_tau1)-1, 2*self.random.rand(dim_tau1)-1
    U_2, tau_2 = 2*self.random.rand(dim_tau1, 3*nb_joints)-1, 2*self.random.rand(dim_tau1)-1

    theta, d = .5*self.random.rand(nb_lights)+.5, .5*self.random.rand(nb_eyes)+.5

    C = self.random.multivariate_normal(np.zeros(3), retina_size*np.identity(3), (nb_eyes, extero))

    M_0, E_0 = 10*self.random.rand(M_size)-5, 10*self.random.rand(E_size)-5

    #------------------------------------------------------------
    # Setting attributes

    self.__dict__.update((key, value) 
                         for key, value in locals().items() if key != 'self')

    self.dim_mu1, self.W_1, self.mu_1, self.W_2, self.mu_2 = dim_mu1, W_1, mu_1, W_2, mu_2
    self.dim_nu1, self.V_1, self.nu_1, self.V_2, self.nu_2 = dim_nu1, V_1, nu_1, V_2, nu_2
    self.dim_tau1, self.U_1, self.tau_1, self.U_2, self.tau_2 = dim_tau1, U_1, tau_1, U_2, tau_2
    self.theta, self.d, self.C, self.M_0, self.E_0 = theta, d, C, M_0, E_0

    self.self_table = '''**Characteristics**|**Value**
    -|-
    Dimension of motor commands|{}
    Dimension of environmental control vector|{}
    Dimension of proprioceptive inputs|{}
    Dimension of exteroceptive inputs|{}
    Number of eyes|{}
    Number of joints|{}
    Diaphragms|None
    Number of lights|{}
    Light luminance|Fixed
    '''.format(M_size, E_size, proprio*nb_joints, extero*nb_eyes, nb_eyes,
              nb_joints, nb_lights)
    
    self.random_state = self.random.get_state()

  
  def get_sensory_inputs(self, M, E):
    """
    Compute sensory inputs for motor command ``M`` and environment position ``E``

    +-----------------------------------+-----------------------------------+
    | Notation                          | Meaning                           |
    +===================================+===================================+
    | $$Q ≝ (Q_1, \\\ldots, Q_{3q})$$   | positions of the joints           |
    +-----------------------------------+-----------------------------------+
    | $$P ≝ (P_1, \\\ldots, P_{3p})$$   | positions of the eyes             |
    +-----------------------------------+-----------------------------------+
    | $$a^θ_i, a^φ_i, a^ψ_i$$           | Euler angles for the orientation  |
    |                                   | of eye \\\(i\\\)                  |
    +-----------------------------------+-----------------------------------+
    | $$Rot(a^θ_i, a^φ_i, a^ψ_i)$$      | rotation matrix for eye \\\(i\\\) |
    |                                   |                                   |
    +-----------------------------------+-----------------------------------+
    | $$C_{i,k}$$                       | relative position of photosensor  |
    |                                   | \\\(k\\\) within eye \\\(i\\\)    |
    +-----------------------------------+-----------------------------------+
    | $$d ≝ (d_1, \\\ldots,d_p)$$       | apertures of diaphragms           |
    +-----------------------------------+-----------------------------------+
    | $$L ≝ (L_1,\\\ldots,L_{3r})$$     | positions of the lights           |
    +-----------------------------------+-----------------------------------+
    | $$θ ≝ (θ_1, \\\ldots, θ_r)$$      | luminances of the lights          |
    +-----------------------------------+-----------------------------------+
    | $$S^e_{i,k}$$                     | sensory input from exteroceptive  |
    |                                   | sensor \\\(k\\\) of eye \\\(i\\\) |
    +-----------------------------------+-----------------------------------+
    | $$S^p_i$$                         | sensory input from proprioceptive |
    |                                   | sensor \\\(i\\\)                  |
    +-----------------------------------+-----------------------------------+
    | $$M, E$$                          | motor command and environmental   |
    |                                   | control vector                    |
    +-----------------------------------+-----------------------------------+

    Computing the sensory inputs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $$\\\\begin{align*}
    (Q,P,a) &≝ σ(W_1 · σ(W_2 · M − μ_2)−μ_1)\\\
    L &≝ σ(V_1 ·σ(V_2 · E − ν_2) − ν_1)\\\\\
    ∀1≤ k ≤ p', 1≤i≤p, \\\quad S^e_{i,k} &≝ d_i \\\sum\\\limits_{j} \\\\frac{θ_j}{\\\Vert P_i + Rot(a_i^θ, a_i^φ, a_i^ψ) \\\cdot C_{i,k} - L_j \\\Vert^2}\\\\\\
    (S^p_i)_{1≤ i ≤ q'q} &≝ σ(U_1 · σ(U_2 · Q − τ_2) − τ_1)\\\\\\\
    \\\end{align*}$$

    where

    -  \\\(W_1, W_2, V_1, V_2, U_1, U_2\\\) are matrices with coefficients drawn randomly from 
    a uniform distribution between \\\(−1\\\) and \\\\(1\\\)
    -  the vectors \\\(μ_1, μ_2, ν_1, ν_2, τ_1, τ_2\\\) too
    -  \\\(σ\\\) is an arbitrary nonlinearity (e.g. the hyperbolic tangent function)
    -  the \\\(C_{i,k}\\\) are drawn from a centered normal distribution 
    whose variance (which can be understood as the size of the retina) is
    so that the sensory changes resulting from a rotation of the eye are
    of the same order of magnitude as the ones resulting from a
    translation of the eye
    -  \\\(θ\\\) and \\\(d\\\) are constants drawn at random in the interval
    \\\([0.5, 1]\\\)


    Parameters
    ----------
    M : (M_size,) array
      Motor command vector
    E : (E_size,) array
      Environmental control vector
                                                                                                
    Returns
    -------
    S : (proprio*nb_joints + extero*nb_eyes,) array
    """
    Q, P, a = [arr.reshape([-1, 3]) 
                for arr in np.split(
                    self.sigma(self.W_1.dot(self.sigma(self.W_2.dot(M)-self.mu_2))-self.mu_1),
                    [3*self.nb_joints, 3*self.nb_joints+3*self.nb_eyes])]
    
    L = self.sigma(self.V_1.dot(self.sigma(self.V_2.dot(E)-self.nu_2))-self.nu_1).reshape([-1, 3])
    Sp = self.sigma(self.U_1.dot(self.sigma(self.U_2.dot(Q.flatten())-self.tau_2))-self.tau_1)
    Se = np.array([self.d[i]*
                    sum(self.theta[j]/np.linalg.norm(P[i]+Rot(a[i]).dot(self.C[i,k])-L[j])**2
                        for j in range(self.nb_lights))
                    for i in range(self.nb_eyes)
                    for k in range(self.extero)])
    S = np.concatenate((Sp, Se))
    return S

  
  def compute_proprioception(self):
    """
    Computes a mask indicating the sensory inputs the organism can reliably
    deem to be proprioceptive, since they remain silent when:
    - the motor command is fixed
    - the environment changes
    
    Useful to separate proprioceptive inputs from exteroceptive ones                                                  
                                                                                               
    Example
    -------
    >>> O = organism1.Organism1(proprio=1, nb_joints=2, extero=1, nb_eyes=2); O.compute_proprioception(); O.mask_proprio
    array([ True,  True, False, False], dtype=bool)
    """
    self.random.set_state(self.random_state)
    
    # Separating proprioceptive input from exteroceptive input
    mask_proprio = np.array([
        self.get_sensory_inputs(self.M_0,
                                self.E_0+self.random.normal(0, self.neighborhood_size, self.E_size))
        for _ in range(self.nb_generating_env_positions)])
    self.mask_proprio = np.all(mask_proprio == mask_proprio[0, :], axis=0)
    
    self.random_state = self.random.get_state()
      
  def neighborhood_lin_approx(self, size):
    """
    Neighborhood linear approximation:

    Parameters
    ----------
    size : int
      Neighborhood size of the linear approximation

    Returns
    -------
    rand_vect : (size,) array
      Random vector drawn from a normal distribution 
      with mean zero and standard deviation ``neighborhood_size`` 
      where coordinates differing from ``0`` by more than 
      the standard deviation have been set equal to ``0``
    """
    self.random.set_state(self.random_state)
    
    rand_vect = self.random.normal(0, self.neighborhood_size, size)
    rand_vect[np.abs(rand_vect) > self.neighborhood_size] = 0
    
    self.random_state = self.random.get_state()
    
    return rand_vect

  
  def compute_variations(self):
    """
    Compute the variations in the exteroceptive inputs when:
      1. only the environment changes
        - result stored in ``self.env_variations``
      2. only the motor commands change
        - result stored in ``self.mot_variations``
      3. both change
        - result stored in ``self.env_mot_variations``
    """
    self.env_variations = np.array([
        self.get_sensory_inputs(self.M_0,
                                 self.E_0+self.neighborhood_lin_approx(self.E_size))[~self.mask_proprio]
        for _ in range(self.nb_generating_env_positions)])

    self.mot_variations = np.array([
        self.get_sensory_inputs(self.M_0+self.neighborhood_lin_approx(self.M_size),
                                 self.E_0)[~self.mask_proprio]
        for _ in range(self.nb_generating_motor_commands)])

    self.env_mot_variations = np.array([
        self.get_sensory_inputs(self.M_0+self.neighborhood_lin_approx(self.M_size),
                                 self.E_0+self.neighborhood_lin_approx(self.E_size))[~self.mask_proprio]
        for _ in range(self.nb_generating_motor_commands*self.nb_generating_env_positions)])
        
  def get_dimensions(self, dim_red='PCA'):
    """
    Parameters
    ----------
    dim_red : {'PCA', 'MDA'}, optional
      Dimension reduction algorithm used to compute the number of degrees of freedom.

    Returns
    -------
    self.dim_rigid_group, self.dim_extero, self.dim_env, self.dim_env_extero : tuple(int, int, int, int)
      Estimated dimension of the rigid group of compensated movements (stored in ``self.dim_rigid_group``),
      and number of parameters needed to describe the exteroceptive variations when:
        1. only the body moves
          - this number is stored in ``self.dim_extero``
        2. only the environment changes
          - this number is stored in ``self.dim_env``
        3. both the body and the environment change
          - this number is stored in ``self.dim_env_extero``
    """
    self.compute_proprioception()
    self.compute_variations()
    
    # Now the number of degrees of freedom!
    self.dim_env = dim_reduction_dict[dim_red](self.env_variations)
    self.dim_extero = dim_reduction_dict[dim_red](self.mot_variations)
    self.dim_env_extero = dim_reduction_dict[dim_red](self.env_mot_variations)
    self.dim_rigid_group = self.dim_env+self.dim_extero-self.dim_env_extero
    
    self.dim_table = '''
    **Characteristics**|**Value**
    -|-
    '''

    end_table = '''Dimension for body (p)|{}
    Dimension for environment (e)|{}
    Dimension for both (b)|{}
    Dimension of group of compensated movements|{}
    '''.format(self.dim_extero, self.dim_env, self.dim_env_extero, self.dim_rigid_group)
    
    self.dim_table += end_table
    self.self_table += end_table

    return self.dim_rigid_group, self.dim_extero, self.dim_env, self.dim_env_extero
  
  def __str__(self):
        return self.self_table
