## Research Plan: Physical–Digital Alignment Study

This document outlines the step‑by‑step plan for conducting the
physical–digital alignment research as described in the paper. It
provides guidance on environment setup, data simulation, model
development, experimental design, analysis, and integration with the
GitHub repository. The goal is to reproduce, in a simplified form,
the methodology used in the original study and generate a small
empirical dataset for reporting purposes.

### 1. Environment Configuration

1. **Set up Python environment**: Ensure Python 3.10+ is installed. A
   conda environment is recommended. Create and activate an
   environment using the provided `environment.yml` or manually
   installing dependencies such as `numpy`, `tyro` (for CLI
   argument parsing), and `pytest` for tests.
2. **Directory structure**: The project is organized into the
   following folders:

   - `src/collectors`: Contains modules for data collection and
     simulation.
   - `src/models`: Contains the world model implementation and
     evaluation utilities.
   - `scripts`: Command‑line scripts to run experiments and train
     models.
   - `tests`: Unit tests to ensure basic functionality.
   - `data`: Storage location for generated datasets and results.
   - `docs`: Documentation, including this plan and technical
     specifications.

### 2. Data Simulation

1. Use the function `simulate_dataset(n_samples, noise_level, complexity)`
   from `src/collectors/simulator.py` to generate synthetic datasets.
   - `n_samples` determines the number of observations per dataset.
   - `noise_level` controls the standard deviation of Gaussian noise
     applied to the target; two levels (low and high) represent
     sensor noise conditions.
   - `complexity` defines the linearity of the underlying function;
     when set to `2` a quadratic term is added to emulate more
     complicated dynamics.
2. The helper `simulate_experiment(num_conditions, n_samples)`
   automatically generates multiple datasets across combinations of
   noise and complexity. In this simplified study we use four
   conditions (2 noise levels × 2 complexity levels).

### 3. Variable Definitions

The key variables measured in the experiment are:

| Variable                | Description                                                 |
|-------------------------|-------------------------------------------------------------|
| `coef`                 | Estimated slope of the linear model                          |
| `intercept`            | Estimated intercept of the linear model                      |
| `rmse`                 | Root mean squared error between predictions and ground truth |
| `mae`                  | Mean absolute error between predictions and ground truth     |
| `fit_time`             | Time (seconds) to fit the linear model                       |

These variables correspond to the information quality (errors) and
system quality (training time) constructs of the original research.

### 4. Research Methodology

1. **Experimental design**: A repeated‑measures design with four
   conditions is used. For each condition, a synthetic dataset with
   specified noise and complexity parameters is generated.
2. **Model training**: A simple linear regression model
   (`LinearWorldModel`) is fitted to each dataset using least squares.
3. **Evaluation metrics**: After fitting, compute RMSE and MAE to
   assess prediction accuracy. Record the coefficient and intercept as
   proxy measures for model performance and underlying process
   recovery. The time taken to fit the model serves as a system
   efficiency measure.
4. **Replication**: The script allows varying the number of samples
   and conditions. For reproducibility, a fixed random seed is used.
5. **Results storage**: Metrics for each condition are aggregated
   into a list and optionally saved as a CSV file within the `data`
   folder. This file can be committed to GitHub for tracking.

### 5. Analysis & Reporting

After running `scripts/run_experiments.py`, examine the printed
metrics or CSV file. Compare RMSE and MAE across conditions to see
how noise and complexity affect prediction accuracy. Inspect `fit_time`
to understand the computational cost. These findings should be
summarized in the final report to provide evidence of how the
physical–digital alignment mechanism (represented here by the world
model) performs under different operational conditions.

### 6. GitHub Workflow

1. **Commit early and often**: Each time you add a new file (e.g.,
   code, results, documentation), use the GitHub web interface to
   create or edit the file. Provide informative commit messages that
   describe what was added or changed.
2. **Branching (optional)**: For larger changes or feature additions,
   create a branch off `main` (e.g., `feature/world-model`) and open a
   pull request when ready. This allows code review and version
   control best practices. For the purposes of this demonstration,
   direct commits on `main` are acceptable.
3. **Issue tracking**: Use GitHub Issues to document tasks, bugs, or
   enhancements. Each task in this plan could correspond to an issue.
4. **Continuous integration**: Tests located in `tests/` can be run
   manually via `pytest` or automatically via a CI workflow (e.g., via
   GitHub Actions) to ensure the codebase remains stable.

### 7. Execution Checklist

- [x] Write simulator and world model modules (`src/collectors/simulator.py`,
  `src/models/world_model.py`)
- [x] Implement experiments script (`scripts/run_experiments.py`)
- [x] Write unit tests (`tests/test_pipeline.py`)
- [x] Generate and save results (`data/experiment_results.csv`)
- [x] Commit all code and documentation changes to GitHub

Upon completing these steps, the project will contain a cohesive
pipeline from data generation through model training to result
reporting, aligned with the objectives of the physical–digital
alignment research.
