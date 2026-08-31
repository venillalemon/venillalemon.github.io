# SNARK Foundations and Functional Commitments

*January 14, 2026*

## Introduction to SNARK

**Interactive proofs** are complete and (statistically) sound, while **interactive arguments** are sound w.r.t computationally bounded prover (computational soundness).

> **Definition (SNARK).**
> A **succinct** (preprocessing) non-interactive argument of knowledge (**SNARK**) is a triple of algorithms $(S, P, V)$ :
>
> - **Setup** $S(C;r)=(pp,vp)$ : Generates public parameters $(pp, vp)$  for the prover and verifier respectively, given a circuit $C$ .
>
> - **Prove** $P(pp, x, w)=\pi$ : Produces a **short** proof $\pi$ , where $\mathsf{len}(\pi) = \mathsf{sublinear}(|w|)$
>
> - **Verify** $V(vp, x, \pi)$ : **Fast to verify**, with verification time: $\mathsf{time}(V) = O_{\lambda}(|x|, \mathsf{sublinear}(|C|))$ ,
>
> that satisfy:
>
> - **Completeness**: For all $x,w$  such that $C(x,w)=0$ , $\mathbf{Pr}\left[\pi \leftarrow P(pp, x, w): V(vp, x, \pi) = 1\right] = 1$ .
>
> - **Knowledge Soundness**: If $V$  accepts, then $P$  “knows” a witness $w$  such that $C(x,w)=0$ .
>
> If the algorithms satisfy:
>
> - **Zero-Knowledge**: The $(C,pp,vp,x,\pi)$  “reveals nothing new” about the witness $w$ .
>
> then the scheme is called a **zk-SNARK**.

Strong SNARK: all sublinear terms are $\log(|C|)$ .

So in SNARK, prover can not simply send a $w$ , for $w$  might be long ($|w|\leq |C|$ ) and it may be hard to verify $C(x,w)=0$ .

Observe that $S$  is randomized for setup phase. If $r$  is revealed to $P$ , it can prove false statements. This is because while $vp$  is visible from $P$ , it can hide some key structures invisible from $P$  without knowing the random $r$ .

The pre-processing has different types:

- **transparent setup**: $S(C)$  uses no random bit.

- **trusted but universal setup**: $S=(S_{\text{init}}, S_{\text{index}})$ , $S_{\text{init}}(r)=gp$  generates global parameters with secret $r$ , $S_{\text{index}}(gp,C)=(pp,vp)$  is deterministic.

- **trusted setup per circuit**: $S(C;r)$  uses random bits for every circuit $C$ .

### Argument of Knowledge

Here we use trusted but universal setup.

> **Definition (Adaptive Knowledge Soundness).** A preprocessing NARK $(S, P, V)$  is **(adaptively) knowledge sound** for a circuit $C$  if for every **polynomial-time** adversary $A = (A_0, A_1)$  such that:
>
> $$
> \begin{aligned}
> & gp \leftarrow S_{\text{init}}(1^\lambda;r), \\
> & (C, x, \text{st}) \leftarrow A_0(gp), \\
> & (pp, vp) \leftarrow S_{\text{index}}(C), \\
> & \pi \leftarrow A_1(pp, x, \text{st})
> \end{aligned}
> $$
>
> and
>
> $$
> \Pr[V(vp, x, \pi) = \text{accept}] > 1/10^6 \quad (\text{non-negligible w.r.t. } \lambda)
> $$
>
> there exists an efficient extractor $E$  (that uses $A$ ) such that:
>
> $$
> \begin{aligned}
> & gp \leftarrow S_{\text{init}}(1^\lambda;r), \\
> & (C, x, \text{st}) \leftarrow A_0(gp), \\
> & w \leftarrow E^A(gp, C, x)
> \end{aligned}
> $$
>
> and

$$
\Pr[C(x, w) = 0] > 1/10^6 - \epsilon \quad (\text{for a negligible } \varepsilon\text{ w.r.t. } \lambda).
$$

Adversary chooses $(C, x)$  after seeing $gp$  (adaptive), then produces a proof $\pi$ . If $A$  produces an accepting proof with non-negligible probability, then $E$  can extract a valid witness $w$  with essentially the same probability (up to negligible $\varepsilon$ ).

