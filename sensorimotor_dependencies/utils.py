import numpy as np
from sklearn import preprocessing

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