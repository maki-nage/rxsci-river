from collections import namedtuple

Utterance = namedtuple('Utterance', ['data', 'label', 'target_values'])
Utterance.__new__.__defaults__ = (None, None)
Utterance.__doc__ = "An Utterance value"
Utterance.data.__doc__ = "The actual data of the utterance"
Utterance.label.__doc__ = "[Optional] The label of the utterance"
Utterance.target_values.__doc__ = "[Optional] The list of possible target values"

Prediction = namedtuple('Prediction', ['utterance', 'prediction'])
Prediction.__doc__ = "The prediction of an utterance"
Prediction.utterance.__doc__ = "The utterance associated to the prediction"
Prediction.prediction.__doc__ = "The actual prediction value"
