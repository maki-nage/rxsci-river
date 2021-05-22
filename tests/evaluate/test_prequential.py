import rx
import rx.operators as ops
import rxsci_river as rsr
from river.anomaly import HalfSpaceTrees
from river.tree import HoeffdingTreeClassifier
from river import synth


def test_prequential_hs_tree():
    actual_result = []

    source = [0.5, 0.45, 0.43, 0.44, 0.445, 0.45, 0.0]
    rx.from_(source).pipe(
        ops.map(lambda i: rsr.Utterance(i)),
        rsr.evaluate.prequential(
            model=HalfSpaceTrees(
                n_trees=5,
                height=3,
                window_size=3,
                seed=42
            ),
            pretrain_size=3),
    ).subscribe(
        on_next=actual_result.append,
        on_error=print,
    )
    
    anomaly_count = 0
    assert len(actual_result) == 4
    for p in actual_result:
        if p.prediction > 0.8:
            anomaly_count += 1
    
    assert anomaly_count == 1


def test_prequential_hoeffding_tree():
    actual_result = []

    gen = synth.Agrawal(classification_function=0, seed=42)

    rx.from_(gen.take(1000)).pipe(
        ops.map(lambda i: rsr.Utterance(i[0], i[1])),
        rsr.evaluate.prequential(
            model=HoeffdingTreeClassifier(
                grace_period=100,
                split_confidence=1e-5,
                nominal_attributes=['elevel', 'car', 'zipcode'],
            ),
            pretrain_size=100),
    ).subscribe(
        on_next=actual_result.append,
        on_error=print,
    )
    
    pred0_count = 0
    pred1_count = 0
    for p in actual_result:
        if p.prediction == 1:
            pred1_count += 1
        if p.prediction == 0:
            pred0_count += 1
    assert len(actual_result) == 900
    assert pred0_count >= 190 and pred0_count < 210
