# MPC: Secret Sharing

*March 15, 2026*

Suppose we have a function $f$ with $n$ inputs and $m$ outputs. The goal of MPC is to develop a protocol for $N$ parties where every input is submitted by one party and every output is obtained by some parties. There are some informal descriptions of the security:

- **privacy**: no party learns anything about any other party's inputs (except for information that is inherently revealed by the outputs);

- **soundness**: honest parties compute correct outputs (if they compute any output at all);

- **input independence**: all parties must choose their inputs independently of the other parties' inputs.

And there are assumptions

- **cryptographic assumptions**

- **number of corrupt parties**

- **communication**: synchronous or asynchronous

- **type of corruption**: malicious or honest-but-curious (of the things to do), static or adapted (of which party to corrupt)

## Intro: Beaver’s protocol

The beaver’s protocol securely computes the output of the arithmetic circuits over $\mathbb{F}_q$ among $2$ parties.

### Basic Idea

To achieve privacy, it is an intuition to split the key value into several parts, and distribute them to different parties. We use $[x]$ to denote a share of value $x$, meaning $[x]=(x_1,x_2)$ where $x=x_1+x_2$. And define

- $[x]+[y]=(x_1+y_1,x_2+y_2)$

- $c[x]=(cx_1,cx_2)$

- $[x]+c=(x_1+c,x_2)$ (I am curious whether it is more secure to split the constant randomly, not just always add it on one side.)

The add gate, scalar multiplication gate and constant add gate is linear; the two parties can compute independently. The multiplication gate needs the *dealer* to generate a random **Beaver triple sharing**: $([a],[b],[c])$ where $c=ab$.

Suppose the two parties are computing the multiplication of $[x]$ and $[y]$. The dealer sends $a_i,b_i$ to $P_i$ each, and the two parties compute $[u]=[x]-[a]$ and $[v]=[y]-[b]$. Then the two parties open the shares $[u],[v]$ to each other so that they both know $u=x-a,v=y-b$, and uses their own share to compute

$$
[z]=uv+u[b]+v[a]+[c].
$$

For example, the party $i$ computes $z_i=uv\times\mathbf{1}_{i=1}+ub_i+va_i+c_i$ and we can verify that $z_1+z_2=uv+ub+va+ab=xy$.

**Bootstrapping.** Suppose $P_i$ has $x$. It randomly picks $x_i$ and send $x-x_i$ to another party. This forms a sharing.

To sum up, the complete semi-honest protocol runs as follows. Suppose the circuit contains $m$ multiplication gates.

- **Setup (offline, input-independent).** For each multiplication gate $j=1,\dots,m$, the dealer samples random $a_j,b_j$, sets $c_j=a_jb_j$, splits each of them randomly and sends $(a_{ij},b_{ij},c_{ij})$ to $P_i$. Every multiplication gate consumes a fresh triple. All of this happens before any input is fixed, so the dealer’s messages are independent of the inputs.

- **Input sharing.** Each party shares its own inputs by bootstrapping as above. The dealer never touches the inputs, so it learns nothing about the data by construction. (The owner of $x$ trivially knows both shares of its own input; this is harmless, since sharing hides a value only from parties who do not already know it.)

- **Evaluation.** Gate by gate: linear gates are computed locally, and each multiplication gate consumes one fresh triple as above.

- **Output.** The two parties open the shares of the output wires and add them up.

### Maliciously secure Beaver’s protocol: authenticated secret sharing

A malicious participant would send a wrong number when opening their shares. We introduce **authenticated sharing** $\llbracket x \rrbracket:=([x],[x^{(1)}],[x^{(2)}])$ where $P_i$ has $(x_i,x^{(1)}_i,x^{(2)}_i)$ and summing over $i$ reveals the original content $(x,x^{(1)},x^{(2)})$. Also there is $[K^{(1)}],[K^{(2)}]$ that the dealer randomly generalize and distribute to the parties during the setup. The authenticated sharing is valid iff $x^{(1)}=K^{(1)}x$, $x^{(2)}=K^{(2)}x$.

The intuition is, if any one of the two parties are corrupt, they will never know the other’s secret $K$, thus cannot make up a fake authenticated sharing. The $K$ here serves as a MAC with **homomorphic** properties, and is initialized during setup phase, where the dealer sends the sharing to each party using $K^{(i)}$.

First, the dealer sends the authenticated sharing to the two parties. The two parties $P_1,P_2$ go through an interaction where $[a],[a^{(i)}],[K^{(i)}]$ is opened to $P_i$. Use the opened sharing, each of them checks whether $a^{(i)}=K^{(i)}a$. This process is called the **reliable key opening protocol,** which runs as an sub-protocol in the maliciously secure 2.5-party protocol. After the protocol, $P_i$ knows only the value of $K^{(i)}$ and a portion of the other key $K^{(3-i)}$.

Thus, simply replace $[x]$ by $\llbracket x \rrbracket$ we shift our protocol to a secure version w.r.t. corrupt parties. We have

- Opening: with $\llbracket x \rrbracket:=([x],[x^{(1)}],[x^{(2)}])$, do:

  - open $[x],[x^{(1)}],[x^{(2)}]$

  - $P_i$ checks if $K^{(i)}x=x^{(i)}$

- Adding: $\llbracket x \rrbracket+\llbracket y \rrbracket=([x]+[y],[x^{(1)}]+[y^{(1)}],[x^{(2)}]+[y^{(2)}])$

- Adding a constant: $\llbracket x \rrbracket+c=([x]+c,[x^{(1)}]+c[K^{(1)}],[x^{(2)}]+c[K^{(2)}])$. This is possible since $P_1$ has the first share of $K^{(2)}$.

This method let $P_i$ prove to $P_{3-i}$ that it will not tamper the opening results.

