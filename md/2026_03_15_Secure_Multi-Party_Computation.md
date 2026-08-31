# Secure Multi-Party Computation

*March 15, 2026*

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

## Garbled Circuit: Quick Catch-up

这里我们用统一的语言描述 GC 的各种构造和优化。设要跑的门是 $g$, 对应 0,1 的 label 为 $a_0,a_1,b_0,b_1$ for input wires, $c_0,c_1$ for output wires. Garbling table 用 map 表示，也可以看作一个函数. 导线上的值用 $v$ 表示，随机 bit 用 $r$ 表示。

### **Yao's GC**

$$
(r_a\oplus v_a,r_b\oplus v_b)\to H(a_{v_a},b_{v_b},i)\oplus c_{g(v_a,v_b)}
$$

附加条件：所有 label 末尾有连续多个 $0$ （和安全参数正比）以判断哪个是正确的 label.

### **Point-and-Permute**

$$
(v_a\oplus r_a,v_b\oplus r_b)\to H(a_{v_a\oplus r_a},b_{v_b\oplus r_b},i)\oplus c_{g(v_a,v_b)\oplus r_c}
$$

附加条件：所有 label 的下标总是和它最后一位相同. 拿到 label 后直接按照最后一位去表格找即可.

### **BMR**

Point-and-Permute 在 $n$ 方的推广。一个 Evaluator，多个 Garbler。

**Garble**: 首先每个 $P_i$ 为每个 wire $a$ 随机选 label $a_0^{(i)},a_1^{(i)}$ 和 pad bit $\lambda_a^{(i)}$.

对于 gate $g$ 假设 input wire 是 $a,b$ ，output wire 是 $c$ 。令

$$
\lambda_a:=\bigoplus_{i\in[n]}\lambda_a^{(i)}.
$$

并且令对于 $x\in\{0,1\}$,

$$
a_{x}=a_x^{(1)}\|\cdots\|a_x^{(n)}\|x.
$$

然后每方 $P_i$ 本地计算 $H(a^{(i)}_{\rho_a},b^{(i)}_{\rho_b},\mathrm{id})$, 其中 $\rho_a,\rho_b\in\{0,1\}$ 都要遍历到.

接下来所有参与方运行 MPC 协议，获取电路的输出，对所有 $\rho_a,\rho_b\in\{0,1\}$ 都重复一遍。电路输入是每个人的份额 $\lambda_a^{(i)},\lambda_b^{(i)},\lambda_c^{(i)},c_{0}^{(i)},c_{1}^{(i)},H(a^{(i)}_{\rho_a},b^{(i)}_{\rho_b},\mathrm{id})$, 计算

$$
\chi=g(\lambda_a\oplus\rho_a,\lambda_b\oplus\rho_b)\oplus\lambda_c=g\left(\bigoplus_{i\in[n]}\lambda_a^{(i)}\oplus\rho_a,\bigoplus_{i\in[n]}\lambda_b^{(i)}\oplus\rho_b\right)\oplus\bigoplus_{i\in[n]}\lambda_c^{(i)}
$$

以及

$$
e_{\rho_a,\rho_b}= (c_\chi^{(1)}\|\cdots\|c_\chi^{(n)}\|\chi)\oplus\left(\bigoplus_{i\in[n]} H(a^{(i)}_{\rho_a},b^{(i)}_{\rho_b},\mathrm{id})\right)
$$

并放在表格的 $(\rho_a,\rho_b)$ 处。

**Evaluate**: 假设对于这个门 $g$ ，拿到了两个 label $a_{\Lambda_a},b_{\Lambda_b}$ ，那么其末位 bit 分别是 $\Lambda_a,\Lambda_b$. 去表格中 $(\Lambda_a,\Lambda_b)$ 位置找即可得到 $e_{\Lambda_a,\Lambda_b}$.

根据 garbling 过程，我们可以得到

