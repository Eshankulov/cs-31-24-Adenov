# CPU Scheduling — Variant B

## Goal
Implement CPU scheduling algorithms, compare performance metrics, study Round Robin quantum sizes, and demonstrate priority aging.

## Algorithms
- FCFS (First Come, First Served)
- SJF (Shortest Job First)
- SRTF (Shortest Remaining Time First)
- Preemptive Priority Scheduling
- Round Robin with configurable quantum
- Priority Scheduling with Aging

## Metrics
- Average Waiting Time
- Average Turnaround Time
- Average Response Time
- CPU Utilization
- Context Switches

Context switches count transitions between two different running processes. Transitions to or from `IDLE` are excluded.

## Experiments
1. Compare FCFS, SJF, SRTF, Priority, and Round Robin on `set1`.
2. Compare Round Robin quanta from 1 through 10 on `set2`.
3. Plot average waiting time and context switches against the quantum.
4. Compare SRTF and RR (`q = 3`).
5. Compare priority scheduling with and without Aging.

## Run
1. Open the notebook in Google Colab using the badge in its first cell.
2. Select **Runtime → Run all**.
3. Confirm that all cells run successfully and the charts appear.
4. Re-run all cells after any code changes so the saved outputs are current.

## Expected interpretation
A smaller Round Robin quantum generally causes more process switches and can improve responsiveness. A larger quantum usually reduces switching overhead but can increase waiting for some processes. Aging improves fairness by increasing the effective priority of processes that have waited for a long time.

> Note: Saved outputs for the affected Round Robin experiment and metric-comparison cells were cleared after correcting the function. Run the entire notebook before submission so all tables and charts reflect the updated code.
