# Reduction & Diagonal Method - 0x03

*July 14, 2025*

~~之前[计算理论]({{< relref "post/2025-01-14-computation-theory.md" >}})的坑还没填完..~~ 但是后面很多内容都在这本复杂性里面，于是先看这个了

Hierarchy, Diagonalization (and its limitations), Circuit Complexity forms the Chapter 9 **INTRACTABILITY** in [Sipser's book](http://venillalemon.github.io/books/itc.pdf)🤣

先挂一张 reduction graph![](https://notes.sjtu.edu.cn/uploads/upload_941446c9dcb2961c3d5d1a140391beea.png)

首先将判定问题扩展到搜索问题.

回顾我们是怎么证 $SAT$ 为 $\mathbf{NP}$ -hard 的, 是假设给到了任意一个 $\mathbf{NP}$ 语言, 根据这个语言造一个逻辑表达式. 由于 $L$ 是 $\mathbf{NP}$ 的，一定存在确定性图灵机 $M$ ，使得 $x\in L\iff\exists u\in\{0,1\}^{\text{poly}(x)},\;M(x,u)=1$. 我们构造一个逻辑表达式，它描述了图灵机 $M$ 每一步的状态直到接受，所需满足的条件. （有一个细节，我们需要根据原来的图灵机构造一个 $2$ 纸带图灵机，有一条是只读带，而且图灵机的指针移动和输入内容无关，只和输入长度有关，这样的图灵机称为 **Oblivious TM**）. 这样一来，逻辑表达式只需要描述 $4$ 个条件：

- 输入的前 $n$ 位等于 $x$

- 初始状态

- 对于每一个时间步，符合图灵机运行规则

- 结束状态，在接受态停机

这样的一个归约函数 $f$ 不仅满足 $x\in L\iff f(x)=1$, 而且将 $x$ 的一个 witness 转换成了逻辑表达式的一个赋值. 同时，由于这个逻辑公式完全符合图灵机的运行情况，一个使表达式为真的赋值也对应了一个 witness. 这样的归约称为 **Levin reduction**, 可被用于搜索问题上（搜索问题就是找到一个 witness）.

**Thm 1.** 如果 $\mathbf{P}=\mathbf{NP}$ ，那么对任意 $L\in\mathbf{NP}$, verifier $M$, 存在多项式时间的确定性图灵机 $B$, 对于任意输入 $x\in L$, $M(x,B(x))=1$.

**Pf.** 首先, 如果我们对 $L=SAT$ 证明了这个结论并得到 $B_{SAT}$ ，那么任何 $L\in\mathbf{NP}$, 对于一个 Levin 归约 $f$ ，将 $f(x)$ 作为输入给到 $B_{SAT}$ 得到一个赋值后，将赋值转化成一个 witness 即可. 下面证明对于 $SAT$ 上面的论断成立.

$B$ 如何构造？首先由于 $\mathbf{P}=\mathbf{NP}$, 存在多项式算法 $A$ 确定 $SAT$ 问题. 对于一个逻辑表达式 $\phi$ ， $B$ 先用 $A$ 确定 $\phi$ 是否可满足；然后假设第一个变量 $x_1=1$ ，得到 $\phi_1$. 我们知道如果 $\phi$ 可满足, 那么 $\phi[x_1=1]$ 和 $\phi[x_1=0]$ 必有一个可满足，因此跑一次 $A$ 就够了. 这样一来，运行时间为 $n\text{time}(A)$, 多项式；同时记录下每个赋值，就是计算出了一个 witness. $\blacksquare$

## $\mathbf{coNP}$

> **Def.** $\mathbf{coNP}=\{L:\overline{L}\in\mathbf{NP}\}$

即，存在一个确定性图灵机 $M$ 和多项式 $p$, 对任意 $x$,

$$
x\in L\iff\forall u\in\{0,1\}^{p(x)},\;M(x,u)=0.
$$

注意核心的区别不在于输出 $0$ 还是 $1$, 在于中间的量词是存在还是任意.

定义 $TAUTO=\{\phi:\;\vdash\phi\}$, 有

**Thm 2.** $TAUTO$ 是 $\mathbf{coNP}$ -complete 语言.

**Pf.** 首先对于 $\phi\not\in TAUTO$ 存在一个 witness 让 $\phi$ 的值为 false, 因此属于 $\mathbf{coNP}$.

下证所有 $L\in\mathbf{coNP}$ 比 $TAUTO$ 容易. 可以知道 $\overline{L}\in\mathbf{NP}$, 因此根据 Cook-Levin 定理的证明，存在多项式可计算的归约函数， $x\in\overline{L}\to f(x)$ 可满足， $x\in L\to f(x)$ 不可满足. 直接取 $\neg f(x)$ 就是 tautology.

## Diagonal Method

回顾一道妙题：

**Ex.** Prove that $TOT=\{x:x=\langle M\rangle,M\text{ halts on every input}\}$ is undecidable.

**Pf.** Soppose there exists a decider TM $R$. Construct a TM $T$ that operates on input $x$: run $R$ on input $x$, if $R$ rejects, halt; if $R$ accepts, simulate $M$ on input $x$ where $x=\langle M\rangle$.

For all possible input $x$, if $x=\langle M\rangle\in TOT$, then $M$ halts and $T$ halts; if not, $R$ rejects and $T$ also halts. Thus $\langle T\rangle\in TOT$.

However, consider $T(\langle T\rangle)$. Since $\langle T\rangle\in TOT$, $T$ will simulate $T$ on input $\langle T\rangle$ recursively and without terminating, a contradiction.

**Thm 3.** (Deterministic time hierarchy thm) If $f,g$ are time-constructible functions that $f(n)\log{f(n)}=o(g(n))$, then $\mathbf{DTIME}(f(n))\subsetneq\mathbf{DTIME}(g(n))$.

**Pf.** For simplicity we relax the condition to $f(n)=n,g(n)=n^{1+\epsilon}$ for all $\epsilon$.

**Goal**: find a language that can be decided in $O(g(n))$ time but never in $O(f(n))$ time.

![](https://notes.sjtu.edu.cn/uploads/upload_d387ebb5b21e089da868c4fe73206948.png)

A Turing Machine $D$ operates like this: on input $x$, run the universal TM $\mathcal{U}$ for $|x|^{1+\epsilon}$ steps, simulating the TM $M_x$ on input $x$. If the step is used up, reject. Otherwise output the opposite of the answer of the simulation.

The language $L$ that is decided by TM $D$ is a member of class $\mathbf{DTIME}(n^{1+\epsilon})$. For contradiction, assume $L\in\mathbf{DTIME}(n)$, then there exists a TM $M$, on input $x$, outputs $D(x)$ in $O(|x|)$ steps Thus the universal TM $\mathcal{U}$ that simulates $M$ on input $\langle M\rangle$ operates in at most $O(|\langle M\rangle|\log{|\langle M\rangle|})$ steps. For enough large $n=|\langle M\rangle|$, $cn\log{n}\lt n^{1+\epsilon}$, so the simulation halts in advance. By definition the output of $D$ on input $\langle M\rangle$ is the opposite of $D(\langle M\rangle)$, which is a contradiction. $\blacksquare$

**Thm 4.** (Ladner) If $\mathbf{P}\not=\mathbf{NP}$, then there is a language $L\in\mathbf{NP}\setminus\mathbf{P}$ that is not $\mathbf{NP}$ -complete.

**Pf.** The key is the language $SAT_H=\{\phi01^{n^{H(n)}}:\phi\in SAT,n=|\phi|\}$ with $H:\mathbb{N}\mapsto\mathbb{N}$.

(to be completed)

---

### 参考资料

- [1] Sanjeev Arora and Boaz Barak. [Computational Complexity: A Modern Approach](http://venillalemon.github.io/books/ccama.pdf). Cambridge University Press, USA, 1st edition, 2009.

- [2] Sipser, M. [Introduction to the Theory of Computation](http://venillalemon.github.io/books/itc.pdf). Thomson Course Technology, Boston, 3rd edition, 2012.
