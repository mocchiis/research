#include <SoftwareSerial.h>
SoftwareSerial mySerial(12, 13); // RX, TX
int received;
int received_pc;

//front
int Echo = 2;  
int Trig = 3;
//bihind
int Echo2 = 8;
int Trig2 = 9;
//right
int Echo3= 4;
int Trig3 = 5;
//left
int Echo4 = 7;
int Trig4 = 6;

double CURRENT_SENSOR[4];
void send(){
  for (int i = 0; i < 4; i++){
    Serial.println(CURRENT_SENSOR[i]);
    //Serial.print(" ");
    }
    //Serial.println();//シリアル通信する
}


//センサー1(2，3がセンサ多いほう)
double Distance_test() {
  digitalWrite(Trig, LOW);  //超音波を出力 
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH); //超音波を出力 
  delayMicroseconds(20);
  digitalWrite(Trig, LOW);   
  double Fdistance = pulseIn(Echo, HIGH);//センサからの入力  
  Fdistance= Fdistance / 58; //cm   //音が返ってくるときの変換？       
  return Fdistance;
}  

//センサー2(8，9)
double Distance_test2() {
  digitalWrite(Trig2, LOW);   
  delayMicroseconds(2);
  digitalWrite(Trig2, HIGH);  
  delayMicroseconds(20);
  digitalWrite(Trig2, LOW);   
  double Fdistance = pulseIn(Echo2, HIGH); // 出力した超音波が返って来る時間を計測 
  Fdistance= Fdistance / 58;  //cm     
  return Fdistance;
}  

//センサー3(4，5)right
double Distance_test3() {
  digitalWrite(Trig3, LOW);   
  delayMicroseconds(2);
  digitalWrite(Trig3, HIGH);  
  delayMicroseconds(20);
  digitalWrite(Trig3, LOW);   
  double Fdistance = pulseIn(Echo3, HIGH);  
  Fdistance= Fdistance / 58;       
  return Fdistance;
} 

//センサー4(7，6)left
double Distance_test4() {
  digitalWrite(Trig4, LOW);   
  delayMicroseconds(2);
  digitalWrite(Trig4, HIGH);  
  delayMicroseconds(20);
  digitalWrite(Trig4, LOW);   
  double Fdistance = pulseIn(Echo4, HIGH);  
  Fdistance= Fdistance / 58;       
  return Fdistance;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // 9600bpsでポートを開く
  pinMode(Echo, INPUT);  //echoピンを入力に設定  
  pinMode(Trig, OUTPUT); 
  pinMode(Echo2, INPUT);    
  pinMode(Trig2, OUTPUT);
  pinMode(Echo3, INPUT);  
  pinMode(Trig3, OUTPUT); 
  pinMode(Echo4, INPUT);    
  pinMode(Trig4, OUTPUT);
  mySerial.begin(9600); // ソフトウェアシリアルの初期化
}

void loop() {
  //Serial.print("シリアル通信");
  //####################### motor #############################
   received = 0;
   if (mySerial.available() > 0){// 受信したデータが存在する
    received = mySerial.read(); // 受信データを読み込む
   }
   if (received == 122) {//122:z（昔）
    
    CURRENT_SENSOR[0] = Distance_test();//センサ１の値。
    CURRENT_SENSOR[1] = Distance_test2();//センサ２の値。
    CURRENT_SENSOR[2] = Distance_test3();
    CURRENT_SENSOR[3] = Distance_test4();
    //delay(500);
    send();
    }

    if (received == 121) {//right_c 
    
    CURRENT_SENSOR[0] = Distance_test();//センサ１の値。
    CURRENT_SENSOR[1] = Distance_test2();//センサ２の値。
    CURRENT_SENSOR[2] = Distance_test3();
    CURRENT_SENSOR[3] = Distance_test4();
    //delay(500);
    send();
    }

    if (received == 120) {//left_c 
    
    CURRENT_SENSOR[0] = Distance_test();//センサ１の値。
    CURRENT_SENSOR[1] = Distance_test2();//センサ２の値。
    CURRENT_SENSOR[2] = Distance_test3();
    CURRENT_SENSOR[3] = Distance_test4();
    //delay(500);
    send();
    }
//######################### pc ##############################
    received_pc = 0;
    if (Serial.available() > 0){// 受信したデータが存在する
    received_pc = Serial.read(); // 受信データを読み込む
   }
   if(received_pc==114){//r
    CURRENT_SENSOR[0] = Distance_test();//センサ１の値。
    CURRENT_SENSOR[1] = Distance_test2();//センサ２の値。
    CURRENT_SENSOR[2] = Distance_test3();//right
    CURRENT_SENSOR[3] = Distance_test4();//leftr
    //delay(500);
    send();
    }
}
