#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Constants
~~~~~~~~~

This module contains package-wide constants, some of which are configurable.

The configuration is loaded upon import from a YAML file in the directory where
CyPhi is run: ``cyphi_config.yml``. If no file is found, the default
configuration is used.

The various options are listed here with their defaults:

- Control whether precomputed results are stored and read from a database or
  from a local filesystem-based cache in the current directory. Set this to
  'fs' for the filesystem, 'db' for the database.

    >>> import cyphi
    >>> cyphi.constants.CACHING_BACKEND
    'db'

- Set the configuration for the MongoDB database backend. This only has an
  effect if the caching backend is set to use the database.

    >>> import cyphi
    >>> cyphi.constants.MONGODB_CONFIG['host']
    'localhost'
    >>> cyphi.constants.MONGODB_CONFIG['port']
    27017
    >>> cyphi.constants.MONGODB_CONFIG['database_name']
    'cyphi'
    >>> cyphi.constants.MONGODB_CONFIG['collection_name']
    'cache'

- If the caching backend is set to use the filesystem, the cache will be stored
  in this directory.

    >>> import cyphi
    >>> cyphi.constants.PERSISTENT_CACHE_DIRECTORY
    '__cyphi_cache__'

- Control the number of CPU cores to evaluate unidirectional cuts. Negative
  numbers count backwards from the total number of available cores, with ``-1``
  meaning "use all available cores".

    >>> import cyphi
    >>> cyphi.constants.NUMBER_OF_CORES
    -1

- Controls the verbosity level for parallel computation (0--100).

    >>> import cyphi
    >>> cyphi.constants.PARALLEL_VERBOSITY
    20

- If set to ``True``, this defines the Phi value of subsystems containing only
  a single node with a self-loop to be ``0.5``. If set to False, their
  |big_phi| will be actually be computed (to be zero, in this implementation).

    >>> import cyphi
    >>> cyphi.constants.SINGLE_NODES_WITH_SELFLOOPS_HAVE_PHI
    False

- CyPhi employs several in-memory LRU-caches to speed up computation. However,
  these can quickly use up all the memory on a system; to avoid thrashing, this
  options limits the percentage of a system's RAM that the LRU caches can use.

    >>> import cyphi
    >>> cyphi.constants.MAXIMUM_CACHE_MEMORY_PERCENTAGE
    50

- Computations in CyPhi rely on finding the Earth Mover's Distance. This is
  done via an external C++ library that uses flow-optimization to find a good
  approximation of the EMD. Consequently, systems with zero |big_phi| will
  sometimes be computed to have a small but non-zero amount. This setting
  controls the number of decimal places to which CyPhi will consider EMD
  calculations accurate. Values of |big_phi| lower than ``10e-PRECISION`` will
  be considered insignificant and treated as zero. The default value is about
  as accurate as the EMD computations get.

    >>> import cyphi
    >>> cyphi.constants.PRECISION
    6
"""

from pprint import pprint
import sys
import errno
import yaml
import joblib

# TODO: document mongo config
# TODO: Use proper logging
# Defaults for configurable constants
config = {
    # The maximum percentage of RAM that CyPhi should use for caching.
    'MAXIMUM_CACHE_MEMORY_PERCENTAGE': 50,
    # MongoDB configuration.
    'MONGODB_CONFIG': {
        'host': 'localhost',
        'port': 27017,
        'database_name': 'cyphi',
        'collection_name': 'cache'
    },
    # The number of CPU cores to use in parallel cut evaluation. -1 means all
    # available cores, -2 means all but one available cores, etc.
    'NUMBER_OF_CORES': -1,
    # Controls whether the concept caching system is used.
    'CACHE_CONCEPTS': True,
    # The caching system to use. "fs" means cache results in a subdirectory of
    # the current directory; "db" means connect to a database and store the
    # results there.
    'CACHING_BACKEND': 'db',
    # Directory for the persistent joblib Memory cache.
    'PERSISTENT_CACHE_DIRECTORY': '__cyphi_cache__',
    # The number of decimal points to which phi values are considered accurate
    'PRECISION': 6,
    # In some applications of this library, the user may prefer to define
    # single-node subsystems as having 0.5 Phi.
    'SINGLE_NODES_WITH_SELFLOOPS_HAVE_PHI': False,
    # The verbosity of parallel computation. See documentation for
    # `joblib.Parallel`.
    'PARALLEL_VERBOSITY': 20
}


def print_config(self):
    """Prints the current configuration."""
    print(''.center(50, '-'))
    pprint(config)
    print(''.center(50, '-'))


# The name of the file to load configuration data from.
CYPHI_CONFIG_FILE = 'cyphi_config.yml'


# Try to load the config file, falling back to the default configuration.
try:
    with open(CYPHI_CONFIG_FILE) as f:
        config = yaml.load(f)
        print("\n[CyPhi] Loaded configuration from", CYPHI_CONFIG_FILE)
except OSError as e:
    if e.errno == errno.ENOENT:
        print("\n[CyPhi] Using default configuration (no config file "
              "provided)")
    else:
        raise e


# Get a reference to this module's dictionary..
this_module = sys.modules[__name__]
# Attach all the entries of the configuration dictionary to this module.
this_module.__dict__.update(config)
# Print the loaded configuration.
print_config(config)


# Un-configurable constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The threshold below which we consider differences in phi values to be
# zero.
EPSILON = 10 ** - this_module.PRECISION
# Constants for accessing the past or future subspaces of concept
# space.
PAST = 0
FUTURE = 1
# Constants for using cause and effect methods.
DIRECTIONS = ('past', 'future')
# Constants for labeling memoization backends.
FILESYSTEM = 'fs'
DATABASE = 'db'
# The protocol used for pickling objects.
PICKLE_PROTOCOL = 4
# Create the joblib Memory object for persistent caching without a
# database.
joblib_memory = joblib.Memory(cachedir=config['PERSISTENT_CACHE_DIRECTORY'],
                              verbose=1)
