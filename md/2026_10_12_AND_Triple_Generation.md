# AND Triple Generation: Half-Gate and FKOS

*October 12, 2026*

## Motivation

[MPC: Secret Sharing](/files/2026_03_15_MPC:_Secret_Sharing.html) 的 TinyOT 一节给出了 authenticated random bit 的生成，以及 leaky AND 与 bucketing 的思路。这篇把从 authenticated random bit 到 AND triple 的两条完整路线写出来：

- **Half-gate**（WRK）：用 half-gate 在 authenticated bit 上直接算乘积，自带正确性检查，得到正确但可能 leaky 的候选；
- **FKOS**：用 random OT 算乘积，再用 cut 和 sacrifice 检查正确性，同样得到正确但可能 leaky 的候选。

两条路线的最后一步相同：随机分桶合并候选，消除 leakage，输出随机 triple $([a],[b],[c])$，$c=ab$。

## Setup

$n$ 个 party $P_1,\dots,P_n$。$P_i$ 持有私有 key $\Delta_i\in\mathbb F_{2^\kappa}$。统计安全参数记 $s$。

**Authenticated bit.** 对 bit $x$，记 $[x]$ 为

$$
x=\bigoplus_{i=1}^n x^{(i)},\qquad
M_{j\to i}[x]=K_{i\leftarrow j}[x]\oplus x^{(j)}\Delta_i\quad(i\ne j),
$$

其中 $P_j$ 持有 share $x^{(j)}$、MAC $\{M_{j\to i}[x]\}_{i\ne j}$、key $\{K_{j\leftarrow i}[x]\}_{i\ne j}$。以下运算在本地完成：

- $[x]\oplus[y]$：share、MAC、key 逐项 XOR。
- 加公开 bit $e$：$x^{(1)}\leftarrow x^{(1)}\oplus e$，$K_{i\leftarrow1}[x]\leftarrow K_{i\leftarrow1}[x]\oplus e\Delta_i\ (i\ne1)$，其余不变。记为 $[x]\oplus e$。
- 乘公开 bit $e$：$e[x]$ 为 $[x]$（$e=1$）或全零 sharing（$e=0$）。

$\operatorname{Open}([x])$：每个 $P_j$ 向每个 $P_i$ 发送 $x^{(j)}$ 与 $M_{j\to i}[x]$，$P_i$ 检查 MAC 关系，失败则 abort；通过则所有 party 得到 $x=\bigoplus_jx^{(j)}$。多个 bit 同时 open 仍是一轮。

$\mathsf{aBit}(m)$：由 pairwise correlated OT 得到 $m$ 个 authenticated random bit，构造与一致性检查见 [MPC: Secret Sharing](/files/2026_03_15_MPC:_Secret_Sharing.html) 2.1 节。两条路线都只以它为输入。

**辅助功能.**

- $\mathcal F_{\mathsf{Rand}}$：在所有 party 的消息固定之后输出公开的均匀随机值（coin 或排列）。
- $\mathcal F_{\mathsf{Zero}}$：输出 zero sharing $(z^{(1)},\dots,z^{(n)})$，$z^{(i)}\in\mathbb F_{2^\kappa}$ 均匀且 $\bigoplus_iz^{(i)}=0$。
- commit-then-open：每个 party 先对自己的值发出 commit，收齐所有 commit 后再 open；后 open 的 party 不能根据先 open 的值改自己的值。

记 $\Delta_\Sigma=\bigoplus_i\Delta_i$。固定一个坐标 $\pi:\mathbb F_{2^\kappa}\to\mathbb F_2$（取域元素的某一个固定 bit），setup 保证 $\pi(\Delta_\Sigma)=1$。

**消费端（Beaver AND）.** 对 share $[x],[y]$ 和一个 triple $([a],[b],[c])$：

$$
e=\operatorname{Open}([x]\oplus[a]),\qquad
f=\operatorname{Open}([y]\oplus[b]),\qquad
[xy]=[c]\oplus f[a]\oplus e[b]\oplus ef .
$$

同一层的所有 AND gate 共用一轮 open。

**候选.** 两条路线都先生成 $\ell'$ 个候选

