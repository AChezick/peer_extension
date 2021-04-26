import numpy as np
import pandas as pd
import scipy.stats as stats

def try2(x):
    return x

def content_filter(q):
    '''
    Input: a dictionary with keys as time
    Output: a
    '''
    content_df={}
    for item in q:

        time = item[2] 
        time2 = item[2][10:16]
        status = str(item[3])
        n_likes=str(item[4])
        photo_check = str(item[5])
        
        if n_likes != 'None':
            n_likes = int( ''.join(n_likes.strip(':') )) 
        if status != 'True' and status != 'False':
            status = int(status)
        vals = [time,status,n_likes,photo_check]
        content_df[time2] = vals    
        
    return content_df      

def content_filter2(q):
    content_df={}
    for item in q:

        time = item[2] 
        time2 = item[2][10:16]
        status = str(item[3])
        n_likes=str(item[4])
        photo_check = str(item[5])
        
        if n_likes != 'None':
            n_likes = int( ''.join(n_likes.strip(':') )) 
        if status != 'True' and status != 'False':
            status = int(status)
        vals = [time,status,n_likes,photo_check]
        content_df[time2] = vals    
        
    return content_df      

def ho_testing(x):
    '''
    Inputs: x= list of lists   
    output: a p_value 
    '''
    
    return stats.ttest_ind(x[0],x[1],equal_var =False, alternative = 'greater')

if __name__ =='__main__':
     