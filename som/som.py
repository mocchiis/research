import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from datetime import datetime
import os


class SOM():
    def __init__(self, df, N):
        self.df = df
        self.N = N

        self.n_teacher = len(df)  # 教師データの数(学習回数)#行数
        np.random.seed(1000)  # シード (種) を指定することで、発生する乱数を固定
        self.dimension = 4 # ベクトルの次元
        i = 0
        # 初期ノード
        # N x N ×dimension の配列の乱数
        nodes = np.random.rand(N, N, self.dimension) # 0.0~1.0の値で一様分布

        for x in range (N):
            for y in range(N):
                for z in range(self.dimension):
                    M = df.iloc[:,z].max()
                    m = df.iloc[:,z].min()
                    # 参照ベクトルを -0.5~0.5(max-min) の一様乱数とする
                    nodes[x, y, z] = 0.5*(M - m) * nodes[x, y, z] + m
        
        
        # BMUとクラスを記録するためのcsvファイルを開く
        with open(os.path.join(new_dir_path, 'bmu.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['index','bmu','classnum'])
            
        ax = plt.subplot()
        ax.set_xticks([0, N/2, N])
        ax.set_yticks([0, N/2, N])
        for df3 in range(2):
            df3 = df
            
            for i in range(int(self.n_teacher/2)):
                # 教師信号
                teachers = np.array(df.loc[i,'front':'left'].values) 
                train(nodes, teachers)
                bmu = best_matching_unit(nodes, teachers)
                y = np.array(df.loc[:, ['action']].values)
                
                # csvファイルにBMUとそのクラスを追記
                with open(os.path.join(new_dir_path, 'bmu.csv'), 'a') as f: 
                    writer = csv.writer(f)
                    writer.writerow([i,bmu,y[i]])
                
                df2 = pd.read_csv(os.path.join(new_dir_path, 'bmu.csv'))
                if y[i] != df2['classnum'].any:
                    if y[i] == [1.]:  # 前
                        col = 'red'
                        mark = 'o'
                        l = 'front'

                    elif y[i] == [0.]:  # 後ろ
                        col = 'blue'
                        mark = '^'
                        l = 'back'
                        
                    elif y[i] == [2.]:  # 右
                        col = 'orange'
                        mark = '*'
                        l = 'right'
                        
                    elif y[i] == [3.]:  # 左
                        col = 'green'
                        mark = 's'
                        l = 'left'
        
                scale = 3 * df2['bmu'].value_counts()
                plot_som = ax.scatter(bmu[0], bmu[1], color = col, marker = mark, s = scale, alpha = 1.0)
                
        plt.xlim(0-1, N+1)
        plt.ylim(0-1, N+1)
        #plt.legend()
        plt.savefig(os.path.join(new_dir_path, f'Rand'+str(length)+'Seq'+str(count)+
                                '('+datetime.now().strftime('%Y.%m.%d.%H.%M')+')'+'.png'), dpi = 400, bbox_inches = 'tight')
        #plt.show()
        
        
    # 学習   
    def train(self, nodes, teachers):
        
        bmu = best_matching_unit(nodes, teachers)

        for x in range(N):
            for y in range(N):
                c = np.array([x,y])
                d = np.linalg.norm(c - bmu)  # ユニットの位置とBMUとの距離
                L = learning_ratio(i)  # 学習時間を決定するパラメータ#iはe^(-t/λ)
                S = learning_radius(i, d)  # ユニットがどの程度BMUの近傍にいるのか
                for z in range(self.dimension):
                    nodes[x, y, z] += L * S * (teachers[z] - nodes[x, y, z])

                    
    def best_matching_unit(self, nodes, teacher):
        norms = np.zeros((N,N))  # N×Nの２次元配列を生成
        for x in range (N):
            for y in range(N):
                for z in range(self.dimension):
                    norms[x, y] += (nodes[x,y,z] - teacher[z])**2
        
        bmu_1 = np.argmin(norms)  # １次元配列で考えたとき何番目かを返す
        bmu = np.unravel_index(bmu_1,(N,N))  # argminと組み合わせることで,もとの行列の何行何列目に最小値があるのかわかる

        return bmu 

    def neighbourhood(self, t):
        halflife = float(self.n_teacher/4)  # 時定数
        initial = float(N/4)
        return initial*np.exp(-t/halflife)

    def learning_ratio(self, t):
        halflife = float(self.n_teacher/4)  # 時定数
        initial = 0.1  # Lの初期値
        return initial*np.exp(-t/halflife)

    def learning_radius(self, t, d):
        s = neighbourhood(t)
        return np.exp(-d**2/(2*s**2))
    
    return plt.show()