import rx
import rxsci_river as rsr
from river.drift import ADWIN
import random


def test_concept_drift_adwin():
    actual_result = []
    random.seed(42)
    source = [random.normalvariate(0.8, 0.05) for _ in range(1000)]
    source.extend([random.normalvariate(0.4, 0.02) for _ in range(1000)])
    source.extend([random.normalvariate(0.6, 0.1) for _ in range(1000)])
        
    rx.from_(source).pipe(
        rsr.detect_concept_drift(ADWIN())
    ).subscribe(
        on_next=actual_result.append,
        on_error=print,
    )

    changes = []
    for index, value in enumerate(actual_result):
        if value == rsr.DriftStatus.CHANGE:
            changes.append(index)

    assert len(changes) == 2
    assert changes[0] > 1000 and changes[0] < 1100
    assert changes[1] > 2000 and changes[1] < 2100
