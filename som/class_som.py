import numpy as np

from matplotlib import pyplot as plt#グラフを書くときは matplotlibライブラリの pyplot が必要

#Jupyterでインライン表示するための宣言

%matplotlib inline 





class SOM():#SOMという名前のclassを創る

   

    #classの内部はすべてdefで定義する

    #第一引数に「self」が指定する＝コンストラクタ

    def __init__(self, teachers, N, seed=None):

        #インスタンス変数teachersを初期化したことになる

        #selfのなかにteachersを持たせnumpyの配列arrayに定義

        self.teachers = np.array(teachers)

        self.n_teacher = self.teachers.shape[0] #.shape:行列の大きさ。.shape[0]:行列の行数。.shape[1]:行列の列数

        self.N = N

        if not seed is None:

            np.random.seed(seed)#乱数の固定

            

        x, y = np.meshgrid(range(self.N), range(self.N)) # 各座標の要素列から格子座標を作成するために使う

        #ユニットの位置 #400*2の行列

        self.c = np.hstack((x.flatten()[:, np.newaxis],

                            y.flatten()[:, np.newaxis])) #hstack :横（hstack）に連結。x.flattenとy.flattenをくっつける 

        #ユニットの更新

        self.nodes = np.random.rand(self.N*self.N,

                                    self.teachers.shape[1])#random.rand:乱数の自動生成#self.teachersの列数

    

    def train(self):

        for i, teacher in enumerate(self.teachers): #teacherは入力ベクトル

            bmu = self._best_matching_unit(teacher) #BMU:データに対し最も似ているベクトルを持つユニットあとで定義

            d = np.linalg.norm(self.c - bmu, axis=1) #ユニットの位置とBMUとの距離

            L = self._learning_ratio(i) #学習時間を決定するパラメータ#iはe^(-t/λ)

            S = self._learning_radius(i, d) #更新するユニットがどの程度BMUの近傍にいるのかを表現

            

            #ユニットの更新

            self.nodes += L * S[:, np.newaxis] * (teacher - self.nodes)

        return self.nodes

    

    #BMUの定義

    def _best_matching_unit(self, teacher):

        #compute all norms (square)

        norms = np.linalg.norm(self.nodes - teacher, axis=1)

        bmu = np.argmin(norms) #argment with minimum element 

        return np.unravel_index(bmu,(self.N, self.N))#ユニットの場所2次元

    

    #BMUの近傍を定義(_learning_radius(S)に使う)

    def _neighbourhood(self, t):#neighbourhood radious

        halflife = float(self.n_teacher/4) #for testing #時定数

        initial  = float(self.N/4) 

        return initial*np.exp(-t/halflife)

    

    #L

    def _learning_ratio(self, t):#ratio:比率

        halflife = float(self.n_teacher/4) #for testing #時定数

        initial  = 0.1 #Lの初期値

        return initial*np.exp(-t/halflife)

    

    #S

    def _learning_radius(self, t, d):#radius:半径

        # d is distance from BMU

        s = self._neighbourhood(t)

        return np.exp(-d**2/(2*s**2))       

        

N = 20 #ユニットの行列

teachers = np.random.rand(1000, 3)#(学習回数，次元)

som = SOM(teachers, N, seed=30)#乱数の初期条件



# Initial map #S初期のSOM

plt.imshow(som.nodes.reshape((N, N, 3)),

           interpolation='none')#interpolation:改変、挿入

plt.show()



# Train #SOM()内で定義したtrain関数を呼び出す

som.train()



# Trained MAP

plt.imshow(som.nodes.reshape((N, N, 3)),

           interpolation='none')

plt.show()
