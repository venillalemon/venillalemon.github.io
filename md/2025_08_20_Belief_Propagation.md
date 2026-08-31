# Belief Propagation

*August 20, 2025*

一个图模型包含 $N$ 个随机变量 $\underline{x}=(x_1,\dots,x_N)$ ，从有限字母表 $\mathcal{X}$ 中取值. 需要解决一些问题，例如：

- 给定一些条件，求另一些变量的边缘分布；

- 一些后验估计相关

但是我们不会去直接计算联合分布 $p(\underline{x})$ ，因为它的状态空间是指数级别 $|\mathcal{X}|^N$ 个取值. BP 将这个问题转化为局部计算，利用图的稀疏性/特殊结构来避免指数级别的计算.

## Example 1: Ising chain

Ferromagnetic Ising model has $\underline{\sigma}=(\sigma_1,\dots, \sigma_N), \sigma_i\in\{1,-1\}$ with joint distribution

$$
\mu_\beta(\underline{\sigma}) = \frac{1}{Z} \exp\left(\beta \sum_{i=1}^{N-1} \sigma_i \sigma_{i+1}+\beta B\sum_{i=1}^N\sigma_i\right)
$$

where $Z$ is the partition function.

我们计算 $\sigma_j$ 的 marginal distribution, 这里用 $\propto$ 来省略归一化因子:

$$
\mu(\sigma_j)\propto\sum_{\sigma_1,\dots,\sigma_{j-1},\sigma_{j+1},\dots,\sigma_{N}}\exp\left(\beta \sum_{i=1}^{N-1} \sigma_i \sigma_{i+1}+\beta B\sum_{i=1}^N\sigma_i\right)
\\=\sum_{\sigma_1,\dots,\sigma_{j-1},\sigma_{j+1},\dots,\sigma_{N}}\exp\left(\beta \sum_{i=1}^{j-1} \sigma_i \sigma_{i+1}+\beta B\sum_{i=1}^{j-1}\sigma_i\right)\exp\left(\beta\sum_{i=j}^{N-1} \sigma_i \sigma_{i+1}+\beta B\sum_{i=j+1}^{N}\sigma_i\right)\exp\left(\beta B\sigma_{j}\right)
$$

分配拆开即可，是两个和的乘积. 定义 "message":

$$
\begin{aligned} \widehat\nu_{\to j}(\sigma_j) &= \frac{1}{Z_{\to j}} \sum_{\sigma_1\dots\sigma_{j-1}} \exp\left\{\beta \sum_{i=1}^{j-1}\sigma_i\sigma_{i+1} + \beta B \sum_{i=1}^{j-1}\sigma_i\right\}, \\[4pt] \widehat\nu_{j\leftarrow}(\sigma_j) &= \frac{1}{Z_{j\leftarrow}} \sum_{\sigma_{j+1}\dots\sigma_N} \exp\left\{\beta \sum_{i=j}^{N-1}\sigma_i\sigma_{i+1} + \beta B \sum_{i=j+1}^{N}\sigma_i\right\}. \end{aligned}
$$

$$
\mu(\sigma_j) \;\cong\; \widehat\nu_{\to j}(\sigma_j)\, e^{\beta B\sigma_j}\, \widehat\nu_{j\leftarrow}(\sigma_j).
$$

> This decomposition is interesting because the various messages can be computed iteratively.

而这两个部分都是 local 信息，左边的求和和右边无关. 例如 $\hat{\nu}_{\to1}(\sigma_1)$ 和 $\hat{\nu}_{\leftarrow n}(\sigma_n)$ 就是均匀二项分布. 这样就可以递推求出各个分布了.

$$
\hat{\nu}_{\to i}(\sigma_i)
\propto \sum_{\sigma_{i-1}} \hat{\nu}_{\to(i-1)}(\sigma_{i-1})
\exp\!\left(\beta \, \sigma_{i-1}\sigma_i +\beta B \sigma_{i-1}\right)
$$

$$
\hat{\nu}_{\leftarrow i}(\sigma_i)
\propto \sum_{\sigma_{i+1}} \hat{\nu}_{\leftarrow(i+1)}(\sigma_{i+1})
\exp\!\left(\beta \, \sigma_{i}\sigma_{i+1} +\beta B \sigma_{i+1}\right)
$$

## Example 2. a tree-parity-check code

We start from a concrete example.

$$
x_0 \oplus x_1 \oplus x_2 = \mathsf{0},
$$

