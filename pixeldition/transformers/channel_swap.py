from typing import Dict, List, Any
from PIL import Image
from pixeldition.core.base import ImageTransformer


class ChannelSwapTransformer(ImageTransformer):
    """Swap two color channels in an image"""

    name = "channel-swap"
    description = "Swap any two color channels (R, G, B)"
    usage_example = """# channel-swap

Swap red and green channels
$ pixeldition image.jpg --channel-swap r g -o output.jpg
    """

    def transform(self, image: Image.Image, channel1 : str, channel2: str) -> Image.Image:
        """Swap specified channels"""
        if not self.validate_params(channel1=channel1, channel2=channel2):
            raise ValueError("Invalid parameters")

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        pixels = list(image.getdata())
        channel_map = {'r': 0, 'g': 1, 'b': 2}
        idx1 = channel_map[channel1.lower()]
        idx2 = channel_map[channel2.lower()]

        swapped_pixels = []
        for pixel in pixels:
            pixel_list = list(pixel)
            pixel_list[idx1], pixel_list[idx2] = pixel_list[idx2], pixel_list[idx1]
            swapped_pixels.append(tuple(pixel_list))

        new_img = Image.new('RGB', image.size)
        new_img.putdata(swapped_pixels)
        return new_img

    def validate_params(self, **params) -> bool:
        """Validate channel parameters"""
        valid_channels = ['r', 'g', 'b']
        channel1 = params.get('channel1', '').lower()
        channel2 = params.get('channel2', '').lower()

        if channel1 not in valid_channels or channel2 not in valid_channels:
            return False
        return True

    def get_cli_args(self) -> List[Dict[str, Any]]:
        """Return CLI argument definitions"""
        return [
            {
                'flags': ['-cs', '--channel-swap'],
                'nargs': 2,
                'metavar': ('CH1', 'CH2'),
                'help': 'Two channels to swap (default: r g)'
            }
        ]

    def parse_cli_args(self, args) -> Dict[str, Any]:
        """Parse CLI arguments into parameters"""
        if hasattr(args, 'channel_swap') and args.channel_swap:
            return {
                'channel1': args.channel_swap[0],
                'channel2': args.channel_swap[1]
            }
        return {}