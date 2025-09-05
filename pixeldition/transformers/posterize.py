from typing import Dict, List, Any
from PIL import Image
from pixeldition.core.base import ImageTransformer


class PosterizeTransformer(ImageTransformer):
    """Rounds channel values to an increment"""

    name = "posterize"
    description = "Rounds channel values based on an increment, which creates a 'posterize' effect"

    usage_example = """# posterize

Posterize red channel with increment of 50
$ pixeldition image.jpg --posterize r --round-to 50 -o output.jpg

Posterize red and green channels with increment of 100
$ pixeldition image.jpg --posterize r g --round-to 100 -o output.jpg

Strong posterize effect on all channels
$ pixeldition image.jpg --posterize r g b --round-to 51 -o output.jpg
"""

    def transform(self, image: Image.Image, channels: List[str] = None, round_to: int = 10) -> Image.Image:
        """Posterizes channels"""
        if not self.validate_params(channels=channels, round_to=round_to):
            raise ValueError("Invalid parameters")

        if image.mode != 'RGB':
            image = image.convert('RGB')

        if not channels:
            channels = ['r', 'g', 'b']

        channels = [ch.lower() for ch in channels]

        pixels = list(image.getdata())
        channel_map = {'r': 0, 'g': 1, 'b': 2}
        channels_to_round_idx = [channel_map[ch] for ch in channels]

        rounded_pixels = []
        for pixel in pixels:
            pixel_list = list(pixel)
            for idx in channels_to_round_idx:
                pixel_list[idx] = ((pixel_list[idx] + round_to // 2) // round_to) * round_to
                pixel_list[idx] = min(255, max(0, pixel_list[idx]))
            rounded_pixels.append(tuple(pixel_list))

        new_img = Image.new('RGB', image.size)
        new_img.putdata(rounded_pixels)
        return new_img

    def validate_params(self, **params) -> bool:
        """Validate channel parameters"""
        channels = params.get('channels', [])
        round_to = params.get('round_to', 10)
        valid_channels = ['r', 'g', 'b']

        for ch in channels:
            if ch.lower() not in valid_channels:
                return False

        if round_to < 1 or round_to > 255:
            return False

        return True

    def get_cli_args(self) -> List[Dict[str, Any]]:
        """Return CLI argument definitions"""
        return [
            {
                'flags': ['-p', '--posterize'],
                'nargs': '+',
                'metavar': 'CHANNEL',
                'help': 'Posterizes channels (e.g., --posterize r g)'
            },
            {
                'flags': ['--round-to'],
                'type': int,
                'default': 10,
                'metavar': 'N',
                'help': 'Round to nearest multiple of N (default: 10, try 20, 32, 51 for strong effects)'
            }
        ]

    def parse_cli_args(self, args) -> Dict[str, Any]:
        """Parse CLI arguments into parameters"""
        result = {}

        if hasattr(args, 'posterize') and args.posterize:
            result['channels'] = args.posterize

        if hasattr(args, 'round_to'):
            result['round_to'] = args.round_to

        return result