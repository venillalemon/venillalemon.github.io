# Universal Composability

*March 20, 2026*

## The Universal Composability framework

The UC framework allows us to formally define the security property and make combinations of different protocols.

There are many details, which includes the interactions of parties in the ideal world and real world. Refer to [A Graduate Course in Applied Cryptography](https://algebraic-arima.github.io/books/appliedcrypto.pdf). The key idea is, the simulator simulates to the environment $\mathcal{Z}$ everything the real-world environment sees, for every adversaries proposing every possible attacks in the real world.

### Intro: composability

Consider the following two protocols: the first one is a PKE-based key exchange protocol

$$
\begin{align*}&\text{Alice: }(A,B,pk_A,sk_A, pk_B)&&&\text{Bob: }(A,B,pk_B,sk_B,pk_A)\\&N_A\leftarrow_R \{0,1\}^n&&\xrightarrow{\quad \mathrm{Enc}_{pk_B}(N_A,A,B)\quad}&\\&N_B=\mathrm{Dec}_{sk_A}(\dots)&&\xleftarrow{\quad \mathrm{Enc}_{pk_A}(N_A,N_B,A,B)\quad}&N_B\leftarrow_R \{0,1\}^n\\&N_B&&\xrightarrow{\quad \mathrm{Enc}_{pk_B}(N_B)\quad}&N_A=\mathrm{Dec}_{sk_B}(\dots),\;N_B\end{align*}
$$

$A,B$ are meta-data pre-known to both parties to ensure the decryption is valid; $pk$ ’s are public. The second one is a one-time pad encryption protocol, where Alice sends message $m$ by masking it with the shared key: $c=N_B\oplus m$.

The composition of these protocol is not secure: here is where Carol comes in.

$$
\begin{align*}&\text{Alice: }(A,B,pk_A,sk_A, pk_B,m)&&&\text{Bob: }(A,B,pk_B,sk_B,pk_A)\\&N_A\leftarrow_R \{0,1\}^n&&\xrightarrow{\quad \mathrm{Enc}_{pk_B}(N_A,A,B)\quad}&\\&N_B=\mathrm{Dec}_{sk_A}(\dots)&&\xleftarrow{\quad \mathrm{Enc}_{pk_A}(N_A,N_B,A,B)\quad}&N_B\leftarrow_R \{0,1\}^n\\&N_B&&\xrightarrow{\quad \mathrm{Enc}_{pk_B}(N_B)\quad}&\text{Carol takes control over the channel 😈}\\&c=N_B\oplus m&&\xrightarrow{\quad c\quad}&\text{Guess }m'\text{ and sends to Bob }\text{Enc}_{pk_B}(c\oplus m')\end{align*}
$$

If Carol is lucky enough (Carol only needs to win for one time) he would guess the correct $m$ that makes Bob accept. This attack assumes that $B$ tends to receive different messages and try decrypting all of them. (In network practice this is common, for example, re-transmission.)

Note that we shall not consider enumerating through the message space and compare the encryption with $\mathrm{Enc}_{pk_B}(N_B)$. This attack only works with deterministic encryption schemes, which is not IND-CPA secure.

### Proof strategies

Real world: $\mathcal{Z}$, $\mathcal{C}$, $P$, $\mathcal{A}$ for environment, public channel, parties, and adversary. The environment tells which parties to be corrupt and the only adversary controls the corrupted parties (sends input if malicious; read-only when honest-but-curious).

Ideal world: $\mathcal{Z}$, $\mathcal{F}$, $S$ for environment, ideal functionality, and simulator. The simulator only interacts with corrupted parties and simulates all the messages that the environment receives in the real world.

All the parties are modelled as interactive Turing machines. We assume they (together) runs in polynomial time of secure parameters.

We say that $\Pi$ **securely implements** $\mathcal{F}$ **against** $\mathcal{A}$ if there exists a simulator $S$ (which may depend on $\mathcal{A}$ / use $\mathcal{A}$ as oracle) that is compatible with $\mathcal{F}$, such that for every well-behaved environment $\mathcal{Z}$,

$$
\operatorname{Exec}_{\Pi, \mathcal{A}, \mathcal{Z}} \approx \operatorname{Exec}_{\mathcal{F}, \mathcal{S}, \mathcal{Z}}.
$$

