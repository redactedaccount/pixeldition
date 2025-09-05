from abc import ABC, abstractmethod, ABCMeta
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image
import inspect

class TransformerMeta(ABCMeta):
    """Metaclass that automatically registers transformers"""
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if not inspect.isabstract(cls) and issubclass(cls, ImageTransformer):
            # Auto-register non-abstract transformers
            from pixeldition.core.registry import TransformRegistry
            if hasattr(cls, 'name'):
                TransformRegistry.register(cls.name, cls)

class ImageTransformer(ABC, metaclass=TransformerMeta):
    """Base class for all image transformers"""

    name: str = None
    description: str = None
    usage_example: str = None

    @abstractmethod
    def transform(self, image, **params):
        pass

    @abstractmethod
    def get_cli_args(self, args) -> List[Dict[str, Any]]:
        """Return CLI argument definitions for argparse"""
        pass

    @abstractmethod
    def parse_cli_args(self, **params) -> bool:
        """Validate transform parameters"""
        return True

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"


