# DroneTools
## DroneTag -  Python Library for creating drone IDs

<img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/03-1312.png" width="300" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/%230000.png" width="300" />\
<img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/U992.png" width="364" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/12-1290.png" width="234" />

## HandlerBadge -  Python Library for creating handler IDs

<img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/style_1.barcode.png" width="250" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/style_2.barcode.png" width="250" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/style_3.barcode.png" width="250" />\
<img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/style_1.qrcode.png" width="250" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/style_2.qrcode.png" width="250" /> <img src="https://raw.githubusercontent.com/YourBoyRory/DroneTools/refs/heads/main/samples/static/style_3.qrcode.png" width="250" /> 

----

## Install Dependancies
```bash
pip install -r requirements.txt
```

## Getting Started
### DroneTag
More examples and tests in [Sample.py](Sample.py#L10-L121)\
Documentation and usage can be found in [DroneTag Docs](docs/DroneTag.md)

```python
# import the class
from DroneTools import DroneTag

drone_ids = [] # This is optional. Used to track used IDs to handle hash collisions.

# Make Drone
drone_data = {
        "name": "Rory",
        "title": "Pup Drone",
        "front_color": "#DC141E",
}
drone_tag = DroneTag(drone_data, drone_ids)

# The only key needed is 'name' or 'drone_id',
# name is used to generate a drone_id and the rest will use default values.
# See Docs and Samples for more info

# Save your tag.
drone_tag.save("/path/to/output.png")

```

### HandlerBadge
More examples and tests in [Sample.py](Sample.py#L142-L178)\
Documentation and usage can be found in [HandlerBadge Docs](docs/HandlerBadge.md)

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
    "front_color": "#DC141E",
    "badge_style": 1,
},
handlers_badge = HandlerBadge(handlers_data)

# Any not supplied keys will use default values or not be rendered.
# See Docs and Samples for more info

# Save your badge.
handlers_badge.save("/path/to/output.png")

```

----

# Docs
## [DroneTag](docs/DroneTag.md)
## [HandlerBadge Docs](docs/HandlerBadge.md)