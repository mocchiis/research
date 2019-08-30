import numpy as np
import matplotlib.pyplot as plt

N = 20#linear size of 2D map
n_teacher = 1000 #教師データの数回数
np.random.seed(100)#test seed for random number

def main():
    #初期ノードベクトル
    nodes = np.random.rand(N,N,3)#ノードの配列。それぞれのノードが3次元の重みベクトルを持つ
    #初期化出力
    #
    plt.imshow(nodes, interpolation='none')
    plt.show()
    
    #教師信号
    teachers = np.random.rand(n_teacher, 3)
    for i in range(n_teacher):
        train(nodes, teachers, i)
        
        #中間の出力
        if i%1000 == 0 or i<100:
            plt.imshow(nodes, interpolation='none')
           # plt.show()
           
    #出力
    #plt.imshow(nodes, interpolation='none')
    #plt.show()
    
def train(nodes, teachers, i):
    bmu = best_matching_unit(nodes, teachers[i])
    #print bmu
    for x in range(N):
        for y in range(N):
            c=np.array([x,y])
            d=np.linalg.norm(c-bmu)
            L=learning_ratio(i)
            S=learning_radius(i, d)
            for z in range(3):
                nodes[x, y, z]+=L*S*(teachers[i, z]-nodes[x,y,z])
                
def best_matching_unit(nodes, teacher):
    norms = np.zeros((N,N))
    for i in range (N):
        for j in range(N):
            for k in range(3):
                norms[i, j] += (nodes[i,j,k]-teacher[k])**2
    
    bmu=np.argmin(norms)
    return np.unravel_index(bmu,(N,N))

def neighbourhood(t):
    halflife=float(n_teacher/4)
    initial=float(N/2)
    return initial*np.exp(-t/halflife)

def learning_ratio(t):
    halflife=float(n_teacher/4)
    initial=0.1
    return initial*np.exp(-t/halflife)

def learning_radius(t, d):
    s=neighbourhood(t)
    return np.exp(-d**2/(2*s**2))
