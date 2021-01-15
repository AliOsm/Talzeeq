# Built-in imports.
import os

from typing import List

# First-party package imports.
from frameworks.layers_registry import layers_registry
from frameworks.layer_interface import LayerInterface


def get_frameworks_list() -> List[str]:
    return layers_registry.keys()


def get_sorted_frameworks_list() -> List[str]:
    return sorted(layers_registry.keys())


def get_framework_layers(framework_name: str) -> List[LayerInterface]:
	return layers_registry[framework_name]


def get_framework_layer_index(framework_name: str, layer_class: LayerInterface) -> int:
	return get_framework_layers(framework_name).index(layer_class)


def get_framework_template(framework_name: str) -> str:
	return open(os.path.join('./src/frameworks', framework_name, 'template.py'), 'r').read()


def get_formatted_framework_template(framework_name: str, layer_definitions: str, model_connections: str) -> str:
    return get_framework_template(framework_name).format(layer_definitions, model_connections)