$$
x_0 \oplus x_3 \oplus x_4 = \mathsf{0},
$$

$$
x_0 \oplus x_5 \oplus x_6 = \mathsf{0}.
$$

![Fig. 14.2 — Left: a simple parity check code with 7 variables and 3 checks. Right: the factor graph corresponding to the problem of finding the sent codeword, given a received message.](/images/BP/fig-14-2-parity-check-factor-graph.png)

*Fig. 14.2 — Left: a simple parity check code with 7 variables and 3 checks. Right: the factor graph corresponding to the problem of finding the sent codeword, given a received message.*

左图是这个方程组的 factor graph.

已知纠错矩阵，将一个 $x$ 通过 BSC($p$) 信道传输（每一 bit 以 $p$ 的概率翻转），接收方得到 $y$. 考虑 distribution conditioned on $y$ ，令 $Q(i|i)=1-p,Q(i|j)=p,\forall\;i\neq j$.

$$
\mu_y(\underline{x}) \;\cong\; \mathbb{I}(x_0\oplus x_1\oplus x_2 = \mathsf{0})\, \mathbb{I}(x_0\oplus x_3\oplus x_4 = \mathsf{0})\, \mathbb{I}(x_0\oplus x_5\oplus x_6 = \mathsf{0}) \prod_{i=0}^{6} Q(y_i \mid x_i),
$$

我们可以逐 bit 分析，需要在给定 $y$ 的情况下计算每个 $x_i$ 的 marginal distribution. 假设 $y=(1000010)$.

$$
\mu(x_1)\propto\sum_{x_0x_2,\dots,x_6}
\mathbb{I}(x_{0} \oplus x_{1} \oplus x_{2} = 0)\,
\mathbb{I}(x_{0} \oplus x_{3} \oplus x_{4} = 0)\,
\mathbb{I}(x_{0} \oplus x_{5} \oplus x_{6} = 0)\,
\prod_{i=0}^{6} Q(y_i | x_i) \,\\
=\sum_{x_0,x_2}\mathbb{I}(x_{0} \oplus x_{1} \oplus x_{2} = 0)Q(y_0|x_0)Q(y_2|x_2)\\\times
\sum_{x_3,x_4}\mathbb{I}(x_{0} \oplus x_{3} \oplus x_{4} = 0)Q(y_3|x_3)Q(y_4|x_4)\\\times
\sum_{x_5,x_6}\mathbb{I}(x_{0} \oplus x_{5} \oplus x_{6} = 0)Q(y_5|x_5)Q(y_6|x_6)\\\times
Q(y_1 | x_1) \, \\
= Q(y_1|x_1) \sum_{x_0,x_2}\mathbb{I}(x_{0} \oplus x_{1} \oplus x_{2} = 0)Q(y_0|x_0)Q(y_2|x_2)\hat{\nu}_{b\to0}(x_0)\hat{\nu}_{c\to0}(x_0)
$$

$$
\mu(x_0)\propto\sum_{x_1,\dots,x_6}
\mathbb{I}(x_{0} \oplus x_{1} \oplus x_{2} = 0)\,
\mathbb{I}(x_{0} \oplus x_{3} \oplus x_{4} = 0)\,
\mathbb{I}(x_{0} \oplus x_{5} \oplus x_{6} = 0)\,
\prod_{i=0}^{6} Q(y_i | x_i) \, \\
=\sum_{x_1,x_2}\mathbb{I}(x_{0} \oplus x_{1} \oplus x_{2} = 0)Q(y_1|x_1)Q(y_2|x_2)\\\times
\sum_{x_3,x_4}\mathbb{I}(x_{0} \oplus x_{3} \oplus x_{4} = 0)Q(y_3|x_3)Q(y_4|x_4)\\\times
\sum_{x_5,x_6}\mathbb{I}(x_{0} \oplus x_{5} \oplus x_{6} = 0)Q(y_5|x_5)Q(y_6|x_6)\\\times
Q(y_0 | x_0) \,
$$

乘积的第一项，就是指 $x_0$ 在 $\{0,a,1,2\}$ 子图中的 marginal distribution, 它和其他节点无关. 可以引入 $\hat{\nu}_{a\to0}(x_0)\propto\sum_{x_1,x_2}\mathbb{I}(x_{0} \oplus x_{1} \oplus x_{2} = 0)Q(y_1|x_1)Q(y_2|x_2)$ 等等，得到

