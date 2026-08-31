# Polynomial IOPs for Circuit SAT and PLONK

*January 20, 2026*

## Polynomial IOP for Circuit SAT

In this lecture we are going to construct a poly-IOP for circuit satisfiability. $C$  is an arithmetic circuit with size $S$ . The prover wants to prove that it knows the solution $w$  to $C(w)=y$ .

First, we label every gate of $C$  with a bit string of length $\log S$ . Thus the computation of $C(w)=y$  can be expressed in a form of function $T:\{0,1\}^{\log S}\mapsto\mathbb{F}$ , which maps the label of some gate to the output of the gate with its output (notice that $T(\text{root})=y$ ). Let $h:\mathbb{F}^{\log S}\mapsto\mathbb{F}$  be the unique **multilinear** extension of $T$ , satisfying $h(x)=T(x)$  for all $x \in \{0,1\}^{\log S}$  (the uniqueness is trivial by dynamic programming).

Why shall we extend the function $T$  to a multilinear polynomial $h$ ? The necessity is shown in the part of the sum-check protocol.

Here $V$  should have verified the $h$  and $T$  are the same on $\{0,1\}^{\log S}$ . However $V$  only has the commitment of $h$ , so $V$  verifies this by another approach shown below.

We use labels to denote gates, and define the polynomial $g_h:\mathbb{F}^{3\log S}\mapsto\mathbb{F}$  as follows:

$$
g_h(a,b,c)=\begin{cases}
h(a)+h(b)-h(c), & \text{if }c\text{ is an add gate with input }a,b, \\
h(a)h(b)-h(c), & \text{if }c\text{ is an mult gate with input }a,b,\\
0,& \text{otherwise}.
\end{cases}
$$

which satisfies:

$$
T\text{ is a correct assignment }\iff \forall (a,b,c)\in\{0,1\}^{3\log S},\;g_h(a,b,c)=0\;(\text{in }\mathbb{F}).
$$

We shall modify a little in $g_h$ : we embed the result $g_h(a,b,c)$  into $\mathbb{Z}$ . So the condition above is equivalent to $\sum_{x\in\{0,1\}^{3\log S}} \tilde{g}_h(x)=0$  where $\tilde{g}_h:\mathbb{F}^{3\log S}\mapsto\mathbb{Z}$  has the same values as $g_h$  on all inputs. Then $P$  and $V$  interact to let $V$  believe that the sum is $0$ . If the sum is $0$ , $V$  believes that $P$  knows the correct $T$ .

Here comes the usage of the **sum-check protocol**.

### Sum-Check Protocol

The goal of the protocol is to check the answer $C$  provided by prover satisfies:

$$
C=\sum_{x\in\{0,1\}^n}g(x)
$$

where $g$  is an $n$ -variate polynomial over the field $\mathbb{F}$  and the sum is computed in $\mathbb{Z}$  (i.e. add them up without taking the modulo).

In setup phase, $P$  sends the commitment of $g$  to $V$ . Then they interact for $n$  rounds, and in the end $V$  checks the final claim by querying the oracle of $g$  for one time at a random point.

$$
\begin{align*}
&\text{Prover}&&&\text{Verifier}\\
\text{start}:&\text{ ``I know }s_0=\sum_{x\in\{0,1\}^n}g(x)\text{'' }&\xrightarrow{s_0}&&\\
\text{round 1}:&\text{``Please verify the last step to compute }s_0\text{''}&\xrightarrow{s_1(X_1)}&&\text{ verify }s_1(0)+s_1(1)=s_0\text{ and the next goal is to verify }s_1(X_1)=\sum_{x\in\{0,1\}^{n-1}}g(X_1,x)\\
&&\xleftarrow{r_1}&&\text{``If indeed, then for most }r\in\mathbb{F},s_1(r)=\sum_{x\in\{0,1\}^{n-1}}g(r,x)\text{. So I send a random $r_1$.''}\\
\text{round 2}:&\text{``I will proof }s_1(r_1)=\sum_{x\in\{0,1\}^{n-1}}g(r_1,x)\text{, please verify...'' }&\xrightarrow{s_2(X_2)}&\;&...\\
&&...&&\\
\text{round }n:&\text{ ``I will proof }s_{n-1}(r_{n-1})=\sum_{x\in\{0,1\}}g(r_1,\dots,r_{n-1},x)\text{, please verify...'' }&\xrightarrow{s_{n}(X_{n})}&\;&\text{ verify }s_n(0)+s_n(1)=s_{n-1}(r_{n-1})\text{ and the next goal is to verify }s_{n}(X_n)=g(r_1,\dots,r_{n-1},X_{n})\\
&&&\;&r_n\xleftarrow{\$}\mathbb{F},\text{ obtaining }s_n(r_n).\text{ Then query the oracle of }g\text{ at }(r_i)_{i=1}^n.\text{ Accept iff }g(r_1,\dots,r_n)=s_n(r_n).
\end{align*}
$$

The probability that a cheating prover can make the verifier accept a false claim is at most $\frac{n\deg(g)}{|\mathbb{F}|}$  (by Schwartz-Zippel lemma, $\deg$  is the maximum degree in total, regardless of different variables). So we can make the soundness error negligible by choosing a large enough field.

Note that every polynomial from $P$  is sent in its coefficients. Let $d=\deg(g)$  and it takes $T_g$  time to verify/evaluate any $g(x)$ , we have

$$
T_V=O(nd+T_g),T_P=O(2^ndT_g)
$$

and the proof length is $O(nd)$ .

