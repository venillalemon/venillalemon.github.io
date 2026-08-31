# Polynomial Commitment Schemes and Fiat-Shamir

*January 26, 2026*

## Polynomial commitment based on discrete-log and pairing

### KZG: pairing

We have $G$  as a group of prime order $p$  with generator $g$ . We have a bilinear map $e:G\times G\to G_T$  where $G\cong G_T\cong C_p$  are $p$ -order cyclic groups. We use $\mathcal{F}=\mathbb{F}_p^{\leq d}[X]$ , and the public parameters $gp$  are generated as

$$
(g,g^\tau,g^{\tau^2},\dots,g^{\tau^d})\leftarrow\mathsf{setup}(\lambda,\mathcal{F};\tau)
$$

where $\tau$  is a random element in $\mathbb{F}_p$ ; after computing, abort the random $\tau$ . To commit to a polynomial $f(X)=\sum_{i=0}^d f_iX^i$ , we compute

$$
\prod_{i=0}^d (g^{\tau^i})^{f_i}\leftarrow\mathsf{commit}(gp, f).
$$

In the evaluation phase, with input $u$ , the prover sends $v$  and a proof $\pi$  for the verifier to verify $f(u)=v$  using $\pi$ . The idea is if $f(u)=v$ , then $f(X)-v$  is divisible by $X-u$ . Let $q(X)=(f(X)-v)/(X-u)$ , then the proof is written as $\pi=g^{q(\tau)}$  and $(v,\pi)\leftarrow\mathsf{open}(gp,f,u)$ . The verifier checks if $e\left(g^{\tau-u},\pi\right)=e\left(\frac{\mathsf{com}_f}{g^{v}}, g\right)$ . The verifier knows $g^{\tau-u}$  because it knows $g^\tau$  from the global parameter and it can compute $g^u$  from $u$ .

Time: commit $O(d)$  group exponentiations, open (including computing $q$ ) $O(d)$  group exponentiations and $O(d)$  group multiplications, verify $O(1)$  pairings. Size: proof and commitment are both $O(1)$  group elements.

