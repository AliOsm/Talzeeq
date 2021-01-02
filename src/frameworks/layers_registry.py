# First-party package imports.
from frameworks.Keras.dense_layer import DenseLayer

keras_layers = [
	DenseLayer,
]

layers_registry = {
	'Keras': keras_layers,
}
