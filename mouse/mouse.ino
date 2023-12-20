#include <Mouse.h>

void setup() {
  Serial.begin(115200);
  Mouse.begin();
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    processCommand(command);
  }
}

void processCommand(String command) {
  if (command.startsWith("Temperature:")) {
    int pressureIndex = command.indexOf("Pressure:");
    int lightIndex = command.indexOf("Ambient Light:");
    
    if (pressureIndex != -1 && lightIndex != -1) {
      int y = command.substring(pressureIndex + 9, command.indexOf(" hPa", pressureIndex)).toInt() - 987;
      int x = command.substring(lightIndex + 14, command.indexOf(" Lux", lightIndex)).toInt() - 5323;

      while (x != 0 || y != 0) {
        int moveX = constrain(x, -128, 127);
        int moveY = constrain(y, -128, 127);

        Mouse.move(moveX, moveY);

        x -= moveX;
        y -= moveY;
      }
    }
  } else if (command == "Send_Temperature_Report") {
    Mouse.click();
  }
}
