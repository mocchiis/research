#include <SoftwareSerial.h>
SoftwareSerial mySerial(12, 13); // RX, TX
int received;
int received_pc;
int Echo = 2;  
int Trig = 3; 
int Echo2 = 8;
int Trig2 = 9;

double CURRENT_SENSOR[2];
void send(){
  for (int i = 0; i < 2; i++){
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

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // 9600bpsでポートを開く
  pinMode(Echo, INPUT);  //echoピンを入力に設定  
  pinMode(Trig, OUTPUT); 
  pinMode(Echo2, INPUT);    
  pinMode(Trig2, OUTPUT);
  mySerial.begin(9600); // ソフトウェアシリアルの初期化
}

void loop() {
  //Serial.print("シリアル通信");
   received = 0;
   if (mySerial.available() > 0){// 受信したデータが存在する
    received = mySerial.read(); // 受信データを読み込む
   }
   if (received == 122) {//z
    
    CURRENT_SENSOR[0] = Distance_test();//センサ１の値。
    CURRENT_SENSOR[1] = Distance_test2();//センサ２の値。
    //delay(500);
    send();
    }

    received_pc = 0;
    if (Serial.available() > 0){// 受信したデータが存在する
    received_pc = Serial.read(); // 受信データを読み込む
   }
   if(received_pc==114){//r
    CURRENT_SENSOR[0] = Distance_test();//センサ１の値。
    CURRENT_SENSOR[1] = Distance_test2();//センサ２の値。
    //delay(500);
    send();
    }
}
