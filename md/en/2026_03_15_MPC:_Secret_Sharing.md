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

The online phase of BDOZ / SPDZ is just Beaver with MACs; all the difficulty lies in how to build authenticated triples without a dealer. The original BDOZ / SPDZ use homomorphic encryption; replace it with OT, and BDOZ becomes TinyOT ($\mathbb{F}_2$, pairwise MAC), SPDZ becomes MASCOT ($\mathbb{F}_q$, global MAC).

### From homomorphic encryption: BDOZ & SPDZ

Each $P_i$ picks random $a^{(i)},b^{(i)}$,

$$
c=ab=\sum_i a^{(i)}b^{(i)}+\sum_{i\ne j}a^{(i)}b^{(j)} .
$$

The diagonal terms are computed locally; each cross term $a^{(i)}b^{(j)}$ is a two-party product, to be turned into a two-party sharing. **BDOZ** uses additively homomorphic encryption:

$$
P_i\to P_j:\ \mathrm{Enc}_{pk_i}(a^{(i)}),\qquad P_j\to P_i:\ \mathrm{Enc}_{pk_i}(a^{(i)})^{b^{(j)}}\cdot\mathrm{Enc}_{pk_i}(-r)=\mathrm{Enc}_{pk_i}\bigl(a^{(i)}b^{(j)}-r\bigr),
$$

$P_j$ keeps $r$, $P_i$ decrypts and keeps $a^{(i)}b^{(j)}-r$; summing everything gives $[c]$. The MAC $\Delta^{(i)}x^{(j)}$ is a two-party product of the same shape ($P_i$ inputs $\Delta^{(i)}$, $P_j$ inputs $x^{(j)}$), produced by the same trick. Malicious security additionally needs ZK proofs that the ciphertexts are well-formed.

**SPDZ** uses somewhat homomorphic encryption: setup publishes one global public key (the secret key is shared among the parties) and $\mathrm{Enc}(\alpha)$. Each $P_i$ broadcasts $\mathrm{Enc}(a^{(i)}),\mathrm{Enc}(b^{(i)})$ with their ZK proofs, and everyone homomorphically computes

$$
\mathrm{Enc}(a)=\prod_i \mathrm{Enc}(a^{(i)}),\qquad \mathrm{Enc}(c)=\mathrm{Enc}(a)\boxtimes \mathrm{Enc}(b),\qquad \mathrm{Enc}(\alpha c)=\mathrm{Enc}(\alpha)\boxtimes\mathrm{Enc}(c),
$$

Each value is multiplied only once, so depth $1$ suffices. Distributed decryption turns $\mathrm{Enc}(c)$ into a fresh random $[c]$ without revealing $c$ to anyone, and at the same time outputs a fresh ciphertext of $c$ for computing the MAC (likewise for the MACs of $a,b$). Finally, **sacrifice** a second triple $(\langle f\rangle,\langle g\rangle,\langle h\rangle)$ to verify $c=ab$: take a public random $r$, open $\rho=r\langle a\rangle-\langle f\rangle$, $\sigma=\langle b\rangle-\langle g\rangle$, then open

$$
r\langle c\rangle-\langle h\rangle-\sigma\langle f\rangle-\rho\langle g\rangle-\rho\sigma=r(c-ab)-(h-fg)\ \overset{?}{=}\ 0,
$$

A wrong triple survives with probability $\frac1q$ over $r$. This corresponds to the earlier interpolation check on the dealer; MASCOT reuses the same check.

This route does not pay off over $\mathbb{F}_2$: a single bit multiplication costs one ciphertext multiplication. For Boolean circuits one uses OT instead; this is TinyOT, described below.

## TinyOT: malicious MPC for Boolean circuits

Below, TinyOT-style authenticated Boolean computation is described in the $n$-party form; triple preprocessing uses half-gate and bucketing. All bit operations are over $\mathbb F_2$: addition is XOR, multiplication is AND.

### 1. Share: authenticated XOR shares

