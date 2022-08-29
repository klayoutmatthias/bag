
from ..klayout import KLayoutLayoutGenerator
from .layout_generator import LayoutGenerator

def make_layout_generator(name: str, config: dict) -> LayoutGenerator:
    """
    Parameters
    ----------
    name : str
        The generator name
    config : dict
        The configuration file's content
    Returns
    -------
    """
    # TODO: add more generators ...
    if name == "klayout" or name == None:
        return KLayoutLayoutGenerator.make_generator(config)
    else:
        raise Exception(f"Unknown layout driver {name}")

