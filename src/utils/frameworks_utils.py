# Built-in imports.
import os

from typing import List

# First-party package imports.
from frameworks.layers_registry import layers_registry
from frameworks.layer_interface import LayerInterface


def get_frameworks_list() -> List[str]:
    """Returns list of the available frameworks.

    Returns:
        List of strings represents the names of the available frameworks.
    """

    return layers_registry.keys()


def get_sorted_frameworks_list() -> List[str]:
    """Returns sorted list of the available frameworks.

    Returns:
        Sorted list of strings represents the names of the available frameworks.
    """

    return sorted(get_frameworks_list())


def get_framework_layers(framework_name: str) -> List[LayerInterface]:
    """Returns a list of available layers for the given framework.

    Args:
        framework_name: String represents the name of the framework.

    Returns:
        List of layers for the given framework.
    """

    return layers_registry[framework_name]


def get_framework_layer_index(framework_name: str, layer_class: LayerInterface) -> int:
    """Returns the index of the given layer in the framework's layers list.

    Args:
        framework_name: String represents the name of the framework.
        layer_class: The required layer class.

    Returns:
        Integer represents the index of the layer in the framework's layers list.
    """

    return get_framework_layers(framework_name).index(layer_class)


def get_framework_template(framework_name: str) -> str:
    """Reads the framework's template.

    Args:
        framework_name: String represents the name of the framework.

    Returns:
        The framework's template.
    """

    return open(os.path.join('./src/frameworks', framework_name, 'template.py'), 'r').read()


def get_formatted_framework_template(framework_name: str, layer_definitions: str, model_connections: str) -> str:
    """Formats the framework's template after reading it using the given layer definitions and model connections.

    Args:
        framework_name: String represents the name of the framework.
        layer_definitions: String of the layer definitions.
        model_connections: String of the model connections.

    Returns:
        String represents the formatted framework's template.
    """

    return get_framework_template(framework_name).format(layer_definitions, model_connections)
