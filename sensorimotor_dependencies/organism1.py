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

      - `nb_joints` joints

          - each of which has `proprio` **proprioceptive** sensors 
          (whose outputs depend on the position of the joint)
          
      - `nb_eyes` eyes (for each of them: 3 spatial and 3 orientation coordinates)

          - on which there are `extero` omnidirectional **exteroceptive** photosensors
          
    2. the motor command is `M_size`-dimensional  

    3. the environment consists of:

        - `nb_lights` lights 
          (3 spatial coordinates and `nb_lights` luminance values for each of them)
        
    Other parameters:
    
    - Random seed: `seed`
    
    - Sensory inputs are generated from `nb_generating_motor_commands` motor commands
      and `nb_generating_env_positions` environment positions
      
    - Neighborhood size of the linear approximation: `neighborhood_size`
      i.e. Motor commands/Environmental positions drawn from normal distribution
      with mean zero and standard deviation `neighborhood_size`
      (Coordinates differing from 0 by more than the std deviation are set equal to 0)
      
    - `retina_size` size of the retina: variance of the normal distribution from
      which are drawn the C[i,k] (relative position of photosensor k within eye i)
      
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
    Compute sensory inputs for motor command M and environment position E
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
    return np.concatenate((Sp, Se))

  
  def compute_proprioception(self):
    """
    Computes a mask indicating the sensory inputs the organism can reliably
    deem to be proprioceptive, since they remain silent when:
    - the motor command is fixed
    - the environment changes
    
    Useful to separate proprioceptive inputs from exteroceptive ones
    """
    self.random.set_state(self.random_state)
    
    # Separating proprioceptive input from exteroceptive input
    mask_proprio = np.array([
        self.get_sensory_inputs(self.M_0,
                                self.E_0+self.random.normal(0, self.neighborhood_size, self.E_size))
        for _ in range(self.nb_generating_env_positions)])
    self.mask_proprio = np.all(mask_proprio == mask_proprio[0, :], axis=0)
    
    self.random_state = self.random.get_state()
      
  def _neighborhood_lin_approx(self, size):
    self.random.set_state(self.random_state)
    
    rand_vect = self.random.normal(0, self.neighborhood_size, size)
    rand_vect[np.abs(rand_vect) > self.neighborhood_size] = 0
    
    self.random_state = self.random.get_state()
    
    return rand_vect

  
  def compute_variations(self):
    """
    Compute the variations in the exteroceptive inputs when:
    1. only the environment changes
    2. only the motor commands change
    3. both change
    """
    self.env_variations = np.array([
        self.get_sensory_inputs(self.M_0,
                                 self.E_0+self._neighborhood_lin_approx(self.E_size))[~self.mask_proprio]
        for _ in range(self.nb_generating_env_positions)])

    self.mot_variations = np.array([
        self.get_sensory_inputs(self.M_0+self._neighborhood_lin_approx(self.M_size),
                                 self.E_0)[~self.mask_proprio]
        for _ in range(self.nb_generating_motor_commands)])

    self.env_mot_variations = np.array([
        self.get_sensory_inputs(self.M_0+self._neighborhood_lin_approx(self.M_size),
                                 self.E_0+self._neighborhood_lin_approx(self.E_size))[~self.mask_proprio]
        for _ in range(self.nb_generating_motor_commands*self.nb_generating_env_positions)])
        
  def get_dimensions(self):
    """
    Compute the number of parameters needed to describe the exteroceptive variations when:
    1. only the environment changes
    2. only the body moves
    3. both the body and the environment change
    
    and then compute the estimated dimension of the group of compensated movements
    """
    self.compute_proprioception()
    self.compute_variations()
    
    # Now PCA!
    self.dim_env = PCA(self.env_variations)
    self.dim_extero = PCA(self.mot_variations)
    self.dim_env_extero = PCA(self.env_mot_variations)
    self.dim_rigid_group = self.dim_env+self.dim_extero-self.dim_env_extero
    
    # MDS
    new_env = mds(self.env_variations)
    
    print('new env data = ', new_env)  
    plt.scatter(new_env[0], new_env[1])
    plt.show

    new_extero = mds(self.mot_variations)
    new_env_extero = mds(self.env_mot_variations)

    
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
