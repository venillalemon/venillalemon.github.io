# Feeding Inputs into a WRK Circuit

*September 29, 2026*

## Motivation

假设 WRK 的 garbled table 已经建好，每条 wire 的 mask 已 share 并认证，每个 garbler 已选好 label，所有 AND gate 的 table 已发出。现在要往 input wire $\omega$ 上送入一个值，让 evaluator 拿到该 wire 上的 masked bit 和 label。

[Garbled Circuits](/files/2026_07_02_Garbled_Circuits.html) 中的 WRK 只处理了值由某个 party 明文持有的情形。这篇处理另外两种来源：

- 值是所有 party 都知道的 public bit $x$；
- 值是一个 BDOZ / TinyOT 式的 authenticated sharing $[x]$，没有任何 party 知道 $x$。

## Setup

$P_1$ 为 evaluator，$P_2,\dots,P_n$ 为 garbler。每个 $P_i$ 持有私有全局 key $\Delta^{(i)}\in\mathbb F_2^\kappa$；对 $i\ge2$ 它同时是 $P_i$ 的 label offset。

**Authenticated sharing.** 对 bit $x$，记 $[x]$ 为

$$
x=\bigoplus_{i=1}^n x^{(i)},\qquad
M^{(i)}_{i\to j,\,x}=K^{(j)}_{i\to j,\,x}\oplus x^{(i)}\Delta^{(j)}
\quad(i\ne j),
$$

其中 $P_i$ 持有 $x^{(i)}$、MAC $\{M^{(i)}_{i\to j,\,x}\}_{j\ne i}$ 和 key $\{K^{(i)}_{j\to i,\,x}\}_{j\ne i}$。$[x]\oplus[y]$ 为份额、MAC、key 逐项 XOR，本地完成。

**Garbling 之后 wire $\omega$ 上已有的东西.**

- 所有 party 持有 mask $[\lambda_\omega]$，$\lambda_\omega$ 对任何真子集保密。
- 每个 garbler $P_j$ 持有 $L^{(j)}_{\omega,0}$ 和 $L^{(j)}_{\omega,1}=L^{(j)}_{\omega,0}\oplus\Delta^{(j)}$。

**目标.** 对 wire 的真实值 $v_\omega$，所有 party 得到公开的 $\widehat v_\omega=v_\omega\oplus\lambda_\omega$，且 $P_1$ 持有

$$
\left(\widehat v_\omega,\ L^{(2)}_{\omega,\widehat v_\omega},\ \dots,\ L^{(n)}_{\omega,\widehat v_\omega}\right).
$$

这正是 [Garbled Circuits](/files/2026_07_02_Garbled_Circuits.html) 中 WRK bootstrapping 之后 input wire 的状态，后续 gate 的 evaluation 不需要任何改动。

## Input from a public bit

wire $\omega$ 的值为所有 party 已知的 $x$。

1. 每个 $P_i$ 公开自己的 mask share 并把 MAC 发给对应的 party：

   $$
   P_i\longrightarrow\text{all}:\quad\lambda_\omega^{(i)},\qquad
   P_i\longrightarrow P_j:\quad M^{(i)}_{i\to j,\,\lambda_\omega}\quad(j\ne i).
   $$

2. 每个 $P_j$ 对所有 $i\ne j$ 检查

   $$
   M^{(i)}_{i\to j,\,\lambda_\omega}\stackrel{?}{=}K^{(j)}_{i\to j,\,\lambda_\omega}\oplus\lambda_\omega^{(i)}\Delta^{(j)},
   $$

   失败则 abort。

3. 每个 party 本地计算

   $$
   \widehat v_\omega=x\oplus\bigoplus_{i=1}^n\lambda_\omega^{(i)}.
   $$

4. 每个 garbler 发送与 $\widehat v_\omega$ 对应的 label：

   $$
   P_j\longrightarrow P_1:\quad L^{(j)}_{\omega,\widehat v_\omega}\qquad(j\ge2).
   $$

**Claim.** $P_1$ 持有 $\left(\widehat v_\omega,L^{(2)}_{\omega,\widehat v_\omega},\dots,L^{(n)}_{\omega,\widehat v_\omega}\right)$，$\widehat v_\omega=x\oplus\lambda_\omega$。

