
XML-ESC/POS
===========

XML-ESC/POS is a simple library that allows you to
interact with ESC/POS devices with a simple utf8 
encoded xml format similar to HTML. The following
example is self-explanatory: 

.. code:: xml
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

.. code:: python
    from xmlescpos.printer import Usb
    printer = Usb(0x04b8,0x0e03)
    printer.receipt("<div>Hello World!</div>")

Limitations
-----------
The utf8 support is incomplete, mostly asian languages
are not working since they are badly documented and
only supported by region-specific hardware.

This is also the very first release, which is a simple
extraction from the Odoo code base. While it works well,
it needs some cleanup for public use.

Also, the doc is non-existent. 
