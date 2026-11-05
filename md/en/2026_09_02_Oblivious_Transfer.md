# Oblivious Transfer

*September 2, 2026*

## Definitions and equivalences

### 1-out-of-2 OT

Throughout, $\kappa$ is the security parameter and messages have length $\kappa$. The sender is denoted $S$, the receiver $R$.

> **Definition (1-out-of-2 OT).** $S$ inputs $(m_0,m_1)\in\{0,1\}^\kappa\times\{0,1\}^\kappa$, $R$ inputs a choice bit $b\in\{0,1\}$:
>
> $$
> \mathsf{OT}\big((m_0,m_1);\,b\big)\longrightarrow(\bot;\,m_b).
> $$
>
> - **Sender security**: apart from $m_b$, $R$ learns nothing about $m_{1-b}$.
> - **Receiver security**: $S$ learns nothing about $b$.

### Random OT and correlated OT

Each of the two variants below takes away one more party's freedom to choose its input.

> **Definition (Correlated OT).** $S$ inputs a correlation $\Delta\in\{0,1\}^\kappa$, $R$ has no input. The functionality samples $q\xleftarrow{\$}\{0,1\}^\kappa$ and $r\xleftarrow{\$}\{0,1\}$:
>
> $$
> \mathsf{COT}(\Delta;\,\bot)\longrightarrow\big(q;\ (r,\,t)\big),\qquad t=q\oplus r\Delta .
> $$
>
> - **Sender security**: $R$ learns nothing about $\Delta$, and hence nothing about the other message $t\oplus\Delta$.
> - **Receiver security**: $S$ learns nothing about $r$.
>
> Difference from random OT: the two messages $(q,\,q\oplus\Delta)$ of $S$ always differ by $\Delta$. $m$ instances share the same $\Delta$:
>
> $$
> t_i=q_i\oplus r_i\Delta,\qquad i\in[m].
> $$
> 

> **Definition (Random OT).** Neither party has input. The functionality samples $(a_0,a_1)\xleftarrow{\$}\{0,1\}^\kappa\times\{0,1\}^\kappa$ and $r\xleftarrow{\$}\{0,1\}$:
>
> $$
> \mathsf{ROT}(\bot;\,\bot)\longrightarrow\big((a_0,a_1);\ (r,\,a_r)\big).
> $$
>
> - **Sender security**: $R$ learns nothing about $a_{1-r}$.
> - **Receiver security**: $S$ learns nothing about $r$.
>
> Difference from 1-out-of-2 OT: $S$ cannot choose $(a_0,a_1)$, and $R$ cannot choose $r$.
> 


COT is exactly the correlation MPC needs: take $\kappa=1$, $\Delta=x$, and use the derandomization of the next subsection to replace $r$ with the $y$ that $R$ wants; then

$$
q\oplus t=xy,
$$

$S$ holds $q$, $R$ holds $t$, and the two form a sharing of the product $xy$. GMW uses it twice per AND gate.

### Equivalence

**Trivial direction.** Given a protocol for a stronger OT, to realize a weaker one you just fill the extra choices you have with random values and call it directly, with no additional communication:

- **1-out-of-2 OT $\Rightarrow$ COT.** The target is COT: $S$ has $\Delta$, $R$ has nothing. $S$ samples $q$ and inputs $(q,\,q\oplus\Delta)$; $R$ samples $r$ and inputs $b=r$; run one 1-out-of-2 OT. $S$ gets $q$, $R$ gets $(r,\,q\oplus r\Delta)$, which is exactly the COT output.
- **COT $\Rightarrow$ random OT.** The target is random OT: neither party has anything. $S$ samples $\Delta$ and runs one COT with it as input, obtaining $(q,\,q\oplus\Delta)$; $R$ gets $(r,\,t)$. Since $\Delta$ is uniformly random, $(q,\,q\oplus\Delta)$ is a pair of uniform independent messages, which is exactly the random OT output. Here each instance's $\Delta$ must be sampled independently. If $m$ instances share the same $\Delta$ (which is exactly what OT extension produces), then $R$ learning $\Delta$ in any one instance opens all instances, and this batch of COTs is not $m$ independent random OTs. In that case, break the correlation with a random oracle $H:[m]\times\{0,1\}^\kappa\to\{0,1\}^\kappa$:

  $$
  a_0=H(i,q_i),\qquad a_1=H(i,q_i\oplus\Delta),\qquad a_{r_i}=H(i,t_i).
  $$

  $R$ does not know $\Delta$ and cannot compute $H(i,t_i\oplus\Delta)$; the index $i$ makes the pads of different instances independent.

