from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.core.math.integer import randomBits,integer,bitsize
from charm.toolbox.hash_module import Hash,int2Bytes,integer
from functools import reduce
import time
import numpy as np


# the length of vectors m = 5
# the depth of hierarchical d = 6
# the length of HID l = 5
# the length of tag t = 1

def setup(m, d, n, param_id='SS512'):
    group = PairingGroup(param_id)
    alpha = group.random(ZR)
    g = group.random(G1)
    f = group.random(G1)
    
    g_alpha = g ** alpha
    
    # the length of vectors n = 5
    h_dict = gen_h(m)
    
    # the depth of hierarchical d = 6, d+1
    u_dict = gen_u(d)
    
    # the number of tag n = 2 #5
    f_dict = gen_f(n)
    
    params = { 'g': g, 'g_alpha': g_alpha, 'f': f, 'h_dict': h_dict, 
              'u_dict': u_dict, 'f_dict': f_dict}
    msk = alpha
    return (params, msk)


def gen_u(d): # bulid u
    
    u_list = []
    u_dict = {}

    for i in range(1, d+2):
        u_list.append(f"u_{i}")

    u_values = group.random(G1, d+2)
    
    for u, value in zip(u_list, u_values):
        u_dict.update({f"{u}": value})
        
    return u_dict

def gen_h(m): # build h
    h_list = []
    h_dict = {}

    for i in range(1, m+1):
        h_list.append(f"h_{i}")

    h_values = group.random(G1, m+1)
    
    for h, value in zip(h_list, h_values):
        h_dict.update({f"{h}": value})
        
    return h_dict


def gen_f(n): # build f
    f_list = []
    f_dict = {}

    for i in range(0, n+1):
        f_list.append(f"f_{i}")

    f_values = group.random(G1, n+1)
    
    for f, value in zip(f_list, f_values):
        f_dict.update({f"{f}": value})
        
    return f_dict


def genHID(l):
    HID = []
    HID_name = []
    ## get l HID
    for i in range(1, l+1):
        r = group.random(ZR)
        HID.append(r)
        HID_name.append("ID_%d"%(i))
    HID_dict = dict(zip(HID_name, HID))
    return HID_dict


def genvec(m):
    vec = [] 
    vec_name = []
    ## get m vector
    for i in range(1,m+1):
        r = group.random(ZR)
        vec.append(r)
        vec_name.append("vec_%d"%(i))
    vec_dict = dict(zip(vec_name, vec))
    return vec_dict


def gen_ploynomial(tags, n):
    # list tags, number of tag n 
    
    # Create the polynomial object
    poly = np.poly1d(tags, True)
    
    coeffi_vec = []
    coeffi_vec_name = []
    
    for i, key in enumerate(poly.coeffs):
        coeffi_vec.append(key)
        coeffi_vec_name.append("z_%d"%(i))
    coeffi_vec = dict(zip(coeffi_vec_name, coeffi_vec))
    
    return coeffi_vec, poly


