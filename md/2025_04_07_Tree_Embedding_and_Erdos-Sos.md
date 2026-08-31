# Tree Embedding and Erdos-Sos

*April 7, 2025*

*Lecture Notes for CS477 combinatorics on 2025/04/07*

### a combinatorial equality

$$
\sum_{r=0}^{50}(-1)^r{101\choose 51+r}{50+r\choose 50}=1
$$

寻找一种组合方法，其代数做法在 [Lecture 06]({{< relref "post/2025-03-24-turan.md" >}}) 中.

101选51+r打勾，最后一个画圈，前面50+r个分方块三角，有 ${101\choose 51+r}{50+r\choose 50}$ 种方法.

换顺序，先选50个三角+1个圈，按顺序；再在圈前面任意选r个方块，r奇数，那么是坏的，偶数是好的。按照圈的位置分，如果圈前面选完三角还有空，那么r奇偶抵消；否则好的比坏的多1.

$\sum_{r=0}^{50}(-1)^r{101\choose 51+r}{50+r\choose 50}=\sum_{k=51}^{101}\sum_{r=0}^{k-1-50}(-1)^r{k-1\choose 50}{k-1-50\choose r}$

### flipping a coin

$p\in(0,1)$ 均匀分布，求100次中50次成功的概率

传统：微积分

成功= $X(\omega)\lt p$, 因此这个概率等价为 rand 101 个数字，第一个数字排在第51位（or 任意位）的概率：1/101

### tree embedding

![](https://notes.sjtu.edu.cn/uploads/upload_a99c99411e1bbaf05fffbf3567c60c01.png)

> **Thm.** $\overline{d}(G)\geq 2k-2\Rightarrow$ 任意一个 $k+1$ 阶树是 $G$ 的子图.

> **Lemma.** $\overline{d}(G)\geq 2k-2$ 那么存在 $\delta(H)\geq k$ 的诱导子图.

$m\geq n(k-1)$, 每次去掉度数 $\leq k-1$ 的点和它的邻边, $m-d(v)\geq m-(k-1)\geq(n-1)(k-1)$. 去掉的过程中， $m\geq n(k-1)$ 一直保持. 停止的时候，没有度数 $\leq k-1$ 的点，因此 $\delta(G)\geq k$.

问题：k还能再大吗？假设k=51，要求一个 $\delta\geq52$ 的诱导子图

左到右足够多的点排成一行，每个点到左边51点、右边51点连边，可以expect它平均度数大于100. 但是最左边的点度数51，去掉；因此按照这个方法会被全部去掉。

或者考虑 $K_{51,N},N\gg 51,\overline{d}=2\times\frac{51N}{51+N}\geq100$, 因此一个 $\delta\geq 52$ 的诱导子图一定不包含右边 $N$ 个点. 左边剩51个点，更不可能.

> **Lemma.** $\delta(G)\geq k$, 那么任意一个 $k+1$ 阶树是 $G$ 的子图.

容易看到，一定存在k+1阶的星星图 or $P_{k+1}$. 树任选根，每个点由于存在至少 $k$ 个邻居，总是可以逐步拓展embedding. 如果挑到x，它的朋友都在已经选的集合中，那么已经完成.

> **Erdos-Sos Conjecture.** $\overline{d}(G)\geq k\Rightarrow$ 任意一个 $k+1$ 阶树是 $G$ 的子图.

除了有限个反例，基本正确.

### some hard problems in graph coloring

![](https://notes.sjtu.edu.cn/uploads/upload_9b2cc6d2bd448554d057ceabae374dd8.png)

前三个解答见 [Lecture 12]({{< relref "post/2025-04-28-probabilistic-method.md" >}})

$\chi\geq\omega+k$ 用 k 个 $C_5$

最后一个见 [girth](https://math.mit.edu/~fox/MAT307-lecture13.pdf)，概率方法证明，用到了 Markov 不等式和 alteration

### 一些基础不等式

$$
\omega\leq\chi\leq n
$$

$$
\frac{n}{\alpha}\leq\chi\leq\Delta+1
$$

右边：归纳法假设30个点以下都满足 $\chi\leq\Delta+1$, 剩下一个点度数至多 29.

左边：每种颜色是一个独立集（k独立集$\iff$k染色）， $n=\sum |D|\leq\sum\alpha=\chi\alpha$

问题：有没有图 $\chi\gg \frac{n}{\alpha}$ ？

第一反应： $K_n$ 的影子图， $n\gg \frac{2n}{n}$.

其实很容易做到， $K_n$ 再带上n个孤立点即可.

$\chi\ll\Delta+1$: star graph

$\chi=\Delta+1$: $K_n$, $C_{2k+1}$

奇妙的图 by xiaomin![](https://notes.sjtu.edu.cn/uploads/upload_4d3b1cd886eb17b06dcac1a3fdb72342.png)

### 定理 0407 系列

> **Thm 040701.** $\chi(G)=k$, 则 $G$ 至少有一个点 $\deg\geq k-1$.

总有人被逼着染 k 色.

> **Thm 040702.** $\chi(G)=100$, 则 $G$ 至少有 100 个点 $\deg\geq99$.

把度数 $\geq99$ 的点提到前面，如果有 $\lt 100$ 个这样的点，那么我可以拿着99种颜色，先给度数 $\geq 99$ 的点一人一个. 后面的点，因为度数 $\leq 98$, 用 99 个颜色一定可以染完, 得到 $\chi\leq99$, 矛盾.

归纳法：按照 $G$ 的阶数归纳，归纳起点是 $K_{100}$. 如果对任意 $|G|\lt n$ 成立，那么 $|G|=n,\chi(G)=100$ 时，若存在一个度数 $\deg v\leq98$, 那么 $\chi(G-v)=100$, $v$ 由于最多只看到98种颜色，它的染色不会影响 $G$ 的染色. 由归纳假设 $G-v$ 至少100个点 $\deg\geq k-1$.

> **Thm 040703'.** $\chi(G)=100$, $\phi$ 最优，则 $G$ 每种颜色都有一个点 $\deg\geq 99$.

> **Thm 040703.** $\chi(G)=100$, $\phi$ 最优，则 $G$ 每种颜色都有一个点和其他所有颜色相邻.

否则可以把这个颜色给分裂掉.

### 贪心染色

每次找最大独立集染色，并且去掉. 这个算法对应一种假设：

> **Conj.** $W\subseteq G$ 为最大独立集，则有一个最优染色使 $W$ 同色.

显然错误，考虑 $P_4$.

> **Conj.** 给定图 $G$, 存在最大独立集 $W\subseteq G$, 存在一个最优染色使 $W$ 同色.

$K_n$ 影子图

### 平面直线交点形成的图

![](https://notes.sjtu.edu.cn/uploads/upload_a0ab3b004a8522a59fe1ea777e94eaf8.png)

$\Delta=4\Rightarrow\chi\leq 5$

四色定理 $\Rightarrow\chi\leq4$ (大炮打蚊子)

> **Thm. (K. Wagner, 1936; I. Fáry, 1948; Sherman K. Stein, 1951, independently)** 任意一个简单平面图总可以用直线段画出来.

或者 Brooks Thm

> **Thm. (Brooks)** Connected graph in which every vertex has at most $\Delta$ neighbors, the vertices can be colored with only $\Delta$ colors, except for two cases, complete graphs and cycle graphs of odd length, which require $\Delta+1$ colors.

这启发我们，无脑染色时的“脑子”只需要保证每个点前面有足够少的邻居即可.

---
