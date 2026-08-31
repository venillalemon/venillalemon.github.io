# Linear PCP and Recursive SNARKs

*February 4, 2026*

## Linear PCP-based SNARK

Here is another paradigm for SNARKs: a cryptographic tool and a linear PCP builds a SNARK system. Before IOP and PCS paradigm was put forward, the main paradigm is PCP, e.g. Kilian’92 and Micali’00 is PCP+Merkle tree; IKO’07 is linear PCP; GGPR’13 uses QAP as linear PCP.

### Quadratic Arithmetic Program (QAP)

QAP is another method to encode a circuit into a polynomial. Recall that in the first IOP for circuit SAT, we label each gate with a bitstring, and the satisfying value is encoded into a multilinear polynomial on the hypercube (interpolated to $\mathbb{F}_p^n$ ). In PLONK, we label each wire with an integer, and the satisfying value is encoded into a univariate polynomial on the roots of unity.

QAP labels all the input and output of all multiplicative gates. We label each gate with integers in $[n]$  and each wire (except output wires of additive gate) with integers in $[m]$ . The value of wire $i$  is $c_i$ . Then we define $l_i(x)$  by $l_i(\omega^j)=1,\omega^n=1$ , iff $c_i$  is the left input of the gate $j$ ; and the same as $r_i(x)$ , $o_i(x)$  for the right input and output.

Note that we say $i$  is the left input of gate $j$  also if $i$  passes several additive gates before it is the left input of gate $j$ . Then we have: the value on the circuit is proper iff

$$
\left.V(x)=\prod_{i\in[n]}(x-\omega^i)\;\middle|\;L(x)R(x)-O(x)\right.
$$

where

$$
L_{\mathbf{c}}(x)=\sum_{i\in[m]}c_il_i(x),R_{\mathbf{c}}(x)=\sum_{i\in[m]}c_ir_i(x),O_{\mathbf{c}}(x)=\sum_{i\in[m]}c_io_i(x)
$$

exactly encodes the left-input, right-input and output of gate $j$  with $L_{\mathbf{c}}(\omega^j)$ , $R_{\mathbf{c}}(\omega^j)$ , and $O_{\mathbf{c}}(\omega^j)$ .

Thus, the statement that $P$  knows $w$  such that $C(x,w)=0$  holds iff $P$  knows a vector $\mathbf{c}$  such that $L_{\mathbf{c}}(x)R_{\mathbf{c}}(x)-O_{\mathbf{c}}(x)=q(x)\prod_{i\in[n]}(x-\omega^i)=q(x)V(x)$ .

### Constructing SNARK: [PGHR13] and [Groth16]

The global parameter is $gp=\left(\left(g^{\tau^i}\right)_{i\in[n]},\left(g^{l_i(\tau)}\right)_{i\in[m]},\left(g^{r_i(\tau)}\right)_{i\in[m]},\left(g^{o_i(\tau)}\right)_{i\in[m]},g^{q(\tau)}\right)$  where $\tau$  is a random element (later deleted) in $\mathbb{F}_p$ .

With KZG in our hands, we reach to a simple protocol: The prover can compute $\pi_l=g^{L_{\mathbf{c}}(\tau)}$ , $\pi_r=g^{R_{\mathbf{c}}(\tau)}$ , $\pi_o=g^{O_{\mathbf{c}}(\tau)}$ , and $\pi=g^{q(\tau)}$  by homomorphically combining the global parameters. The verifier checks if $e(\pi_l,\pi_r)=e(\pi_o,g) e(\pi,g^{V(\tau)})$ .

However, the protocol is far from the real protocol.

### Problem 1: How to make sure that $\pi_l$  is computed from $g^{l_i(\tau)}$ ?

**KoE Assumption.** We use $gp=(g^{l_i(\tau)},g^{\alpha l_i(\tau)})^{i\in[m]}$ . If the prover can compute $\pi_1=g^{\sum_ic_il_i(\tau)}$  and $\pi_2=g^{\alpha \sum_ic_il_i(\tau)}$  without knowing $\alpha$ , then there is an extractor that can extract $c_i$ ’s from the prover. The Pinocchio [PGHR13] uses KoE assumption.

