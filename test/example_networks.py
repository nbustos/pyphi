#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from pyphi.network import Network
from pyphi.subsystem import Subsystem


# TODO pass just the subsystem (contains a reference to the network)

use_connectivity_matrices = True


def standard(cm=False):
    """Matlab default network.

    Diagram:

    |           +~~~~~~+
    |    +~~~~~>|   A  |<~~~~+
    |    |      | (OR) +~~~+ |
    |    |      +~~~~~~+   | |
    |    |                 | |
    |    |                 v |
    |  +~+~~~~~~+      +~~~~~+~+
    |  |   B    |<~~~~~+   C   |
    |  | (COPY) +~~~~~>| (XOR) |
    |  +~~~~~~~~+      +~~~~~~~+

    TPM:

    +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
    | Past state ~~> Current state |
    |~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~|
    |   A, B, C    |    A, B, C    |
    |~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~|
    |  {0, 0, 0}   |   {0, 0, 0}   |
    |  {0, 0, 1}   |   {1, 1, 0}   |
    |  {0, 1, 0}   |   {1, 0, 1}   |
    |  {0, 1, 1}   |   {1, 1, 1}   |
    |  {1, 0, 0}   |   {0, 0, 1}   |
    |  {1, 0, 1}   |   {1, 1, 1}   |
    |  {1, 1, 0}   |   {1, 0, 0}   |
    |  {1, 1, 1}   |   {1, 1, 0}   |
    +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+

    Connectivity matrix:

    (CM_ij = 1 means that node i is connected to node j)

    |       A  B  C
    |     +~~~~~~~~~+
    |   A | 0, 0, 1 |
    |   B | 1, 0, 1 |
    |   C | 1, 1, 0 |
    |     +~~~~~~~~~+

    """
    # TODO? make these into dictionaries/named tuples
    current_state = (1, 0, 0)
    past_state = (1, 1, 0)
    tpm = np.array([[0, 0, 0],
                    [0, 0, 1],
                    [1, 0, 1],
                    [1, 0, 0],
                    [1, 1, 0],
                    [1, 1, 1],
                    [1, 1, 1],
                    [1, 1, 0]])
    if cm is False:
        cm = np.array([[0, 0, 1],
                    [1, 0, 1],
                    [1, 1, 0]])
    return Network(tpm, current_state, past_state, connectivity_matrix=cm)


def s_empty():
    m = standard()
    return Subsystem((), m)


def s_single():
    m = standard()
    return Subsystem([0], m)


def subsys_n0n2():
    m = standard()
    return Subsystem((0, 2), m)


def subsys_n1n2():
    m = standard()
    return Subsystem((1, 2), m)


def s():
    m = standard()
    return Subsystem(range(m.size), m)


def s_complete():
    n = standard(cm=None)
    return Subsystem(range(n.size), n)


def noised(cm=False):
    current_state = (1, 0, 0)
    past_state = (1, 1, 0)
    tpm = np.array([[0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.8],
                    [0.7, 0.0, 1.0],
                    [1.0, 0.0, 0.0],
                    [0.2, 0.8, 0.0],
                    [1.0, 1.0, 1.0],
                    [1.0, 1.0, 0.3],
                    [0.1, 1.0, 0.0]])

    if cm is False:
        cm = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])

    cm = cm if use_connectivity_matrices else None
    return Network(tpm, current_state, past_state, connectivity_matrix=cm)


def s_noised():
    n = noised()
    return Subsystem(range(n.size), n)


def s_noised_complete():
    n = noised(cm=None)
    return Subsystem(range(n.size), n)


s_about_to_be_on = (0, 1, 1)
s_just_turned_on = (1, 0, 0)
s_all_off = (0, 0, 0)


