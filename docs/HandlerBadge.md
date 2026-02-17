# DroneTools Docs | HandlerBadge (WIP)
## HandlerBadge - Python Library for creating handler IDs

`handler_badge = HandlerBadge(handler_data)`

- `handler_data: DICT` [Required]\
    Options used to create the handler badge.\
    Keys and vaues for options are below.

##### Data Memebers
- `handler_data DICT`
    Stored options used to construct the handler badge.
- `handler_badge: PIL.Image.Image`
    Stored handler badge image.

## General Options
- `'front_color': HEX COLOR`\
    Sets the color of text and images.\
    When ommited, the default is white.
- `'back_color': HEX COLOR`\
    Sets the color of the backgroud.\
    When ommited, the default is black.

## Text Options
- `'front_path': STRING`\
    Sets path for the font file used for text to a custom one.\
    When ommited, the default font is used.

## QR/Barcode Options

- `'barcode': BOOLEAN`\
    When 'True' a barcode is generated instead of a QR Code.
    This should only be used with small sizes of data, such as the ID number.
    Links or messages should use a QR code.\
    Logo options are ignored in this mode.\
    When ommited, the default is 'False'.
- `'code_data': BYTES|STRING`\
    Sets what data the QR code stores.
    This can be any "bytes" object or string, and the QR code will change "versions" to fit the data.\
    When ommited, `side_text` or the first entry in `handler_info` will be used as the QR code text.
- `'qr_roundness': [ 1.0 - 0.0 ]`\
    Sets roundness of the lines on the QR code. 1 is fully round and 0 is fully square.
    This option is ignored when `barcode` is set to 'True'.\
    When ommited, the QR code is rounded.
- `'barcode_height': [ 1.0 - 0.0 ]`\
    Sets height of the lines on the Barcode.
    This option is ignored when `barcode` is set to 'False' or ommited.\
    When ommited, the Barcode height is selected automatically.

##### Logo Options (Not compatible with barcodes)

- `'logo': STRING`\
    Path to the logo file. This is intended to be a solid color png.\
    This option is ignored when `barcode` is set to 'True'.\
    When ommited, the logo will not be rendered.
- `'logo_color': HEX COLOR`\
    Overrides the logo's color.\
    When ommited, `front_color` will be used.
- `'logo_size': [ 1.0 - 0.0 ]`\
    Sets the logo's size.\
    When ommited, the default is `0.2`.
- `'logo_border': [ 1.0 - 0.0 ]`\
    Sets the logo's border thickness.\
    When ommited, the default is `0.2`.
- `'border_radius': [ 1.0 - 0.0 ]`\
    Sets the logo's border corner roundness.\
    When ommited, the default is `0.125`.

# Examples
