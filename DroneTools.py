from PIL import Image, ImageDraw, ImageFont

class HandlerBadge():

    handler_data = {}
    handler_badge = None

    def __init__(self, handler_data={}):
        #generate datacode
        dronetools = DroneTag()
        if handler_data.get("barcode", True):
            # These are not changeable for handlers
            handler_data['code_data'] = handler_data.get("code_data", handler_data.get("side_text", handler_data.get("handler_info", ["Unknown"])[0]))
            handler_data['barcode_height'] = 5
            handler_data['quiet_zone'] = 0
            hander_code = dronetools.generate_drone_barcode(handler_data)
        else:
            handler_data['code_data'] = handler_data.get("code_data", handler_data.get("side_text", handler_data.get("handler_info", ["Unknown"])[0]))
            front_color, back_color = handler_data.get("front_color", "#FFFFFF"), handler_data.get("back_color", "#010101")
            if handler_data.get("badge_style", 2) == 2:
                handler_data['front_color'], handler_data['back_color'] = back_color, front_color
            hander_code = dronetools.place_qrcode_logo(dronetools.generate_drone_qr(handler_data), handler_data)
            handler_data['front_color'], handler_data['back_color'] = front_color, back_color
        self.handler_badge = self.generate_hander_badge(hander_code, handler_data)
        self.handler_data = handler_data


    def save(self, path=None):
        if path != None and self.handler_badge != None: self.handler_badge.save(path)
    def get_image(self):
        return self.handler_badge

    def generate_hander_badge(self, code_img, handler_data):

        # This is a standard
        badge_width = 670
        badge_height = 990

        # Not current changable
        margin = 100
        top_padding = 50
        bottom_padding=30

        style= handler_data.get("badge_style", 2)
        barcode = handler_data.get("barcode", True)
        show_badge_holder = handler_data.get("show_badge_holder", False)
        front_color = tuple(int(handler_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(handler_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        font_path = handler_data.get("font_path", "./assets/font.otf")
        id_image_path = handler_data.get("id_image_path", "./assets/id.jpg")

        if barcode: default_handler_info = ["Authorized", "Administator"]
        else: default_handler_info = ["Authorized", "Administator of", "", "Drone", "00-0000"]

        title = handler_data.get("top_title", "Drone")
        subtext = handler_data.get("top_subtext", "Handler")
        side_text = handler_data.get("side_text", "")
        handler_info = handler_data.get("handler_info", default_handler_info)
        handler_side_info = handler_data.get("handler_side_info", [])

        # Style def
        if style == 2: box_color = front_color
        else: back_color = back_color
        if style == 3:
            border_front_color = back_color
            border_back_color = tuple(max(0, int(c * 0.7)) for c in front_color)
        else:
            border_front_color = front_color
            border_back_color = back_color

        def __generate_text(text, badge_width, text_margin, modifier, text_spacing, reqested_size=None):
            # Set Font size
            font_size=1
            if reqested_size == None:
                # Auto Set Font
                font_size = 1
                text_width = 0
                while text_width <= badge_width - text_margin:
                    font = ImageFont.truetype(font_path, font_size)
                    bbox = font.getbbox(text)
                    text_width = bbox[2] - bbox[0]
                    font_size += 1
            else:
                # Set Size from option
                font_size=reqested_size
                font = ImageFont.truetype(font_path, font_size)
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
            text_height = int((bbox[3] - bbox[1])*modifier) + text_spacing
            if any(ord(c) > 127 for c in text): text_height = int(text_height*.75)
            return font, text_height, text_width

        # Draw new canvase
        new_img = Image.new("RGBA", (badge_width, badge_height), border_back_color)
        draw = ImageDraw.Draw(new_img)

        # Draw badge holder
        if show_badge_holder:
            mask = Image.new("L", (badge_width, badge_height), 255)
            holder_x = (new_img.width - 140) // 2
            ImageDraw.Draw(mask).rounded_rectangle(
                (holder_x, 40, holder_x+140, 63),
                radius=40,
                fill=0
            )
            new_img.putalpha(mask)

        # Draw Title and Subtext
        title_padding = -20
        subtext_padding = 35
        font, title_text_height, title_text_width = __generate_text(title, badge_width, margin, 1.4, title_padding)
        text_x = (new_img.width - title_text_width) // 2
        draw.text((text_x, top_padding), title, fill=border_front_color, font=font)
        font, subtext_text_height, subtext_text_width = __generate_text(subtext, badge_width, margin, 1.4, subtext_padding)
        text_x = (new_img.width - subtext_text_width) // 2
        draw.text((text_x, title_text_height+top_padding), subtext, fill=border_front_color, font=font)
        current_total_height = title_text_height+subtext_text_height+top_padding+subtext_padding+title_padding

        # Only if style 1 is selected, calculate the side text size now .
        if side_text != "" and style == 1:
            name_top_padding = -20
            name_bottom_padding = 40
            if barcode: name_side_padding= 30
            else: name_side_padding = 40
            name_text_width = badge_height - current_total_height - name_side_padding - bottom_padding
            name_font, name_text_height, dump = __generate_text(side_text, name_text_width, 0, 1.4, 0)
            name_text_height = name_text_height
            name_total_width = name_text_height+name_top_padding+name_bottom_padding
        else: name_total_width = 0

        # Load barcode for later
        code_img_height = int(badge_height*0.152)
        if barcode:
            if style == 1:
                code_img_height += code_img_height//10
            if style == 3:
                barcode_padding = bottom_padding*2
                barcode_margin = margin+50
            else:
                barcode_padding = bottom_padding
                barcode_margin = margin
            code_img_aspect_ratio = code_img.width /code_img.height
            code_img_width = badge_width - barcode_margin - name_total_width
            code_img = code_img.resize((code_img_width, code_img_height), Image.LANCZOS)
            total_code_height = code_img.height+barcode_padding
        # Load QR code for later
        else:
            if style == 1:
                QR_padding = int(bottom_padding*1.4)
                code_img_height += 10
                code_x = (margin//4)+(QR_padding//6)
            else:
                QR_padding = int(bottom_padding*2.2)
                code_x = (margin//2)+(QR_padding//6)
            code_img_aspect_ratio = code_img.width /code_img.height
            code_img_width = badge_width
            code_img_width = int(code_img_height * code_img_aspect_ratio)
            code_img = code_img.resize((code_img_width, code_img_height), Image.LANCZOS)
            total_code_height = code_img.height + QR_padding

        # Image Info Section background
        bg_width = badge_width-margin
        if not barcode or style == 3: bg_padding = bottom_padding
        else: bg_padding = max(total_code_height, bottom_padding)
        if style == 2:
            info_back_color = front_color
            info_front_color = back_color
        else:
            info_back_color = back_color
            info_front_color = front_color
        bg_height =  badge_height - current_total_height - bg_padding

        bg = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
        # Round conrners
        ImageDraw.Draw(bg).rounded_rectangle(
            (0, 0, bg_width, bg_height),
            radius=bg_width // 15,
            fill=(*info_back_color, 255),
        )
        bg_x = (new_img.width - bg_width) // 2
        new_img.paste(bg, (bg_x, current_total_height-20), bg)

        # Draw barcode now
        if barcode:
            new_img.paste(code_img, (barcode_margin//2+name_total_width, badge_height-code_img.height-barcode_padding))
            total_code_width = 0
        else:
            new_img.paste(code_img, (code_x, badge_height-code_img.height-QR_padding))
            total_code_width = code_img.width

        # Draw side text
        if side_text != "":
            # style def for style 1 is above barcode
            if style != 1:
                name_top_padding = 10
                name_bottom_padding = 0
                name_side_padding=37
            if not barcode or style == 3: name_side_padding = name_side_padding-30
            if not barcode or style != 1:
                # For style 1, this code is above barcode
                name_text_width = badge_height - current_total_height - name_side_padding - total_code_height
                name_font, name_text_height, dump = __generate_text(side_text, name_text_width, 2, 1.4, 0)
            sidetext_img = Image.new("RGB", (name_text_width, name_text_height), info_back_color)
            draw_sidetext = ImageDraw.Draw(sidetext_img)
            text_x = (sidetext_img.width - name_text_width) // 2
            draw_sidetext.text((text_x, 0), side_text, fill=info_front_color, font=name_font)
            sidetext_img = sidetext_img.rotate(90, expand=True)
            new_img.paste(sidetext_img, (((margin//2)+name_top_padding), current_total_height))
            name_total_width = name_text_height+name_top_padding+name_bottom_padding
            current_total_width = name_total_width
        else:
            current_total_width = 0

        #Photo
        photo_margin=margin//2
        badge_photo = Image.open(id_image_path)
        badge_photo = badge_photo.convert("RGBA")
        bagge_photo_aspect_ratio = badge_photo.width / badge_photo.height
        bagge_photo_height = (badge_width//2) - photo_margin
        bagge_photo_width = int(bagge_photo_height * bagge_photo_aspect_ratio)
        badge_photo = badge_photo.resize((bagge_photo_width, bagge_photo_height), Image.LANCZOS)
        photo_x = (badge_width-current_total_width) - badge_photo.width
        if handler_side_info != []:
            if style == 1: photo_x = photo_x - int(margin*0.75)
            else: photo_x = photo_x - margin
        else: photo_x = photo_x // 2
        # Create mask for round corners
        mask = Image.new("L", (badge_photo.width, badge_photo.height), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, badge_photo.width, badge_photo.height),
            radius=badge_photo.width // 15,
            fill=255
        )

        # Draw Photo background
        bg_height =  badge_width//2
        bg_width = badge_width - margin - photo_margin - current_total_width
        if style == 1: bg_width +=  photo_margin
        bg = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
        # Round conrners
        ImageDraw.Draw(bg).rounded_rectangle(
            (0, 0, bg_width, bg_height),
            radius=bg_width // 15,
            fill=(*info_front_color, 255),

        )
        bg_x = ((new_img.width - current_total_width) - bg_width) // 2
        new_img.paste(bg, (bg_x+current_total_width, current_total_height), bg)
        new_img.paste(badge_photo, (photo_x+current_total_width, current_total_height+photo_margin//2),mask)
        total_badge_photo_width=bagge_photo_width+(photo_margin*2)


        # Draw Side Hander Info
        if handler_side_info != []:
            longest_len = len(max(handler_side_info, key=len))
            for i, item in enumerate(handler_side_info):
                handler_side_info[i] = item+" "*(longest_len - len(item))
            total_side_info_text_height=0
            new_side_info_img = None
            current_side_info_img = None
            for info_text in handler_side_info[::-1]:
                if new_side_info_img:
                    current_side_info_img = new_side_info_img

                if info_text == " "*longest_len: info_bottom_padding = 20
                else: info_bottom_padding = 0
                info_margin = margin//2
                # Set Font size
                font, side_info_text_height, side_info_text_width = __generate_text(info_text, bg_width-bagge_photo_width-(photo_margin//2), info_margin, 1.4, info_bottom_padding)

                # Draw new canvase
                new_side_info_img = Image.new("RGB", (bg_width-bagge_photo_width-(photo_margin//2), side_info_text_height+total_side_info_text_height), info_front_color)

                # Center Text
                ImageDraw.Draw(new_side_info_img).text((info_margin//2, 0), info_text, fill=info_back_color, font=font)

                # paste old Image
                if current_side_info_img:
                    new_side_info_img.paste(current_side_info_img, (0, side_info_text_height))
                total_side_info_text_height += side_info_text_height
            new_img.paste(new_side_info_img, (bg_x+current_total_width, current_total_height+((bg_height-total_side_info_text_height)//2)))


        # add break here
        current_total_height += bg_height

        # Draw Hander Info
        info_top_padding = 10
        info_current_total_width = current_total_width
        last_info_text_wide = True
        for info_text in handler_info:
            if info_text == "":
                info_text = " "*10
                info_bottom_padding = 10
            else: info_bottom_padding = 0
            if style == 1: info_margin = margin
            else: info_margin = margin+50
            font, info_text_height, info_text_width = __generate_text(info_text, (badge_width-info_current_total_width), info_margin, 1.4, info_bottom_padding)
            if not barcode and current_total_height + total_code_height + info_text_height > badge_height:
                old_info_text_height = info_text_height + info_top_padding
                info_current_total_width = total_code_width
                font, info_text_height, info_text_width = __generate_text(info_text, (badge_width-info_current_total_width), info_margin, 1.4, info_bottom_padding)
                if last_info_text_wide and last_info_text == " "*10:
                    info_top_padding = info_top_padding +(badge_height-(current_total_height + total_code_height)) - 10
                last_info_text_wide = False

            #elif barcode:
            #    print(f"To many info lines to render! Stopped at: {info_text}")
            #    break
            text_x = ((badge_width-info_current_total_width) - info_text_width) // 2
            draw.text((text_x+info_current_total_width, current_total_height+info_top_padding), info_text, fill=info_front_color, font=font)
            current_total_height += info_text_height + info_top_padding
            last_info_text = info_text
            if last_info_text_wide: info_top_padding = -5
            else: info_top_padding = -10

        return new_img



class DroneTag():

    drone_ids = []
    drone_data=None
    drone_tag=None
    drone_id=None

    def __init__(self, drone_data={},  drone_ids=[]):

        # Set variables
        self.drone_data = drone_data
        self.drone_ids = drone_ids
        name = drone_data.get("name", None)
        self.drone_id = self.drone_data.get("drone_id", None)

        # Generate ID number
        if self.drone_id == None:
            if name != None:
                self.drone_id = self.generate_drone_id(name, self.drone_ids)
                self.drone_data["drone_id"] = self.drone_id
            else: return # if the user provided nothing, well just return. Maybe they just wanna use the functions.
        self.drone_ids.append(self.drone_id)

        # Generate Code
        if self.drone_data.get("barcode", False):
            drone_code = self.generate_drone_barcode(self.drone_data)
        else:
            drone_code = self.place_qrcode_logo(self.generate_drone_qr(self.drone_data), self.drone_data)

        # Construct Tag
        self.generate_drone_tag(drone_code, self.drone_data)

        # delete the name, it is no longer needed.
        self.drone_data.pop("name", None)

    def save(self, path=None):
        if path == None and self.drone_id != None: path=f'{self.drone_id}.png'
        if path != None and self.drone_tag!= None: self.drone_tag.save(path)
    def get_image(self):
        return self.drone_tag

    def generate_drone_tag(self, code_img, drone_data):

        new_img = code_img

        # Get Options
        front_color = tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        square = drone_data.get("square", False)
        is_barcode = self.drone_data.get("barcode", False)
        # Spacing
        top_padding = drone_data.get("top_padding",(20 - code_img.width//25) + 20)
        if is_barcode: bottom_padding = drone_data.get("bottom_padding", 30)
        else: bottom_padding = drone_data.get("bottom_padding", 0)
        left_padding = drone_data.get("left_padding", top_padding)
        right_padding = drone_data.get("right_padding", 0)
        #Text
        font_path = drone_data.get("font_path", "./assets/font.otf")
        text_margin = drone_data.get("text_margin", 75)
        text_spacing = drone_data.get("text_padding", 0)
        # ID
        text = drone_data.get("drone_id", "")
        id_size = drone_data.get("id_size", None)
        id_shift = drone_data.get("id_shift", 0)
        id_margin = drone_data.get("id_margin_override", text_margin)
        id_spacing = drone_data.get("id_padding_override", text_spacing)
        # Title
        side_text = drone_data.get("title", "")
        title_size = drone_data.get("title_size", None)
        title_shift = drone_data.get("title_shift", 0)
        title_margin = drone_data.get("title_margin_override", text_margin)
        title_spacing = drone_data.get("title_padding_override", text_spacing)

        def __generate_text(text, text_margin, modifier, text_spacing, reqested_size=None):
            # Set Font size
            font_size=1
            if reqested_size == None:
                # Auto Set Font
                font_size = 1
                text_width = 0
                while text_width <= code_img.width - text_margin:
                    font = ImageFont.truetype(font_path, font_size)
                    bbox = font.getbbox(text)
                    text_width = bbox[2] - bbox[0]
                    font_size += 1
            else:
                # Set Size from option
                font_size=reqested_size
                font = ImageFont.truetype(font_path, font_size)
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
            text_height = int((bbox[3] - bbox[1])*modifier) + text_spacing
            if any(ord(c) > 127 for c in text): text_height = int(text_height*.75)
            return font, text_height, text_width

        # Render Top Text
        if text != "":
            # Set Font size
            font, id_text_height, id_text_width = __generate_text(text, id_margin, 1.4, id_spacing, id_size)

            # Draw new canvase
            new_img = Image.new("RGB", (code_img.width, code_img.height + id_text_height + bottom_padding + top_padding), back_color)
            draw = ImageDraw.Draw(new_img)

            # Center Text
            text_x = (new_img.width - id_text_width) // 2
            draw.text((text_x+id_shift, top_padding), text, fill=front_color, font=font)

            # Set Image
            new_img.paste(code_img, (0, id_text_height+top_padding))

        # Render Side Text
        if side_text != "":
            # Rotate the image 90 degrees to make it easier to work with
            code_img = new_img.rotate(-90, expand=True)

            # Set Font size
            if is_barcode: title_margin += 20
            font, title_text_height, title_text_width = __generate_text(side_text, title_margin, 1.35, title_spacing, title_size)

            # Draw new canvase
            new_img = Image.new("RGB", (code_img.width, code_img.height + title_text_height + right_padding + left_padding), back_color)
            draw = ImageDraw.Draw(new_img)

            # Center Text
            text_x = ((new_img.width) - title_text_width) // 2
            draw.text((text_x+title_shift, left_padding), side_text, fill=front_color, font=font)

            # Set image and rotate image back to normal
            new_img.paste(code_img, (0, title_text_height+left_padding))
            new_img = new_img.rotate(90, expand=True)

        # Square off image
        if square:
            long_size = max(new_img.width, new_img.height)
            short_size =min(new_img.width, new_img.height)
            squared_img = Image.new("RGB", (long_size, long_size), back_color)
            if new_img.width > new_img.height:
                squared_img.paste(new_img, (0,(long_size - short_size)//2))
            else:
                squared_img.paste(new_img, ((long_size - short_size)//2, 0))
            new_img = squared_img

        self.drone_tag = new_img
        return new_img

    def place_qrcode_logo(self, qr_img, drone_data):

        # Get options
        logo = drone_data.get("logo", None)
        if logo == None:
            return qr_img # if no logo is provided, do nothing.
        else: logo = Image.open(logo)
        logo_mod = drone_data.get("logo_size", 0.2)
        logo_border = drone_data.get("logo_border", 0.2)
        border_radius = drone_data.get("border_radius", 0.125)
        front_color = drone_data.get("logo_color",
        tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        qr_img = qr_img.convert("RGBA")
        logo = logo.convert("RGBA")

        # Recolor logo
        r, g, b, a = logo.split()
        logo = Image.new("RGBA", logo.size, (*front_color, 255))
        logo.putalpha(a)

        # Resize Logo
        qr_w, qr_h = qr_img.size
        logo_size = int(qr_w*logo_mod) # Calcuale logo size
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # Add logo border
        pad = int(logo_size*logo_border) # Calcuale border padding
        bg_size = logo_size + pad * 2    # Calcuale border size
        bg = Image.new("RGBA", (bg_size, bg_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bg)
        # Round conrners
        radius = int(bg_size*border_radius)
        draw.rounded_rectangle(
            (0, 0, bg_size, bg_size),
            radius=radius,
            fill=(*back_color, 255),
        )

        # Center Logo
        bg_x = (qr_w - bg_size) // 2
        bg_y = (qr_h - bg_size) // 2
        logo_x = (qr_w - logo_size) // 2
        logo_y = (qr_h - logo_size) // 2
        qr_img.paste(bg, (bg_x, bg_y), bg)
        qr_img.paste(logo, (logo_x, logo_y), logo)

        return qr_img.convert("RGB")

    def generate_drone_qr(self, drone_data):

        # Imports for this function
        import qrcode
        from qrcode.image.styledpil import StyledPilImage
        from qrcode.image.styles.moduledrawers import RoundedModuleDrawer,SquareModuleDrawer
        from qrcode.image.styles.colormasks import SolidFillColorMask

        # Get Options
        front_color = tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        qr_roundness = drone_data.get("qr_roundness", 1)
        data = self.drone_data.get("code_data", self.drone_id)

        # QR code generation
        qr = qrcode.QRCode(
            version=None,  # auto size
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=20,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(radius_ratio=qr_roundness),
            eye_drawer=RoundedModuleDrawer(radius_ratio=qr_roundness),
            color_mask=SolidFillColorMask(
                back_color=back_color,
                front_color=front_color,
            ),
        )

        return qr_img.convert("RGB")

    def generate_drone_barcode(self, drone_data):

        # Imports for this function
        import barcode
        from barcode.writer import ImageWriter

         # Get Options
        front_color = tuple(int(drone_data.get("front_color", "#FFFFFF").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = tuple(int(drone_data.get("back_color", "#010101").lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        data = drone_data.get("code_data", self.drone_id)
        barcode_height = drone_data.get("barcode_height", len(data)+6)
        quiet_zone = drone_data.get("quiet_zone", 1.8)

        # Barcode generation
        code128 = barcode.get("Code128", data, writer=ImageWriter())
        img = code128.render(
            {
                "module_width": 0.2,
                "module_height": barcode_height,
                "quiet_zone": quiet_zone,
                "dpi": 650-(barcode_height*10),
                "write_text": False,
                "foreground": front_color,
                "background": back_color
            }
        )

        return img.convert("RGB")

    def generate_drone_id(self, name, ids=[]):
        # This just does a bunch of stuff to convert a string to a small number.
        name = name.upper()
        base_number=(ord(name[0]) // 10) * 10
        id_number=f"0{ord(name[0])%10}-"
        temp=""
        if len(name) < 2: name+=name
        for i in name[1:]:
            temp+=str(abs(ord(i)-base_number))
        temp = f"{int(temp)%10000}"
        while int(temp) < 1000: temp+="0"
        id_number+=f"{temp}"
        while id_number in ids: id_number = str(int(id_number[0])+1) + id_number[1:]
        return id_number

# Call Unit tests
if __name__ == "__main__":
    import Sample as sample
    sample.drone()
    sample.handler()


