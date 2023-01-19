from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.core.math.integer import randomBits,integer,bitsize
from charm.toolbox.hash_module import Hash,int2Bytes,integer
import time

# the length of vectors n = 5
# the depth of hierarchical d = 5
# the length of HID l = 5

def setup(param_id='SS512'):
    group = PairingGroup(param_id)
    alpha = group.random(ZR)
    g = group.random(G1)
    
    g_alpha = g ** alpha
    
    # the length of vectors n = 5
    h_1, h_2, h_3, h_4, h_5 = group.random(G1, 5)
    
    # the depth of hierarchical d = 6, d+1, l = 5
    u_1, u_2, u_3, u_4, u_5, u_6, u_7  = group.random(G1, 7)

    
    params = { 'g': g, 'g_alpha': g_alpha, 'h_1': h_1, 'h_2': h_2, 'h_3': h_3, 'h_4': h_4, 'h_5': h_5,  
              'u_1': u_1, 'u_2': u_2, 'u_3': u_3, 'u_4': u_4, 'u_5': u_5, 'u_6': u_6, 'u_7': u_7}
    msk = alpha
    return (params, msk)


def genHID(l):
    HID = []
    HID_name = []
    for i in range(1,l+1):
        r = group.random(ZR)
        HID.append(r)
        HID_name.append("ID_%d"%(i))
    HID_dict = dict(zip(HID_name, HID))
    return HID_dict


def genvec(m):
    vec = [] 
    vec_name = []
    for i in range(1,m+1):
        r = group.random(ZR)
        vec.append(r)
        vec_name.append("vec_%d"%(i))
    vec_dict = dict(zip(vec_name, vec))
    return vec_dict


def KeyGen(params, msk, HID_dict, vec_y):
    
    t = group.random(ZR)
    
    h_1_v_1 = params['h_1']**vec_y['vec_1']
    h_2_v_2 = params['h_2']**vec_y['vec_2']
    h_3_v_3 = params['h_3']**vec_y['vec_3']
    h_4_v_4 = params['h_4']**vec_y['vec_4']
    h_5_v_5 = params['h_5']**vec_y['vec_5']
    
    u_ID_1 = params['u_1']**HID_dict['ID_1']
    u_ID_2 = params['u_2']**HID_dict['ID_2']
    u_ID_3 = params['u_3']**HID_dict['ID_3']
    u_ID_4 = params['u_4']**HID_dict['ID_4']
    u_ID_5 = params['u_5']**HID_dict['ID_5']
    
    K_h = ((h_1_v_1*h_2_v_2*h_3_v_3*h_4_v_4*h_5_v_5)**msk)*(u_ID_1*u_ID_2*u_ID_3*u_ID_4*u_ID_5*params['u_7'])**(-t)
    K_t = params['g'] ** t   
    K_6 = params['u_6'] ** t
    K_7 = params['u_7'] ** t
    
    SK = {'HID_dict':HID_dict, 'vec_y': vec_y, 'K_h': K_h, 'K_t': K_t, 'K_6': K_6, 'K_7': K_7}
    return SK


def Enc(params, HID_dict, vec_x):
    r = group.random(ZR)
    
    u_ID_1 = params['u_1']**HID_dict['ID_1']
    u_ID_2 = params['u_2']**HID_dict['ID_2']
    u_ID_3 = params['u_3']**HID_dict['ID_3']
    u_ID_4 = params['u_4']**HID_dict['ID_4']
    u_ID_5 = params['u_5']**HID_dict['ID_5']
    
    C_x1 = (pair(params['g'], params['g'])**vec_x['vec_1'])*(pair(params['g_alpha'], params['h_1'])**r)
    C_x2 = (pair(params['g'], params['g'])**vec_x['vec_2'])*(pair(params['g_alpha'], params['h_2'])**r)
    C_x3 = (pair(params['g'], params['g'])**vec_x['vec_3'])*(pair(params['g_alpha'], params['h_3'])**r)
    C_x4 = (pair(params['g'], params['g'])**vec_x['vec_4'])*(pair(params['g_alpha'], params['h_4'])**r)
    C_x5 = (pair(params['g'], params['g'])**vec_x['vec_5'])*(pair(params['g_alpha'], params['h_5'])**r)
    
    C_r = params['g']**r
    
    C_u = (u_ID_1*u_ID_2*u_ID_3*u_ID_4*u_ID_5*params['u_7'])**r
    
    CT = {'HID_dict': HID_dict, 'C_r': C_r, 'C_u': C_u, 'C_x1': C_x1, 'C_x2': C_x2, 'C_x3': C_x3, 'C_x4': C_x4, 'C_x5': C_x5}
    return CT


