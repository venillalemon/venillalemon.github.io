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

Therefore the direct GMW protocol uses OT to compute every cross term of an AND gate, while Beaver assumes triples generated in the preprocessing by a dealer, OT, or other primitives, and leaves only the two openings online. If the GMW preprocessing produces Boolean triples, its online phase is exactly Beaver’s protocol over $\mathbb{F}_2$.

## From semi-honest to malicious: BDOZ & SPDZ

BDOZ and SPDZ remove the dealer and scale to $n$ parties with a dishonest majority. The online phase is still Beaver; we only an authentication scheme.

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

**Where the triples come from.** Each $P_i$ picks random $a^{(i)},b^{(i)}$, and

$$
c=ab=\sum_i a^{(i)}b^{(i)}+\sum_{i\ne j}a^{(i)}b^{(j)}.
$$

The diagonal terms are local. Each cross term $a^{(i)}b^{(j)}$ is turned into a two-party sharing with additively homomorphic encryption:

- $P_i$ sends $\mathrm{Enc}_{pk_i}(a^{(i)})$

- $P_j$ picks a random $r$, replies $\mathrm{Enc}_{pk_i}(a^{(i)})^{b^{(j)}}\cdot \mathrm{Enc}_{pk_i}(-r)=\mathrm{Enc}_{pk_i}(a^{(i)}b^{(j)}-r)$, and keeps $r$ as its share

- $P_i$ decrypts and keeps $a^{(i)}b^{(j)}-r$ as its share

Summing all the terms gives $[c]$. The MACs are products of the same two-party shape ($P_i$ inputs $\Delta^{(i)}$, $P_j$ inputs $x^{(j)}$), so the same trick generates them too; malicious security additionally needs ZK proofs that the ciphertexts are well-formed.

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

**Where the triples come from.** The setup publishes a global public key whose secret key is shared among the parties, together with a ciphertext $\mathrm{Enc}(\alpha)$. Each $P_i$ broadcasts $\mathrm{Enc}(a^{(i)}),\mathrm{Enc}(b^{(i)})$ with a ZK proof of well-formedness, and everyone computes homomorphically

$$
\mathrm{Enc}(a)=\prod_i \mathrm{Enc}(a^{(i)}),\qquad \mathrm{Enc}(c)=\mathrm{Enc}(a)\boxtimes \mathrm{Enc}(b)
$$

— a single ciphertext multiplication, which is why *somewhat* homomorphic encryption (depth $1$) suffices. A distributed decryption protocol then converts $\mathrm{Enc}(c)$ into a fresh random sharing $[c]$ without revealing $c$ to anyone, and it also outputs a fresh ciphertext of $c$, so the MAC $\mathrm{Enc}(\alpha c)=\mathrm{Enc}(\alpha)\boxtimes\mathrm{Enc}(c)$ again costs only depth $1$ (same for the MACs of $a,b$). Finally $c=ab$ is checked by **sacrificing** a second triple $(\langle f \rangle,\langle g \rangle,\langle h \rangle)$: pick a public random $r$, open $\rho=r\langle a \rangle-\langle f \rangle$ and $\sigma=\langle b \rangle-\langle g \rangle$, then open

$$
r\langle c \rangle-\langle h \rangle-\sigma\langle f \rangle-\rho\langle g \rangle-\rho\sigma=r(c-ab)-(h-fg)
$$

and accept iff it is $0$; a wrong triple survives w.p. $\frac{1}{q}$ over $r$. This plays the role of our interpolation check against the dealer. (MASCOT etc. replace the offline phase by oblivious transfer; the online phase never changes.)
