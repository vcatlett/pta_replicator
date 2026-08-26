*********************************
The Gravitational Wave Background
*********************************

We can model the GWB as a sum of the gradients and curls of spherical harmonics :math:`Y_{lm}` starting with :math:`l=2`. (:math:`l=0` would just add a constant value, and :math:`l=1` would imply a preferred direction.)
Modeling the GWB as gradient and curl modes as in :cite:t:`Gair-2014` allows one to probe the GWB with no assumptions. However, PTAs are only sensitive to the gradient modes, no matter how many pulsars you add.

For a given :math:`N_p`, a PTA is sensitive to :math:`2N_p` components of the GWB (:math:`l_{max}=4` requires :math:`N_p=21`, :math:`l_{max}=10` requires :math:`N_p=100`) :math:.

For the GWB, we define

* :math:`v_{ph}` is the GW phase velocity. Default to :math:`v_{ph}=1` unless dealing with modified GR (in that case, watch out for numerical singularities)
* :math:`e_{ij}^{+}(\hat{k})=\hat{l}_{a}\hat{l}_{b}-\hat{m}_{a}\hat{m}_{b}` is the polarization tensor of the :math:`+` mode for a given :math:`\hat{k}` (Eq. 16 of :cite:t:`Gair-2014`)
* :math:`e_{ij}^{\times}(\hat{k})=\hat{l}_{a}\hat{m}_{b}+\hat{m}_{a}\hat{l}_{b}` is the polarization tensor of the :math:`\times` mode for a given :math:`\hat{k}` (Eq. 16 of :cite:t:`Gair-2014`)

For a given mode :math:`A \in \{+, \times\}` (or others for modified theories), a given source :math:`a`, and given direction :math:`\hat{n}`, Equation 5 of :cite:t:`Cordes-2025` defines the antenna response function (or "detector pattern function") as

.. math::

    F_{a}^{A}(\hat{k}) = \frac{1}{2} \left( \frac{u_a^i u_a^j}{1+\hat{k} \cdot \hat{u}_a / v_{ph}} \right) e_{ij}^{A}(\hat{k})

That's an equation that can cause numerical issues if :math:`v_{ph} \neq 1`, which is discussed in :cite:t:`Cordes-2025`. Equation 68 of :cite:t:`Gair-2014` is similar except that there is no :math:`v_{ph}` in the denominator (as it sets :math:`v_{ph}=1`).

For an isotropic, stationary, Gaussian, unpolarized GWB, the (dimensionless) GW amplitude is given by (Equation 14 of :cite:t:`Chamberlin-2015`)

.. math::

    h_{c}(f) = A_{GWB} \left( \frac{f}{f_{yr}} \right)^{\alpha}


If the power spectrum is one-sided, then the spectrum is given by (Equation 17 of :cite:t:`Chamberlin-2015`)

.. math::

    \Omega_{GWB}(f)
    =
    \left( \frac{2 \pi^2}{3H_{0}^{2}} \right)
    A_{GWB}^2 f^2 \left( \frac{f}{f_{yr}} \right)^{2\alpha}
