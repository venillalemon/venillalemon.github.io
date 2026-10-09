# Oblivious Transfer

*September 2, 2026*

## Definitions and equivalences

### 1-out-of-2 OT

全文取 $\kappa$ 为安全参数，消息长度为 $\kappa$。Sender 记 $S$，receiver 记 $R$。

> **Definition (1-out-of-2 OT).** $S$ 输入 $(m_0,m_1)\in\{0,1\}^\kappa\times\{0,1\}^\kappa$，$R$ 输入 choice bit $b\in\{0,1\}$：
>
> $$
> \mathsf{OT}\big((m_0,m_1);\,b\big)\longrightarrow(\bot;\,m_b).
> $$
>
> - **Sender security**：$R$ 除 $m_b$ 外学不到 $m_{1-b}$ 的任何信息。
> - **Receiver security**：$S$ 学不到 $b$。

### Random OT and correlated OT

下面两个变体依次拿掉 party 的选择权。

> **Definition (Random OT).** 双方无输入。functionality 采样 $(a_0,a_1)\xleftarrow{\$}\{0,1\}^\kappa\times\{0,1\}^\kappa$ 和 $r\xleftarrow{\$}\{0,1\}$：
>
> $$
> \mathsf{ROT}(\bot;\,\bot)\longrightarrow\big((a_0,a_1);\ (r,\,a_r)\big).
> $$
>
> - **Sender security**：$R$ 学不到 $a_{1-r}$。
> - **Receiver security**：$S$ 学不到 $r$。
>
> 与 1-out-of-2 OT 的区别：$S$ 不能选择 $(a_0,a_1)$，$R$ 不能选择 $r$。
> 

> 
> **Definition (Correlated OT).** $S$ 输入 correlation $\Delta\in\{0,1\}^\kappa$，$R$ 无输入。functionality 采样 $q\xleftarrow{\$}\{0,1\}^\kappa$ 和 $r\xleftarrow{\$}\{0,1\}$：
>
> $$
> \mathsf{COT}(\Delta;\,\bot)\longrightarrow\big(q;\ (r,\,t)\big),\qquad t=q\oplus r\Delta .
> $$
>
> - **Sender security**：$R$ 学不到 $\Delta$，因此学不到另一条消息 $t\oplus\Delta$。
> - **Receiver security**：$S$ 学不到 $r$。
>
> 与 random OT 的区别：$S$ 的两条消息 $(q,\,q\oplus\Delta)$ 之差固定为 $\Delta$。$m$ 个实例共用同一个 $\Delta$：
>
> $$
> t_i=q_i\oplus r_i\Delta,\qquad i\in[m].
> $$
> 

COT 正是 MPC 需要的 correlation：取 $\kappa=1$，$\Delta=x$，并用下一小节的 derandomization 把 $r$ 换成 $R$ 想要的 $y$，则

$$
q\oplus t=xy,
$$

$S$ 持有 $q$，$R$ 持有 $t$，二者是乘积 $xy$ 的 sharing。GMW 的每个 AND gate 用两次。

### Equivalence

**Trivial direction.** 手上有一个较强的 OT 协议，要实现较弱的那个，只需把自己多出来的选择权用随机数填掉，直接调用即可，不需要任何额外通信：

- **1-out-of-2 OT $\Rightarrow$ COT.** 目标是 COT，$S$ 手上有 $\Delta$，$R$ 手上什么都没有。$S$ 采样 $q$，以 $(q,\,q\oplus\Delta)$ 为输入；$R$ 采样 $r$，以 $b=r$ 为输入；跑一次 1-out-of-2 OT。$S$ 得到 $q$，$R$ 得到 $(r,\,q\oplus r\Delta)$，正是 COT 的输出。
- **COT $\Rightarrow$ random OT.** 目标是 random OT，双方手上什么都没有。$S$ 采样 $\Delta$，以它为输入跑一次 COT，得到 $(q,\,q\oplus\Delta)$；$R$ 得到 $(r,\,t)$。$\Delta$ 均匀随机，所以 $(q,\,q\oplus\Delta)$ 是一对均匀独立的消息，正是 random OT 的输出。这里每个实例的 $\Delta$ 必须独立采样。若 $m$ 个实例共用同一个 $\Delta$（OT extension 产出的正是这种），$R$ 在任一实例学到 $\Delta$ 就能打开全部实例，这批 COT 不是 $m$ 个独立的 random OT。此时用 random oracle $H:[m]\times\{0,1\}^\kappa\to\{0,1\}^\kappa$ 打断关联：

  $$
  a_0=H(i,q_i),\qquad a_1=H(i,q_i\oplus\Delta),\qquad a_{r_i}=H(i,t_i).
  $$

  $R$ 不知道 $\Delta$，算不出 $H(i,t_i\oplus\Delta)$；下标 $i$ 使不同实例的 pad 独立。