After intro, we proceed to constructing a SNARK, which uses 2 building blocks, one is functional commitment scheme, and the other is interactive oracle proof. The former is a cryptographic object and the latter is an information-theoretical object.

### Building Blocks 1: functional commitment scheme

> **Definition (Commitment Scheme)**. A commitment scheme consists of
>
> - $\mathsf{setup}(1^\lambda)\to gp$ , outputs public parameters $gp$
>
> - $\mathsf{commit}(gp, f, r)\to \mathsf{com}$ , commitment to $f \in \mathcal{F}$  with $r \in \mathcal{R}$  randomly chosen
>
> - $\mathsf{open}(\mathsf{com}, f, r)$ : if $\mathsf{com} = \mathsf{commit}(gp, f, r)$ , then $\mathsf{open}(\mathsf{com}, f, r) = 1$ ; otherwise $\mathsf{open}(\mathsf{com}, f, r) = 0$
>
> satisfying hiding and binding properties:
>
> - **Binding**: for all PPT adversary $\mathcal{A}$ ：
>
> $$
> \Pr\left[
> \begin{array}{l}
> gp \leftarrow \mathsf{setup}(1^\lambda) \\
> (\mathsf{com}_f, f_0, r_0, f_1, r_1) \leftarrow \mathcal{A}(gp)
> \end{array}
> :
> \begin{array}{l}
> (f_0, r_0) \neq (f_1, r_1) \\
> \wedge \; \mathsf{com}_f = \mathsf{Commit}(gp, f_0, r_0) \\
> \wedge \; \mathsf{com}_f = \mathsf{Commit}(gp, f_1, r_1)
> \end{array}
> \right] \le \mathsf{negl}(\lambda)
> $$
>
> - **Hiding**: for all PPT adversary $\mathcal{A}=(\mathcal{A}_1,\mathcal{A}_2)$ :
>
> $$
> \left|
> \Pr\left[
> \begin{array}{l}
> gp \leftarrow \mathsf{Setup}(1^\lambda) \\
> (f_0, f_1, st) \leftarrow \mathcal{A}_1(gp) \\
> b \leftarrow \{0,1\}, \; r \leftarrow \mathcal{R} \\
> com_f \leftarrow \mathsf{Commit}(gp, f_b, r) \\
> b' \leftarrow \mathcal{A}_2(st, com_f)
> \end{array}
> : b' = b
> \right] - \frac{1}{2}
> \right| \le \mathsf{negl}(\lambda)
> $$
>
> also defined as computational indistinguishability.
>
> Note: the $r$  in the open algorithm is the same as that in the commit algorithm.

After sender’s commitment, the sender should also send $(x,r)$  for the receiver to verify. For example, if I want to play paper-scissors-rock with a friend remotely: first we determine our choices; then we send the commitments to each other; finally we send the choice and the random bits used and verify the commitments sent by one another.

To hide the message along the interaction (also, to make the proof short instead of $(x,r)$ ), we define functional commitment scheme.

> **Definition (Functional Commitment Scheme)**. A **functional commitment scheme** for $\mathcal{F}=\{f:X\mapsto Y\}$ :
>
> - $\mathsf{setup}(1^\lambda)\to gp$ , outputs public parameters $gp$
>
> - $\mathsf{commit}(gp, f, r)\to \mathsf{com}_f$ , commitment to $f \in \mathcal{F}$  with $r \in \mathcal{R}$ , which is a **binding** (and **hiding** for zk-SNARK) commitment scheme for $\mathcal{F}$
>
> - $\mathsf{eval}(P, V)$ : for a given $\mathsf{com}_f$  and all $x \in X$ :
>
> $$
> \mathsf{open}(gp, f, x, r) \to \text{short proof } \pi\text{ and value }y\in Y
> $$
>
>
>
> $$
> \mathsf{verify}(gp, \mathsf{com}_f, x, y, \pi) \to \text{accept/reject}
> $$
>
> satisfying
>
> - **Completeness**: If $f \in \mathcal{F}$  and $x \in X$  with $f(x)=y$ , then $\Pr[V(gp, \mathsf{com}_f, x, y, \pi) = \mathsf{accept}] = 1$ .
>
> - **Knowledge Soundness**: $(\mathsf{setup}\;\|\;\mathsf{commit}, \mathsf{open}, \mathsf{verify})$  is knowledge sound.
>
> The interaction within $\mathsf{eval}(P,V)$  is actually a SNARK for the relation (circuit)
>
> $$
> \{(gp,\mathsf{com}_f,x,y): \exists (f,r),f(x)=y, f\in\mathcal{F},\mathsf{com}_f=\mathsf{commit}(gp, f, r)\}
> $$
>
> whose witness is essentially $(f,r)$ . The proof $\pi$  actually proves that $f\in\mathcal{F}$ , $f(x)=y$  and $\mathsf{com}_f$  is a commitment to $f$ .

