Speed := 50
DllCall("mouse_event", "UInt", 0x0001, "Int", 0, "Int", Speed, "UInt", 0, "UPtr", 0)
Sleep, 100
