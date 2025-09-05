from typing import Dict, Type, Optional
from pixeldition.core.base import ImageTransformer

class TransformRegistry:
    """Registry for image transformers"""
    _transformers: Dict[str,Type[ImageTransformer]] = {}

    @classmethod
    def register(cls, name:str, transformer_class: Type[ImageTransformer]):
        """Register a transformer"""
        if name in cls._transformers:
            raise ValueError(f"Transformer '{name}' already registered.")
        cls._transformers[name] = transformer_class

    @classmethod
    def get(cls, name: str) -> Optional[Type[ImageTransformer]]:
        """Get transformer by name"""
        return cls._transformers.get(name)

    @classmethod
    def list_all(cls) -> Dict[str, Type[ImageTransformer]]:
        """List all registered transformers"""
        return cls._transformers.copy()

    @classmethod
    def create(cls, name:str, **kwargs) -> ImageTransformer:
        """Create transformer instance"""
        transformer_class = cls.get(name)
        if not transformer_class:
            raise ValueError(f"Unknown Transformer: '{name}'")
        return transformer_class(**kwargs)