So, in terms of how hard they are to produce, 1-out-of-2 OT $\geq$ COT $\geq$ random OT: the fewer the choices, the easier to produce. The constructions below only produce COT or random OT.

**Reverse direction.** For the three to be equivalent, we still need to build 1-out-of-2 OT back from the easiest one, random OT. This step is called derandomization, from Beaver's precomputed OT; it means replacing the random inputs with the inputs actually wanted, and is unrelated to derandomization in complexity theory. $S$ inputs $(m_0,m_1)$, $R$ inputs $b$; first call random OT once, then use two messages to swap the random outputs for the real inputs:

$$
\begin{align*}
&\text{Sender}&&&\text{Receiver}\\
&\text{gets }(a_0,a_1)
&\xleftarrow{\ \ \mathsf{ROT}(\bot;\,\bot)\ \ }&\;&\text{gets }(r,\,a_r)\\
&&\xleftarrow{d}&\;&d\leftarrow b\oplus r\\
&c_0\leftarrow m_0\oplus a_d,\quad c_1\leftarrow m_1\oplus a_{1\oplus d}
&\xrightarrow{c_0,\,c_1}&\;&m_b\leftarrow c_b\oplus a_r
\end{align*}
$$

Correctness: the pad index used by $c_b$ is $b\oplus d=r$, which is exactly the $a_r$ that $R$ holds.

Security: $d$ is masked by the uniform $r$, so $S$ learns nothing about $b$; $R$ lacks $a_{1\oplus r}$ and cannot open $c_{1\oplus b}$. Online communication is only $1+2\kappa$ bits, and all public-key operations fall in the phase that produces random OT.

### Why OT needs public-key assumptions

OT implies key agreement, and Impagliazzo–Rudich proved that key agreement cannot be constructed black-box from one-way functions or random oracles. So OT needs at least one use of a public-key-type assumption; all the techniques below aim to make that use as small as possible.

## Base OT: Chou–Orlandi

**Motivation.** The previous section showed that we only need to produce random OT or COT, but these still require public-key assumptions. This section gives a concrete construction. It only needs to run $\kappa$ times, after which OT extension takes over.

**Objects.** $\mathbb G$ is a cyclic group of prime order $p$ with generator $g$, in which CDH holds. $H:\mathbb G\to\{0,1\}^\kappa$ is a random oracle. $S$ holds $(m_0,m_1)$, $R$ holds $b$.

$$
\begin{align*}
&\text{Sender}&&&\text{Receiver}\\
&\alpha\xleftarrow{\$}\mathbb Z_p,\quad A\leftarrow g^{\alpha}
&\xrightarrow{A}&\;&\\
&&\xleftarrow{B}&\;&\beta\xleftarrow{\$}\mathbb Z_p,\quad B\leftarrow g^{\beta}A^{b}\\
&k_0\leftarrow H(B^{\alpha}),\quad k_1\leftarrow H\big((B/A)^{\alpha}\big)
&&&k\leftarrow H(A^{\beta})\\
&c_0\leftarrow m_0\oplus k_0,\quad c_1\leftarrow m_1\oplus k_1
&\xrightarrow{c_0,\,c_1}&\;&m_b\leftarrow c_b\oplus k
\end{align*}
$$

**Claim.** $R$ outputs $m_b$.

Correctness: $B/A^{b}=g^{\beta}$, so $(B/A^{b})^{\alpha}=g^{\alpha\beta}=A^{\beta}$, i.e. $k_b=k$.

Security: $B=g^{\beta}A^{b}$ is uniform in $\mathbb G$ for both $b=0,1$, so $S$ learns nothing about $b$. To obtain $k_{1-b}$, $R$ must compute $(B/A^{1-b})^{\alpha}=A^{\beta}\cdot g^{\pm\alpha^2}$, and computing $g^{\alpha^2}$ from $A=g^{\alpha}$ is equivalent to CDH.

A batch of $\ell$ instances reuses $\alpha$ and $A$, with $H$ additionally absorbing the instance index; each party does about one exponentiation per instance.

**Malicious receiver.** For a malicious $R$, the simulator can only read $b$ from $R$'s queries to $H$ (whether it queries $B^{\alpha}$ or $(B/A)^{\alpha}$). But $R$ can delay its queries until after receiving $c_0,c_1$, while the simulator must ask the functionality for $m_b$ before that in order to construct $c_0,c_1$. Hence CO cannot be used directly as a UC-secure base OT. CSW, the default in emp-ot, adds a challenge–response round on top of CO, forcing $R$ to query $H$ before $S$ accepts. PVW and BMM take another route, replacing DH with PKE: $R$ generates two public keys and holds the secret key for only one of them.

## IKNP: COT extension