def KeyGen(params, msk, HID_dict, vec_y):
    t = group.random(ZR)
    t_0  = group.random(ZR)
    r_ID = group.random(ZR)
    
    T = []
    
    h_i_v_i = {}
    u_ID_i = {}
    
    # vec m = 5, HID l = 5
    for i in range(1, len(HID_dict)+1):
        h_i_v_i.update({f"h_{i}_v_{i}": params['h_dict'][f"h_{i}"]**vec_y[f"vec_{i}"]})
        u_ID_i.update({f"u_ID_{i}": params['u_dict'][f"u_{i}"]**HID_dict[f"ID_{i}"]})
  
    result_h_i_v_i = reduce(lambda x, y: x*y, h_i_v_i.values())
    result_u_ID_i = reduce(lambda x, y: x*y, u_ID_i.values())
    
    K_h = (result_h_i_v_i**msk)*(result_u_ID_i*params['u_dict']['u_6'])**(-t)
    
    K_6 = params['u_dict']['u_6'] ** t
    K_7 = params['u_dict']['u_7'] ** t
    
    sk_01 = (params['f']**msk)*(params['f_dict']['f_0']**t)*(result_u_ID_i*params['u_dict']['u_6'])**r_ID
    
    sk_02 = {}
    f_count = 2
    for i in range(1, f_count+1):
        sk_02[f"sk_02_{i}"] = ((params['f_dict']['f_0'])**(t_0**i)/params['f_dict'][f"f_{i}"])**t

    sk_3 = params['g'] ** t
    sk_4 = params['g'] ** r_ID
    sk_5 = {'sk_5_1': params['u_dict']['u_1']**r_ID, 'sk_5_2': params['u_dict']['u_2']**r_ID, 
            'sk_5_3': params['u_dict']['u_3']**r_ID, 'sk_5_4': params['u_dict']['u_4']**r_ID, 
            'sk_5_5': params['u_dict']['u_5']**r_ID, 'sk_5_6': params['u_dict']['u_6']**r_ID,
            'sk_5_7': params['u_dict']['u_7']**r_ID}
    
    SK = {'vec_y': vec_y, 'K_h': K_h, 'K_6': K_6, 'K_7': K_7,
          'sk_01': sk_01, 'sk_02': sk_02, 'sk_3': sk_3, 'sk_4': sk_4, 'sk_5': sk_5, 't_0': t_0, 'T': T, 't': t}
    return SK


def Delegate(params, SK, HID_dict, ID_l_1):
    t_prime = group.random(ZR)
    r_ID_prime = group.random(ZR)
    T = SK['T']
    
    # SK = {'vec_y': vec_y, 'K_h': K_h, 'K_5': K_5, 'K_6': K_6,
    #      'sk_01': sk_01, 'sk_02': sk_02, 'sk_3': sk_3, 'sk_4': sk_4, 'sk_5': sk_5, 't_0': t_0, 'T': T, 't': t}
        
    left = SK['K_h']*(SK['K_6']**(-ID_l_1))
    u_ID_1 = params['u_dict']['u_1']**HID_dict['ID_1']
    u_ID_2 = params['u_dict']['u_2']**HID_dict['ID_2']
    u_ID_3 = params['u_dict']['u_3']**HID_dict['ID_3']
    u_ID_4 = params['u_dict']['u_4']**HID_dict['ID_4']
    u_ID_5 = params['u_dict']['u_5']**HID_dict['ID_5']
    
    u_ID_6 = params['u_dict']['u_6']**ID_l_1
    
     
    K_h_prime = left *(u_ID_1*u_ID_2*u_ID_3*u_ID_4*u_ID_5*u_ID_6*params['u_dict']['u_7'])**(-t_prime)
    
    K_7_prime = SK['K_7']*(params['u_dict']['u_7']**(t_prime))
    K_d_prime = SK['K_6']*(params['u_dict']['u_6']**(t_prime))
    
    sk_01_prime = SK['sk_01']*(params['u_dict']['u_7']**r_ID_prime)*(SK['sk_5']['sk_5_6']**ID_l_1)*((u_ID_1*u_ID_2*u_ID_3*u_ID_4*u_ID_5*u_ID_6)**r_ID_prime)
    
    sk_3_prime = SK['sk_3']*(params['g']**(t_prime))
    sk_4_prime = SK['sk_4']*(params['g']**r_ID_prime)
    sk_5_prime = {'sk_5_7': SK['sk_5']['sk_5_7']*(params['u_dict']['u_7']**r_ID_prime),
                  'sk_5_6': SK['sk_5']['sk_5_6']*(params['u_dict']['u_6']**r_ID_prime)}
    
    Dele_SK = {'vec_y': vec_y, 'K_h': K_h_prime, 'K_7': K_7_prime, 'K_d': K_d_prime,
               'sk_01': sk_01_prime, 'sk_02': SK['sk_02'], 'sk_3': sk_3_prime,
               'sk_4': sk_4_prime, 'sk_5': sk_5_prime, 't_0': SK['t_0'], 'T': T}
    
    return Dele_SK