Each $P_i$ holds a private authentication key $\Delta_i\in\mathbb F_{2^\kappa}$. A secret bit $x$ is shared as

$$
x=\bigoplus_{i=1}^n x^{(i)},
$$

Throughout, the superscript $(i)$ denotes the additive share held by $P_i$.

For each pair $i\ne j$, $P_i$ stores a random key $K_{i\leftarrow j}[x]$, and $P_j$ stores the MAC

$$
M_{j\to i}[x]=K_{i\leftarrow j}[x]\oplus x^{(j)}\Delta_i.
$$

Write $[x]$ for these shares and their authentication information. Each $P_i$ holds only

$$
x^{(i)},\qquad\{M_{i\to j}[x],K_{i\leftarrow j}[x]\}_{j\ne i}.
$$

As in BDOZ, the following operations are all done locally:

- XOR: $[x]\oplus[y]=(\boldsymbol{x}\oplus\boldsymbol{y},\boldsymbol{M}[x]\oplus\boldsymbol{M}[y],\boldsymbol{K}[x]\oplus\boldsymbol{K}[y])$, i.e. shares, MACs and keys are XORed entrywise.
- Adding a public bit $b$: $x^{(1)}\leftarrow x^{(1)}\oplus b,\quad K_{i\leftarrow1}\leftarrow K_{i\leftarrow1}\oplus b\Delta_i\ (i\ne1)$; all other shares and MACs/keys are unchanged.
- NOT: $[\neg x]=[x]\oplus1$.

Below, $\operatorname{Open}([x])$ means: verify the MACs of the shares, then reconstruct $x=\bigoplus_i x^{(i)}$; abort if a check fails.

### 2. Preprocess: generating authenticated triples

The goal is to generate, without knowing the circuit inputs, random

$$
([a],[b],[c]),\qquad c=ab.
$$

Three steps: COT generates authenticated random bits; half-gate generates candidates that may leak; bucketing lowers the leakage probability.

#### 2.1 COT → authenticated bit

Goal: generate $\ell$ authenticated random bits $[p_1],\ldots,[p_\ell]$. Let $p_k^{(j)}\in\{0,1\}$ be the share of $p_k$ held by $P_j$, $p_k=\bigoplus_jp_k^{(j)}$.

The relation of one correlated OT is exactly the authentication relation:

$$
\underbrace{P_i:(\Delta_i,K)}_{\text{sender}},\qquad
\underbrace{P_j:(p_k^{(j)},M)}_{\text{receiver}},\qquad
M=K\oplus p_k^{(j)}\Delta_i.
$$

Between each pair $i\ne j$, run $\ell$ COTs via OT extension: $P_i$ gets $K_{i\leftarrow j}[p_k]$, $P_j$ gets $M_{j\to i}[p_k]$. $P_i$'s key toward $P_j$, $\Delta_{i\to j}$, is its choice vector in the base OTs; every COT produced by the extension uses the same $\Delta_{i\to j}$, so $P_i$ cannot switch keys on some of these COTs; this is guaranteed by the construction of the extension. That $P_j$'s choices are consistent across the COTs within the same pair is guaranteed by the KOS check; see the OT note.

What the extension does not guarantee is that the same party is consistent across different counterparts, hence two checks are needed:

- Check 1: $P_i$'s $\Delta_{i\to j}$ are equal for all $j$. The key is fixed at base-OT time, so it only needs to be checked once.
- Check 2: $P_j$ uses the same share $p_k^{(j)}$ for all $i$. Must be checked for every batch.

Once the checks pass, write $\Delta_i=\Delta_{i\to j}$.

**Check 1: the same sender uses the same $\Delta_i$.** Otherwise the MACs of different receivers are not authenticated under the same key, and a unified $\Delta_i$ cannot be used later.

When authenticated bits are generated for the first time, each pair $i\ne j$ additionally runs $\kappa=128$ test COTs: sender $P_i$ still uses $\Delta_i$, receiver $P_j$ uses random test bits $x_{j,i,k}$ ($k=0,\ldots,\kappa-1$). $P_i$ gets $K_{i\leftarrow j,k}$, $P_j$ gets $M_{j\to i,k}$, satisfying

