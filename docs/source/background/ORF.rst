************************************
The Overlap Reduction Function (ORF)
************************************

The ORF is a two-point correlation function that quantifies the correlated response of two sources due to the GWB.

Uncorrelated
------------

If the ORF is fully uncorrelated, the matrix is just the identity. If the PTA and astrometric components are not correlated, then the off-diagonal blocks are all zeros.

The PTA ORF
-----------

For each pair of pulsars (where :math:`\zeta_{aa}=0` for a pair that's the same pulsar, that is, :math:`a=b`), compute the ORF :math:`\Gamma_{ab}(\zeta_{ab}, f)` for each frequency :math:`f` you care about.

In general, the ORF is given by

.. math::
    \kappa_{ab}(f, \hat{k}) &=
    \left[1 - e^{-2\pi i f L_a (1+\hat{k}\cdot\hat{u_a}/v_{ph})}\right]
    \left[1 - e^{2\pi i f L_b (1+\hat{k}\cdot\hat{u_b}/v_{ph})}\right]
    \\
    \Gamma_{ab}(\zeta_{ab}, f)
    &=
    \frac{3}{8\pi} \int d^2 \hat{k} \ \kappa_{ab}(f, \hat{k}) \ \sum_{A} F_a^{A}(\hat{n})F_b^{A}(\hat{n})

For a statistically isotopic background, :cite:t:`Gair-2014` uses clever math (rotating the frame so one pulsar is on the z-axis) to show that we only need Legendre polynomials :math:`P_l` for the ORF, yielding

.. math::
    \Gamma_{ab}(\zeta_{ab}, f)
    &=
    \frac{1}{(2\pi f)^2} \sum_{l=2}^{\infty}
    C_l(N_l)^2 (2l + 1) \pi P_l(\mathrm{cos}(\zeta_{ab}))
    \\
    &=
    \frac{\pi}{4 f^2} \sum_{l=2}^{\infty}
    C_l(N_l)^2 (2l + 1) P_l(\mathrm{cos}(\zeta_{ab}))

where (Eq. 6 of :cite:t:`Gair-2014`)

.. math::

    N_l = \sqrt{\frac{2(l-2)!}{(l+2)!}}

Equation 15 of :cite:t:`Cordes-2025` writes this instead as

.. math::

    \Gamma_{ab}(\zeta_{ab}, f)
    &=
    \sum_{l=2}^{\infty}
    b_l(f) P_l(\mathrm{cos}(\zeta_{ab}))
    \\
    b_l(f)
    &=
    \frac{3}{32}(2l+1)\frac{(l-2)!}{(l+2)!}|c_l(f)|^2

which may be more useful for a computational approach where users can vary the coefficients. In these simulations, a user will provide an :math:`l_{max}` (since we cannot do an infinite sum) as well as the coefficients :math:`C_l` (or :math:`b_l`) for each :math:`l` mode.
In the caption of its Figure 4, :cite:t:`Gair-2014` states that :math:`l_{max}=4` tends to be sufficient to recover the HD curve.

More complicated GWBs require a sum over :math:`Y_{lm}`'s, so a simulation code should require that flexibility in ORF definition.

The Astrometry ORF
------------------

idk dawg
