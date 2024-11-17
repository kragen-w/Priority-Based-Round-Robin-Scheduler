Here’s the README in plain text format, ready for pasting:

---

# Job Scheduler Simulator

Welcome to the **Job Scheduler Simulator**, a Python project designed to simulate scheduling algorithms for jobs. This simulator allows users to define job sequences and experiment with various scheduling strategies, providing insights into how these algorithms handle time slices and block durations. 

## Features

- **Flexible Job Simulation:** Input jobs with customizable parameters (arrival time, CPU bursts, block events, etc.).
- **Adjustable Scheduler Parameters:** Define `time_slice` and `block_duration` to simulate Round-Robin scheduling and blocking behavior.
- **Realistic Output:** Observe detailed logs for job execution, completion, and waiting times.

---

## Getting Started

Follow these steps to set up and use the Job Scheduler Simulator.

### Prerequisites

- **Python 3.7+**
- **Required libraries**: Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

### Running the Simulator

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/job-scheduler-simulator.git
   cd job-scheduler-simulator
   ```

2. Run the program:
   ```bash
   python scheduler.py <job_file> <time_slice> <block_duration>
   ```
   - Replace `<job_file>` with the path to your job file (e.g., `jobs.txt`).
   - Replace `<time_slice>` with the maximum time a job can run before switching (e.g., `3`).
   - Replace `<block_duration>` with the time a job is blocked (e.g., `2`).

Example:
```bash
python scheduler.py jobs.txt 3 2
```

---

## Job File Format

The **job file** contains a list of jobs, each defined by specific parameters. Use the following format for each line in the file:

```
<name> <priority> <arrival_time> <total_time> <block_interval>
```

- **`name`**: The name of the job (string, e.g., `A`).
- **`priority`**: The priority level of the job (integer, optional depending on the algorithm).
- **`arrival_time`**: The time the job arrives in the queue (integer, e.g., `0`).
- **`total_time`**: The total CPU time required for the job (integer, e.g., `8`).
- **`block_interval`**: The time when the job will block (integer, e.g., `4` or `8 (same as total_time)` if no blocking).

### Example Job File (`jobs.txt`)

```txt
A 1 0 100 25
B 5 1 50 20
C 2 2 90 45
```

Explanation:
1. Job `A` has priority `1`, arrives at time `0`, requires `100` units of CPU time, blocks after running for `25`.
2. Job `B` has priority `5`, arrives at time `1`, requires `50` units of CPU time, blocks after running for `20`.
3. Job `C` has priority `2`, arrives at time `2`, requires `90` units of CPU time, blocks after running for `45`.

---

## Output

The simulator outputs the following information:

- Job execution timeline.
- Waiting and turnaround times for each job.
- Scheduler statistics (e.g., average waiting time, throughput).

---

## Contributing

We welcome contributions! If you'd like to improve this project:
1. Fork this repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

---

## Questions or Feedback?

Feel free to open an issue or contact me at `kragen.wild@du.edu`.

---
