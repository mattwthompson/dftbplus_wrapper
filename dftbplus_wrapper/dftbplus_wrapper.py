import os
import pathlib
from distutils.spawn import find_executable
from subprocess import PIPE, Popen

import numpy as np
import mbuild as mb


def run_xyz2gen(filename, lattfile=None):
    """Call `xyz2gen`

    TODO: Call these functions directly from Python
    """
    ext = pathlib.Path(filename).suffix
    if ext != '.xyz':
        raise ValueError('Expected xyz input')

    cmd = 'xyz2gen {}'.format(filename)

    if lattfile is not None:
        cmd += ' -l {}'.format(lattfile)

    os.system(cmd)


def mbuild_to_gen(compound):
    if not isinstance(compound, mb.Compound):
        raise ValueError(
            'Input must be a mbuild.Compound. Read in '
            'type {}'.format(type(compound))
        )

    compound.save('compound.xyz')
    run_xyz2gen(filename='compound.xyz')


def _box_to_lattfile(box, lattfile_name):
    """Write out lattice vectors from an mbuild.Box"""

    if not isinstance(box, mb.Box):
        raise ValueError('Input box must be an mbuild.Box instance')

    if not np.allclose(box.angles, [90, 90, 90]):
        raise ValueError('Only rectangular boxes are currently supported')

    if np.max(box.lengths) != np.min(box.lengths):
        raise ValueError('Only cubic boxes are currently supported')

    L = box.lengths[0]

    box_vectors = np.array([
        [L, 0, 0],
        [0, L, 0],
        [0, 0, L],
    ])

    np.savetxt(lattfile_name, box_vectors, fmt="%f")


def write_hsd(gen_path, skf_path='/Users/mwt/software/dftbplus/external/slakos/origin/mio-1-1/'):
    MOMENTA = {
        'H': 's',
        'C': 'p',
        'O': 'p',
        'N': 'p',
    }

    stem = pathlib.Path(gen_path).stem

    compound = mb.load(stem + '.xyz')

    elements = ""

    for elem in set([p.name for p in compound.particles()]):
        elements += '\n    {} = "{}"'.format(elem, MOMENTA[elem])

    INP = """Geometry = GenFormat {{
    <<< {0}
    }}

    Driver = ConjugateGradient {{
      MaxSteps = 1000
    }}

    Hamiltonian = DFTB {{
      Scc = Yes
      SlaterKosterFiles = Type2FileNames {{
        Prefix = "{1}"
        Separator = "-"
        Suffix = ".skf"
        LowerCaseTypeName = No
      }}
      MaxAngularMomentum {{{2}
      }}
    }}
    """.format(gen_path, skf_path, elements)

    with open('dftb_in.hsd', 'w') as fi:
        fi.write(INP)


def run_dftbplus():
    DFTBPLUS = find_executable('dftb+')

    proc = Popen('{} {}'.format(DFTBPLUS, 'dftb_in.hsd'),
                 stdin=PIPE, stdout=PIPE, stderr=PIPE,
                 universal_newlines=True, shell=True)

    out, err = proc.communicate()
    print(out)
    print(err)
