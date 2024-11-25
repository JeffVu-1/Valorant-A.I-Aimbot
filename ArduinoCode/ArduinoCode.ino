#include "ImprovedMouse.h"
#include "HID-Project.h"
#include <hiduniversal.h>
#include <SPI.h>
#include "hidmouserptparser.h"

#define pingCode 0xDF
USB Usb;
HIDUniversal Hid(&Usb);
HIDMouseEvents MouEvents;
HIDMouseReportParser Mou(&MouEvents);

uint8_t rawhidData[RAWHID_SIZE];
bool clientConnected = false;

void flushRawHIDBuffer() {
  RawHID.enable();
}

bool checkPing() {
  if (rawhidData[0] == pingCode) {
    RawHID.write(rawhidData, sizeof(rawhidData));
    return true;
  } else return false;
}

void setup() {
  ImprovedMouse.begin();

  if (Usb.Init() == -1)
    delay(200);

  if (!Hid.SetReportParser(0, &Mou))
    ErrorMessage<uint8_t > (PSTR("SetReportParser"), 1);
    
  RawHID.begin(rawhidData, sizeof(rawhidData));
}

void loop() {
  Usb.Task();
  if (!RawHID.available())
    return ;

  int8_t mouseclick = rawhidData[0];
  int8_t xm = rawhidData[1];
  int8_t ym = rawhidData[3];
  
  if (checkPing()) {
    clientConnected = true;
  } else if(clientConnected) {
    ImprovedMouse.move(xm,ym,0, mouseclick);
  }
  flushRawHIDBuffer();
}
