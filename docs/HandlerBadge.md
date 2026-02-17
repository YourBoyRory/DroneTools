# DroneTools Docs | HandlerBadge (WIP)
## HandlerBadge - Python module for creating handler IDs

`handler_badge = HandlerBadge(handler_data)`

- `handler_data: DICT` [Required]  
    Options used to create the handler badge.  
    Keys and vaues for options are below.

##### Data Memebers
- `handler_data DICT`
    Stored options used to construct the handler badge.
- `handler_badge: PIL.Image.Image`
    Stored handler badge image.

## General Options
- `'badge_style': [ 1 - 3 ]`  
    Sets the style of the badge to one of the 3 options as shown in the [README.md](../README.md#handlerbadge----python-library-for-creating-handler-ids).  
	These styles change slightly based on if a QR code or barcode is selected.  
    When ommited, the default is 1.
- `'front_color': HEX COLOR`  
    Sets the color of text and images.  
    When ommited, the default is white.
- `'back_color': HEX COLOR`  
    Sets the color of the backgroud.  
    When ommited, the default is black.
- `'show_badge_holder': BOOLEAN`  
    When 'True' a hole is cut out in place of where a badge holder should be place.
	Useful when printing the badge out for use at a convention.   
    When ommited, the default is False.
- `'id_image_path': STRING`  
	The path of the image to show on the ID.  
    When ommited, a placeholder is used.

## Text Options
- `'front_path': STRING`  
    Sets path for the font file used for text to a custom one.  
    When ommited, the default font is used.

##### Header
- `'top_title': STRING`  
    Sets the top most title at the top of the badge.  
    When ommited, the default text is 'DRONE'.
- `'top_subtext': STRING`  
    Sets the subtitle at the top of the badge under the top most title.  
    When ommited, the default text is 'HANDLER'.

##### Side Text
- `'side_text': STRING`  
    Sets the text on the side of the badge, intended to be used for the name.  
	This text will be used at the `code_data` if it ommited.  
	When ommited, the sidebar will not be rendered.

##### Information Blocks
- `'handler_info': ARRAY[STRING]`  
    Sets the text under the ID photo. Each line of the text should be its own string in the array.  
	If the text supplied cannot fit in the Information block, it will be cut off.  
	A empty line can be inserted with a empty string. If a empty line lines up with the break of the QR code, The empty line will inherit the spacing nessisary to line the text up with the QR code rather then the default new line spacing. Example show below.

	```python
	["Authorized", "Administator of", "", "Drone", "00-0000"]
	# This string is used as defult on all styles when QR code is in use, See README.md.
	# The empty string is used to inset an empty line.
	# The empty line lines up with the break of the QR code and inherit its spacing
	```
	When ommited, a defult string is used based on the selected style.
- `'handler_side_info': ARRAY[STRING]`  
	Sets the text to the left of the ID photo. Each line of the text should be its own string in the array.  
	If the text supplied cannot fit in the Information block, it will be cut off.  
	A empty line can be inserted with a empty string.

	```python
	[
		"prn:", "they/", "them", "",
		"Gen:", "NB", "",
		"blood:", "A","",
		"Class:", "D",
	]
	# The empty strings are used to inset an empty line. 
	# This text is used in the examples in README.md.
	```
	When ommited, the info sidebar will not be rendered and the ID image in centered.
## QR/Barcode Options

- `'barcode': BOOLEAN`  
    When 'True' a barcode is generated instead of a QR code.
    This should only be used with small sizes of data, such as the badge holder name number.
    Links or messages should use a QR code.  
    Logo options are ignored in this mode.  
    When ommited, the default is 'True'.
- `'code_data': BYTES|STRING`  
    Sets what data the QR code stores.
    This can be any "bytes" object or string, and the QR code will change "versions" to fit the data.  
    When ommited, `side_text` or the first entry in `handler_info` will be used as the QR code text. 
	If no possible text is avalible, the string 'Unknown' is used in place.
- `'qr_roundness': [ 1.0 - 0.0 ]`  
    Sets roundness of the lines on the QR code. 1 is fully round and 0 is fully square.
    This option is ignored when `barcode` is set to 'True'.  
    When ommited, the QR code is rounded.
- `'barcode_height': [ 1.0 - 0.0 ]`  
    Sets height of the lines on the Barcode.
    This option is ignored when `barcode` is set to 'False' or ommited.  
    When ommited, the Barcode height is selected automatically.

##### Logo Options (Not compatible with barcodes)

- `'logo': STRING`  
    Path to the logo file. This is intended to be a solid color png.  
    This option is ignored when `barcode` is set to 'True'.  
    When ommited, the logo will not be rendered.
- `'logo_color': HEX COLOR`  
    Overrides the logo's color.  
    When ommited, `front_color` will be used.
- `'logo_size': [ 1.0 - 0.0 ]`  
    Sets the logo's size.  
    When ommited, the default is `0.2`.
- `'logo_border': [ 1.0 - 0.0 ]`  
    Sets the logo's border thickness.  
    When ommited, the default is `0.2`.
- `'border_radius': [ 1.0 - 0.0 ]`  
    Sets the logo's border corner roundness.  
    When ommited, the default is `0.125`.

# Examples
More examples and tests in [Sample.py](../Sample.py#L142-L178)

### Minimal Configuration

This example will generate a white badge with all default values.

```python
# import the class
from DroneTools import HandlerBadge

# Make Drone
handlers_badge = HandlerBadge()

# Save your badge.
handlers_badge.save("/path/to/output.png")

```

### Simple Configuration

This example puts custom text in the space next to the photo  
It also sets a custom side text, the IDs name in this case, and a custom color.

```python
# import the class
from DroneTools import HandlerBadge

# Array for stats info
handler_side_info = [
    "prn:", "they/them", "",
    "Gen:", "NB", "",
    "blood:", "A","",
    "Class:", "D",
]

# Make Badge
handlers_data = {
    "side_text": "Your Name",
	"handler_side_info": handler_side_info,
	"id_image_path": "./assets/id.jpg",
    "front_color": "#DC141E",
    "badge_style": 1,
},
handlers_badge = HandlerBadge(handlers_data)

# Any not supplied keys will use default values or not be rendered.
# See Docs and Samples for more info

# Save your badge.
handlers_badge.save("/path/to/output.png")

```

### Fine Grain Configuration
All Options in one example.  
Note that not all options are valid together, some will be ignored.

```python
# import the class
from DroneTools import HandlerBadge

# Array for stats info
handler_side_info = [
    "prn:", "they/them", "",
    "Gen:", "NB", "",
    "blood:", "A","",
    "Class:", "D",
]

# WIP
handlers_data = {}
handlers_badge = HandlerBadge(handlers_data)
# Save your badge.
handlers_badge.save("/path/to/output.png")

```