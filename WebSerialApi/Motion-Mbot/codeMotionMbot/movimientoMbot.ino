 /*
 * OBSERVACION:
 *
 * pinAIN1 y pinAIN2 utilizan el mismo Pin de tal manera que cuando uno está a HIGH el otro estará a LOW
 * Los mismo para pinBIN1 y pinBIN2
 * El Pin stantbye ya se encuentra a +5V y por tanto en HIGH.
 *
 */
 char input;
 const int pinPWMA = 6;
 const int pinAIN1_AIN2 = 7;
 const int pinPWMB = 5;
 const int pinBIN1_BIN2 = 4;

 void setup()
 {
 pinMode(pinPWMA, OUTPUT);
 pinMode(pinAIN1_AIN2, OUTPUT);

 pinMode(pinPWMB, OUTPUT);
 pinMode(pinBIN1_BIN2, OUTPUT);
 Serial.begin(9600);
 }

 void loop()
{
  if (Serial.available()>0){

    input=Serial.read();
     
    if (input=='0'){
      Avance(255);
      delay(2000); 
    }
    else if(input=='1')
    {
      Retroceso(255);
      delay(2000);
    }
     else if(input=='2')
    {
      Izquierda(255);
      delay(2000);
    }
    else if(input=='3')
    {
      Derecha(255);
      delay(2000);
    }
    else if(input=='4')
    {
      Parar();
      delay(2000);
    }
 }
}

 void Avance(int velocidad)
 {
 analogWrite(pinPWMA, velocidad);
 digitalWrite(pinAIN1_AIN2, LOW);

 analogWrite(pinPWMB, velocidad);
 digitalWrite(pinBIN1_BIN2, HIGH);
 }

 void Retroceso(int velocidad)
 {
 analogWrite(pinPWMA, velocidad);
 digitalWrite(pinAIN1_AIN2, HIGH);

 analogWrite(pinPWMB, velocidad);
 digitalWrite(pinBIN1_BIN2, LOW);
 }

 void Izquierda(int velocidad)
 {
 analogWrite(pinPWMA, velocidad);
 digitalWrite(pinAIN1_AIN2, HIGH);

 analogWrite(pinPWMB, velocidad);
 digitalWrite(pinBIN1_BIN2, HIGH);
 }

 void Derecha(int velocidad)
 {
 analogWrite(pinPWMA, velocidad);
 digitalWrite(pinAIN1_AIN2, LOW);

 analogWrite(pinPWMB, velocidad);
 digitalWrite(pinBIN1_BIN2, LOW);
 }

 void Parar()
 {

 analogWrite(pinPWMA, 0);
 digitalWrite(pinAIN1_AIN2, HIGH);

 analogWrite(pinPWMB, 0);
 digitalWrite(pinBIN1_BIN2, HIGH);
 }
