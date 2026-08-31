# Measurable Functions

*June 14, 2024*

*In Axiomization of probability.*

i.e. Random variables

## Notations

- $\mathcal{L}^+_{b}(\mathcal{C})$: the set of all bounded measurable functions on $\mathcal{C}$.

## Definition and Theorem of Approximation

***Definition 1.*** 设 $(\Omega,\mathcal{F})$ 和 $(E,\mathcal{E})$ 是测度空间， $f:\Omega\to E$ 是一个映射，如果对于每一个 $A\in\mathcal{E}$ ， $f^{-1}(A)\in\mathcal{F}$ ，则称 $f$ 是 $\mathcal{F}/\mathcal{E}$ **-可测映射**.

***Definition 2.*** 令 $E=\overline{\mathbb{R}},\mathcal{E}=\mathcal{B}(\overline{\mathbb{R}})$ ，则称 $f$ 为**Borel可测函数**.

***Example 3.*** Let $\mathscr{F}$ be some collection of $f\in C(0,1)$. Then $\Phi(x)=\sup_{f\in\mathscr{F}} f$ and $\Psi(x)=\inf_{f\in\mathscr{F}} f$ is measurable.

***Proof.*** Consider $E_t={\{x:\Phi(x)>t\}}$. Then $\Phi(x_0)>t$ implies that there exists $f_{x_0}\in\mathscr{F}$ such that $f_{x_0}(x_0)>t$. Since $f$ is continuous, there exists $\delta>0$ s.t. for all $x\in B_{\delta}(x_0)$, $f_{x_0}(x)>t$. Thus $B_{\delta}(x_0)\subseteq E_t$. Hence $E_t$ is open, and $\Phi$ is measurable. $\blacksquare$

***Example 4.*** Let $\{f_k(x)\}$ be a sequence of measurable functions over $\mathbb{R}^n$. Then $\{x:\lim_{k\to+\infty}f_k(x) \text{ exists}\}$ is measurable.

***Proof.*** Let $E=\{x:\lim_{k\to+\infty}f_k(x) \text{ exists}\}$. Then

$$
E=\bigcap_{m=1}^{\infty}\bigcup_{k=1}^{\infty}\bigcap_{n=k}^{\infty}\bigcap_{l=k}^{\infty}\{x:|f_n(x)-f_l(x)|<\frac{1}{m}\}
$$

, which is measurable. $\blacksquare$

***Example 5.*** Let $\mathscr{F}$ be some collection of measurable functions. Then $\Phi(x)=\sup_{f\in\mathscr{F}} f$ and $\Psi(x)=\inf_{f\in\mathscr{F}} f$ may not be measurable.

Let $\mathscr{F}=\{\chi_{\{y\}}:y\in N\}$, where $N$ is a **Vitali Set**. Then $\Phi(x)=\chi_N$ which is not measurable.

***Definition 6.*** $f$ is a **simple function** if $f$ is measurable and takes only finitely many values. (non-continuous r.v.)

For a simple function $f$, $f=\sum_{i=1}^n a_i\chi_{A_i}$, where $A_i$ are disjoint sets. We can prove the representation is unique.

And if all $E_i$ are measurable, then $f$ is measurable.

***Theorem 7.*** Let $f$ be a non-negative measurable function. Then there exists an increasing sequence of simple functions $\{f_n\}$ s.t. $f_n\to f$ pointwise.

***Proof.*** Let

$$
f_n(x)=\sum_{k=0}^{n2^n-1}\frac{k}{2^{n}}\chi_{\{\frac{k}{2^{n}}\leq x < \frac{k}{2^{n+1}}\}}+n\chi_{\{f\geq n\}}
$$

. Then $f_n\to f$ pointwise.

***Theorem 8.*** Let $f$ be a measurable function. Then there exists a sequence of simple functions $\{f_n\}$ s.t. $|f_n(x)|<|f(x)|$ and $f_n\to f$ pointwise.

In particular, if $f$ is bounded, then $f_n\to f$ uniformly.

