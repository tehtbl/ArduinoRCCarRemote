
int PWR = 12;

int FWD = 11;
int RWD = 10;
int LFT = 9;
int RGT = 8;

int FWD_state = false;
int RWD_state = false;
int LFT_state = false;
int RGT_state = false;

void setup()
{
  Serial.begin(9600);
  
  pinMode(PWR, OUTPUT);
  pinMode(FWD, OUTPUT);
  pinMode(RWD, OUTPUT);
  pinMode(LFT, OUTPUT);
  pinMode(RGT, OUTPUT);  
  
//  digitalWrite(PWR, HIGH);
}

void loop()
{
  int in;
  
  if (Serial.available() > 0) 
  {
    in = Serial.read();
    Serial.flush();
  }

  switch(in)
  {
    case '0':
      digitalWrite(PWR, LOW);
      break;
    case '1':
      digitalWrite(PWR, HIGH);
      break;
      
    case '2':
      FWD_state = false;
      RWD_state = false;
      LFT_state = false;
      RGT_state = false;
    
      digitalWrite(FWD, LOW);
      digitalWrite(RWD, LOW);
      digitalWrite(LFT, LOW);
      digitalWrite(RGT, LOW);
      break;

    case '4':
      FWD_state = true;
      RWD_state = false;
      LFT_state = true;
      RGT_state = false;
      break;
    case '5':
      FWD_state = true;
      RWD_state = false;
      LFT_state = false;
      RGT_state = true;
      break;

    case '8':
      FWD_state = false;
      RWD_state = true;
      LFT_state = true;
      RGT_state = false;
      break;
    case '9':
      FWD_state = false;
      RWD_state = true;
      LFT_state = false;
      RGT_state = true;
      break;
      
    case 'w':
      FWD_state = true;
      RWD_state = false;
      break;
    case 's':
      FWD_state = false;
      RWD_state = true;
      break;
    case 'a':
      LFT_state = true;
      RGT_state = false;
      break;
    case 'd':
      LFT_state = false;
      RGT_state = true;
      break;
      
    default:
      break;
  }

  // just fwd
  if ( FWD_state && !RWD_state && !LFT_state && !RGT_state )
  {
    digitalWrite(FWD, HIGH);
    digitalWrite(RWD, LOW);
    digitalWrite(LFT, LOW);
    digitalWrite(RGT, LOW);
  }  
  // fwd lft
  if ( FWD_state && !RWD_state && LFT_state && !RGT_state )
  {
    digitalWrite(FWD, HIGH);
    digitalWrite(RWD, LOW);
    digitalWrite(LFT, HIGH);
    digitalWrite(RGT, LOW);    
  }  
  // fwd rgt
  if ( FWD_state && !RWD_state && !LFT_state && RGT_state )
  {
    digitalWrite(FWD, HIGH);
    digitalWrite(RWD, LOW);
    digitalWrite(LFT, LOW);
    digitalWrite(RGT, HIGH);    
  }  

  // just rwd
  if ( !FWD_state && RWD_state && !LFT_state && !RGT_state )
  {
    digitalWrite(FWD, LOW);
    digitalWrite(RWD, HIGH);
    digitalWrite(LFT, LOW);
    digitalWrite(RGT, LOW);    
  }  
  // rwd lft
  if ( !FWD_state && RWD_state && LFT_state && !RGT_state )
  {
    digitalWrite(FWD, LOW);
    digitalWrite(RWD, HIGH);
    digitalWrite(LFT, HIGH);
    digitalWrite(RGT, LOW);    
  }  
  // rwd rgt
  if ( !FWD_state && RWD_state && !LFT_state && RGT_state )
  {
    digitalWrite(FWD, LOW);
    digitalWrite(RWD, HIGH);
    digitalWrite(LFT, LOW);
    digitalWrite(RGT, HIGH);    
  }  
  
  // just lft
  if ( !FWD_state && !RWD_state && LFT_state && !RGT_state )
  {
    digitalWrite(FWD, LOW);
    digitalWrite(RWD, LOW);
    digitalWrite(LFT, HIGH);
    digitalWrite(RGT, LOW);    
  }  
  
  // just rgt
  if ( !FWD_state && !RWD_state && !LFT_state && RGT_state )
  {
    digitalWrite(FWD, LOW);
    digitalWrite(RWD, LOW);
    digitalWrite(LFT, LOW);
    digitalWrite(RGT, HIGH);   
  }  
  
  // clear
  delay(500);
/*
  FWD_state = false;
  RWD_state = false;
  LFT_state = false;
  RGT_state = false;

  digitalWrite(FWD, LOW);
  digitalWrite(RWD, LOW);
  digitalWrite(LFT, LOW);
  digitalWrite(RGT, LOW);
*/
}
