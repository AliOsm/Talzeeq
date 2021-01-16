# First-party package imports.
from frameworks.Keras.dense_layer import DenseLayer
from frameworks.Keras.input_layer import InputLayer


keras_layers = [
	InputLayer,
	DenseLayer,
]

layers_registry = {
	'Keras': keras_layers,
}
