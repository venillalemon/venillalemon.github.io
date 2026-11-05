# AND Triple Generation: Half-Gate and FKOS

*October 12, 2026*

## Motivation

The TinyOT section of [MPC: Secret Sharing](/files/2026_03_15_MPC:_Secret_Sharing.html) gives the generation of authenticated random bits, and the ideas behind leaky AND and bucketing. This note writes out the two complete routes from authenticated random bits to AND triples:

- **Half-gate** (WRK): use half-gates to compute the product directly on authenticated bits, with a built-in correctness check, giving correct but possibly leaky candidates;
- **FKOS**: compute the product with random OT, then check correctness with cut and sacrifice, likewise giving correct but possibly leaky candidates.

The last step of both routes is the same: randomly bucket and combine the candidates to remove the leakage, outputting random triples $([a],[b],[c])$, $c=ab$.

## Setup

$n$ parties $P_1,\dots,P_n$. $P_i$ holds a private key $\Delta_i\in\mathbb F_{2^\kappa}$. The statistical security parameter is denoted $s$.

**Authenticated bit.** For a bit $x$, write $[x]$ for

$$
x=\bigoplus_{i=1}^n x^{(i)},\qquad
M_{j\to i}[x]=K_{i\leftarrow j}[x]\oplus x^{(j)}\Delta_i\quad(i\ne j),
$$

where $P_j$ holds the share $x^{(j)}$, the MACs $\{M_{j\to i}[x]\}_{i\ne j}$, and the keys $\{K_{j\leftarrow i}[x]\}_{i\ne j}$. The following operations are done locally:

- $[x]\oplus[y]$: XOR share, MAC, and key componentwise.
- Adding a public bit $e$: $x^{(1)}\leftarrow x^{(1)}\oplus e$, $K_{i\leftarrow1}[x]\leftarrow K_{i\leftarrow1}[x]\oplus e\Delta_i\ (i\ne1)$, everything else unchanged. Written $[x]\oplus e$.
- Multiplying by a public bit $e$: $e[x]$ is $[x]$ ($e=1$) or the all-zero sharing ($e=0$).

$\operatorname{Open}([x])$: each $P_j$ sends $x^{(j)}$ and $M_{j\to i}[x]$ to each $P_i$; $P_i$ checks the MAC relation and aborts on failure; if it passes, all parties obtain $x=\bigoplus_jx^{(j)}$. Opening several bits at once is still one round.

$\mathsf{aBit}(m)$: obtains $m$ authenticated random bits from pairwise correlated OT; for the construction and consistency check see [MPC: Secret Sharing](/files/2026_03_15_MPC:_Secret_Sharing.html) Section 2.1. Both routes take only this as input.

**Auxiliary functionalities.**

- $\mathcal F_{\mathsf{Rand}}$: outputs a public uniformly random value (coin or permutation) after all parties' messages are fixed.
- $\mathcal F_{\mathsf{Zero}}$: outputs a zero sharing $(z^{(1)},\dots,z^{(n)})$, with $z^{(i)}\in\mathbb F_{2^\kappa}$ uniform and $\bigoplus_iz^{(i)}=0$.
- commit-then-open: each party first sends a commitment to its value, and opens only after all commitments have been received; a party that opens later cannot change its value based on values opened earlier.

Write $\Delta_\Sigma=\bigoplus_i\Delta_i$. Fix a coordinate $\pi:\mathbb F_{2^\kappa}\to\mathbb F_2$ (taking one fixed bit of the field element); the setup guarantees $\pi(\Delta_\Sigma)=1$.

**Consumer side (Beaver AND).** For shares $[x],[y]$ and a triple $([a],[b],[c])$:

$$
e=\operatorname{Open}([x]\oplus[a]),\qquad
f=\operatorname{Open}([y]\oplus[b]),\qquad
[xy]=[c]\oplus f[a]\oplus e[b]\oplus ef .
$$

All AND gates in the same layer share one round of opening.

**Candidates.** Both routes first generate $\ell'$ candidates

