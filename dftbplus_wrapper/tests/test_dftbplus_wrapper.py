import sys

import mbuild as mb

from dftbplus_wrapper.dftbplus_wrapper import (
    _box_to_lattfile, mbuild_to_gen, write_hsd, run_dftbplus)



def test_dftbplus_wrapper_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "dftbplus_wrapper" in sys.modules


def test_box_to_lattfile():
    _box_to_lattfile(mb.Box([4, 4, 4]), 'lat.lat')


def test_mbuild_conversion():
    SMILES = 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C'
    compound = mb.load(SMILES, smiles=True)

    mbuild_to_gen(compound)


def test_full_optimization():
    SMILES = 'N#CC'

    compound = mb.load(SMILES, smiles=True)
    mbuild_to_gen(compound)

    write_hsd(gen_path='compound.gen')

    run_dftbplus()