所以困难程度是 1-out-of-2 OT $\geq$ COT $\geq$ random OT：能选的越少，越容易生产。后文的构造只生产 COT 或 random OT。

**Reverse direction.** 三者等价，还需要从最容易的 random OT 造回 1-out-of-2 OT。这一步称为 derandomization，来自 Beaver 的 precomputed OT，意思是把随机输入换成真正想用的输入，与复杂性理论里的 derandomization 无关。$S$ 输入 $(m_0,m_1)$，$R$ 输入 $b$，先调用一次 random OT，再用两条消息把随机输出换成真实输入：

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

Correctness：$c_b$ 用的 pad 下标是 $b\oplus d=r$，正是 $R$ 持有的 $a_r$。

Security：$d$ 被均匀的 $r$ 遮住，$S$ 学不到 $b$；$R$ 缺 $a_{1\oplus r}$，打不开 $c_{1\oplus b}$。在线通信只有 $1+2\kappa$ bit，所有公钥运算都落在生产 random OT 的阶段。

### Why OT needs public-key assumptions

OT 蕴含 key agreement，而 Impagliazzo–Rudich 证明 key agreement 不能 black-box 地从 one-way function 或 random oracle 构造。所以 OT 至少要用一次公钥类假设；后文的全部技巧都是让这一次尽可能少。

## Base OT: Chou–Orlandi

**Motivation.** 上一节说明只需生产 random OT 或 COT，但它们本身仍需公钥假设。本节给出一个具体构造。它只需跑 $\kappa$ 次，之后由 OT extension 接管。

**Objects.** $\mathbb G$ 是素数阶 $p$ 的循环群，生成元 $g$，CDH 假设成立。$H:\mathbb G\to\{0,1\}^\kappa$ 是 random oracle。$S$ 持有 $(m_0,m_1)$，$R$ 持有 $b$。

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

**Claim.** $R$ 输出 $m_b$。

Correctness：$B/A^{b}=g^{\beta}$，故 $(B/A^{b})^{\alpha}=g^{\alpha\beta}=A^{\beta}$，即 $k_b=k$。

Security：$B=g^{\beta}A^{b}$ 对 $b=0,1$ 都在 $\mathbb G$ 上均匀，$S$ 学不到 $b$。$R$ 要得到 $k_{1-b}$ 需算 $(B/A^{1-b})^{\alpha}=A^{\beta}\cdot g^{\pm\alpha^2}$，而由 $A=g^{\alpha}$ 求 $g^{\alpha^2}$ 等价于 CDH。

批量 $\ell$ 个实例复用 $\alpha$ 和 $A$，$H$ 额外吸收实例下标，每个 party 每实例约一次 exponentiation。

**Malicious receiver.** 对 malicious $R$，simulator 只能从 $R$ 对 $H$ 的查询中读出 $b$（查的是 $B^{\alpha}$ 还是 $(B/A)^{\alpha}$）。但 $R$ 可以把查询推迟到收到 $c_0,c_1$ 之后，而 simulator 在那之前就必须向 functionality 索取 $m_b$ 才能构造 $c_0,c_1$。因此 CO 不能直接作为 UC 安全的 base OT。emp-ot 默认的 CSW 在 CO 之上加一轮 challenge–response，迫使 $R$ 在 $S$ 接受之前查询 $H$。PVW 和 BMM 走另一条路，把 DH 换成 PKE：$R$ 生成两个 public key，只对其中一个持有 secret key。

## IKNP: COT extension

**Motivation.** 上一节每个 OT 花一次公钥运算。IKNP 只跑 $\kappa$ 次 base OT，之后用 PRG 和 XOR 生产 $m\gg\kappa$ 个 COT。

**Objects.**