**GGM Assumption.** Any prover can only compute linear combinations of $g^{l_i(\tau)}$ ’s, i.e., if the prover can compute $\pi=g^{\sum_ic_il_i(\tau)}$ , then it must know every $c_i$ . [Groth16] uses GGM assumption.

### Problem 2: How to make sure every $\pi$  share the same $c_i$ ’s?

We use another random $\beta$  for setup (also deleted after setup). We add $g^{\beta(l_i(\tau)+r_i(\tau)+o_i(\tau))}$  and $g^{\beta}$  to the global parameters.

### Problem 3: How to handle the public input and the expected output?

Recall that all the wires except the output of add gates are labelled. So the input wire and output wire (if not labelled, add a multiply $1$  gate) are labelled with $I_{io}$ . The idea is to split $L_{\mathbf{c}}$  apart, and let verifier compute $\sum_{i\in I_{io}}c_il_i(x)$ .

### Analysis

- Setup: $O(n)$  group exps, since there is a unique $j$  that makes $l_i(\omega^j)=1$ , if we label different wires with a same output gate with different labels.

- Prover: $O(n\log n)$  for NTT. The prover computes the values of polynomial $q$  on the unity set $\langle\omega\rangle$  and uses NTT to get its coefficients. Only with coefficients can the prover compute $g^{q(\tau)}$ . Also, $O(n)$  group exps.

- Proof size: $O(1)$

- Verifier: $O(1)$  for pairing, $O(|I_{io}|)$  group exps.

## Recursive SNARKs

Recall if the circuit size is $n$ :

- Pinocchio and Groth16: prover time $O(n\log n)$  and proof size $O(1)$

- PLONK-KZG: prover time $O(n\log n)$  (every gadgets the prover should compute NTT) and proof size $O(1)$

- FRI-based: prover time and proof size $O(\log^2 n)$

How can we achieve the better one in both prover time and proof size? The recursive proof provides a “proof of proof”. Let the inner system be $(S,P,V)$ , which proves that the prover knows the $w$  such that $C(x,w)=1$ . Suppose that the prover and verifier $P$  and $V$  is fast but the proof $\pi$  is long, the idea is to construct another proof system $(S^\prime,P^\prime,V^\prime)$  proving that the prover knows the $\pi$  such that $V(vp,x,\pi)=1$ . This outer system has slower prover, but since the verifier $V$  is fast, the circuit of $V$  is much smaller than that of the original $C$ . So the outer prover $P^\prime$  is not so slow, as we expected.

A simple argument shows that if $(S,P,V)$  and $(S^\prime,P^\prime,V^\prime)$  are both knowledge sound, then the integrated proof system is also knowledge sound. The idea of proof is to regard the extractor $E^\prime$  as a malicious prover of $(S,P,V)$ . The probability gap is the sum of those of the original prove systems, thus negligible.

### Application 1: incrementally verifiable computation

Suppose that a computation $F$  is applied to initial state $s_0$  recursively, each round takes an input $w_i$ . The prover wants to prove that it knows the $w_i$  ’s such that each computation step is correct. The verifier wants to verify that after $n$  steps, the state $s_0$  eventually becomes $s_n$ . (TODO)

### Application 2: streaming proof generation

Suppose there is a bunch of transactions to be proved. We need not wait the transactions all to take place; rather, we generate proofs on every arrival of batches. For example if the batch size is $1$ , first $\pi_1$  proves the prover knows $w_1$  that $C(x_1,w_1)=0$ ; then $\pi_2$  proves that the prover knows $w_2$  such that $C(x_2,w_2)=0$ . Then a proof is generated to prove that the prover knows $\pi_1,\pi_2,\dots$  such that the verifier accepts them all.

### Construction: alternating groups

Recall in KZG, the public parameter is a tuple $(p,G,q,g,e)$ , where $G$  is a group of order $p$  with $g$  its generator. And in this section, we regard the verifier algorithm as a circuit, so we had better embed $G$  into some vector space over $\mathbb{F}_q$ .

