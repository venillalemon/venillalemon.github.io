# Field Extensions

*April 26, 2024*

***Lemma 1.*** $[K:F]=[K:E][E:F]$ ， 如果 $K/E/F$ 是域扩张.

若 $[K:F]$ 有限，则称 $K/F$ 是**有限**扩张.

### 构造

通过向域 $F$ 中添加元素来扩张.

设 $K/F$, $S\subseteq K$ ， $S$ 是 $K$ 的子集， $F(S)$ 表示 $F$ 和 $S$ 生成的最小扩张.

***Lemma 2.*** $F(S)=\{\frac{f(u_1,\dots,u_n)}{g(u_1,\dots,u_n)}: f,g\in F[x_1,\dots,x_n],g|_u\neq 0,u_i\in S\}$

若 $S$ 有限，则称 $F(S)$ 为 $F$ 上的**有限生成**扩张.

***Proof.*** 首先 $RHS$ 是域.

最小 $\Longrightarrow$ $F(S)\subseteq RHS$ ；

$RHS$ 是域， $F\subseteq RHS$ ， $S\subseteq RHS$ ，故 $F(S)\subseteq RHS$. $\blacksquare$

***Corollary 3.*** 如果 $\alpha\in F(S)$ ，存在有限子集 $S_0\subseteq S$ ，使得 $\alpha\in F(S_0)$.

***Lemma 4.*** $F(S_1\cup S_2)=F(S_1)(S_2)=F(S_2)(S_1)$.

***Proof.*** $F(S_1\cup S_2)$ 是 包含 $F$ 和 $S_1\cup S_2$ 的最小域，故 $F(S_1\cup S_2)\subseteq F(S_1)(S_2)$.

$F(S_1)(S_2)$ 是包含 $F(S_1)$ 和 $S_2$ 的最小域，故 $F(S_1)(S_2)\subseteq F(S_1\cup S_2)$. $\blacksquare$

***Corollary 3*** 和 ***Lemma 4*** 说明，域扩张的构造是可交换的， 而且可以通过有限次的构造得到（?）. 总之，域扩张可归结为单扩张.

## 单扩域

$K/F$ 中至少有一个元素是超越的，则称 $K/F$ 是**超越扩域**. 否则为**代数扩域**. 例如，域 $F$ 上的有理函数域 $F(x)=\{\frac{f}{g}:f,g\in F[x],g\neq 0\}$ 是超越扩域（不存在 $f$ 使得 $f(x)=0$ ）.

A fact: $\text{frac}(F[x])=F(x)$ where $F[x]$ is an integral domain for every field $F$. Note that $x$ here is merely a symbol.

Similarly we have for $u\in K/F$, $\text{frac}(F[u])=F(u)$.

***Theorem 5.*** $u\in K/F$, $F(u)=\{f(u):f\in F[x]\}$

- $u$ is algebraic with minimal poly $f(x)\in F[x]$, $\deg f=n$, then $F(u)\cong F[x]/(f)$, $[F(u):F]=n$, and $F(u)=F[u]$;

- $u$ is transcendental. Then $F(u)\cong F(x)$.

***Sketch of Proof.*** Consider ring homomorphism $\pi:F[x]\mapsto F(u)$ with $\pi(g(x))=g(u)$. With isomorphism thm we have $F(u)\cong F[x]/\text{Im}\;\pi$.

***Corollary 6.*** $u,v\in K/F$ are algebraic on $F$. There exists $\sigma:F(u)\cong F(v)$ where $\sigma(u)=v$, $\sigma|_F=\mathbf{Id}$ if and only if $u$ and $v$ share the same minimal polynomial.

***Corollary 7.*** $u,v\in K/F$ are transcendental on $F$. There exists $\sigma:F(u)\cong F(v)$ where $\sigma(u)=v$, $\sigma|_F=\mathbf{Id}$.

## 正规扩域

***Definition*** $K/F$ 是**正规扩域**，如果对于每一个 $f\in F[x]$ ， $f(u)=0,u\in K$, 那么 $f$ 的所有零点都在 $K$ 中.

正规： $\mathbb{Q}[\sqrt{2}],\mathbb{Q}[i]$

非正规： $\mathbb{Q}[\sqrt[3]{2}]$

考虑 $x^3-1$, 根为 $1,\zeta,\zeta^2$

$\mathbb{C}$ 是其任意子域的正规扩域.

## 应用：尺规作图

(0,0) 和 (0,1) 是可做出的；

已作出两点 $p_0,p_1$, 那么 直线 $p_0p_1$ 、以 $p_0$ 为圆心 经过 $p_1$ 的圆是可做出的；

直线和直线、圆和圆、圆和直线的交点是可做出的.

每一次圆和直线（或圆和圆）相交，在域 $\mathbb{Q}$ 中添加了 $\sqrt{\Delta}$.

则如果 $p$ 可做出，那么 $p$ 的坐标是 $\mathbb{K}$ 的元素，其中 $[K:\mathbb{Q}]=2^r$.

***Corollary.*** 正n边形是可做出的当且仅当 $\varphi(n)$ 是2的次方幂.

***Proof.***

$``\to"$

$[\mathbb{Q}(\omega_n):\mathbb{Q}]=[\mathbb{Q}(\omega_n):\mathbb{Q}(cos\frac{2\pi}{n})][\mathbb{Q}(cos\frac{2\pi}{n}):\mathbb{Q}]$

$\omega_n=e^{\frac{2\pi i}{n}}$ 是方程 $x^2-2cos\frac{2\pi}{n}x+1=0$ 的根，故 $[\mathbb{Q}(\omega_n):\mathbb{Q}(cos\frac{2\pi}{n})]=2$.

若正n边形可做出，则 $[\mathbb{Q}(cos\frac{2\pi}{n}):\mathbb{Q}]$ 是2的次方幂，那么 $[\mathbb{Q}(\omega_n):\mathbb{Q}]$ 也是2的次方幂. 已知 $\omega_n$ 是方程 $x^n-1=0$ 的根，下面求 $[\mathbb{Q}(\omega_n):\mathbb{Q}]$.

分圆多项式 $\Phi_n(x)=\prod_{\text{gcd}(k,n)=1}(x-e^{\frac{2k\pi i}{n}})$ 是 $\omega_n$ 的极小多项式，故 $[\mathbb{Q}(\omega_n):\mathbb{Q}]=\deg\Phi_n(x)=\varphi(n)$.

***Do not eat a fat man at one time***

---
