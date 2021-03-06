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

    expected_result = [rsr.DriftStatus.NO_CHANGE for _ in range(3000)]
    expected_result[1055] = rsr.DriftStatus.CHANGE
    expected_result[2079] = rsr.DriftStatus.CHANGE

    rx.from_(source).pipe(
        rsr.detect_concept_drift(ADWIN())
    ).subscribe(
        on_next=actual_result.append,
        on_error=print,
    )

    assert actual_result == expected_result
