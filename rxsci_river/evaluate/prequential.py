import rx
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
    if isinstance(model, base.Classifier):
       predict = model.predict_one
    elif isinstance(model, base.AnomalyDetector):
        predict = model.score_one 
    else:
        raise NotImplementedError("prequential not implemented for model {}, contributions are welcome!".format(type(model)))

    def _learn_one(i):
        if type(i) is tuple:
            model.learn_one(i[0], i[1])
        elif type(i) is dict:
            if 'y' in i:
                model.learn_one({'x': i['x'], 'y': i['y']})
            else:
                model.learn_one({'x': i['x']})
        else:
            model.learn_one({'x': i})

    def _predict(i):
        if type(i) is tuple:
            return predict(i[0])
        elif type(i) is dict:
            return predict({'x': i['x']})
        else:
            return predict({'x': i})

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
                    observer.on_next(predict)

            return source.subscribe(
                on_next=on_next,
                on_error=observer.on_error,
                on_completed=observer.on_completed,
                scheduler=scheduler,
            )
        return rx.create(on_subscribe)

    return _prequential
