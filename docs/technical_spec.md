# Physical–Digital Alignment Research System

This document defines the technical specifications and deployment plan for the
research described in the paper *Physical–Digital Alignment for IS Success*.  It
covers the system environment configuration, software dependencies, high‑level
design, data collection procedures, and repository structure.  The goal is to
enable reproducibility and ease of deployment for collaborators.

## 1. System environment configuration

The experiments are designed to run on a Linux host.  The recommended base
environment matches that used during development:

- **Operating system**: Ubuntu 22.04 LTS (64‑bit)
- **Processor**: Intel Core i7‑12700 (or equivalent; 8+ cores recommended)
- **Memory**: 16 GiB RAM minimum (32 GiB or more preferred)
- **Storage**: ≥100 GB free disk space for datasets and logs
- **GPU**: NVIDIA RTX 3080 (10 GiB) or better; CUDA 11.8; optional but
  recommended for training the transformer world model
- **Network**: Broadband connection to download dependencies and (optionally)
  interact with external datasets

### 1.1 Software prerequisites

The following packages and services should be installed before running any
experiments:

| Component              | Version                | Source/Notes                                                     |
|----------------------- |----------------------- |-----------------------------------------------------------------|
| **Python**            | 3.11                   | Install via `pyenv` or system package manager                   |
| **ROS**               | Noetic Ninjemys        | Use `sudo apt install ros-noetic-desktop-full`                  |
| **Gazebo**            | 11 (Noetic default)    | Comes with ROS Noetic                                           |
| **TurtleBot3**        | `robotis-gazebo`       | Install via ROS package `ros-noetic-turtlebot3-simulations`     |
| **LeRobot SDK**       | Latest release         | Install from Hugging Face: `pip install lerobot`                |
| **Transformers**      | 4.31                   | `pip install transformers==4.31.0`                              |
| **PyTorch**           | 2.1                    | `pip install torch==2.1.0+cu118 -f https://download.pytorch.org/whl/cu118/torch_stable.html` |
| **Data virtualization**| Palantir AIP Virtual Tables† | Use Palantir Foundry API or alternative (e.g. DuckDB external tables) |
| **Docker** (optional) | 24.0                   | To encapsulate and share reproducible images                   |
| **Git**               | 2.40+                  | Version control for project code                                |

