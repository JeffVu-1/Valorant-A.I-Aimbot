
#pragma once
#include <HID.h>


#if !defined(_USING_HID)
#warning "Using legacy HID core (non pluggable)"
#else

#define MOUSE_DATA_SIZE 5
#define MOUSE_LEFT 1
#define MOUSE_RIGHT 2
#define MOUSE_MIDDLE 4
#define MOUSE_ALL (MOUSE_LEFT | MOUSE_RIGHT | MOUSE_MIDDLE)

class ImprovedMouse_ 
{
private:
  uint8_t _buttons;
  void buttons(uint8_t b);
public:
  ImprovedMouse_();
  void begin();
  void end();
  void click(uint8_t b = MOUSE_LEFT);
  void move(signed char x, signed char y, signed char wheel = 0, signed char mouseclick =0); 
  void press(uint8_t b = MOUSE_LEFT);   // press LEFT by default
  void release(uint8_t b = MOUSE_LEFT); // release LEFT by default
  bool isPressed(uint8_t b = MOUSE_LEFT); // check LEFT by default
};
extern ImprovedMouse_ ImprovedMouse;

#endif
