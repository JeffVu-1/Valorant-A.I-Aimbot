
#include "ImprovedMouse.h"

#if defined(_USING_HID)

static const uint8_t _hidReportDescriptor[] PROGMEM = {
 
  //  Mouse
    0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)  // 54
    0x09, 0x02,                    // USAGE (Mouse)
    0xa1, 0x01,                    // COLLECTION (Application)
    0x09, 0x01,                    //   USAGE (Pointer)
    0xa1, 0x00,                    //   COLLECTION (Physical)
    0x85, 0x01,                    //     REPORT_ID (1)
    0x05, 0x09,                    //     USAGE_PAGE (Button)
    0x19, 0x01,                    //     USAGE_MINIMUM (Button 1)
    0x29, 0x05,                    //     USAGE_MAXIMUM (Button 5)
    0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
    0x25, 0x01,                    //     LOGICAL_MAXIMUM (1)
    0x95, 0x05,                    //     REPORT_COUNT (5)
    0x75, 0x01,                    //     REPORT_SIZE (1)
    0x81, 0x02,                    //     INPUT (Data,Var,Abs)
    0x95, 0x01,                    //     REPORT_COUNT (1)
    0x75, 0x03,                    //     REPORT_SIZE (3)
    0x81, 0x03,                    //     INPUT (Cnst,Var,Abs)
    0x05, 0x01,                    //     USAGE_PAGE (Generic Desktop)
    0x09, 0x30,                    //     USAGE (X)
    0x09, 0x31,                    //     USAGE (Y)
    0x09, 0x38,                    //     USAGE (Wheel)
    0x15, 0x81,                    //     LOGICAL_MINIMUM (-127)
    0x25, 0x7f,                    //     LOGICAL_MAXIMUM (127)
    0x75, 0x08,                    //     REPORT_SIZE (8)
    0x95, 0x03,                    //     REPORT_COUNT (3)
    0x81, 0x06,                    //     INPUT (Data,Var,Rel)
    0xc0,                          //   END_COLLECTION
    0xc0,                          // END_COLLECTION
};


#define LOW_BYTE(x) ((uint8_t)(x & 0xFF))
#define HIGH_BYTE(x) ((uint8_t)((x >> 8) & 0xFF))

//================================================================================
//================================================================================
//  Mouse

ImprovedMouse_::ImprovedMouse_(): _buttons(0)
{
  static HIDSubDescriptor node(_hidReportDescriptor, sizeof(_hidReportDescriptor));
  HID().AppendDescriptor(&node);
}

void ImprovedMouse_::begin() 
{
}

void ImprovedMouse_::end() 
{
}

void ImprovedMouse_::click(uint8_t b)
{
  _buttons = b;
  move(0,0,0,0);
  _buttons = 0;
  move(0,0,0,0);
}

void ImprovedMouse_::move(signed char x, signed char y, signed char wheel, signed char mouseclick)
{
  if (mouseclick == 1){
    ImprovedMouse.click();
    }
  uint8_t m[4];
  m[0] = _buttons;
  m[1] = x;
  m[2] = y;
  m[3] = wheel;
  HID().SendReport(1,m,4);
}

void ImprovedMouse_::buttons(uint8_t b)
{
  if (b != _buttons)
  {
    _buttons = b;
    move(0,0,0);
  }
}

void ImprovedMouse_::press(uint8_t b) 
{
  buttons(_buttons | b);
}

void ImprovedMouse_::release(uint8_t b)
{
  buttons(_buttons & ~b);
}

bool ImprovedMouse_::isPressed(uint8_t b)
{
  if ((b & _buttons) > 0) 
    return true;
  return false;
}

ImprovedMouse_ ImprovedMouse;

#endif
