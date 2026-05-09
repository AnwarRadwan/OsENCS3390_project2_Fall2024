# OS CPU Scheduling & Resource Management Simulator

A comprehensive Python-based simulation of an Operating System's CPU scheduler and resource manager. This project simulates process execution, I/O handling, resource allocation, and deadlock detection/recovery using a Priority-based scheduling algorithm with Round-Robin characteristics.

## 🚀 Features

- **Multi-Queue Simulation**: Implements Ready, Wait (Resource), and I/O queues.
- **Dynamic Scheduling**: Priority-based scheduling with internal logic for handling Round-Robin slices.
- **Resource Management**: Processes can request (`R[n]`) and release (`F[n]`) shared resources dynamically during CPU bursts.
- **Deadlock Handling**:
    - **Detection**: Uses a Resource Allocation Graph (RAG) to identify cycles and potential deadlocks.
    - **Recovery**: Implements a recovery mechanism to resolve deadlocks by preempting/restarting high-priority processes.
- **I/O Operations**: Simulates non-blocking I/O bursts where multiple processes can perform I/O simultaneously.
- **Performance Analysis**:
    - Generates a detailed **Gantt Chart**.
    - Calculates **Average Waiting Time**.
    - Calculates **Average Turnaround Time**.

## 📂 Project Structure

- `code.py`: The main simulation engine.
- `test.txt`: Input file containing process definitions.
- `README.md`: This documentation.

## 🛠️ Input File Format (`test.txt`)

The simulator reads process information from `test.txt`. Each line represents a process with the following structure:

```text
[PID] [Arrival] [Priority] [CPU Burst/Resource Commands] [IO Burst] [CPU Burst/Resource Commands] ...
```

### Examples:
- `1 0 1 CPU{5} IO{8} CPU{5}`: PID 1, arrives at time 0, priority 1. Executes 5 units of CPU, then 8 units of IO, then 5 units of CPU.
- `2 3 5 CPU{R[2],6,F[2]}`: PID 2, arrives at time 3, priority 5. Requests resource 2, runs for 6 units, then frees resource 2.

### Resource Commands:
- `R[n]`: Request resource number `n`.
- `F[n]`: Free resource number `n`.

## ⚙️ How to Run

1. Ensure you have Python 3.x installed.
2. Prepare your test cases in `test.txt`.
3. Run the script:
   ```bash
   python code.py
   ```

## 📊 Output

The script outputs the following metrics to the console:
1. **Process Stats**: `[PID, Wait_time, IO_time, Ready_time]`
2. **Gantt Chart**: Visual representation of CPU occupancy over time.
3. **Average Waiting Time**: Total ready time divided by number of processes.
4. **Average Turnaround Time**: Total time from arrival to completion.

## 👤 Author
**Ibraheem Sleet**
Student ID: 1220200
ENCS3390 - Operating Systems Project
