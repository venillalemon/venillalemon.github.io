# Feeding Inputs into a WRK Circuit

*September 29, 2026*

## Motivation

Suppose the WRK garbled tables have already been built: the mask of every wire has been shared and authenticated, every garbler has chosen its labels, and the tables of all AND gates have been sent. We now want to feed a value into an input wire $\omega$, so that the evaluator obtains the masked bit and the labels on that wire.

WRK as presented in [Garbled Circuits](/files/2026_07_02_Garbled_Circuits.html) only handles the case where the value is held in the clear by some party. This note handles two other sources:

- the value is a public bit $x$ known to all parties;
- the value is a BDOZ / TinyOT-style authenticated sharing $[x]$, and no party knows $x$.

## Setup

$P_1$ is the evaluator and $P_2,\dots,P_n$ are the garblers. Each $P_i$ holds a private global key $\Delta^{(i)}\in\mathbb F_2^\kappa$; for $i\ge2$ it is also $P_i$'s label offset.

**Authenticated sharing.** For a bit $x$, write $[x]$ for

$$
x=\bigoplus_{i=1}^n x^{(i)},\qquad
M^{(i)}_{i\to j,\,x}=K^{(j)}_{i\to j,\,x}\oplus x^{(i)}\Delta^{(j)}
\quad(i\ne j),
$$

where $P_i$ holds $x^{(i)}$, the MACs $\{M^{(i)}_{i\to j,\,x}\}_{j\ne i}$ and the keys $\{K^{(i)}_{j\to i,\,x}\}_{j\ne i}$. $[x]\oplus[y]$ is the entrywise XOR of shares, MACs and keys, done locally.

**What wire $\omega$ already has after garbling.**

- All parties hold the mask $[\lambda_\omega]$; $\lambda_\omega$ is hidden from every proper subset of the parties.
- Each garbler $P_j$ holds $L^{(j)}_{\omega,0}$ and $L^{(j)}_{\omega,1}=L^{(j)}_{\omega,0}\oplus\Delta^{(j)}$.

**Goal.** For the true value $v_\omega$ of the wire, all parties obtain the public $\widehat v_\omega=v_\omega\oplus\lambda_\omega$, and $P_1$ holds

$$
\left(\widehat v_\omega,\ L^{(2)}_{\omega,\widehat v_\omega},\ \dots,\ L^{(n)}_{\omega,\widehat v_\omega}\right).
$$

Throughout, we borrow the notation of [Garbled Circuits](/files/2026_07_02_Garbled_Circuits.html).

## Input from a public bit

The value of wire $\omega$ is $x$, known to all parties.

1. Offline: the parties open $[\lambda_\omega]$ (publish shares, send MACs, check MACs), abort on failure; all parties obtain $\lambda_\omega$.

2. Each party locally computes

   $$
   \widehat v_\omega=x\oplus\lambda_\omega .
   $$

3. Each garbler sends the label corresponding to $\widehat v_\omega$:

   $$
   P_j\longrightarrow P_1:\quad L^{(j)}_{\omega,\widehat v_\omega}\qquad(j\ge2).
   $$

**Claim.** $P_1$ holds $\left(\widehat v_\omega,L^{(2)}_{\omega,\widehat v_\omega},\dots,L^{(n)}_{\omega,\widehat v_\omega}\right)$, with $\widehat v_\omega=x\oplus\lambda_\omega$.

**Security.** The value $x$ is public, so there is nothing to hide; opening $\lambda_\omega$ does not affect other wires, because the WRK selective failure argument only uses the honest mask shares of secret wires. If a corrupted $P_i$ tampers with $\lambda_\omega^{(i)}$, it must forge a MAC without knowing $\Delta^{(j)}$, which succeeds with probability $2^{-\kappa}$. If a corrupted garbler sends a wrong label, the next gate that uses $\omega$ aborts because the MAC check fails, independently of any secret.

Step 1 is independent of $x$; only steps 2–3 are online. If it is known when building the circuit that $\omega$ is a public wire, one can directly take $[\lambda_\omega]=[0]$ (shares, MACs and keys all zero); then $\widehat v_\omega=x$ and only step 3 remains.

**Online communication.** One round, all sent to $P_1$, one label per garbler:

$$
(n-1)\kappa\ \text{bit}.
$$

## Input from a BDOZ share

The value of wire $\omega$ is $x$; the parties hold $[x]$, whose MAC keys are the same as WRK's $\Delta^{(1)},\dots,\Delta^{(n)}$. No party knows $x$. $P_1$ is the evaluator, $P_2,\dots,P_n$ are the garblers, and $L^{(j)}_{\omega,1}=L^{(j)}_{\omega,0}\oplus\Delta^{(j)}$.

1. Each $P_i$ locally computes $[\widehat v_\omega]=[x]\oplus[\lambda_\omega]$, i.e.

   $$
   \widehat v_\omega^{(i)}=x^{(i)}\oplus\lambda_\omega^{(i)},\qquad
   M^{(i)}_{i\to j,\,\widehat v_\omega}=M^{(i)}_{i\to j,\,x}\oplus M^{(i)}_{i\to j,\,\lambda_\omega},\qquad
   K^{(j)}_{i\to j,\,\widehat v_\omega}=K^{(j)}_{i\to j,\,x}\oplus K^{(j)}_{i\to j,\,\lambda_\omega}
   \quad(j\ne i).
   $$