$$
M_{j\to i,k}=K_{i\leftarrow j,k}\oplus x_{j,i,k}\Delta_i.
$$

The subscripts $j,i,k$ denote receiver, sender and test index respectively. The test material is discarded after the check; when the same session keeps using the fixed key, Check 1 is not repeated.

Represent elements of the field $\mathbb F_{2^\kappa}$ as $\kappa$ binary coefficients. $e_k$ denotes the element whose $k$-th bit is $1$ and all other bits are $0$; $e_0,\ldots,e_{\kappa-1}$ is called a basis of this field over $\mathbb F_2$. Thus $\bigoplus_ke_kx_{j,i,k}$ just puts these choice bits into the corresponding positions to form a field element. For example, with $\kappa=3$ and choices $(1,0,1)$, the result is $e_0\oplus e_2$, with bit representation $101$.

Combine the MACs/keys with the same coefficients (here $e_kM$, $e_kK$ are finite-field multiplications, not bitwise AND):

$$
\begin{aligned}
X_{j,i}&=\bigoplus_{k=0}^{\kappa-1}e_kx_{j,i,k},\\
\bar M_{j\to i}&=\bigoplus_ke_kM_{j\to i,k},\\
\bar K_{i\leftarrow j}&=\bigoplus_ke_kK_{i\leftarrow j,k}.
\end{aligned}
$$

Let $Y_i=\bigoplus_{j\ne i}X_{j,i}$, and check

$$
\bigoplus_{j\ne i}\left(\bar M_{j\to i}\oplus\bar K_{i\leftarrow j}\right)
\oplus Y_i\Delta_i\overset?=0.
$$

If the keys are consistent, then $\bar M_{j\to i}\oplus\bar K_{i\leftarrow j}=X_{j,i}\Delta_i$, so the left-hand side is

$$
\left(\bigoplus_{j\ne i}X_{j,i}\right)\Delta_i\oplus Y_i\Delta_i=0.
$$

If $P_i$ uses $\Delta_{i\to j}$ toward $P_j$, the residual is

$$
\bigoplus_{j\ne i}X_{j,i}\left(\Delta_{i\to j}\oplus\Delta_i\right).
$$

The random test serves to detect this residual. The protocol masks the test values with a zero sharing and opens the aggregated check value after committing, without directly revealing each MAC/key; the formula above must not be read as each party handing over its key and then checking.

**Check 2: the same receiver uses the same $p_k^{(j)}$.** Otherwise the various $P_i$ authenticate different bits, and no unified share $p_k^{(j)}$ can be defined.

After the $\ell$ COTs of this batch are done, all parties sample public random coefficients $\chi_1,\ldots,\chi_\ell\in\mathbb F_{2^\kappa}$. $P_j$ broadcasts, sending the same value to every other party,

$$
w_j=\bigoplus_k\chi_kp_k^{(j)}.
$$

and sends each $P_i$ the aggregated MAC $\bigoplus_k\chi_kM_{j\to i}[p_k]$. $P_i$ checks

$$
\bigoplus_k\chi_kM_{j\to i}[p_k]
\overset?=\bigoplus_k\chi_kK_{i\leftarrow j}[p_k]\oplus w_j\Delta_i.
$$

Correctness follows from the linearity of the MAC relation:

$$
\begin{aligned}
\bigoplus_k\chi_kM_{j\to i}[p_k]
&=\bigoplus_k\chi_k\left(K_{i\leftarrow j}[p_k]\oplus p_k^{(j)}\Delta_i\right)\\
&=\bigoplus_k\chi_kK_{i\leftarrow j}[p_k]\oplus
\left(\bigoplus_k\chi_kp_k^{(j)}\right)\Delta_i.
\end{aligned}
$$

All $P_i$ must receive the same $w_j$; if $P_j$ could announce different $w_j$ to different $P_i$, there would be no way to check whether its shares toward different $P_i$ are consistent.

