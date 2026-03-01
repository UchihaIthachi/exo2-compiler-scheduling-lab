# Dependency Analysis and Scheduling — Exo 2 Submission Pack

This repository contains the completed assignment for the **In21-S8-CS4553 Dependency Analysis and Scheduling** course, focusing on the [Exo 2 scheduling language](https://arxiv.org/pdf/2411.07211). 

## Directory Contents

- **`report.md` / `report.tex` / `report.pdf`**: The comprehensive technical write-up covering Steps 1 through 3, including notes on Exo's scheduling primitives and analysis of the debugging quizzes.
- **`solutions/`**: Contains the corrected Exo Python schedules (`quiz1_solution.py`, `quiz2_solution.py`, `quiz3_solution.py`) that successfully compile and resolve the issues presented in the assignment.
- **`target/`**: The output directory containing the generated target C and Header (`.c`, `.h`) files derived from the solved schedules.
- **`generate_targets.sh`**: A utility shell script used to generate the required target C/H code by invoking the `exocc` compiler against the provided solutions.

---

## Running on the University VM (SSH)

The university provides a dedicated Virtual Machine (VM) for running this assignment.

1. **Connect to the VM via SSH:**
   Use the IP address and credentials provided by the university. Open your terminal and run:
   ```bash
   ssh username@<VM_IP_ADDRESS>
   ```
   *(Replace `username` and `<VM_IP_ADDRESS>` with your actual credentials).*

2. **Clone this submission repository onto the VM:**
   ```bash
   git clone <URL_TO_THIS_REPO>
   cd <REPO_NAME>
   ```

3. **Follow the generation instructions below** to install Exo and build the target outputs directly on the VM environment.

---

## Instructions for Generating Target Code (C/H)

To manually regenerate the compiled target files from the solved Exo schedules, follow these steps:

### 1. Clone the Exo Language Repository
You must have a local copy of the Exo compiler repository. Clone it and initialize its submodules:
```bash
git clone https://github.com/exo-lang/exo
cd exo && git submodule update --init --recursive
```

### 2. Install Dependencies
Ensure the Exo compiler (`exocc`) is available in your Python environment. You can install it via `pip` or build it from the source cloned in the previous step:
```bash
pip install exo-lang
```
*(Alternatively, you may build it from the cloned source directory following the instructions in the Exo repository).*

### 3. Generate the Target Code
From the root directory of this submission pack, execute the generation script, providing the path to your cloned Exo repository as an argument:
```bash
./generate_targets.sh /path/to/exo
```
This script will automatically invoke `exocc` on each solution file and populate the `target/` directory with the compiled C and header files.

---

## Submission Checklist

Ensure the following artifacts are included in your final upload:
- `report.pdf` (The final compiled write-up)
- `solutions/` (The corrected Python schedule files)
- `target/quiz1/`, `target/quiz2/`, `target/quiz3/` (The compiled C/H source outputs)
