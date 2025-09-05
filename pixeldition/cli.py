"""Main CLI interface for pixeldition"""

import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Any
from PIL import Image

from pixeldition.core.registry import TransformRegistry
from pixeldition.core.pipeline import TransformPipeline


class PixelditionCLI:
    """Command-line interface for pixeldition"""

    def __init__(self):
        self.registry = TransformRegistry
        self.pipeline = TransformPipeline()

    def build_parser(self) -> argparse.ArgumentParser:
        """Build the argument parser dynamically from registered transformers"""

        parser = argparse.ArgumentParser(
            prog='pixeldition',
            description='Apply artistic transformations to images',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_examples()
        )

        # Required arguments
        parser.add_argument(
            'input',
            type=str,
            help='Path to input image file',
            nargs="?"
        )

        # Optional arguments
        parser.add_argument(
            '-o', '--output',
            type=str,
            help='Filepath to output image file (default: displays image)'
        )

        parser.add_argument(
            '--save-intermediate-images',
            action='store_true',
            help='Save intermediate images between steps in the pipeline'
        )

        parser.add_argument(
            '--list-transformers',
            action='store_true',
            help='List all available transformers'
        )

        parser.add_argument(
            '--no-display',
            action='store_true',
            help='Do not display the image (useful for scripts)'
        )

        # Add arguments for each registered transformer
        transformers = self.registry.list_all()

        for name, transformer_class in transformers.items():
            transformer = transformer_class()
            cli_args = transformer.get_cli_args()

            # Create a group for each transformer
            group = parser.add_argument_group(
                f'{name} transformer',
                transformer.description
            )

            for arg_config in cli_args:
                flags = arg_config.pop('flags', [])
                group.add_argument(*flags, **arg_config)

        return parser

    def _get_examples(self) -> str:
        """Get usage examples"""
        examples_string = """EXAMPLES:
# Chain multiple transformations
pixeldition image.jpg --swap r b --channel-invert g --drift 50

# Save without displaying
pixeldition image.jpg --channel-swap g b -o result.jpg --no-display

# Save images between steps in pipeline
pixeldition image.jpg --channel-swap r g --channel-invert b --save-intermediate-images -o final.jpg

# List all available transformers
pixeldition --list-transformers
"""
        for name, transformer in self.registry._transformers.items():
            examples_string += transformer.usage_example
            examples_string += "\n"

        return examples_string



    def parse_arguments(self, args: List[str]) -> Tuple[argparse.Namespace, List[Tuple[str, dict]]]:
        """Parse CLI arguments and build transformation pipeline"""

        parser = self.build_parser()
        parsed_args = parser.parse_args(args)

        # Handle special cases
        if parsed_args.list_transformers:
            self.list_transformers()
            sys.exit(0)

        if not parsed_args.input:
            parser.error("Input image is required")

        # Build pipeline from arguments
        transforms = []

        # Check each transformer to see if its arguments were provided
        print(self.registry.list_all().items())
        for name, transformer_class in self.registry.list_all().items():

            transformer = transformer_class()
            params = transformer.parse_cli_args(parsed_args)

            if params:  # If this transformer has arguments set
                transforms.append((name, params))

        return parsed_args, transforms

    def list_transformers(self):

        print("\nAvailable Transformers:")
        print("=" * 50)

        transformers = self.registry.list_all()
        for name, transformer_class in transformers.items():
            transformer = transformer_class()
            print(f"\n{name}:")
            print(f"  {transformer.description}")

            cli_args = transformer.get_cli_args()
            if cli_args:
                print("  Usage:")
                for arg_config in cli_args:
                    flags = arg_config.get('flags', [])
                    help_text = arg_config.get('help', '')
                    if flags:
                        print(f"    {' '.join(flags)}: {help_text}")

    def run(self, args: List[str] = None):
        """Entrypoint"""

        if args is None:
            args = sys.argv[1:]

        # Parse arguments
        try:
            parsed_args, transforms = self.parse_arguments(args)
            print('parsed_args')
            print(parsed_args)
            print(args)


        except SystemExit:
            return

        # Check if input file exists
        input_path = Path(parsed_args.input)
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist")
            sys.exit(1)

        # Load image
        try:
            image = Image.open(input_path)
            print(f"Loaded image: {input_path} ({image.size[0]}x{image.size[1]}, {image.mode})")
        except Exception as e:
            print(f"Error loading image: {e}")
            sys.exit(1)

        # Build and execute pipeline
        if transforms:
            print(f"\nApplying transformations:")
            for name, params in transforms:
                print(f"  • {name}: {params}")
                self.pipeline.add_step(name, params)

            try:
                result = self.pipeline.execute(
                    image,
                    save_history=parsed_args.save_intermediate_images
                )
            except Exception as e:
                print(f"Error during transformation: {e}")
                sys.exit(1)
        else:
            print("No transformations specified, using original image")
            result = image

        # save intermediate images
        if parsed_args.save_intermediate_images and self.pipeline.history:
            output_path = Path(parsed_args.output) if parsed_args.output else Path("output.jpg")
            base_name = output_path.stem
            extension = output_path.suffix

            for i, step_image in enumerate(self.pipeline.history[:-1]):  # Exclude final
                step_path = output_path.parent / f"{base_name}_step{i}{extension}"
                step_image.save(step_path)
                print(f"Saved step {i}: {step_path}")

        # Save or display result
        if parsed_args.output:
            output_path = Path(parsed_args.output)
            result.save(output_path)
            print(f"\nSaved result to: {output_path}")

        if not parsed_args.no_display:
            result.show()
            print("\nDisplaying result...")