$$
\bigl([a_m],[b_m],[c_m]\bigr)_{m\in[0,\ell')},\qquad c_m=a_mb_m,
$$

其中每个候选可能是 **leaky** 的：对手可能以 $1/2$ 的 abort 风险换取某个 honest party 的 $a_m^{(j)}$。最后由 Bucketing 一节把 $\ell'=\ell B$ 个候选合并成 $\ell$ 个 triple。

## Leaky AND from half-gates (WRK)

### Objects

$$
\bigl([a_m],[b_m],[r_m]\bigr)_{m\in[0,\ell')}\leftarrow\mathsf{aBit}(3\ell').
$$

$H:\{0,1\}^*\to\mathbb F_{2^\kappa}$ 为 hash。

### Protocol

对每个候选独立执行。固定候选 $m$，本小节省略下标 $m$：输入 $[a],[b],[r]$，输出 $[c]$。

1. 调用 $\mathcal F_{\mathsf{Zero}}$ 得 $z^{(i)}$。每个 $P_i$ 本地计算

   $$
   \begin{aligned}
   \phi_i&=z^{(i)}\oplus b^{(i)}\Delta_i\oplus\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[b]\oplus M_{i\to j}[b]\bigr),\\
   \psi_i&=r^{(i)}\Delta_i\oplus\bigoplus_{j\ne i}\bigl(K_{i\leftarrow j}[r]\oplus M_{i\to j}[r]\bigr).
   \end{aligned}
   $$

2. 对每对 $i\ne j$：

   $$
   P_i\longrightarrow P_j:\qquad
   G_{i\to j}=H\bigl(K_{i\leftarrow j}[a]\bigr)\oplus H\bigl(K_{i\leftarrow j}[a]\oplus\Delta_i\bigr)\oplus\phi_i .
   $$

3. 每个 $P_j$ 本地计算

   $$
   E_{i\to j}=H\bigl(M_{j\to i}[a]\bigr)\oplus a^{(j)}G_{i\to j}\quad(i\ne j),\qquad
   T_j=a^{(j)}\phi_j\oplus\psi_j\oplus\bigoplus_{i\ne j}\Bigl(H\bigl(K_{j\leftarrow i}[a]\bigr)\oplus E_{i\to j}\Bigr).
   $$

4. 每个 $P_j$ 以 commit-then-open 公布 $\beta_j=\pi(T_j)$。所有 party 计算

   $$
   d=\bigoplus_j\beta_j,\qquad [c]=[r]\oplus d,\qquad \alpha_j=T_j\oplus d\Delta_j .
   $$

5. 每个 $P_j$ 以 commit-then-open 公布 $\alpha_j$。所有 party 检查

   $$
   \bigoplus_j\alpha_j\overset?=0,
   $$

   失败则 abort。

**Claim.** 诚实执行时 $c=ab$，且检查通过。

**Correctness.** 由 MAC 关系 $K_{i\leftarrow j}[b]\oplus M_{j\to i}[b]=b^{(j)}\Delta_i$，对所有有序对求和并加上对角项，$z^{(i)}$ 求和为零：

$$
\bigoplus_i\phi_i=\Bigl(\bigoplus_jb^{(j)}\Bigr)\Bigl(\bigoplus_i\Delta_i\Bigr)=b\Delta_\Sigma,\qquad
\bigoplus_i\psi_i=r\Delta_\Sigma .
$$

由 $M_{j\to i}[a]=K_{i\leftarrow j}[a]\oplus a^{(j)}\Delta_i$，按 $a^{(j)}$ 分情况得

$$
E_{i\to j}=H\bigl(K_{i\leftarrow j}[a]\bigr)\oplus a^{(j)}\phi_i .
$$

对 $j$ 求和时，每个 $H(K_{i\leftarrow j}[a])$ 在 $T_i$ 与 $T_j$ 中各出现一次而抵消：

$$
\bigoplus_jT_j
=\bigoplus_ja^{(j)}\phi_j\oplus\bigoplus_{i\ne j}a^{(j)}\phi_i\oplus r\Delta_\Sigma
=\Bigl(\bigoplus_ja^{(j)}\Bigr)\Bigl(\bigoplus_i\phi_i\Bigr)\oplus r\Delta_\Sigma
=(ab\oplus r)\Delta_\Sigma .
$$

$\pi$ 线性且 $\pi(\Delta_\Sigma)=1$，故 $d=ab\oplus r$，$c=r\oplus d=ab$，$\bigoplus_j\alpha_j=(ab\oplus r\oplus d)\Delta_\Sigma=0$。

**Security.** $P_j$ 从 $G_{i\to j}$ 看到的是 $\phi_i$ 被 $H(K_{i\leftarrow j}[a])\oplus H(K_{i\leftarrow j}[a]\oplus\Delta_i)$ 掩蔽的值；$P_j$ 由 $M_{j\to i}[a]$ 只能算出其中一项，另一项需要 $\Delta_i$，所以 $b^{(i)}$ 不泄露。$\beta_j$ 是 $T_j$ 的一位，$T_j$ 被 $\psi_j$ 中的随机 $r$ 掩蔽。open 的 $\alpha_i$ 被 $z^{(i)}$ 掩蔽，只给出已知为零的和。commit-then-open 使最后公布的 party 不能把 $\beta_j$ 或 $\alpha_j$ 凑成想要的值。

腐化 $P_i$ 若发送 $G_{i\to j}\oplus\delta$，则 $\alpha_j$ 偏移 $a^{(j)}\delta$，$P_i$ 可以同时把 $\alpha_i$ 偏移 $\delta$ 或不偏移：两种选择下检查恰在 $a^{(j)}$ 取某一个值时通过。于是 abort 与否泄露 $a^{(j)}$，每次尝试以 $1/2$ 的概率 abort。这就是候选 leaky 的含义；检查保证通过时 $c=ab$，但不能阻止这种 selective failure。

**与 garbled-circuit half-gate 的关系.** 把 $P_i$ 看作 garbler、$P_j$ 看作 evaluator：$K_{i\leftarrow j}[a]$ 与 $K_{i\leftarrow j}[a]\oplus\Delta_i$ 是 wire $a^{(j)}$ 的两个 label，$P_j$ 持有的 $M_{j\to i}[a]=K_{i\leftarrow j}[a]\oplus a^{(j)}\Delta_i$ 是其中与 $a^{(j)}$ 对应的那个。$G_{i\to j}$ 就是 [Garbled Circuits](/files/2026_07_02_Garbled_Circuits.html) 中 generator half-gate 的那一行 $T_G$，garbler 的常数 $\lambda_\beta\Delta$ 换成 $\phi_i$；$E_{i\to j}$ 就是 evaluator 算出的输出 label。区别有两处：$P_i$ 把 $H(K_{i\leftarrow j}[a])$ 留在手里而不是当作 label，于是 $H(K_{i\leftarrow j}[a])\oplus E_{i\to j}=a^{(j)}\phi_i$ 成为乘积的 XOR sharing；没有 evaluator half-gate，因为这里 $a$ 与 $b$ 都是 share，$ab\Delta_\Sigma=\bigoplus_{i,j}a^{(j)}\phi_i$ 的每个交叉项各用一个 generator half-gate，对角项本地计算。

## Leaky AND from random OT with cut-and-choose (FKOS)

### Objects

参数 $(N,\nu,T)$：

$$
N=T\ell'+\nu,
$$

$N$ 为候选数，$\nu$ 个候选被完全 open（cut），$T$ 为 sacrifice 组大小。

$$
\bigl([a_m],[b_m],[r_m]\bigr)_{m\in[0,N)}\leftarrow\mathsf{aBit}(3N).
$$

$\mathsf{ROT}$：sender 得到均匀的 $(q_0,q_1)\in\{0,1\}^2$，持有 choice bit $\chi$ 的 receiver 得到 $q_\chi$；见 [Oblivious Transfer](/files/2026_09_02_Oblivious_Transfer.html)。本节对每个候选、每对 $i\ne j$ 用一个独立实例，$P_i$ 为 sender，记其输出为 $(q_{i\to j,0},q_{i\to j,1})$，$P_j$ 为 receiver，choice bit 为 $a^{(j)}$。

$\Pi_1,\Pi_2$ 为 $\mathcal F_{\mathsf{Rand}}$ 输出的均匀随机排列，在全部候选固定之后抽取。

### Multiplication

对每个候选独立执行。固定候选 $m$，本小节省略 $a_m,b_m,r_m$ 的下标；输出 $[c]$。

1. 对每对 $i\ne j$ 调用 $\mathsf{ROT}$：$P_i$ 得 $(q_{i\to j,0},q_{i\to j,1})$，$P_j$ 得 $q_{i\to j,a^{(j)}}$。

2. 对每对 $i\ne j$：

   $$
   P_i\longrightarrow P_j:\qquad
   u_{i\to j}=q_{i\to j,0}\oplus q_{i\to j,1}\oplus b^{(i)} .
   $$

3. 每个 $P_j$ 本地计算

   $$
   v_{i\to j}=q_{i\to j,a^{(j)}}\oplus a^{(j)}u_{i\to j}\quad(i\ne j).
   $$

4. 每个 $P_i$ 本地计算

   $$
   z^{(i)}=a^{(i)}b^{(i)}\oplus\bigoplus_{j\ne i}\bigl(q_{i\to j,0}\oplus v_{j\to i}\bigr).
   $$

5. 每个 $P_i$ 广播 $z^{(i)}\oplus r^{(i)}$。所有 party 计算

   $$
   e=\bigoplus_i\bigl(z^{(i)}\oplus r^{(i)}\bigr),\qquad [c]=[r]\oplus e .
   $$

**Claim.** 诚实执行时 $c=ab$。

**Correctness.** 按 $a^{(j)}$ 分情况，

$$
v_{i\to j}=q_{i\to j,0}\oplus a^{(j)}b^{(i)} .
$$

代入 $z^{(i)}$，每个 $q_{i\to j,0}$ 在 $z^{(i)}$ 与 $z^{(j)}$ 中各出现一次而抵消：

$$
\bigoplus_iz^{(i)}=\bigoplus_ia^{(i)}b^{(i)}\oplus\bigoplus_{i\ne j}a^{(j)}b^{(i)}=ab,
\qquad e=ab\oplus r,\qquad c=ab .
$$

$z^{(i)}$ 没有 MAC，所以 $e$ 不受认证；$[c]$ 的认证信息全部来自 $[r]$，腐化 party 可以把 $e$ 改成任意值，使 $c\ne ab$。下面两步检查正确性。

### Cut

取 $\Pi_1$。对候选 $m=\Pi_1(0),\dots,\Pi_1(\nu-1)$：

$$
\operatorname{Open}([a_m]),\ \operatorname{Open}([b_m]),\ \operatorname{Open}([c_m]),\qquad a_mb_m\overset?=c_m .
$$

失败则 abort；这 $\nu$ 个候选丢弃。

### Sacrifice

取 $\Pi_2$，把剩余 $T\ell'$ 个候选分成 $\ell'$ 组，每组 $T$ 个；组内第一个记为 head $\eta$，其余记为 $k$。对每组的每个 $k$：

1. 一轮 open

   $$
   \rho_{\eta,k}=\operatorname{Open}\bigl([a_\eta]\oplus[a_k]\bigr),\qquad
   \sigma_{\eta,k}=\operatorname{Open}\bigl([b_\eta]\oplus[b_k]\bigr).
   $$

2. 一轮 open

   $$
   \operatorname{Open}\Bigl([c_\eta]\oplus[c_k]\oplus\rho_{\eta,k}[b_k]\oplus\sigma_{\eta,k}[a_k]\oplus\rho_{\eta,k}\sigma_{\eta,k}\Bigr)\overset?=0 .
   $$

失败则 abort。每组保留 $\eta$，丢弃其余 $T-1$ 个。$\ell'$ 个 head 就是本节输出的候选。

**Correctness.** 若 $c_\eta=a_\eta b_\eta$、$c_k=a_kb_k$，代入 $a_\eta=a_k\oplus\rho_{\eta,k}$、$b_\eta=b_k\oplus\sigma_{\eta,k}$：

$$
a_\eta b_\eta=a_kb_k\oplus\sigma_{\eta,k}a_k\oplus\rho_{\eta,k}b_k\oplus\rho_{\eta,k}\sigma_{\eta,k},
$$

所以被 open 的值为 $0$。

**Security.** $P_j$ 只知道 $q_{i\to j,0},q_{i\to j,1}$ 中的一个，$u_{i\to j}$ 中的 $b^{(i)}$ 被另一个掩蔽。$P_i$ 不收任何消息。$e=ab\oplus r$ 被随机 $r$ 掩蔽。sacrifice 中 open 的 $\rho_{\eta,k},\sigma_{\eta,k}$ 被丢弃候选的 $a_k,b_k$ 掩蔽。

记候选 $m$ 的误差为 $c_m\oplus a_mb_m$。对手可以使任意 $g$ 个候选的误差为 $1$，但要在 $\Pi_1,\Pi_2$ 抽取之前决定。通过 cut 要求这 $g$ 个都不在被 open 的 $\nu$ 个之中；通过 sacrifice 要求每组内所有候选误差相同（被 open 的值是 head 与成员误差的 XOR），即 $g$ 个错误候选恰好填满 $g/T$ 个整组。所以

$$
\Pr[\text{存在错误候选且全部检查通过}]
\le\max_{1\le q\le\ell'}
\frac{\binom{N-Tq}{\nu}}{\binom{N}{\nu}}\cdot
\frac{\binom{\ell'}{q}}{\binom{T\ell'}{Tq}} .
$$

$q$ 小时第二个因子小，$q$ 接近 $\ell'$ 时第一个因子小；cut 的作用是堵住“全部候选都错”这种 sacrifice 无法发现的情形。

腐化 $P_i$ 若发送 $u_{i\to j}\oplus\delta$，则 $z^{(j)}$ 偏移 $a^{(j)}\delta$：$a^{(j)}=0$ 时候选正确，$a^{(j)}=1$ 时候选错误并在检查中被发现。abort 与否泄露 $a^{(j)}$，每次尝试以 $1/2$ 的概率 abort。这与 half-gate 的 selective failure 相同，由下一节的 bucketing 消除。

## From leaky candidates to triples: bucketing

### Objects

输入上面任一节输出的 $\ell'=\ell B$ 个候选 $([a_m],[b_m],[c_m])_{m\in[0,\ell')}$，每个满足 $c_m=a_mb_m$，其中若干个可能 leaky。$B\ge2$ 为桶大小。$\Pi_3$ 为 $\mathcal F_{\mathsf{Rand}}$ 输出的均匀随机排列，在全部候选固定之后抽取。

把候选按 $\Pi_3$ 分成 $\ell$ 桶，每桶 $B$ 个；桶 $p\in[0,\ell)$ 内第一个记为 head $\eta$，其余 $B-1$ 个记为 $k$。

### Protocol

1. 一轮 open 全部 $(B-1)\ell$ 个差值：

   $$
   d_{\eta,k}=\operatorname{Open}\bigl([b_\eta]\oplus[b_k]\bigr).
   $$

2. 本地合并：

   $$
   [A_p]=[a_\eta]\oplus\bigoplus_k[a_k],\qquad
   [B_p]=[b_\eta],\qquad
   [C_p]=[c_\eta]\oplus\bigoplus_k\Bigl([c_k]\oplus d_{\eta,k}[a_k]\Bigr).
   $$

**Claim.** 输出 $([A_p],[B_p],[C_p])_{p\in[0,\ell)}$，$C_p=A_pB_p$。

**Correctness.**

$$
C_p=a_\eta b_\eta\oplus\bigoplus_k\bigl(a_kb_k\oplus(b_\eta\oplus b_k)a_k\bigr)
=a_\eta b_\eta\oplus\bigoplus_ka_kb_\eta=A_pB_p .
$$

**Security.** $d_{\eta,k}$ 由 $\operatorname{Open}$ 认证，且被成员候选的随机 $b_k$ 掩蔽。对手要获知 $A_p$，需要桶 $p$ 内全部 $B$ 个候选的 $a$，即桶内全部候选都被它攻击过；每次攻击存活概率 $1/2$，且 $\Pi_3$ 在攻击发生之后才抽取。设对手共攻击 $g$ 个候选，均匀排列下某个固定桶全由被攻击候选组成的概率为 $\binom gB\big/\binom{\ell B}{B}$，对 $\ell$ 个桶求期望并用 Markov 不等式：

$$
\Pr[\text{通过检查且某桶全部 leaky}]
\le\max_{B\le g\le\ell B}2^{-g}\,\frac{\ell\binom gB}{\binom{\ell B}{B}} .
$$

取使右边 $\le2^{-s}$ 的最小 $B$。
