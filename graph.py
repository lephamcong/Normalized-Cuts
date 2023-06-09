#Import libraries
from pylab import *
from scipy.sparse import *
import cv2
from numpy.lib import stride_tricks
from skimage.transform import resize
import math
import numpy as np
from numpy.linalg import norm


#Load image for test
path1 = r"Image_processing/Normalized-Cuts/Kodak/1.png"  # Input 1
src1 = cv2.imread(path1,0)
src1 = resize(src1, (src1.shape[0] // 4, src1.shape[1] // 4),anti_aliasing=True)
path2  = r"Image_processing/Normalized-Cuts/Kodak/12.png"            #Input 2
src2 = cv2.imread(path2,0)
src2 = resize(src2, (src2.shape[0] // 4, src2.shape[1] // 4),anti_aliasing=True)

                                #Get indices of radius R
def indRad(img,r) :
    '''
    I/p to function
    img : Image whose information is to be extracted
    r : measure of neighbourhood
    O/ps of function
    indptr : Gives which set of indices is for which set of rows
    indrow : 1D array containing row values needed to be filled by wgt matrix
    indcol : 1D array containing column values needed to be filled by wgt matrix
    indcenr : 1D array containing the centre pixel row indices around which weight is found
    indcenc : 1D array containing the centre pixel column indices around which weight is found
    indices : Suitable format for sparse matrix generation
    '''
    print("Entered indRad")
    V = len(img.flatten())      #No of vertices in graph
    Nrow = img.shape[0]         #No of rows in image
    Ncol = img.shape[1]        #Vectors to containing centres
    rowvec = (np.arange(Nrow).repeat(Ncol)).reshape(1,V)
    colvec = np.array(list(np.arange(Ncol))*Nrow).reshape(1,V)
    one = np.ones((1,int(2*r+1),int(2*r+1)))
                                #Blocks of centres used for computing radius around it
    blkcenr = (one.T @ rowvec).T
    blkcenc = (one.T @ colvec).T
                                #Create a square wall of -(r+2) around the image
    ind = -(r+2)*np.ones((2,img.shape[0]+int(2*r),img.shape[1]+int(2*r)))
    ind[:,r:-r,r:-r] = np.indices(img.shape)   #This is (2,N,N) hence need patch for row and col
    indr = ind[0]
    indc = ind[1]               #Create patches/blocks of these indices around each pixel as centre
    strides = indr.strides*2
    size = int(2*r)+1           #Patch for row indices
    dim = (indr.shape[0] - size + 1, indr.shape[1] - size + 1, size, size)
    patchr = stride_tricks.as_strided(indr, shape=dim, strides=strides)
    patchr = patchr.reshape(V,size,size)
                                
    strides = indc.strides*2    #Patch for column indices
    size = int(2*r)+1
    dim = (indc.shape[0] - size + 1, indc.shape[1] - size + 1, size, size)
    patchc = stride_tricks.as_strided(indc, shape=dim, strides=strides)
    patchc = patchc.reshape(V,size,size)
                                #Blockwise distance of each point from centre
    diffr = patchr - blkcenr
    diffc = patchc - blkcenc
    
    indnorm = norm(np.array([diffr,diffc]),axis = 0)   
    fullind = np.where((indnorm <= r))          #Find the indices in radius r
    indcen = fullind[0]                         #The centre indices values with neighbours within their radius
    indcenc = indcen % img.shape[1]              #Obtain indcenc
    indcenr = (indcen-indcenc)// img.shape[1]   #Obtain indcenr
    
    indrow = fullind[1]+indcenr-r               #Obtain indrow
    indcol = fullind[2]+indcenc-r               #Obtain indcol
    indices = indrow*img.shape[1] + indcol     #Suitable format for sparse matrix generation
        
    indptr = np.cumsum(np.unique(fullind[0],return_counts= True)[1])
    indptr = np.array([0] + list(indptr))          #Obtain indptr
    
    return indptr,indrow,indcol,indcenr,indcenc,indices
   
                                #Find the weight function    
def wval(img,indrow,indcol,indcenr,indcenc,sigI,sigX) :
    '''
    I/ps to function
    img : Image whose information is to be extracted
    indrow : 1D array containing row values needed to be filled by wgt matrix
    indcol : 1D array containing column values needed to be filled by wgt matrix
    indcenr : 1D array containing the centre pixel row indices around which weight is found
    indcenc : 1D array containing the centre pixel column indices around which weight is found
    sigI : Image variance
    sigX : Index variance
    O/p of function
    wgt : weight values of the graph corresponding to the indices
    '''
    print("Entered wval")
                                #Image intensity contribution to weight
    imgexp = np.exp(-1*((img[indrow,indcol] - img[indcenr,indcenc])**2)/(sigI**2))
                                #Index distance contribution to weight
    indexp = np.exp(-(norm(np.array([indrow,indcol])-np.array([indcenr,indcenc]),axis=0)**2)/(sigX**2))
    wgt = imgexp*indexp         #Define the weight values
    
    return wgt                                   
    
                                #Generate weighted graph
def wgraph(img,sigI=0.1/math.sqrt(3),sigX=4,r=7) :
    '''
    I/p to function
    img : Image whose information is to be extracted
    sigI : Image variance
    sigX : Index variance
    r : measure of neighbourhood
    O/p of function
    graph : sparse matrix consisting of the values,indices of weighted graph
    '''
    print("Entered wgraph")
    V = len(img.flatten())          #Obtain radius indices and weights
    indptr,indrow,indcol,indcenr,indcenc,indices = indRad(img,r)
    wgt = wval(img,indrow,indcol,indcenr,indcenc,sigI,sigX)
                                    #Define the weight-sparse matrix
    graph = csr_matrix((wgt,indices,indptr),shape=(V,V))
        
    return graph
                                    #Generate D matrix
def Dgraph(graph) :
    '''
    I/p to function
    graph : Sparse matrix representing the weighted graph
    O/p of function
    D : matrix D with sum of weights of each node
    '''
    print("Entered Dgraph")         #Sum all weights of each pixel = dij
    diagD = np.asarray(csr_matrix.sum(graph,axis = 1)).reshape(-1)
    V = len(diagD)                  #diag sparse matrix
    D = diags(diagD,shape = (V,V))
    
    return D