> **Definition (Algebraic Groups).** Group $G\leq\mathbb{F}_q^\ell$  is an algebraic group if and only if
>
> - there are polynomials $f_1,\dots,f_\ell\in\mathbb{F}_q[X^\ell]$  such that for all $a,b\in G$ , $a+b=\left(f_1(a,b),\dots,f_\ell(a,b)\right)$ ;
>
> - there is an efficient algorithm testing if $a=b$ .

Can we make $|G|=p$  a subgroup of $\mathbb{F}_p^\ell$ ? No, because the discrete log is trivial in such groups. Take **Smart Attack** in the anomalous curve for an example.

The idea is to construct a group chain that: $|G_1|=p$ , $G_1<\mathbb{F}_q^\ell$ ; $|G_2|=q$ , $G_2<\mathbb{F}_r^\ell$ . The original circuit $C$  is over $\mathbb{F}_p$ . The KZG PCS will help us understand this recursive SNARK, because in that scheme, an exponentiation embeds every elements in $\mathbb{F}_p$  into $G_1<\mathbb{F}_q^\ell$ . Now that $V$  is a circuit over $\mathbb{F}_q$ , the proof that the prover $P^\prime$  knows a proof $\pi_1$  involves group arithmetic on $\mathbb{F}_q$ . Since $G_2$  has order $q$ , then $P^\prime$  sends a proof in $G_2$ .

However it is inefficient to have two pairing groups. For one pairing group and another non-pairing group, we can use KZG for one and bulletproofs for the other. The Halo is based on two non-pairing groups, i.e. elliptic group $E(\mathbb{F}_p)$  and $E(\mathbb{F}_q)$  of the elliptic curve $y^2=x^3+5$ . Details [https://eprint.iacr.org/2019/1021.pdf](https://eprint.iacr.org/2019/1021.pdf)

### Construction: folding

Another idea is homomorphic commitment, which we can compute a commitment of an addition simply by adding the commitments. We use this to prove two circuits at once (generate one proof for the two circuits). More precisely, all circuits can be written in R1CS form $(Az)\circ(Bz)=Dz$ . An idea to prove two instance $z_1 = (x_1, w_1),z_2 = (x_2, w_2)$  of the same R1CS at one time is to randomly choose an $r$  and prove for some R1CS, the combination $z_1+rz_2$  is feasible. However, we cannot have $(Az_1+rAz_2)\circ(Bz_1+rBz_2)=D(z_1+rz_2)$  if $z_1,z_2$  are feasible inputs. Thus we turn to modify the definition and put forward **Relaxed R1CS**.

## HW

- ❎ Knowledge soundness is a meaningful notion when a prover claims that there are no satisfying assignments to a system of constraints

- ❎ Knowledge soundness is a meaningful notion for the sumcheck protocol

- ✅ Knowledge soundness (as defined in lecture 2) implies soundness

- ❎ Non-interactive implies publicly verifiable

- ❎ Vector commitments are as expressive as polynomial commitments

- ✅ Polynomial extensions are distance amplifying encodings

- ✅ Multivariate polynomial encoding reduces the total degree by an exponential factor compared to univariate polynomial encoding

- ✅ The verifier in the sum-check protocol is oblivious to the polynomial g whose evaluations are being summed until the last step

- ❎ The uniqueness of multilinear extensions is crucial for the soundness of the sumcheck protocol

- ❎ The claim f(x) = g(x) for all k-bit inputs, where f and g are low degree polynomials over a large field, can be reduced to the following sumcheck claim: _{x ^k} (f(x)-g(x)) = 0

- ❎ The polynomial IOP for SAT (from lecture 4) can be transformed into a SNARK with verifier complexity independent of circuit size

- ✅ The polynomial IOP for SAT (from lecture 4) has optimal prover complexity

- ✅ Extending the polynomial IOP for SAT in the natural way to support gates with n inputs will result in a sumcheck protocol over (n+1) * logS variables

verkle trees
