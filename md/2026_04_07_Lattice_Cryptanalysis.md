# Lattice Cryptanalysis

*April 7, 2026*

## Lattice-Based Signatures: Hash-and-Sign, Fiat-Shamir

### Trapdoors for hard lattices and new cryptographic constructions

[[GPV08]](https://eprint.iacr.org/2007/432)

First showed how to solve DGS in polynomial time for large parameters.

The sampling algorithm itself is actually a simple randomized variant of Babai’s nearest-plane algorithm [Bab86], which was originally proposed by Klein [Kle00] in another context.

The early GGH signature proposal of Goldreich, Goldwasser, and Halevi [GGH97] was directly related to a certain lattice problem, but it lacked a security proof, and recently, Nguyen and Regev [NR06] showed how to recover the entire secret key (or its equivalent) from a transcript of signatures.

So the paper proposes a Hash-and-Sign / Identity-Based Encryption based on **Preimage Sampleable Functions (PSF).**

Below is the signature scheme based on lattice trapdoors. Here TrapGen generates a trapdoor function and its trapdoor $(f_a,t)$; SampleDom outputs $x$ randomly such that $f_a(x)$ is uniform; SamplePre receives $y$ and outputs $x$ according to the conditional distribution $x\leftarrow \mathrm{SampleDom}()\mid f_a(x)=y$.

The PSF is realized by $(f_A,T)$ be the function-trapdoor pair, with $f_A(x)=Ax\bmod q$ and $T$ be a good basis. The inverse $\mathrm{SampleISIS}(A,T,s,u)$ first computes $At=u\bmod q$ by linear algebra methods; then sample $v\sim D_{\Lambda^\bot(A),s,-t}$ using Gaussian sampler w.r.t basis $T$.

[![](/images/LC/image.png)](/images/LC/image.png)

This is the Hash-and-Sign regime, where we first hash the message, then use the trapdoor to sample a preimage as the signature. The verification only computes the trapdoor function.

GGH signature: pk=basis $B$, sk=a good basis $T$; signature= $v$ the closest vector of $H(m)$

So by signing a large amount of messages, the attacker can see the parallelpipe by collecting $H(m)-v$. [GPV08] avoids the weakness of GGH to generate within a range of close vectors of $H(m)$.

Additionally, GPV08 provides a sampling algorithm as follows:

[![](/images/LC/image1.png)](/images/LC/image1.png)[![](/images/LC/image2.png)](/images/LC/image2.png)

This algorithm only adjusts a little from Babai’s nearest-plane algorithm.

A following work [[PT26]](https://eprint.iacr.org/2026/1208.pdf) extends this construction without Gaussian sampling.

### **Lattice Signatures Without Trapdoors**

[[Lyu12]](https://eprint.iacr.org/2011/537)

Fiat-Shamir with abort, which is a new method other then [GPV08]’s Hash-and-Sign.

In Quorus: Essentially all prior works on lattice-based threshold signatures based on the Fiat-Shamir transform either rely on threshold homomorphic encryption or attempted to leverage the similarities between Lyubashevsky-like signatures [Lyu12] and Schnorr.

### Solving the Shortest Vector Problem in $2^n$ Time via Discrete Gaussian Sampling

[[ADRS14]](https://arxiv.org/pdf/1412.7994)

Solve SVP through SIS and reduce variance during each sampling/sieving

### Classical Hardness of Learning with Errors

[[BLP+13]](https://arxiv.org/pdf/1306.0281)

A concrete Gaussian sampler with relatively large variance

### Lattice-Based Identification Schemes Secure Under Active Attacks

[[Lyu08]](https://cseweb.ucsd.edu/~vlyubash/papers/idlatticeconf.pdf)

The first signature with rejection sampling for ID scheme

[![](/images/LC/image3.png)](/images/LC/image3.png)

The paper also includes lemmas from [[Reg05]](https://cims.nyu.edu/~regev/papers/average.pdf):

[![](/images/LC/image4.png)](/images/LC/image4.png)[![](/images/LC/image5.png)](/images/LC/image5.png)

and from [[LM06]](https://cseweb.ucsd.edu/~vlyubash/papers/generalknapsackfull.pdf):

[![](/images/LC/image6.png)](/images/LC/image6.png)

[![](/images/LC/image7.png)](/images/LC/image7.png)[![](/images/LC/image8.png)](/images/LC/image8.png)

## Ideal Lattices

### Generalized compact knapsacks, cyclic lattices, and efficient one-way functions

[[Micciancio02]](https://cseweb.ucsd.edu/~daniele/papers/Cyclic.pdf) OWF using cyclic lattices (ideal lattices are extension of them)

### Generalized Compact Knapsacks Are Collision Resistant

[[LM06]](https://cseweb.ucsd.edu/~vlyubash/papers/generalknapsackfull.pdf) Lyubashevsky & Micciancio

Ideal lattices were first studied in the context of cryptography in it, concerning worst-case to average-case reduction. Here is the main theorem, formulated in [[Lyu08]](https://cseweb.ucsd.edu/~vlyubash/papers/idlatticeconf.pdf):

**Theorem 2.** For integer $m = \lceil 4n \log n \rceil$ and some integer $p = \tilde{O}(n^3)$, if there exists a polynomial-time algorithm that solves $\mathrm{SIS}(A)$ for uniformly random $A \in \operatorname{ROT}(n, m, p)$, then SIVP (and also SVP) can be approximated in polynomial time to within a factor of $\tilde{O}(n^2)$ in every $n$ -dimensional lattice corresponding to an ideal in $\mathbb{Z}[x] / \langle x^n + 1 \rangle$.

### On Ideal Lattices and Learning with Errors Over Rings

[[LPR12]](https://eprint.iacr.org/2012/230.pdf) Lyubashevsky, Peikert, Regev
