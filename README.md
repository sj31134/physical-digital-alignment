# Physical–Digital Alignment for IS Success

This repository contains the open‑source implementation of the
**physical–digital alignment** research described in our paper
“Physical–Digital Alignment for IS Success: A Design Science Integration of
Robots, Transformer World Models, and Virtual Data in SMEs.”  The goal of
this project is to provide a reproducible framework that seamlessly
integrates physical robotics, AI‑driven world models, and virtual data
integration to improve information and system quality in resource‑constrained
organizations.

## Features

- **Automated data acquisition** using the [LeRobot](https://huggingface.co/lerobot)
  SDK for real‑time sensor logging and control of TurtleBot3 robots.
- **Transformer-based world model** for learning latent dynamics of the
  robot and predicting future states, enabling robust forecasts and
  closed‑loop control.
- **Virtual data integration** via Palantir AIP Virtual Tables or
  open‑source alternatives (DuckDB/Trino) to join sensor data with
  enterprise databases without costly ETL pipelines.
- **Simulation environment** built on ROS Noetic and Gazebo to support
  hundreds of experimental scenarios, varying task complexity, noise,
  network latency, and hardware constraints.
- **Reproducible analysis** using Jupyter notebooks for statistical tests
  (ANOVA, t‑tests, correlation) and visualization of results.

## Quick start

1. Clone this repository:
   ```bash
   git clone https://github.com/<your‑username>/physical-digital-alignment.git
   cd physical-digital-alignment
   ```
2. Create and activate a Python 3.11 virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   ```
3. Install the core dependencies:
   ```bash
   pip install -r requirements.txt
   # or manually: pip install lerobot transformers torch duckdb pandas numpy
   ```
4. Follow the [technical specification](docs/technical_spec.md) to set up
   ROS, Gazebo, TurtleBot3, and data virtualization.  The document
   outlines hardware requirements, software versions, and step‑by‑step
   configuration.
5. Run the example simulation script (coming soon) to collect data and
   train a simple world model.

## Repository structure

See the [`docs/technical_spec.md`](docs/technical_spec.md) document for a
detailed description of the directory layout and execution plan.  The
top‑level folders include:

| Folder     | Purpose                                                         |
|------------|-----------------------------------------------------------------|
| `docs/`    | Technical specifications, reports, and documentation            |
| `src/`     | Source code for data collection, modeling, virtualization, etc. |
| `data/`    | Raw and processed datasets (ignored by git)                     |

## Contributing

Contributions are welcome!  Please open an issue to discuss ideas or report
problems.  For code contributions, create a feature branch, commit your
changes with clear messages, and open a pull request.  Ensure that your
code is well documented and passes linting and unit tests.

## License

This project is licensed under the MIT License.  See `LICENSE` for details.

## Citation

If you use this code in your research, please cite the accompanying
paper and this repository.  A `CITATION.cff` file will be provided to
facilitate citation.