- $\Delta\in\mathbb F_2^{\kappa}$：$S$ 的 correlation，第 $j$ bit 记 $\Delta_j$。
- $r\in\mathbb F_2^{m}$：$R$ 的 choice 向量，第 $i$ bit 记 $r_i$。
- $G:\{0,1\}^{\kappa}\to\mathbb F_2^{m}$：PRG。
- $k_{j,0},k_{j,1}\in\{0,1\}^{\kappa}$，$j\in[\kappa]$：$R$ 采样的 base OT 种子。
- $T,U,Q\in\mathbb F_2^{m\times\kappa}$：列 $j$ 记 $T_{*,j}\in\mathbb F_2^{m}$，行 $i$ 记 $T_{i,*}\in\mathbb F_2^{\kappa}$。$T,U$ 由 $R$ 计算，$Q$ 由 $S$ 计算。

**Protocol.** base OT 的角色反转：$R$ 做 base OT 的 sender，$S$ 以 $\Delta_j$ 为 choice。

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

**Claim.** 对每个 $i\in[m]$，

$$
t_i=q_i\oplus r_i\Delta,
$$

即 $m$ 个 correlation 为 $\Delta$ 的 COT。

Correctness：按列，

$$
Q_{*,j}=G(k_{j,\Delta_j})\oplus\Delta_j\big(G(k_{j,0})\oplus G(k_{j,1})\oplus r\big)=G(k_{j,0})\oplus\Delta_j r=T_{*,j}\oplus\Delta_j r .
$$

读第 $i$ 行得 $Q_{i,j}=T_{i,j}\oplus r_i\Delta_j$。

Security（semi-honest）：$S$ 的 view 是 $U$ 和 $k_{j,\Delta_j}$。每列 $U_{*,j}$ 被 $G(k_{j,1-\Delta_j})$ 遮住，$S$ 没有该种子，由 PRG 安全性 $U$ 与 $r$ 独立。$R$ 的 view 只有 base OT，$\Delta$ 由 base OT 对 sender 的安全性保护。之后按第一节用 $H(i,\cdot)$ 变成 random OT，再 derandomize。

**Cost.** $\kappa$ 次 base OT，$m\kappa$ bit 通信，$2\kappa$ 次 PRG 展开，对比直接做 $m$ 次 base OT。

SoftSpoken 是同一构造的推广：把列 $j$ 的 1-out-of-2 base OT 换成 $\mathbb F_{2^k}$ 上的 small-field VOLE，每 $k$ 列合并为一列，通信降为 $m\kappa/k$ bit，计算升为每 COT 约 $2^k/k$ 次 PRG 调用。IKNP 是 $k=1$。

## Malicious IKNP: KOS check

**Attack.** 上面的 security 假设 $R$ 在每列都用同一个 $r$。malicious $R$ 在列 $j$ 改用 $\rho_j\in\mathbb F_2^{m}$，其中 $\rho_j$ 只在第 $i$ bit 与 $r$ 不同。此时

$$
t_i=q_i\oplus r_i\Delta\oplus\Delta_j e_j,
$$

$e_j$ 是第 $j$ 个单位向量。$R$ 对 $\Delta_j\in\{0,1\}$ 各试一次 $H(i,t_i\oplus\Delta_j e_j)$，看哪个能解开 $c_{r_i}$，就学到 $\Delta_j$；对 $\kappa$ 个实例各做一次就得到整个 $\Delta$，之后能打开所有其他实例的两条消息。

**Objects.** 把 $\mathbb F_2^{\kappa}$ 视为 $\mathbb F_{2^\kappa}$，乘法记 $\cdot$。$\chi_i\in\mathbb F_{2^\kappa}$，$i\in[m]$，是 $S$ 在收到 $U$ 之后才选的随机系数。

**Protocol.** 在 IKNP 的 claim 成立之后、使用 $q_i,t_i$ 之前：

$$
\begin{align*}
&\text{Sender}&&&\text{Receiver}\\
&\chi_1,\dots,\chi_m\xleftarrow{\$}\mathbb F_{2^\kappa}
&\xrightarrow{\chi_1,\dots,\chi_m}&\;&\\
&&\xleftarrow{x,\,t}&\;&x\leftarrow\bigoplus_{i}r_i\chi_i,\quad t\leftarrow\bigoplus_{i}\chi_i\cdot t_i\\
&q\leftarrow\bigoplus_{i}\chi_i\cdot q_i,\quad t\stackrel{?}{=}q\oplus x\cdot\Delta&&&
\end{align*}
$$

