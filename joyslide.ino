#include <Trill.h>
#include <Joystick.h>

Trill trillSensor;
Joystick_ Joystick(
  JOYSTICK_DEFAULT_REPORT_ID, 
  JOYSTICK_TYPE_JOYSTICK, 
  0, // no buttons
  0, // no hat switches
  false, // no X axis
  false, // no Y axis
  false, // no Z axis
  false, // no Rx axis
  false, // no Ry axis
  false, // no Rz axis
  false, // no rudder
  false, // no throttle
  false, // no accelerator
  false, // no brake
  true  // yes steering
);

const int sliderMax = 3200;
const float thresholdPercentage = 0.15;  // % of 'deadzone' at either end to be used for 100% steering
const int threshold = sliderMax * thresholdPercentage;

const float deadzonePercentage = 0.02;  // % of slider in the middle to be a deadzone
const int deadzoneStart = sliderMax * (0.5 - deadzonePercentage / 2);
const int deadzoneEnd = sliderMax * (0.5 + deadzonePercentage / 2);

const int movementThreshold = sliderMax * 0.05; // % movement threshold for considering a touch to be a continuation of a previous touch

struct Touch {
  int location;
  unsigned long timestamp;
  bool active;
};

const int maxTouches = 5;
Touch touches[maxTouches];

void setup() {
  Serial.begin(115200);

  int ret = trillSensor.setup(Trill::TRILL_BAR);
  if(ret != 0) {
    Serial.println("Failed to initialise Trill sensor");
    Serial.print("Error code: ");
    Serial.println(ret);
  }

  trillSensor.setScanSettings(1, 10);  // Fast speed, 10-bit resolution

  // have the sensor automatically scan input as quickly as possible
  trillSensor.setAutoScanInterval(1);

  trillSensor.setNoiseThreshold(200);

  Joystick.begin();
  
  // set steering range to match the trill slider range
  Joystick.setSteeringRange(0, sliderMax);

  for (int i = 0; i < maxTouches; i++) {
    touches[i].location = -1;
    touches[i].timestamp = 0;
    touches[i].active = false;
  }
}

void loop() {
  trillSensor.read();
  
  int numTouches = trillSensor.getNumTouches();
  unsigned long currentTime = millis();

  int matchedTouches[maxTouches];
  for (int i = 0; i < maxTouches; i++) {
    matchedTouches[i] = false;
  }

  // loop to track touch order by by proximity
  for (int i = 0; i < numTouches; i++) {
    int currentLocation = trillSensor.touchLocation(i);
    bool matched = false;

    // matches any previous active touch within the movement threshold?
    for (int j = 0; j < maxTouches; j++) {
      if (touches[j].active && abs(touches[j].location - currentLocation) <= movementThreshold) {
        touches[j].location = currentLocation;
        matchedTouches[j] = true;
        matched = true;
        break;
      }
    }

    // new touch
    if (!matched) {
      for (int j = 0; j < maxTouches; j++) {
        if (!touches[j].active) {
          touches[j].location = currentLocation;
          touches[j].timestamp = currentTime;
          touches[j].active = true;
          matchedTouches[j] = true; 
          break;
        }
      }
    }
  }

  for(int i = 0; i < maxTouches; i++) {
    if(!matchedTouches[i]) {
      touches[i].active = false;
    }
  }

  // we'll use the latest touch for nulls effect
  int latestTouchIndex = -1;
  unsigned long latestTimestamp = 0;
  for (int i = 0; i < maxTouches; i++) {
    if (touches[i].active && touches[i].timestamp > latestTimestamp) {
      latestTouchIndex = i;
      latestTimestamp = touches[i].timestamp;
    }
  }

  int steeringValue = sliderMax / 2; // default no steer, middle val
  if (latestTouchIndex != -1) {
    int touchLocation = touches[latestTouchIndex].location;

    if (touchLocation <= threshold) {
      steeringValue = 0; // max left
    } else if (touchLocation >= (sliderMax - threshold)) {
      steeringValue = sliderMax; // max right
    } else if (touchLocation >= deadzoneStart && touchLocation <= deadzoneEnd) {
      steeringValue = sliderMax / 2; // centre deadzone
    } else if (touchLocation < deadzoneStart) {
      // linear map from threshold to deadzone start
      steeringValue = map(touchLocation, threshold, deadzoneStart, 0, sliderMax / 2);
    } else {
      // linear map from deadzone end to sliderMax - threshold
      steeringValue = map(touchLocation, deadzoneEnd, sliderMax - threshold, sliderMax / 2, sliderMax);
    }
  }

  Joystick.setSteering(sliderMax - steeringValue);

  // 250 Hz
  delay(4);
}