************
Introduction
************

One approach to simulating the GWB is to generate the GW from individual sources, then sum them, which is what ``holodeck`` can do.
However, this can be quite computationally expensive, so to save time, one may simulate a GWB statistically. The general set of steps for doing so, which I've primarily derived from Section IV of \cite{Chamberlin-2015}, are as follows:

* Load the sources
* Zero out the residuals of the sources
* Define a set of equally-spaced observation times spanning the overall minimum and maximum time of the data plus a pad on either side (like 1 day)
* Define a set of frequencies ranging from DC (constant, :math:`f_{DC}=0`) to Nyquist (:math:`f_{nyq}=\frac{1}{2\delta t}`).
* Compute the ORF
* Use Cholesky transform to take "square root" of ORF
* The GWB power spectrum
* Timing residuals