For dense polynomial $g$ , the time to evaluate its multilinear extension $\tilde g$  on point $x$  is at most $O(2^n)$ . Thus our prover has quadratic time. The [[Libra]](https://eprint.iacr.org/2019/317.pdf) puts forwards a linear time sum-check prover.

This sum-check protocol is also used in the proof that $\mathbf{IP}=\mathbf{PSPACE}$ . Define the decisional counting problem of 3CNF as:

$$
(\#\mathsf{SAT})_D:=\left\{\langle\varphi,k\rangle:k=\sum_{b_1,\dots,b_n\in\{0,1\}}\varphi(b_1,\dots,b_n)\right\}
$$

so by translating the boolean formula into a multilinear polynomial, with the sum-check protocol we have $(\#\mathsf{SAT})_D\in\mathbf{IP}$ .

Suppose we have a $\mathsf{TQBF}$  formula $\psi=\forall x_1\exists x_2\dots Qx_n.\varphi(x_1,x_2,\dots,x_n)$ , if we directly make $\forall$  into multiplication and $\exists$  into addition, the degree will skyrocket. Define for a $p\in\mathbb{F}[X_1,\dots,X_n]$ ,

$$
\begin{align*}
&\mathsf{L}_ip:=(1-X_i)p^{i\leftarrow0}+X_ip^{i\leftarrow1}\in\mathbb{F}[X_1\dots,X_n],\\
&\mathsf{A}_ip:=p^{i\leftarrow0}p^{i\leftarrow1}\in\mathbb{F}[X_1\dots X_{i-1},X_{i+1},\dots,X_n],\\
&\mathsf{E}_ip:=1-(1-p^{i\leftarrow0})(1-p^{i\leftarrow1})\in\mathbb{F}[X_1\dots X_{i-1},X_{i+1},\dots,X_n],
\end{align*}
$$

these polynomials are all in $\mathbb{F}[X_1\dots,X_n]$ .

In analogy to the sum-check protocol, we can also define $\mathsf{X}_ip:=p^{i\leftarrow0}+p^{i\leftarrow1}\in\mathbb{F}[X_1\dots X_{i-1},X_{i+1},\dots,X_n]$ .

The idea is to linearize the polynomial after each multiplication. So the formula is described by the polynomial

$$
\mathsf{A}_1\mathsf{L}_1\mathsf{E}_2\mathsf{L}_1\mathsf{L}_2\mathsf{A}_3\mathsf{L}_1\mathsf{L}_2\mathsf{L}_3\dots\mathsf{Q}_n\mathsf{L}_1\mathsf{L}_2\dots\mathsf{L}_np_{\varphi}=1
$$

then the prover and verifier go through a $O(n^2)$  interaction to establish the protocol. Thus $\mathsf{TQBF}\in\mathbf{IP}$  and $\mathbf{IP}=\mathbf{PSPACE}$ .

## PLONK IOP

Based on the lecture 4, we can encode a circuit problem into a polynomial. The sum-check protocol uses multi-variable polynomials with a large proof size (linear to $n\sim\log |C|$  even if we send commitments of polynomials instead of coefficients). PLONK is also used for circuit SAT with a different encoding, which uses univariate polynomials and has a proof size independent of $n$ .

### Small gadgets to build PLONK IOP

Let $\Omega=\langle\omega\rangle\subset\mathbb{F}_p$  be a multiplicative subgroup of size $k\mid\varphi(p)$ . And we want to provide protocols to prove that a committed polynomial $f$  has some properties on $\Omega$ . The properties of given $f,g\in\mathbb{F}_p[X]$  include:

- Zeroness: $f(x)=0$  for all $x\in\Omega$

- Sum/Product over $\Omega$ : $\sum_{x\in\Omega}\left(f(x)-g(x)\right)=0$  or $\prod_{x\in\Omega}\frac{f(x)}{g(x)}=1$

- Permutation: $(f(\omega^i))_{i=0}^{k-1}$  is a permutation of $(g(\omega^i))_{i=0}^{k-1}$ . Warning: it is not enough to check $\prod_{x\in\Omega}\frac{f(x)}{g(x)}=1$ ! The soundness relies on the random challenge by the verifier.

- Prescribed permutation: $f(y)=g(W(y))$  for some known permutation $W:\Omega\to\Omega$

### Encoding a circuit into a polynomial

We again take $C(x,w)$  as the circuit satisfiability problem. Let $d=3|C|+|x|+|w|$ , and label each gate with a integer. And we have the $d$ -th root $\omega$ , which satisfies $\omega^d=1$ .

Setup phase outputs polynomial $S$  and permutation $W$ . The prover wants to prove that it knows $w$  such that $C(x,w)=0$ , so it interpolates a polynomial $T\in\mathbb{F}_p^{\leq d}[X]$  such that

- $T(\omega^{-j})=$  the value of the $j$ -th input

- $T(\omega^{3i}),T(\omega^{3i+1}),T(\omega^{3i+2})$  are the left-input/right-input/output of the $i$ -th gate, $i=0,1,\dots,|C|-1$

using FFT in time $O(d\log d)$ .

Then the prover proves the following:

- The inputs are correct: $T(\omega^{-j})=x_j$  for $j=0,1,\dots,|x|-1$

- The math operations are correct: Use a public $S(\omega^{3i})=1$  iff $i$ -th gate is multiplicative; then, prove for all $y\in\{\omega^{3i}:i<|C|\}$ ,

$$
S(y)\cdot T(y)\cdot T(y\omega)+(1-S(y))\cdot(T(y)+T(y\omega))-T(y\omega^{2})=0.
$$

- Wiring is correct: Use a public $W$  to rotate the wires that share the same value; then, prove $T(y)=T(W(y))$  for all $y\in\{\omega^{i}:i<d\}$

- The output is $0$ : $T(\omega^{3|C|-1})=0$

using the gadgets mentioned above.
