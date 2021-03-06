import argparse
import click
import itertools
import librosa
import numpy as np
import os
import sys
import time

_EPS = 1e-14

def simpleab(seq_a, seq_b, subseq_len):
    
    # prerequisites
    ndim = seq_b.shape[0]    
    seq_a_len = seq_a.shape[1]
    seq_b_len = seq_b.shape[1]
    
    matrix_profile_len = seq_a_len - subseq_len + 1;
    
    # the "inverted" dot products will be used as the first value for reusing the dot products
    prods_inv = np.full([ndim,seq_a.shape[1]+subseq_len-1], np.inf)
    first_subseq = np.flip(seq_b[:,0:subseq_len],1)  
    for i_dim in range(0,ndim):
        prods_inv[i_dim,:] = np.convolve(first_subseq[i_dim,:],seq_a[i_dim,:])
    prods_inv = prods_inv[:, subseq_len-1:seq_a.shape[1]]
       
    # windowed cumulative sum of the sequence b
    seq_b_cum_sum2 = np.insert(np.sum(np.cumsum(np.square(seq_b),1),0), 0, 0)
    seq_b_cum_sum2 = seq_b_cum_sum2[subseq_len:]-seq_b_cum_sum2[0:seq_b_len - subseq_len + 1]
    
    subseq_cum_sum2 = np.sum(np.square(seq_a[:,0:subseq_len]))
    
    # first distance profile
    first_subseq = np.flip(seq_a[:,0:subseq_len],1)
    dist_profile = seq_b_cum_sum2 + subseq_cum_sum2
    
    prods = np.full([ndim,seq_b_len+subseq_len-1], np.inf)
    for i_dim in range(0,ndim):
        prods[i_dim,:] = np.convolve(first_subseq[i_dim,:],seq_b[i_dim,:])
        dist_profile -= (2 * prods[i_dim,subseq_len-1:seq_b_len])
    prods = prods[:, subseq_len-1:seq_b_len] # only the interesting products
        
    matrix_profile = list(np.full(matrix_profile_len, np.inf))
    matrix_profile[0] = dist_profile[:-1]

    mp_index = -np.ones((matrix_profile_len), dtype=int)
    mp_index[0] = np.argmin(dist_profile)

    # for all the other values of the profile
    for i_subseq in range(1,matrix_profile_len):
        
        sub_value = seq_a[:,i_subseq-1, np.newaxis] * seq_b[:,0:prods.shape[1]-1]
        add_value = seq_a[:,i_subseq+subseq_len-1, np.newaxis] * seq_b[:, subseq_len:subseq_len+prods.shape[1]-1]
        
        prods[:,1:] = prods[:,0:prods.shape[1]-1] - sub_value + add_value
        prods[:,0] = prods_inv[:,i_subseq]
        
        subseq_cum_sum2 += -np.sum(np.square(seq_a[:,i_subseq-1])) + np.sum(np.square(seq_a[:,i_subseq+subseq_len-1]))
        dist_profile = seq_b_cum_sum2 + subseq_cum_sum2 - 2 * np.sum(prods,0)
        
        matrix_profile[i_subseq] = dist_profile[:-1]
        mp_index[i_subseq] = np.argmin(dist_profile)
        
    return np.array(matrix_profile), mp_index

