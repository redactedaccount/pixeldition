from typing import Dict, List, Any
from PIL import Image
from pixeldition.core.base import ImageTransformer


class ChannelInvertTransformer(ImageTransformer):
    """Invert (negate) specified color channels"""

    name = "channel-invert"
    description = "Invert specified color channels."
    usage_example = """
# channel_invert

Invert the red channel
$ pixeldition image.jpg --channel-invert r

Invert all channels (create negative image)
$ pixeldition image.jpg --channel-invert r g b
"""

    def transform(self, image: Image.Image, channels: List[str] = None) -> Image.Image:
        """Invert specified channels"""
        if channels is None:
            channels = ['r', 'g', 'b']

        if not self.validate_params(channels=channels):
            raise ValueError("Invalid parameters")

        if image.mode != 'RGB':
            image = image.convert('RGB')

        pixels = list(image.getdata())
        channel_map = {'r': 0, 'g': 1, 'b': 2}
        channels_to_invert = [channel_map[ch.lower()] for ch in channels]

        inverted_pixels = []
        for pixel in pixels:
            pixel_list = list(pixel)
            for idx in channels_to_invert:
                pixel_list[idx] = 255 - pixel_list[idx]
            inverted_pixels.append(tuple(pixel_list))

        new_img = Image.new('RGB', image.size)
        new_img.putdata(inverted_pixels)
        return new_img

    def validate_params(self, **params) -> bool:
        """Validate channel parameters"""
        channels = params.get('channels', [])
        valid_channels = ['r', 'g', 'b']

        for ch in channels:
            if ch.lower() not in valid_channels:
                return False
        return True

    def get_cli_args(self) -> List[Dict[str, Any]]:
        """Return CLI argument definitions"""
        return [
            {
                'flags': ['-ci','--channel-invert'],
                'nargs': '+',
                'metavar': 'CHANNEL',
                'help': 'Invert specified channels (e.g., --channel-invert r g)'
            }
        ]

    def parse_cli_args(self, args) -> Dict[str, Any]:
        """Parse CLI arguments into parameters"""
        if hasattr(args, 'channel_invert') and args.channel_invert:
            return {'channels': args.channel_invert}
        return {}