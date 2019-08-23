
#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3); // RX, TX

#define ENA 5
#define ENB 6
#define IN1 7//左前
#define IN2 8//右前
#define IN3 9//左後
#define IN4 11//右後
//analogPin 0-255の間
#define CarSpeed 100
#define TurnSpeed 150//回るときのスピード
#define HighSpeed 200
#define LowSpeed 0



void back(){ 
  
  digitalWrite(ENA,HIGH);//HIGHまたはLOWを、ENAに出力 
  digitalWrite(ENB,HIGH);
  analogWrite(IN1,HighSpeed);//左前on
  analogWrite(IN2,LowSpeed);//右前off
  analogWrite(IN3,LowSpeed);//左後off
  analogWrite(IN4,HighSpeed);//右後on
  //Serial.println("Forward");
}

void forward(){
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  
  analogWrite(IN1,LowSpeed);//左前off
  analogWrite(IN2,HighSpeed);//右前on
  analogWrite(IN3,HighSpeed);//左後on
  analogWrite(IN4,LowSpeed);//右後off
  //Serial.println("Back");
}

void stop(){
  digitalWrite(ENA,LOW);
  digitalWrite(ENB,LOW);
  //Serial.println("Stop!");
}


void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
   //pinMode(IN1,OUTPUT);//IN1ピンに出力の動作を指定
   //pinMode(IN2,OUTPUT);
   //pinMode(IN3,OUTPUT);
   //pinMode(IN4,OUTPUT);
   pinMode(ENA,OUTPUT);
   pinMode(ENB,OUTPUT);
   stop(); 
   mySerial.begin(9600); // ソフトウェアシリアルの初期化

}

void loop() {
  int count = 0;
  //Serial.print("-----シリアル------");
  int received = 0;//a,0,1でない数字
  
   if (Serial.available() > 0){// 受信したデータが存在する
    received = Serial.read(); // 受信データを読み込む
   }
   //#################RandomWalk####################
    if(received==97){//「a」と打ったらランダムウォーク
     for(int i=0; i<20; i++){
    
      int c = 5;
      c= (int)random(0, 2)*2 - 1;//randomwalk
      Serial.println(c);
      if(c==1){ // 乱数が１なら
        forward();
        delay(200);
        stop();
        delay(2000);
        count =122; //z
        mySerial.write(count);
        delay(1000);
        
     }else if(c==-1){//乱数が0なら
        back();
        delay(200);//0.2秒
        stop();
        delay(2000);
        count =122; 
        mySerial.write(count);
        delay(1000);
     } 
    
    }
  
  }
  //#######################前後##########################
  if(received==49){//「1」と送られたら前に進む
    Serial.println(1);
    forward();
    delay(200);
    stop();
    delay(2000);
    count =122; 
    mySerial.write(count);
    delay(1000);
 }
 if(received==48){//「0」と送られたら後ろに進む
    Serial.println(-1);
    back();
    delay(200);//0.2秒
    stop();
    delay(2000);
    count =122; 
    mySerial.write(count);
    delay(1000);
 }
}