$$
c_{\Lambda_c}=c_\chi=e_{\Lambda_a,\Lambda_b}\oplus\left(\bigoplus_{i\in[n]} H(a^{(i)}_{\Lambda_a},b^{(i)}_{\Lambda_b},\mathrm{id})\right)
$$

其中

$$
\Lambda_c=\chi=g(\lambda_a\oplus\Lambda_a,\lambda_b\oplus\Lambda_b)\oplus\lambda_c
$$

我们发现， $\Lambda_c$ 正好是 wire 真实值 $v_c$ 经过掩码的结果，即 $\Lambda_c=v_c\oplus \lambda_c$, 这样上面的式子正好在说 $v_c=g(v_a,v_b)$.

**Bootstrapping**: 对于 input wire $w$, 其所有者 $P_{j_w}$ 广播 $\Lambda_w=v_w\oplus \lambda_w^{(j_w)}$. 注意这里换了定义，我们不用 $\Lambda_w=v_w\oplus \lambda_w$ 是因为这样还需要额外多一轮通信.

> 由于以上的原因，在 Garbling 的时候也需要对不同的 wire 设置不同的掩码规则。具体来说就是
>
> $$
> \lambda_w = \begin{cases} \lambda_w^{(j_w)} & w \in \mathsf{Input} \\ \lambda_w^{(1)} \oplus \cdots \oplus \lambda_w^{(n)} & \text{otherwise} \end{cases}
> $$
>
> 一个直观的解释是，掩码的存在是让不该看到明文的人看不到明文（label的最后一位就是明文加掩码，所以如果不用掩码，直接看最后一位就知道明文了）
>
> 对于 input wire w， $P_{j_w}$ 已经知道明文，因此目的就是不让任何剩下 $n-1$ 方的子集能够恢复明文。因此只需要让掩码全部由 $j_w$ 提供即可。（如果 $P_{j_w}$ 被腐化，那么 adversary 本身就可以串通，互相知道明文，也不需要保护）。
>
> 对于内部 wire ，为了保证任何一个子集都不能恢复明文，才需要所有人参与分享掩码。

然后大家都得到 $\Lambda_w$, 于是可以互相广播拼凑出

$$
w_{\Lambda_w}=w_{\Lambda_w}^{(1)}\|\cdots\|w_{\Lambda_w}^{(n)}\|\Lambda_w.
$$

然后直接开始 Evaluation 即可.

### **FreeXOR**

每个 party 选一个全局偏移 $\Delta^{(i)}$, 对于每条 wire $a$, $a_1^{(i)}$ 不随机采样而是满足 $a_x^{(i)}=a_0^{(i)}\oplus x\Delta^{(i)}$. Garbling 生成的标签满足对于一个 XOR gate 输入 $a,b$ 输出 $c$,

$$
a_0^{(i)}\oplus b_0^{(i)}=c_0^{(i)},\quad
\lambda_a^{(i)}\oplus \lambda_b^{(i)}=\lambda_c^{(i)}
$$

聚合起来就是

$$
a_{x}=a_0\oplus x(\Delta\|1),\quad a_0\oplus b_0=c_0,\quad \lambda_a\oplus\lambda_b=\lambda_c,
$$

其中对于 $w\in\mathsf{Input}$ 我们约定 $\lambda_w^{(i)}=1$ 当仅当 $i=j_w$, 否则 $\lambda_w^{(i)}=0$. 因此有

$$
a_{\Lambda_a}\oplus b_{\Lambda_b}=c_0\oplus (\Lambda_a\oplus\Lambda_b)(\Delta\|1)=c_0\oplus (\lambda_c\oplus v_a\oplus v_b)(\Delta\|1)=c_{\Lambda_c}.
$$

也就是遇到 XOR 的时候可以简单把两个 label 进行 XOR 得到输出的 label. AND 门不变.

### **Half-Gates**

TODO

## Intro: Beaver’s protocol