† If Palantir AIP is unavailable, we recommend using the open‑source query
engine [DuckDB](https://duckdb.org) with external tables or [Trino/Presto]
as a drop‑in replacement for virtual table functionality.

### 1.2 GPU setup

To accelerate training of the transformer world model, install the appropriate
NVIDIA drivers and CUDA toolkit matching your GPU.  Verify PyTorch can detect
the GPU by running

```bash
python3 -c "import torch; print(torch.cuda.get_device_name(0))"
```

If a GPU is not available, set the environment variable `CUDA_VISIBLE_DEVICES=""`
so that PyTorch falls back to CPU execution.  Training will take longer but
results should still be reproducible.

## 2. Repository layout

The project is structured as follows:

```
physical-digital-alignment/
├─ docs/                    # Documentation (this file and reports)
├─ src/
│  ├─ lerobot/              # Scripts for automated data collection
│  ├─ world_model/          # Transformer model definition and training scripts
│  ├─ virtual_tables/       # Interfaces for data virtualization (AIP, DuckDB)
│  ├─ simulation/           # ROS/Gazebo scenario definitions and launch files
│  └─ analysis/             # Statistical analysis and visualization notebooks
├─ data/                    # Raw and processed datasets
│  ├─ raw/                  # Sensor logs and external data snapshots
│  └─ processed/            # Cleaned data ready for modeling
├─ .gitignore              # Patterns to exclude from git version control
├─ README.md               # Project overview and setup instructions
└─ LICENSE                 # Open‑source license (e.g. MIT)
```

All code should be written in Python 3.11 using clear docstrings and type
annotations.  Each submodule contains its own README describing how to run
scripts in that directory.  The `analysis/` folder contains Jupyter notebooks
for exploratory data analysis and reproducible statistical tests.

## 3. Setup and installation

1. **Clone the repository.**
   ```bash
   git clone https://github.com/<your‑username>/physical-digital-alignment.git
   cd physical-digital-alignment
   ```

2. **Create a virtual environment.**  We recommend using `venv` or `conda` to
   isolate dependencies.  For example:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   ```

3. **Install Python dependencies.**  A `requirements.txt` file will be
   generated during development.  For now, install the primary packages:
   ```bash
   pip install lerobot transformers torch==2.1.0 duckdb pandas numpy scipy
   ```

4. **Install ROS and Gazebo.**  Follow the official ROS Noetic installation
   guide for Ubuntu 22.04.  After installation, run:
   ```bash
   source /opt/ros/noetic/setup.bash
   ```
   Install TurtleBot3 simulation packages:
   ```bash
   sudo apt install ros-noetic-turtlebot3-simulations
   ```

5. **Configure Palantir AIP or an alternative.**  If you have access to
   Palantir, configure authentication and create Virtual Tables pointing to
   your data sources.  Otherwise, create external tables in DuckDB or Presto
   connecting to your CSVs or relational databases.  See `src/virtual_tables/README.md`
   for instructions.

## 4. Execution plan

The research execution is organized into phases.  Each phase maps to scripts
and tasks within the repository.

### Phase 0: Planning and repository setup

1. **Define scenarios.**  Document the 360 simulation scenarios varying task
   complexity, environmental uncertainty, data volatility, network latency,
   resource constraints, and operator interventions as described in the paper.
2. **Create a GitHub repository.**  Initialize the local git repo (see
   instructions below) and push to GitHub.
3. **Draft documentation.**  Include this technical spec and create READMEs for
   each module.

### Phase 1: Environment configuration

1. Install OS dependencies and Python packages per Section 1.
2. Configure ROS/Gazebo and download TurtleBot3 models.
3. Verify LeRobot SDK can connect to your robot simulator.
4. Prepare AIP or DuckDB connection strings and test simple queries.

### Phase 2: Data acquisition

1. **Automated data collection.**  Implement scripts in `src/lerobot/` to
   interface with LeRobot for real‑time sensor and control signal capture.  For
   each simulation scenario, collect:
   - Position, velocity, and force readings at 10 Hz
   - Environmental variables (e.g. noise level, task complexity indicator)
   - Timestamps for start and end of each task cycle
2. **External data ingestion.**  Use Virtual Tables (or DuckDB) to fetch
   enterprise data (e.g. inventory levels, production orders).  Archive
   snapshots in `data/raw/external/`.
3. **Data logging.**  Store raw logs in `data/raw/sim/`.  Use a consistent
   naming convention: `scenario_<id>_run_<rep>.csv`.

### Phase 3: World model training and prediction

1. **Data preprocessing.**  Write a pipeline in `src/world_model/data.py` to
   clean, resample, and merge sensor and external data.  Produce
   feature matrices and target variables for the transformer model.
2. **Model definition.**  Implement a transformer encoder–decoder in
   `src/world_model/model.py`.  Start with default hyperparameters (e.g.
   d_model=256, 4 heads, 3 layers) and adjust based on validation loss.
3. **Training.**  Use PyTorch to train on the combined dataset.  Save
   checkpoints in `data/processed/models/`.  Implement early stopping and
   logging.
4. **Prediction interface.**  Create a function to generate predictions
   on new sensor streams in real time.  Expose this via a REST API or ROS
   service, if desired.

### Phase 4: Data virtualization and integration

1. **Configure Virtual Tables** to point to the processed world model
   outputs and external data.  If using DuckDB, register the model outputs
   as tables via `CREATE VIEW`.  If using Palantir AIP, create a virtual
   dataset from the S3 or database sources.
2. **Join data.**  Demonstrate joining sensor predictions with enterprise
   data in real time.  Validate that queries execute quickly (<500 ms).

### Phase 5: Evaluation and analysis

1. **Scenario runs.**  Execute all 360 scenarios with and without the
   full integration.  Automate runs via a master script (see
   `src/simulation/run_all.py`).  Each run writes summary metrics (accuracy,
   RMSE, processing time) to `data/processed/metrics.csv`.
2. **Statistical analysis.**  Using notebooks in `src/analysis/`, compute
   means, standard deviations, ANOVA tests, and effect sizes.  Plot results.
3. **Quality coupling**: Compute Pearson correlation between info and system
   quality improvements.  Visualize scatter plots and regression lines.
4. **Report generation.**  Summarize findings in Markdown or LaTeX for
   publication.  Use the figures and tables generated during analysis.

## 5. Git repository setup and contribution workflow

1. **Initialize the local repository.**  After cloning the GitHub repo, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit with technical spec and project structure"
   ```

2. **Push to GitHub.**  Add the remote origin (replace `<username>`):
   ```bash
   git remote add origin https://github.com/<username>/physical-digital-alignment.git
   git branch -M main
   git push -u origin main
   ```
   You will be prompted for credentials; authenticate with your GitHub
   username and personal access token (PAT) instead of a password.

3. **Branching strategy.**  Use feature branches (e.g. `feature/world-model`)
   for new components.  Submit pull requests (PRs) for review before merging
   into `main`.  Use semantic commit messages.

4. **Issue tracking.**  Track tasks and enhancements via the GitHub Issues
   tab.  Link commits and PRs to issue numbers using `#<issue>` notation.

5. **Continuous integration (optional).**  Configure GitHub Actions to run
   linting (e.g. flake8), unit tests, and static type checking on each PR.

## 6. License and citation

We recommend releasing this project under the MIT License to maximize
reusability.  Include a `LICENSE` file and a `CITATION.cff` file to help
others cite your work correctly.  The citation should reference the
associated publication and include the GitHub DOI generated by Zenodo.

---

This technical specification provides the roadmap for reproducing the
physical–digital alignment research.  Future contributors should follow
these guidelines to ensure consistency and reproducibility.
