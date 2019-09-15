import numpy as np
import sys

class NeuralNetMLP(object):
   
    """入力
       n_hidden:隠れユニットの数
       l2:正規化パラメータλ(L2が0のときは正規化なし)
        epochs:学習回数
       eta:学習率
       shuffle:循環を避けるための変数(boolでtrueのときトレーニングデータをシャッフル)
       minibatch_size:ミニバッチ当たりのトレーニングサンプルの個数
       seed:重みとシャッフルを初期化するための乱数シード
        """ 

    def __init__(self, n_hidden=30,
                 l2=0., epochs=100, eta=0.001,
                 shuffle=True, minibatch_size=1, seed=None):# teachers, N, seed=None
        
        if not seed is None:
            np.random.seed(seed)#乱数の固定
        self.random = np.random.RandomState(seed)
        self.n_hidden = n_hidden
        self.l2 = l2
        self.epochs = epochs
        self.eta = eta
        self.shuffle = shuffle
        self.minibatch_size = minibatch_size
        
    
    def _onehot(self, y, n_classes):
        """ラベルをone-hot表現にエンコード
        入力
            y:目的変数の値（shape=(n_classes, n_labels)）
        出力     
        onehot 
        """   
        onehot = np.zeros((n_classes, y.shape[0]))
        for idx, val in enumerate(y.astype(int)):#int型に変換
            onehot[val, idx] = 1.
        return onehot.T

    def _sigmoid(self, z):
        return 1. / (1. + np.exp(-np.clip(z, -250, 250)))
    
    
    ####################################################################
    ############################ SOM ###################################
    ###################################################################
     
    def _best_matching_unit(self,nodes, X):
        n_features = X.shape[1]
        norms = np.zeros((self.n_hidden, self.n_hidden))# n_hidden×n_hiddenの２次元配列を生成
        for x in range (self.n_hidden):
            for y in range(self.n_hidden):
                for z in range(n_features):
                    norms[x, y] += (nodes[x,y,z] - X[z])**2

        bmu_1 = np.argmin(norms)#１次元配列で考えたとき何番目かを返す
        bmu = np.unravel_index(bmu_1,(self.n_hidden, self.n_hidden))#argminと組み合わせることで,もとの行列の何行何列目に最小値があるのかわかる

        return bmu 

    def _neighbourhood(self, t):
        halflife = float(n_teacher/4)#時定数
        initial = float(self.n_hidden /4)
        return initial*np.exp(-t/halflife)

    def _learning_ratio(self, t):
        halflife = float(n_teacher/4)#時定数
        initial = 0.1#Lの初期値
        return initial*np.exp(-t/halflife)

    def _learning_radius(self, t, d):
        s = self._neighbourhood(t)
        return np.exp(-d**2/(2*s**2)) 
    

    def _forward(self, nodes, X):
        """フォワードプロパゲーションのステップを計算"""

        # step 1: 隠れ層の入力     
        z_h = np.dot(X, self.w_h) + self.b_h

        # step 2: 隠れ層の活性化関数
        #a_h = self._sigmoid(z_h)
        
        n_teacher = X.shape[0]#学習する行
        bmu = self._best_matching_unit(nodes, X)
        for x in range(self.n_hidden):
            for y in range(self.n_hidden):
                c = np.array([x,y])
                d = np.linalg.norm(c - bmu)
                L = self._learning_ratio(i)
                S = self._learning_radius(i, d)
                for z in range(n_features):
                    nodes[x, y, z] += L * S * (X[z] - nodes[x, y, z])
        
        a_h = nodes
        
        # step 3: 出力層の総入力
        z_out = np.dot(a_h, self.w_out) + self.b_out

        # step 4: 出力層の活性化関数
        a_out = self._sigmoid(z_out)

        return z_h, a_h, z_out, a_out 

    
    def _compute_cost(self, y_enc, output):
        """コスト関数
        
        入力
        ----------
        y_enc : one-hot表現にエンコードされたクラスラベル
        output : 出力層の活性化関数(フォワードプロパゲーション)

        出力
        ---------
        cost :正規化されたコスト
        """
        L2_term = (self.l2 *
                   (np.sum(self.w_h ** 2.) +
                    np.sum(self.w_out ** 2.)))
        
        ####ロジスティック関数のコスト関数#####
        ######対数尤度関数#自然対数を最小化するほうが簡単#######
        term1 = -y_enc * (np.log(output))
        term2 = (1. - y_enc) * np.log(1. - output)
        cost = np.sum(term1 - term2) + L2_term
              
        return cost
    
    ########クラスラベル予測###########
    def predict(self, X):
        """
      　入力
        -----------
        X :元の特徴量が設定された入力層
        
       出力
        ----------
        y_pred :予測されたクラスラベル
        """
        z_h, a_h, z_out, a_out = self._forward(nodes, X)
        y_pred = np.argmax(z_out, axis=1)#出力層で一番大きい値をとるものを予測に適応
        return y_pred
    
    #########重みの学習##########
    def fit(self, X_train, y_train):
        """
        入力
        -----------
        X_train : 元の特徴量が設定された入力層
        y_train :目的値のクラスラベル
        X_valid :トレーニング時の検証に使用するサンプル特徴量
        y_valid : トレーニング時の検証に使用するサンプルラベル

        出力
        ----------
        self
        """
        n_output = np.unique(y_train).shape[0]  # クラスラベルの個数が出力の数
        n_features = X_train.shape[1]#次元

        ##########################
        ###### 重みの初期化 ######
        ##########################

        # 入力層→隠れ層の重み
        self.b_h = np.zeros((self.n_hidden, self.n_hidden))
        self.w_h = self.random.normal(loc=0.0, scale=0.1,size=(n_features, self.n_hidden))
        
        
        # 隠れ層の参照ベクトル
        nodes = np.random.rand(self.n_hidden, self.n_hidden, n_features)#0.0~1.0の値で一様分布

        for x in range (self.n_hidden):
            for y in range(self.n_hidden):
                for z in range(n_features):
                    "今までと結果変わる"
                    M = X_train.max() 
                    m = X_train.min()
                    #参照ベクトルを -0.5~0.5(max-min) の一様乱数とする
                    nodes[x, y, z] = 0.5 *(M - m) * nodes[x, y, z] + m
                    
        #BMUとクラスを記録するためのcsvファイルを開く
        bmu_list = np.array([])
        classnum_list =  np.array([])
        
        # 隠れ層→出力層の重み
        self.b_out = np.zeros(n_output)
        self.w_out = self.random.normal(loc=0.0, scale=0.1,size=(self.n_hidden, self.n_hidden, n_output))
        
        y_train_enc = self._onehot(y_train, n_output)#y_train:目的変数の値, n_output:クラスラベルの個数
        
       
        #ax = plt.subplot()
        
        # エポック数だけトレーニングを繰り返す
        for i in range(self.epochs):

            #インデックス
            indices = np.arange(X_train.shape[0])

            if self.shuffle:
                self.random.shuffle(indices)
            
            #ミニバッチの反復処理(イテレーション)
            for start_idx in range(0, indices.shape[0] - self.minibatch_size +1, 
                                   self.minibatch_size):
                #ミニバッチ学習の範囲の移動
                batch_idx = indices[start_idx:start_idx + self.minibatch_size]
                
                ##################################
                ### フォワードプロパゲーション###
                #################################

                z_h, a_h, z_out, a_out = self._forward(nodes, X_train[batch_idx])
                
                bmu = best_matching_unit(nodes, X_train)
                y = y_train
                
                bmu_list = np.array(bmu)
                classnum_list = np.array(y)
                
                #df2 = pd.read_csv('bmu.csv')
                #if y[i] != df2['classnum'].any:
                    #if y[i]==[0]:#後ろ
                        #col='red'
                        #mark = 'o'

                    #elif y[i]==[1]:#前
                        #col='blue'
                        #mark = '^'

                #scale = 1 * df2['bmu'].value_counts()
                #ax.scatter(bmu[0],bmu[1],color = col, marker=mark, s=scale, alpha = 1.0)

                ##############################
                ### バックプロパゲーション###
                #############################
                "＋参照ベクトル修正"
                
                ####誤差行列(コスト関数の微分)####
                # [n_samples, n_classlabels]
                sigma_out = a_out - y_train_enc[batch_idx]
                
                "rbf関数"
                ####シグモイド関数の微分#####
                # [n_classlabels, n_hidden]
                sigmoid_derivative_h = a_h * (1. - a_h)
                
                ####誤差行列(コスト関数の入力z微分)#####
                # [n_samples, n_classlabels] dot [n_classlabels, n_hidden]
                # -> [n_samples, n_hidden]
                sigma_h = (np.dot(sigma_out, self.w_out.T) * sigmoid_derivative_h)
                
                #####偏微分係数(コスト関数の重みw微分)##########
                # [n_features, n_samples] dot [n_samples, n_hidden]
                # -> [n_features, n_hidden]
                grad_w_h = np.dot(X_train[batch_idx].T, sigma_h)
                grad_b_h = np.sum(sigma_h, axis=0)

                #####偏微分係数(コスト関数の重みw微分)##########
                # [n_hidden, n_samples] dot [n_samples, n_classlabels]
                # -> [n_hidden, n_classlabels]
                grad_w_out = np.dot(a_h.T, sigma_out)
                grad_b_out = np.sum(sigma_out, axis=0)

                # 正則化
                delta_w_h = (grad_w_h + self.l2*self.w_h)
                delta_b_h = grad_b_h # バイアスは正則化しない
                
                #####接続重み修正########勾配に対して反対方向
                self.w_h -= self.eta * delta_w_h
                #######バイアス修正######
                self.b_h -= self.eta * delta_b_h

                # 正則化
                delta_w_out = (grad_w_out + self.l2*self.w_out)
                delta_b_out = grad_b_out  #バイアスは正則化しない
                
                #####接続重み修正########
                self.w_out -= self.eta * delta_w_out
                #######バイアス修正######
                self.b_out -= self.eta * delta_b_out

        return self

nn = NeuralNetMLP(n_hidden = 15, #隠れユニットの行列
                 l2 = 0.01,#正則化のλパラメータ
                 epochs = 50, #n_epochs, #トレーニング回数
                 eta = 0.0005, #学習率
                 minibatch_size = 1, 
                 shuffle = True, #各エポックでデータをシャッフルするかどうか
                 seed = 1)
dimension = 2