The beaver’s protocol securely computes the output of the arithmetic circuits over $\mathbb{F}_q$ among $2$ parties.

### Basic Idea

To achieve privacy, it is an intuition to split the key value into several parts, and distribute them to different parties. We use $[x]$ to denote a share of value $x$, meaning $[x]=(x_1,x_2)$ where $x=x_1+x_2$. And define

- $[x]+[y]=(x_1+y_1,x_2+y_2)$

- $c[x]=(cx_1,cx_2)$

- $[x]+c=(x_1+c,x_2)$ (I am curious whether it is more secure to split the constant randomly, not just always add it on one side.)

The add gate, scalar multiplication gate and constant add gate is linear; the tow parties can compute independently. The multiplication gate needs the *dealer* to generate a random **Beaver triple sharing**: $([a],[b],[c])$ where $c=ab$.

Suppose the two parties are computing the multiplication of $[x]$ and $[y]$. The dealer sends $a_i,b_i$ to $P_i$ each, and the two parties compute $[u]=[x]-[a]$ and $[v]=[y]-[b]$. Then the two parties open the shares $[u],[v]$ to each other so that they both know $u=x-a,v=y-b$, and uses their own share to compute

$$
[z]=uv+u[b]+v[a]+[c].
$$

For example, the party $i$ computes $z_i=uv\times\mathbf{1}_{i=1}+ub_i+va_i+c_i$ and we can verify that $z_1+z_2=uv+ub+ua+ab=xy$.

And the dealer would split the input $x=x_1+x_2$ and distributes them to $P_i$ ’s.

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

### Keeping the dealer honest

However, the dealer can be malicious. Although it cannot know the data computed, it can:

- offer an invalid sharing or wrong keys such that $x^{(i)}\not=K^{(i)}x$

- inappropriately split the input $x\not=x_1+x_2$

- provide incorrect Beaver’s triple $([a],[b],[c])$

The first one is easily defenced through checking, and I suppose that the second one is not a problem, because the protocol is in fact computing another problem with a replaced input. We consider the third problem and suppose the dealer sends $a_{ij},b_{ij},c_{ij}$ where $i=1,2$ and $j=1,2,\dots,m$.

The dealer will do additional computations to prove that for every $j$, $(a_{1j}+a_{2j})(b_{1j}+b_{2j})=c_{1j}+c_{2j}$ using interpolation. The dealer randomly picks $a_{j0},b_{j0},c_{j0},j=1,2$ such that $(a_{10}+a_{20})(b_{10}+b_{20})=c_{10}+c_{20}$ and interpolates a degree- $m$ polynomial $A_1(X),A_2(X)$ such that $A_i(j)=a_{ij},i=1,2,j=0,\dots,m$. Similar for $B$, and $C(X)=(A_1(X)+A_2(X))(B_1(X)+B_2(X))$. Then for $k=m+1,\dots,2m$, randomize $c_{1k}+c_{2k}=C(k)$.

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

So the soundness probability of the dealer to be corrupt is about $\frac{2m}{q}$.

Further, we should use simulator as in ZKP to prove that with a corrupted $P_i$, the $P_i$ cannot learn anything from $P_{3-i}$.

This protocol is placed after the reliable key opening protocol, before the main process.

### Beaver protocol for $n$ parties

The protocol can extend to $n$ parties easily, for the sharing can be $[x]=(x^{(1)},\dots,x^{(n)})$. The protocol requires $2$ broadcasts through public (maybe not safe) channels.

## Garbled Circuits

A **garbling scheme** consists of four algorithms; the first is non-deterministic while others are deterministic:

- $\mathsf{Garble}$: $(\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f)$

- $\mathsf{Encode}$: $\mathcal{X} \leftarrow \mathsf{Encode}(e, {x})$

- $\mathsf{Eval}$: $\mathcal{Y} \leftarrow \mathsf{Eval}(\mathcal{F}, \mathcal{X})$

