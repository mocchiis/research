import numpy as np
import sys

class NeuralNetMLP(object):

    def __init__(self, n_hidden=30,
                 l2=0., epochs=100, eta=0.001,
                 shuffle=True, minibatch_size=1, seed=None):

        self.random = np.random.RandomState(seed)
        self.n_hidden = n_hidden
        self.l2 = l2
        self.epochs = epochs
        self.eta = eta
        self.shuffle = shuffle
        self.minibatch_size = minibatch_size
        
        n_features = 4
        n_output = 4  # 出力の数

        ########################
        ##### 重みの初期化 #####
        ########################

        # 入力層→隠れ層の重み
        self.b_h = np.zeros(self.n_hidden)
        self.w_h = self.random.normal(loc=0.0, scale=0.1,size=(n_features, self.n_hidden))

        # 隠れ層→出力層の重み
        self.b_out = np.zeros(n_output)
        self.w_out = self.random.normal(loc=0.0, scale=0.1,size=(self.n_hidden, n_output))
        
    def _onehot(self, y, n_classes):
       
        onehot = np.zeros((n_classes, y.shape[0]))
        for idx, val in enumerate(y.astype(int)):  #int型に変換
            onehot[val, idx] = 1.
        return onehot.T

    def _sigmoid(self, z):
        return 1. / (1. + np.exp(-np.clip(z, -250, 250)))

    def _forward(self, X):
        """フォワードプロパゲーションのステップを計算"""

        # step 1: 隠れ層の入力     
        z_h = np.dot(X, self.w_h) + self.b_h

        # step 2: 隠れ層の活性化関数
        a_h = self._sigmoid(z_h)

        # step 3: 出力層の総入力
        z_out = np.dot(a_h, self.w_out) + self.b_out

        # step 4: 出力層の活性化関数
        a_out = self._sigmoid(z_out)

        return z_h, a_h, z_out, a_out

    def _compute_cost(self, y_enc, output):
        """コスト関数"""
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
        
        z_h, a_h, z_out, a_out = self._forward(X)
        y_pred = np.argmax(z_out, axis=1)#出力層で一番大きい値をとるものを予測に適応
        return y_pred
    
    #########重みの学習##########
    def fit(self, X_train, y_train_enc):
        """
        入力
        -----------
        X_train : 元の特徴量が設定された入力層
        y_train :目的値のクラスラベル

        出力
        ----------
        self
        """
        
        # エポック数だけトレーニングを繰り返す
        for i in range(self.epochs):

            # インデックス
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
                z_h, a_h, z_out, a_out = self._forward(X_train[batch_idx])

                ##############################
                ### バックプロパゲーション ###
                #############################
                
                ####誤差行列(コスト関数の微分)####
                # [n_samples, n_classlabels]
                sigma_out = a_out - y_train_enc[batch_idx]
                
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