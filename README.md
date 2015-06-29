
# XML-ESC/POS

XML-ESC/POS is a simple python library that allows you to
print receipts on ESC/POS Compatible receipt printers with a simple utf8 
encoded XML format similar to HTML. Barcode, pictures, 
text encoding are automatically handled. No more dicking
around with esc-pos commands !

The following example is self-explanatory: 

    <receipt>
        <h1>Receipt!</h1>
        <h2>div,span,p,ul,ol are also supported</h2>:w
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

And printing from python is quite easy, you just
need the USB product / vendor id of your printer. 
Some common ids are found in `supported_devices.py`

    from xmlescpos.printer import Usb
    printer = Usb(0x04b8,0x0e03)
    printer.receipt("<div>Hello World!</div>")

## Install

    sudo pip install pyxmlescpos

## Limitations

The utf8 support is incomplete, mostly asian languages
are not working. Documentation is hard to find, support relies on region-specific hardware, etc. There is some very basic 
support for Japanese.

# Documentation
## XML Structure
The library prints receipts defined by utf-8 encoded XML
documents. The tags and structure of the document are in
many ways similar to HTML. The two main differences between
XML-ESC/POS and HTML, is the presence of ESC/POS specific
tags, and the lack of CSS. Oh, and it is XML based, so you *must* provide
valid XML, or you'll get a traceback on your receipt.

The styling is done with custom attributes on the elements
themselves. The styling is inherited by child elements. 

## Supported HTML Tags
### Inline Tags
 - `span`,`em`,`b`
 
### Block level Tags
 - `p`,`div`,`section`,`article`,`header`,`footer`,`li`,`h1-5`,`hr`

### List tags
 - `ul`,`ol`

The indentation width is determined by the `tabwidth`
attribute, which specifies the indentation in number of white
space characters. `tabwidth` is inherited by child elements, 
like all styling attributes.

`ul` elements also support the `bullet` attribute which specifies
the character used to represent bullets. 

    <ul tabwidth='3' bullet='-'>
        <li>foo</li>
        <li>bar</li>
    </ul>

### Image Tags
The `img` tag prints the picture specified by the `src` attribute. 
The `src` attribute must contain the picture encoded in png, gif 
or jpeg in a base64 data-url.

    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAA..." />
    
## Esc/Pos Specific tags
 - `cut`, cuts the recipt
 - `partialcut`, partially cuts the receipt
 - `cashdraw`, activates the cash-drawer connected to the printer

### Barcode Tags
It is possible to include barcodes in your receipt with the `barcode
tag`. The `encoding` attribute lets you specify the barcode encoding
used, and its presence is mandatory. The following encodings are 
supported: `UPC-A`,`UPC-E`,`EAN13`,`EAN8`,`CODE39`,`ITF`,`NW7`.

    <barcode encoding="EAN13">
        5400113509509
    </barcode>

### Line Tag
The `line` tag is used to quickly layout receipt lines. Its child elements
must have either the `left` or `right` tag, and will be aligned left or right
on the same line. There is a hard limit between the left and right part of the
line, and content overflow is hidden. The placement of the limit is given
by the `line-ratio` attribute, which is the ratio of the left part's width with
the total width of the line. A ratio of 0.5 ( the default ) thus divides the line in two
equal parts. 

    <line line-ratio='0.6'>
        <left>Product Name</left>
        <right>$0.15</right>
    </line>

### Value Tag
The `value` tag is used to format numerical values. It allows to specify 
the number of digits, the decimal and thousands separator independently of
the formatting of the provided number. The following attributes are supported:

 - `value-decimals` : The number of decimals
 - `value-width`    : The number will be left-padded with zeroes until its 
   formatting has that many characters.
 - `value-decimals-separator` : The character used to seprate the decimal and
   integer part of the number.
 - `value-thousands-separator` : The character used to separate thousands.
 - `value-autoint` : The number will not print decimals if it is an integer
 - `value-symbol`  : The unit symbol will be placed before or after the number
 - `value-symbol-position` : `before` or `after`
 
<span />
    
    <value value-symbol='€' value-symbol-position='after'>
        3.1415
    </value>

Those attributes are inherited, and can thus be specified once and for all
on the receipt's root element.

## Styling Attributes

The following attributes are used to style the elements. They are inherited and can be applied to
any element.

- `align`: `left`,`right` or `center`. Specifies the text alignment.
- `underline`: `off` or `on` or `double`
- `bold`: `off` or `on`
- `size`: `normal`,`double`,`double-height`,`double-width`, the font size.
- `font`: `a` or `b`, the font used (two fonts ought to be enough ... )
- `width`: the width of block level elements, in characters. (default 48)
- `indent`: The indentation (in tabs) before a block level element.
- `tabwidth`: The number of spaces in a single indentation level (default 2)
- `color` : `black` or `red` 