- $\mathsf{Decode}$: $\{{y},\bot\} \leftarrow \mathsf{Decode}(d, \mathcal{Y})$

**Correctness:** For all $f, (\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f), {x}$,

$$
\mathsf{Decode}(d, \mathsf{Eval}(\mathcal{F}, \mathsf{Encode}(e, {x}))) = f({x})
$$

Intuitive security goals:

- **Obliviousness**: $\mathcal{F}, \mathcal{X}$ reveals nothing about $x$. This is about preventing the evaluator from gaining the input.

- **Authenticity**: Given $\mathcal{F}, \mathcal{X}$ it is of negligible probability for all PPT adversaries to find $\mathcal{Y}'\not=\mathsf{Eval}(\mathcal{F},\mathcal{X})$ that decodes to a value (not a $\bot$). This is about preventing the evaluator from forging the result.

- **Output simulatability**: $\mathcal{Y}$ can be efficiently computed by $f(x)$ and $d$.

Here is a scheme of **outsourcing computation:** suppose Alice uses Bob’s computation resources to compute $f(x)$. First Alice generates $(\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f)$; then sends $\mathcal{F}$ to Bob, and keeps $e,d$ herself. When she wants to compute, she has $\mathcal{X} \leftarrow \mathsf{Encode}(e, {x})$ and sends $\mathcal{X}$ to Bob, where Bob computes $\mathcal{Y} \leftarrow \mathsf{Eval}(\mathcal{F}, \mathcal{X})$ and returns to Alice. Then Alice can decode.

Note that Alice should generate a garbled circuit on different inputs and the same boolean circuit. If we use the same GC for different computation tasks, then a honest-but-curious party would know some relations of the two inputs through comparing the encoded $\mathcal{X}$; or some information about $e$. We should always keep in mind that the encoding algorithm is deterministic.

### Formal definition of the security goals

**Obliviousness.** For $b = 0, 1$, we have experiment $\mathsf{Exp}_b$:

- Adversary submits $(f, \mathbf{x}^{(0)}, \mathbf{x}^{(1)})$

- Challenger computes:

$$
(\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f), \quad \mathcal{X} \leftarrow \mathsf{Encode}(e, \mathbf{x}^{(b)})
$$

and sends $(\mathcal{F}, \mathcal{X})$ to adversary.

- Adversary outputs $\hat{b} \in \{0,1\}$, let $W_b$ be the event that the adversary outputs $1$.

A garbling scheme is oblivious iff for every PPT adversary, the game has a negligible advantage defined by $|\Pr[W_0] - \Pr[W_1]|$.

**Output Simulatability.** A garbling scheme is output simulatable if there exists an efficient deterministic algorithm $\mathsf{Reverse}$ such that for every $f$, every $(\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f)$, and every ${x}$:

$$
\mathsf{Eval}(\mathcal{F}, \mathsf{Encode}(e, \mathbf{x})) = \mathsf{Reverse}(d, f(\mathbf{x})).
$$

### $\texttt{Garble0}$: an implementation of garbling scheme

Suppose the boolean circuit has $n$ variables and $m$ outputs. The below $e$ is called a **projective input encoding**, where the encoding process is for every bit, use one value out of two.

$$
\begin{align*}
e&=((X_1^0,X_1^1),\dots,(X_n^0,X_n^1))\\
\mathcal{X}&=(X_1^{x_1},\dots,X_n^{x_n})\\
d&=((Y_1^0,Y_1^1),\dots,(Y_m^0,Y_m^1))\\
\mathcal{Y}&=(Y_1,\dots,Y_m)
\end{align*}
$$

where $x$ is the input and $\mathcal{Y}$ is the garbled output. The decoding algorithm is to compare each $Y_j$ to the pair $(Y_j^0,Y_j^1)$.

Our goal is to establish the algorithm $\mathsf{Eval}$ that with input $\mathcal{F}$ and $\mathcal{X}$ carries out the garbled output.

