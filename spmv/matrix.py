import numpy as np
from pyamg import smoothed_aggregation_solver
from pyamg.gallery import stencil_grid
from pyamg.gallery.diffusion import diffusion_stencil_2d

n=100
X,Y = np.meshgrid(np.linspace(0,1,n),np.linspace(0,1,n))
stencil = diffusion_stencil_2d(type='FE',epsilon=0.001,theta=np.pi/3)
A = stencil_grid(stencil, (n,n), format='csr')

from pyamg.gallery.laplacian import poisson
A = poisson( (n,n) , format ='csr')
b = np.random.rand(A.shape[0])
ml = smoothed_aggregation_solver(A,
        B=X.reshape(n*n,1),
        strength='symmetric',
        aggregate='standard',
        smooth=('jacobi', {'omega': 4.0/3.0,'degree':2}),
        presmoother=('jacobi', {'omega': 4.0/3.0}), 
        postsmoother=('jacobi', {'omega': 4.0/3.0}), 
        max_levels=10,
        max_coarse=5,
        keep=False)

print ml