The completeness is trivial. For soundness, if the prover outputs another $(v',\pi')$  such that $f(u)\not=v'$  and $e\left(g^{\tau-u},\pi'\right)=e\left(\frac{\mathsf{com}_f}{g^{v'}}, g\right)$ , then we have (denote $\delta=f(u)-v'$ ):

$$
e\left(\frac{\mathsf{com}_f}{g^{v'}}, g\right)=e\left(g^{f(\tau)-f(u)+\delta}, g^{}\right)=e\left(g^{q(\tau)+\frac{\delta}{\tau-u}}, g^{\tau-u}\right)=e\left(g^{\tau-u},\pi'\right)
$$

so as a result

$$
e\left(g, g\right)^{\frac{\delta}{\tau-u}}=\frac{e\left(g,\pi'\right)}{e\left(g, g\right)^{q(\tau)}}
$$

where the operations on the exponent are in $\mathbb{F}_p$  which corresponds to the multiplication in the groups $G$  and $G_T$ . This is the $q$ -**S**trong **B**ilinear **D**iffie-**H**ellman** assumption, which says that it is hard to compute $e(g,g)^{\frac{1}{\tau-u}}$  given $(p,G,g,G_T,e)$  and $gp=(g,g^\tau,\dots,g^{\tau^d})$ .

### Knowledge Soundness

The plain KZG is not knowledge soundness without assumptions like KoE or GGM. We will discuss the assumptions in the PCP-based SNARK.

### Zero-Knowledge-ness

The plain KZG is not zk since the commit algorithm is deterministic. For example, you can use $g^{f(\tau)}$  to test if $f$  is a zero polynomial. Here, we denote the protocol modified to zk in the graph below.

$$
\begin{align*}
&\text{Setup: sample }\tau,\eta\xleftarrow{\$}\mathbb{F}_p\text{ and compute }gp←(g,g^{\tau},\dots,g^{\tau^d},g^\eta);\text{ then delete }\tau,\eta.\\
&\text{Prover}&&&\text{Verifier}\\
&r\xleftarrow{\$}\mathbb{F}_p,\mathsf{com}_f=g^{f(\tau)+r\eta}\leftarrow\mathsf{commit}(gp, f; r)&\xrightarrow{\mathsf{com}_f}&&\\
&r'\xleftarrow{\$}\mathbb{F}_p,v\leftarrow f(u),\pi=\left(g^{q(\tau)+r'\eta},g^{r-r'(\tau-u)}\right)\leftarrow\mathsf{open}(gp, f, u, r;r')&\xleftarrow{u\in\mathbb{F}_p}&\;&\\
&&\xrightarrow{v,\pi}&\;&e\left(\pi_1,g^{\tau-u}\right)e\left(\pi_2,g^{\eta}\right) \stackrel{?}{=} e\left(\frac{\mathsf{com}_f}{g^{v}}, g\right)
\end{align*}
$$

The polynomial is hidden by the random $r'$ .

### Variants of KZG

- For multivariate poly: $f(x_1,\dots,x_k)-f(u_1,\dots,u_k)=\sum_{i\in[k]}(x_i-u_i)q_i(x_1,\dots,x_k)$ . Prover computes and sends $\pi_i=g^{q_i(\tau_1,\dots,\tau_n)}$ . Prover time is $O(km)$  group exponentials where $m\leq 2^k$  is the number of terms of $f$ . [[Chopin]](https://eprint.iacr.org/2026/480.pdf) claims to reduce the prover time to $m+O(\sqrt{m})$  MSMs (compute $\prod_j g_j^{a_j}$ ).

- For batch query on $u_1,\dots,u_m$ : $f(x)-h(x)=q(x)\prod_{i\in[m]}(x-u_i)$  where $h(x)$  is the extrapolation of $(u_i,f(u_i))$ ’s.

- For multi-party, each party has a private number for setup, and the public parameters are (for example, 2-party) $gp=\left(g,g^{st},\dots,g^{(st)^d}\right)$ . The parameters can be generated party after party, since $g^{(st)^i}=\left(g^{s^i}\right)^{t^i}$ .

And it is worth noting that PLONK uses univariate KZG and plonk IOP, while vSQL uses multivariate KZG and sum-check protocol.

### Bulletproofs: discrete-log

KZG requires trusted setup. Here we present Bulletproofs which has transparent setup. The goal of the prover is to convince the verifier that $f(u)=v$  where $f=\sum_{i=0}^{d+1}f_ix^i\in\mathbb{F}_p[X]$ . The setup phase is just a random $gp=(gp_{0,0},\dots,gp_{0,d})\in G$  and we assume $d+1=2^k$  is some exponential of $2$ . Then the prover and verifier go through a interaction shown below:

$$
\begin{align*}
&\text{Prover}
&
&
&\text{Verifier}\\
&\mathsf{com}_f=\prod_{i=0}^{2^k-1}gp_{0,i}^{f_i}\leftarrow\mathsf{commit}(gp, f)
&\xrightarrow{\mathsf{com}_f,v}
&
&\\
\text{round }1:\;
&f=f_0\rightarrow f_L+u^{2^{k-1}}f_R,L=\prod_{i=0}^{2^{k-1}-1}gp_{0,i+2^{k-1}}^{f_{0,i}},R=\prod_{i=2^{k-1}}^{2^k-1}gp_{0,i-2^{k-1}}^{f_{0,i}},v_L=f_L(u),v_R=f_R(u)
&\xrightarrow{L,R,v_L,v_R}
&
&\;\text{``I verify } f_0(u)=v \text{ '': }v\stackrel{?}{=}v_L+v_Ru^{2^{k-1}}\\
&f_1\leftarrow rf_L+f_R
&\xleftarrow{gp_1,r}
&
&gp_1\leftarrow (gp_{0,i}^{r^{-1}}gp_{0,i+2^{k-1}})_{i\in[0,2^{k-1})},r\xleftarrow{\$}\mathbb{F}_p[X],v_1\leftarrow rv_L+v_R,\mathsf{com}_{f_1}\leftarrow L^rR^{r^{-1}}\mathsf{com}_f\\
\text{round }2:\;
&f_1\rightarrow f_L+u^{2^{k-2}}f_R,L=\prod_{i=0}^{2^{k-2}-1}gp_{1,i+2^{k-2}}^{f_{1,i}},R=\prod_{i=2^{k-2}}^{2^{k-1}-1}gp_{1,i-2^{k-2}}^{f_{1,i}},v_L=f_L(u),v_R=f_R(u)
&\xrightarrow{L,R,v_L,v_R}
&
&\text{`` I verify } f_1(u)=v_1 \text{'': }v_1\stackrel{?}{=}v_L+v_Ru^{2^{k-2}}\\
&...
&...
&
&...\\
\text{round }k:\;
&f_{k-1}\rightarrow f_L+uf_R,L=gp_{k-1,1}^{f_{k-1,0}},R=gp_{k-1,0}^{f_{k-1,1}},v_L=f_L(u),v_R=f_R(u)
&\xrightarrow{L,R,v_L,v_R}
&
&\;\text{``I verify } f_{k-1}(u)=v_{k-1} \text{ '': }v_{k-1}\stackrel{?}{=}v_L+v_Ru\\
&f_k\in\mathbb{F}_p\leftarrow rf_L+f_R
&\xleftarrow{gp_k,r}
&
&gp_k\leftarrow (gp_{k-1,0}^{r^{-1}}gp_{k-1,1}),r\xleftarrow{\$}\mathbb{F}_p[X],v_k\leftarrow rv_L+v_R,\mathsf{com}_{f_k}\leftarrow L^rR^{r^{-1}}\mathsf{com}_{f_{k-1}}\\
\text{final }:\;
&
&
&
&\text{`` I verify } f_{k}=v_{k} \text{ as a constant polynomial '': }\mathsf{com}_{f_k}\stackrel{?}{=}gp_{k}^{v_k}\\
\end{align*}
$$

The $r$ ’s at every round is sampled randomly and independently. Then we apply Fiat-Shamir to the protocol. The $gp$ ’s should be computed by the verifier to prevent backdoor in parameters.

Time analysis

- Setup: $O(d)$  sampling

- Commit: $O(d)$  group exponentiations

- Prover: $O(d)$  group exponentiations

- Verifier: $O(d)$  group exponentiations

The proof size is $O(\log d)$  group elements, and the commitment size is $O(1)$  group elements (this is the first commitment $\mathsf{com}_f$ . Other commitments are computed by the verifier).

### **Soundness analysis.**

Statistical soundness: we assume the prover does not know the correct $v$ . The final $f_k$  is a multilinear polynomial of all the random $r$ ’s, say $f_k=g_f(r_1,\dots,r_{k})$  and the function $g_f$  is deterministic. Note that every $f$  corresponds to a unique $g_f$ .

So, conditioned on the prover does not know the correct $v$  but send a $v^*\not=v$  instead, we can say $v^*=f^*(u)$  for some $f^*\not=f$ . Thus by the Schwartz-Zippel lemma, we have

$$
\mathbf{Pr}_{r_1,\dots,r_k\sim \mathbb{F}_p}\left[f^*_k-v_k=g^*(r_1,\dots,r_k)-g(r_1,\dots,r_k)=0\middle|v^*\not=v\right]\leq\frac{k}{p}
$$

Since $v_k\in\mathbb{F}_p$ , $f^*_k=v_k$  if and only if $\mathsf{com}_{f_k}=gp_{k}^{v_k}$ , so the soundness error is at most $\frac{k}{p}=\frac{\log d}{p}$ .

## Polynomial commitment based on linear codes

The motivations to develop code-based commitment scheme are:

- post-quantum secure

- no group exponentiations (only hash, addition and multiplication)

- small global parameters

but the new commitment scheme has larger proof sizes; additionally, without the algebraic structure, it is not homomorphic and harder to aggregate.

The goal of the prover is to prove $f(u)=v$  where $f\in\mathbb{F}_p[X]$  is a degree- $d-1$  polynomial. The value $f(u)$  equals a quadratic form

$$
f(u)=
\begin{bmatrix}1&u&\dots&u^{\sqrt{d}-1}\end{bmatrix}
\begin{bmatrix}f_{0,0}&\cdots&f_{0,\sqrt{d}-1}\\f_{1,0}&\cdots&f_{1,\sqrt{d}-1}\\\vdots&\ddots&\vdots\\f_{\sqrt{d}-1,0}&\cdots&f_{\sqrt{d}-1,\sqrt{d}-1}\end{bmatrix}
\begin{bmatrix}1\\ u^{\sqrt{d}}\\ \vdots\\ u^{(\sqrt{d}-1)\sqrt{d}}\end{bmatrix}
$$

because $f(u)=\mathbf{u}^T\mathbf{F}\mathbf{u}'=\sum_{i=0}^{\sqrt{d}-1}\sum_{j=0}^{\sqrt{d}-1} f_{i,j}u^{i\sqrt{d}+j}$ .

Setup phase samples a random hash function. Then in commit phase, the prover encode each row of $\mathbf{F}$  with a $[n,\sqrt{d}]$  linear code (this encoding is a public algorithm, e.g. Reed-Solomon code), represented by a matrix $\mathbf{C}\in\mathbb{F}_p^{\sqrt{d}\times n}$ . The result is a matrix of $\sqrt{d}\times n$ :

$$
\mathbf{P}=\begin{bmatrix}\mathbf{f}_0\mathbf{C}\\\mathbf{f}_1\mathbf{C}\\\vdots\\\mathbf{f}_{\sqrt{d}-1}\mathbf{C}\end{bmatrix}.
$$

After encoding, use Merkle tree to generate the commitment with the hash function in the global parameters. The leaf nodes are the $n$  columns of the matrix $\mathbf{P}$ . The root hash is the commitment of the function.

Then the prover and verifier go through the following interaction to verify $f(u)=x$ :

$$
\begin{align*}
&\text{Prover}&&&\text{Verifier}\\
&
&\xleftarrow{\mathbf{r}}
&
&\mathbf{r}\xleftarrow{\$}\mathbb{F}_p^{\sqrt{d}}\\
&\mathbf{w}\leftarrow\mathbf{r}^T\mathbf{F}\;(\text{originally we send encoded version }\mathbf{r}^T\mathbf{P}\text{, this is for optimization})
&\xrightarrow{\mathbf{w}}
&\;
&\mathbf{w}\leftarrow\mathbf{w}\mathbf{C}\text{ is indeed a codeword}\\
&
&\xleftarrow{s}
&\;
&s\xleftarrow{\$}\mathbb{F}_p\\
&\text{Generate Merkle proof }\pi\text{ that the }s\text{-th column of }\mathbf{P}\text{ equals to }\mathbf{v}\in\mathbb{F}_p^{\sqrt{d}}
&\xrightarrow{\pi,\mathbf{v}}
&\;
&\text{verify the proof }\pi\text{, and verify }\mathbf{r}^T\mathbf{v}=\mathbf{w}_s\text{, then repeat sampling }s\text{ multiple times}\\
&\mathbf{w}'\leftarrow\mathbf{u}^T\mathbf{F}
&\xrightarrow{\mathbf{w}'}
&\;
&\mathbf{w}'\leftarrow\mathbf{w}'\mathbf{C}\text{ is indeed a codeword}\\
&
&\xleftarrow{s}
&\;
&s\xleftarrow{\$}\mathbb{F}_p\\
&\text{Generate Merkle proof }\pi\text{ that the }s\text{-th column of }\mathbf{P}\text{ equals to }\mathbf{v}\in\mathbb{F}_p^{\sqrt{d}}
&\xrightarrow{\pi,\mathbf{v}}
&\;
&\text{verify the proof }\pi\text{, and verify }\mathbf{r}^T\mathbf{v}=\mathbf{w}'_s\text{, then repeat sampling }s\text{ multiple times}\\
&
&
&\;
&\mathbf{w}'\mathbf{u}'\stackrel{?}{=}x
\end{align*}
$$

Analysis of the protocol is as follows:

- **Keygen**: $O(1)$ , transparent

- **Commit**:

  - Encoding: $O(d \log d)$  field multiplications using Reed-Solomon code, $O(d)$  using linear-time encodable code

  - Merkle tree: $O(d)$  hashes, $O(1)$  commitment size

- **Prover time**: $O(d)$  field multiplications

- **Proof size**: $O(\sqrt{d})$

- **Verifier time**: $O(\sqrt{d})$

## Fast Reed-Solomon IOPP

### Intro: Merkle trees for univariate poly-commitment

An intuitive attempt is to commit to a vector of evaluations of a given polynomial $f\in\mathbb{F}_p^{\leq d}[X]$ . The leaves of the tree are $\{f(x):x\in\mathbb{F}_p\}$  and the tree hashes every neighboring $2$  nodes to form a new layer. When $V$  requires $f(r)$ , the prover sends the hash values along the path up to the root.

The Merkle tree for commitment requires $O(pd)$  field multiplication (using Qin-Horner method) to commit, and the proof size is $O(\log p)$  hash values. The verifier takes $O(\log p)$  hashes. The setup only generates a hash function, so it is transparent.

There are 2 problems:

- The field may be very large; and the time is linear to the max degree.

- The verifier cannot know if $f$  has degree at most $d$ .

### Fix the Problem 1

FRI commitment uses a multiplicative subset of $\mathbb{F}_p$ : $\Omega=\{\omega^i:\omega^n=1,i=0,1,\dots,n-1\}$ , for example, $\{1,3,9,27,-1,-3,-9,-27\}$  in $\mathbb{F}_{41}$ . The leaves of the Merkle tree will be the values $f(\omega^i)$ .

We call the rate $\rho=\frac{d}{n}$  the FRI blowup factor.

### Fix the Problem 2

$$
\begin{align*}
&\text{Prover}
&
&
&\text{Verifier}\\
&f_0=f,\deg f_0\leq k-1,\Omega_0=\{1,\omega,\dots,\omega^{n-1}\},n=\rho^{-1}k
&\xrightarrow{\mathsf{com}_0=\mathsf{MerkleCommit}(f_0|_{\Omega_0})}
&
&\\
\text{round }1:\;
&f_0(X)=f_{0,e}(X^2)+Xf_{0,o}(X^2)
&\xleftarrow{r_1}
&
&r_1\xleftarrow{\$}\mathbb{F}_p\\
&f_1(Z)=f_{0,e}(Z)+r_1f_{0,o}(Z),\deg f_1\leq\frac{k}{2}-1,\Omega_1=\{x^2:x\in\Omega_0\}
&\xrightarrow{\mathsf{com}_1=\mathsf{MerkleCommit}(f_1|_{\Omega_1})}
&
&\\
\text{round }2:\;
&f_1(X)=f_{1,e}(X^2)+Xf_{1,o}(X^2)
&\xleftarrow{r_2}
&
&r_2\xleftarrow{\$}\mathbb{F}_p\\
&f_2(Z)=f_{1,e}(Z)+r_2f_{1,o}(Z),\deg f_2\leq\frac{k}{4}-1,\Omega_2=\{x^2:x\in\Omega_1\}
&\xrightarrow{\mathsf{com}_2=\mathsf{MerkleCommit}(f_2|_{\Omega_2})}
&
&\\
&...
&
&
&...\\
\text{round }\log_2k:\;
&f_{t-1}(X)=f_{t-1,e}(X^2)+Xf_{t-1,o}(X^2)
&\xleftarrow{r_t}
&
&r_t\xleftarrow{\$}\mathbb{F}_p\\
&f_t(Z)=f_{t-1,e}(Z)+r_tf_{t-1,o}(Z),\deg f_t=0,\Omega_t=\{x^{2^{\log_2k}}:x\in\Omega_0\}
&\xrightarrow{\mathsf{com}_t=f_t|_{\Omega_t}\ }
&
&\text{verify that }f_t|_{\Omega_t}\text{ is a constant vector}\\
\text{query }:\;
&\text{对于每个 }j_q,\text{打开从第 }t=\log_2k\text{ 层到第 }0\text{ 层的路径:}\pi_{t,j_q}\leftarrow\text{MerkleOpen}(\mathsf{com}_t,j_q)&\xleftarrow{\{j_q\}_{q=1}^s}
&
&\text{随机选择 }j_1,\dots,j_s\in[0,|\Omega_t|-1]\\
&\\
&\pi_{t-1,j_q^+},\pi_{t-1,j_q^-}\leftarrow\text{MerkleOpen}(\mathsf{com}_{t-1},\text{对应的两个索引})\\
&...
&\xrightarrow{\text{所有打开值}+\text{路径}}
&
&\text{验证每条路径的一致性；同时，}\\
&&&& \text{对于第 }t\text{ 层: }f_t(\omega_t^{j_q})\text{ 是常数}\\
&&&& \text{对于第 }i\text{ 层: 检查}f_{i+1}(z)\stackrel{?}{=}\frac{r_{i+1}+x}{2x}f_i(x)+\frac{r_{i+1}-x}{-2x}f_i(-x)\\
&&&& \text{其中 }z=x^2,x=\omega_i^{j},\omega_i\text{ 是第 }i\text{ 层的生成元}\\
\end{align*}
$$

**Remark.**

- It is easy from $f_i|_{\Omega_i}$  to $f_{i+1}|_{\Omega_{i+1}}$ . This is because $f_{i+1}(x^2)=f_{i,e}(x^2)+r_{i+1}f_{i,o}(x^2)=\frac{f_i(x)+f_i(-x)}{2}+r_{i+1}\frac{f_i(x)-f_i(-x)}{2x}$ . Also, the verifying process relies on this equation.

- To analysis the soundness, we introduce the relative Hamming distance $\mathsf{Ham}_{\Omega}(f,g)=\frac{|\{x\in\Omega:f(x)\not=g(x)\}|}{|\Omega|}$  and $\delta=\min_{h\in\mathbb{F}_p^{\leq k-1}[X]}\left(\mathsf{Ham}_{\Omega}(f,h)\right)$ , which is the distance on $\Omega$  of $f$  to the closest degree- $(k-1)$  polynomial.

- We consider $f$  such that $\delta\leq 1-\sqrt{\rho}$ , which is to say, the $f$  is far from any degree- $(k-1)$  polynomial.

- A cheating prover has a high ($> k-1$ ) degree polynomial $f$ . In case the prover is accepted, either it folds incorrectly, or it folds correctly and is lucky to have those $r_i$ ’s that reduce the degree to $0$  eventually. In the first case, the accept probability is $\left(1-\delta\right)^t$ ; in the second case, the accept probability is at most $\frac{k}{p}$ . As a result, to reach an accept probability $2^{-\lambda}$  ($\lambda$  is the security parameter), $s$  should be $\Omega\left(\frac{\lambda}{\log\rho^{-1}}\right)$ .

(The security proof is problematic.)

### Polynomial commitment from FRI

The FRI introduces another two problems:

- Prover has only committed to evaluations on a subset $\Omega\subset\mathbb{F}_p$ .

- Verifier only knows that $f$  is close to a low-degree polynomial (in the sense of Hamming distance), but not necessarily a low-degree polynomial.

There is an attack to the first problem: the prover can commit to a polynomial $g$  that agrees with $f$  on $T\subset\Omega$  with much lower degree ($|T|=k$ ). Then $\delta<1-\rho<1-\sqrt{\rho}$  and the soundness is broken.

Then to confirm that $f(r)=v$  where $f\in\mathbb{F}_p^{\leq d}[X]$ , the prover applies FRI on the polynomial $(f(x)-v)/(x-r)$ , which has degree at most $d-1$ .

## Fiat-Shamir transform

**Definition. (Interactive Security)** A poly-commitment scheme runs at $\lambda$  bits of interactive security if and only if: assume $P$  cannot find a collision of the hash function in the global parameters, then for every $P^*$ , the probability that $P^*$  can make the verifier accept a false claim is at most $2^{-\lambda}$ .

To find out if a challenge is lucky, the prover should interact with the verifier at least $2^\lambda$  times in average. It is unlikely that $V$  continues to interact after rejecting the same prover so many rounds. So following is the

**Definition. (Non-interactive security)** A poly-commitment scheme runs at $\lambda$  bits of non-interactive security if and only if: for every $P^*$  willing to compute $2^k$  hashs, the probability that $P^*$  can make the verifier accept a false claim is at most $2^{k-\lambda}$ .

In this scheme, a lying $P$  can propose the grinding attack silently, without interacting. This definition is weaker than the interactive security, i.e., if a prover breaks the interactive security of one interactive protocol, then it can also break the non-interactive security of the Fiat-Shamir transform of that protocol.

We show that Fiat-Shamir transform may be insecure. Consider a protocol of the empty language. In this protocol, $P$  sends a nonce, and then $V$  sends a random bit $r$ , and accepts iff $r=1$ . The $V$  accepts iff every round it accepts, so the soundness error is $2^{-\lambda}$  with $\lambda$  rounds. However, the Fiat-Shamir transform of this protocol is insecure, since the prover can grind for a nonce 2 times per round in average, in order to find a nonce that leads to $r=1$  for every round. The cost is $2\lambda$  in average, which is much smaller than $2^\lambda$  and the protocol does not satisfy the non-interactive security.

Applying Fiat-Shamir to a many-round interactive protocol can lead to a huge loss in security, whereby the resulting non-interactive protocol is totally insecure. So we need “round-by-round” soundness to describe the security of an interactive protocol, which means that for every prover in every round, if the prover is not “lucky” enough to make the verifier accept, then the probability that the prover can make the verifier accept in the next round is at most $2^{-\lambda}$ .

The sum-check protocol is round-by-round sound, so its Fiat-Shamir transform is secure.