The garbled circuit $\mathcal{F}$ consists of a function for each gate $g$, which we will denote by $\mathsf{GateEval}_g$ satisfying

$$
\mathsf{GateEval}(\mathcal{G},I_1^u,I_2^v)=O^{g(u,v)}
$$

where $I_i^x$ ‘s are the garbled values of input wires and $O^y$ are that of the output wire. For example an AND gate, we have $\mathsf{GateEval}(I_1^u,I_2^v)=O^{\mathbf{1}[u=1\land v=1]}$. The encoding $\mathcal{G}$ for this gate is called a **garbled encoding**, which should be used together with a **garbled evaluation algorithm** $\mathsf{GateEval}$.

### Implementation of garbled encoding

This implementation entails a public key encryption scheme. We index each wire by $I$ and each wire $i$ corresponds to two public keys $(k_i^0,k_i^1)$ as the **private encoding**. Then consider one gate with inputs wires $i,j$ and output wire $t$.

$$
E^{(a,b)}=\mathsf{Enc}_{k_i^a}(\mathsf{Enc}_{k_j^b}(k_t^{g(a,b)}\|000\dots00))
$$

where the length of the trailing zeros is the security parameter $\lambda$. And the garbled circuit is the tuple

$$
\mathcal{G}=(i,j,t,E^{(0,0)},E^{(0,1)},E^{(1,0)},E^{(1,1)})
$$

with the evaluation algorithm

