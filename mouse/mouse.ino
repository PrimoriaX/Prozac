#include <Mouse.h>

void setup() {
  Serial.begin(115200);
  Mouse.begin();
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    if (command == "CLICK") {
      Mouse.press();
      delay(60);
      Mouse.release();
    } else {
      int commaIndex = command.indexOf(',');
      if (commaIndex != -1) {
        int x = command.substring(0, commaIndex).toInt();
        int y = command.substring(commaIndex + 1).toInt();

        while (x != 0 || y != 0) {
          int moveX = constrain(x, -127, 127);
          int moveY = constrain(y, -127, 127);

          Mouse.move(moveX, moveY);

          x -= moveX;
          y -= moveY;
        }
      }
    }
  }
}