## Convergence of Measurable Functions

***Definition 9.*** Let $f_n,f$ be measurable functions from $(\Omega,\mathcal{F},\mu)$ to $(\mathbb{R},\mathcal{B}(\mathbb{R}),m)$. Define

- $f_n\to f$ **a.e.** if there exists a zero-measure set $N$ s.t. $f_n(\omega)\rightarrow f(\omega)$ over $N^c$.

- $f_n\to f$ **a.un.** if there exists a zero-measure set $N$ s.t. $f_n(\omega)\rightrightarrows f(\omega)$ over $N^c$.

- $f_n\to f$ **in measure** if $\lim_{n\to\infty}\mu(\{|f_n(\omega)-f(\omega)|>\epsilon\})=0$ for all $\epsilon>0$.

The convergence mentioned above of measurable functions is equivalent to the extent of $\text{a.e.}$ equality. For example, if $f_n\stackrel{\mu}{\rightarrow}f$ and $f_n\stackrel{\mu}{\rightarrow}g$,

$$
[|f-g|>\epsilon]\subset\big[|f-f_k|>\frac{\epsilon}{2}\big]\cup\big[|g-f_k|>\frac{\epsilon}{2}\big]
$$

take $k\to\infty$ gives $\mu\big([|f-g|>\epsilon]\big)=0$, which implies $f=g$ a.e.

***Theorem 10.*** Let $\{f_n\}$ and $f$ be measurable functions. Then $f_n\stackrel{a.e.}{\rightarrow}f$ if and only if for all $\epsilon>0$,

$$
\mu\big(\bigcap_{n=1}^{+\infty}\bigcup_{i=n}^{+\infty}[|f_i-f|\geq\epsilon]\big)= 0
$$

***Proof.*** $x\in \{f_n\to f\}$ if and only if for all $k>0$, there exists $N$ s.t. for all $n>N$, $|f_n(x)-f(x)|<\frac{1}{k}$ $\iff$

$$
x\in\bigcap_{k=1}^{+\infty}\bigcup_{n=1}^{+\infty}\bigcap_{i=n}^{+\infty}[|f_i-f|<\frac{1}{k}].
$$

So $x\notin\{f_n\to f\}$ if and only if

$$
x\in\bigcup_{k=1}^{+\infty}\bigcap_{n=1}^{+\infty}\bigcup_{i=n}^{+\infty}[|f_i-f|\geq\frac{1}{k}]
$$

and

$$
\mu\big(\bigcup_{k=1}^{+\infty}\bigcap_{n=1}^{+\infty}\bigcup_{i=n}^{+\infty}[|f_i-f|\geq\frac{1}{k}]\big)=0\iff\forall k>0\;\mu\big(\bigcap_{n=1}^{+\infty}\bigcup_{i=n}^{+\infty}[|f_i-f|\geq\frac{1}{k}]\big)=0
$$

***Theorem 11.*** Let $\{f_n\}$ and $f$ be measurable functions. Then $f_n\stackrel{a.un.}{\rightarrow}f$ if and only if for all $\epsilon>0$,

$$
\lim_{n\to+\infty}\mu\big(\bigcup_{i=n}^{+\infty}[|f_i-f|\geq\epsilon]\big)=0
$$

***Proof.*** $f_n\stackrel{a.un.}{\rightarrow}f$ implies that for all $\delta>0$ there exists a set $F$ that $\mu(F)<\delta$ s.t. $\forall\epsilon>0$, $\exists N>0$ s.t. $\forall x\in F^c$, $\forall n>N$, $|f_n(x)-f(x)|<\epsilon$, i.e.

$$
\forall\delta>0\;\exists F\;\mu(F)<\delta\; \text{ s.t. } \forall\epsilon>0\;\exists n>0\;\bigcup_{i=n}^{+\infty}[|f_i-f|\geq\epsilon]\subset F
$$

that is,

$$
\forall\delta>0\;\forall\epsilon>0\;\exists n>0\;\mu\big(\bigcup_{i=n}^{+\infty}[|f_i-f|\geq\epsilon]\big)\leq\delta
$$

