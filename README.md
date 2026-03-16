# 🔥 Wildfire Risk Detection Model

This repository contains my **Leaving Cert Computer Science project**.

The project focuses on **nature and the environment**, specifically on **wildfire risk detection**.

The system reads **temperature and soil moisture data**, calculates a **wildfire risk level**, and visualises the results using graphs.

The program can run in two modes:

- **Real-Time Mode** → Uses live data from a **Micro:Bit**
- **Simulation Mode** → Uses predefined datasets

---

# 🚀 Running the Program

The main program is **`wildfire_risk.py`**.

Running the program directly will start it in **Real-Time Mode** by default.  
You can change behaviour using command-line arguments.

---

## ⚙️ Command Line Arguments

```
./wildfire_risk.py [options]
```

| Argument | Description |
|--------|-------------|
| `-m`, `--mode` | Select mode: `realtime` or `simulation` (default: `realtime`) |
| `-tu`, `--time_units` | Time units: `hours`, `minutes`, `seconds` |
| `-d`, `--dataset` | Dataset file used in simulation mode |
| `-i`, `--interval` | Sampling interval |
| `-s`, `--savefig` | Interval for saving graph images |
| `-v`, `--verbose` | Enable verbose output |

---

### Example — Real-Time Mode

```
./wildfire_risk.py --mode realtime --interactive 5 --savefig 10 --time_units minutes
```

This example:

- Runs the program in **real-time**
- Updates every **5 minutes**
- Saves graph images every **10 minutes**

---

### Example — Simulation Mode

```
./wildfire_risk.py --mode simulation --dataset Input/01_dataset_high_risk.csv
```

This example runs the model using a **dataset instead of real sensor data**.

---

# 🧠 Program Workflow

The project follows the **Observer Design Pattern**.

- **SerialReader** acts as the **Subject**
- **DataManagerCSV** and **MultiAxesGraph** act as **Observers**

Whenever new data is received, the **Subject notifies the Observers**, which then store and visualise the data.

---

## Real-Time Mode Workflow

```
                +----------------+
                | wildfire_risk  |
                +--------+-------+
                         |
                         v
                +----------------+
                |  SerialReader  |  (Subject)
                +--------+-------+
                         |
              Notify Observers
                /             \
               v               v
   +----------------+   +----------------+
   | DataManagerCSV |   | MultiAxesGraph |
   |   (Observer)   |   |   (Observer)   |
   +----------------+   +----------------+
```

**Responsibilities**

- **SerialReader**
  - Reads sensor data from the Micro:Bit through USB serial
  - Generates new records

- **DataManagerCSV**
  - Stores records in a CSV database

- **MultiAxesGraph**
  - Displays the data using **Matplotlib**

---

## Simulation Mode Workflow

Simulation mode is simpler because it uses **predefined datasets**.

```
wildfire_risk
      ↓
DataSetReader
```

`DataSetReader` reads the dataset and generates the graph.

---

# 📂 Project Structure

The program is organised into modules to keep the design **clean, modular, and maintainable**.

---

## Databases

Contains **`DataManagerCSV`**, which manages the CSV database.

Responsibilities:

- Reading stored data
- Writing new records

---

## Graph

Contains **`MultiAxesGraph`**, which visualises the collected data using **Matplotlib**.

Note:

`AnalogGraph` and `DigitalGraph` remain in the directory but are not used.  
They were part of an earlier design before the graph system was redesigned.

---

## Input

This directory stores **datasets used for simulation mode**.

The first four datasets correspond to the following **What-If scenarios**:

| Dataset | Scenario |
|-------|---------|
| Dataset 1 | High temperature + low soil moisture |
| Dataset 2 | Low temperature + high soil moisture |
| Dataset 3 | Mild temperature + high soil moisture |
| Dataset 4 | Mild temperature + low soil moisture |

You can add additional datasets to test other conditions.

---

## Microbit

This directory contains the code used by the **Micro:Bit**.

Included files:

- A **Python sample**
- Two ready-to-use `.hex` firmware files

### Hex Files

**microbit-test-at-home.hex**

- Moisture detected when value **> 30**

**microbit-Wildfire-Risk-Detection.hex**

- Moisture detected when value **> 300**

The difference between them is the **moisture threshold used to detect moisture**.

---

# 🌡️ Wildfire Risk Model

The wildfire risk model uses **two inputs**:

- **Temperature** \(T\) in degrees Celsius (analog input)
- **Moisture presence** \(M\) (digital input)

Although soil moisture is normally measured more accurately as an **analog value**, the project requirements required it to be implemented as a **digital input**.

---

## Model Calculation

### 1️⃣ Temperature Factor

The temperature factor is calculated and **clamped between 0 and 1**:

$$
T_f = \max\left(0,\ \min\left(1,\ \frac{T - 10}{30}\right)\right)
$$

Where:

- \(T\) = temperature in °C  
- \(T_f\) = normalized temperature factor

This means:

- Temperatures below **10 °C** produce very low wildfire risk.
- Temperatures above **40 °C** reach the maximum temperature contribution.

---

### 2️⃣ Moisture Factor

The moisture factor adjusts the wildfire risk depending on soil conditions:

$$
M_f =
\begin{cases}
0.6 & \text{if moisture is present} \\
1.0 & \text{if the environment is dry}
\end{cases}
$$

Dry conditions increase wildfire risk.

---

### 3️⃣ Final Wildfire Risk

The wildfire risk percentage is calculated as:

$$
R = T_f \times M_f \times 100
$$

Where:

- \(R\) = wildfire risk percentage  
- \(T_f\) = temperature factor  
- \(M_f\) = moisture factor  

---

### 4️⃣ Risk Classification

The resulting percentage is converted into four **risk levels**:

- **Low**
- **Moderate**
- **High**
- **Very High**

The model returns **both the risk percentage and the risk category**.

---

## Output

All images produced by the program are saved in this directory.

File names follow the format:

```
YYMMDD_HMS
```

This automatically sorts images **chronologically**.

---

## Tools

This directory contains utilities that can potentially be reused outside the project.

### SerialReader
Communicates with the **Micro:Bit via USB serial**, creates records, and sends data to the wildfire model.

### DataCollector
An **older data collection system** used before implementing the **Observer Design Pattern**.

### DataSetReader
Reads datasets and generates graphs during **simulation mode**.

---

# 📊 What-If Simulation Output

This directory contains **six graphs generated by the program**.

### Random simulations

1. Random dataset simulation  
2. Extreme edge case where **temperature changes abruptly**

---

### What-If scenario simulations

The remaining four graphs correspond to the **What-If datasets**:

| Scenario | Description |
|--------|-------------|
| What-If 1 | High temperature + low soil moisture |
| What-If 2 | Low temperature + high soil moisture |
| What-If 3 | Mild temperature + high soil moisture |
| What-If 4 | Mild temperature + low soil moisture |

These graphs demonstrate how the wildfire risk model reacts to different environmental conditions.

---