# the length of encrypted tag S_n = 1
def Enc(params, HID_dict, vec_x):
    r = group.random(ZR)
    tag = group.random(ZR)
    
    u_ID_i = {}
    for i in range(1, len(HID_dict)+1):
        u_ID_i.update({f"u_ID_{i}": params['u_dict'][f"u_{i}"]**HID_dict[f"ID_{i}"]})
  
    result_u_ID_i = reduce(lambda x, y: x*y, u_ID_i.values())
    
    right_add = pair(params['g_alpha'], params['f'])**r
    
    tags = [tag]
    coeffi_vec, poly = gen_ploynomial(tags, 1)
    
    C_x_i = {}
    for i in range(1, len(vec_x)+1):
        C_x_i.update({f"C_x_{i}": (pair(params['g'], params['g'])**vec_x[f'vec_{i}'])*(pair(params['g_alpha'], params['h_dict'][f'h_{i}'])**r)*right_add})
    
    C_1 = params['g']**r
    C_2 = (result_u_ID_i*params['u_dict']['u_6'])**r
    C_3 = ((params['f_dict']['f_0']**coeffi_vec['z_0'])*(params['f_dict']['f_1']**coeffi_vec['z_1'])*r)
    
    CT = {'C_x_i': C_x_i, 'C_1': C_1, 'C_2': C_2, 'C_3': C_3}
    return CT, coeffi_vec, poly


def Punct(params, SK, t):
    
    r_i = group.random(ZR)
    r_prime = group.random(ZR)
    lambda_0, lambda_i = group.random(ZR, 2)
    
    t_i = t ## random number
    SK['T'].append(t)
    
    sk_01_prime = SK['sk_01']*(params['f']**lambda_0)*(params['f_dict']['f_0']**r_prime)
    sk_02_prime = {}
    for i, key in enumerate(SK['sk_02']):
        sk_02_prime[f"sk_02_prime_{i+1}"] = SK['sk_02'][key] * ((params['f_dict']['f_0'])**(SK['t_0']**(i+1))/params['f_dict'][f"f_{i+1}"])**r_prime
    
    sk_03_prime = SK['sk_3']*params['g']**r_prime
    
    sk_i_1 = (params['f']**lambda_i)*(params['f_dict']['f_0']**r_i)
    sk_i_2 = params['g']**r_i
    sk_i_3 = {}
    for i, key in enumerate(SK['sk_02']):
        sk_i_3[f"sk_i_3_{i+1}"] = ((params['f_dict']['f_0'])**(t_i**(i+1))/params['f_dict'][f"f_{i+1}"])**r_i


    SK_HID_T = {'vec_y': SK['vec_y'], 'K_h': SK['K_h'], 'K_6': SK['K_6'], 'K_7': SK['K_7'],
                'sk_01': sk_01_prime, 'sk_02': sk_02_prime, 'sk_03': sk_03_prime,
                'sk_1_1': sk_i_1, 'sk_1_2': sk_i_2, 'sk_1_3': sk_i_3,
                'sk_3': SK['sk_3'], 'sk_4': SK['sk_4'], 'sk_5': SK['sk_5'], 't_0': SK['t_0'], 'T': SK['T']}
    return SK_HID_T
    

def Dec(params, CT, SK_HID_T, coeffi_vec, poly):
    k_0 = (SK['sk_02']['sk_02_1']**coeffi_vec['z_1'])    
    f_0 = SK['t_0']*coeffi_vec['z_1'] + coeffi_vec['z_0']
 
    A = pair(SK['sk_01'], CT['C_1'])/pair(SK['sk_4'], CT['C_2'])/(pair(k_0, CT['C_1'])*pair(SK['sk_3'], CT['C_3']))**(1/f_0)
       
    C_xi_prime = {}
    for i in range(1, len(vec_x)+1):
        C_xi_prime.update({f"C_x{i}_prime": CT['C_x_i'][f"C_x_{i}"]/(A)})
    
    left = (C_xi_prime['C_x1_prime']**SK_HID_T['vec_y']['vec_1'])*(C_xi_prime['C_x2_prime']**SK_HID_T['vec_y']['vec_2'])*(C_xi_prime['C_x3_prime']**SK_HID_T['vec_y']['vec_3'])*(C_xi_prime['C_x4_prime']**SK_HID_T['vec_y']['vec_4'])*(C_xi_prime['C_x5_prime']**SK_HID_T['vec_y']['vec_5'])
    mid = pair(CT['C_1'], SK_HID_T['K_h'])**(-1)
    right = pair(CT['C_2'], SK_HID_T['sk_3'])**(-1)
    
    pair_inner = left*mid*right
    
    return pair_inner