$$
\begin{align*}
\mathsf{GateEval}(\mathcal{G},X,Y)=
&\;\mathbf{for}\;a\in\{0,1\},b\in\{0,1\}:\\
&\quad\mathbf{if}\;\mathsf{Dec}_{k_j^Y}(\mathsf{Dec}_{k_i^X}(E^{(a,b)}))\text{ end with }\lambda\; 0\text{'s}\\
&\quad\quad\mathbf{return}\;\mathsf{Dec}_{k_j^Y}(\mathsf{Dec}_{k_i^X}(E^{(a,b)}))
\end{align*}
$$

This algorithm is obviously correct, but requires computations for all $4$ possibilities. Below we propose the point-and-permute method to make it more efficient.

(In fact this method has a constant complexity for all gates; if we construct a big look-up table for the whole circuit, the total time will be exponential!)

### More efficient

We have $T=\{0,1\}^\ell$ be our set of **tokens** and $I$ is the finite set of identifiers that each gate has a unique identifier $i\in I$. And $H:T\times T\times I\mapsto T$ a hash function. For each wire, the garbling process generates $(X^0,X^1,r)$ as the **private encoding** such that $X^i$ begins with $i$. Then consider the gate $i$ with its input private encodings $(A^0,A^1,r),(B^0,B^1,s)$ and the output private encodings $(C^0,C^1,t)$. We set for $a,b\in\{0,1\}$,

$$
E^{(a,b)}=H(A^{a},B^b,i)\oplus C^{g(a\oplus r,b\oplus s)\oplus t}.
$$

Note that And we define the garbled encoding

$$
\mathcal{G}=(i,E^{(0,0)},E^{(0,1)},E^{(1,0)},E^{(1,1)})
$$

with the garbled evaluation algorithm

$$
\mathsf{GateEval}(\mathcal{G},X,Y)=H(X,Y,i)\oplus E^{(a,b)}
$$

where $a$ is the first bit of $X$ and $b$ is the first bit of $Y$.

This is just like the above scheme where the double encryption is realized by the hash function and the XOR operation. So we can also introduce such a **point-and-permute** method into the scheme above. Suppose $E^{(a,b)}=\mathsf{Enc}_{k_i^a}(\mathsf{Enc}_{k_j^b}(k_t^{g(a,b)}))$, and the table is

$$
E^{(1,0)},E^{(1,1)},E^{(0,0)},E^{(0,1)}
$$

So we let the $k_i^a$ begin by $1-a$ and $k_j^b$ begin by $b$, the evaluator would know from the keys which entry to decode. Note that this method only supports $4$ out of $|S_4|=24$ permutations.

The correctness of the algorithm is one line of formula. When computing, if the first input wire has value $u$, then the corresponding encoding is $X^u:=A^{u\oplus r}$, and the same for the second input and the output, say, $Y^v:=B^{v\oplus s}$ and $Z^w:=C^{w\oplus t}$. Then we have

$$
\mathsf{GateEval}(\mathcal{G},X^u,Y^v)=H(A^{u\oplus r},B^{v\oplus s},i)\oplus E^{(u\oplus r,v\oplus s)}=C^{g(u,v)\oplus t}=Z^{g(u,v)}.
$$

The random bit here is used to mask the true value. Imagine you send $A^u,B^v$ directly, the evaluator immediately knows the hidden value because $A^u$ has the first bit $u$, and the same as $B^v$.

### The full protocol

$$
\begin{align*}&\text{Garbler},\left(x^{(0)}_i\right)_{i=0}^{k-1}&&&\text{Evaluator},\left(x^{(1)}_i\right)_{i=k}^{n-1}\\&\mathcal{F}=\{\mathcal{G}_i\}_{i=0}^{t-1}, \quad e=((X_1^0,X_1^1),\ldots,(X_n^0,X_n^1)), \quad d=((Y_1^0,Y_1^1),\ldots,(Y_m^0,Y_m^1))&\xrightarrow{\mathcal{F},\;\left(X_i^{x^{(0)}_i}\right)_{i=0}^{k-1}}&&\\&e&\xleftrightarrow{\text{1-out-of-2 }\mathbf{OT}}&&\left(X_i^{x^{(1)}_i}\right)_{i=k}^{n-1}\\&y=\mathsf{Decode}\left(d,\mathcal{Y}\right)&\xleftarrow{\mathcal{Y}}&&\mathcal{Y}=\mathsf{Eval}\left(\mathcal{F},\left(X_i^{x_i}\right)_{i=0}^{n-1}\right)\text{, runs }\mathsf{GateEval}\text{ on each gate}\\\end{align*}
$$

### Why OT?

Here is a more direct version: the garbler sends the full $(X_i^0,X_i^1)$ and let the evaluator choose one from the pair. Thus the garbler will not know what the evaluator chooses; so the problem is, why do we mask the other value from the evaluator in the protocol $\texttt{Garble0}$?

For one AND gate $x_1\land x_2$, where $x_1$ is from the garbler and $x_2$ is from the evaluator. Now suppose the evaluator gets both $X_2^0$ and $X_2^1$, and the evaluator would secretly compute the garbled output with the garbled circuit, using different values of $x_2$. If the garbled output are different, the evaluator knows that $x_1=1$.

### FreeXOR

The garbler uses a global difference $\Delta$ and let for every wire, $X^0\oplus\Delta=X^1$. For one XOR gate, let the labels of the input/output gates be $A^0,A^1=A^0\oplus \Delta,B^0,B^1=B^0\oplus \Delta,C^0=A^0\oplus B^0,C^1=C^0\oplus \Delta$. Then if the two inputs are $x,y$ then $A^{x}\oplus B^y=A^0\oplus B^0\oplus x\Delta\oplus y\Delta=C^{0}\oplus (x\oplus y)\Delta=C^{x\oplus y}$.

The evaluator cannot have access to $\Delta$ and the reason is the same as **Why OT**. Now communication is $0$ per XOR and $4\kappa$ per AND; verification is $0$ per XOR and $\kappa$ per AND.

### 3-party protocol against 1 malicious adversary

We consider a 3-party setting where $P_1$ and $P_2$ hold private inputs (a partition of the $n$ input bits), and an additional party $P_3$ acts as an evaluator. The goal is to compute $f(x)$ while tolerating 1 malicious adversary.

High-level idea: $P_1$ and $P_2$ jointly generate the *same* garbled circuit $\mathcal{F}$ (using shared randomness) and send it to $P_3$ together with *commitments/hashes* to the wire tokens. Each of $P_1$ and $P_2$ then “opens” only the tokens corresponding to its own input bits, in a way that lets $P_3$ evaluate but not learn the raw input bits.

Protocol sketch (for a fixed circuit $f$):

A compact “message-flow” diagram (aligned):

$$
\begin{align*}P_1(x^{(1)}) && P_2(x^{(2)}) && P_3 \\(\mathcal{F},e,d) \leftarrow \mathsf{Garble}(f;G(s))\,,\; \{C_i^{(b)}\}_{i,b}& \xrightarrow{\;\mathcal{F},\,\{C_i^{(b)}\}\; }& (\mathcal{F},e,d) \leftarrow \mathsf{Garble}(f;G(s))\,,\; \{C_i^{(b)}\}_{i,b}& \xrightarrow{\;\mathcal{F},\,\{C_i^{(b)}\}\; }& \text{check and store }\mathcal{F},\{C_i^{(b)}\} \\(i,a_i, X_i, r_i)_{i\in I_1}& \xrightarrow{\text{open own inputs}}&&& \text{check } C_i^{(a_i)} = H_1(X_i,r_i) \\&& (i,a_i, X_i, r_i)_{i\in I_2}& \xrightarrow{\text{open own inputs}}& \text{check } C_i^{(a_i)} = H_1(X_i,r_i) \\y \leftarrow \mathsf{Decode}(d,\mathcal{Y})& \xleftarrow{\;\mathcal{Y}\; } & y \leftarrow \mathsf{Decode}(d,\mathcal{Y})& \xleftarrow{\;\mathcal{Y}\; } & \mathcal{Y} \leftarrow \mathsf{Eval}(\mathcal{F},\mathcal{X})\end{align*}
$$

Here, $e = ((X_1^{(0)}, X_1^{(1)}), \dots, (X_n^{(0)}, X_n^{(1)}))$, and the tuple list $\{C_i^{(b)}\}$ is generated by randomly choosing $(b_i)_{i=1}^n$ and $(r_i^{(b)})_{i\in[n],b\in\{0,1\}}$ and computing $C_i^{(b)}=H_1(X_i^{(b \oplus b_i)}, r_i^{(b)})$.

Then $P_1,P_2$ sends their known bits in the encoded value $X_i=X_i^{(x_i)},a_i=x_i\oplus b_i,r_i=r_i^{(a_i)}$.

Note that the output of the two garblers are expected to be the same, since they use the same PRG $G$ and the same seed $s$.

Why this helps against a malicious party:

- If one of $P_1$ or $P_2$ tries to cheat by sending inconsistent garbling information, $P_3$ detects it because it receives two versions and checks equality.

- If a party tries to cheat by sending an invalid wire token, the hash/commitment check fails.

- The random “swap” bits $b_i$ hide which of the two tokens corresponds to 0/1 for each wire, so $P_3$ can evaluate without learning the underlying input bits.

[BitGC: Garbled Circuits with 1 Bit per Gate](https://app.notion.com/p/BitGC-Garbled-Circuits-with-1-Bit-per-Gate-33fd71e335be804dad33e13a61e02702?pvs=21)

## Multi-party computation with a secure core

“In practice, a typical way to build a multi-party protocol is to start with a secure 3-party protocol, and to use that protocol as a service provided to a larger set of parties.”

Here we consider (for example) how to use Beaver’s 2.5-party maliciously secure protocol to obtain an $N$ -party protocol.

I have many problems with this part, especially with some certain interactions that I do not consider necessary. So I leave it blank. Check out the textbook [A Graduate Course in Applied Cryptography](https://algebraic-arima.github.io/books/appliedcrypto.pdf).

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
