import numpy as np
import math
def random_data(sensor_df):

    X_sensor = np.array(sensor_df.loc[:,'front':'left'])
    length = len(sensor_df)

    action = np.array(np.zeros(length))
    action = np.array(sensor_df.loc[:,'action'])

    # 各行の最小センサ値の列名
    minimum_kind = sensor_df.loc[:,'front':'left'].idxmin(axis = 1)
    # 教師の初期化
    teacher = np.zeros((length,4))

    for i in range(1, length):

        min_fir_before = sorted(X_sensor[i-1])[0]
        min_sec_before = sorted(X_sensor[i-1])[1]
        senor_min_before = math.sqrt(min_fir_before**2 + min_sec_before**2)

        min_fir_now = sorted(X_sensor[i])[0]
        min_sec_now = sorted(X_sensor[i])[1]

        senor_min_now = math.sqrt(min_fir_now**2 + min_sec_now**2)

        if action[i] == -1:
            action[i] = 0
        elif action[i] == 1:
            action[i] = 1
        elif action[i] == 3:
            action[i] = 2
        elif action[i] == -3:
            action[i] = 3

        # 前に動いたとき
        if action[i] == 1:
            # 正解
            if senor_min_now - senor_min_before > 0: # and X_sensor[i][minimum_num] >=8:
                teacher[i] = (1,0,0,0)
            # 不正解
            else: 
                teacher[i] = (0,0.5,0.5,0.5)

        # 後に動いたとき
        if action[i] == 0:
            # 正解
            if senor_min_now - senor_min_before > 0: # and X_sensor[i][minimum_num] >=8:
                teacher[i] = (0,1,0,0)
            # 不正解
            else: 
                teacher[i] = (0.5,0,0.5,0.5)

        # 右に進んだとき
        elif action[i] == 2:
            if senor_min_now - senor_min_before > 0: #and X_sensor[i][minimum_num - 2]>=8:
                teacher[i] = (0,0,1,0)
            # 不正解
            else:
                teacher[i] = (0.5,0.5,0,0.5)

        # 左に進んだとき
        elif action[i] == 3:
            # 正解
            if senor_min_now - senor_min_before > 0: #and X_sensor[i][minimum_num + 2] >= 8:
                teacher[i] = (0,0,0,1)
            # 不正解
            else: 
                teacher[i] = (0.5,0.5,0.5,0)

    X_sensor = np.delete(X_sensor, 0,0)
    teacher = np.delete(teacher, 0,0)
    teacher = teacher.astype(int)
    action = np.delete(action, 0,0)

    return X_sensor, teacher, action