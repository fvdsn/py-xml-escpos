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
        <line size='double-height'>
                    <left>TOTAL</left>
                                <right>0.15</right>
                                        </line>
                                                <line size='double-height'>
                                                            <left>TOTAL</left>
                                                                        <right>0.15</right>
                                                                                </line>        <line size='double-height'>
                                                                                            <left>TOTAL</left>
                                                                                                        <right>0.15</right>
                                                                                                                </line>
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
from xmlescpos.exceptions import *
from xmlescpos.printer import Usb
import usb
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

try:
    printer = Usb(0x04b8,0x0202)

    printer._raw('\x1D\x28\x47\x02\x00\x30\x04');
    printer._raw('AAAA');
    printer._raw('\x0c');
    
    printer._raw('\x1c\x61\x31');
    printer._raw('BBBB');
    printer._raw('\x0c');

    printer._raw('\x1d\x28\x47\x02\x00\x50\x04');
    printer._raw('\x1D\x28\x47\x02\x00\x30\x04');
    printer._raw('\x1D\x28\x47\x02\x00\x54\x00');
    printer._raw('CCCC');
    printer._raw('\x1D\x28\x47\x02\x00\x54\x01');

    #printer.receipt(test_temp)
    pp.pprint(printer.get_printer_status())

except NoDeviceError as e:
    print "No device found %s" %str(e)
except HandleDeviceError as e:
    print "Impossible to handle the device due to previous error %s" % str(e)
except TicketNotPrinted as e:
    print "The ticket does not seems to have been fully printed %s" % str(e)
except NoStatusError as e:
    print "Impossible to get the status of the printer %s" % str(e)
finally:
    printer.close()

