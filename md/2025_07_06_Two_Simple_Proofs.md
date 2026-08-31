# Two Simple Proofs

*July 6, 2025*

两个简单的证明

首先有定义 $\mathrm{decCVP}=\{(B,t,r):\mathrm{dist}(t,\mathcal{L}(B))\leq r\}$. (btr: Bocchi the Rock)

**Prob1.** Decisional $\mathrm{decCVP}$ is $\mathbf{NP}$ -complete.

**Pf.** NP 类的证明比较显然，因为给一个距离小于 $r$ 的格中向量即可, 且这个向量能用多项式长度的字符串描述（其长度小于 $||t||+r$ ）.

NP-hard: 考虑归约 $\mathrm{decCVP}\geq_m \mathrm{SUBSETSUM}$. 给定 $\{a_1,a_2,\dots,a_n\},S$ ，构造格基 $v_1=(a_1,2,0,\dots),\dots,v_i=(a_i,0,\dots,2,\dots)$. 相当于 $B$ 的最上面一行是 $a_i$, 下面是 $2I$. $t=(S,1,\dots,1)$, $r=\sqrt{n}$ 即可，考虑到 $n$ 可能不是完全平方数，直接把缺少的补 $0$ 即可.

**Prob2.** For full rank lattice $\Lambda$, $\lambda_1(\Lambda)\lambda_n(\Lambda^*)\geq 1$.

**Pf.** 注意到 $\lambda_n\geq\lambda_i$, 只需找到一个 $i$ 满足即可. 设 $||v||=\lambda_1(\Lambda)$, 对于对偶格中每一个向量 $x$ ，都有 $\langle x,v\rangle\in\mathbb{Z}$. 我们选取 $x_1,\dots,x_n$ 使得 $||x_i||=\lambda_i(\Lambda^*)$, 那么由于满秩，不可能每个都和 $v$ 垂直，因此存在 $i$, $\langle x_i,v\rangle\geq1$, 因此， $\lambda_1(\Lambda)\lambda_n(\Lambda^*)\geq||x_n||·||v||\geq\langle x_i,v\rangle\geq 1$

---