def simple(current_state=s_all_off, past_state=s_all_off, cm=False):
    """ Simple 'AND' network.

    Diagram:

    |           +~~~~~~~+
    |    +~~~~~~+   A   |<~~~~+
    |    | +~~~>| (AND) +~~~+ |
    |    | |    +~~~~~~~+   | |
    |    | |                | |
    |    v |                v |
    |  +~+~+~~~~+      +~~~~~~+~+
    |  |   B    |<~~~~~+    C   |
    |  | (OFF)  +~~~~~>|  (OFF) |
    |  +~~~~~~~~+      +~~~~~~~~+

    TPM:

    +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
    |  Past state ~~> Current state |
    |~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~|
    |   A, B, C    |    A, B, C     |
    |~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~|
    |  {0, 0, 0}   |   {0, 0, 0}    |
    |  {0, 0, 1}   |   {0, 0, 0}    |
    |  {0, 1, 0}   |   {0, 0, 0}    |
    |  {0, 1, 1}   |   {1, 0, 0}    |
    |  {1, 0, 0}   |   {0, 0, 0}    |
    |  {1, 0, 1}   |   {0, 0, 0}    |
    |  {1, 1, 0}   |   {0, 0, 0}    |
    |  {1, 1, 1}   |   {0, 0, 0}    |
    +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
    """
    tpm = np.array([[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [1, 0, 0],
                    [0, 0, 0]])
    if cm is False:
        cm = None
    return Network(tpm, current_state, past_state, connectivity_matrix=cm)


def simple_all_off():
    return simple(s_all_off, s_all_off)


def simple_a_just_on():
    return simple(s_just_turned_on, s_about_to_be_on)


def s_subsys_all_off():
    s = simple(s_all_off, s_all_off)
    return Subsystem(range(s.size), s)


def s_subsys_all_a_just_on():
    a_about_to_be_on = (0, 1, 1)
    a_just_turned_on = (1, 0, 0)
    s = simple(a_just_turned_on, a_about_to_be_on)
    return Subsystem(range(s.size), s)


def big(cm=False):
    """Return a large network."""
    tpm = np.array([[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0],
                    [0, 0, 0, 1, 1],
                    [0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1],
                    [0, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 1, 0, 1, 1],
                    [1, 0, 0, 1, 1],
                    [1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0],
                    [1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0],
                    [1, 0, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 0, 0, 0],
                    [1, 1, 1, 0, 0],
                    [1, 1, 1, 0, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1]])
    # All on
    current_state = (1,) * 5
    # All on
    past_state = (1,) * 5
    if cm is False:
        cm = None
    return Network(tpm, current_state, past_state, connectivity_matrix=cm)


def big_subsys_all():
    """Return the subsystem associated with ``big``."""
    b = big()
    return Subsystem(range(b.size), b)


def big_subsys_all_complete():
    """Return the subsystem associated with ``big`` with all nodes
    connected."""
    b = big(cm=None)
    return Subsystem(range(b.size), b)


def big_subsys_0_thru_3():
    """Return a subsystem consisting of the first 4 nodes of ``big``."""
    b = big()
    return Subsystem(range(5)[:-1], b)


def reducible(cm=False):
    tpm = np.zeros([2] * 2 + [2])
    current_state = (0, 0)
    past_state = (0, 0)
    if cm is False:
        cm = np.array([[1, 0],
                       [0, 1]])
    r = Network(tpm, current_state, past_state, connectivity_matrix=cm)
    # Return the full subsystem
    return Subsystem(range(r.size), r)


def rule30(cm=False):
    tpm = np.array([[0, 0, 0, 0, 0],
                    [1, 1, 0, 0, 1],
                    [1, 1, 1, 0, 0],
                    [1, 0, 1, 0, 1],
                    [0, 1, 1, 1, 0],
                    [1, 0, 1, 1, 1],
                    [1, 1, 0, 1, 0],
                    [1, 0, 0, 1, 1],
                    [0, 0, 1, 1, 1],
                    [1, 1, 1, 1, 0],
                    [1, 1, 0, 1, 1],
                    [1, 0, 0, 1, 0],
                    [0, 1, 1, 0, 1],
                    [1, 0, 1, 0, 0],
                    [1, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0],
                    [1, 0, 0, 1, 1],
                    [0, 1, 0, 1, 1],
                    [0, 1, 1, 1, 1],
                    [0, 0, 1, 1, 1],
                    [1, 1, 1, 0, 1],
                    [0, 0, 1, 0, 1],
                    [0, 1, 0, 0, 1],
                    [0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 0],
                    [0, 1, 1, 1, 0],
                    [0, 1, 0, 1, 0],
                    [0, 0, 0, 1, 0],
                    [1, 1, 1, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0]])

    if cm is False:
        cm = np.array([[1, 1, 0, 0, 1],
                       [1, 1, 1, 0, 0],
                       [0, 1, 1, 1, 0],
                       [0, 0, 1, 1, 1],
                       [1, 0, 0, 1, 1]])

    all_off = (0, 0, 0, 0, 0)

    rule30 = Network(tpm, all_off, all_off, connectivity_matrix=cm)

    return Subsystem(range(rule30.size), rule30)


def trivial():
    """Single-node network with a self-loop."""

    trivial = Network(np.array([[1], [1]]), (1, ), (1, ),
                      connectivity_matrix=np.array([[1]]))

    return Subsystem(range(trivial.size), trivial)


def eight_node(cm=False):
    """Eight-node network."""

    tpm = np.array(
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 0, 0, 0, 0, 0, 1],
         [0, 1, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 0, 0, 0, 0, 0],
         [1, 0, 1, 0, 0, 0, 0, 1],
         [0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 1],
         [1, 0, 1, 0, 0, 0, 0, 0],
         [1, 1, 1, 0, 0, 0, 0, 1],
         [0, 1, 1, 1, 0, 0, 0, 0],
         [0, 1, 1, 1, 0, 0, 0, 1],
         [1, 1, 0, 1, 0, 0, 0, 0],
         [1, 0, 0, 1, 0, 0, 0, 1],
         [0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 1],
         [1, 0, 0, 1, 0, 0, 0, 0],
         [1, 1, 0, 1, 0, 0, 0, 1],
         [0, 1, 0, 1, 0, 0, 0, 0],
         [0, 1, 0, 1, 0, 0, 0, 1],
         [1, 1, 1, 1, 0, 0, 0, 0],
         [1, 0, 1, 1, 0, 0, 0, 1],
         [0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 1, 1, 1, 0, 0, 1],
         [1, 0, 1, 1, 1, 0, 0, 0],
         [1, 1, 1, 1, 1, 0, 0, 1],
         [0, 1, 1, 0, 1, 0, 0, 0],
         [0, 1, 1, 0, 1, 0, 0, 1],
         [1, 1, 0, 0, 1, 0, 0, 0],
         [1, 0, 0, 0, 1, 0, 0, 1],
         [0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 1],
         [1, 0, 0, 0, 1, 0, 0, 0],
         [1, 1, 0, 0, 1, 0, 0, 1],
         [0, 1, 0, 0, 1, 0, 0, 0],
         [0, 1, 0, 0, 1, 0, 0, 1],
         [1, 1, 1, 0, 1, 0, 0, 0],
         [1, 0, 1, 0, 1, 0, 0, 1],
         [0, 0, 1, 0, 1, 0, 0, 0],
         [0, 0, 1, 0, 1, 0, 0, 1],
         [1, 0, 1, 0, 1, 0, 0, 0],
         [1, 1, 1, 0, 1, 0, 0, 1],
         [0, 1, 1, 1, 1, 0, 0, 0],
         [0, 1, 1, 1, 1, 0, 0, 1],
         [1, 1, 0, 1, 1, 0, 0, 0],
         [1, 0, 0, 1, 1, 0, 0, 1],
         [0, 0, 0, 1, 1, 1, 0, 0],
         [0, 0, 0, 1, 1, 1, 0, 1],
         [1, 0, 0, 1, 1, 1, 0, 0],
         [1, 1, 0, 1, 1, 1, 0, 1],
         [0, 1, 0, 1, 1, 1, 0, 0],
         [0, 1, 0, 1, 1, 1, 0, 1],
         [1, 1, 1, 1, 1, 1, 0, 0],
         [1, 0, 1, 1, 1, 1, 0, 1],
         [0, 0, 1, 1, 0, 1, 0, 0],
         [0, 0, 1, 1, 0, 1, 0, 1],
         [1, 0, 1, 1, 0, 1, 0, 0],
         [1, 1, 1, 1, 0, 1, 0, 1],
         [0, 1, 1, 0, 0, 1, 0, 0],
         [0, 1, 1, 0, 0, 1, 0, 1],
         [1, 1, 0, 0, 0, 1, 0, 0],
         [1, 0, 0, 0, 0, 1, 0, 1],
         [0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 1],
         [1, 0, 0, 0, 0, 1, 0, 0],
         [1, 1, 0, 0, 0, 1, 0, 1],
         [0, 1, 0, 0, 0, 1, 0, 0],
         [0, 1, 0, 0, 0, 1, 0, 1],
         [1, 1, 1, 0, 0, 1, 0, 0],
         [1, 0, 1, 0, 0, 1, 0, 1],
         [0, 0, 1, 0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0, 1, 0, 1],
         [1, 0, 1, 0, 0, 1, 0, 0],
         [1, 1, 1, 0, 0, 1, 0, 1],
         [0, 1, 1, 1, 0, 1, 0, 0],
         [0, 1, 1, 1, 0, 1, 0, 1],
         [1, 1, 0, 1, 0, 1, 0, 0],
         [1, 0, 0, 1, 0, 1, 0, 1],
         [0, 0, 0, 1, 0, 1, 0, 0],
         [0, 0, 0, 1, 0, 1, 0, 1],
         [1, 0, 0, 1, 0, 1, 0, 0],
         [1, 1, 0, 1, 0, 1, 0, 1],
         [0, 1, 0, 1, 0, 1, 0, 0],
         [0, 1, 0, 1, 0, 1, 0, 1],
         [1, 1, 1, 1, 0, 1, 0, 0],
         [1, 0, 1, 1, 0, 1, 0, 1],
         [0, 0, 1, 1, 1, 1, 0, 0],
         [0, 0, 1, 1, 1, 1, 0, 1],
         [1, 0, 1, 1, 1, 1, 0, 0],
         [1, 1, 1, 1, 1, 1, 0, 1],
         [0, 1, 1, 0, 1, 1, 0, 0],
         [0, 1, 1, 0, 1, 1, 0, 1],
         [1, 1, 0, 0, 1, 1, 0, 0],
         [1, 0, 0, 0, 1, 1, 0, 1],
         [0, 0, 0, 0, 1, 1, 1, 0],
         [0, 0, 0, 0, 1, 1, 1, 1],
         [1, 0, 0, 0, 1, 1, 1, 0],
         [1, 1, 0, 0, 1, 1, 1, 1],
         [0, 1, 0, 0, 1, 1, 1, 0],
         [0, 1, 0, 0, 1, 1, 1, 1],
         [1, 1, 1, 0, 1, 1, 1, 0],
         [1, 0, 1, 0, 1, 1, 1, 1],
         [0, 0, 1, 0, 1, 1, 1, 0],
         [0, 0, 1, 0, 1, 1, 1, 1],
         [1, 0, 1, 0, 1, 1, 1, 0],
         [1, 1, 1, 0, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 0, 1, 1, 1, 1, 0],
         [1, 0, 0, 1, 1, 1, 1, 1],
         [0, 0, 0, 1, 1, 0, 1, 0],
         [0, 0, 0, 1, 1, 0, 1, 1],
         [1, 0, 0, 1, 1, 0, 1, 0],
         [1, 1, 0, 1, 1, 0, 1, 1],
         [0, 1, 0, 1, 1, 0, 1, 0],
         [0, 1, 0, 1, 1, 0, 1, 1],
         [1, 1, 1, 1, 1, 0, 1, 0],
         [1, 0, 1, 1, 1, 0, 1, 1],
         [0, 0, 1, 1, 0, 0, 1, 0],
         [0, 0, 1, 1, 0, 0, 1, 1],
         [1, 0, 1, 1, 0, 0, 1, 0],
         [1, 1, 1, 1, 0, 0, 1, 1],
         [0, 1, 1, 0, 0, 0, 1, 0],
         [0, 1, 1, 0, 0, 0, 1, 1],
         [1, 1, 0, 0, 0, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 1, 1],
         [0, 0, 0, 0, 0, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0, 0, 1, 0],
         [0, 1, 0, 0, 0, 0, 1, 1],
         [0, 1, 0, 0, 0, 0, 1, 0],
         [1, 1, 0, 0, 0, 0, 1, 1],
         [1, 1, 1, 0, 0, 0, 1, 0],
         [0, 0, 1, 0, 0, 0, 1, 1],
         [0, 0, 1, 0, 0, 0, 1, 0],
         [1, 0, 1, 0, 0, 0, 1, 1],
         [1, 0, 1, 0, 0, 0, 1, 0],
         [0, 1, 1, 0, 0, 0, 1, 1],
         [0, 1, 1, 1, 0, 0, 1, 0],
         [1, 1, 1, 1, 0, 0, 1, 1],
         [1, 1, 0, 1, 0, 0, 1, 0],
         [0, 0, 0, 1, 0, 0, 1, 1],
         [0, 0, 0, 1, 0, 0, 1, 0],
         [1, 0, 0, 1, 0, 0, 1, 1],
         [1, 0, 0, 1, 0, 0, 1, 0],
         [0, 1, 0, 1, 0, 0, 1, 1],
         [0, 1, 0, 1, 0, 0, 1, 0],
         [1, 1, 0, 1, 0, 0, 1, 1],
         [1, 1, 1, 1, 0, 0, 1, 0],
         [0, 0, 1, 1, 0, 0, 1, 1],
         [0, 0, 1, 1, 1, 0, 1, 0],
         [1, 0, 1, 1, 1, 0, 1, 1],
         [1, 0, 1, 1, 1, 0, 1, 0],
         [0, 1, 1, 1, 1, 0, 1, 1],
         [0, 1, 1, 0, 1, 0, 1, 0],
         [1, 1, 1, 0, 1, 0, 1, 1],
         [1, 1, 0, 0, 1, 0, 1, 0],
         [0, 0, 0, 0, 1, 0, 1, 1],
         [0, 0, 0, 0, 1, 0, 1, 0],
         [1, 0, 0, 0, 1, 0, 1, 1],
         [1, 0, 0, 0, 1, 0, 1, 0],
         [0, 1, 0, 0, 1, 0, 1, 1],
         [0, 1, 0, 0, 1, 0, 1, 0],
         [1, 1, 0, 0, 1, 0, 1, 1],
         [1, 1, 1, 0, 1, 0, 1, 0],
         [0, 0, 1, 0, 1, 0, 1, 1],
         [0, 0, 1, 0, 1, 0, 1, 0],
         [1, 0, 1, 0, 1, 0, 1, 1],
         [1, 0, 1, 0, 1, 0, 1, 0],
         [0, 1, 1, 0, 1, 0, 1, 1],
         [0, 1, 1, 1, 1, 0, 1, 0],
         [1, 1, 1, 1, 1, 0, 1, 1],
         [1, 1, 0, 1, 1, 0, 1, 0],
         [0, 0, 0, 1, 1, 0, 1, 1],
         [0, 0, 0, 1, 1, 1, 1, 0],
         [1, 0, 0, 1, 1, 1, 1, 1],
         [1, 0, 0, 1, 1, 1, 1, 0],
         [0, 1, 0, 1, 1, 1, 1, 1],
         [0, 1, 0, 1, 1, 1, 1, 0],
         [1, 1, 0, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 1, 1, 1, 1, 1, 1],
         [0, 0, 1, 1, 0, 1, 1, 0],
         [1, 0, 1, 1, 0, 1, 1, 1],
         [1, 0, 1, 1, 0, 1, 1, 0],
         [0, 1, 1, 1, 0, 1, 1, 1],
         [0, 1, 1, 0, 0, 1, 1, 0],
         [1, 1, 1, 0, 0, 1, 1, 1],
         [1, 1, 0, 0, 0, 1, 1, 0],
         [0, 0, 0, 0, 0, 1, 1, 1],
         [0, 0, 0, 0, 0, 1, 1, 1],
         [1, 0, 0, 0, 0, 1, 1, 0],
         [1, 0, 0, 0, 0, 1, 1, 1],
         [0, 1, 0, 0, 0, 1, 1, 0],
         [0, 1, 0, 0, 0, 1, 1, 1],
         [1, 1, 0, 0, 0, 1, 1, 0],
         [1, 1, 1, 0, 0, 1, 1, 1],
         [0, 0, 1, 0, 0, 1, 1, 0],
         [0, 0, 1, 0, 0, 1, 1, 1],
         [1, 0, 1, 0, 0, 1, 1, 0],
         [1, 0, 1, 0, 0, 1, 1, 1],
         [0, 1, 1, 0, 0, 1, 1, 0],
         [0, 1, 1, 1, 0, 1, 1, 1],
         [1, 1, 1, 1, 0, 1, 1, 0],
         [1, 1, 0, 1, 0, 1, 1, 1],
         [0, 0, 0, 1, 0, 1, 1, 0],
         [0, 0, 0, 1, 0, 1, 1, 1],
         [1, 0, 0, 1, 0, 1, 1, 0],
         [1, 0, 0, 1, 0, 1, 1, 1],
         [0, 1, 0, 1, 0, 1, 1, 0],
         [0, 1, 0, 1, 0, 1, 1, 1],
         [1, 1, 0, 1, 0, 1, 1, 0],
         [1, 1, 1, 1, 0, 1, 1, 1],
         [0, 0, 1, 1, 0, 1, 1, 0],
         [0, 0, 1, 1, 1, 1, 1, 1],
         [1, 0, 1, 1, 1, 1, 1, 0],
         [1, 0, 1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 0, 1, 1, 1, 1],
         [1, 1, 1, 0, 1, 1, 1, 0],
         [1, 1, 0, 0, 1, 1, 1, 1],
         [0, 0, 0, 0, 1, 1, 1, 0],
         [0, 0, 0, 0, 1, 1, 0, 1],
         [1, 0, 0, 0, 1, 1, 0, 0],
         [1, 0, 0, 0, 1, 1, 0, 1],
         [0, 1, 0, 0, 1, 1, 0, 0],
         [0, 1, 0, 0, 1, 1, 0, 1],
         [1, 1, 0, 0, 1, 1, 0, 0],
         [1, 1, 1, 0, 1, 1, 0, 1],
         [0, 0, 1, 0, 1, 1, 0, 0],
         [0, 0, 1, 0, 1, 1, 0, 1],
         [1, 0, 1, 0, 1, 1, 0, 0],
         [1, 0, 1, 0, 1, 1, 0, 1],
         [0, 1, 1, 0, 1, 1, 0, 0],
         [0, 1, 1, 1, 1, 1, 0, 1],
         [1, 1, 1, 1, 1, 1, 0, 0],
         [1, 1, 0, 1, 1, 1, 0, 1],
         [0, 0, 0, 1, 1, 1, 0, 0],
         [0, 0, 0, 1, 1, 0, 0, 1],
         [1, 0, 0, 1, 1, 0, 0, 0],
         [1, 0, 0, 1, 1, 0, 0, 1],
         [0, 1, 0, 1, 1, 0, 0, 0],
         [0, 1, 0, 1, 1, 0, 0, 1],
         [1, 1, 0, 1, 1, 0, 0, 0],
         [1, 1, 1, 1, 1, 0, 0, 1],
         [0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0, 1],
         [1, 0, 1, 1, 0, 0, 0, 0],
         [1, 0, 1, 1, 0, 0, 0, 1],
         [0, 1, 1, 1, 0, 0, 0, 0],
         [0, 1, 1, 0, 0, 0, 0, 1],
         [1, 1, 1, 0, 0, 0, 0, 0],
         [1, 1, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0]]
    )
    if cm is False:
        cm = np.array(
            [[1, 1, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 1, 1]]
        )

    current_state = tuple([0] * 8)
    past_state = tuple([0] * 8)

    return Network(tpm, current_state, past_state, connectivity_matrix=cm)


