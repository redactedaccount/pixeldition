import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))

from pixeldition.cli import PixelditionCLI
from pixeldition.core.loader import load_transformers
# Dynamically load all transformers. Placed up near imports for LoB (Locality of Behavior)
load_transformers()


def main():

    cli = PixelditionCLI()
    cli.run()

if __name__ == "__main__":
    main()

# from PIL import Image
# import sys
# import argparse
# import math
#
# def swap_channels(image_path, channel1='r', channel2='g', show_image=True):
#     """
#     Swap any two color channels in an image and optionally display it.
#
#     Args:
#         image_path (str): Path to the input image
#         channel1 (str): First channel to swap ('r', 'g', or 'b')
#         channel2 (str): Second channel to swap ('r', 'g', or 'b')
#         show_image (bool): Whether to display the image (default: True)
#
#     Returns:
#         PIL.Image: The modified image
#     """
#     # Validate channel inputs
#     valid_channels = ['r', 'g', 'b']
#     channel1 = channel1.lower()
#     channel2 = channel2.lower()
#
#     if channel1 not in valid_channels or channel2 not in valid_channels:
#         print(f"Error: Channels must be one of {valid_channels}")
#         return None
#
#     if channel1 == channel2:
#         if show_image:
#             print("Warning: Both channels are the same, no swap will occur")
#
#     try:
#         # Open the image
#         img = Image.open(image_path)
#
#         # Convert to RGB if not already
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         # Get image data as a list of pixels
#         pixels = list(img.getdata())
#
#         # Create channel mapping
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#         idx1 = channel_map[channel1]
#         idx2 = channel_map[channel2]
#
#         # Swap specified channels for each pixel
#         swapped_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#             # Swap the specified channels
#             pixel_list[idx1], pixel_list[idx2] = pixel_list[idx2], pixel_list[idx1]
#             swapped_pixels.append(tuple(pixel_list))
#
#         # Create new image with swapped pixels
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(swapped_pixels)
#
#         # Optionally display the image
#         if show_image:
#             new_img.show()
#             channel_names = {'r': 'Red', 'g': 'Green', 'b': 'Blue'}
#             print(f"{channel_names[channel1]} and {channel_names[channel2]} channels swapped successfully!")
#
#         return new_img
#
#     except FileNotFoundError:
#         print(f"Error: Could not find image file '{image_path}'")
#         return None
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def invert_channels(image_path, channels_to_invert, show_image=True):
#     """
#     Invert (negate) specified color channels.
#
#     Args:
#         image_path (str): Path to the input image
#         channels_to_invert (list): List of channels to invert ('r', 'g', 'b')
#         show_image (bool): Whether to display the image (default: True)
#
#     Returns:
#         PIL.Image: The modified image
#     """
#     # Validate channel inputs
#     valid_channels = ['r', 'g', 'b']
#     channels_to_invert = [ch.lower() for ch in channels_to_invert]
#
#     if not all(ch in valid_channels for ch in channels_to_invert):
#         print(f"Error: Channels must be one of {valid_channels}")
#         return None
#
#     try:
#         # Open the image
#         img = Image.open(image_path)
#
#         # Convert to RGB if not already
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         # Get image data as a list of pixels
#         pixels = list(img.getdata())
#
#         # Create channel mapping
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#         channels_to_invert_idx = [channel_map[ch] for ch in channels_to_invert]
#
#         # Invert specified channels for each pixel
#         inverted_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#
#             # Invert specified channels (255 - value)
#             for idx in channels_to_invert_idx:
#                 pixel_list[idx] = 255 - pixel_list[idx]
#
#             inverted_pixels.append(tuple(pixel_list))
#
#         # Create new image with inverted pixels
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(inverted_pixels)
#
#         # Optionally display the image
#         if show_image:
#             new_img.show()
#             channel_names = {'r': 'Red', 'g': 'Green', 'b': 'Blue'}
#             inverted_names = [channel_names[ch] for ch in channels_to_invert]
#             print(f"Inverted channels: {', '.join(inverted_names)}")
#
#         return new_img
#
#     except FileNotFoundError:
#         print(f"Error: Could not find image file '{image_path}'")
#         return None
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def swap_channels_from_image(img, channel1='r', channel2='g'):
#     """Apply channel swapping to an existing PIL Image object."""
#     valid_channels = ['r', 'g', 'b']
#     channel1 = channel1.lower()
#     channel2 = channel2.lower()
#
#     if channel1 not in valid_channels or channel2 not in valid_channels:
#         print(f"Error: Channels must be one of {valid_channels}")
#         return None
#
#     try:
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         pixels = list(img.getdata())
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#         idx1 = channel_map[channel1]
#         idx2 = channel_map[channel2]
#
#         swapped_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#             pixel_list[idx1], pixel_list[idx2] = pixel_list[idx2], pixel_list[idx1]
#             swapped_pixels.append(tuple(pixel_list))
#
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(swapped_pixels)
#         return new_img
#
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def clamp_channels_from_image(img, channel_limits):
#     """Apply channel clamping to an existing PIL Image object."""
#     valid_channels = ['r', 'g', 'b']
#
#     for channel in channel_limits:
#         if channel not in valid_channels:
#             print(f"Error: Channel '{channel}' must be one of {valid_channels}")
#             return None
#
#     try:
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         pixels = list(img.getdata())
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#
#         clamped_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#
#             for channel, limits in channel_limits.items():
#                 idx = channel_map[channel]
#                 value = pixel_list[idx]
#
#                 if 'floor' in limits:
#                     value = max(value, limits['floor'])
#                 if 'ceiling' in limits:
#                     value = min(value, limits['ceiling'])
#
#                 pixel_list[idx] = value
#
#             clamped_pixels.append(tuple(pixel_list))
#
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(clamped_pixels)
#         return new_img
#
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def invert_channels_from_image(img, channels_to_invert):
#     """Apply channel inversion to an existing PIL Image object."""
#     valid_channels = ['r', 'g', 'b']
#     channels_to_invert = [ch.lower() for ch in channels_to_invert]
#
#     if not all(ch in valid_channels for ch in channels_to_invert):
#         print(f"Error: Channels must be one of {valid_channels}")
#         return None
#
#     try:
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         pixels = list(img.getdata())
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#         channels_to_invert_idx = [channel_map[ch] for ch in channels_to_invert]
#
#         inverted_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#             for idx in channels_to_invert_idx:
#                 pixel_list[idx] = 255 - pixel_list[idx]
#             inverted_pixels.append(tuple(pixel_list))
#
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(inverted_pixels)
#         return new_img
#
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def pixel_drift_from_image(img, drift_intensity=50, drift_direction='radial', drift_reverse=False):
#     """Apply pixel drift to an existing PIL Image object."""
#     valid_directions = ['horizontal', 'vertical', 'radial', 'spiral', 'color-based']
#     if drift_direction not in valid_directions:
#         print(f"Error: Drift direction must be one of {valid_directions}")
#         return None
#
#     if drift_intensity < 1 or drift_intensity > 500:
#         print("Error: Drift intensity must be between 1 and 500")
#         return None
#
#     try:
#         # Convert to RGB if not already
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         width, height = img.size
#         pixels = img.load()
#
#         # Create new image
#         new_img = Image.new('RGB', (width, height))
#         new_pixels = new_img.load()
#
#         # Process each pixel (same logic as pixel_drift)
#         for y in range(height):
#             for x in range(width):
#                 r, g, b = pixels[x, y]
#                 brightness = (r + g + b) // 3
#                 brightness_norm = brightness / 255.0
#
#                 if drift_reverse:
#                     brightness_norm = 1.0 - brightness_norm
#
#                 drift_distance = int(brightness_norm * drift_intensity)
#
#                 # Calculate source coordinates based on direction
#                 if drift_direction == 'horizontal':
#                     source_x = (x + drift_distance) % width
#                     source_y = y
#                 elif drift_direction == 'vertical':
#                     source_x = x
#                     source_y = (y + drift_distance) % height
#                 elif drift_direction == 'radial':
#                     center_x, center_y = width // 2, height // 2
#                     dx = x - center_x
#                     dy = y - center_y
#                     if dx == 0 and dy == 0:
#                         angle = 0
#                     else:
#                         angle = math.atan2(dy, dx)
#                     source_x = x + int(math.cos(angle) * drift_distance)
#                     source_y = y + int(math.sin(angle) * drift_distance)
#                 elif drift_direction == 'spiral':
#                     center_x, center_y = width // 2, height // 2
#                     dx = x - center_x
#                     dy = y - center_y
#                     dist_from_center = math.sqrt(dx*dx + dy*dy)
#                     spiral_angle = dist_from_center * 0.1 + brightness_norm * 6.28
#                     source_x = x + int(math.cos(spiral_angle) * drift_distance)
#                     source_y = y + int(math.sin(spiral_angle) * drift_distance)
#                 elif drift_direction == 'color-based':
#                     if r > g and r > b:
#                         source_x = (x + drift_distance) % width
#                         source_y = y
#                     elif g > r and g > b:
#                         source_x = x
#                         source_y = (y - drift_distance) % height
#                     else:
#                         source_x = (x + drift_distance // 2) % width
#                         source_y = (y + drift_distance // 2) % height
#
#                 source_x = source_x % width
#                 source_y = source_y % height
#                 new_pixels[x, y] = pixels[source_x, source_y]
#
#         return new_img
#
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def round_channels_to_image(img, channels_to_round, round_to=10):
#     """Apply channel rounding to an existing PIL Image object."""
#     valid_channels = ['r', 'g', 'b']
#     channels_to_round = [ch.lower() for ch in channels_to_round]
#
#     if not all(ch in valid_channels for ch in channels_to_round):
#         print(f"Error: Channels must be one of {valid_channels}")
#         return None
#
#     if round_to < 1 or round_to > 255:
#         print("Error: Round-to value must be between 1 and 255")
#         return None
#
#     try:
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         pixels = list(img.getdata())
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#         channels_to_round_idx = [channel_map[ch] for ch in channels_to_round]
#
#         rounded_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#             for idx in channels_to_round_idx:
#                 pixel_list[idx] = ((pixel_list[idx] + round_to // 2) // round_to) * round_to
#                 pixel_list[idx] = min(255, max(0, pixel_list[idx]))
#             rounded_pixels.append(tuple(pixel_list))
#
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(rounded_pixels)
#         return new_img
#
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def create_channel_permutation_from_image(img, red_source='r', green_source='g', blue_source='b'):
#     """Apply channel permutation to an existing PIL Image object."""
#     valid_channels = ['r', 'g', 'b']
#     sources = [red_source.lower(), green_source.lower(), blue_source.lower()]
#
#     if not all(ch in valid_channels for ch in sources):
#         print(f"Error: All channel sources must be one of {valid_channels}")
#         return None
#
#     try:
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         pixels = list(img.getdata())
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#
#         remapped_pixels = []
#         for pixel in pixels:
#             new_r = pixel[channel_map[red_source]]
#             new_g = pixel[channel_map[green_source]]
#             new_b = pixel[channel_map[blue_source]]
#             remapped_pixels.append((new_r, new_g, new_b))
#
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(remapped_pixels)
#         return new_img
#
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def conditional_channels_from_image(img, conditional_rules):
#     """Apply conditional channel modifications to an existing PIL Image object."""
#     valid_channels = ['r', 'g', 'b', 'x']  # 'x' means all channels
#     valid_operators = ['<', '>', '<=', '>=', '==', '!=']
#
#     # Debug: print the rules being validated
#     for rule in conditional_rules:
#         print(f"Validating rule: {rule}")
#         if rule['source_channel'] not in valid_channels:
#             print(f"Error: Source channel '{rule['source_channel']}' must be one of {valid_channels}")
#             return None
#         if rule['target_channel'] not in valid_channels:
#             print(f"Error: Target channel '{rule['target_channel']}' must be one of {valid_channels}")
#             return None
#         if rule['operator'] not in valid_operators:
#             print(f"Error: Operator '{rule['operator']}' must be one of {valid_operators}")
#             return None
#
#     try:
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         pixels = list(img.getdata())
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#
#         modified_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#
#             for rule in conditional_rules:
#                 threshold = rule['threshold']
#                 operator = rule['operator']
#                 set_value = rule['set_value']
#
#                 # Handle 'x' (any/all channels) for source
#                 source_channels = []
#                 if rule['source_channel'] == 'x':
#                     source_channels = ['r', 'g', 'b']
#                 else:
#                     source_channels = [rule['source_channel']]
#
#                 # Handle 'x' (any/all channels) for target
#                 target_channels = []
#                 if rule['target_channel'] == 'x':
#                     target_channels = ['r', 'g', 'b']
#                 else:
#                     target_channels = [rule['target_channel']]
#
#                 # Check condition for each source channel
#                 for src_ch in source_channels:
#                     source_idx = channel_map[src_ch]
#                     source_value = pixel_list[source_idx]
#
#                     # Check condition
#                     condition_met = False
#                     if operator == '<':
#                         condition_met = source_value < threshold
#                     elif operator == '>':
#                         condition_met = source_value > threshold
#                     elif operator == '<=':
#                         condition_met = source_value <= threshold
#                     elif operator == '>=':
#                         condition_met = source_value >= threshold
#                     elif operator == '==':
#                         condition_met = source_value == threshold
#                     elif operator == '!=':
#                         condition_met = source_value != threshold
#
#                     # Apply modification to target channels if condition is met
#                     if condition_met:
#                         for tgt_ch in target_channels:
#                             target_idx = channel_map[tgt_ch]
#                             pixel_list[target_idx] = set_value
#
#             modified_pixels.append(tuple(pixel_list))
#
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(modified_pixels)
#         return new_img
#
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def pixel_drift(image_path, drift_intensity=50, drift_direction='radial', drift_reverse=False, show_image=True):
#     """
#     Apply pixel drift effect where pixels are replaced based on their brightness.
#
#     Args:
#         image_path (str): Path to the input image
#         drift_intensity (int): How far pixels can drift (default: 50)
#         drift_direction (str): Direction of drift ('horizontal', 'vertical', 'radial', 'spiral', 'color-based')
#         drift_reverse (bool): If True, bright pixels drift less, dark pixels drift more
#         show_image (bool): Whether to display the image (default: True)
#
#     Returns:
#         PIL.Image: The modified image
#     """
#     valid_directions = ['horizontal', 'vertical', 'radial', 'spiral', 'color-based']
#     if drift_direction not in valid_directions:
#         print(f"Error: Drift direction must be one of {valid_directions}")
#         return None
#
#     if drift_intensity < 1 or drift_intensity > 500:
#         print("Error: Drift intensity must be between 1 and 500")
#         return None
#
#     try:
#         # Open the image
#         img = Image.open(image_path)
#
#         # Convert to RGB if not already
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         width, height = img.size
#         pixels = img.load()  # Use load() for faster pixel access
#
#         # Create new image
#         new_img = Image.new('RGB', (width, height))
#         new_pixels = new_img.load()
#
#         # Process each pixel
#         for y in range(height):
#             for x in range(width):
#                 r, g, b = pixels[x, y]
#
#                 # Calculate brightness (0-255)
#                 brightness = (r + g + b) // 3
#
#                 # Normalize brightness to 0-1 range
#                 brightness_norm = brightness / 255.0
#
#                 # Apply reverse if requested
#                 if drift_reverse:
#                     brightness_norm = 1.0 - brightness_norm
#
#                 # Calculate drift distance based on brightness
#                 drift_distance = int(brightness_norm * drift_intensity)
#
#                 # Calculate source coordinates based on direction
#                 if drift_direction == 'horizontal':
#                     # Drift horizontally based on brightness
#                     source_x = (x + drift_distance) % width
#                     source_y = y
#
#                 elif drift_direction == 'vertical':
#                     # Drift vertically based on brightness
#                     source_x = x
#                     source_y = (y + drift_distance) % height
#
#                 elif drift_direction == 'radial':
#                     # Drift radially outward from center
#                     center_x, center_y = width // 2, height // 2
#                     dx = x - center_x
#                     dy = y - center_y
#
#                     # Calculate angle from center
#                     if dx == 0 and dy == 0:
#                         angle = 0
#                     else:
#                         angle = math.atan2(dy, dx)
#
#                     # Move along the radial direction
#                     source_x = x + int(math.cos(angle) * drift_distance)
#                     source_y = y + int(math.sin(angle) * drift_distance)
#
#                 elif drift_direction == 'spiral':
#                     # Create spiral drift pattern
#                     center_x, center_y = width // 2, height // 2
#                     dx = x - center_x
#                     dy = y - center_y
#
#                     # Calculate distance from center for spiral effect
#                     dist_from_center = math.sqrt(dx*dx + dy*dy)
#                     spiral_angle = dist_from_center * 0.1 + brightness_norm * 6.28  # 2*pi
#
#                     source_x = x + int(math.cos(spiral_angle) * drift_distance)
#                     source_y = y + int(math.sin(spiral_angle) * drift_distance)
#
#                 elif drift_direction == 'color-based':
#                     # Drift direction based on dominant color
#                     if r > g and r > b:  # Red dominant - drift right
#                         source_x = (x + drift_distance) % width
#                         source_y = y
#                     elif g > r and g > b:  # Green dominant - drift up
#                         source_x = x
#                         source_y = (y - drift_distance) % height
#                     else:  # Blue dominant - drift diagonally
#                         source_x = (x + drift_distance // 2) % width
#                         source_y = (y + drift_distance // 2) % height
#
#                 # Wrap coordinates to stay within image bounds
#                 source_x = source_x % width
#                 source_y = source_y % height
#
#                 # Get pixel from source location
#                 new_pixels[x, y] = pixels[source_x, source_y]
#
#         # Optionally display the image
#         if show_image:
#             new_img.show()
#             direction_desc = drift_direction.replace('_', '-')
#             reverse_desc = " (reversed)" if drift_reverse else ""
#             print(f"Applied pixel drift: intensity={drift_intensity}, direction={direction_desc}{reverse_desc}")
#
#         return new_img
#
#     except FileNotFoundError:
#         print(f"Error: Could not find image file '{image_path}'")
#         return None
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def conditional_channels(image_path, conditional_rules, show_image=True):
#     """
#     Apply conditional modifications to channels based on other channel values.
#     If source_channel meets condition, set target_channel to specified value.
#
#     Args:
#         image_path (str): Path to the input image
#         conditional_rules (list): List of rules like [{'source_channel': 'r', 'operator': '<',
#                                  'threshold': 50, 'target_channel': 'r', 'set_value': 0}]
#         show_image (bool): Whether to display the image (default: True)
#
#     Returns:
#         PIL.Image: The modified image
#     """
#     # Validate inputs
#     valid_channels = ['r', 'g', 'b', 'x']  # 'x' means all channels
#     valid_operators = ['<', '>', '<=', '>=', '==', '!=']
#
#     for rule in conditional_rules:
#         if rule['source_channel'] not in valid_channels:
#             print(f"Error: Source channel '{rule['source_channel']}' must be one of {valid_channels}")
#             return None
#         if rule['target_channel'] not in valid_channels:
#             print(f"Error: Target channel '{rule['target_channel']}' must be one of {valid_channels}")
#             return None
#         if rule['operator'] not in valid_operators:
#             print(f"Error: Operator '{rule['operator']}' must be one of {valid_operators}")
#             return None
#
#         threshold = rule['threshold']
#         set_value = rule['set_value']
#         if threshold < 0 or threshold > 255 or set_value < 0 or set_value > 255:
#             print(f"Error: Threshold and set values must be between 0 and 255")
#             return None
#
#     try:
#         # Open the image
#         img = Image.open(image_path)
#
#         # Convert to RGB if not already
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         # Get image data as a list of pixels
#         pixels = list(img.getdata())
#
#         # Create channel mapping
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#
#         # Apply conditional rules to each pixel
#         modified_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#
#             # Apply each rule
#             for rule in conditional_rules:
#                 threshold = rule['threshold']
#                 operator = rule['operator']
#                 set_value = rule['set_value']
#
#                 # Handle 'x' (any/all channels) for source
#                 source_channels = []
#                 if rule['source_channel'] == 'x':
#                     source_channels = ['r', 'g', 'b']
#                 else:
#                     source_channels = [rule['source_channel']]
#
#                 # Handle 'x' (any/all channels) for target
#                 target_channels = []
#                 if rule['target_channel'] == 'x':
#                     target_channels = ['r', 'g', 'b']
#                 else:
#                     target_channels = [rule['target_channel']]
#
#                 # Check condition for each source channel
#                 for src_ch in source_channels:
#                     source_idx = channel_map[src_ch]
#                     source_value = pixel_list[source_idx]
#
#                     # Check condition
#                     condition_met = False
#                     if operator == '<':
#                         condition_met = source_value < threshold
#                     elif operator == '>':
#                         condition_met = source_value > threshold
#                     elif operator == '<=':
#                         condition_met = source_value <= threshold
#                     elif operator == '>=':
#                         condition_met = source_value >= threshold
#                     elif operator == '==':
#                         condition_met = source_value == threshold
#                     elif operator == '!=':
#                         condition_met = source_value != threshold
#
#                     # Apply modification to target channels if condition is met
#                     if condition_met:
#                         for tgt_ch in target_channels:
#                             target_idx = channel_map[tgt_ch]
#                             pixel_list[target_idx] = set_value
#
#             modified_pixels.append(tuple(pixel_list))
#
#         # Create new image with modified pixels
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(modified_pixels)
#
#         # Optionally display the image
#         if show_image:
#             new_img.show()
#
#             # Print summary of applied rules
#             channel_names = {'r': 'Red', 'g': 'Green', 'b': 'Blue', 'x': 'All'}
#             rule_descriptions = []
#             for rule in conditional_rules:
#                 src_name = channel_names[rule['source_channel']]
#                 tgt_name = channel_names[rule['target_channel']]
#                 operator = rule['operator']
#                 threshold = rule['threshold']
#                 set_value = rule['set_value']
#                 rule_descriptions.append(f"If {src_name} {operator} {threshold} → set {tgt_name} = {set_value}")
#
#             print(f"Applied conditional rules: {'; '.join(rule_descriptions)}")
#
#         return new_img
#
#     except FileNotFoundError:
#         print(f"Error: Could not find image file '{image_path}'")
#         return None
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def clamp_channels(image_path, channel_limits, show_image=True):
#     """
#     Apply floor and/or ceiling limits to specified channels.
#
#     Args:
#         image_path (str): Path to the input image
#         channel_limits (dict): Dictionary with channel limits
#         show_image (bool): Whether to display the image (default: True)
#
#     Returns:
#         PIL.Image: The modified image
#     """
#     # Validate channel inputs
#     valid_channels = ['r', 'g', 'b']
#
#     for channel in channel_limits:
#         if channel not in valid_channels:
#             print(f"Error: Channel '{channel}' must be one of {valid_channels}")
#             return None
#
#         limits = channel_limits[channel]
#         if 'floor' in limits and (limits['floor'] < 0 or limits['floor'] > 255):
#             print(f"Error: Floor value for {channel} must be between 0 and 255")
#             return None
#         if 'ceiling' in limits and (limits['ceiling'] < 0 or limits['ceiling'] > 255):
#             print(f"Error: Ceiling value for {channel} must be between 0 and 255")
#             return None
#         if 'floor' in limits and 'ceiling' in limits and limits['floor'] > limits['ceiling']:
#             print(f"Error: Floor ({limits['floor']}) cannot be higher than ceiling ({limits['ceiling']}) for {channel}")
#             return None
#
#     try:
#         # Open the image
#         img = Image.open(image_path)
#
#         # Convert to RGB if not already
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         # Get image data as a list of pixels
#         pixels = list(img.getdata())
#
#         # Create channel mapping
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#
#         # Apply limits to specified channels for each pixel
#         clamped_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#
#             # Apply limits to each specified channel
#             for channel, limits in channel_limits.items():
#                 idx = channel_map[channel]
#                 value = pixel_list[idx]
#
#                 # Apply floor (minimum value)
#                 if 'floor' in limits:
#                     value = max(value, limits['floor'])
#
#                 # Apply ceiling (maximum value)
#                 if 'ceiling' in limits:
#                     value = min(value, limits['ceiling'])
#
#                 pixel_list[idx] = value
#
#             clamped_pixels.append(tuple(pixel_list))
#
#         # Create new image with clamped pixels
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(clamped_pixels)
#
#         # Optionally display the image
#         if show_image:
#             new_img.show()
#
#             # Print summary of applied limits
#             channel_names = {'r': 'Red', 'g': 'Green', 'b': 'Blue'}
#             limit_descriptions = []
#             for channel, limits in channel_limits.items():
#                 parts = []
#                 if 'floor' in limits:
#                     parts.append(f"floor={limits['floor']}")
#                 if 'ceiling' in limits:
#                     parts.append(f"ceiling={limits['ceiling']}")
#                 limit_descriptions.append(f"{channel_names[channel]}({', '.join(parts)})")
#
#             print(f"Applied channel limits: {', '.join(limit_descriptions)}")
#
#         return new_img
#
#     except FileNotFoundError:
#         print(f"Error: Could not find image file '{image_path}'")
#         return None
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def round_channels(image_path, channels_to_round, round_to=10):
#     """
#     Round specified channels to the nearest multiple of a given value.
#
#     Args:
#         image_path (str): Path to the input image
#         channels_to_round (list): List of channels to round ('r', 'g', 'b')
#         round_to (int): Value to round to nearest multiple of (default: 10)
#
#     Returns:
#         PIL.Image: The modified image
#     """
#     # Validate channel inputs
#     valid_channels = ['r', 'g', 'b']
#     channels_to_round = [ch.lower() for ch in channels_to_round]
#
#     if not all(ch in valid_channels for ch in channels_to_round):
#         print(f"Error: Channels must be one of {valid_channels}")
#         return None
#
#     if round_to < 1 or round_to > 255:
#         print("Error: Round-to value must be between 1 and 255")
#         return None
#
#     try:
#         # Open the image
#         img = Image.open(image_path)
#
#         # Convert to RGB if not already
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         # Get image data as a list of pixels
#         pixels = list(img.getdata())
#
#         # Create channel mapping
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#         channels_to_round_idx = [channel_map[ch] for ch in channels_to_round]
#
#         # Round specified channels for each pixel
#         rounded_pixels = []
#         for pixel in pixels:
#             pixel_list = list(pixel)
#
#             # Round specified channels to nearest multiple
#             for idx in channels_to_round_idx:
#                 # Round to nearest multiple: (value + round_to//2) // round_to * round_to
#                 # This ensures proper rounding behavior
#                 pixel_list[idx] = ((pixel_list[idx] + round_to // 2) // round_to) * round_to
#                 # Ensure value stays in valid range [0, 255]
#                 pixel_list[idx] = min(255, max(0, pixel_list[idx]))
#
#             rounded_pixels.append(tuple(pixel_list))
#
#         # Create new image with rounded pixels
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(rounded_pixels)
#
#         # Display the image
#         new_img.show()
#
#         channel_names = {'r': 'Red', 'g': 'Green', 'b': 'Blue'}
#         rounded_names = [channel_names[ch] for ch in channels_to_round]
#         print(f"Rounded channels to nearest {round_to}: {', '.join(rounded_names)}")
#
#         return new_img
#
#     except FileNotFoundError:
#         print(f"Error: Could not find image file '{image_path}'")
#         return None
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def create_channel_permutation(image_path, red_source='r', green_source='g', blue_source='b', show_image=True):
#     """
#     Remap RGB channels to any permutation.
#
#     Args:
#         image_path (str): Path to the input image
#         red_source (str): Source channel for red output ('r', 'g', or 'b')
#         green_source (str): Source channel for green output ('r', 'g', or 'b')
#         blue_source (str): Source channel for blue output ('r', 'g', or 'b')
#         show_image (bool): Whether to display the image (default: True)
#
#     Returns:
#         PIL.Image: The modified image
#     """
#     # Validate inputs
#     valid_channels = ['r', 'g', 'b']
#     sources = [red_source.lower(), green_source.lower(), blue_source.lower()]
#
#     if not all(ch in valid_channels for ch in sources):
#         print(f"Error: All channel sources must be one of {valid_channels}")
#         return None
#
#     try:
#         # Open the image
#         img = Image.open(image_path)
#
#         # Convert to RGB if not already
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
#
#         # Get image data
#         pixels = list(img.getdata())
#
#         # Create channel mapping
#         channel_map = {'r': 0, 'g': 1, 'b': 2}
#
#         # Remap channels for each pixel
#         remapped_pixels = []
#         for pixel in pixels:
#             new_r = pixel[channel_map[red_source]]
#             new_g = pixel[channel_map[green_source]]
#             new_b = pixel[channel_map[blue_source]]
#             remapped_pixels.append((new_r, new_g, new_b))
#
#         # Create new image
#         new_img = Image.new('RGB', img.size)
#         new_img.putdata(remapped_pixels)
#
#         # Optionally display the image
#         if show_image:
#             new_img.show()
#             print(f"Channels remapped: R←{red_source.upper()}, G←{green_source.upper()}, B←{blue_source.upper()}")
#
#         return new_img
#
#     except FileNotFoundError:
#         print(f"Error: Could not find image file '{image_path}'")
#         return None
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None
#
# def main():
#     """Main function with argument parsing"""
#     parser = argparse.ArgumentParser(
#         description='Swap or remap color channels in an image',
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog="""
# Examples:
#   %(prog)s image.jpg                          # Swap red and green (default)
#   %(prog)s image.jpg -s r b                   # Swap red and blue
#   %(prog)s image.jpg -s g b                   # Swap green and blue
#   %(prog)s image.jpg --invert r               # Invert red channel (alien effect)
#   %(prog)s image.jpg --invert r g             # Invert red and green channels
#   %(prog)s image.jpg --invert r g b           # Invert all channels (full negative)
#   %(prog)s image.jpg --drift 50               # Pixel drift with radial direction
#   %(prog)s image.jpg --drift 100 --drift-direction spiral  # Spiral drift effect
#   %(prog)s image.jpg --drift 75 --drift-direction color-based  # Color-based drift
#   %(prog)s image.jpg --drift 80 --drift-reverse  # Reversed drift (dark pixels move more)
#   %(prog)s image.jpg --floor r 100            # Set red minimum to 100
#   %(prog)s image.jpg --ceiling g 150          # Set green maximum to 150
#   %(prog)s image.jpg --floor r 80 --ceiling r 200  # Red between 80-200
#   %(prog)s image.jpg --floor r 100 --floor g 50    # Multiple channel floors
#   %(prog)s image.jpg --round r                # Round red channel to nearest 10
#   %(prog)s image.jpg --round r g b            # Round all channels to nearest 10
#   %(prog)s image.jpg --round r --round-to 20  # Round red to nearest 20 (strong effect)
#   %(prog)s image.jpg --round r g --round-to 32  # Round red+green to nearest 32
#   %(prog)s image.jpg --round r g b --round-to 51  # Extreme posterize effect
#   %(prog)s image.jpg --if r '<' 50 r 0        # Set red values below 50 to 0 (remove dark reds)
#   %(prog)s image.jpg --if r '<' 50 r 255      # Set red values below 50 to 255 (bright shadows)
#   %(prog)s image.jpg --if g '>' 200 b 0       # If green > 200, set blue to 0 (remove blue from bright greens)
#   %(prog)s image.jpg --if x '<' 50 x 0        # Set ALL channel values below 50 to 0 (remove all dark colors)
#   %(prog)s image.jpg --if x '>' 200 x 255     # Set ALL channel values above 200 to 255 (extreme contrast)
#   %(prog)s image.jpg --if r '>' 150 x 0       # If red > 150, set ALL channels to 0 (black out red areas)
#   %(prog)s image.jpg --if x '==' 128 x 255    # If any channel exactly 128, set all channels to 255
#   %(prog)s image.jpg --if r '<' 50 r 0 --if g '<' 50 g 0  # Multiple conditions
#   %(prog)s image.jpg -r g -g r -b b           # Custom remapping: R←G, G←R, B←B
#   %(prog)s image.jpg -r b -g g -b r           # Custom remapping: R←B, G←G, B←R
#         """
#     )
#
#     parser.add_argument('image', help='Path to input image file')
#
#     # Group for channel inversion
#     invert_group = parser.add_argument_group('Channel Inversion')
#     invert_group.add_argument('--invert', nargs='+', metavar='CHANNEL',
#                              help='Invert specified channels (e.g., --invert r g)')
#
#     # Group for pixel drift effect
#     drift_group = parser.add_argument_group('Pixel Drift Effect')
#     drift_group.add_argument('--drift', type=int, metavar='INTENSITY',
#                             help='Apply pixel drift effect with given intensity (1-500)')
#     drift_group.add_argument('--drift-direction', choices=['horizontal', 'vertical', 'radial', 'spiral', 'color-based'],
#                             default='radial', help='Direction of pixel drift (default: radial)')
#     drift_group.add_argument('--drift-reverse', action='store_true',
#                             help='Reverse drift logic (bright pixels drift less)')
#
#     # Group for channel clamping
#     clamp_group = parser.add_argument_group('Channel Clamping (Floor/Ceiling)')
#     clamp_group.add_argument('--floor', action='append', nargs=2, metavar=('CHANNEL', 'VALUE'),
#                             help='Set minimum value for a channel (e.g., --floor r 100)')
#     clamp_group.add_argument('--ceiling', action='append', nargs=2, metavar=('CHANNEL', 'VALUE'),
#                             help='Set maximum value for a channel (e.g., --ceiling g 200)')
#
#     # Group for channel thresholding
#     conditional_group = parser.add_argument_group('Conditional Channel Modification')
#     conditional_group.add_argument('--if', action='append', nargs=5,
#                                   metavar=('SRC_CHANNEL', 'OPERATOR', 'THRESHOLD', 'TGT_CHANNEL', 'SET_VALUE'),
#                                   help='If SRC_CHANNEL OPERATOR THRESHOLD, set TGT_CHANNEL to SET_VALUE (use \'x\' for all channels, e.g., --if x \'<\' 50 x 0)')
#
#     # Group for channel rounding
#     round_group = parser.add_argument_group('Channel Rounding')
#     round_group.add_argument('--round', nargs='+', metavar='CHANNEL',
#                             help='Round specified channels to nearest multiple (e.g., --round r g)')
#     round_group.add_argument('--round-to', type=int, default=10, metavar='N',
#                             help='Round to nearest multiple of N (default: 10, try 20, 32, 51 for strong effects)')
#
#     # Group for simple swapping
#     swap_group = parser.add_argument_group('Simple Channel Swapping')
#     swap_group.add_argument('-s', '--swap', nargs=2, metavar=('CH1', 'CH2'),
#                            default=['r', 'g'],
#                            help='Two channels to swap (default: r g)')
#
#     # Group for advanced remapping
#     remap_group = parser.add_argument_group('Advanced Channel Remapping')
#     remap_group.add_argument('-r', '--red-source', metavar='CHANNEL',
#                             help='Source channel for red output (r/g/b)')
#     remap_group.add_argument('-g', '--green-source', metavar='CHANNEL',
#                             help='Source channel for green output (r/g/b)')
#     remap_group.add_argument('-b', '--blue-source', metavar='CHANNEL',
#                             help='Source channel for blue output (r/g/b)')
#
#     args = parser.parse_args()
#
#     # Start with the original image
#     current_image = args.image
#     effects_applied = []
#
#     # Parse all arguments and their positions to apply effects in order
#     import sys
#     arg_positions = []
#
#     # Get the raw command line arguments to determine order
#     raw_args = sys.argv[1:]  # Skip script name
#
#     # Parse arguments to find their positions and types
#     i = 0
#     while i < len(raw_args):
#         arg = raw_args[i]
#
#         if arg == '--invert' and i + 1 < len(raw_args):
#             # Find how many channels follow
#             channels = []
#             j = i + 1
#             while j < len(raw_args) and raw_args[j] in ['r', 'g', 'b']:
#                 channels.append(raw_args[j])
#                 j += 1
#             if channels:
#                 arg_positions.append((i, 'invert', channels))
#                 i = j
#             else:
#                 i += 1
#
#         elif arg == '--floor' and i + 2 < len(raw_args):
#             channel = raw_args[i + 1]
#             value = raw_args[i + 2]
#             arg_positions.append((i, 'floor', (channel, value)))
#             i += 3
#
#         elif arg == '--ceiling' and i + 2 < len(raw_args):
#             channel = raw_args[i + 1]
#             value = raw_args[i + 2]
#             arg_positions.append((i, 'ceiling', (channel, value)))
#             i += 3
#
#         elif arg == '--if' and i + 5 < len(raw_args):
#             src_channel = raw_args[i + 1]
#             operator = raw_args[i + 2]
#             threshold = raw_args[i + 3]
#             tgt_channel = raw_args[i + 4]
#             set_value = raw_args[i + 5]
#             arg_positions.append((i, 'conditional', (src_channel, operator, threshold, tgt_channel, set_value)))
#             i += 6
#
#         elif arg == '--round' and i + 1 < len(raw_args):
#             channels = []
#             j = i + 1
#             while j < len(raw_args) and raw_args[j] in ['r', 'g', 'b']:
#                 channels.append(raw_args[j])
#                 j += 1
#             if channels:
#                 # Get round-to value if it exists
#                 round_to = 10  # default
#                 if '--round-to' in raw_args:
#                     round_to_idx = raw_args.index('--round-to')
#                     if round_to_idx + 1 < len(raw_args):
#                         try:
#                             round_to = int(raw_args[round_to_idx + 1])
#                         except ValueError:
#                             pass
#                 arg_positions.append((i, 'round', (channels, round_to)))
#                 i = j
#             else:
#                 i += 1
#
#         elif arg == '-s' and i + 2 < len(raw_args):
#             ch1 = raw_args[i + 1]
#             ch2 = raw_args[i + 2]
#             arg_positions.append((i, 'swap', (ch1, ch2)))
#             i += 3
#
#         elif arg == '--drift' and i + 1 < len(raw_args):
#             try:
#                 intensity = int(raw_args[i + 1])
#                 # Get direction if specified
#                 direction = 'radial'  # default
#                 reverse = False
#                 if '--drift-direction' in raw_args:
#                     dir_idx = raw_args.index('--drift-direction')
#                     if dir_idx + 1 < len(raw_args):
#                         direction = raw_args[dir_idx + 1]
#                 if '--drift-reverse' in raw_args:
#                     reverse = True
#                 arg_positions.append((i, 'drift', (intensity, direction, reverse)))
#                 i += 2
#             except ValueError:
#                 i += 1
#
#         elif arg in ['-r', '-g', '-b'] and i + 1 < len(raw_args):
#             # Handle remapping - collect all three if they exist
#             remap_data = {}
#             if args.red_source:
#                 remap_data['r'] = args.red_source
#             if args.green_source:
#                 remap_data['g'] = args.green_source
#             if args.blue_source:
#                 remap_data['b'] = args.blue_source
#
#             # Only add remap once when we see the first remap argument
#             if len(remap_data) == 3 and not any(effect[1] == 'remap' for effect in arg_positions):
#                 arg_positions.append((i, 'remap', remap_data))
#             i += 2
#
#         else:
#             i += 1
#
#     # Sort effects by their position in the command line
#     arg_positions.sort(key=lambda x: x[0])
#
#     # Apply effects in argument order
#     for pos, effect_type, params in arg_positions:
#
#         if effect_type == 'invert':
#             if isinstance(current_image, str):
#                 temp_img = invert_channels(current_image, params, show_image=False)
#             else:
#                 temp_img = invert_channels_from_image(current_image, params)
#
#             if temp_img:
#                 current_image = temp_img
#                 effects_applied.append(f"invert({','.join(params)})")
#
#         elif effect_type == 'floor':
#             channel, value_str = params
#             try:
#                 value = int(value_str)
#                 channel_limits = {channel.lower(): {'floor': value}}
#
#                 if isinstance(current_image, str):
#                     temp_img = clamp_channels(current_image, channel_limits, show_image=False)
#                 else:
#                     temp_img = clamp_channels_from_image(current_image, channel_limits)
#
#                 if temp_img:
#                     current_image = temp_img
#                     effects_applied.append(f"floor({channel}={value})")
#             except ValueError:
#                 print(f"Error: Invalid floor value '{value_str}'")
#                 continue
#
#         elif effect_type == 'ceiling':
#             channel, value_str = params
#             try:
#                 value = int(value_str)
#                 channel_limits = {channel.lower(): {'ceiling': value}}
#
#                 if isinstance(current_image, str):
#                     temp_img = clamp_channels(current_image, channel_limits, show_image=False)
#                 else:
#                     temp_img = clamp_channels_from_image(current_image, channel_limits)
#
#                 if temp_img:
#                     current_image = temp_img
#                     effects_applied.append(f"ceiling({channel}={value})")
#             except ValueError:
#                 print(f"Error: Invalid ceiling value '{value_str}'")
#                 continue
#
#         elif effect_type == 'conditional':
#             src_channel, operator, threshold_str, tgt_channel, set_value_str = params
#             try:
#                 threshold_value = int(threshold_str)
#                 set_value = int(set_value_str)
#                 conditional_rules = [{
#                     'source_channel': src_channel.lower(),
#                     'operator': operator,
#                     'threshold': threshold_value,
#                     'target_channel': tgt_channel.lower(),
#                     'set_value': set_value
#                 }]
#
#                 if isinstance(current_image, str):
#                     temp_img = conditional_channels(current_image, conditional_rules, show_image=False)
#                 else:
#                     temp_img = conditional_channels_from_image(current_image, conditional_rules)
#
#                 if temp_img:
#                     current_image = temp_img
#                     effects_applied.append(f"if({src_channel} {operator} {threshold_value} → {tgt_channel}={set_value})")
#             except ValueError:
#                 print(f"Error: Invalid threshold or set value in conditional rule")
#                 continue
#
#         elif effect_type == 'round':
#             channels, round_to = params
#
#             if isinstance(current_image, str):
#                 temp_img = round_channels(current_image, channels, round_to)
#             else:
#                 temp_img = round_channels_to_image(current_image, channels, round_to)
#
#             if temp_img:
#                 current_image = temp_img
#                 effects_applied.append(f"round({','.join(channels)}, {round_to})")
#
#         elif effect_type == 'swap':
#             ch1, ch2 = params
#
#             if isinstance(current_image, str):
#                 temp_img = swap_channels(current_image, ch1, ch2, show_image=False)
#             else:
#                 temp_img = swap_channels_from_image(current_image, ch1, ch2)
#
#             if temp_img:
#                 current_image = temp_img
#                 effects_applied.append(f"swap({ch1}↔{ch2})")
#
#         elif effect_type == 'remap':
#             remap_data = params
#
#             if isinstance(current_image, str):
#                 temp_img = create_channel_permutation(current_image,
#                     remap_data['r'], remap_data['g'], remap_data['b'], show_image=False)
#             else:
#                 temp_img = create_channel_permutation_from_image(current_image,
#                     remap_data['r'], remap_data['g'], remap_data['b'])
#
#             if temp_img:
#                 current_image = temp_img
#                 effects_applied.append(f"remap(R←{remap_data['r'].upper()},G←{remap_data['g'].upper()},B←{remap_data['b'].upper()})")
#
#         elif effect_type == 'drift':
#             intensity, direction, reverse = params
#
#             if isinstance(current_image, str):
#                 temp_img = pixel_drift(current_image, intensity, direction, reverse, show_image=False)
#             else:
#                 temp_img = pixel_drift_from_image(current_image, intensity, direction, reverse)
#
#             if temp_img:
#                 current_image = temp_img
#                 reverse_str = ",rev" if reverse else ""
#                 effects_applied.append(f"drift({intensity},{direction}{reverse_str})")
#
#     # If no effects were applied, use default swap
#     if not effects_applied and not arg_positions:
#         temp_img = swap_channels(current_image, args.swap[0], args.swap[1], show_image=False)
#         if temp_img:
#             current_image = temp_img
#             effects_applied.append(f"swap({args.swap[0]}↔{args.swap[1]})")
#
#     # Show final result
#     if isinstance(current_image, str):
#         print("No effects were applied.")
#     else:
#         current_image.show()
#         print(f"Applied effects in order: {' → '.join(effects_applied)}")
#
#     if not current_image:
#         print("Failed to process image.")
#         sys.exit(1)
#
# if __name__ == "__main__":
#     main()