**Security.** 值 $x$ 是公开的，没有东西需要隐藏；公开 $\lambda_\omega$ 不影响其他 wire，因为 WRK 的 selective failure 论证只用到秘密 wire 的诚实 mask share。腐化 $P_i$ 若篡改 $\lambda_\omega^{(i)}$，需在不知 $\Delta^{(j)}$ 的情况下伪造 MAC，成功概率 $2^{-\kappa}$。腐化 garbler 若发错 label，下一个用到 $\omega$ 的 gate 会因 MAC 检查失败而 abort，与任何秘密无关。

步骤 1–2 与 $x$ 无关，可放进 preprocessing，online 只剩步骤 3–4。若建电路时就知道 $\omega$ 是 public wire，可直接取 $[\lambda_\omega]=[0]$（份额、MAC、key 全为零），此时 $\widehat v_\omega=x$，只剩步骤 4。

## Input from a BDOZ share

wire $\omega$ 的值为 $x$，各 party 持有 $[x]$，其 MAC key 与 WRK 的 $\Delta^{(1)},\dots,\Delta^{(n)}$ 相同（例如 $[x]$ 来自同一组 key 下的 TinyOT preprocessing，或前一段电路的 authenticated 输出）。没有 party 知道 $x$。

1. 每个 $P_i$ 本地计算 $[\widehat v_\omega]=[x]\oplus[\lambda_\omega]$，即

   $$
   \widehat v_\omega^{(i)}=x^{(i)}\oplus\lambda_\omega^{(i)},\qquad
   M^{(i)}_{i\to j,\,\widehat v_\omega}=M^{(i)}_{i\to j,\,x}\oplus M^{(i)}_{i\to j,\,\lambda_\omega},\qquad
   K^{(i)}_{j\to i,\,\widehat v_\omega}=K^{(i)}_{j\to i,\,x}\oplus K^{(i)}_{j\to i,\,\lambda_\omega}
   \quad(j\ne i).
   $$

2. 每个 $P_i$ 公开自己的份额并把 MAC 发给对应的 party：

   $$
   P_i\longrightarrow\text{all}:\quad\widehat v_\omega^{(i)},\qquad
   P_i\longrightarrow P_j:\quad M^{(i)}_{i\to j,\,\widehat v_\omega}\quad(j\ne i).
   $$

3. 每个 $P_j$ 对所有 $i\ne j$ 检查

   $$
   M^{(i)}_{i\to j,\,\widehat v_\omega}\stackrel{?}{=}K^{(j)}_{i\to j,\,\widehat v_\omega}\oplus\widehat v_\omega^{(i)}\Delta^{(j)},
   $$

   失败则 abort。

4. 每个 party 本地计算

   $$
   \widehat v_\omega=\bigoplus_{i=1}^n\widehat v_\omega^{(i)}.
   $$

5. 每个 garbler 发送与 $\widehat v_\omega$ 对应的 label：

   $$
   P_j\longrightarrow P_1:\quad L^{(j)}_{\omega,\widehat v_\omega}\qquad(j\ge2).
   $$

**Claim.** $P_1$ 持有 $\left(\widehat v_\omega,L^{(2)}_{\omega,\widehat v_\omega},\dots,L^{(n)}_{\omega,\widehat v_\omega}\right)$，$\widehat v_\omega=x\oplus\lambda_\omega$。

**Correctness.**

$$
\bigoplus_i\widehat v_\omega^{(i)}=\bigoplus_i\left(x^{(i)}\oplus\lambda_\omega^{(i)}\right)=x\oplus\lambda_\omega .
$$

**Security.** 被公开的是 $x^{(i)}\oplus\lambda_\omega^{(i)}$。诚实 party 的 $\lambda_\omega^{(i)}$ 均匀随机且从未公开，所以这些份额对对手均匀，$x$ 不泄露；$[x]$ 本身没有被打开，之后仍可使用。腐化 $P_i$ 若篡改 $\widehat v_\omega^{(i)}$，需在不知 $\Delta^{(j)}$ 的情况下伪造 MAC，成功概率 $2^{-\kappa}$。腐化 garbler 若发错 label，下一个用到 $\omega$ 的 gate 会因 MAC 检查失败而 abort；garbler 做选择时只知道公开的 $\widehat v_\omega$，所以 abort 与 $x$ 无关，没有 selective failure。
