# Fix 5 pin_not_connected và 4 label_dangling:
# 1. J1: B9 pin in symbol was at y = -10.16. But j1_pins had y - 10.16 (jy - 10.16)
#    Wait, in symbol:
#    (pin passive line (at 10.16 -10.16 180) ... (number "B9"))
#    In KiCad schematic, if symbol is at (x, y), a pin at (px, py) in symbol coordinate:
#    KiCad Y axis points DOWN!
#    In symbol definition: py is Y-up or Y-down?
#    Let's check: (at 10.16 -10.16 180).
#    When placed at (x, y), pin pos = (x + 10.16, y - (-10.16)) = (x + 10.16, y + 10.16)!
#    KiCad inverts Y for symbols! (Y_pin = Y_sym - py_sym)
