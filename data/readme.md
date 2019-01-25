Quantum Computing Metrics
=========================

This directory contains an analytics program to produce timing metrics for running a quantum computing program on a QisKit simulator versus IBM Q Experience.

The metrics include:

```text
machine name
minimum seconds
mean seconds
maximum seconds
```

Machines include ibmqx4, ibmq_16_melbourne, and the QisKit simulator.

## Results

```text
               type runs   min        mean    max
1         simulator  175  0.06   0.1300571   0.25
2            ibmqx4   94 53.81  58.2200000  90.23
3 ibmq_16_melbourne   33 59.87 141.4306061 627.30
4  IBM Q Experience  127 53.81  79.8416535 627.30
```

![Mean Quantum Computing Execution Times in seconds](metrics.png)

## Conclusion

The results record significant wait times for programs executed on IBM Q Experience versus the simulator.

## Author

Kory Becker, 2019
http://primaryobjects.com