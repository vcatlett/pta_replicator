*********************
Astrophysical Sources
*********************

``pta_replicator`` stores each pulsar as a `SimulatedPulsar` object.

In general, when simulating a combined PTA and astrometric detector, we will have

* :math:`N_p` is the number of pulsars
* :math:`N_{*}` is the number of stars
* :math:`N = N_p + N_{*}` is the total number of sources

For a single source, we have

* :math:`L` is the distance to the source
* :math:`\hat{u}` is a unit vector pointing to the source

For a pair of sources denoted by :math:`a` and :math:`b`, we define their angular separation :math:`\zeta_{ab}` as

.. math::

    \zeta_{ab} &= \mathrm{arccos} \left[ \hat{u}_a \cdot \hat{u}_b \right]
    \\
    &= \mathrm{arccos} \left[  \mathrm{sin}(\theta_a) \mathrm{sin}(\theta_b) + \ \mathrm{cos}(\theta_a) \mathrm{cos}(\theta_b) \mathrm{cos}(\phi_a - \phi_b) \right]
    \\

.. warning::

    `pta_replicator.spharmORFbasis.calczeta()` uses a different formula that seems to have the sin and cos terms flipped. What's up with that?
