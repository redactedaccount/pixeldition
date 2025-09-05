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
pixeldition image.jpg --swap r b --channel-invert g

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

        # Build pipeline from arguments in CLI order by parsing raw args
        transforms = []

        # Create mappings for transformers and their flags
        flag_to_transformer = {}
        transformer_instances = {}

        for name, transformer_class in self.registry.list_all().items():
            transformer = transformer_class()
            transformer_instances[name] = transformer
            cli_args = transformer.get_cli_args()

            for arg_config in cli_args:
                flags = arg_config.get('flags', [])
                for flag in flags:
                    flag_to_transformer[flag] = name

        # Process raw arguments in order to preserve sequence and handle multiple instances
        raw_args = args.copy()

        # Remove the input file from consideration
        if raw_args and not raw_args[0].startswith('-'):
            raw_args.pop(0)

        i = 0
        while i < len(raw_args):
            arg = raw_args[i]

            if arg in flag_to_transformer:
                transformer_name = flag_to_transformer[arg]
                transformer = transformer_instances[transformer_name]
                temp_args = argparse.Namespace()
                transformer_cli_args = transformer.get_cli_args()
                current_arg_config = None

                for arg_config in transformer_cli_args:
                    if arg in arg_config.get('flags', []):
                        current_arg_config = arg_config
                        break

                if current_arg_config:
                    nargs = current_arg_config.get('nargs', 0)
                    attr_name = arg.lstrip('-').replace('-', '_')

                    if nargs == '+':
                        values = []
                        j = i + 1
                        while j < len(raw_args) and not raw_args[j].startswith('-'):
                            values.append(raw_args[j])
                            j += 1
                        setattr(temp_args, attr_name, values)
                        i = j - 1

                    elif nargs == 2:
                        if i + 2 < len(raw_args):
                            values = [raw_args[i + 1], raw_args[i + 2]]
                            setattr(temp_args, attr_name, values)
                            i += 2
                        else:
                            i += 1
                            continue

                    elif isinstance(nargs, int) and nargs == 1:
                        # Single argument
                        if i + 1 < len(raw_args):
                            setattr(temp_args, attr_name, raw_args[i + 1])
                            i += 1
                        else:
                            i += 1
                            continue
                    else:
                        # Flag without arguments
                        setattr(temp_args, attr_name, True)

                for attr_name, attr_value in vars(parsed_args).items():
                    if not hasattr(temp_args, attr_name):
                        setattr(temp_args, attr_name, attr_value)

                params = transformer.parse_cli_args(temp_args)

                if params:
                    transforms.append((transformer_name, params))

            i += 1

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
        except SystemExit:
            return

        # Check if input file exists
        input_path = Path(parsed_args.input)
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist")
            sys.exit(1)

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
