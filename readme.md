# CMS From Python Proof of Concept with [Python.NET](https://pythonnet.github.io/)

## Quick Start with Docker

### Get a local copy of the docker container image

**Option 1- pull the image from Docker Hub:**

```bash
docker pull clorton/idmcms:1.0
```

**Option 2- build the image locally:**

```bash
docker build --tag clorton/idmcms:1.0 .
```

### Choose one of the following options for running compartmental models:

1. _Run the default command in the container (`python3 seir.py`)._<br>This will write trajectory data to `trajectories.net.csv` and a plot to `trajectory.png`.
```bash
docker run --rm -it -v $(pwd):/host -w /host clorton/idmcms:1.0 
```
Run this from the directory where your python scripts live. The container will see them under `/host/`. You can modify `seir.py` in place if you want to try other epidemiological parameters.

2. _Run the SEIR model with Python._<br>This will write trajectory data to `trajectories.net.csv` and a plot to `trajectory.png`.
```bash
docker run --rm -it -v $(pwd):/host -w /host clorton/idmcms:1.0 python3 seir.py --png
```
Run this from the directory where your python scripts live. You can add your own model here instead of `seir.py`.

3. _Run the model of your choice, written in EMODL, directly in CMS with the Mono .Net runtime (this verifies that the container is correctly set up to run .Net code with the Mono runtime)._<br>This will write trajectory data to `trajectories.cms.csv`.
```bash
docker run --rm -it -v $(pwd):/host -w /host clorton/idmcms:1.0 mono bin/compartments.exe --model seir.emodl --config config.json
```
Run this from the directory where your model and config files live. You can add your own model and config here instead of `seir.emodl` and `config.json`.

## Documentation

* [1-pager overview](https://github.com/InstituteforDiseaseModeling/pycms/blob/master/specs/one-pager.md)
* [Specification](https://github.com/InstituteforDiseaseModeling/pycms/blob/master/specs/specification.md)

## Local Setup

- consider creating a virtual environment with `python -m virtualenv venv`
- activate your virtual environment with `venv\scripts\activate.bat`
- install requirements (Python.NET and Matplotlib) with `pip install -r requirements.txt`

## Execution

- run the simple SEIR model with `python seir.py`

## Ideas for Extension

- Convert trajectory data from the solver to a pandas dataframe.
- `ISolver.Solve()` repeatedly calls `StartRealization()` followed by `SolveOnce()` - expose these calls in `ISolver`.
- `SolveOnce()` calls `StepOnce()` while `CurrentTime < duration` followed by `trajectories.RecordObservables()` - expose `StepOnce()` in `ISolver` and `RecordObservables()` (TBD)
- Expose `SolverBase.model` to Python code to inspect state.

### Additional Extensions

- Creating the textual representation of the model and loading it with the EMODL parser is a little clunky. Consider wrapping a Python class around the `ModelBuilder` and its various parts, e.g. `SpeciesDescription`, in order to build the model directly.

### [Mono](https://www.mono-project.com/)

- Investigate building `compartments` with Mono on macOS &| Linux.
- Verify that Python.NET on macOS &| Linux works with Mono version of `compartments`
- Might need [IronScheme](https://github.com/IronScheme/IronScheme) to compile against Mono if we don't have "Additional Extensions" above.

### [.NET Core](https://docs.microsoft.com/en-us/dotnet/core/)

- Investigate building `compartments` with .NET Core on macOS &| Linux.
- Look for Python.NET to [support .NET Core](https://github.com/pythonnet/pythonnet/issues/984)
- Might need [IronScheme](https://github.com/IronScheme/IronScheme) to compile against .NET Core if we don't have "Additional Extensions" above.

### Python.Net [Troubleshooting Installation on Linux](https://github.com/pythonnet/pythonnet/wiki/Troubleshooting-on-Windows,-Linux,-and-OSX#2-build-and-install-from-command-line)

- requires mono-complete or mono-devel
- requires clang (`sudo apt-get install clang`)
- requires glib (`sudo apt-get install libglib2.0-dev`)
- requires python-dev

- `sudo pip3 install pythonnet` fails with `error: option --single-version-externally-managed not recognized`
- try `sudo pip3 install --egg git+https://github.com/pythonnet/pythonnet`

### Python.Net Installation on macOS

- These instructions assume Python 3 on the machine [(download here)](https://www.python.org/downloads/).
- [install homebrew](https://brew.sh/)
- install pkg-config with `brew install pkg-config`
- [install mono for macOS](https://www.mono-project.com/download/stable/)
- **Note: mono includes a `mono-2.pc` file compatible with pkg-config, but does not put it where pkg-config can find it.**
  - verify that the `mono-2.pc` file is in the following location: `/Library/Frameworks/Mono.framework/Versions/6.10.0/lib/pkgconfig/`
  - run the following command to help `pkg-config` find `mono-2.pc`:  
    `export PKG_CONFIG_PATH=/Library/Frameworks/Mono.framework/Versions/6.10.0/lib/pkgconfig/`
  - verify that `pkg-config` sees the `mono-2.pc` file by running `pkg-config --libs mono-2`
- install Python.Net with `pip3 install pythonnet` (_alternatively_ install the latest Python.Net with `pip3 install git+https://github.com/pythonnet/pythonnet`)
