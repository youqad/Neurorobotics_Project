import numpy as np
from sklearn import preprocessing

#------------------------------------------------------------
#@title Parameters

M_size = 40 #@param {type:"slider", min:10, max:100, step:5}
E_size = 40 #@param {type:"slider", min:10, max:100, step:5}

# Number of Joints / q
nb_joints = 4 #@param {type:"slider", min:3, max:5, step:1}

# Number of eyes / p
nb_eyes = 2 #@param {type:"slider", min:2, max:5, step:1}

# Number of lights / r
nb_lights = 3 #@param {type:"slider", min:2, max:5, step:1}

# Number of exteroceptive photosensors / p'
extero = 20 #@param {type:"slider", min:15, max:25, step:1}

# Number of proprioceptive sensors / q'
proprio = 4 #@param {type:"slider", min:3, max:5, step:1}


# Sensory inputs were generated from...
nb_generating_motor_commands = 50 #@param {type:"slider", min:10, max:200, step:10}
nb_generating_env_positions = 50 #@param {type:"slider", min:10, max:200, step:10}

# Neighborhood size of the linear approximation:
# Motor commands/Environmental positions drawn from normal distribution
# with mean zero and standard deviation... 
neighborhood_size = 1e-8
# (Coordinates differing from 0 by more than the std deviation are set equal to 0)

sigma = np.tanh

#------------------------------------------------------------
# Rotation matrix computation

def Rot(euler_angles):
  R = np.empty((3,3))
  c = np.cos(euler_angles)
  s = np.sin(euler_angles)

  # cf. https://en.wikipedia.org/wiki/Euler_angles#Rotation_matrix 
  R[0,0] = c[0]*c[2] - c[1]*s[0]*s[2]
  R[0,1] = -c[0]*s[2] - c[1]*c[2]*s[0]
  R[0,2] = s[0]*s[1]

  R[1,0] = s[0]*c[2] + c[0]*c[1]*s[2]
  R[1,1] = c[0]*c[1]*c[2] - s[0]*s[2]
  R[1,2] = -c[0]*s[1]

  R[2,0] = s[1]*s[2]
  R[2,1] = -c[2]*s[1]
  R[2,2] = c[1]

  return R

# PCA to compute the degrees of freedom
def PCA(data):
  cov_matrix = np.cov(preprocessing.scale(data.T))
  eig_val, _ = np.linalg.eigh(cov_matrix)
  
  #print(cov_matrix)
  #print([eig_val[i+1]/eig_val[i] for i in range(len(eig_val)-1)])
  
  max_ratio = np.argmax([eig_val[i+1]/eig_val[i] for i in range(len(eig_val)-1)])
  
  return len(eig_val[max_ratio+1:])
#------------------------------------------------------------