Applying sup limit to $n$ gives

$$
\forall\epsilon>0\;\forall\delta>0\;\overline{\lim_{n\to+\infty}}\mu\big(\bigcup_{i=n}^{+\infty}[|f_i-f|\geq\epsilon]\big)\leq\delta
$$

and the result follows.

For the other side, for all $k>0$ and $\delta>0$, there exists $n_k$ s.t.

$$
\mu\big(\bigcup_{i=n_k}^{+\infty}[|f_i-f|\geq\frac{1}{k}]\big)<\frac{\delta}{2^k}.
$$

Let

$$
F=\bigcup_{k=1}^{+\infty}\bigcup_{i=n_k}^{+\infty}[|f_i-f|\geq\frac{1}{k}]
$$

and $\mu(F)<\delta$. Then

$$
F^c=\bigcap_{k=1}^{+\infty}\bigcap_{i=n_k}^{+\infty}[|f_i-f|<\frac{1}{k}]
$$

Note that $n_k$ is only a function of $k$. So the convergence is uniform over $F^c$, and $f_n\stackrel{a.un.}{\rightarrow}f$.

***Theorem 12.*** Let $\{f_n\}$ and $f$ be measurable functions. Then $f_n\stackrel{\mu}{\rightarrow}f$ if and only if for all subsequence $\{f_{n_k}\}$, there exists a further subsequence $\{f_{n_{k_l}}\}$ s.t. $f_{n_{k_l}}\stackrel{a.un.}{\rightarrow}f$.

***Corollary 13.*** (1) $\text{a.un.}\Rightarrow\text{a.e.}$; $\text{a.un.}\Rightarrow\mu$

(2) **(Егоров)** If $\mu(\Omega)<\infty$, then $\text{a.e.}\Rightarrow\text{a.un.}$

(3) **(Riesz)** If $f_n\stackrel{\mu}{\rightarrow}f$, then there exists a subsequence $\{f_{n_k}\}$ s.t. $f_{n_k}\stackrel{a.e.}{\rightarrow}f$.

***Proof.*** (2) Finite measure is upward continuous.

***Note.*** Be cautious of the difference of a.e. finite and a.e. bounded!

## An essential part: convergence in distribution

***Lemma.(not verified)*** $f_n,f:\Omega\mapsto\mathbb{R}$ are measurable functions (i.e. random variables). Then

$$
f_n\stackrel{\text{d}}{\rightarrow}f\Leftrightarrow\forall a,b\in\Lambda_f,\int_{\mathbb{R}}\mathbf{1}_{[a,b)}\circ f_n\to\int_{\mathbb{R}}\mathbf{1}_{[a,b)}\circ f
$$

***Attempt.*** Let $F_n,F$ be the distribution functions of $f_n,f$. Then

$$
F_n{\rightarrow}F \text{ on }\Lambda_f\Leftrightarrow\forall a,b\in\Lambda_f,F_n(b)-F_n(a)\to F(b)-F(a)
$$

$\Rightarrow$ is trivial.

$\Leftarrow$: Pick $\{a_n\},b$ from $\Lambda_f$ arbitrarily s.t. $a_n\to-\infty$ as $n\to+\infty$.

Then $|F_n(b)-F(b)|\leq|F_n(a_k)-F(a_k)|+|F_n(b)-F_n(a_k)+F(a_k)-F(b)|$.

For every $\epsilon>0$, we pick $n=N$ large enough s.t. $|F_n(b)-F_n(a_k)+F(a_k)-F(b)|<\frac{\epsilon}{3}$, for such $N$, using the property of a distribution function, there exists $k=K$ large enough s.t. $|F_N(a_K)|<\frac{\epsilon}{3}$ and $|F(a_K)|<\frac{\epsilon}{3}$.

To conclude, $|F_N(b)-F(b)|<\epsilon$, and can be arbitrarily small.

The proof is deemed fake because the process of $n\to+\infty$ and $k\to+\infty$ can not exchange.

---
