import importlib
import pkgutil
from pathlib import Path
import pixeldition.transformers

def load_transformers():

    package_path = Path(pixeldition.transformers.__path__[0])

    for importer, modname, ispkg in pkgutil.iter_modules([str(package_path)]):
        if not modname.startswith('_'): # skip private modules
            full_modname = f"pixeldition.transformers.{modname}"
            try:
                importlib.import_module(full_modname)
            except Exception as e:
                print(f"  ✗ Failed to load {modname}: {e}")