def cal_time():
    list_time = []
    temp = 0
    start = time.time()
    for i in range(1,1001):
        ## insert which calculation you want
    end = time.time()
    temp += end - start
    list_time.append(temp)
    print(list_time)
    
if __name__ == '__main__':
    param_id = 'SS512'
    params = setup(param_id)
    group = PairingGroup(param_id)

    ## System Setup
    params, msk = setup(5, 6, 2, param_id)

    ## Generate HID
    HID_dict = genHID(5)

    ## Generate vector
    vec_x = genvec(5)
    vec_y = genvec(5)

    ## Key Generate
    SK = KeyGen(params, msk, HID_dict, vec_y)

    ## Encryption 
    CT, coeffi_vec, poly = Enc(params, HID_dict, vec_x)

    ## Decryption
    plaintext = Dec(params, CT, SK, coeffi_vec, poly)

    ## Puncture
    #t_1 = 5
    #SK_HID_T = Punct(params, SK, t_1)

    ## Delegate
    #Dele_SK = Delegate(params, SK, ID_l_1)

    ## Check inner product
    inner_product = vec_x['vec_1']*vec_y['vec_1']+vec_x['vec_2']*vec_y['vec_2']+vec_x['vec_3']*vec_y['vec_3']+vec_x['vec_4']*vec_y['vec_4']+vec_x['vec_5']*vec_y['vec_5']
    pair_inner = pair(params['g'], params['g'])**inner_product

    if plaintext == pair_inner:
        print(True)


#### Delegate key Re-encryption 

def Del_Enc(params, HID_dict, vec_x):
    r = group.random(ZR)
    
    u_ID_1 = params['u_1']**HID_dict['ID_1']
    u_ID_2 = params['u_2']**HID_dict['ID_2']
    u_ID_3 = params['u_3']**HID_dict['ID_3']
    u_ID_4 = params['u_4']**HID_dict['ID_4']
    u_ID_5 = params['u_5']**HID_dict['ID_5']
    u_ID_6 = params['u_6']**HID_dict['ID_6']
    
    C_x1 = (pair(params['g'], params['g'])**vec_x['vec_1'])*(pair(params['g_alpha'], params['h_1'])**r)
    C_x2 = (pair(params['g'], params['g'])**vec_x['vec_2'])*(pair(params['g_alpha'], params['h_2'])**r)
    C_x3 = (pair(params['g'], params['g'])**vec_x['vec_3'])*(pair(params['g_alpha'], params['h_3'])**r)
    C_x4 = (pair(params['g'], params['g'])**vec_x['vec_4'])*(pair(params['g_alpha'], params['h_4'])**r)
    C_x5 = (pair(params['g'], params['g'])**vec_x['vec_5'])*(pair(params['g_alpha'], params['h_5'])**r)
    
    C_r = params['g']**r
    
    C_u = (u_ID_1*u_ID_2*u_ID_3*u_ID_4*u_ID_5*u_ID_6*params['u_7'])**r
    
    CT = {'HID_dict': HID_dict, 'C_r': C_r, 'C_u': C_u, 'C_x1': C_x1, 'C_x2': C_x2, 'C_x3': C_x3, 'C_x4': C_x4, 'C_x5': C_x5}
    
    return CT

#### Delegate Key Example
ID_3 = group.random(ZR)

Dele_SK = Delegate(params, SK, HID_dict, ID_3)
HID_dict['ID_6'] = ID_3
