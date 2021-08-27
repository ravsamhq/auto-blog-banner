"""
Main module for the App.
"""

import os
import sys
import random
import shutil
import igraph
from PIL import Image, ImageDraw
from cairosvg import svg2png


class BlogBanner:
    """
    Blog Banner class to generate blog banners.
    """

    def __init__(
        self,
        icon_color_darken_ratio=0.68,
        main_icon_scale=0.4,
        main_icon_opacity=1,
        image_width=1280,
        image_height=720,
        logo_size=160,
        grid_size=8
    ):

        self.icon_color_darken_ratio = icon_color_darken_ratio
        self.main_icon_scale = main_icon_scale
        self.main_icon_opacity = main_icon_opacity
        self.image_width = image_width
        self.image_height = image_height
        self.image_padding_x = image_width // 20
        self.image_padding_y = image_height // 20
        self.logo_size = logo_size
        self.grid_size = grid_size

    def _generate_background_color(self):
        """
        Generate a random background color.
        """

        r = random.randint(0, 256)
        g = random.randint(0, 256)
        b = random.randint(0, 256)
        return (r, g, b, 255)

    def _create_icon_image(self, icon_path, background_color):
        """
        Generate a png icon from the svg icon for the banner.
        """

        icons = icon_path.replace(' ', '').split(',')

        icon_color = igraph.drawing.colors.darken(background_color, ratio=self.icon_color_darken_ratio)
        icon_color = tuple([int(_) for _ in icon_color])

        # convert rgba to hex format
        icon_color = '#{:02x}{:02x}{:02x}'.format(*icon_color)

        # create a transparent image
        icon_image = Image.new('RGBA', (self.image_width, self.image_height), color=0)

        # find the x and y coordinates for placing the icon
        points = []
        for y in range(0, self.image_height, self.image_height//self.grid_size):
            for x in range(0, self.image_width, self.image_width//self.grid_size):
                points.append([(x, y), (x+self.image_width//self.grid_size, y+self.image_height//self.grid_size)])

        for point in points:

            # create random scale and fill
            scale = round(random.uniform(0.01, 0.05), 2)
            fill_opacity = round(random.uniform(0.28, 0.5), 2)

            # randomly select a icon
            icon_path = random.choice(icons)
            with open(icon_path) as fl:
                svg_icon_original = fl.read()

            # add fill and fill opacity to svg icon
            svg_icon = svg_icon_original.replace('<svg', f'<svg fill="{icon_color}" fill-opacity="{fill_opacity}"')

            # icon image file name
            icon_file_name = 'icon.png'

            # create a png image from the svg icon
            svg2png(bytestring=svg_icon, write_to=icon_file_name, scale=scale)

            # create and open the icon
            icon = Image.open(icon_file_name, 'r')

            # create x and y coordinate for placing the icon
            icon_x = random.randint(point[0][0] + icon.size[0]//2, point[1][0] - icon.size[0]//2)
            icon_y = random.randint(point[0][1] + icon.size[1]//2, point[1][1] - icon.size[1]//2)

            # place the icon on the banner image
            icon_image.paste(icon, (icon_x, icon_y), mask=icon)

        return icon_image

    def _color_variant(self, hex_color, brightness_offset=1):
        """
        Creates a lighter version of the color.
        """

        rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
        new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
        new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb_int)

    def _create_main_icon_image(self, icon_path, background_color):
        """
        Generate a png icon from the svg icon for the banner.
        """

        # create a transparent image
        main_icon_image = Image.new('RGBA', (self.image_width, self.image_height), color=0)

        icons = icon_path.replace(' ', '').split(',')

        background_color = '#{:02x}{:02x}{:02x}'.format(*background_color)

        for index, icon_path in enumerate(icons, start=1):
            with open(icon_path) as fl:
                svg_icon_original = fl.read()

            # create the icon color
            icon_color = self._color_variant(background_color, brightness_offset=159)

            # icon image file name
            icon_file_name = 'main-icon.png'

            # create random scale and fill
            scale = self.main_icon_scale
            fill_opacity = self.main_icon_opacity

            # add fill and fill opacity to svg icon
            svg_icon = svg_icon_original.replace('<svg', f'<svg fill="{icon_color}" fill-opacity="{fill_opacity}"')

            # create a png image from the svg icon
            svg2png(bytestring=svg_icon, write_to=icon_file_name, scale=scale)

            # create and open the icon
            icon = Image.open(icon_file_name, 'r')

            if len(icons) == 1:
                icon_x = (self.image_width - icon.size[0]) // 2
            elif len(icons) == 2:
                if (index % 2 == 0):
                    icon_x = self.image_width//2 + self.image_padding_x
                elif (index % 2 != 0):
                    icon_x = self.image_width//2 - icon.size[0] - self.image_padding_x

            icon_y = (self.image_height - icon.size[1]) // 2

            # place the icon on the banner image
            main_icon_image.paste(icon, (icon_x, icon_y), mask=icon)

        return main_icon_image

    def _interpolate(self, from_color, to_color, interval):
        """
        Create an interpolation from `f_co` to `t_co`.
        """

        det_color = [(t - f) / interval for f, t in zip(from_color, to_color)]
        for i in range(interval):
            yield [round(f + det * i) for f, det in zip(from_color, det_color)]

    def _create_gradient_background_image(self, background_color):
        """
        Create a linear gradient background image from the given `background_color`.
        """

        # create a transparent image
        image = Image.new('RGBA', (self.image_width, self.image_height), color=0)

        # create a gradient transparent image
        gradient = Image.new('RGBA', (self.image_width, self.image_height), color=0)

        # create a draw object to draw gradient
        draw = ImageDraw.Draw(gradient)

        # create a from and to color
        f_co = background_color
        t_co = igraph.drawing.colors.darken(background_color, ratio=0.36)

        for i, color in enumerate(self._interpolate(f_co, t_co, image.width * 2)):
            draw.line([(i, 0), (0, i)], tuple(color), width=10)

        image = Image.alpha_composite(gradient, image)
        return image

    def create(self, title, icon):
        """
        Create the blog banner.
        """

        # define the banner image name
        img_name = f'{title}.png'

        # initialize the required values
        background_color = self._generate_background_color()

        # open the blog banner image
        banner_image = Image.new(mode='RGBA', size=(self.image_width, self.image_height))

        # create a linear gradient background image
        gradient_background_image = self._create_gradient_background_image(background_color)

        # create a icon background image
        icon_background_image = self._create_icon_image(icon, background_color)

        # create a main icon background image
        main_icon_background_image = self._create_main_icon_image(icon, background_color)

        # create ravsam logo image
        ravsam = Image.open('custom-icons/ravsam.png')
        ravsam.thumbnail((self.logo_size, self.logo_size), Image.ANTIALIAS)

        # create the final banner image with icons
        banner_image = Image.alpha_composite(main_icon_background_image, banner_image)

        # create the final banner image with icons
        banner_image = Image.alpha_composite(icon_background_image, banner_image)

        # create the final banner image
        banner_image = Image.alpha_composite(gradient_background_image, banner_image)

        # add ravsam logo
        banner_image.paste(ravsam, (self.image_width - ravsam.width - self.image_padding_x,
                                    self.image_height - ravsam.height - self.image_padding_y), mask=ravsam)

        # save the final banner image
        banner_image.save(img_name, format='png')

        return img_name

    def move(self, src, dest):
        """
        Move the banner to the destination `dest`.
        """

        try:
            shutil.move(src, dest + src)
        except shutil.Error as err:
            print(err)

    def clean(self):
        """
        Remove all the leftovers.
        """

        for fl in os.listdir('./'):
            if fl.endswith('.png'):
                os.remove(fl)


if __name__ == '__main__':

    ICONS_PATH = sys.argv[1]  # 'font/svgs/solid/robot.svg,font/svgs/brands/google.svg'
    DESTINATION = sys.argv[2]  # '/home/username/Public/blogs/hello-world/assets/images/'
    TITLE = sys.argv[3]  # 'this-is-a-demo-title'

    blog_banner = BlogBanner()

    IMG_NAME = blog_banner.create(title=TITLE, icon=ICONS_PATH)

    blog_banner.move(
        src=IMG_NAME,
        dest=DESTINATION,
    )

    os.remove('icon.png')
    os.remove('main-icon.png')
