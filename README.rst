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

    import rxsci_river as rsm
    from river.data import SEAGenerator
    from river.trees import HoeffdingTreeClassifier

    rsm.from_stream(SEAGenerator(random_state=1), count=200).pipe(
        rsm.evaluate.prequential(
            model=HoeffdingTreeClassifier(),
            pretrain_size=0),
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
