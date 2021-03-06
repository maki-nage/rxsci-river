import rx

def preprocess(processor):
    """Pre-processes data

    Source:
        An observable emitting Utterance items.

    Args:
        processor: A river preprocessor

    Returns:
        An Observable emitting preprocessed items for each input item.
    """
    def _preprocess(source):
        def on_subscribe(observer, scheduler):
            def on_next(i):
                processor.learn_one(i.data)
                result = processor.transform_one(i.data)
                observer.on_next(result)

            return source.subscribe(
                on_next=on_next,
                on_error=observer.on_error,
                on_completed=observer.on_completed,
                scheduler=scheduler,
            )

        return rx.create(on_subscribe)

    return _preprocess
