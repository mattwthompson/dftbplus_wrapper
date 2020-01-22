"""
Unit and regression test for the dftbplus_wrapper package.
"""

# Import package, test suite, and other packages as needed
import dftbplus_wrapper
import pytest
import sys

def test_dftbplus_wrapper_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "dftbplus_wrapper" in sys.modules