Moreover, the protocol will abort if any one of the parties has maliciously computed an incorrect output of any gate. This is equivalent to opening with a incorrect share of some value. If the result of $P_1$ is modified by $\delta$, and outputs $(x_1+\delta,x_1^{(1)}+K^{(1)}\delta,x_1^{(2)}+\delta^{(2)})$, the accepting probability of $P_2$ is the probability that $K^{(2)}\delta=\delta^{(2)}$.

Or you may wonder if $P_1$ computes $x+2y$ instead of $x+y$ of its share. The result is $(x_1+2y_1,x_1^{(1)}+2y_1^{(1)},x_1^{(2)}+2y_1^{(2)})$. Then $P_2$ checks if $K^{(2)}y_1=y_1^{(2)}$. Also a low probability to accept.

### Keeping the dealer honest: the interpolation protocol

However, the dealer can be malicious. Although it cannot know the data computed, it can:

- offer an invalid sharing or wrong keys such that $x^{(i)}\not=K^{(i)}x$

- inappropriately split the input $x\not=x_1+x_2$

- provide incorrect Beaver’s triple $([a],[b],[c])$

The first one is easily defenced through checking, and I suppose that the second one is not a problem, because the protocol is in fact computing another problem with a replaced input. We consider the third problem and suppose the dealer sends $a_{ij},b_{ij},c_{ij}$ where $i=1,2$ and $j=1,2,\dots,m$.

The dealer will do additional computations to prove that for every $j$, $(a_{1j}+a_{2j})(b_{1j}+b_{2j})=c_{1j}+c_{2j}$ using interpolation. The dealer randomly picks $a_{i0},b_{i0},c_{i0},i=1,2$ such that $(a_{10}+a_{20})(b_{10}+b_{20})=c_{10}+c_{20}$ and interpolates a degree- $m$ polynomial $A_1(X),A_2(X)$ such that $A_i(j)=a_{ij},i=1,2,j=0,\dots,m$. Similar for $B$, and $C(X)=(A_1(X)+A_2(X))(B_1(X)+B_2(X))$. Then for $k=m+1,\dots,2m$, randomize $c_{1k}+c_{2k}=C(k)$.

Each of the participant $P_i$ receives $a_{ik},b_{ik},k=0,\dots,m$ and $c_{ik},k=0,\dots,2m$, and interpolates the polynomials $A_i,B_i,C_i$. The next step, the participants run an argument of proving the polynomial equals $0$, all done by sending a random number and reveal the evaluations to each other. To be precise,

- Party $P_1$ randomly chooses $r \in \mathbb{Z}_q \setminus \{0, \ldots, m\}$ and sends it to $P_2$.

- Party $P_2$ verifies that $r \in \mathbb{Z}_q \setminus \{0, \ldots, m\}$; if not, $P_2$ aborts the protocol.

- Each party $P_i$ (for $i = 1, 2$) sends to the other party

$$
\alpha_i \leftarrow A_i(r), \quad \beta_i \leftarrow B_i(r), \quad \gamma_i \leftarrow C_i(r).
$$

- Each party locally checks whether

$$
(\alpha_1 + \alpha_2)(\beta_1 + \beta_2) = (\gamma_1 + \gamma_2)
$$

holds. If not, the party aborts the protocol.

So the soundness probability of the dealer to be corrupt is about $\frac{2m}{q}$. Because the difference polynomial $(A_1+A_2)(B_1+B_2)-(C_1+C_2)$ has degree $2m$, so the probability that $(\alpha_1 + \alpha_2)(\beta_1 + \beta_2) = (\gamma_1 + \gamma_2)$ when dealer is corrupt is at most $\frac{2m}{q}$.

Further, we should use simulator as in ZKP to prove that with a corrupted $P_i$, the $P_i$ cannot learn anything from $P_{3-i}$.

This protocol is placed after the reliable key opening protocol, before the main process.

**The complete maliciously secure protocol.** Putting all the pieces together, the whole protocol runs in this order.

- **Offline distribution (dealer, input-independent).** The dealer samples the MAC keys $K^{(1)},K^{(2)}\leftarrow\mathbb{F}_q$ and distributes $[K^{(1)}],[K^{(2)}]$; for each multiplication gate $j$, a fresh authenticated triple $\llbracket a_j \rrbracket,\llbracket b_j \rrbracket,\llbracket c_j \rrbracket$ with $c_j=a_jb_j$; for each input wire, an authenticated random mask $\llbracket r \rrbracket$ whose value $r$ is additionally revealed to the owner of that input; and the authenticated random values consumed by the reliable key opening below.

- **Reliable key opening.** For each $i$, $[a],[a^{(i)}],[K^{(i)}]$ are opened to $P_i$, who checks $a^{(i)}=K^{(i)}a$. Afterwards $P_i$ knows its own key $K^{(i)}$ in the clear and keeps a share of the other key.

- **Triple check.** The parties verify $c_j=a_jb_j$ for all $m$ triples at once by the interpolation protocol above, with soundness error about $\frac{2m}{q}$:

  - The dealer picks random $a_{i0},b_{i0},c_{i0}$, $i=1,2$, subject to $(a_{10}+a_{20})(b_{10}+b_{20})=c_{10}+c_{20}$, interpolates the degree- $m$ polynomials $A_i(X),B_i(X)$ through $A_i(j)=a_{ij}$, $B_i(j)=b_{ij}$ for $j=0,\dots,m$, sets $C(X)\gets(A_1(X)+A_2(X))(B_1(X)+B_2(X))$, and for $k=m+1,\dots,2m$ sends random shares $c_{1k},c_{2k}$ with $c_{1k}+c_{2k}=C(k)$.

  - Each $P_i$ interpolates $A_i,B_i$ from $a_{ik},b_{ik}$, $k=0,\dots,m$, and $C_i$ from $c_{ik}$, $k=0,\dots,2m$.

  - $P_1$ picks a random $r\in\mathbb{Z}_q\setminus\{0,\dots,m\}$ and sends it to $P_2$; $P_2$ aborts unless $r\in\mathbb{Z}_q\setminus\{0,\dots,m\}$.

  - Each $P_i$ sends $\alpha_i=A_i(r)$, $\beta_i=B_i(r)$, $\gamma_i=C_i(r)$ to the other party, and both check $(\alpha_1+\alpha_2)(\beta_1+\beta_2)=\gamma_1+\gamma_2$, aborting on failure.