These two checks are needed only when $n>2$; when $n=2$ each party has only one counterpart, but the KOS check must still be run.

#### 2.2 authenticated bits → leaky AND

Take as input three authenticated random bits $[a],[b],[r]$ and construct a candidate $[c]$. The equations below first explain why $c=ab$ in an honest execution, then explain the check and the leakage.

**(a) Get shares of $b\Delta_\Sigma$ from the authentication information,** where $\Delta_\Sigma=\bigoplus_i\Delta_i$. Take a zero sharing $\bigoplus_i z^{(i)}=0$; each party can locally compute

$$
\phi^{(i)}\gets b^{(i)}\Delta_i\oplus
\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[b]\oplus M_{i\to j}[b]\bigr)\oplus z^{(i)}.
$$

This is a share of $b\Delta_\Sigma$, because

$$
\begin{aligned}
\bigoplus_i\phi^{(i)}
&=\bigoplus_i b^{(i)}\Delta_i
 \oplus\bigoplus_{i\ne j}\bigl(K_{i\leftarrow j}[b]\oplus M_{j\to i}[b]\bigr)\\
&=\bigoplus_i b^{(i)}\Delta_i\oplus\bigoplus_{i\ne j}b^{(j)}\Delta_i\\
&=\left(\bigoplus_jb^{(j)}\right)\left(\bigoplus_i\Delta_i\right)=b\Delta_\Sigma.
\end{aligned}
$$

The zero sharing is used to mask each share 

$$
b^{(i)}\Delta_i\oplus
\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[b]\oplus M_{i\to j}[b]\bigr),
$$

because this value is deterministically determined by the MAC/Key.

**(b) Compute the cross terms $a^{(j)}\phi^{(i)}$ with the existing COTs.** Let $H:\{0,1\}^*\to\mathbb F_{2^\kappa}$ be a hash, and $k$ the public index of this candidate within the batch. For $i\ne j$, $P_i$ sends $P_j$

$$
G_{i\to j}=H(i,j,k,K_{i\leftarrow j}[a])\oplus
H(i,j,k,K_{i\leftarrow j}[a]\oplus\Delta_i)\oplus\phi^{(i)}.
$$

$P_j$ computes

$$
E_{i\to j}=H(i,j,k,M_{j\to i}[a])\oplus a^{(j)}G_{i\to j}.
$$

Substituting $a^{(j)}=0,1$ respectively:

$$
E_{i\to j}=
\begin{cases}
H(i,j,k,K_{i\leftarrow j}[a]),&a^{(j)}=0,\\
H(i,j,k,K_{i\leftarrow j}[a]\oplus\Delta_i)\oplus G_{i\to j}
=H(i,j,k,K_{i\leftarrow j}[a])\oplus\phi^{(i)},&a^{(j)}=1.
\end{cases}
$$

That is, $E_{i\to j}=H(i,j,k,K_{i\leftarrow j}[a])\oplus a^{(j)}\phi^{(i)}$. The sender holds $H(i,j,k,K_{i\leftarrow j}[a])$, the receiver holds $E_{i\to j}$, and their XOR is the cross term.

**(c) Combine the cross terms, then mask with $r$.** Each party computes

$$
T_i=a^{(i)}\phi^{(i)}\oplus
\bigoplus_{j\ne i}\bigl(H(i,j,k,K_{i\leftarrow j}[a])\oplus E_{j\to i}\bigr)
\oplus F_i([r]).
$$

Here $F_i([r])=r^{(i)}\Delta_i\oplus\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[r]\oplus M_{i\to j}[r]\bigr)$, i.e. $P_i$'s share of $r\Delta_\Sigma$, computed locally from $[r]$ as in (a).

Each $H(i,j,k,K_{i\leftarrow j}[a])$ appears once in $T_i$ and once in $T_j$, so they cancel:

$$
\begin{aligned}
\bigoplus_iT_i
&=\bigoplus_i a^{(i)}\phi^{(i)}\oplus\bigoplus_{i\ne j}a^{(j)}\phi^{(i)}\oplus r\Delta_\Sigma\\
&=\left(\bigoplus_ja^{(j)}\right)\left(\bigoplus_i\phi^{(i)}\right)\oplus r\Delta_\Sigma\\
&=(ab\oplus r)\Delta_\Sigma.
\end{aligned}
$$

Fix in advance a public linear map $\pi:\mathbb F_{2^\kappa}\to\mathbb F_2$, and constrain the keys to satisfy $\pi(\Delta_\Sigma)=1$. Each party sends $s_i=\pi(T_i)$, giving

$$
d=\bigoplus_i s_i
=\pi\left(\bigoplus_iT_i\right)
=(ab\oplus r)\pi(\Delta_\Sigma)=ab\oplus r.
$$

Therefore

$$
[c]=[r]\oplus d,\qquad c=r\oplus(ab\oplus r)=ab.
$$

The authentication information of the product comes from the existing $[r]$ plus the public constant $d$, with no need to reveal $ab$.

**(d) Check, but selective leakage is still possible.** Each party computes

$$
\alpha_i=T_i\oplus d\Delta_i,\qquad
\bigoplus_i\alpha_i=(ab\oplus r\oplus d)\Delta_\Sigma=0.
$$

For a batch of candidates, sample public random coefficients $\rho_k$ after the candidate messages are fixed, and check their random linear combination:

$$
A_i=\sum_k\rho_k\alpha_{i,k}+U_i,\quad\sum_iU_i=0,
\qquad\sum_iA_i=\sum_k\rho_k\left(\sum_i\alpha_{i,k}\right)\overset?=0.
$$

Here all additions are XOR; multiplication can be read as polynomial multiplication in characteristic $2$. Each party first commits to $A_i$ and then opens it, so that the last party to send cannot choose its value after seeing the others' to force the sum to zero. When $n=2$, the zero-sum condition is just $\alpha_1=\alpha_2$, and vector digests can be compared.

This does not show that the candidate is fully secure. If a malicious party sends $G_{i\to j}\oplus\delta$, the deviation produced at the receiver is

$$
E'_{i\to j}\oplus E_{i\to j}=a^{(j)}\delta.
$$

When $a^{(j)}=0$ the deviation is zero; when $a^{(j)}=1$ the deviation is $\delta$. Hence whether the protocol aborts may leak $a^{(j)}$; this is called **selective failure**, which is why it is "leaky".

#### 2.3 Bucketing → usable triples

First, how two candidates are combined. Given $c_1=a_1b_1$, $c_2=a_2b_2$, perform an authenticated opening of $d=b_1\oplus b_2$, and let

$$
[A]=[a_1]\oplus[a_2],\quad[B]=[b_1],\quad
[C]=[c_1]\oplus[c_2]\oplus d[a_2].
$$

Correctness:

$$
C=a_1b_1\oplus a_2b_2\oplus(b_1\oplus b_2)a_2
=(a_1\oplus a_2)b_1=AB.
$$

Combining $t$ candidates works the same way:

$$
[A]=\bigoplus_{k=1}^t[a_k],\quad[B]=[b_1],\quad
[C]=[c_1]\oplus\bigoplus_{k=2}^t\bigl([c_k]\oplus(b_1\oplus b_k)[a_k]\bigr),
$$

$$
C=a_1b_1\oplus\bigoplus_{k=2}^t a_kb_1=AB.
$$

**Why does this reduce leakage?** In the leaky-triple model, for the attacker to learn the output $A$, the $a$ of all $t$ candidates in the bucket must leak; each attacked candidate also contributes a survival factor of $1/2$.

To produce $\ell$ outputs, first generate $t$ layers of $\ell$ candidates each, then cyclically shift each layer by a random offset to form buckets. Suppose layer $k$ has $g_k$ leaky candidates, $g=\sum_kg_k$; then the number of fully leaky buckets $N_{\rm leak}$ satisfies