def Dec(params, CT, SK):
    #SK = [HID_dict, vec_y, K_h, K_t, K_3, K_4]
    #CT = [HID_dict, C_r, C_u, C_x1, C_x2]
    left = (CT['C_x1']**vec_y['vec_1'])*(CT['C_x2']**vec_y['vec_2'])*(CT['C_x3']**vec_y['vec_3'])*(CT['C_x4']**vec_y['vec_4'])*(CT['C_x5']**vec_y['vec_5'])
    mid = pair(CT['C_r'], SK['K_h'])**(-1)
    right = pair(CT['C_u'], SK['K_t'])**(-1)
    
    pair_inner = left*mid*right
    
    return pair_inner


def Delegate(params, SK, ID_l_1):
    t_prime = group.random(ZR)
    # SK = {'HID_dict':HID_dict, 'vec_y': vec_y, 'K_h': K_h, 'K_t': K_t, 'K_6': K_6, 'K_7': K_7}
    #K_h:2, K_t:3, K_3:4, K_4:5
    left = SK['K_h']*(SK['K_6']**(-ID_l_1))
    u_ID_1 = params['u_1']**SK['HID_dict']['ID_1']
    u_ID_2 = params['u_2']**SK['HID_dict']['ID_2']
    u_ID_3 = params['u_3']**SK['HID_dict']['ID_3']
    u_ID_4 = params['u_4']**SK['HID_dict']['ID_4']
    u_ID_5 = params['u_5']**SK['HID_dict']['ID_5']
    
    u_ID_6 = params['u_6']**ID_l_1
    
    K_h_prime = left *(u_ID_1*u_ID_2*u_ID_3*u_ID_4*u_ID_5*u_ID_6*params['u_7'])**(-t_prime)
    
    K_t_prime = SK['K_t']*(params['g']**(t_prime))
    K_7_prime = SK['K_7']*(params['u_7']**(t_prime))
    K_d_prime = SK['K_6']*(params['u_6']**(t_prime))
    
    HID_dict['ID_6'] = ID_l_1
    Dele_SK = {'HID_dict': HID_dict, 'vec_y': vec_y, 'K_h': K_h_prime, 'K_t': K_t_prime, 
               'K_7': K_7_prime, 'K_d': K_d_prime}
    
    return Dele_SK


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
    params, msk = setup(param_id)

    ## Generate HID
    HID_dict = genHID(5)

    ## Generate vector
    vec_x = genvec(5)
    vec_y = genvec(5)

    ## Key Generate
    SK = KeyGen(params, msk, HID_dict, vec_y)

    ## Encryption 
    CT = Enc(params, HID_dict, vec_x)

    ## Decryption
    plaintext = Dec(params, CT, SK)
    
    ## Check inner product
    inner_product = vec_x['vec_1']*vec_y['vec_1']+vec_x['vec_2']*vec_y['vec_2']+vec_x['vec_3']*vec_y['vec_3']+vec_x['vec_4']*vec_y['vec_4']+vec_x['vec_5']*vec_y['vec_5']

    #left = (CT['C_x1']**vec_y['vec_1'])*(CT['C_x2']**vec_y['vec_2'])*(CT['C_x3']**vec_y['vec_3'])*(CT['C_x4']**vec_y['vec_4'])*(CT['C_x5']**vec_y['vec_5'])

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

Dele_SK = Delegate(params, SK, ID_3)

CT = Del_Enc(params, Dele_SK['HID_dict'], vec_x)
plaintext_ = Dec(params, CT, Dele_SK)