- **Authenticated input sharing.** For each input $x$ owned by $P_i$: the owner broadcasts $\delta=x-r$, and both parties locally compute $\llbracket x \rrbracket=\llbracket r \rrbracket+\delta$ with the constant-add rule. Since $r$ is uniform and unknown to the other party, $\delta$ hides $x$; the dealer never sees $x$ at all. The resulting sharing is authenticated, so from now on the owner is bound to its shares like everyone else.

- **Evaluation.** Run the semi-honest protocol with $[\cdot]$ replaced by $\llbracket \cdot \rrbracket$: linear gates locally, one fresh authenticated triple per multiplication gate, and every opening is checked via $K^{(i)}x=x^{(i)}$. A party aborts on any failed check.

- **Output.** Open the output wires with authenticated opening and add the shares up.

In summary: a corrupt party is caught except with probability about $\frac{1}{q}$ per opening; a corrupt dealer is caught by the reliable key opening and the triple check; and the dealer’s view is independent of the inputs by construction.

### Beaver protocol for $n$ parties

The protocol can extend to $n$ parties easily, for the sharing can be $[x]=(x^{(1)},\dots,x^{(n)})$. The protocol requires $2$ broadcasts through public (maybe not safe) channels.

## From $2$ to $n$: GMW protocol

The GMW protocol securely computes a Boolean circuit among $n$ parties. Here we consider the semi-honest version with private channels and OT.

### Original GMW: online OT

The original protocol has no preprocessing: every AND gate runs its OTs on the spot, during the evaluation.

For a bit $x\in\mathbb{F}_2$, let

$$
[x]=(x_1,\dots,x_n),\qquad x=\bigoplus_{i=1}^n x_i.
$$

The XOR and NOT gates are local:

$$
\begin{aligned}
[x\oplus y]&=(x_1\oplus y_1,\dots,x_n\oplus y_n),\\
[\neg x]&=(x_1\oplus1,x_2,\dots,x_n).
\end{aligned}
$$

Only the AND gate requires communication. We have

$$
xy=\left(\bigoplus_i x_i\right)\left(\bigoplus_j y_j\right)
=\bigoplus_i x_iy_i\oplus\bigoplus_{i\ne j}x_iy_j.
$$

Every diagonal term $x_iy_i$ is computed by $P_i$. For every ordered pair $(i,j)$ where $i\ne j$, $P_i$ and $P_j$ use a $1$-out-of-$2$ OT to obtain a sharing of $x_iy_j$:

- $P_i$ samples $r_{ij}\leftarrow\mathbb{F}_2$ and acts as the sender with

$$
(m_0,m_1)=(r_{ij},r_{ij}\oplus x_i).
$$

- $P_j$ uses $y_j$ as the choice bit and receives

$$
s_{ij}=m_{y_j}=r_{ij}\oplus x_iy_j.
$$

Thus $r_{ij}\oplus s_{ij}=x_iy_j$. Party $P_i$ defines its output share as

$$
z_i=x_iy_i\oplus\bigoplus_{j\ne i}r_{ij}\oplus\bigoplus_{j\ne i}s_{ji}.
$$

Then

$$
\begin{aligned}
\bigoplus_i z_i
&=\bigoplus_i x_iy_i\oplus\bigoplus_{i\ne j}(r_{ij}\oplus s_{ij})\\
&=\bigoplus_i x_iy_i\oplus\bigoplus_{i\ne j}x_iy_j\\
&=xy.
\end{aligned}
$$

**Bootstrapping.** Suppose $P_k$ has an input bit $x$. It samples $x_i\leftarrow\mathbb{F}_2$ for every $i\ne k$, sends $x_i$ to $P_i$, and keeps

$$
x_k=x\oplus\bigoplus_{i\ne k}x_i.
$$

To sum up, the parties share the input wires, compute XOR and NOT locally, execute the OTs above for every AND gate, and finally open the output shares. All AND gates in the same layer can be computed in parallel, so the round complexity is the AND-depth of the circuit. An AND gate uses $n(n-1)$ directional OTs in this direct description.

### Relation with Beaver’s protocol

Over $\mathbb{F}_2$, addition is XOR and multiplication is AND. A Boolean Beaver triple is

$$
([a],[b],[c]),\qquad c=ab=a\land b.
$$

Given $[x],[y]$, open $d=x\oplus a$ and $e=y\oplus b$, then compute

$$
[xy]=[c]\oplus d[b]\oplus e[a]\oplus de.
$$

So original GMW computes the cross terms by OT *online*, whereas Beaver spends a triple and opens $d,e$. To preprocess triples, run these OTs on fresh random shares $[a],[b]$, independently of the actual inputs; the online phase then runs Beaver over $\mathbb{F}_2$. Per AND gate, per party:

- original: $2(n-1)$ OTs (one as sender, one as receiver, with each $P_j$), so $\Theta(n\kappa)$ bits online;

- Beaver: $2$ bits broadcast ($d$ and $e$), i.e. $2(n-1)$ bits sent, and information-theoretic — no cryptography once the triples are there;

- rounds are the same for both, one per AND layer, i.e. the AND-depth of the circuit;

**Generating the triples (semi-honest).** Sample $[a],[b]$ locally and run the AND-gate OTs above on them: for every ordered pair $(i,j)$, $i\ne j$,

