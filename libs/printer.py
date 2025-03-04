

from escpos.printer import Usb


p = Usb(1137, 85,0, in_ep=0x81, out_ep=0x02)
# p.image()
p.block_text("sdasd", columns=3)
p.cut()
exit()