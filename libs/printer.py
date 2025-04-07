import cairosvg
from escpos.printer import Usb


p = Usb(1137, 85,0, in_ep=0x81, out_ep=0x02)
cairosvg.svg2png(url='/mnt/c/Users/zinan/Documents/generate_receipt/output.svg', write_to='output.png')
p.image("output.png")
# p.block_text("sdasd", columns=3)

p.cut()
exit()