$$
P_i:(r_{ij},r_{ij}\oplus a_i),\quad P_j:\text{choice }b_j
\quad\Longrightarrow\quad s_{ij}=r_{ij}\oplus a_ib_j,
$$

$$
c_i=a_ib_i\oplus\bigoplus_{j\ne i}r_{ij}\oplus\bigoplus_{j\ne i}s_{ji}.
$$

Nothing depends on the inputs, so all $n(n-1)M$ OTs run offline in one batch — which is worth it only if OT itself is cheap.

OT implementations and IKNP extension are described in [Oblivious Transfer](/files/2026_09_02_Oblivious_Transfer.html).

## From semi-honest to malicious: BDOZ & SPDZ

BDOZ and SPDZ scale to $n$ parties with a dishonest majority. Their online phase is still Beaver, now with authenticated sharing. How to generate the authenticated triples from OT instead of homomorphic encryption is the next section.

### BDOZ: pairwise MACs on shares

Each $P_i$ privately holds a fixed global key $\Delta^{(i)}$ (notation: a superscript $^{(i)}$ marks that $P_i$ holds the object). The BDOZ sharing of $x$ is

$$
[x]_{\mathrm{B}}=\bigl([x],[M_1],\dots,[M_n]\bigr),\qquad M_i=K^{(i)}+\Delta^{(i)}x,
$$

where all the sharings are uniformly random, $K^{(i)}$ is a one-time offset freshly picked per value, and $P_i$ stores it as a split $K^{(i)}=\sum_j K_j^{(i)}$ matched to the shares:

$$
M_i^{(j)}=\Delta^{(i)}x^{(j)}+K_j^{(i)}.
$$

This is the right way to share: the fresh pad $K^{(i)}$ makes $[M_i]$ uniform given $[x]$, so the MACs leak nothing about $\Delta^{(i)}$ or $x$ (without the pad, $P_j$ would solve its clear share $M_i^{(j)}=\Delta^{(i)}x^{(j)}$ for the key); and faking an opened share by $\delta$ requires shifting the MAC by $\Delta^{(i)}\delta$ without knowing $\Delta^{(i)}$. All linear operations are local:

- $[x]_{\mathrm{B}}+[y]_{\mathrm{B}}$: all shares add; $P_i$ sets $K_j^{(i)}\leftarrow K_j^{(i)}+K_j^{\prime(i)}$

- $c[x]_{\mathrm{B}}$: all shares and $K_j^{(i)}$ multiply by $c$

- $[x]_{\mathrm{B}}+c$: $x^{(1)}\leftarrow x^{(1)}+c$, $K_1^{(i)}\leftarrow K_1^{(i)}-c\Delta^{(i)}$, shares of $M_i$ untouched

- opening: $P_j$ broadcasts $x^{(j)}$ and sends $M_i^{(j)}$ to $P_i$, who accepts iff $M_i^{(j)}=\Delta^{(i)}x^{(j)}+K_j^{(i)}$; a cheater passes w.p. $\frac{1}{q}$

Multiplication is Beaver with authenticated triples. Our $K^{(i)}$ plays the role of $\Delta^{(i)}$; the difference is that we MAC the value and share the MAC with no structure, while BDOZ remembers the per-share split, so single shares can be verified. The cost is $n(n-1)$ MACs per wire.

In the standard presentation the $[M_i]$ never appear summed up: $P_j$ just holds $m_i^{(j)}=\Delta^{(i)}x^{(j)}+K_j^{(i)}$ as a pairwise MAC on its share $x^{(j)}$ under $P_i$’s key $(\Delta^{(i)},K_j^{(i)})$ — the same data as above.

### SPDZ: one shared global key

A single global key $\alpha$ is secret-shared as $[\alpha]$ during setup and never opened — knowing $\alpha$ means forging every MAC, so there is no analogue of our reliable key opening. A value is

$$
\langle x \rangle=([x],[\gamma]),\quad \gamma=\alpha x,
$$

one shared MAC per value: $O(n)$ per wire. Operations:

- $\langle x \rangle+\langle y \rangle=([x]+[y],[\gamma]+[\gamma'])$, and $c\langle x \rangle=(c[x],c[\gamma])$, where the primed MAC belongs to $\langle y \rangle$

- $\langle x \rangle+c$: $x^{(1)}\leftarrow x^{(1)}+c$, $\gamma^{(i)}\leftarrow\gamma^{(i)}+c\alpha^{(i)}$ (here $\alpha^{(i)}$ is $P_i$’s share of $\alpha$, unlike BDOZ’s private $\Delta^{(i)}$)

- opening: broadcast the $x^{(i)}$; each $P_i$ computes $\sigma^{(i)}=\gamma^{(i)}-x\alpha^{(i)}$ and **commits** to it; open all commitments and accept iff $\sum_i\sigma^{(i)}=0$ (indeed $\sum_i\sigma^{(i)}=\alpha x-x\alpha$, and the commitments stop a cheater from choosing $\sigma^{(i)}$ after seeing the others). A random linear combination of many opened values checks a whole batch at once.

- multiplication: Beaver with $\langle a \rangle,\langle b \rangle,\langle c \rangle$.

## Generating Beaver Triples

BDOZ / SPDZ 的 online 阶段只是带 MAC 的 Beaver，全部困难在于没有 dealer 时怎么造 authenticated triple。原始的 BDOZ / SPDZ 用同态加密；把它换成 OT，BDOZ 就变成 TinyOT（$\mathbb{F}_2$，pairwise MAC），SPDZ 就变成 MASCOT（$\mathbb{F}_q$，global MAC）。

### From homomorphic encryption: BDOZ & SPDZ

每个 $P_i$ 取随机 $a^{(i)},b^{(i)}$，

$$
c=ab=\sum_i a^{(i)}b^{(i)}+\sum_{i\ne j}a^{(i)}b^{(j)} .
$$

对角项本地算；每个交叉项 $a^{(i)}b^{(j)}$ 是一个两方乘积，要变成两方 sharing。**BDOZ** 用加法同态加密：

$$
P_i\to P_j:\ \mathrm{Enc}_{pk_i}(a^{(i)}),\qquad P_j\to P_i:\ \mathrm{Enc}_{pk_i}(a^{(i)})^{b^{(j)}}\cdot\mathrm{Enc}_{pk_i}(-r)=\mathrm{Enc}_{pk_i}\bigl(a^{(i)}b^{(j)}-r\bigr),
$$

$P_j$ 留 $r$，$P_i$ 解密留 $a^{(i)}b^{(j)}-r$；全部求和得 $[c]$。MAC $\Delta^{(i)}x^{(j)}$ 是同样形状的两方乘积（$P_i$ 输入 $\Delta^{(i)}$，$P_j$ 输入 $x^{(j)}$），用同一招产生。malicious 安全还需要密文合法的 ZK 证明。

**SPDZ** 用 somewhat 同态加密：setup 公布一个全局公钥（私钥在 parties 之间 shared）和 $\mathrm{Enc}(\alpha)$。每个 $P_i$ 广播 $\mathrm{Enc}(a^{(i)}),\mathrm{Enc}(b^{(i)})$ 及其 ZK 证明，大家同态地算

$$
\mathrm{Enc}(a)=\prod_i \mathrm{Enc}(a^{(i)}),\qquad \mathrm{Enc}(c)=\mathrm{Enc}(a)\boxtimes \mathrm{Enc}(b),\qquad \mathrm{Enc}(\alpha c)=\mathrm{Enc}(\alpha)\boxtimes\mathrm{Enc}(c),
$$

每个值只乘一次，所以深度 $1$ 就够。distributed decryption 把 $\mathrm{Enc}(c)$ 变成新鲜随机的 $[c]$ 而不向任何人揭示 $c$，同时输出 $c$ 的新鲜密文供算 MAC 用（$a,b$ 的 MAC 同理）。最后 **sacrifice** 第二个 triple $(\langle f\rangle,\langle g\rangle,\langle h\rangle)$ 来验证 $c=ab$：取公开随机 $r$，打开 $\rho=r\langle a\rangle-\langle f\rangle$、$\sigma=\langle b\rangle-\langle g\rangle$，再打开

$$
r\langle c\rangle-\langle h\rangle-\sigma\langle f\rangle-\rho\langle g\rangle-\rho\sigma=r(c-ab)-(h-fg)\ \overset{?}{=}\ 0,
$$

错的 triple 对 $r$ 存活概率 $\frac1q$。这对应前面对 dealer 的 interpolation check；MASCOT 沿用同一个检查。

这条路在 $\mathbb{F}_2$ 上不划算：一个 bit 的乘法要配一次密文乘法。布尔电路走 OT，就是下面的 TinyOT。

## TinyOT: malicious MPC for Boolean circuits

下面用 $n$ 个 party 的形式说明 TinyOT-style 认证布尔计算；三元组预处理采用 half-gate 与 bucketing。所有 bit 运算都在 $\mathbb F_2$ 上：加法为 XOR，乘法为 AND。

### 1. Share：认证 XOR 份额

每个 $P_i$ 持有私有认证密钥 $\Delta_i\in\mathbb F_{2^\kappa}$。秘密 bit $x$ 被分享为

$$
x=\bigoplus_{i=1}^n x^{(i)},
$$

上标 $(i)$ 统一表示 $P_i$ 持有的 additive 份额。

对每对 $i\ne j$，$P_i$ 保存随机 key $K_{i\leftarrow j}[x]$，$P_j$ 保存 MAC

$$
M_{j\to i}[x]=K_{i\leftarrow j}[x]\oplus x^{(j)}\Delta_i.
$$

记 $[x]$ 为这些份额及其认证信息。每个 $P_i$ 只持有

$$
x_i,\qquad\{M_{i\to j}[x],K_{i\leftarrow j}[x]\}_{j\ne i}.
$$

与 BDOZ 一样，以下运算均在本地完成：

- XOR：$[x]\oplus[y]=(\boldsymbol{x}\oplus\boldsymbol{y},\boldsymbol{M}[x]\oplus\boldsymbol{M}[y],\boldsymbol{K}[x]\oplus\boldsymbol{K}[y])$，即份额、MAC、key 逐项 XOR。
- 加公开 bit $b$：$x^{(1)}\leftarrow x^{(1)}\oplus b,\quad K_{i\leftarrow1}\leftarrow K_{i\leftarrow1}\oplus b\Delta_i\ (i\ne1)$，其余份额及 MAC/key 不变。
- NOT：$[\neg x]=[x]\oplus1$。

下文 $\operatorname{Open}([x])$ 表示：验证份额的 MAC 后重构 $x=\bigoplus_i x^{(i)}$；检查失败则 abort。

### 2. Preprocess：生成认证三元组

目标是在不知道电路输入时生成随机

$$
([a],[b],[c]),\qquad c=ab.
$$

分三步：COT 生成认证随机 bit；half-gate 生成可能泄漏的候选；bucketing 降低泄漏概率。

#### 2.1 COT → authenticated bit

目标：生成 $\ell$ 个认证随机 bit $[p_1],\ldots,[p_\ell]$。记 $p_k^{(j)}\in\{0,1\}$ 为 $P_j$ 持有的 $p_k$ 的份额，$p_k=\bigoplus_jp_k^{(j)}$。

一次 correlated OT 的关系恰好是认证关系：

$$
\underbrace{P_i:(\Delta_i,K)}_{\text{sender}},\qquad
\underbrace{P_j:(p_k^{(j)},M)}_{\text{receiver}},\qquad
M=K\oplus p_k^{(j)}\Delta_i.
$$

每对 $i\ne j$ 之间用 OT extension 跑 $\ell$ 个 COT：$P_i$ 得到 $K_{i\leftarrow j}[p_k]$，$P_j$ 得到 $M_{j\to i}[p_k]$。$P_i$ 对 $P_j$ 的密钥 $\Delta_{i\to j}$ 是它在 base OT 里的 choice 向量，之后扩展出的每个 COT 都乘同一个 $\Delta_{i\to j}$，$P_i$ 无法在其中某几个 COT 上换密钥；这是 extension 的构造保证的。$P_j$ 在同一对之间各个 COT 的 choice 一致由 KOS 检查保证，见 OT 笔记。

extension 不保证的是同一个 party 对不同对象一致，因此需要两个检查：

- Check 1：$P_i$ 对所有 $j$ 的 $\Delta_{i\to j}$ 相等。密钥在 base OT 时固定，只需检查一次。
- Check 2：$P_j$ 对所有 $i$ 使用同一个份额 $p_k^{(j)}$。每批都要检查。

检查通过后记 $\Delta_i=\Delta_{i\to j}$。

**Check 1：同一 sender 使用同一个 $\Delta_i$。** 否则不同 receiver 的 MAC 不受同一密钥认证，后面无法使用统一的 $\Delta_i$。

首次生成认证 bit 时，每对 $i\ne j$ 额外执行 $\kappa=128$ 个测试 COT：sender $P_i$ 仍使用 $\Delta_i$，receiver $P_j$ 使用随机测试 bit $x_{j,i,k}$（$k=0,\ldots,\kappa-1$）。$P_i$ 得到 $K_{i\leftarrow j,k}$，$P_j$ 得到 $M_{j\to i,k}$，满足

$$
M_{j\to i,k}=K_{i\leftarrow j,k}\oplus x_{j,i,k}\Delta_i.
$$

下标 $j,i,k$ 分别表示 receiver、sender、测试编号。测试材料检查后丢弃；同一会话继续使用固定密钥时，不再重复 Check 1。

将域 $\mathbb F_{2^\kappa}$ 中的元素表示为 $\kappa$ 个二进制系数。$e_k$ 表示第 $k$ 位为 $1$、其余位为 $0$ 的元素；$e_0,\ldots,e_{\kappa-1}$ 称为这个域在 $\mathbb F_2$ 上的一组基。于是 $\bigoplus_ke_kx_{j,i,k}$ 就是把这些 choice bit 放入对应位，组成一个域元素。例如 $\kappa=3$、choices 为 $(1,0,1)$ 时，结果为 $e_0\oplus e_2$，位表示为 $101$。

按同一组系数合并 MAC/key（这里的 $e_kM$、$e_kK$ 是有限域乘法，不是逐位 AND）：

$$
X_{j,i}=\bigoplus_{k=0}^{\kappa-1}e_kx_{j,i,k},\\
\bar M_{j\to i}=\bigoplus_ke_kM_{j\to i,k},\\
\bar K_{i\leftarrow j}=\bigoplus_ke_kK_{i\leftarrow j,k}.
$$

记 $Y_i=\bigoplus_{j\ne i}X_{j,i}$，检查

$$
\bigoplus_{j\ne i}\left(\bar M_{j\to i}\oplus\bar K_{i\leftarrow j}\right)
\oplus Y_i\Delta_i\overset?=0.
$$

若密钥一致，则 $\bar M_{j\to i}\oplus\bar K_{i\leftarrow j}=X_{j,i}\Delta_i$，故左边为

$$
\left(\bigoplus_{j\ne i}X_{j,i}\right)\Delta_i\oplus Y_i\Delta_i=0.
$$

若 $P_i$ 对 $P_j$ 使用 $\Delta_{i\to j}$，残差为

$$
\bigoplus_{j\ne i}X_{j,i}\left(\Delta_{i\to j}\oplus\Delta_i\right).
$$

随机测试用来检测这个残差。协议通过零分享掩蔽测试值、承诺后开启聚合检查量，不直接公开每条 MAC/key；不能把上式理解为让每个 party 交出密钥后检查。

**Check 2：同一 receiver 使用同一个 $p_k^{(j)}$。** 否则各个 $P_i$ 认证的是不同的 bit，无法定义统一的份额 $p_k^{(j)}$。

本批 $\ell$ 个 COT 完成后，所有 party 采样公开随机系数 $\chi_1,\ldots,\chi_\ell\in\mathbb F_{2^\kappa}$。$P_j$ 向其他 party 一致公布

$$
w_j=\bigoplus_k\chi_kp_k^{(j)}.
$$

并向每个 $P_i$ 发送聚合 MAC $\bigoplus_k\chi_kM_{j\to i}[p_k]$。$P_i$ 检查

$$
\bigoplus_k\chi_kM_{j\to i}[p_k]
\overset?=\bigoplus_k\chi_kK_{i\leftarrow j}[p_k]\oplus w_j\Delta_i.
$$

正确性来自 MAC 关系的线性：

$$
\begin{aligned}
\bigoplus_k\chi_kM_{j\to i}[p_k]
&=\bigoplus_k\chi_k\left(K_{i\leftarrow j}[p_k]\oplus p_k^{(j)}\Delta_i\right)\\
&=\bigoplus_k\chi_kK_{i\leftarrow j}[p_k]\oplus
\left(\bigoplus_k\chi_kp_k^{(j)}\right)\Delta_i.
\end{aligned}
$$

所有 $P_i$ 必须收到同一个 $w_j$；若 $P_j$ 可以对不同的 $P_i$ 公布不同的 $w_j$，便不能检查它对不同 $P_i$ 的份额是否一致。

这两个检查只在 $n>2$ 时需要；$n=2$ 时每个 party 只有一个对象，但仍须执行 KOS 检查。

#### 2.2 authenticated bits → leaky AND

输入三个认证随机 bit $[a],[b],[r]$，构造候选 $[c]$。以下等式先说明诚实执行时为什么 $c=ab$，再说明检查与泄漏。

**(a) 从认证信息得到 $b\Delta_\Sigma$ 的份额，** 其中 $\Delta_\Sigma=\bigoplus_i\Delta_i$。取零分享 $\bigoplus_i z^{(i)}=0$，每个 party 都可以本地计算

$$
\phi^{(i)}\gets b^{(i)}\Delta_i\oplus
\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[b]\oplus M_{i\to j}[b]\bigr)\oplus z^{(i)}.
$$

就是 $b\Delta_\Sigma$ 的 share, 因为

$$
\begin{aligned}
\bigoplus_i\phi^{(i)}
&=\bigoplus_i b^{(i)}\Delta_i
 \oplus\bigoplus_{i\ne j}\bigl(K_{i\leftarrow j}[b]\oplus M_{j\to i}[b]\bigr)\\
&=\bigoplus_i b^{(i)}\Delta_i\oplus\bigoplus_{i\ne j}v^{(j)}\Delta_i\\
&=\left(\bigoplus_jb^{(j)}\right)\left(\bigoplus_i\Delta_i\right)=b\Delta_\Sigma.
\end{aligned}
$$

零分享用于 mask 每个 share 

$$
b^{(i)}\Delta_i\oplus
\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[b]\oplus M_{i\to j}[b]\bigr),$$