$$
\bigl([a_m],[b_m],[c_m]\bigr)_{m\in[0,\ell')},\qquad c_m=a_mb_m,
$$

where each candidate may be **leaky**: the adversary may learn some honest party's $a_m^{(j)}$ at the cost of a $1/2$ abort probability. Finally, the Bucketing section combines the $\ell'=\ell B$ candidates into $\ell$ triples.

## Leaky AND from half-gates (WRK)

### Objects

$$
\bigl([a_m],[b_m],[r_m]\bigr)_{m\in[0,\ell')}\leftarrow\mathsf{aBit}(3\ell').
$$

$H:\{0,1\}^*\to\mathbb F_{2^\kappa}$ is a hash.

### Protocol

Executed independently for each candidate. Fix candidate $m$; this subsection omits the subscript $m$: input $[a],[b],[r]$, output $[c]$.

1. Call $\mathcal F_{\mathsf{Zero}}$ to get $z^{(i)}$. Each $P_i$ locally computes

   $$
   \begin{aligned}
   \phi_i&=z^{(i)}\oplus b^{(i)}\Delta_i\oplus\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[b]\oplus M_{i\to j}[b]\bigr),\\
   \psi_i&=r^{(i)}\Delta_i\oplus\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[r]\oplus M_{i\to j}[r]\bigr).
   \end{aligned}
   $$

2. For each pair $i\ne j$:

   $$
   P_i\longrightarrow P_j:\qquad
   G_{i\to j}=H\bigl(K_{i\leftarrow j}[a]\bigr)\oplus H\bigl(K_{i\leftarrow j}[a]\oplus\Delta_i\bigr)\oplus\phi_i .
   $$

3. Each $P_j$ locally computes

   $$
   E_{i\to j}=H\bigl(M_{j\to i}[a]\bigr)\oplus a^{(j)}G_{i\to j}\quad(i\ne j),\qquad
   T_j=a^{(j)}\phi_j\oplus\psi_j\oplus\bigoplus_{i\ne j}\Bigl(H\bigl(K_{j\leftarrow i}[a]\bigr)\oplus E_{i\to j}\Bigr).
   $$

4. Each $P_j$ publishes $\beta_j=\pi(T_j)$ via commit-then-open. All parties compute

   $$
   d=\bigoplus_j\beta_j,\qquad [c]=[r]\oplus d,\qquad \alpha_j=T_j\oplus d\Delta_j .
   $$

5. Each $P_j$ publishes $\alpha_j$ via commit-then-open. All parties check

   $$
   \bigoplus_j\alpha_j\overset?=0,
   $$

   and abort on failure.

**Claim.** In an honest execution, $c=ab$ and the check passes.

**Correctness.** By the MAC relation $K_{i\leftarrow j}[b]\oplus M_{j\to i}[b]=b^{(j)}\Delta_i$, summing over all ordered pairs and adding the diagonal terms, with the $z^{(i)}$ summing to zero:

$$
\bigoplus_i\phi_i=\Bigl(\bigoplus_jb^{(j)}\Bigr)\Bigl(\bigoplus_i\Delta_i\Bigr)=b\Delta_\Sigma,\qquad
\bigoplus_i\psi_i=r\Delta_\Sigma .
$$

From $M_{j\to i}[a]=K_{i\leftarrow j}[a]\oplus a^{(j)}\Delta_i$, case analysis on $a^{(j)}$ gives

$$
E_{i\to j}=H\bigl(K_{i\leftarrow j}[a]\bigr)\oplus a^{(j)}\phi_i .
$$

When summing over $j$, each $H(K_{i\leftarrow j}[a])$ appears once in $T_i$ and once in $T_j$ and cancels:

$$
\bigoplus_jT_j
=\bigoplus_ja^{(j)}\phi_j\oplus\bigoplus_{i\ne j}a^{(j)}\phi_i\oplus r\Delta_\Sigma
=\Bigl(\bigoplus_ja^{(j)}\Bigr)\Bigl(\bigoplus_i\phi_i\Bigr)\oplus r\Delta_\Sigma
=(ab\oplus r)\Delta_\Sigma .
$$

$\pi$ is linear and $\pi(\Delta_\Sigma)=1$, so $d=ab\oplus r$, $c=r\oplus d=ab$, and $\bigoplus_j\alpha_j=(ab\oplus r\oplus d)\Delta_\Sigma=0$.

**Security.** What $P_j$ sees in $G_{i\to j}$ is $\phi_i$ masked by $H(K_{i\leftarrow j}[a])\oplus H(K_{i\leftarrow j}[a]\oplus\Delta_i)$; from $M_{j\to i}[a]$, $P_j$ can compute only one of the two terms, and the other requires $\Delta_i$, so $b^{(i)}$ does not leak. $\beta_j$ is one bit of $T_j$, and $T_j$ is masked by the random $r$ in $\psi_j$. The opened $\alpha_i$ is masked by $z^{(i)}$ and only reveals a sum already known to be zero. Commit-then-open prevents the last party to publish from steering $\beta_j$ or $\alpha_j$ to a value of its choice.

If a corrupted $P_i$ sends $G_{i\to j}\oplus\delta$, then $\alpha_j$ is shifted by $a^{(j)}\delta$, and $P_i$ can at the same time either shift $\alpha_i$ by $\delta$ or not: under either choice, the check passes exactly when $a^{(j)}$ takes one particular value. Thus whether or not it aborts leaks $a^{(j)}$, and each attempt aborts with probability $1/2$. This is what it means for a candidate to be leaky; the check guarantees $c=ab$ when it passes, but cannot prevent this selective failure.

**Relation to the garbled-circuit half-gate.** View $P_i$ as the garbler and $P_j$ as the evaluator: $K_{i\leftarrow j}[a]$ and $K_{i\leftarrow j}[a]\oplus\Delta_i$ are the two labels of wire $a^{(j)}$, and the $M_{j\to i}[a]=K_{i\leftarrow j}[a]\oplus a^{(j)}\Delta_i$ held by $P_j$ is the one corresponding to $a^{(j)}$. $G_{i\to j}$ is exactly the row $T_G$ of the generator half-gate in [Garbled Circuits](/files/2026_07_02_Garbled_Circuits.html), with the garbler's constant $\lambda_\beta\Delta$ replaced by $\phi_i$; $E_{i\to j}$ is exactly the output label computed by the evaluator. There are two differences: $P_i$ keeps $H(K_{i\leftarrow j}[a])$ to itself instead of using it as a label, so $H(K_{i\leftarrow j}[a])\oplus E_{i\to j}=a^{(j)}\phi_i$ becomes an XOR sharing of the product; and there is no evaluator half-gate, because here both $a$ and $b$ are shared, so each cross term of $ab\Delta_\Sigma=\bigoplus_{i,j}a^{(j)}\phi_i$ uses one generator half-gate, and the diagonal terms are computed locally.

## Leaky AND from random OT with cut-and-choose (FKOS)

### Objects

Parameters $(N,\nu,T)$:

$$
N=T\ell'+\nu,
$$

$N$ is the number of candidates, $\nu$ candidates are fully opened (cut), and $T$ is the sacrifice group size.

$$
\bigl([a_m],[b_m],[r_m]\bigr)_{m\in[0,N)}\leftarrow\mathsf{aBit}(3N).
$$

$\mathsf{ROT}$: the sender gets a uniform $(q_0,q_1)\in\{0,1\}^2$, and the receiver holding choice bit $\chi$ gets $q_\chi$; see [Oblivious Transfer](/files/2026_09_02_Oblivious_Transfer.html). This section uses one independent instance for each candidate and each pair $i\ne j$, with $P_i$ as sender, its output written $(q_{i\to j,0},q_{i\to j,1})$, and $P_j$ as receiver, with choice bit $a^{(j)}$.

$\Pi_1,\Pi_2$ are uniformly random permutations output by $\mathcal F_{\mathsf{Rand}}$, drawn after all candidates are fixed.

### Multiplication

Executed independently for each candidate. Fix candidate $m$; this subsection omits the subscripts of $a_m,b_m,r_m$; output $[c]$.

1. For each pair $i\ne j$, call $\mathsf{ROT}$: $P_i$ gets $(q_{i\to j,0},q_{i\to j,1})$, $P_j$ gets $q_{i\to j,a^{(j)}}$.

2. For each pair $i\ne j$:

   $$
   P_i\longrightarrow P_j:\qquad
   u_{i\to j}=q_{i\to j,0}\oplus q_{i\to j,1}\oplus b^{(i)} .
   $$

3. Each $P_j$ locally computes

   $$
   v_{i\to j}=q_{i\to j,a^{(j)}}\oplus a^{(j)}u_{i\to j}\quad(i\ne j).
   $$

4. Each $P_i$ locally computes

   $$
   z^{(i)}=a^{(i)}b^{(i)}\oplus\bigoplus_{j\ne i}\bigl(q_{i\to j,0}\oplus v_{j\to i}\bigr).
   $$

5. Each $P_i$ broadcasts $z^{(i)}\oplus r^{(i)}$. All parties compute

   $$
   e=\bigoplus_i\bigl(z^{(i)}\oplus r^{(i)}\bigr),\qquad [c]=[r]\oplus e .
   $$

**Claim.** In an honest execution, $c=ab$.

**Correctness.** By case analysis on $a^{(j)}$,

$$
v_{i\to j}=q_{i\to j,0}\oplus a^{(j)}b^{(i)} .
$$

Substituting into $z^{(i)}$, each $q_{i\to j,0}$ appears once in $z^{(i)}$ and once in $z^{(j)}$ and cancels:

$$
\bigoplus_iz^{(i)}=\bigoplus_ia^{(i)}b^{(i)}\oplus\bigoplus_{i\ne j}a^{(j)}b^{(i)}=ab,
\qquad e=ab\oplus r,\qquad c=ab .
$$

$z^{(i)}$ has no MAC, so $e$ is not authenticated; all of the authentication of $[c]$ comes from $[r]$, and a corrupted party can change $e$ to any value, making $c\ne ab$. The next two steps check correctness.

### Cut

Take $\Pi_1$. For candidates $m=\Pi_1(0),\dots,\Pi_1(\nu-1)$:

$$
\operatorname{Open}([a_m]),\ \operatorname{Open}([b_m]),\ \operatorname{Open}([c_m]),\qquad a_mb_m\overset?=c_m .
$$

Abort on failure; these $\nu$ candidates are discarded.

### Sacrifice

Take $\Pi_2$ and split the remaining $T\ell'$ candidates into $\ell'$ groups of $T$ each; the first in each group is called the head $\eta$, and the rest are denoted $k$. For each $k$ in each group:

1. One round of opening

   $$
   \rho_{\eta,k}=\operatorname{Open}\bigl([a_\eta]\oplus[a_k]\bigr),\qquad
   \sigma_{\eta,k}=\operatorname{Open}\bigl([b_\eta]\oplus[b_k]\bigr).
   $$

2. One round of opening

   $$
   \operatorname{Open}\Bigl([c_\eta]\oplus[c_k]\oplus\rho_{\eta,k}[b_k]\oplus\sigma_{\eta,k}[a_k]\oplus\rho_{\eta,k}\sigma_{\eta,k}\Bigr)\overset?=0 .
   $$

Abort on failure. Each group keeps $\eta$ and discards the other $T-1$. The $\ell'$ heads are the candidates output by this section.

**Correctness.** If $c_\eta=a_\eta b_\eta$ and $c_k=a_kb_k$, substituting $a_\eta=a_k\oplus\rho_{\eta,k}$ and $b_\eta=b_k\oplus\sigma_{\eta,k}$:

$$
a_\eta b_\eta=a_kb_k\oplus\sigma_{\eta,k}a_k\oplus\rho_{\eta,k}b_k\oplus\rho_{\eta,k}\sigma_{\eta,k},
$$

so the opened value is $0$.

**Security.** $P_j$ knows only one of $q_{i\to j,0},q_{i\to j,1}$, and the $b^{(i)}$ in $u_{i\to j}$ is masked by the other. $P_i$ receives no messages. $e=ab\oplus r$ is masked by the random $r$. The $\rho_{\eta,k},\sigma_{\eta,k}$ opened in sacrifice are masked by the $a_k,b_k$ of the discarded candidates.

Define the error of candidate $m$ as $c_m\oplus a_mb_m$. The adversary can make any $g$ candidates have error $1$, but must decide before $\Pi_1,\Pi_2$ are drawn. Passing the cut requires that none of these $g$ be among the $\nu$ opened ones; passing the sacrifice step requires all candidates within each group to have the same error (the opened value is the XOR of the head's and the member's errors), i.e., the $g$ erroneous candidates exactly fill $g/T$ whole groups. Therefore

$$
\Pr[\text{an erroneous candidate exists and all checks pass}]
\le\max_{1\le q\le\ell'}
\frac{\binom{N-Tq}{\nu}}{\binom{N}{\nu}}\cdot
\frac{\binom{\ell'}{q}}{\binom{T\ell'}{Tq}} .
$$

When $q$ is small the second factor is small, and when $q$ is close to $\ell'$ the first factor is small; the role of the cut is to close off the case "all candidates are erroneous", which sacrifice cannot detect.

If a corrupted $P_i$ sends $u_{i\to j}\oplus\delta$, then $z^{(j)}$ is shifted by $a^{(j)}\delta$: when $a^{(j)}=0$ the candidate is correct, and when $a^{(j)}=1$ the candidate is erroneous and is caught by the checks. Whether or not it aborts leaks $a^{(j)}$, and each attempt aborts with probability $1/2$. This is the same selective failure as in the half-gate route, and it is removed by the bucketing in the next section.

## From leaky candidates to triples: bucketing

### Objects

The input is the $\ell'=\ell B$ candidates $([a_m],[b_m],[c_m])_{m\in[0,\ell')}$ output by either section above, each satisfying $c_m=a_mb_m$, some of which may be leaky. $B\ge2$ is the bucket size. $\Pi_3$ is a uniformly random permutation output by $\mathcal F_{\mathsf{Rand}}$, drawn after all candidates are fixed.

