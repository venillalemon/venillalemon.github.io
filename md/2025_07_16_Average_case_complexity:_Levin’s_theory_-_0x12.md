# Average case complexity: Levin’s theory - 0x12

*July 16, 2025*

$\mathbf{NP}$ 是用最坏复杂性定义的：一个语言 $L\in\{0,1\}^*$, 如果存在一个 NTM, 能在多项式时间内运行完毕，**接受**任意 YES instance 并拒绝所有 NO instance, 那么称 $L$ 是 $\mathbf{NP}$ 语言. 注意我们对 NO instance 也有多项式时间的要求.

实际中我们有时候不关心最坏情况，而关心平均情况.

## Distributional Problems

**例1.** $CLIQUE=\{\langle G,k\rangle:\exists K_k\subset G\}$ 是一个 $\mathbf{NP}$ -complete 问题，可用 $3SAT$ 或者 $VERTEXCOVER$ 归约.

> 复习一下 $CLIQUE$ 难于 $VERTEXCOVER$:
>
> **Pf.** 给定一个 instance $\langle G,k\rangle$, 目标输出 $G$ 是否有大小为 $k$ 的顶点覆盖.
>
> 如果 $G$ 有一个大小为 $k$ 的 vertex cover, 那么这个顶点集的补集一定是独立集（否则一定有边没有被覆盖到）. 反之某个独立集补集的诱导子图也一定是顶点覆盖.
>
> 所以直接把 $\langle\overline{G},n-k\rangle$ 喂给 oracle 即可.

一个直接的问题是对于一个随机图 $\mathcal{G}_{n,\frac{1}{2}}$, 给定 $k(n)$, 询问是否有这样大小的团. [Erdös](http://venillalemon.github.io/articles/cliques_in_random_graphs.pdf) 说随机图中, 极大团的大小大概率是 $2\log{n}$ 左右，也可以参考这篇 [lecnote](http://venillalemon.github.io/articles/Largest_Clique_in_a_Random_Graph.pdf).

> **例2.** $3SAT$ 问题.

> **例3.** $LPN$ 问题.

以上启发我们定义平均复杂性的 $\mathbf{distP}$: 称一个语言和分布的组合 $\langle L,\mathcal{D}=\{D_1,D_2,\dots\}\rangle$ 属于 $\mathbf{distP}$ ，当且仅当存在算法 $A$ 和多项式 $p$ 使得对于任意 $n$ ，输入 $x$ 满足 $D_n$ 分布下，时间的期望不大于 $p(n)$.

其中 $D_n$ 是 $\{0,1\}^n$ 上的某个分布.

> Recall. 图灵机衡量时间复杂度的时候，必须有前提，即无论输入是什么（包括不合法输入，简而言之输入集合就是 $\{0,1\}^n$ ），图灵机一定 halt.

这样定义时间的期望固然合理，然而我们考虑这个定义在多项式复合下的封闭性；为何要考虑多项式复合？因为不同的图灵机模型之间一般只差一个多项式，例如 $t(n)$ 的多纸带 TM 都有一个 $t^2(n)$ 的单纸带 TM.

假设一个图灵机，在全 $0$ 输入上运行 $2^n$ 步，其他运行 $n$ 步. 这样一来虽然原始的时间期望是 $O(n)$, 但是平方之后就变成了 $2^{-n}2^{2n}+n^2=O(2^n)$. 这不好!

![](https://notes.sjtu.edu.cn/uploads/upload_98e443b014cb014dc31b7089daee1855.png)

![](https://notes.sjtu.edu.cn/uploads/upload_28ef21bb02beac15e8b7a2ce2b40022d.png)![](https://notes.sjtu.edu.cn/uploads/upload_284e99bed37aa91861f1603cee566a99.png)

(实际上 18.4 中的分母 $n$ 可以提出来放在 $C$ 的右边)

$\mathbf{distNP}$ 相当于为 $\mathbf{NP}$ 中的每个语言添加了一种结构，这个结构涉及到字符串集合上的某一个分布.

**Q:** 我们可以认为 $\mathcal{D}$ 和语言无关：这样一来 $\mathbf{distNP}$ 和 $\mathbf{NP}\times\{\mathcal{D}:\mathcal{D}\text{ is }\mathbf{P}\text{-computable}\}$ 有一一对应？这样一来 $\mathbf{distNP}$ 只是 $\mathbf{NP}$ 套了一层皮？或许之后的研究会带给我答案，略过.

## Average-case Reduction

**Def.** We say $\langle L,\mathcal{D}\rangle\leq_p\langle L^\prime,\mathcal{D}^\prime\rangle$, if and only if there is a polynomial-time computable function $f$ and polynomials $p,q:\mathbb{N}\mapsto\mathbb{N}$, such that

- **Correctness**: $\forall x\in\{0,1\}^*,x\in L\iff f(x)\in L^\prime$;

- **Length Regularity**: $\forall x\in\{0,1\}^n,|f(x)|=p(n)$;

- **Domination**: $\forall n\in\mathbb{N},y\in\{0,1\}^{p(n)},$ $\mathbb{P}_{X\sim D_n}[f(X)=y]\leq q(n)\mathbb{P}_{X\sim \mathcal{D}^\prime_{p(n)}}[X=y]$.

---

### 参考材料

- [1] Sanjeev Arora and Boaz Barak. [Computational Complexity: A Modern Approach](http://venillalemon.github.io/books/ccama.pdf). Cambridge University Press, USA, 1st edition, 2009.