因为这个值由 MAC/Key 确定性地决定。

**(b) 用已有 COT 计算交叉项 $a^{(j)}\phi_i$。** 设 $H:\{0,1\}^*\to\mathbb F_{2^\kappa}$ 为 hash，$k$ 为本候选在批中的公开编号。对 $i\ne j$，$P_i$ 给 $P_j$ 发送

$$
G_{i\to j}=H(i,j,k,K_{i\leftarrow j}[a])\oplus
H(i,j,k,K_{i\leftarrow j}[a]\oplus\Delta_i)\oplus\phi_i.
$$

$P_j$ 计算

$$
E_{i\to j}=H(i,j,k,M_{j\to i}[a])\oplus a^{(j)}G_{i\to j}.
$$

分别代入 $a^{(j)}=0,1$：

$$
E_{i\to j}=
\begin{cases}
H(i,j,k,K_{i\leftarrow j}[a]),&a^{(j)}=0,\\
H(i,j,k,K_{i\leftarrow j}[a]\oplus\Delta_i)\oplus G_{i\to j}
=H(i,j,k,K_{i\leftarrow j}[a])\oplus\phi_i,&a^{(j)}=1.
\end{cases}
$$

即 $E_{i\to j}=H(i,j,k,K_{i\leftarrow j}[a])\oplus a^{(j)}\phi_i$。sender 持有 $H(i,j,k,K_{i\leftarrow j}[a])$，receiver 持有 $E_{i\to j}$，两者 XOR 就是交叉项。

