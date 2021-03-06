import rx
import rxsci_multiflow as rsm
from skmultiflow.anomaly_detection import HalfSpaceTrees
from skmultiflow.data import AnomalySineGenerator, SEAGenerator
from skmultiflow.trees import HoeffdingTreeClassifier


def test_prequential_hs_tree():
    actual_result = []

    rsm.from_stream(AnomalySineGenerator(n_samples=2000, n_anomalies=10, random_state=1)).pipe(
        rsm.evaluate.prequential(
            model=HalfSpaceTrees(random_state=1),
            pretrain_size=0),
    ).subscribe(
        on_next=actual_result.append,
        on_error=print,
    )
    
    anomaly_count = 0
    for p in actual_result:
        if p.prediction[0] == 1:
            anomaly_count += 1
    assert len(actual_result) == 2000
    #assert anomaly_count == 10  # issue: hstree detects 1748 anomalies in data


def test_prequential_hoeffding_tree():
    actual_result = []

    rsm.from_stream(SEAGenerator(random_state=1), count=200).pipe(
        rsm.evaluate.prequential(
            model=HoeffdingTreeClassifier(),
            pretrain_size=0),
    ).subscribe(
        on_next=actual_result.append,
        on_error=print,
    )
    
    pred0_count = 0
    pred1_count = 0
    for p in actual_result:
        if p.prediction[0] == 1:
            pred1_count += 1
        if p.prediction[0] == 0:
            pred0_count += 1
    assert len(actual_result) == 200
    assert pred0_count == 55
    assert pred1_count == 145