The definition above essentially illustrates an interactive process. It is like the verifier “queries” the oracle $f$  at $x$  with an additional cost of verifying.

$$
\begin{align*}
&\text{Prover}&&&\text{Verifier}\\
&r\xleftarrow{\$}R,\mathsf{com}_f\leftarrow\mathsf{commit}(gp, f, r)&\xrightarrow{\mathsf{com}_f}&&\\
&&\xleftarrow{x}&\;&x\xleftarrow{\$} X\\
&y\leftarrow f(x),\pi\leftarrow\mathsf{open}(gp, f, x, y, r)&\xrightarrow{y,\pi}&\;&\mathsf{verify}(gp, \mathsf{com}_f, x, y, \pi) \to \text{accept/reject}
\end{align*}
$$

With the scheme above we **commit to** a function. The $\mathcal{F}$  vary from many different function classes.

- Polynomial commitments: $\mathcal{F} = \mathbb{F}^{\leq d}[X]$

- Multilinear commitments: $\mathcal{F} = \mathbb{F}^{\leq 1}[X_1, \ldots, X_n]$ , where the degree is defined the maximum degree of the polynomial in every variable ($\leq1$  means multilinear)

- Vector commitments: $\mathcal{F} = \{f_u: [n] \to \mathbb{F}:f(i) = u_i,u\in\mathbb{F}^n\}$

- Inner product commitments: $\mathcal{F} = \{f_{u}: \mathbb{F}^n \to \mathbb{F}:f_{u}(v) = \langle u,v\rangle, u\in\mathbb{F}^n\}$

### Building Blocks 2: $\mathcal{F}$ -Interactive Oracle Proof

IOP is a proof system that proves the prover knows $w$  such that $C(x,w)=0$ . The verifier uses oracles of $f\in\mathcal{F}$ , which is later replaced by functional commitments to construct a SNARK; here we use oracles.

> **Definition (** $\mathcal{F}$ **-IOP)**: An $\mathcal{F}$ -IOP is a proof system that proves $\exists w,\;C(x,w)=0$  and consists of
>
> - $\mathsf{setup}(1^\lambda)\to pp,vp=(\mathsf{Oracle}_{f_{-s}},\dots,\mathsf{Oracle}_{f_{0}})$
>
> - At round $i\in[t]$ , prover $P$  sends $\mathsf{Oracle}_{f_i}$  where $f_i$  is based on the interaction history from view of $P$ ; verifier sends $r_i\xleftarrow{\$} R$  unless $i=t$ .
>
> - $\mathsf{verify}^{\mathsf{Oracle}_{f_{-s}},\dots,\mathsf{Oracle}_{f_t}}(vp,x,r_1,\dots,r_{t-1})$  uses $(f_i)_{i=-s}^t$  as oracles and output the result.
>
> which satisfies
>
> - **Completeness: **If** ** $\exists w,\;C(x,w)=0$ , then the verifier is bound to accept
>
> - **Knowledge Soundness**: if we use $\mathsf{com}_f$ ’s for $\mathsf{Oracle}_f$ ’s, the extractor can use $(f_{i})_{i=-s}^t$  to compute $w$  because the functional commitment scheme is knowledge sound (functional commitment scheme is actually a SNARK).
>
> - (Optional) **Zero-Knowledge**