2. For all $i\ge 2$, the following messages do not depend on one another:

   $$
   \begin{aligned}
   P_i\longrightarrow P_1:&\quad \widehat v_\omega^{(i)},\ M^{(i)}_{i\to 1,\,\widehat v_\omega},\\
   P_i\longrightarrow P_1:&\quad S^{(i)}_\omega
     =L^{(i)}_{\omega,0}\oplus\widehat v_\omega^{(i)}\Delta^{(i)}
      \oplus\bigoplus_{j\ne i}K^{(i)}_{j\to i,\,\widehat v_\omega},\\
   P_i\longrightarrow P_1:&\quad M^{(i)}_{i\to j,\,\widehat v_\omega}\quad\text{for all }j\notin\{1,i\}.
   \end{aligned}
   $$

3. $P_1$ checks, for all $i\ge2$,

   $$
   M^{(i)}_{i\to 1,\,\widehat v_\omega}\stackrel{?}{=}K^{(1)}_{i\to 1,\,\widehat v_\omega}\oplus\widehat v_\omega^{(i)}\Delta^{(1)},
   $$

   and aborts on failure. It then computes $\widehat v_\omega=\bigoplus_{i=1}^n\widehat v_\omega^{(i)}$.

4. For each garbler $j\ge2$, $P_1$ locally computes

   $$
   S^{(j)}_\omega\oplus\bigoplus_{i\ne j}M^{(i)}_{i\to j,\,\widehat v_\omega},
   $$

   where the $i=1$ term $M^{(1)}_{1\to j,\,\widehat v_\omega}$ is held by $P_1$ itself.

**Claim.** $P_1$ holds $\left(\widehat v_\omega,L^{(2)}_{\omega,\widehat v_\omega},\dots,L^{(n)}_{\omega,\widehat v_\omega}\right)$, with $\widehat v_\omega=x\oplus\lambda_\omega$. The other parties do not know $\widehat v_\omega$.

**Correctness.** Since $M^{(i)}_{i\to j}=K^{(j)}_{i\to j}\oplus\widehat v^{(i)}_\omega\Delta^{(j)}$,

$$
S^{(j)}_\omega\oplus\bigoplus_{i\ne j}M^{(i)}_{i\to j,\,\widehat v_\omega}
=L^{(j)}_{\omega,0}\oplus\widehat v_\omega^{(j)}\Delta^{(j)}\oplus\bigoplus_{i\ne j}\widehat v_\omega^{(i)}\Delta^{(j)}
=L^{(j)}_{\omega,0}\oplus\widehat v_\omega\Delta^{(j)}
=L^{(j)}_{\omega,\widehat v_\omega}.
$$

**Security.**

- *Privacy.* The $\widehat v_\omega^{(i)}$ seen by $P_1$ are masked by the honest parties' uniformly random, never-opened $\lambda_\omega^{(i)}$, so $x$ is not leaked; $[x]$ is not opened and can still be used afterwards. $S^{(j)}_\omega$ is masked by the fresh $L^{(j)}_{\omega,0}$ and does not leak $K^{(j)}_{i\to j}$; the key of $M^{(i)}_{i\to j}$ is one-time and does not leak $\Delta^{(j)}$. From an honest garbler $j$, $P_1$ can only obtain $L^{(j)}_{\omega,\widehat v_\omega}$; obtaining the other label requires $\Delta^{(j)}$.
- *Integrity of $\widehat v_\omega$.* For a corrupted $P_i$ to tamper with $\widehat v_\omega^{(i)}$, it must forge a MAC without knowing $\Delta^{(1)}$, which succeeds with probability $2^{-\kappa}$.
- *Integrity of the labels.* $P_1$ does not know $\Delta^{(j)}$ ($j\ge2$), so in step 2 $S^{(j)}_\omega$ and $M^{(i)}_{i\to j}$ are **not checked**. If a corrupted party adds $e$ to any of them, $P_1$ obtains $L^{(j)}_{\omega,\widehat v_\omega}\oplus e$; the next gate that uses $\omega$ aborts because the row's MAC check fails, unless $e\in\{0,\Delta^{(j)}\}$. For an honest garbler $j$, the probability that $e=\Delta^{(j)}$ is $2^{-\kappa}$; if garbler $j$ is itself corrupted, it can flip its own label to $L^{(j)}_{\omega,\widehat v_\omega\oplus1}$, but this is inconsistent with the honest garblers' labels and likewise fails at the next gate. When the sender makes its decision it does not even know $\widehat v_\omega$ (it is no longer public), so the abort is independent of $x$ and there is no selective failure.

**Online communication.** One round, all sent to $P_1$. Each garbler sends $\widehat v_\omega^{(i)}$ (1 bit), $M^{(i)}_{i\to1,\widehat v_\omega}$ and $S^{(i)}_\omega$ ($\kappa$ bits each), and $n-2$ values $M^{(i)}_{i\to j,\widehat v_\omega}$ ($\kappa$ bits each), in total

$$
(n-1)(n\kappa+1)\ \text{bit}.
$$
