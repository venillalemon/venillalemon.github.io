# Properties of LLL Basis

*July 9, 2025*

题目摘自 [Regev Hw2](https://cims.nyu.edu/~regev/teaching/lattices_fall_2009/homework2.pdf) 的第 $4$ 题.![hw2](https://notes.sjtu.edu.cn/uploads/upload_cac5b034c9d247058da163c0fc127825.png)

首先回顾 $\delta$ -LLL reduced basis 的定义 ($\frac{1}{4}\leq\delta\leq1$)

**Def.** For linearly independent basis $b_1,\dots, b_n\in\mathbb{R}^n$, we have for all $1\leq j\lt i\leq n$, $\mu_{i,j}=\frac{\langle b_i,\tilde{b_j}\rangle}{\langle\tilde{b_j},\tilde{b_j}\rangle}$, and **Gram-Schmidt orthogonalization** $\tilde{b_i}=b_i-\sum_{j=1}^{i-1}\mu_{i,j}\tilde{b_j}$. Such a basis $B=\{b_1,\dots,b_n\}$ is a ** $\delta$ -LLL reduced basis** if the following holds:

- **Size Reduction** For all $1 \leq j \lt i \leq n$, $|\mu_{i,j}| \leq \frac{1}{2}$.

- **Lovász Condition** For all $1 \leq i \leq n$, $\delta \|\tilde{b_{i}}\|^2 \leq \|\tilde{b_{i+1}} + \mu_{i+1,i} \tilde{b_i}\|^2$

事实上所有 $\tilde{b_i}$ 两两正交，上述两个条件可以推导出对于所有的 $1 \leq j \lt i \leq n$,

$$
2^{\frac{i}{2}}\|\tilde{b_{i}}\| \leq 2^{\frac{j}{2}}\|\tilde{b_{j}}\|.
$$

### **Property 1.** $\|b_1\|\leq2^{\frac{n-1}{4}}\det^{\frac{1}{n}}\Lambda$

**Pf.** 对于每个 $i$, $2^{\frac{1}{2}}\|\tilde{b_{1}}\| \leq 2^{\frac{i}{2}}\|\tilde{b_{i}}\|$, 再应用 $b_1=\tilde{b_1}$, 累乘即可.

### **Property 2.** For all $1\leq i\leq n,\;\|b_i\|\leq2^{\frac{i-1}{2}}\|\tilde{b_i}\|$

**Pf.** $\|b_i\|^2=\|\tilde{b_i}\|^2+\sum_{j=1}^{i-1}|\mu_{i,j}|^2\|\tilde{b_j}\|^2\leq\|\tilde{b_i}\|^2+\frac{1}{4}\sum_{j=1}^{i-1}2^{i-j}\|\tilde{b_i}\|^2\leq\frac{1+2^{i-1}}{2}\|\tilde{b_i}\|^2$.

做累乘即可得到 $\prod_{i=1}^n\|b_i\|\leq2^{\frac{n(n-1)}{4}}\det\Lambda$

*Orthogonality defect* which is used to determine how good is a lattice basis.

### **Property 3.** For all $1\leq i\leq j\leq n$, $\|b_i\|\leq2^{\frac{j-1}{2}}\|\tilde{b_j}\|$

**Pf.** $\|b_i\|\leq2^{\frac{i-1}{2}}\|\tilde{b_i}\|\leq2^{\frac{i-1}{2}}2^{\frac{j-i}{2}}\|\tilde{b_j}\|$.

### **Property 4.** For all $1\leq i\leq n$, $\lambda_i(\Lambda)\leq2^{\frac{i-1}{2}}\|\tilde{b_i}\|$

**Pf.** 根据 (d) 问，只要有一个 $k\leq i$ 满足 $\lambda_i(\Lambda)\leq \|b_k\|$ 即可.

假设不存在这样的 $k$, 那么对任意 $1\leq k\leq i$, $\lambda_i(\Lambda)\gt \|b_k\|$. 由于 $b_1,\dots,b_i$ 是线性独立的格中向量, $\dim(\text{span}(b_1,\dots,b_i))=i$ ，和 $\lambda_i(\Lambda)=\inf\{r:\dim(\text{span}(\Lambda\cap\overline{B}(0,r)))\geq i\}$ 矛盾.

### **Property 5.** For all $1\leq i\leq n$, $\lambda_i(\Lambda)\geq2^{-\frac{n-1}{2}}\|b_i\|$

**Pf.** 根据 (d) 问，对于任意 $j\geq i$, $\|b_i\|\leq2^{\frac{j-1}{2}}\|\tilde{b_j}\|\leq2^{\frac{n-1}{2}}\|\tilde{b_j}\|$. 因此只要证存在 $j\geq i$ 使得 $\lambda_i(\Lambda)\geq\|\tilde{b_j}\|$ 即可.

考虑格 $\Lambda_0=\{b_i,\dots,b_n\}$, 在 $V_0=\text{span}(b_i,\dots,b_n)$ 中进行 Gram-Schmidt 正交化得到 $b_i^*,\dots,b_n^*$.

我们有 $\lambda_1(\Lambda_0)\geq\min_{j\geq i}\|b_j^*\|$. 根据 Gram-Schmidt 性质， $\|b_i^*\|\geq\|\tilde{b_i}\|$, 因为后者减掉的多.

**<一个伪证>**考虑线性无关组 $v_1,\dots,v_i$, 其中 $\|v_i\|=\lambda_i(\Lambda)$, 由于 $\dim V_0=n-i+1$, **必有一个向量 $v_k$ 在 $\Lambda_0$ 中**(fake!)，因此 $\|\lambda_i(\Lambda)\|\geq\|\lambda_k(\Lambda)\|\geq\lambda_1(\Lambda_0)\geq\min_{j\geq i}\|b_j^*\|$.

目前还不知道怎么证, 但是 [Lecture 12](https://cims.nyu.edu/~regev/teaching/lattices_fall_2004/ln/averagecase.pdf) 会用到这个结论, 即

> the length of the longest vector in an LLL-reduced basis gives a $2^{\frac{n-1}{2}}$ approximation of $\lambda_n(\Lambda)$.

## update on 2025-08-17

这段时间看了 LLL 的原论文，里面就有写到关于 **Property 5** 的证明.

**Lem.** 给定格 $L\subset\mathbb{R}^n$ 上的约简基 $\{b_1,\dots,b_n\}$ 和线性无关组 $\{x_1,\dots,x_t\}\subset L$, 对任意 $1\leq j\leq t$, 有

$$
\|b_j\|^2\leq2^{n-1}\max\{\|x_1\|^2,\dots,\|x_t\|^2\}.
$$

**Pf.** 设 $x_j=\sum_{i=1}^{n} r_{ij} b_i$, $r_{ij}\in\mathbb{Z}$. 同时我们根据给定的约简基 $\{b_i\}$ 可以得到 Gram-Schimidt 基 $\{\tilde{b_i}\}$ ， 有 $x_j=\sum_{i=1}^n \tilde{r_{ij}} \tilde{b_i}$

对于每个 $j$, 定义 $i(j)$ 为满足 $r_{i(j)j}\neq 0$ 的最大的 $i$.

首先，由 $i(j)$ 的定义， $x_j=\sum_{k=1}^{i(j)} r_{kj}b_k=\sum_{k=1}^{i(j)} r_{kj}\big(\tilde{b_k}+\sum_{l=1}^{k-1}\mu_{k,l}\tilde{b_l}\big)$. 我们发现 $\tilde{b_{i(j)}}$ 的系数正好是 $r_{i(j)j}$, 而且 $\tilde{b_{pj}},p\gt i(j)$ 的系数都是 $0$. 由此 $\|x_j\|^2\geq|r_{i(j)j}|^2\|\tilde{b_{i(j)}}\|^2\geq\|\tilde{b_{i(j)}}\|^2$.

其次, 不妨设 $i(j)$ 随 $j$ 单调递增（只需要将 $x_j$ 重新排列即可）. 这样一来，如果存在 $j$ 使得 $j\gt i(j)$, 那么对于每个 $1\leq k\leq j$, $x_k\in\text{Span}\{b_1,\dots,b_{i(j)}\}$, 但是 $i(j)\lt j$, 和线性无关矛盾. 因此对于每个 $j$ 来说， $j\leq i(j)$.

应用 **Property 3**, 对于每一个 $1\leq j\leq t$, $\|b_j\|^2\leq2^{i(j)-1}\|\tilde{b_{i(j)}}\|^2\leq2^{n-1}\|x_j\|^2$.

注意这个 $x_j$ 是排序后的, 我们并不知道它原来是什么. 因此结论为

$$
\|b_j\|^2\leq2^{n-1}\max\{\|x_1\|^2,\dots,\|x_t\|^2\}.
$$

### **Property 5.** For all $1\leq i\leq n$, $\lambda_i(\Lambda)\geq2^{-\frac{n-1}{2}}\|b_i\|$

**Pf.** 设 successive minima 得到的基为 $\{v_1,\dots,v_n\}$, $\|v_i\|=\lambda_i$. 在 **Lem.** 中取 $t=i$ ，线性无关组为 $\{v_1,\dots,v_t\}$, 有 $\|b_i\|^2\leq2^{n-1}\max\{\|v_1\|^2,\dots,\|v_i\|^2\}=2^{n-1}\lambda_i^2$, 得证.

**Comment.** 由 **Property 4**, $\lambda_i(\Lambda)\leq2^{\frac{i-1}{2}}\|\tilde{b_i}\|\leq2^{\frac{i-1}{2}}\|{b_i}\|$. 因此

$$
2^{-\frac{i-1}{2}}\lambda_i(\Lambda)\leq\|b_i\|\leq2^{\frac{n-1}{2}}\lambda_i(\Lambda)
$$

---
