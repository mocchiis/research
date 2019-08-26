import numpy as np
import serial

for l in range(10):
   
    ################### センサー値取得 ####################
    # COMポート(Arduino接続)
    ser_sensor = serial.Serial('COM4',9600)#センサー
    ser_sensor.write(b"r")#センサ読み込む

    input_num = 2 
    sensor_list = np.zeros((1,input_num))
    for i in range(input_num):

        #シリアル通信で受け取った情報（文字列）を改行コードがくるまで代入
        data = ser_sensor.readline().rstrip() # readline:行終端まで読み込む  rstrip:行終端コード削除　→　# \nまで読み込む(\nは削除
        data = data.decode() #対話型だとこれが必要。その情報をデコードする。

        sensor_list[0,i] = data

    sensor_list = np.array(sensor_list)
    ser_sensor.close()

    ################### 予測 #######################

    print(sensor_list)
    pre = nn.predict(sensor_list)#.swapaxes(1,0))
    print(pre)

    #################### 移動 #######################
    ser_motor = serial.Serial("COM3",9600)

    #予測した値をロボットに送る
    if pre == 1:
        ser_motor.write(b"1")
    elif pre == 0:
        ser_motor.write(b"0")#バイト型で送信

    data = ser_motor.readline().rstrip()
    data = data.decode()
    #print(data)
    
    ser_motor.close()
    
    ###############################################
    ################## 逐次学習 ###################
    ###############################################


    ############## センサー値取得 #################
    next_ser_sensor = serial.Serial('COM4',9600)
    next_ser_sensor.write(b"r")#センサ読み込む

    next_sensor_list = np.zeros((1,input_num))

    for i in range(input_num):

        data = next_ser_sensor.readline().rstrip()
        data = data.decode()
        next_sensor_list[0,i] = data

    next_sensor_list = np.array(next_sensor_list)
    #print(next_sensor_list)
    next_ser_sensor.close()

    #2つのセンサ値のうち小さいほう
    minimum_kind = np.argmin(sensor_list)
    print("minimum_num:"+str(minimum_kind))

    #教師の初期化
    t_teacher = np.array(np.zeros(1))

    if pre == 1:
        t_teacher[0] = 1
    elif pre == 0:
        t_teacher[0] = -1

    #前の行との差が正->その方向が正解
    if next_sensor_list[0,minimum_kind] - sensor_list[0,minimum_kind] > 0:
        t_teacher[0] = t_teacher[0]
    #前の行との差が負->逆方向が正解
    elif next_sensor_list[0,minimum_kind] - sensor_list[0,minimum_kind] <= 0:
        t_teacher[0] = -t_teacher[0]

    if t_teacher[0] == 1:
        t_teacher[0] = 1
    elif t_teacher[0] ==-1:
        t_teacher[0] = 0

    t_teacher = np.array(t_teacher)
    #print(t_teacher)
    
    sensor_list_append = np.zeros((l,input_num))
    sensor_list_append = np.append(sensor_list_append, sensor_list)
    
    X_train = np.append(X_sensor, sensor_list_append,axis= 0)
    y_train = np.append(teacher, t_teacher, axis= 0)
    #print(y_train)
    fit = nn.fit(X_train  ,y_train )
    #fit = nn.fit(X_train = sensor_list ,y_train = t_teacher)#前か後ろか
    #print(predict)
