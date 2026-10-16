# mocsy (CSCS uenv fork)

Routines to model ocean carbonate system thermodynamics.

This is a fork of [jamesorr/mocsy](https://github.com/jamesorr/mocsy)
(upstream `master`, commit `65ac49e`). The Fortran code is unchanged. The
`Makefile` and documentation are updated so that the Python module builds with
current NumPy/f2py (meson backend), in particular on
[CSCS Alps](https://docs.cscs.ch/) inside a
[uenv](https://docs.cscs.ch/software/uenv/).

- Canonical repository: <https://gitlab.climate.unibe.ch/ocean_modelling/mocsy_cscs_uenv>
- Mirror: <https://github.com/ursho2552/mocsy_CSCS_uenv>
- Original: <https://github.com/jamesorr/mocsy>

## Synopsis

mocsy is a Fortran 95 package designed to compute all carbonate system
variables from total dissolved inorganic carbon (DIC) and total alkalinity,
particularly from models. It updates previous OCMIP code, avoids 3 common model
approximations, and offers the best-practice constants as well as more recent
options. It agrees with CO2SYS within 0.005%.

The package is described by Orr and Epitalon (2015) and has been compared to
other packages that compute marine carbonate chemistry (Orr et al., 2015).
Routines to propagate uncertainties and compute sensitivities of derived
variables to input variables were added later (Orr et al., 2018).

## Requirements

- a Fortran compiler (`gfortran` by default), `make` and `m4`
- Python 3 with **NumPy >= 2.4**
- `meson` and `ninja` (f2py's build backend)

> **NumPy version matters.** f2py's meson backend only links the extra object
> files (the GSW and DNAD routines) from NumPy 2.4.0 onwards. With older NumPy
> the build appears to succeed, but `import mocsy` then fails with
> `undefined symbol: __dual_num_auto_diff_MOD_...`.

## Build on CSCS Alps (uenv)

### 1. Get the code

```bash
git clone <repo url>
cd mocsy_cscs_uenv
```

### 2. Start the uenv

The `netcdf-tools` uenv provides GCC/gfortran and Python
([CSCS docs](https://docs.cscs.ch/software/cw/netcdf-tools/)).

```bash
uenv image find netcdf-tools     # list the versions available on this cluster
uenv start --view=netcdf netcdf-tools/2025:v2
```

> `netcdf-tools/2025:v2` is currently available on **Eiger only**. On other
> Alps clusters, use `netcdf-tools/2025:v1`.

### 3. Create a Python virtual environment on top of the uenv

This follows the
[CSCS Python guide](https://docs.cscs.ch/build-install/python/):

```bash
unset PYTHONPATH
export PYTHONUSERBASE="$(dirname "$(dirname "$(which python)")")"
python -m venv --system-site-packages path/to/my-venv
source path/to/my-venv/bin/activate
```

Install the build dependencies listed in [`requirements.txt`](requirements.txt)
(`numpy>=2.4`, `meson`, `ninja`, `charset_normalizer`):

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

The venv only works from inside the uenv it was created in. When you log in
again, start the same uenv before activating the venv. If you switch to a
different uenv version, create a new venv.

### 4. Compile

```bash
make clean
make mocsy.so
```

Compiler warnings during the build are expected. The result is a file named
like `mocsy.cpython-313-x86_64-linux-gnu.so` (the suffix depends on the Python
version). Running `make mocsy.so` again does nothing unless sources changed.

### 5. Check the build

```bash
python -c "import mocsy; print(mocsy.__file__)"
```

## Build elsewhere

On any Linux machine with the [requirements](#requirements) above, activate a
Python environment, then run:

```bash
pip install --upgrade -r requirements.txt
make clean
make mocsy.so
```

On module-based clusters, load a GCC module first and create the
Python environment on top of it.

Useful Makefile variables:

- `PYTHON`: interpreter to build for, e.g. `make mocsy.so PYTHON=/path/to/python`
- `FCBIN`: Fortran compiler command (default `gfortran`)
- `PRECISION`: `2` for double precision (default), `1` for single

The Fortran library and test programs build without Python:

```bash
make test_mocsy
./test_mocsy
```

`make` without a target builds the library, the Python module and all Fortran
test programs.

## Using mocsy from Python

```python
import mocsy
print(mocsy.__doc__)                 # list of modules
print(mocsy.mvars.vars.__doc__)      # arguments of the main routine

pH, pco2, fco2, co2, hco3, co3, OmegaA, OmegaC, BetaD, rhoSW, p, tempis = mocsy.mvars.vars(
    temp=[18.0], sal=[35.0], alk=[2300e-6], dic=[2000e-6], sil=[0.0], phos=[0.0],
    patm=[1.0], depth=[0.0], lat=[0.0],
    optcon="mol/kg", optt="Tinsitu", optp="db",
)
```

Each Fortran module is exposed as `mocsy.m<name>` and contains the routine of
the same name, e.g. `mocsy.mconstants.constants(...)` or
`mocsy.mdepth2press.depth2press(...)`. The gas exchange routines are in
`mocsy.gasx`. Use `print(mocsy.<module>.<routine>.__doc__)` to see the
arguments.

The compiled module is not installed into the environment (the repository has
no `pip install` support). Run Python from the repository directory, or add
that directory to your path:

```bash
export PYTHONPATH=/path/to/mocsy_cscs_uenv:$PYTHONPATH
```

or, in Python:

```python
import sys
sys.path.append("/path/to/mocsy_cscs_uenv")
```

Note that step 3 above runs `unset PYTHONPATH`, so if you use the environment
variable, set it after activating the venv.

## Documentation

The original online documentation (`ocmip5.ipsl.jussieu.fr/mocsy`) no longer
exists. Build it locally with [Doxygen](https://www.doxygen.nl/):

```bash
doxygen Doxyfile
# open doc/html/index.html
```

The main page source is [`mainpage.txt`](mainpage.txt).

## Examples and tests

After `make mocsy.so`, from the repository root:

| What | How to run |
|---|---|
| Python examples ([`examples/*.py`](examples/)) | `python examples/test_mocsy.py` |
| Fortran examples ([`examples/*.f90`](examples/)) | `make test_errors && ./test_errors` |
| Regression test ([`test/test_mocsy.py`](test/test_mocsy.py)) | `pip install pytest`, then `pytest test` |
| Jupyter notebooks ([`notebooks/`](notebooks/)) | need `jupyter`, `pandas` and `matplotlib`; the notebooks find the module one directory up |

Example input data are in [`examples/data/`](examples/data/).

## References

Orr, J. C. and Epitalon, J.-M. (2015) Improved routines to model the ocean
carbonate system: mocsy 2.0, *Geosci. Model Dev.*, 8, 485–499,
<https://doi.org/10.5194/gmd-8-485-2015>.

Orr, J. C., Gattuso, J.-P., and Epitalon, J.-M. (2015) Comparison of ten
packages that compute ocean carbonate chemistry, *Biogeosciences*, 12,
1483–1510, <https://doi.org/10.5194/bg-12-1483-2015>.

Orr, J. C., Epitalon, J.-M., Dickson, A. G., and Gattuso, J.-P. (2018) Routine
uncertainty propagation for the marine carbon dioxide system, *Marine
Chemistry*, 207, 84–107, <https://doi.org/10.1016/j.marchem.2018.10.006>.

## License

MIT, Copyright (c) 2014 James Orr. See [`LICENSE`](LICENSE). The changes in
this fork are under the same license.
