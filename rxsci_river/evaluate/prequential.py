import rx

from rxsci_river.base import Utterance, Prediction


def prequential(model, pretrain_size=200):
    """Prequential predict/train evaluation of a model

    The source items may or may not have associated labels. If a label is
    present, then the item is used for training. Otherwise only inference is done.
    
    Source: 
        An observable emitting Utterance items.

    Args:
        model: A river model object
        pretrain_size: [Optional] number of initial items used to train the
        model before doing predictions.

    Returns:
        An Observable emitting Prediction items for each input item. The
        firsts pretrain_size items do not emit predictions.
    """
    def _prequential(source):
        def on_subscribe(observer, scheduler):
            pretrain = pretrain_size

            def on_next(i):
                nonlocal pretrain
                if pretrain > 0:
                    if i.label is not None:
                        model.learn_one(i.data, i.label)
                        pretrain -= 1
                else:
                    predict = model.predict_one(i.data)
                    if i.label is not None:
                        model.learn_one(i.data, i.label)
                    observer.on_next(Prediction(i, predict))

            return source.subscribe(
                on_next=on_next,
                on_error=observer.on_error,
                on_completed=observer.on_completed,
                scheduler=scheduler,
            )
        return rx.create(on_subscribe)

    return _prequential
