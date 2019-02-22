import numpy as np
import matplotlib
matplotlib.use('agg')

from BeamDeconvolution import elliptic2quadratic
from BeamDeconvolution import convolve
from BeamDeconvolution import deconvolve
from BeamDeconvolution import quadratic2elliptic
from BeamDeconvolution import testError



def test_elliptic2quadratic():

     for i in range(100):
         bpa = np.random.uniform()*180.-90.#deg
         bmaj = np.random.uniform()
         bmin = np.random.uniform()*bmaj

         A,B,C = elliptic2quadratic(bmaj,bmin,bpa)
         bmaj2,bmin2,bpa2 = quadratic2elliptic(A,B,C)
#         assert np.isclose(bmaj,bmaj2) and np.isclose(bmin,bmin2) and np.isclose(bpa,bpa2), "Failed to pass {},{},{} != {},{},{}".format(bmaj,bmin,bpa,bmaj2,bmin2,bpa2)

def test_convolvedeconvolve(N=100):
     for i in range(N):
         bpa = np.random.uniform()*180.-90.#deg
         bmaj = np.random.uniform()
         bmin = np.random.uniform()*bmaj

         A1,B1,C1 = elliptic2quadratic(bmaj,bmin,bpa)

         bpa2 = np.random.uniform()*180.-90.#deg
         bmaj2 = np.random.uniform()
         bmin2 = np.random.uniform()*bmaj2

         A2,B2,C2 = elliptic2quadratic(bmaj2,bmin2,bpa2)

         Ac,Bc,Cc = convolve(A1,B1,C1,A2,B2,C2)

         Ak,Bk,Ck = deconvolve(Ac,Bc,Cc,A1,B1,C1)

         bmaj2_,bmin2_,bpa2_ = quadratic2elliptic(Ak,Bk,Ck)

#         assert np.isclose(bmaj2_,bmaj2) and np.isclose(bmin2_,bmin2) and np.isclose(bpa2_,bpa2), "Failed to pass {},{},{} != {},{},{}".format(bmaj2_,bmin2_,bpa2_,bmaj2,bmin2,bpa2)

def test_deltaFunctionDeconvolve():
     bpa = np.random.uniform()*180.-90.#deg
     bmaj = np.random.uniform()
     bmin = np.random.uniform()*bmaj

     A1,B1,C1 = elliptic2quadratic(bmaj,bmin,bpa)
     #deconv same beam
     Ak,Bk,Ck = deconvolve(A1,B1,C1,A1,B1,C1)
     bmaj_d, bmin_d, bpa_d = quadratic2elliptic(Ak,Bk,Ck)
#     assert bmaj_d==0 and bmin_d==0 and bpa_d==0,"Supposed to be the delta"

def test_test_error():
    testError(show_plot=False)
