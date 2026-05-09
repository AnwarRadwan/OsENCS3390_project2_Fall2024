# 🖥️ OS CPU Scheduling & Resource Management Simulator

A high-fidelity Python simulation of an Operating System's kernel-level tasks, focusing on **CPU Scheduling**, **Dynamic Resource Allocation**, and **Deadlock Management**. This project demonstrates complex process synchronization and performance optimization using a hybrid Priority and Round-Robin scheduling approach.

---

## 🌟 Key Features

- **🎯 Hybrid Scheduling Algorithm**: 
  - Uses **Priority-based scheduling** as the primary logic.
  - Implements **Round-Robin (Quantum = 5)** for processes sharing the same priority level.
- **🏗️ Comprehensive Queue Management**: 
  - **Ready Queue**: Processes waiting for CPU.
  - **Wait Queue**: Processes blocked by resource unavailability.
  - **I/O Queue**: Processes performing non-blocking I/O operations.
- **🔐 Advanced Resource Management**: 
  - Dynamic request (`R[n]`) and release (`F[n]`) of shared resources during execution.
  - Real-time tracking of resource ownership.
- **🛡️ Deadlock Handling System**:
  - **Detection**: Implements a **Resource Allocation Graph (RAG)** to identify circular wait conditions.
  - **Recovery**: Automatic resolution of deadlocks by preempting/restarting high-priority processes involved in the cycle.
- **📊 Performance Analytics**:
  - Generates a text-based **Gantt Chart** for visual execution flow.
  - Calculates **Average Waiting Time** and **Average Turnaround Time**.

---

## 📁 Project Components

| File | Description |
| :--- | :--- |
| `code.py` | The core simulation engine containing the scheduler and RAG logic. |
| `test.txt` | Input configuration file defining processes, bursts, and resource requests. |
| `README.md` | Comprehensive documentation and usage guide. |

---

## 🛠️ Input Specification (`test.txt`)

The simulator processes a sequence of instructions defined in `test.txt`. Each line represents a unique process:

```text
[PID] [Arrival] [Priority] [CPU Burst/Resource Commands] [IO Burst] ...
```

### Resource Command Syntax:
- **`R[n]`**: Request resource number `n`.
- **`F[n]`**: Release resource number `n`.
- **`CPU{...}`**: Defines a CPU burst. Can contain nested resource commands.
- **`IO{n}`**: Defines an I/O burst of `n` time units.

### Example Input:
`5 12 2 CPU{10,R[1],5,R[2],8,F[2],3,F[1],4}`
> PID 5 arrives at T=12 with Priority 2. It performs a complex CPU burst requesting/releasing Resource 1 and 2.

---

## ⚙️ Execution Guide

1. **Prerequisites**: Python 3.8+ installed.
2. **Setup**: Define your process workload in `test.txt`.
3. **Run**:
   ```bash
   python code.py
   ```

---

## 📈 System Output

Upon completion, the simulator provides:
1. **Detailed Process Logs**: `[PID, Wait_time, IO_time, Ready_time]` for every process.
2. **Gantt Chart**: A chronological map of CPU usage.
3. **Efficiency Metrics**: Average Waiting and Turnaround times to evaluate system throughput.

---

## 👥 Authors

| Name | Student ID | Role |
| :--- | :--- | :--- |
| **Ibraheem Sleet** | 1220200 | Lead Developer / Simulation Logic |
| **Anwar Atawna** | 1222275 | Resource Management / Deadlock Logic |

**ENCS3390 - Operating Systems Project**  
*Birzeit University*
