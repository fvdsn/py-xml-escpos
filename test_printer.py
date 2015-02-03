test_temp = """
    <receipt>
        <h1>Receipt!</h1>
        <h2>div,span,p,ul,ol are also supported</h2>:w
        <line>
            <left>Product</left>
            <right>0.15</right>
        </line>
        <hr />
        <line size='double-height'>
            <left>TOTAL</left>
            <right>0.15</right>
        </line>
        <barcode encoding='ean13'>
            5449000000996
        </barcode>
        <cashdraw /> 
        <cut />
    </receipt>
"""

from xmlescpos.printer import Usb
import usb
import pprint

i = 10
pp = pprint.PrettyPrinter(indent=4)

while i:
    i-=1
    printer = Usb(0x04b8,0x0e03) 
    printer.receipt(test_temp)
    pp.pprint(printer.get_status())
    if not usb.control.get_status(printer.device):
        print "device status error"
    printer.close()