**(c) 合并交叉项，再用 $r$ 掩蔽。** 每个 party 计算

$$
T_i=a^{(i)}\phi_i\oplus
\bigoplus_{j\ne i}\bigl(H(i,j,k,K_{i\leftarrow j}[a])\oplus E_{j\to i}\bigr)
\oplus F_i([r]).
$$

每个 $H(i,j,k,K_{i\leftarrow j}[a])$ 在 $T_i$ 和 $T_j$ 里各出现一次，相互抵消：

$$
\begin{aligned}
\bigoplus_iT_i
&=\bigoplus_i a^{(i)}\phi_i\oplus\bigoplus_{i\ne j}a^{(j)}\phi_i\oplus r\Delta_\Sigma\\
&=\left(\bigoplus_ja^{(j)}\right)\left(\bigoplus_i\phi_i\right)\oplus r\Delta_\Sigma\\
&=(ab\oplus r)\Delta_\Sigma.
\end{aligned}
$$

预先约定一个公开线性映射 $\pi:\mathbb F_{2^\kappa}\to\mathbb F_2$，并约束密钥满足 $\pi(\Delta_\Sigma)=1$。每个 party 发送 $s_i=\pi(T_i)$，得到

$$
d=\bigoplus_i s_i
=\pi\left(\bigoplus_iT_i\right)
=(ab\oplus r)\pi(\Delta_\Sigma)=ab\oplus r.
$$

因此

$$
[c]=[r]\oplus d,\qquad c=r\oplus(ab\oplus r)=ab.
$$

乘积的认证信息来自已有的 $[r]$ 加公开常数 $d$，无需公开 $ab$。

**(d) 检查，但仍允许选择性泄漏。** 每个 party 计算

$$
\alpha_i=T_i\oplus d\Delta_i,\qquad
\bigoplus_i\alpha_i=(ab\oplus r\oplus d)\Delta_\Sigma=0.
$$

对一批候选，在候选消息固定后采样公开随机系数 $\rho_k$，检查其随机线性组合：

$$
A_i=\sum_k\rho_k\alpha_{i,k}+U_i,\quad\sum_iU_i=0,
\qquad\sum_iA_i=\sum_k\rho_k\left(\sum_i\alpha_{i,k}\right)\overset?=0.
$$

这里加法均为 XOR；乘法可理解为特征 $2$ 上的多项式乘法。每个 party 先承诺 $A_i$ 再开启，避免最后一个 sender 根据别人的值凑出零。$n=2$ 时，零和条件就是 $\alpha_1=\alpha_2$，可比较向量摘要。

不能由此断言候选完全安全。若恶意 party 发送 $G_{i\to j}\oplus\delta$，receiver 产生的偏差为

