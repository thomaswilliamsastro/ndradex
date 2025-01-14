# standard library
from pathlib import Path
from tempfile import TemporaryDirectory


# dependencies
import numpy as np
import ndradexhyperfine


# constants
COMMONS = {
    "N_mol": 1e15,
    "n_H2": 1e3,
    "T_bg": 2.73,
    "dv": 1.0,
    "geom": "uni",
}


# test functions
def test_binary_existences():
    """Ensure that builtin RADEX binaries exist."""
    assert (ndradexhyperfine.RADEX_BINPATH / "radex-uni").exists()
    assert (ndradexhyperfine.RADEX_BINPATH / "radex-lvg").exists()
    assert (ndradexhyperfine.RADEX_BINPATH / "radex-slab").exists()


def test_radex_single_run():
    """Ensure that the output of RADEX single run is correct."""
    ds = ndradexhyperfine.run("co.dat", "1-0", 100, **COMMONS)
    assert np.isclose(ds["I"], 1.36)
    assert np.isclose(ds["F"], 2.684e-8)


def test_radex_grid_run():
    """Ensure that the output of RADEX grid run is correct."""
    ds = ndradexhyperfine.run(
        "co.dat",
        ["1-0", "2-1", "3-2"],
        [100, 200, 300],
        **COMMONS,
    )
    assert np.isclose(ds["I"].sel(QN_ul="1-0", T_kin=100), 1.36)
    assert np.isclose(ds["F"].sel(QN_ul="1-0", T_kin=100), 2.684e-8)


def test_work_dir():
    """Ensure that work_dir option works correctly."""
    with TemporaryDirectory(dir=".") as work_dir:
        ndradexhyperfine.run("co.dat", "1-0", 100, work_dir=work_dir)
        assert not list(Path(work_dir).glob("*"))


def test_dataset_io():
    """Ensure that I/O functions works correctly."""
    with TemporaryDirectory(dir=".") as temp_dir:
        filename = Path(temp_dir) / "test.nc"

        ds_before = ndradexhyperfine.run("co.dat", "1-0", 100)
        ndradexhyperfine.save_dataset(ds_before, filename)
        ds_after = ndradexhyperfine.load_dataset(filename)

        ds_bool = (ds_before == ds_after).all()
        for dataarray in ds_bool.values():
            assert dataarray
