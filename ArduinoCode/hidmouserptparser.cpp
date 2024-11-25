#include "ImprovedMouse.h"
#include "hidmouserptparser.h"

HIDMouseReportParser::HIDMouseReportParser(HIDMouseEvents *evt) : mouEvents(evt), oldButtons(0) {}

void HIDMouseReportParser::Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf) {  
  for (uint8_t but_id = 1; but_id <= 16; but_id <<= 1) {
    if (buf[0] & but_id) {
      if (!(oldButtons & but_id)) {
        mouEvents->OnButtonDn(but_id);
      }
    } else {
      if (oldButtons & but_id) {
        mouEvents->OnButtonUp(but_id);
      }
    }
  }
  oldButtons = buf[0];
 
  xm = 0;
  ym = 0;
  scr = 0;
  tilt = 0;

  //Logitech G Pro Superlight - Change these values to match your mouse hid reports
  xbrute = buf[2];
  ybrute = buf[4];
  scr = buf[6];
  tilt = buf[7];

  if(xbrute > 127){
    xm = map(xbrute, 255, 128, -1, -127);
  }
  else if(xbrute > 0){
    xm = xbrute;
  }
  if(ybrute > 127){
    ym = map(ybrute, 255, 128, -1, -127);
  }
  else if(ybrute > 0){
    ym = ybrute;
  }

  if ((xm != 0) || (ym != 0) || (scr != 0) || (tilt != 0)) {
    mouEvents->Move(xm, ym, scr, tilt);
  }
}

void HIDMouseEvents::OnButtonDn(uint8_t but_id) {
  ImprovedMouse.press(but_id);
}

void HIDMouseEvents::OnButtonUp(uint8_t but_id) {
  ImprovedMouse.release(but_id);
}

void HIDMouseEvents::Move(int8_t xm, int8_t ym, int8_t scr, int8_t tilt) {
 if (xm > 1){
  xm = xm -1;
 }
 if (ym > 1){
  ym = ym -1;
 }

 ImprovedMouse.move(xm, ym, scr);
}
