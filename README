
# XML-ESC/POS

XML-ESC/POS is a simple library that allows you to
interact with ESC/POS devices with a simple utf8 
encoded xml format similar to HTML. The following
example is self-explanatory: 

    <receipt>
        <h1>Receipt!</h1>
        <h2>div,span,p,ul,ol are also supported</h2>
        <line>
            <left>Product</left>
            <right>0.15€</right>
        </line>
        <hr />
        <line size='double-height'>
            <left>TOTAL</left>
            <right>0.15€</right>
        </line>
        <barcode encoding='ean13'>
            5449000000996
        </barcode>
        <cashdraw /> 
        <cut />
    </receipt>

And printing from python is not that hard, you just
need the USB product / vendor id of your printer. 
Some common ids are found in `supported_devices.py`

    from xmlescpos.printer import Usb
    printer = Usb(0x04b8,0x0e03)
    printer.receipt("<div>Hello World!</div>")

Limitations
-----------
The utf8 support is incomplete, mostly asian languages
are not working since documentation is hard to find
and they are only supported by region-specific hardware,
which I don't have access to.

This is also the very first release, which is a simple
extraction from the Odoo code base.

Also, the doc is non-existent. 
