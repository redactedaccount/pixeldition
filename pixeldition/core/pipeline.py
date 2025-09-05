from typing import List, Tuple, Any
from PIL import Image
from pixeldition.core.registry import TransformRegistry

class TransformPipeline:
    """Manages a pipeline of transforms"""

    def __init__(self):
        self.steps: List[Tuple[str,dict]] = []
        self.history: List[Image.Image] = []

    def add_step(self, transformer_name: str, params: dict):
        """Add a transformation step to the pipeline"""
        self.steps.append((transformer_name, params))

    def execute(self, image:Image.Image, save_history: bool = False)-> Image.Image:
        """Execute the pipeline on an image"""
        current = image

        if save_history:
            self.history.append(current.copy())

        for transformer_name, params in self.steps:
            transformer = TransformRegistry.create(transformer_name)
            current = transformer.transform(current, **params)

            if save_history:
                self.history.append(current.copy())

        return current

    def clear(self):
        """Clear the pipeline"""
        self.steps = []
        self.history = []

    def __repr__(self):
        steps_str = " -> ".join([name for name, _ in self.steps])
        return f"Pipeline({steps_str}"