And if $\Pi$ is secure against all $\mathcal{A}$, we say that $\Pi$ securely implements $\mathcal{F}$. Note that in real world, $\Pi$ represents the honest parties; in ideal world, the honest parties only forwards their inputs from the environment (so they are merely wires).

In the real world, every variable that $\mathcal{Z}$ sees is either from the input of the adversary (from an honest party to the trivial adversary, i.e. directly to $\mathcal{Z}$), or from the output of the adversary (in fact sent directly by $\mathcal{Z}$ through trivial adversary). So a simulator should

- Read the outputs of the adversary, pretending to have output them and at the same time ensure the fidelity of the data that the environment sees;

- Forge the inputs of the adversary, since there are no way of simulator knowing anything of the input of the adversary.

### Universal composition

Since all parties are modelled as ITM, it is natural to compose different parties into a larger ITM. Utilizing this property, we derive lemmas concerning the trivial adversary, concurrency, subprotocol composition and transitivity.

### Maliciously secure 3-party OT protocol

Helper $P_h$, sender $P_s$, receiver $P_r$:

**Setup.** Helper has $p_0,p_1\leftarrow_R \mathcal{M}$, $r_0,r_1\leftarrow_R \mathcal{R}$; then sends $(p_0,p_1,r_0,r_1)$ to sender; then $b\leftarrow_R\{0,1\}$ and sends $(b,p_b,r_b,c_{1\oplus b}=H(p_{1\oplus b},r_{1\oplus b}))$ to the receiver.

**Check.** Receiver sends $(b,c_b=H(p_b,r_b),c_{1\oplus b})$ to the sender, whereafter the sender checks if $c_0=H(p_0,r_0)$ and $c_1=H(p_1,r_1)$.

**Request.** Receiver sends $\tau=b\oplus\sigma$ to sender. Sender computes $e_0=m_0\oplus p_\tau$ and $e_1=m_1\oplus p_{1\oplus \tau}$, then sends them back to the receiver.

**Compute.** Sender gets $e_\sigma\oplus p_b$.

(I mistake $p$ for $c$ in the above protocol. Since the receiver knows $c_0,c_1$ it can has $m_0,m_1$ by computing $e_{1\oplus\sigma}\oplus c_{1\oplus b}$. But in the correct protocol, the receiver only knows $p_b$.)

### A failed **BMR**

**The following protocol fails under mixed corruption (one garbler and one evaluator is semi-honest)**

Point-and-Permute 在 $n$ 方的推广。一个 Evaluator，多个 Garbler。

**Garble**: 首先每个 $P_i$ 为每个 wire $a$ 随机选 label $a_0^{(i)},a_1^{(i)}$ 和 pad $r_a^{(i)}$, $p_a^{(i)}$.

对于 gate $g$ 假设 input wire 是 $a,b$ ，output wire 是 $c$ 。假设目前所有人都已知 $p_{a,0},p_{a,1},p_{b,0},p_{b,1},r_a,r_b$ 。打开

$$
p_{c,0}\gets\bigoplus_{i\in[n]}p_c^{(i)}, \quad r_c\gets\bigoplus_{i\in[n]}r_c^{(i)}.
$$

并且令对于 $x\in\{0,1\}$,

$$
c_{x}=c_x^{(1)}\|\cdots\|c_x^{(n)}\|p_{c,x},\quad p_{c,x}=x\oplus p_{c,0},
$$

然后计算

$$
e_{v_a,v_b}\gets c_{g(v_a,v_b)\oplus r_c}\oplus\left(\bigoplus_{i\in[n]} H(a^{(i)}_{v_a\oplus r_a},b^{(i)}_{v_b\oplus r_b},\mathrm{id})\right)
$$

并放在表格的 $(p_{a,v_a},p_{b,v_b})$ 处。

**Evaluate**: 假设对于这个门 $g$ ，拿到了两个 label $a_{v_a\oplus r_a},b_{v_b\oplus r_b}$ ，那么其末位 bit 分别是 $p_{a,v_a\oplus r_a},p_{b,v_b\oplus r_b}$. 由于知道 $r_a,r_b$, 可以计算

$$
p_{a,v_a}=p_{a,v_a\oplus r_a}\oplus r_a,p_{b,v_b}=p_{b,v_b\oplus r_b}\oplus r_b.
$$

去表格中对应位置找即可得到 $e_{v_a,v_b}$ 然后可恢复出 $c_{g(v_a,v_b)\oplus r_c}$.
