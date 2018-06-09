import numpy as np

from sklearn import preprocessing
from scipy.spatial import distance

#------------------------------------------------------------
# Rotation matrix computation

def Rot(euler_angles):
    """                                                                                       
    Compute rotation matrix corresponding the given Euler angle
    cf. https://en.wikipedia.org/wiki/Euler_angles#Rotation_matrix                                                                
    """
    R = np.empty((3,3))
    c = np.cos(euler_angles)
    s = np.sin(euler_angles)

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

#------------------------------------------------------------
# PCA to compute the degrees of freedom

def PCA(data, return_matrix=False):
    """                                                                                       
    Principal Component Analysis (PCA) to compute the number of degrees of freedom.

    Parameters                                                                                
    ----------                                                                                
    data : (n, k) array                                                                          
        Data points matrix (data points = row vectors in the matrix)
    return_matrix : bool
        If True, returns the matrix of the data points projection on the eigenvectors                                                       
                                                                                               
    Returns                                   
    -------                                                                                
    nb : int                                                                        
        Number of non-zero eigenvalues of the covariance matrix,
        thought of as the number of degrees of freedom.
        The eigenvalues thereof fall into two classes (non-zero and zero eigenvalues) \\\(V_1\\\) and \\\(V_2\\\),
        distinguished as follows: 
        > each \\\(λ ∈ V_1\\\) has a size closer to other the \\\(λ\\\)'s of \\\(V_1\\\) 
        than the ones of \\\(V_2\\\), and conversely. 
        The boundary between \\\(V_1\\\) and \\\(V_2\\\) corresponds to the largest ratio \\\(λ_{i+1}/λ_i\\\),
        where the \\\(λ_i\\\) are in decreasing order.
    Proj : (n, dim_rigid_group) array                                                                          
        If return_matrix == True: Projection of the data points on the eigenvectors                                                     
    """

    # Covariance matrix
    cov_matrix = np.cov(preprocessing.scale(data.T))

    # Diagonalization of the covariance matrix
    eig_val, eig_vec = np.linalg.eigh(cov_matrix)
    
    # Compute the boundary index separating zero eigenvalues to non-zero ones
    max_ratio = np.argmax([eig_val[i+1]/eig_val[i] for i in range(len(eig_val)-1)])
    
    if return_matrix:
        # Projection of the data points over the eigenvectors 
        Proj = data.dot(eig_vec[:,max_ratio+1:])
        return len(eig_val[max_ratio+1:]), Proj

    return len(eig_val[max_ratio+1:])

#------------------------------------------------------------
# Classical multidimensional scaling (MDS)

def MDS(data, return_matrix=False):
    """                                                                                       
    Classical multidimensional scaling (MDS) to compute the number of degrees of freedom
    cf. https://en.wikipedia.org/wiki/Multidimensional_scaling#Classical_multidimensional_scaling
                                                                                               
    Parameters                                                                                
    ----------                                                                                
    data : (n, k) array                                                                          
        Data points matrix (data points = row vectors in the matrix)
    return_matrix : bool
        If True, returns the coordinate matrix                                                      
                                                                                               
    Returns                                   
    -------                                                                               
    nb : int                                                                        
        Number of non-zero eigenvalues of $$B = X X^T$$ (where \\\(X\\\) is the coordinate matrix), 
        thought of as the number of degrees of freedom.
        The eigenvalues thereof fall into two classes (non-zero and zero eigenvalues) \\\(V_1\\\) and \\\(V_2\\\),
        distinguished as follows: 
        > each \\\(λ ∈ V_1\\\) has a size closer to other the \\\(λ\\\)'s of \\\(V_1\\\) 
        than the ones of \\\(V_2\\\), and conversely. 
        The boundary between \\\(V_1\\\) and \\\(V_2\\\) corresponds to the largest ratio \\\(λ_{i+1}/λ_i\\\),
        where the \\\(λ_i\\\) are in decreasing order.
    X : (n, dim_rigid_group) array                                                                          
        If return_matrix == True: Coordinate matrix.                                                    
    """
    
    # Number of points                                                                        
    n = len(data)

    # 1. Squared Symmetric pairwise distance matrix.
    D_sq = distance.cdist(data, data, 'euclidean')**2
 
    # Centering matrix                                                                        
    J = np.eye(n)-np.ones((n, n))/n
 
    # 2. Double centering: B = X X^T                                                                                    
    B = -J.dot(D_sq).dot(J)/2
 
    # 3. Diagonalize
    eig_val, eig_vec = np.linalg.eigh(B)

    # Compute the boundary index separating zero eigenvalues to non-zero ones
    max_ratio = np.argmax([eig_val[i+1]/eig_val[i] for i in range(len(eig_val)-1)])
    
    if return_matrix:
        # Compute the coordinate matrix
        Λ_sqrt  = np.diag(np.sqrt(eig_val[max_ratio+1:]))
        E  = eig_vec[max_ratio+1:]
        X  = E.dot(Λ_sqrt)
        return len(eig_val[max_ratio+1:]), X
    
    return len(eig_val[max_ratio+1:])

#------------------------------------------------------------
# Dictionary to access the dimension reduction functions in the classes later

dim_reduction_dict = {'PCA': PCA, 'MDS': MDS}