def eights():
    net = eight_node()
    return Subsystem(range(net.size), net)


def eights_complete():
    net = eight_node(cm=None)
    return Subsystem(range(net.size), net)


def eight_node_sbs(cm=False):
    tpm = [[1] + ([0] * 255)] * 256
    if cm is False:
        cm = np.array(
            [[1, 1, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 1, 1]]
        )

    current_state = tuple([0] * 8)
    past_state = tuple([0] * 8)

    return Network(tpm, current_state, past_state, connectivity_matrix=cm)


def rule152(cm=False):
    tpm = np.array(
        [[0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0],
         [0, 0, 1, 0, 0],
         [1, 0, 1, 0, 0],
         [0, 0, 0, 1, 0],
         [0, 0, 0, 1, 0],
         [0, 1, 0, 1, 0],
         [1, 1, 0, 1, 0],
         [0, 0, 0, 0, 1],
         [0, 1, 0, 0, 0],
         [0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0],
         [0, 0, 1, 0, 1],
         [0, 0, 1, 0, 0],
         [0, 1, 1, 0, 1],
         [1, 1, 1, 0, 0],
         [1, 0, 0, 0, 0],
         [0, 1, 0, 0, 1],
         [0, 0, 1, 0, 0],
         [1, 0, 1, 0, 1],
         [1, 0, 0, 0, 0],
         [0, 0, 0, 0, 1],
         [0, 1, 0, 0, 0],
         [1, 1, 0, 0, 1],
         [1, 0, 0, 1, 0],
         [0, 1, 0, 1, 1],
         [0, 0, 0, 1, 0],
         [1, 0, 0, 1, 1],
         [1, 0, 1, 1, 0],
         [0, 0, 1, 1, 1],
         [0, 1, 1, 1, 0],
         [1, 1, 1, 1, 1]]
    )
    if cm is False:
        cm = np.array(
            [[1, 1, 0, 0, 1],
             [1, 1, 1, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 0, 1, 1, 1],
             [1, 0, 0, 1, 1]]
        )

    current_state = tuple([0] * 5)
    past_state = tuple([0] * 5)

    return Network(tpm, current_state, past_state, connectivity_matrix=cm)


def rule152_s():
    net = rule152()
    return Subsystem(range(net.size), net)


def rule152_s_complete():
    net = rule152(cm=None)
    return Subsystem(range(net.size), net)