**Motivation.** In the previous section each OT costs one public-key operation. IKNP runs only $\kappa$ base OTs, and afterwards produces $m\gg\kappa$ COTs using a PRG and XOR.

**Objects.**

- $\Delta\in\mathbb F_2^{\kappa}$: the correlation of $S$; its $j$-th bit is $\Delta_j$.
- $r\in\mathbb F_2^{m}$: the choice vector of $R$; its $i$-th bit is $r_i$.
- $G:\{0,1\}^{\kappa}\to\mathbb F_2^{m}$: a PRG.
- $k_{j,0},k_{j,1}\in\{0,1\}^{\kappa}$, $j\in[\kappa]$: the base OT seeds sampled by $R$.
- $T,U,Q\in\mathbb F_2^{m\times\kappa}$: column $j$ is $T_{*,j}\in\mathbb F_2^{m}$, row $i$ is $T_{i,*}\in\mathbb F_2^{\kappa}$. $T,U$ are computed by $R$, $Q$ by $S$.

**Protocol.** The base OT roles are reversed: $R$ acts as the base OT sender, and $S$ uses $\Delta_j$ as its choice.

$$
\begin{align*}
&\text{Sender}&&&\text{Receiver}\\
&\text{choice }\Delta_j,\ \text{gets }k_{j,\Delta_j}
&\xleftarrow{\ \mathsf{OT}\big((k_{j,0},k_{j,1});\,\Delta_j\big),\ j\in[\kappa]\ }&\;&(k_{j,0},k_{j,1})\xleftarrow{\$}\{0,1\}^{\kappa}\times\{0,1\}^{\kappa}\\
&&&&T_{*,j}\leftarrow G(k_{j,0}),\quad U_{*,j}\leftarrow G(k_{j,0})\oplus G(k_{j,1})\oplus r\\
&Q_{*,j}\leftarrow G(k_{j,\Delta_j})\oplus\Delta_j U_{*,j}
&\xleftarrow{U}&\;&\\
&q_i\leftarrow Q_{i,*}&&&t_i\leftarrow T_{i,*}
\end{align*}
$$

**Claim.** For each $i\in[m]$,

$$
t_i=q_i\oplus r_i\Delta,
$$

i.e. $m$ COTs with correlation $\Delta$.

Correctness: column-wise,

$$
Q_{*,j}=G(k_{j,\Delta_j})\oplus\Delta_j\big(G(k_{j,0})\oplus G(k_{j,1})\oplus r\big)=G(k_{j,0})\oplus\Delta_j r=T_{*,j}\oplus\Delta_j r .
$$

Reading row $i$ gives $Q_{i,j}=T_{i,j}\oplus r_i\Delta_j$.

Security (semi-honest): the view of $S$ is $U$ and $k_{j,\Delta_j}$. Each column $U_{*,j}$ is masked by $G(k_{j,1-\Delta_j})$, a seed $S$ does not have, so by PRG security $U$ is independent of $r$. The view of $R$ consists only of the base OTs, and $\Delta$ is protected by the sender security of the base OT. Afterwards, as in the first section, use $H(i,\cdot)$ to turn these into random OTs, then derandomize.

**Cost.** $\kappa$ base OTs, $m\kappa$ bits of communication, $2\kappa$ PRG expansions, compared with doing $m$ base OTs directly.

SoftSpoken is a generalization of the same construction: replace the 1-out-of-2 base OT of column $j$ with small-field VOLE over $\mathbb F_{2^k}$, merging every $k$ columns into one; communication drops to $m\kappa/k$ bits, while computation rises to about $2^k/k$ PRG calls per COT. IKNP is $k=1$.

## Malicious IKNP: KOS check

**Attack.** The security above assumes $R$ uses the same $r$ in every column. A malicious $R$ instead uses $\rho_j\in\mathbb F_2^{m}$ in column $j$, where $\rho_j$ differs from $r$ only in the $i$-th bit. Then

$$
t_i=q_i\oplus r_i\Delta\oplus\Delta_j e_j,
$$

where $e_j$ is the $j$-th unit vector. $R$ tries $H(i,t_i\oplus\Delta_j e_j)$ once for each $\Delta_j\in\{0,1\}$, sees which one decrypts $c_{r_i}$, and thereby learns $\Delta_j$; doing this once for each of $\kappa$ instances yields all of $\Delta$, after which it can open both messages of every other instance.

**Objects.** View $\mathbb F_2^{\kappa}$ as $\mathbb F_{2^\kappa}$, with multiplication written $\cdot$. $\chi_i\in\mathbb F_{2^\kappa}$, $i\in[m]$, are random coefficients that $S$ chooses only after receiving $U$.

**Protocol.** After the IKNP step above and before $q_i,t_i$ are used:

