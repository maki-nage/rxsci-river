=======================
RxSci-River
=======================

.. image:: https://badge.fury.io/py/rxsci-river.svg
    :target: https://badge.fury.io/py/rxsci-river

.. image:: https://github.com/maki-nage/rxsci-river/workflows/Python%20package/badge.svg
    :target: https://github.com/maki-nage/rxsci-river/actions?query=workflow%3A%22Python+package%22
    :alt: Github WorkFlows

.. image:: https://github.com/maki-nage/rxsci-river/raw/master/asset/docs_read.svg
    :target: https://www.makinage.org/doc/rxsci-river/latest/index.html
    :alt: Documentation


RxSci operators for Scikit River.

Get Started
============

Evaluate and train a Hoeffding Tree Classifier from a stream of events:

.. code:: Python

    import rx
    import rxsci_river as rsr
    from river import synth
    from river.tree import HoeffdingTreeClassifier

    gen = synth.Agrawal(classification_function=0, seed=42)
    rx.from_(gen.take(1000)).pipe(
        rsr.evaluate.prequential(
            model=HoeffdingTreeClassifier(
                grace_period=100,
                split_confidence=1e-5,
                nominal_attributes=['elevel', 'car', 'zipcode'],
            ),
            pretrain_size=100),
    ).subscribe(
        on_next=print,
    )


See the
`Maki Nage documentation <https://www.makinage.org/doc/makinage-book/latest/index.html>`_
for more information.

Installation
=============

RxSci River is available on PyPi and can be installed with pip:

.. code:: console

    python3 -m pip install rxsci-river