$$
\mu(x_1)\propto Q(y_1|x_1)\hat{\nu}_{a\to1}(x_1)
$$

$$
\mu(x_0)\propto Q(y_0|x_0)\hat{\nu}_{a\to0}(x_0)\hat{\nu}_{b\to0}(x_0)\hat{\nu}_{c\to0}(x_0)
$$

## Belief Propagation on Trees

In this section,

$$
\mu(\underline{x})=\frac{1}{Z}\psi_a(\underline{x}_{\partial a})
$$

where $\psi_a$ has input in $\{x_i:i\in\partial a\}$, i.e. the neighborhood of $a$. Similar sets are defined for notation $\partial i$.

When the factor graph has no loop the following are among the basic problems that can be solved efficiently with a message-passing procedure:

1. Compute the marginal distributions of one variable, $\mu(x_i)$, or the joint distribution of a small number of variables.

2. Sample from $\mu(\underline{x})$, i.e. draw independent random configurations $\underline{x}$ with distribution $\mu(\underline{x})$.

3. Compute the partition function $Z$, or equivalently, in statistical physics language, the free-entropy $\log Z$.

We have BP rules:

$$
\nu_{j \to a}(x_j) \;\cong\; \prod_{b \in \partial j \setminus a}
\hat{\nu}_{b \to j}(x_j)\\
\hat{\nu}_{a \to j}(x_j) \;\cong\;
\sum_{\underline{x}_{\partial a \setminus j}}
\psi_a(\underline{x}_{\partial a}) \prod_{k \in \partial a \setminus j}
\nu_{k \to a}(x_k).
$$

Simple computation is able to show that the example of parity check code is consistent with the equations above.

If $j$ has only $1$ neighbor $a$, then $\nu_{j \to a}(x_j)\propto1$, thus uniform.

Let us verify $\hat{\nu}_{a\to0}(x_0)\propto\sum_{x_1,x_2}\mathbb{I}(x_{0} \oplus x_{1} \oplus x_{2} = 0)Q(y_1|x_1)Q(y_2|x_2)$:

$\text{LHS}=\sum_{x_1,x_2}\mathbb{I}(x_{0} \oplus x_{1} \oplus x_{2} = 0)Q(y_1|x_1)Q(y_2|x_2)\prod_{k=1,2}\nu_{k\to a}(x_k)$

