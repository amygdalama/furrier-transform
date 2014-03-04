import numpy as np


def step(x, y, nx=10):
    X = np.linspace(x.min(), x.max(), len(x)*nx)
    Y = np.zeros(len(x)*nx)
    for i in xrange(0,len(x)):
        for j in xrange(0,nx):
            Y[i*nx + j] = y[i]    
    return X, Y


def lerp(x, y, nx=326, nBlend=50):
    X = np.linspace(x.min(), x.max(), len(x)*nx)
    Y = np.zeros(len(x)*nx)
    for i in xrange(0,len(x)):
        for j in xrange(0,nx):
            Y[i*nx + j] = y[i]
         
    for i in xrange(0, len(x)-1):
        if i == 0:
            continue
        X_temp = X[i*nx-nBlend:i*nx+nBlend+1]
        x_temp = (X[i*nx-nBlend], X[i*nx+nBlend])
        y_temp = y[i-1:i+1]
        Y[i*nx-nBlend:i*nx+nBlend+1] = np.interp(X_temp, x_temp, y_temp)
    return X, Y