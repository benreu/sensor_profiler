
const int mosfet_pin = 12;
const int beeper_pin = 8;
const int button = 2;
int sensor_count = 1;
bool previous_switch;


void setup () {
  Serial.begin( 115200 );
  pinMode( mosfet_pin, OUTPUT );
  pinMode( beeper_pin, OUTPUT );
}

void loop () {
  digitalWrite( beeper_pin, LOW );
  if (digitalRead( button ) == LOW and previous_switch == HIGH) {
    runSensor();
  }
  previous_switch = digitalRead( button );
}

void runSensor() {
  digitalWrite( mosfet_pin, HIGH );
  delay( 100 );
  unsigned long on_millis = millis();
  while (millis() - on_millis < 10500) {
    Serial.print( sensor_count );
    Serial.print( " " );
    Serial.println( analogRead( A2 ));
    delay(10);
  }
  digitalWrite( mosfet_pin, LOW );
  digitalWrite( beeper_pin, HIGH );
  delay( 50 );
  digitalWrite( beeper_pin, LOW );
  sensor_count += 1;
}