$$
E'_{i\to j}\oplus E_{i\to j}=a^{(j)}\delta.
$$

$a^{(j)}=0$ 时偏差为零，$a^{(j)}=1$ 时偏差为 $\delta$。因此是否 abort 可能泄漏 $a^{(j)}$；这称为 **selective failure（选择性失败）**，也就是“leaky”的原因。

#### 2.3 Bucketing → 可用三元组

先看两个候选如何合并。给定 $c_1=a_1b_1$、$c_2=a_2b_2$，认证开启 $d=b_1\oplus b_2$，令

$$
[A]=[a_1]\oplus[a_2],\quad[B]=[b_1],\quad
[C]=[c_1]\oplus[c_2]\oplus d[a_2].
$$

正确性为

$$
C=a_1b_1\oplus a_2b_2\oplus(b_1\oplus b_2)a_2
=(a_1\oplus a_2)b_1=AB.
$$

合并 $t$ 个候选时，同理：

$$
[A]=\bigoplus_{k=1}^t[a_k],\quad[B]=[b_1],\quad
[C]=[c_1]\oplus\bigoplus_{k=2}^t\bigl([c_k]\oplus(b_1\oplus b_k)[a_k]\bigr),
$$

$$
C=a_1b_1\oplus\bigoplus_{k=2}^t a_kb_1=AB.
$$

**为什么降低泄漏？** 在 leaky-triple 模型下，攻击者要获知输出 $A$，需泄漏桶内全部 $t$ 个候选的 $a$；每个受攻击候选还有 $1/2$ 的存活因子。

为产生 $\ell$ 个输出，先生成 $t$ 层、每层 $\ell$ 个候选，再随机循环移位各层形成桶。设第 $k$ 层有 $g_k$ 个泄漏候选，$g=\sum_kg_k$，则全泄漏桶数 $N_{\rm leak}$ 满足

$$
\mathbb E[N_{\rm leak}]
=\ell\prod_{k=1}^t\frac{g_k}{\ell}
=\frac{\prod_kg_k}{\ell^{t-1}}
\le\frac{(g/t)^t}{\ell^{t-1}}.
$$

结合存活因子和 $\Pr[N_{\rm leak}\ge1]\le\mathbb E[N_{\rm leak}]$，得到分桶泄漏界

$$
\Pr[\text{通过检查且有全泄漏桶}]
\le\max_{t\le g\le t\ell}2^{-g}\frac{(g/t)^t}{\ell^{t-1}}.
$$

选择 $t$ 使该界不超过 $2^{-s}$。候选消息必须先固定、再确定分桶，否则攻击者可以针对同一个桶作弊。这是分桶的误差界，不包含其他认证和哈希检查的误差。

**保留预先选定的随机 $a,b$。** 若要求输出仍使用第一对 $a=a_1,b=b_1$，分桶后再开启 $u=a\oplus A$，令

$$
[c]=[C]\oplus u[B],\qquad c=Ab\oplus(a\oplus A)b=ab.
$$

这一步把合并结果转换回指定乘积；得到的随机 $([a],[b],[c])$ 留给电路 AND 门使用。

### 3. Input：把私有输入变成认证份额

假设 party $P_k$ 持有 bit $x$：

1. 取新鲜认证随机 bit $[r]$，仅向 $P_k$ 开启 $r$。
2. $P_k$ 一致广播 $\delta=x\oplus r$。
3. 所有 party 本地计算 $[x]=[r]\oplus\delta$。

正确性为

$$
r\oplus\delta=r\oplus(x\oplus r)=x.
$$

对不知道 $r$ 的 party，$\delta$ 隐藏 $x$；$\delta$ 固定后，输入值也固定为 $r\oplus\delta$。恶意 input party 仍可选择自己的输入，认证约束的是之后不能随意篡改份额。

### 4. Evaluate：用三元组计算 AND

XOR、NOT 按 Share 部分本地处理。计算 $z=xy$ 时，消耗一个尚未使用的随机三元组 $([a],[b],[c])$，$c=ab$：

$$
d=\operatorname{Open}([x]\oplus[a]),\qquad
e=\operatorname{Open}([y]\oplus[b]),
$$

$$
[z]=[c]\oplus d[b]\oplus e[a]\oplus de.
$$

因为 $x=a\oplus d$、$y=b\oplus e$，所以

$$
xy=(a\oplus d)(b\oplus e)
=ab\oplus ae\oplus db\oplus de
=c\oplus e a\oplus d b\oplus de.
$$

$a,b$ 掩蔽输入，开启 $d,e$ 不直接揭示 $x,y$。三元组不得复用：同一个 $a$ 若分别掩蔽 $x,x'$，会公开

$$
(x\oplus a)\oplus(x'\oplus a)=x\oplus x'.
$$

同一 AND 深度的门可一起开启 $d,e$；深度为 $D$ 的电路需要 $D$ 批认证开启。一次认证开启可能包含多个通信阶段。

### 5. Output：验证并重构输出

对允许公开的输出 $[y]$，每个 party 提交自己的份额及认证信息。$P_i$ 检查每个 $j\ne i$：

$$
M_{j\to i}[y]\overset?=K_{i\leftarrow j}[y]\oplus y^{(j)}\Delta_i.
$$

检查通过且开启视图一致后，输出 $y=\bigoplus_jy^{(j)}$；否则 abort。若 $P_j$ 把份额改成 $y^{(j)}\oplus1$，所需的新 MAC 为

$$
M'_{j\to i}=K_{i\leftarrow j}\oplus(y^{(j)}\oplus1)\Delta_i
=M_{j\to i}\oplus\Delta_i.
$$

伪造它需要知道诚实 $P_i$ 的 $\Delta_i$。认证三元组、认证开启和本地线性运算共同约束计算；上述代数等式说明正确性，恶意安全还依赖预处理检查及其误差界。