$$
\mathbb E[N_{\rm leak}]
=\ell\prod_{k=1}^t\frac{g_k}{\ell}
=\frac{\prod_kg_k}{\ell^{t-1}}
\le\frac{(g/t)^t}{\ell^{t-1}}.
$$

Combining the survival factor with $\Pr[N_{\rm leak}\ge1]\le\mathbb E[N_{\rm leak}]$ gives the bucketing leakage bound

$$
\Pr[\text{checks pass and a fully leaky bucket exists}]
\le\max_{t\le g\le t\ell}2^{-g}\frac{(g/t)^t}{\ell^{t-1}}.
$$

Choose $t$ so that this bound is at most $2^{-s}$. The candidate messages must be fixed first and the bucketing determined afterwards; otherwise the attacker can concentrate its leaky candidates in a single bucket. This is the error bound of bucketing and does not include the errors of the other authentication and hash checks.

**Keeping the preselected random $a,b$.** If the output is required to still use the first pair $a=a_1,b=b_1$, open $u=a\oplus A$ after bucketing and let

$$
[c]=[C]\oplus u[B],\qquad c=Ab\oplus(a\oplus A)b=ab.
$$

This step converts the combined result back to the designated product; the resulting random $([a],[b],[c])$ is kept for the AND gates of the circuit.

### 3. Input: turning private inputs into authenticated shares

Suppose party $P_k$ holds bit $x$:

1. Take a fresh authenticated random bit $[r]$ and open $r$ only to $P_k$.
2. $P_k$ broadcasts $\delta=x\oplus r$, sending the same value to every party.
3. All parties locally compute $[x]=[r]\oplus\delta$.

Correctness:

$$
r\oplus\delta=r\oplus(x\oplus r)=x.
$$

To a party that does not know $r$, $\delta$ hides $x$; once $\delta$ is fixed, the input value is also fixed as $r\oplus\delta$. A malicious input party can still choose its own input; what authentication constrains is that it cannot freely tamper with shares afterwards.

### 4. Evaluate: computing AND with triples

XOR and NOT are handled locally as in the Share part. To compute $z=xy$, consume an unused random triple $([a],[b],[c])$, $c=ab$:

$$
d=\operatorname{Open}([x]\oplus[a]),\qquad
e=\operatorname{Open}([y]\oplus[b]),
$$

$$
[z]=[c]\oplus d[b]\oplus e[a]\oplus de.
$$

Since $x=a\oplus d$, $y=b\oplus e$,

$$
xy=(a\oplus d)(b\oplus e)
=ab\oplus ae\oplus db\oplus de
=c\oplus e a\oplus d b\oplus de.
$$

$a,b$ mask the inputs, so opening $d,e$ does not directly reveal $x,y$. Triples must not be reused: if the same $a$ masks $x,x'$ respectively, this reveals

$$
(x\oplus a)\oplus(x'\oplus a)=x\oplus x'.
$$

Gates at the same AND depth can open $d,e$ together; a circuit of depth $D$ needs $D$ batches of authenticated openings. One authenticated opening may involve several communication phases.

### 5. Output: verifying and reconstructing outputs

For an output $[y]$ that may be revealed, each party submits its share and authentication information. $P_i$ checks, for every $j\ne i$:

$$
M_{j\to i}[y]\overset?=K_{i\leftarrow j}[y]\oplus y^{(j)}\Delta_i.
$$

Once the checks pass and the opening views are consistent, output $y=\bigoplus_jy^{(j)}$; otherwise abort. If $P_j$ changes its share to $y^{(j)}\oplus1$, the new MAC it needs is

$$
M'_{j\to i}=K_{i\leftarrow j}\oplus(y^{(j)}\oplus1)\Delta_i
=M_{j\to i}\oplus\Delta_i.
$$

Forging it requires knowing honest $P_i$'s $\Delta_i$. Authenticated triples, authenticated opening and local linear operations jointly constrain the computation; the algebraic equations above show correctness, while malicious security additionally relies on the preprocessing checks and their error bounds.