$$
\begin{align*}
&\text{Sender}&&&\text{Receiver}\\
&\chi_1,\dots,\chi_m\xleftarrow{\$}\mathbb F_{2^\kappa}
&\xrightarrow{\chi_1,\dots,\chi_m}&\;&\\
&&\xleftarrow{x,\,t}&\;&x\leftarrow\bigoplus_{i}r_i\chi_i,\quad t\leftarrow\bigoplus_{i}\chi_i\cdot t_i\\
&q\leftarrow\bigoplus_{i}\chi_i\cdot q_i,\quad t\stackrel{?}{=}q\oplus x\cdot\Delta&&&
\end{align*}
$$

Abort if they are not equal.

**Claim.** An honest $R$ always passes; a cheating $R$ incurs an abort probability of $1/2$ for each bit of $\Delta$ it tries to learn.

Correctness:

$$
\bigoplus_i\chi_i\cdot t_i=\bigoplus_i\chi_i\cdot(q_i\oplus r_i\Delta)=q\oplus\Big(\bigoplus_i r_i\chi_i\Big)\cdot\Delta=q\oplus x\cdot\Delta .
$$

Security: if $R$ used $\rho_j\neq r$ in column $j$, then $t_i=q_i\oplus r_i\Delta\oplus d_i$, where the $j$-th bit of $d_i\in\mathbb F_2^{\kappa}$ is $\Delta_j(\rho_{j,i}\oplus r_i)$. For $R$ to pass by sending arbitrary $(x',t')$, it needs

$$
t'\oplus x'\cdot\Delta=q\oplus\bigoplus_i\chi_i\cdot d_i .
$$

The right-hand side depends on $\Delta_j$ for every inconsistent column $j$, and $R$ does not know $\Delta_j$, so it can only guess. Each wrong guess causes an abort; the probability of guessing $c$ of them correctly is $2^{-c}$. This is no different from $R$ not cheating and directly guessing $c$ bits of $\Delta$; the entropy of the remaining $\kappa-c$ bits is absorbed by the slack in $\kappa$.

$x$ is a linear function of $r$ whose coefficients are known to $S$, and $t$ likewise leaks a linear combination of the $t_i$. Fix: $R$ extends $r$ by $\kappa$ uniformly random bits; these rows only take part in the check and are then discarded, and their contributions one-time pad $x$ and $t$.

Two preconditions: $\chi_i$ must be fixed only after $R$ sends $U$, which implementations derive via Fiat–Shamir from a hash of the transcript; the base OT must be secure against a malicious party, otherwise $R$ can cheat in the base OT and obtain both seeds.

## Code notes (emp-ot)

The mathematical protocol is as above; implementation differences:

- `ot.h`: `RandomCOT::recv_cot` sends $d_i=r_i\oplus b_i$, and `COT::send` constructs $c_0,c_1$, i.e. the derandomization of the first section. The choice bit is not stored separately; instead the convention $\mathrm{LSB}(\Delta)=1$, $\mathrm{LSB}(q_i)=0$ gives $\mathrm{LSB}(t_i)=r_i$.
- `base_ot/co.h`: `CO::send` reuses $A$ for the whole batch, and computes $(B/A)^{\alpha}$ as $B^{\alpha}\cdot A^{-\alpha}$; $H$ absorbs the session id and the instance index.
- `ot_extension/iknp.h`: $\chi_i$ is derived via Fiat–Shamir from `io->get_digest()`; every 128 rows are first packed into one $\mathbb F_{2^{128}}$ element with `GaloisFieldPacking` before the $\chi$ linear combination; the extra 128 COTs are generated and sacrificed in `end()`.

## References

- Beaver, [Precomputing Oblivious Transfer](https://link.springer.com/chapter/10.1007/3-540-44750-4_8), CRYPTO 1995.
- Impagliazzo, Rudich, [Limits on the Provable Consequences of One-way Permutations](https://dl.acm.org/doi/10.1145/73007.73012), STOC 1989.
- Chou, Orlandi, [The Simplest Protocol for Oblivious Transfer](https://eprint.iacr.org/2015/267), LATINCRYPT 2015.
- Canetti, Sarkar, Wang, Blazing Fast OT for Three-Round UC OT Extension, PKC 2020.
- Ishai, Kilian, Nissim, Petrank, [Extending Oblivious Transfers Efficiently](https://www.iacr.org/archive/crypto2003/27290145/27290145.pdf), CRYPTO 2003.
- Keller, Orsini, Scholl, [Actively Secure OT Extension with Optimal Overhead](https://eprint.iacr.org/2015/546), CRYPTO 2015.
- Roy, [SoftSpokenOT](https://eprint.iacr.org/2022/192), CRYPTO 2022.
