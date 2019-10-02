
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

void forward(){
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  
  analogWrite(IN1,LowSpeed);//左前off
  analogWrite(IN2,HighSpeed);//右前on
  analogWrite(IN3,HighSpeed);//左後on
  analogWrite(IN4,LowSpeed);//右後off
  
}


void back(){ 
  
  digitalWrite(ENA,HIGH);//HIGHまたはLOWを、ENAに出力 
  digitalWrite(ENB,HIGH);
  analogWrite(IN1,HighSpeed);//左前on
  analogWrite(IN2,LowSpeed);//右前off
  analogWrite(IN3,LowSpeed);//左後off
  analogWrite(IN4,HighSpeed);//右後on
}

void left(){
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  analogWrite(IN1,HighSpeed);
  analogWrite(IN2,LowSpeed);
  analogWrite(IN3,HighSpeed);
  analogWrite(IN4,LowSpeed);
  //Serial.println("Left");
}

void right(){

  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  analogWrite(IN1,LowSpeed);
  analogWrite(IN2,HighSpeed);
  analogWrite(IN3,LowSpeed);
  analogWrite(IN4,HighSpeed);  
  //Serial.println("Right");
  
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
  int normal = 0;
  int right_c = 0;
  int left_c = 0;
  //Serial.print("-----シリアル------");
  int received = 0;//a,0,1でない数字
  
   if (Serial.available() > 0){// 受信したデータが存在する
    received = Serial.read(); // 受信データを読み込む
   }
   //################# RandomWalk ####################
    if(received==97){//「a」と打ったらランダムウォーク
     for(int i=0; i<20; i++){
      int c = 5;
      c= ((int)random(-1, 3)*4 - 2) / 2;//-1~2の乱数生成→-4,0,4,8生成→-2,/2すれば「-1」「1」「-3」「3」
      Serial.println(c);
      normal =122; //z
      right_c = 121;//y
      left_c = 120;//x
      
      if(c==1){ // 乱数が１なら
        forward();
        delay(200);
        stop();
        delay(2000);
        
        mySerial.write(normal);
        delay(1000);
        
     }else if(c==-1){//乱数が-1なら
        back();
        delay(200);//0.2秒
        stop();
        delay(2000);
   
        mySerial.write(normal);
        delay(1000);
        
     }else if(c==3){//乱数が3なら
        right();
        delay(1000);//0.5秒
        stop();
        delay(200);
        forward();
        delay(200);
        stop();
        delay(2000);
        
        mySerial.write(right_c);
        delay(1000);
        
     }else if(c==-3){//乱数が-3なら
        left();
        delay(1000);//0.2秒
        stop();
        delay(200);
        forward();
        delay(200);
        stop();
        delay(2000);
        
        mySerial.write(left_c);
        delay(1000);
     } 
    
    
    
    }
  
  }
  //####################### 前後左右 ##########################
  if(received==49){//「1」と送られたら前に進むf:102
    //Serial.println(1);//←いる？これがじゃまになってる可能性
    forward();
    delay(200);
    stop();
    delay(2000);
    //normal =122; 
    //mySerial.write(normal);
    Serial.println(1);
    //Serial.write(112);//p
    delay(100);
 }
 if(received==48){//「0」と送られたら後ろに進むb:98
    //Serial.println(-1);
    back();
    delay(200);//0.2秒
    stop();
    delay(2000);
    //normal =122; 
    //mySerial.write(normal);
    Serial.println(1);
    //Serial.write(112);//p
    delay(100);
 }
 if(received==50){//「2」と送られたら右に進む
    //Serial.println(2);
    right();
    delay(800);
    stop();
    //delay(200);
    //forward();
    //delay(200);
    //stop();
    delay(2000);
    //count =122; 
    //mySerial.write(count);
    Serial.println(1);
    //Serial.write(112);//p
    delay(100);
  
  }

  if(received==51){//「3」と送られたら左に進む
    //Serial.println(3);
    left();
    delay(800);
    stop();
    //delay(200);
    //forward();
    //delay(200);
    //stop();
    delay(2000);
    //count =122; 
    //mySerial.write(count);
    Serial.println(1);
    //Serial.write(112);//p
    delay(100);
  
  } 
}
