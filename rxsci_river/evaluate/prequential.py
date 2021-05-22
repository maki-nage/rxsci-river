import rx
import rxsci_river as rsr
from river import base


def prequential(model, pretrain_size=200):
    """Prequential predict/train evaluation of a model

    The source items may or may not have associated labels. If a label is
    present, then the item is used for training. Otherwise only inference is done.
    
    Source: 
        An observable emitting tuples of (x, y) items.

    Args:
        model: A river model object
        pretrain_size: [Optional] number of initial items used to train the
        model before doing predictions.

    Returns:
        An Observable emitting prediction items for each input item. The
        firsts pretrain_size items do not emit predictions.
    """
    learn_dict = False
    if isinstance(model, base.Classifier):
       predict = model.predict_one
    elif isinstance(model, base.AnomalyDetector):
        predict = model.score_one 
        learn_dict = True
    else:
        raise NotImplementedError("prequential not implemented for model {}, contributions are welcome!".format(type(model)))

    def _learn_one(i):
        if learn_dict is False:
            model.learn_one(i.data, i.label)
        else:
            model.learn_one({'x': i.data})

    def _predict(i):
        if learn_dict is False:
            return predict(i.data)
        else:
            return predict({'x': i.data})

    def _prequential(source):
        def on_subscribe(observer, scheduler):
            pretrain = pretrain_size

            def on_next(i):                
                nonlocal pretrain
                if pretrain > 0:
                    _learn_one(i)
                    pretrain -= 1
                else:
                    predict = _predict(i)
                    _learn_one(i)
                    observer.on_next(rsr.Prediction(utterance=i, prediction=predict))

            return source.subscribe(
                on_next=on_next,
                on_error=observer.on_error,
                on_completed=observer.on_completed,
                scheduler=scheduler,
            )
        return rx.create(on_subscribe)

    return _prequential
