import rx

def compute_metric(metric):
    def _metric(source):
        def on_subscribe(observer, scheduler):
            def on_next(i):
                result = metric.update(i.utterance.label, i.prediction)
                observer.on_next(result)

            return source.subscribe(
                on_next=on_next,
                on_error=observer.on_error,
                on_completed=observer.on_completed,
                scheduler=scheduler,
            )

        return rx.create(on_subscribe)

    return _metric