不等则 abort。

**Claim.** 诚实的 $R$ 总能通过；作弊的 $R$ 每想学 $\Delta$ 的一个 bit，就要承担 $1/2$ 的 abort 概率。

Correctness：

$$
\bigoplus_i\chi_i\cdot t_i=\bigoplus_i\chi_i\cdot(q_i\oplus r_i\Delta)=q\oplus\Big(\bigoplus_i r_i\chi_i\Big)\cdot\Delta=q\oplus x\cdot\Delta .
$$

Security：若 $R$ 在列 $j$ 用了 $\rho_j\neq r$，则 $t_i=q_i\oplus r_i\Delta\oplus d_i$，其中 $d_i\in\mathbb F_2^{\kappa}$ 的第 $j$ bit 是 $\Delta_j(\rho_{j,i}\oplus r_i)$。$R$ 发送任意 $(x',t')$ 想通过，需要

$$
t'\oplus x'\cdot\Delta=q\oplus\bigoplus_i\chi_i\cdot d_i .
$$

右边对每个不一致的列 $j$ 都依赖于 $\Delta_j$，而 $R$ 不知道 $\Delta_j$，只能猜。每猜错一个就 abort，猜对 $c$ 个的概率是 $2^{-c}$。这与 $R$ 不作弊直接猜 $\Delta$ 的 $c$ 个 bit 无异，剩余 $\kappa-c$ bit 的熵由 $\kappa$ 的余量吸收。

$x$ 是 $r$ 的一个 $S$ 已知的线性函数，$t$ 同理泄露 $t_i$ 的线性组合。修补：$R$ 把 $r$ 延长 $\kappa$ 个均匀随机 bit，这些行只参与 check 后即丢弃，$x$ 和 $t$ 被它们的贡献 one-time pad 住。

两个前提：$\chi_i$ 必须在 $R$ 发出 $U$ 之后才确定，实现中用 Fiat–Shamir 从 transcript 的 hash 派生；base OT 必须对 malicious party 安全，否则 $R$ 可以在 base OT 里作弊拿到两个种子。

## Code notes (emp-ot)

数学协议如上，实现上的差别：

- `ot.h`: `RandomCOT::recv_cot` 发送 $d_i=r_i\oplus b_i$，`COT::send` 构造 $c_0,c_1$，即第一节的 derandomization。choice bit 不单独存储，而是约定 $\mathrm{LSB}(\Delta)=1$、$\mathrm{LSB}(q_i)=0$，于是 $\mathrm{LSB}(t_i)=r_i$。
- `base_ot/co.h`: `CO::send` 对整批复用 $A$，$(B/A)^{\alpha}$ 算作 $B^{\alpha}\cdot A^{-\alpha}$；$H$ 吸收 session id 和实例下标。
- `ot_extension/iknp.h`: $\chi_i$ 由 `io->get_digest()` 的 Fiat–Shamir 派生；每 128 行先用 `GaloisFieldPacking` 打包成一个 $\mathbb F_{2^{128}}$ 元素再做 $\chi$ 线性组合；额外的 128 个 COT 在 `end()` 里生成并牺牲。

## References

- Beaver, [Precomputing Oblivious Transfer](https://link.springer.com/chapter/10.1007/3-540-44750-4_8), CRYPTO 1995.
- Impagliazzo, Rudich, [Limits on the Provable Consequences of One-way Permutations](https://dl.acm.org/doi/10.1145/73007.73012), STOC 1989.
- Chou, Orlandi, [The Simplest Protocol for Oblivious Transfer](https://eprint.iacr.org/2015/267), LATINCRYPT 2015.
- Canetti, Sarkar, Wang, Blazing Fast OT for Three-Round UC OT Extension, PKC 2020.
- Ishai, Kilian, Nissim, Petrank, [Extending Oblivious Transfers Efficiently](https://www.iacr.org/archive/crypto2003/27290145/27290145.pdf), CRYPTO 2003.
- Keller, Orsini, Scholl, [Actively Secure OT Extension with Optimal Overhead](https://eprint.iacr.org/2015/546), CRYPTO 2015.
- Roy, [SoftSpokenOT](https://eprint.iacr.org/2022/192), CRYPTO 2022.
