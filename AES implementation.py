
import math
rcon = ['0x0', '0x1', '0x2', '0x4', '0x8', '0x10', '0x20', '0x40', '0x80', '0x1b','0x36']
SBox = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
        ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
        ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
        ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
        ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
        ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
        ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
        ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
        ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
        ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
        ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
        ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
        ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
        ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
        ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
        ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]
def mix_cols(state):
    temp,result,xor=[],[],[]
    static = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
    transposedState,answer = [[i for i in range(4)] for j in range(4)], [[i for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            transposedState[j][i] = state[i][j] #transpose the input to simplify the next step
    for i in range(4):
        for j in range(4):
            zipped = list(zip(static[j], transposedState[i])) #zip row with column and make it a list
            for pair in zipped:
                coef, val = pair[0],pair[1] #coef comes from static matrix and val is from the state matrix
                bits = bin(val)
                bits = bits[2:] #get rid of the 0b python adds onto binary numbers
                if len(bits) < 8:
                    l = '0'*(8-len(bits)) #bit length is important
                    l += bits
                    bits = l #reset the names to make code more readable
                if coef==1:
                    temp.append(val)
                elif coef==2:
                    u = (val<<1) & 255 #mask bytes with 255 to eliminate extra value
                    if bits[0] == '1': #bits are stored as a string natively
                        u = u^27 #27 = 1b
                    temp.append(u)
                elif coef==3:
                    u = (val<<1) & 255
                    if bits[0] == '1':
                        u=u^27
                        u=u^val
                    else:
                        u=u^val
                    temp.append(u)
    for i in range(0,64,4):
        for j in range(4):
            xor.append(temp[i+j])
        result.append(hex(xor[0]^xor[1]^xor[2]^xor[3]))
        xor[:]=[] #clear xor to prevent calculating the same thing everytime
    for i in range(0,16):
        u,v = math.floor(i/4),i%4 #math.floor(i) gives row, i%4 gives col
        answer[u][v] = result[i]
    return answer

def shift(state):
    result = [[i for i in range(4)] for j in range(4)]
    temp=[]
    for i in range(4):
        for j in range(i,4):
            temp.append(state[i][j])
        for k in range(0,i):
            temp.append(state[i][k])
        for l in range(4):
            result[i][l] = temp[l]
        temp[:]=[]
    return result

def byte_sub(state):
    temp = []
    result=[[i for i in range(4)]for j in range(4)]
    for i in state:
        for j in i:
            u,v = j[2].lower(),j[3].lower()
            k,l =int(u,16), int(v,16)
            y = '0x'
            y+= SBox[k][l]
            temp.append(y)
    for i in range(len(temp)):
        result[math.floor(i/4)][i%4] = temp[i]
    return result

def generate_key_matrix_from_key(keyAsInteger):
    hexKey = hex(keyAsInteger)[2:]
    keyMatrix = [[i for i in range(4)]for j in range(4)]
    colNumber = int(math.sqrt(int(len(hexKey)/2)))
    for i in range(0,len(hexKey),2):
        u='0x'
        u+=hexKey[i]
        u+=hexKey[i+1]
        keyMatrix[math.floor(int(i/2)/colNumber)][int(i/2)%colNumber] = u
    return keyMatrix
def t_w_i(L):
    temp=[]
    for i in L:
        u,v = i[2],i[3]
        k,l = int(u,16), int(v,16)
        y = '0x'
        y+= SBox[k][l]
        temp.append(y)
    return temp

def not_mult_4(L1,L2):
    temp = []
    for i in range(4):
        temp.append(hex(int(L1[i],16)^int(L2[i],16)))
    return temp

def is_mult_4(L1,L2,i):
    result=[]
    TW = []
    SB = t_w_i(L2)
    TW.append(int(SB[1],16)^int(rcon[i],16))
    TW.append(int(SB[2],16))
    TW.append(int(SB[3],16))
    TW.append(int(SB[0],16))
    for i in range(4):
        u = (int(L1[i],16))^(TW[i])
        result.append(hex(u))
    return result

def key_expansion(state):
    temp=[]
    temp = state
    for i in range(4,12):
        if i%4 != 0:
            L1 = state[i-4]
            L2 = state[i-1]
            A = not_mult_4(L1,L2)
            temp.append(A)
        elif i%4 == 0:
            A = is_mult_4(state[i-4], state[i-1],i)
            temp.append(A)
    return temp

if __name__ == "__main__" :
    A = generate_key_matrix_from_key(34561551968104528306916370693414191105)
    print("key matrix =   ",A)
    B = key_expansion(A)
    print("expanded =     ",B)
    V = [[48, 202, 150, 36],[50, 146, 9, 35],[63, 202, 67, 0],[125, 90, 248, 150]]
    C = mix_cols(V)
    print("mixed columns =", C)
    W = [['0x08','0x10', '0x35', '0xA6'],['0x32', '0xA1', '0x74', '0x40'],['0x64 ','0x00', '0x25', '0x10'],['0x46','0xE1', '0x35', '0x13']]
    D = byte_sub(W)
    print("subbed bytes = ",D)
    E = shift(D)
    print("shifted =      ",E)
