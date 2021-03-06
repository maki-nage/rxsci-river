import rx

from enum import Enum

DriftStatus = Enum('DriftStatus', 'NO_CHANGE CHANGE')


def detect_concept_drift(model):
    """Concept drift detection.

    Source:
        An Observable of integer or real values.

    Args:
        method: A river drift detection object.

    Returns:
        An observable emitting DrifStatus items.
    """
    def _detect_concept_drift(source):
        def on_subscribe(observer, scheduler):
            def on_next(i):
                model.update(i)
                status = DriftStatus.NO_CHANGE
                if model.change_detected:
                    status = DriftStatus.CHANGE
                    model.reset()                    
                observer.on_next(status)

            return source.subscribe(
                on_next=on_next,
                on_error=observer.on_error,
                on_completed=observer.on_completed,
            )

        return rx.create(on_subscribe)

    return _detect_concept_drift
