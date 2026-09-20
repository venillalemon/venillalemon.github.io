# Oblivious Transfer

*September 2, 2026*

## $1$-out-of-$2$ OT

Sender $S$ holds $(m_0,m_1)$; receiver $R$ holds $b\in\{0,1\}$:

$$
\begin{aligned}
S &: (m_0,m_1), & R &: b,\\
\mathsf{OT}((m_0,m_1),b)&\longrightarrow (\bot,m_b).
\end{aligned}
$$

- $S$ learns nothing about $b$.
- $R$ learns nothing about $m_{1-b}$ beyond its input and $m_b$.

For bits, $m_b=m_0\oplus b(m_0\oplus m_1)$. This gives a sharing of a product:

$$
S:\ x,\ r\leftarrow\mathbb F_2,\ (m_0,m_1)=(r,r\oplus x),
\qquad R:\ y,
$$

$$
s=m_y=r\oplus xy,\qquad r\oplus s=xy.
$$

$S$ keeps $r$; $R$ keeps $s$.

## Direct constructions

OT can be instantiated with public-key constructions:

- **Naor–Pinkas:** DDH.
- **Chou–Orlandi (Simplest OT):** Diffie–Hellman groups + hashing.
- **PVW:** DDH / quadratic residuosity / LWE.

The bottleneck is repeating expensive public-key operations. For example, [GMW](/files/2026_03_15_MPC:_Secret_Sharing.html) uses $n(n-1)$ OTs per AND gate:

$$
\#\mathrm{OT}=n(n-1)N_\land,\qquad
n=2,\ N_\land=10^6\ \Longrightarrow\ \#\mathrm{OT}=2\cdot10^6.
$$

## IKNP extension

**IKNP** bootstraps many OTs from a few base OTs:

$$
\kappa\text{ base OTs}+\text{PRG, hash, XOR}
\quad\Longrightarrow\quad m\gg\kappa\text{ OTs}.
$$

Let $S$ hold $\ell$-bit message pairs $(m_{i,0},m_{i,1})$, $R$ hold choices $r\in\mathbb F_2^m$, and $G:\{0,1\}^\kappa\to\{0,1\}^m$ be a PRG.

- **Base OTs (roles reversed).** $R$ samples seeds $k_j^0,k_j^1$; $S$ samples $s\in\mathbb F_2^\kappa$. For $j\in[\kappa]$:

  $$
  R:(k_j^0,k_j^1)
  \quad\xrightarrow{\mathrm{OT},\ \text{choice }s_j}\quad
  S:k_j^{s_j}.
  $$

- **Expand.** $R$ computes and sends $u^j$; $S$ computes $q^j$:

  $$
  \begin{aligned}
  t^j&=G(k_j^0),\\
  u^j&=G(k_j^0)\oplus G(k_j^1)\oplus r,\\
  q^j&=G(k_j^{s_j})\oplus s_j u^j=t^j\oplus s_j r.
  \end{aligned}
  $$

- **Transpose.** $t^j,q^j$ are columns of $T,Q\in\mathbb F_2^{m\times\kappa}$; their rows satisfy

  $$
  q_i=t_i\oplus r_i s
  \quad\Longrightarrow\quad
  t_i=\begin{cases}q_i&r_i=0,\\q_i\oplus s&r_i=1.\end{cases}
  $$

- **Transfer.** $S$ sends $(c_{i,0},c_{i,1})$; $R$ decrypts:

  $$
  \begin{aligned}
  c_{i,0}&=m_{i,0}\oplus H(i,q_i),\\
  c_{i,1}&=m_{i,1}\oplus H(i,q_i\oplus s),\\
  m_{i,r_i}&=c_{i,r_i}\oplus H(i,t_i).
  \end{aligned}
  $$

Here $H$ is modeled as a random oracle with $\ell$-bit output; $i$ includes the batch identifier. $S$ lacks the other seeds, hiding $r$; $R$ lacks $s$, hiding the other pad.

**Cost.** Per batch between two parties, excluding base-OT communication:

$$
\begin{aligned}
\text{base OTs:}&\quad m\ \longrightarrow\ \kappa,\\
\text{hash calls:}&\quad 2m\ (S)+m\ (R),\\
\text{communication:}&\quad m\kappa+2m\ell\text{ bits}.
\end{aligned}
$$

The public-key cost is amortized to $\kappa/m$ base OTs per transfer; the remaining work is PRG expansion, transposition, XOR, and hashing. This is the semi-honest version; malicious security needs additional consistency checks.

References: [IKNP03](https://www.iacr.org/archive/crypto2003/27290145/27290145.pdf), [seed-based extension](https://eprint.iacr.org/2014/692.pdf), [Naor–Pinkas / PVW](https://www.iacr.org/archive/crypto2008/51570556/51570556.pdf), [Chou–Orlandi](https://eprint.iacr.org/2015/267.pdf).