A graph: and a clarifying [lecnote](https://mlg.eng.cam.ac.uk/teaching/4f13/1415/lect0809.pdf):

![Fig. 14.3 — Left: portion of the factor graph involved in the computation of $\nu^{(t+1)}_{j\to a}(x_j)$; this message is a function of the incoming messages $\widehat\nu^{(t)}_{b\to j}(x_j)$, with $b \ne a$. Right: portion involved in the computation of $\widehat\nu^{(t)}_{a\to j}(x_j)$; a function of the incoming messages $\nu^{(t)}_{k\to a}(x_k)$, with $k \ne j$.](/images/BP/fig-14-3-message-passing.png)

*Fig. 14.3 — Left: portion of the factor graph involved in the computation of $\nu^{(t+1)}_{j\to a}(x_j)$; this message is a function of the incoming messages $\widehat\nu^{(t)}_{b\to j}(x_j)$, with $b \ne a$. Right: portion involved in the computation of $\widehat\nu^{(t)}_{a\to j}(x_j)$; a function of the incoming messages $\nu^{(t)}_{k\to a}(x_k)$, with $k \ne j$.*

![Factor graph marginalisation, worked through on one example — the braces tie each bracketed sum to the message it defines. Complexity drops from $\mathcal{O}(K^5)$ to $\mathcal{O}(K^2)$. (Rasmussen and Ghahramani, *Message passing on Factor Graphs*.)](/images/BP/factor-graph-marginalisation.png)

*Factor graph marginalisation, worked through on one example — the braces tie each bracketed sum to the message it defines. Complexity drops from $\mathcal{O}(K^5)$ to $\mathcal{O}(K^2)$. (Rasmussen and Ghahramani, *Message passing on Factor Graphs*.)*

实际上，以上的 BP 应该按照迭代的方式理解.

$$
\nu^{(t+1)}_{j\to a}(x_j) \cong \prod_{b\in\partial j\setminus a} \widehat\nu^{(t)}_{b\to j}(x_j), \tag{14.14}
$$

$$
\widehat\nu^{(t)}_{a\to j}(x_j) \cong \sum_{\underline{x}_{\partial a\setminus j}} \psi_a(\underline{x}_{\partial a}) \prod_{k\in\partial a\setminus j} \nu^{(t)}_{k\to a}(x_k). \tag{14.15}
$$

这个有点像 Bellmann-ford, 明明我们要对整体进行分析（比如计算边缘分布）但是我们可以对局部（也就是每一条边）进行迭代得到结果.

We have converging theorem:

Theorem 14.1 — BP is exact on trees

Consider a tree-graphical model with diameter $t_*$ (which means that $t_*$ is the maximum distance between any two variable nodes). Then

1. Irrespective of the initial condition, the BP update (14.14), (14.15) converges after at most $t_*$ iterations. In other words, for any edge $(ia)$, and any $t > t_*$,
   $$
   \nu^{(t)}_{i\to a} = \nu^{*}_{i\to a}, \qquad \widehat\nu^{(t)}_{a\to i} = \widehat\nu^{*}_{a\to i}.
   $$

2. The fixed point messages provide the exact marginals: for any variable node $i$, and any $t > t_*$, $\nu^{(t)}_i(x_i) = \mu(x_i)$.

## Correlations and Energy

现在我们更进一步，想要计算某两个变量的联合边缘分布 $\mu_{ij}(x_i,x_j)$. 因为我们可以计算 $\mu(x_i)$, 只需计算 $\mathbb{P}_{\underline{x}\sim\mu}(\underline{x}_j=x_j|\underline{x}_i=x_i)$ 即可. (注意这里稍微有点符号混用，你可以将 $\underline{x}$ 看成一个随机变量). 可以定义

$$
\mu(\underline{x}|x_i=b)\propto\prod_{a=1}^M\psi(\underline{x}_{\partial a})\mathbb{I}(x_i=b).
$$

其实相当于加一条约束 $x_i=b$, 在 factor graph 中的体现为 $i$ 号节点挂出去了一个方块节点.

记 $F_R$ 是某个由方块节点构成的集合（也就是由约束节点构成）， $V_R=\partial F_R$ 是和 $F_R$ 相连的变量节点，其中 $R$ 代表诱导子图. 令 $\underline{x}_R$ 代表 $R$ 中变量构成的联合向量. 不妨设 $R$ 是连通图.

根据 message 的物理意义，可以计算 $\underline{x}_R$ 的边缘联合分布，它由内部因子 $\phi_a(a\in F_R)$ 和外部 message (相当于对子树代表的变量积分) 构成:

$$
\mu(\underline{x}_R)\propto\prod_{a\in F_R}\psi_a(\underline{x}_{\partial a})\prod_{a\in\partial R}\hat{\nu}_{a\to i(a)}(x_{i(a)})
$$

其中 $i(a)$ 表示 $a$ 在 $R$ 中的唯一邻居（如果有两个邻居就总会成环，可以对连通图 $R$ 证明这一点）.

### Internal Energy

In physics problems, the compatibility functions $\psi_a$ take the form $\psi_a(\underline{x}_{\partial a})=e^{-\beta E_a(\underline{x}_{\partial a})}$.

The internal Energy is defined to be the expectation of total energy among all possible configurations $\underline{x}$.

$$
U=\langle E\rangle=\sum_{\underline{x}}\mu(\underline{x})\sum_{a=1}^ME_a(\underline{x}_{\partial a})=-\frac{1}{\beta}\sum_{\underline{x}}\mu(\underline{x})\sum_{a=1}^M\log \psi_a(\underline{x}_{\partial a})
$$

Exchange the summing order, with fixed $a$ our aim is to compute

$$
\sum_{\underline{x}}\mu(\underline{x})\log\psi_a(\underline{x}_{\partial a})\\
=\sum_{\underline{x}_{\partial a}}\sum_{\underline{x}_{i\notin\partial a}}\mu(\underline{x})\log\psi_a(\underline{x}_{\partial a})\\
=\sum_{\underline{x}_{\partial a}}\mu(\underline{x}_{\partial a})\log\psi_a(\underline{x}_{\partial a})
$$

这里我们要算 $\mu(\underline{x}_{\partial a})$, 相当于在上一节中我们取 $F_R=\{a\}$, 得到最终结果

$$
U=-\sum_{a=1}^M\frac{1}{Z_a}\sum_{\underline{x}_{\partial a}}\left(\psi_a(\underline{x}_{\partial a})\log\psi_a(\underline{x}_{\partial a})\prod_{i\in\partial a}\nu_{i\to a}(x_i)\right)
$$

### Entropy

First, a surprising Thm:

Theorem 14.2

In a tree graphical model, the joint probability distribution $\mu(\underline{x})$ of all the variables can be written in terms of the marginals $\mu_a(\underline{x}_{\partial a})$ and $\mu_i(x_i)$ as:

$$
\mu(\underline{x}) = \prod_{a\in F} \mu_a(\underline{x}_{\partial a}) \prod_{i\in V} \mu_i(x_i)^{\,1-|\partial i|}.
$$

这样一来就可以算 $H(\underline{x})=\langle\log\mu(\underline{x})\rangle_\mu$ 了.

$$
H[\mu] = -\sum_{a\in F} \mu_a(\underline{x}_{\partial a}) \log \mu_a(\underline{x}_{\partial a}) - \sum_{i\in V} \big(1-|\partial i|\big)\, \mu_i(x_i) \log \mu_i(x_i).
$$

有自由熵 $\Phi=H-U$.（第一眼量纲不对；在热统中，有定义 Helmholtz 自由能 $F=U-TS$ ，实际上这个差了一个负号和一些因数： $\Phi=-\beta F=\frac{S}{k_B}-\beta U=H-\beta U$, 用 $\beta=1$ 简化）.

It is also easy to express the free-entropy $\Phi = \log Z$ in terms of *local* quantities. Recalling that $\Phi = H[\mu] - U[\mu]$ (where $U[\mu]$ is the internal energy given by Eq. (14.21)) we get $\Phi = \mathbb{F}[\mu]$, where

$$
\mathbb{F}[\mu] = -\sum_{a\in F} \mu_a(\underline{x}_{\partial a}) \log\left\{\frac{\mu_a(\underline{x}_{\partial a})}{\psi_a(\underline{x}_{\partial a})}\right\} - \sum_{i\in V} (1-|\partial i|)\mu_i(x_i)\log\mu_i(x_i).
$$

Expressing local marginals in terms of messages, via Eq. (14.18), we can in turn write the free-entropy as a function of the fixed point messages. We shall introduce the function $\mathbb{F}_*(\underline{\nu})$, that yields the free-entropy in terms of $2|E|$ messages $\underline{\nu} = \{\nu_{i\to a}(\cdot), \widehat\nu_{a\to i}(\cdot)\}$:

$$
\mathbb{F}_*(\underline{\nu}) = \sum_{a\in F}\mathbb{F}_a(\underline{\nu}) + \sum_{i\in V}\mathbb{F}_i(\underline{\nu}) - \sum_{(ia)\in E}\mathbb{F}_{ia}(\underline{\nu}) \tag{14.27}
$$

where:

$$
\begin{aligned} \mathbb{F}_a(\underline{\nu}) &= \log\left[\sum_{\underline{x}_{\partial a}} \psi_a(\underline{x}_{\partial a}) \prod_{i\in\partial a} \nu_{i\to a}(x_i)\right], & \mathbb{F}_i(\underline{\nu}) &= \log\left[\sum_{x_i} \prod_{b\in\partial i} \widehat\nu_{b\to i}(x_i)\right], \\[6pt] \mathbb{F}_{ai}(\underline{\nu}) &= \log\left[\sum_{x_i} \nu_{i\to a}(x_i) \widehat\nu_{a\to i}(x_i)\right]. & & \end{aligned}
$$

It is not hard to show that, evaluating this functional on the BP fixed point $\underline{\nu}^*$, one gets $\mathbb{F}_*(\underline{\nu}^*) = \mathbb{F}[\mu] = \Phi$, thus recovering the correct free-entropy. The function $\mathbb{F}_*(\underline{\nu})$ defined in (14.27) is known as the **Bethe free-entropy** (when multiplied by a factor $-1/\beta$, it is called the **Bethe free-energy**).

Theorem 14.3 — Bethe free-entropy is exact on trees

Consider a tree graphical model. Let $\{\mu_a,\mu_i\}$ denote its local marginals, and $\underline{\nu}^* = \{\nu^{*}_{i\to a}, \widehat\nu^{*}_{a\to i}\}$ be the fixed point BP messages. Then $\Phi = \log Z = \mathbb{F}[\mu] = \mathbb{F}_*(\underline{\nu}^*)$.

---

### 参考资料

- [1] [Information, Physics, and Computation](http://venillalemon.github.io/books/ipc.pdf). Marc Mézard, Andrea Montanari