Split the candidates into $\ell$ buckets of $B$ each according to $\Pi_3$; the first in bucket $p\in[0,\ell)$ is called the head $\eta$, and the other $B-1$ are denoted $k$.

### Protocol

1. Open all $(B-1)\ell$ differences in one round:

   $$
   d_{\eta,k}=\operatorname{Open}\bigl([b_\eta]\oplus[b_k]\bigr).
   $$

2. Combine locally:

   $$
   [A_p]=[a_\eta]\oplus\bigoplus_k[a_k],\qquad
   [B_p]=[b_\eta],\qquad
   [C_p]=[c_\eta]\oplus\bigoplus_k\Bigl([c_k]\oplus d_{\eta,k}[a_k]\Bigr).
   $$

**Claim.** The output is $([A_p],[B_p],[C_p])_{p\in[0,\ell)}$ with $C_p=A_pB_p$.

**Correctness.**

$$
C_p=a_\eta b_\eta\oplus\bigoplus_k\bigl(a_kb_k\oplus(b_\eta\oplus b_k)a_k\bigr)
=a_\eta b_\eta\oplus\bigoplus_ka_kb_\eta=A_pB_p .
$$

**Security.** $d_{\eta,k}$ is authenticated by $\operatorname{Open}$ and masked by the random $b_k$ of the member candidate. To learn $A_p$, the adversary needs the $a$ of all $B$ candidates in bucket $p$, i.e., it must have attacked every candidate in the bucket; each attack survives with probability $1/2$, and $\Pi_3$ is drawn only after the attacks take place. Suppose the adversary attacks $g$ candidates in total; under a uniform permutation, the probability that a fixed bucket consists entirely of attacked candidates is $\binom gB\big/\binom{\ell B}{B}$; taking the expectation over the $\ell$ buckets and applying Markov's inequality:

$$
\Pr[\text{checks pass and some bucket is entirely leaky}]
\le\max_{B\le g\le\ell B}2^{-g}\,\frac{\ell\binom gB}{\binom{\ell B}{B}} .
$$

Take the smallest $B$ such that the right-hand side is $\le2^{-s}$.
