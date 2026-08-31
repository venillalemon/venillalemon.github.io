# Computation Theory - 0x00

*January 14, 2025*

*…ようこそ。Ave Mujicaの世界へ*

> 2025 冬休み

## Chapter 1 正则语言

> **定义.** 有限自动机，(deterministic) finite automaton (pl.-ta) (DFA) 有限自动机是一个五元组 $(Q,\Sigma,\delta,q_0,F)$ ： $Q$ - 有限状态集 $\Sigma$ - 有限字符集 $\delta:Q\times\Sigma\mapsto Q$ - 转移函数 $q_0\in Q$ - 初始状态 $F\subseteq Q$ - 接受状态集合

**语言**是字符串的集合，即 $\Sigma^*\cup\{\epsilon\}$ 的子集. 一个有限自动机所接受的所有字符串集合也是一个语言，记作 $L(M)$. 需要特别注意语言 $\varnothing$ 和字符串 $\epsilon$ 的区别.

> **定义.** 正则语言，regular language 对于语言 $A$ ，如果存在自动机 $M$ 使得 $L(M)=A$ ，那么 $A$ 是正则语言。

> **定义.** 正则运算，regular operation 对语言 $A,B$ ， 定义 $A\cup B=\{x:x\in A\text{ or }x\in B\}$, $A\circ B=\{xy:x\in A\text{ and }y\in B\}$, $A^*=\{x_1\dots x_k:k\geq 0, \forall i\;x_i\in A\}$

通过构造有限自动机的 Cartesian product（接收状态不一定是两个接收状态集合的积），我们可以证明正则语言的有限交并封闭，即两个正则语言的交或并，还是正则语言.

> **命题** 正则语言对于有限正则运算封闭.

为了证明以上命题，我们引入**非确定性有限自动机**的概念，它在确定版本的基础上允许“并行”计算.

> **定义.** 非确定性有限自动机，nondeterministic finite automaton (NFA) 非确定性有限自动机是一个五元组 $(Q,\Sigma,\delta,q_0,F)$ ： $Q$ - 有限状态集 $\Sigma$ - 有限字符集 $\delta:Q\cup\{\epsilon\}\times\Sigma\mapsto \mathcal{P}(Q)$ - 转移函数， $\mathcal{P}(Q)=\{A:A\subseteq Q\}$ $q_0\in Q$ - 初始状态 $F\subseteq Q$ - 接受状态集合

转移函数的定义允许一个状态在同一个字符的情况下跳转到多个状态。

> **定义.** Nerode 等价关系 对于 DFA $M$, 如果两个字符串 $x,y$ 经过 $M$ 后达到相同的状态，那么说 $x\textbf{R}_My$. 这是一个等价关系.

实际上 Nerode 等价说的是两个字符串在 DFA 上的不可区分性. 类似地可以定义两个字符串在语言上的不可区分性 $x\textbf{R}_Ly\iff\forall z,\;x\circ z\in L\leftrightarrow y\circ z\in L$. 显然 $x\textbf{R}_My\rightarrow x\textbf{R}_{L(M)}y$.

> **定理.** Myhill-Nerode $A$ 是正则语言当且仅当 $\textbf{R}_A$ 导出的等价类有限.

**证明.** $\rightarrow$ 显然. $\leftarrow$ 假设等价类个数为 $m$. 构造 DFA $M=(Q,\Sigma,\delta,q_0,F)$, $|Q|=m$, $q_0$ 对应 $\epsilon$ 代表的等价类. Admitted.

> **习题** 1.52 令 $\Sigma=\{1,/\}$ ，
>
> $$
> Y=\{x_1/\dots/x_k:k\geq 0,\;x_i\in 1^*,\;\forall i\not=j,\;x_i\not=x_j\}
> $$
>
> 求证 $Y$ 不是正则语言.

**证明.** 假设 $L(M)=Y$ ， $p$ 为 pumping length. $s=1^p/1^{p-1}/\dots/1/$. 由 pumping 引理，存在 $s=xyz$ 满足三个条件，故 $y=1^k,1\leq k\leq p$ ，且 $xz\in Y$. 但是在 $xz$ 中，前导1的个数小于 $p$ （注意 $|y|>0$ ）. 因此和后面某一段重复， $xz\notin Y$ ，矛盾. 故 $Y$ 非正则. $\blacksquare$

## Chapter 2 上下文无关语言

CFL

前面说到语言 $B=\{0^n1^n|n\in\mathbb{N}\}$ 不是正则语言。 但是我们发现这样的语言在一种操作下是封闭的，即前面加上0，后面加上1. 如果字符串 $A\in B$ ，那么 $0A1\in B$.

$$
A\to0A1\\
A\to\epsilon
$$

可以表示 $A\in B$ 可以是一个空字符串，也可以由另一个 $B$ 中的字符串前加0、后加1得到。 $A$ 称为一个变量，可以根据推导规则来替换； $0,1,\epsilon$ 都是终结符，它不能继续被替换.

> **定义.** 上下文无关文法，context-free grammar 四元组 $G=(V,\Sigma,R,S)$ $V$ - 有限变量集合 $\Sigma$ - 有限终结符集合，它和 $V$ 交集为空 $R$ - 有限推导规则集合，将变量推导到由变量、终结符组成的字符串 $S\in V$ - 初始变量

如果 $u,v,w\in(V\cup\Sigma)^+$ ，且有规则 $A\to v$ ，那么可以说 $uAw$ 导出 (yield) $uvw$ ，记作 $uAw\Rightarrow uvw$. 如果 $u\Rightarrow^*v$ （可能相等，也可能经过有限步推导得到v），那么说 $u$ 派生出(derive) $v$. 上下文无关文法 $G$ 的语言定义为 $L(G)=\{w\in\Sigma^*:S\Rightarrow^*w\}$ ，上下文无关语言就是能由一个上下文无关文法导出的字符串集合.

一般来说，初始变量就是第一条推导规则的左边变量.

> **定义.** Chomsky 正规形式 每条规则都有
>
> $$
> A\to BC\\A\to a
> $$
>
> 的形式，其中 $a$ 为终结符， $A,B,C$ 为变量.

> **定理.** 每个上下文无关语言都可以被一个 Chomsky 正规形式的上下文无关语言所生成.

**证明.** step0. 添加 $S_0\to S$ ，使初始变量变成 $S_0$ ，它不会出现在推导规则右侧.

step1. 去掉形如 $A\to\epsilon$ 的规则：为每次 $A$ 的出现添加一条规则，左侧变量不变，右侧替换。例如

$$
A\to\epsilon
$$

$$
B\to uAvAw
$$

经过两次替换，变为

$$
A\to\epsilon
$$

$$
B\to uAvAw
$$

$$
B\to uvAw
$$

$$
B\to uAvw
$$

$$
B\to uvw
$$

step2. 去掉形如 $A\to B$ 的 unit rule：对于所有形如 $B\to u$ 的规则，添加规则 $A\to u$. **所有添加操作后，必须去掉重复的规则.**

step3. 现在所有的规则都没有 $A\to\epsilon$ 或 $A\to B$ 的形式. 对于规则 $A\to v_1\dots v_k$ ，其中 $v_i\in(V\cup\Sigma)^+,k\geq 3$ ，可以拆成相继的 $A_{k-1}\to V_kA_k,\;V_k\to v_k$ 形式. $\blacksquare$

> **定义.** 下推自动机（非确定性） 六元组 $(Q,\Sigma,\Gamma,\delta,q_0,F)$ ：相比 NDFA，增加了栈字符集. $\delta:Q\times\Sigma_{\epsilon}\times\Gamma_{\epsilon}\mapsto\mathcal{P}(Q\times\Gamma_{\epsilon})$ ，根据当前状态+输入字符+栈顶元素，非确定性地改变状态+出入栈操作. 第二个输入为 $\epsilon$ 表示无需读字符串；第三个输入为 $\epsilon$ 表示无需出栈；第二个输出为 $\epsilon$ 表示无需入栈。可简记为 $a,b\to c$.

> **定理.** 一个语言 $G$ 是上下文无关的，当且仅当存在一个（非确定性）下推自动机 $M$ ，使得 $L(M)=G$.

> **引理** 如果 $G$ 是上下文无关语言，那么存在一个（非确定性）下推自动机 $M$ ，使得 $L(M)=G$.

**证明.** 我们构造一个下推自动机. $Q=\{q_{\text{st}},q_{\text{lp}},q_{\text{ac}}\}$. 为了更高效的描述该自动机，我们用一种简洁的办法，即一次可以在栈中写入多个字符. 它与一次写入一个字符等价，参考下图.（观察到起止状态之间添加了若干状态，下一次读入时，中间状态会自动reject，因此等价.）![](https://notes.sjtu.edu.cn/uploads/upload_732fe144e74a6fb84c5d733283839a26.png)

我们可以描述转移函数 $\delta$ ：

$$
q_{\text{st}},\epsilon,\epsilon\to q_{\text{lp}},S{\$}
$$

$$
q_{\text{lp}},a,a\to q_{\text{lp}},\epsilon
$$

$$
q_{\text{lp}},\epsilon,A\to q_{\text{lp}},w\;(\text{where $A\to w\in R$ is a rule})
$$

$$
q_{\text{lp}},\epsilon,\$\to q_{\text{ac}},\epsilon
$$

相当于在 parse tree 上做 dfs. $\blacksquare$

我们略去反方向的证明. 不难发现，NDFA 天然是一个 PDA，因此正则语言一定上下文无关，上下文无关是一种更强的模型.

> **定理.** (Pumping Lemma for CFL) $A$ 是一个上下文无关语言，那么存在 $p$ ，对于任意长度大于等于 $p$ 的字符串 $s\in A$ ，存在分解 $s=uvxyz$ 满足以下三个条件
>
> - 对于 $i\geq 0$ ， $uv^ixy^iz\in A$,
>
> - $|vy|>0$,
>
> - $|vxy|\leq p$.

> **定义.** 确定性下推自动机（DPDA） 六元组 $(Q,\Sigma,\Gamma,\delta,q_0,F)$ ：相比 PDA，每个状况下可取的操作都是固定的. $\delta:Q\times\Sigma_{\epsilon}\times\Gamma_{\epsilon}\mapsto(Q\times\Gamma_{\epsilon})\cup\{\varnothing\}$ ，根据当前状态+输入字符+栈顶元素，确定性地改变状态+出入栈操作， $\varnothing$ 表示函数在该处未定义. 参数定义同非确定性，但是 $\delta$ 必须满足：
>
> $$
> \forall q\in Q,a\in\Sigma,x\in\Gamma,\\\text{在 }\delta(q,a,x),\delta(q,\epsilon,x),\delta(q,a,\epsilon),\delta(q,\epsilon,\epsilon)\text{ 四个函数值中，}\\\text{有且仅有一个为}\varnothing.
> $$
>
> 它保证了不会出现歧义，如果没有这一条限制，当栈非空时，若栈顶为 $a$ ，下一个输入为 $x$ ，四个函数值都有可能使用. **注意：如果在栈空时尝试弹出，则自动拒绝该输入.**

由确定性状态机接受的语言称为**确定性上下文无关语言**.

> **引理** 对于任一 DPDA，相应存在一个 DPDA 能够读取完整的字符串并对于任意字符串输入，都给出和原来的自动机相同的结果（即等价）. **说明** DPDA可能在读取完字符串之前就给出接受/拒绝的结果. 情况1：对空栈进行pop操作；情况2：无限循环，如果自动机在 $(q,x)\in Q\times\Gamma$ 之后，不再弹出 $x$ 之前的任何字符，且不读取输入字符串，则自动机将会陷入死循环. 称这样的 $(q,x)$ 为 *looping situation*. （问题：导致自动机出现死循环的字符串应算作接受or拒绝？）

**证明思路.** 我们对于原来的 DPDA $M$ 做亿点点修改，得到满足条件的 DPDA $M^\prime$ ： step0. 添加公共起始状态 $q_s$ 、接受状态 $q_a$ 、拒绝状态 $q_r$.

step1. 复制 $Q$ （不包括step0中添加的）到 $Q_a$ ， $Q_a$ 中的状态全为接受态，记新的接受集为 $F^\prime$. 适当添加状态转换，使该自动机在进入接受状态（不管是否读到字符串末尾）时，一直保持在接受状态，直到读取下一个字符.

step2. 在 $q_a$ 转移到 $q_0$ 的同时，向栈中添加 $. 在 $F^\prime$ 检测到 $ 时，跳转到 $q_a$ ，此时如果输入还有后续字符，跳转到 $q_r$ 并读到输入的末尾；在其他态上检测到 $ 时，跳转到 $q_r$ 并读到末尾.

step3. 假设自动机遇到了一个 **looping situation** $(q,x)$. 那么由 step1 引入的性质，在此之后，无论是否接受，自动机必将稳定在接受态或拒绝态其一状态. 如果稳定在接受态，跳转到 $q_a$ ；反之跳转到 $q_r$. 然后 step2 保证了输入一定会被读完.

**确定性上下文无关文法**

这里我们将研究对象设为**带结束符的语言**，即语言中每个字符串都以 $\vdash$ 结尾. 后面会证明，如果没有这个结束符 $\vdash$ ，DPDA 和 DCFG（确定性上下文无关文法） 将不等价.

回顾上下文无关文法，我们使用**推导**（derivation）来生成语法树，存在歧义的问题，同一个字符串的语法树可能不相同，它是一个自顶向下方法. 在确定性的版本中，我们使用**归约**（reduction，注意和计算复杂性中的*归约*相区别）. 对于一个由终结符和变量组成的字符串，首先得到它所有可归约的子串. 然后进行**最左归约**，每一次最左归约时，被归约的字符串左侧没有待归约的字符串. 直到最后得到初始变量为止.

下面我们开始讨论，谨记我们的目标是：对上下文无关文法做一些调整，使它能够成为某个**确定性下推自动机**的语言.

对于语言 $L(G)$ 的完整的、可行的归约，定义**有效串**（valid string）为所有出现在 $L(G)$ 归约过程中的、由终结符、变量组成的字符串. 对于归约过程中出现的字符串，我们称它的可被归约的、由终结符/变量组成的子字符串（连带其归约规则）为**句柄**（handle）. 注意对于一个文法 $G$ ，句柄的概念只对有效串有定义.

如果一个有效串有多个句柄，那么语法一定有歧义. 因为如果语法无歧义，那么 parse tree 唯一，最左归约也唯一. 因此句柄唯一.

> （以下内容摘自 p.136 原文，**曾经**存疑） 如果一个有效串有多个句柄，那么语法一定有歧义. 因为如果语法无歧义，那么 parse tree 唯一，最左归约也唯一. 因此句柄唯一.![](https://notes.sjtu.edu.cn/uploads/upload_c74966a6df432143c9718f1c6b44a4c5.png) 反例：考虑语法 $G$
>
> $$
> A\to abc\;|\;cAa\\B\to cab
> $$
>
> 对于 $cabca\in L(G)$ ，按照定义，cab 和 abc 都是句柄. 然而 $G$ 在 $L(G)$ 上无歧义，对于 $L(G)$ 中的字符串，解析树节点一定都是A，且除了叶节点外，所有节点都只有一个子节点。 错误说明：书上的定义不甚了然，笔者误认为句柄是**左侧没有可归约子串的可归约子串**.

~~暂且不论以上存疑的部分，~~我们接下来讨论，为什么句柄的唯一性也不能保证语言能由确定性下推自动机生成. 考虑文法

$$
R\to S\;|\;T\\S\to ab\;|\;aSb\\T\to abb\;|\;aTbb
$$

对于任一文法满足的字符串，句柄唯一. 但是该语言不可由确定性下推自动机生成.

我们需要更强的条件. 如果字符串 $xhy$ 中有唯一句柄 $h$ ，且 $h$ 在读取完成时就可以被确定为一个句柄，那么就可以做相应的归约. 形式化地说，如果 $h$ 是所有形如 $xhz$ 的有效串的唯一句柄，那么这样的 $h$ 就是字符串 $xhy$ 的**强制句柄**.

> **定义.** 确定性上下文无关文法，DCFG 对于一个CFG，如果每个有效串都有一个强制句柄，那么它是 DCFG.

接下来省去具体的说明，仅对一些定理作了解.

> **定理.** $G$ 能够通过 DK-测试当且仅当 $G$ 是 DCFG.

> **定理.** 带结束符的语言能被 DCFG 生成，当且仅当该语言是确定性上下文无关的（i.e. 能被 DPDA 识别）.

**说明.** 如果没有结束标识符，DCFG 仅仅生成所有 DCFL 中 ***prefix-free*** 的那些语言（即，语言中任意一个字符串都不是任何其他字符串的前缀，带结束符的语言一定 prefix-free）. DPDA 不受影响.

很多时候，强制句柄的要求太高，因此我们允许 $k$ 个字符的前瞻。称 $h$ 为 $xhy$ 的 ** $k$ -前瞻强制句柄**，如果对任意和 $y$ 共有前 $k$ 个字符的串 $z$ ， $h$ 是 $xhz$ 唯一的句柄.

> **定义.** 对于一个上下文无关文法，如果每个有效串都有一个 $k$ -lookahead 强制句柄，那么它是 $LR(k)$ 文法.

$\bigtriangleup$ $\bigtriangledown$

## Chap7 时间复杂性

在这里，我们会频繁用到 $n$ 这个变量，它指的是图灵机的输入规模，即初始状态下纸带中内容的长度.

> **定义.** 时间复杂度，time complexity 假设 $M$ 是一个确定性图灵机，而且它对于任何输入都停机. 时间复杂度是一个函数 $f:\mathcal{N}\mapsto\mathcal{N}$ ，表示在长度为 $n$ 的输入下， $f(n)$ 是图灵机需要运行的最大步数. 一般我们用渐进记号表示复杂度，那么可以取 $f:\mathcal{N}\mapsto\mathcal{R}^+$.

> **定义.** 时间复杂度类，time complexity class 对于函数 $t:\mathcal{N}\mapsto\mathcal{R}^+$ ，**TIME** $(t(n))$ 是在 $O(t(n))$ 内可被图灵机决定的语言集合。

前面我们证明过，图灵机的不同变体之间等价，但是它们之间存在效率的差别.

> **定理.** 假设 $t(n)>n$ ，任意 $t(n)$ 时间的多纸带确定性图灵机等价于某一个 $O(t^2(n)$ 复杂度的单纸带确定性图灵机.

**证明思路.** 回顾如何将多纸带变成单纸带，我们将所有纸带内容拼接成单纸带，那么多纸带每完成一步操作，单纸带为了知道每个指针的位置，需要扫描所有的内容. 然后，根据状态机决定是否将后续字符后移. 这两步总体来说耗费的时间复杂度近似于所有纸带内容长度之和.

由于多纸带最多跑 $O(t(n))$ 步，第一条纸带上最多写 $n+O(t(n))=O(t(n))$ 个字符，其余纸带上最多写 $O(t(n))$. 因此长度总和为 $O(t(n))$. 因此最终复杂度为 $O(t^2(n))$.

除了增加纸带，还有非确定性图灵机的变体，我们为其定义时间复杂度.

> **定义.** 非确定性图灵机的运行时间 如果非确定性图灵机在所有分支上都停机，那么可以定义运行时间为最深分支的深度. 其他定义与确定性类似.

> **定理.** 可被单纸带 TM 在 $o(n\log{n})$ 时间复杂度内识别的语言一定是正则语言.

也就是说，单纸带图灵机需要花至少 $n\log{n}$ 的时间复杂度来识别非正则语言.

**证明思路.** 引入*穿越序列*，用于记录每次纸带的读写头进入某一个位置时，TM 的状态 $q\in Q$. step1. 证明若在任意输入下，TM 的穿越序列都不长于 $k$ ，那么我们可以用 NFA 模拟该 TM. 这一步参考论文 [https://doi.org/10.1016/S0019-9958(65)90399-2](https://doi.org/10.1016/S0019-9958(65)90399-2) step2. 假设一个满足题设的 TM 拥有任意长的穿越序列，构造一个可接受的最短输入，使该输入在 TM 纸带上第 $i$ 个位置的穿越序列长度大于 $k$. step3. 在保持可接受的情况下，将该输入进行删节，推出矛盾. 以上思路参考论文 [https://doi.org/10.1016/0304-3975(85)90165-3](https://doi.org/10.1016/0304-3975(85)90165-3)

素数判定问题属于多项式时间类. 见 AKS 素性测试 [https://doi.org/10.4007/annals.2004.160.781](https://doi.org/10.4007/annals.2004.160.781)

> **定义.** 验证机，verifier 如果
>
> $$
> A=\{w:\exists c, \text{图灵机 } V \text{ 接受 }\langle w,c\rangle\},
> $$
>
> 那么 $V$ 是 $A$ 的验证机.

> **定义.** NP 是能以多项式时间被验证的语言集合.

> **定义.** 非确定性时间复杂度类，nondeterministic time complexity class 对于函数 $t:\mathcal{N}\mapsto\mathcal{R}^+$ ， $\textbf{NTIME}(t(n))$ 是在 $O(t(n))$ 内可被非确定性图灵机决定的语言集合。

有 $P = \bigcup_k\textbf{TIME}(n^k)$ ， $NP = \bigcup_k\textbf{NTIME}(n^k)$

> **定理.** 一个语言是 NP 的当且仅当它能被非确定性图灵机决定.

**证明.** 如果 $A\in \text{NP}$ ，那么存在多项式时间的验证机 $V$ ，并假设它在 $cn^k$ 步内停机（只有对所有输入都停机的 TM 才能定义时间复杂度）. 在这 $cn^k$ 步内最多可以看到纸带上的 $cn^k$ 个字符. 因此如果对于所有长度小于 $cn^k$ 的输入， $V$ 都拒绝，那么 $V$ 拒绝所有输入.

构造非确定性图灵机 $N$. 对于输入串 $w$ ，先遍历得到长度 $n$ ，然后非确定性地产生长度小于 $cn^k$ 地所有串 $c$ （由于字母表有限，这样的字符串也是有限个），合并为 $\langle w,c\rangle$ 并输入到 $V$ 中. 如果有一个 $V$ 接受，那么接受；否则拒绝.

如果 $A$ 能被某个 NTM $N$ 决定，那么验证机 $V$ 以输入 $w$ 模拟 $N$ ，然后选择和 $c$ 对应的分支. （缺少具体的细节，但是正确）

这一段证明实际上参考的是前面我们对“确定性和非确定性图灵机在计算能力上等价”的证明.

> **定理.** (Cook-Levin) $SAT$ 是 NP-完全问题.

**证明大纲.** 目标是证明所有 NP 问题归约到 $SAT$. 在此证明中，先任取 NP 问题 $A$ ，假设它能被非确定性图灵机以 $n^k$ 步以内决定（注意并非渐进分析）. 因此对于每一个分支，我们可以只记录纸带的前 $n^k$ 个字符在前 $n^k$ 步的状态，列表.

我们用逻辑变量 $x_{i,j,s}$ 记录表格的情况， $x_{i,j,s}=true$ 表示表格 $i,j$ 位记录 $s$. 那么一个合法的表格可以用一个逻辑关系式表示. 它描述每个位置的存在性、唯一性，描述初始状态和接受状态，也描述合法的状态转移（2*3滑动窗口）.

余下的只需证明这个规约可被多项式时间内计算. 事实上大多数 formula 都是重复的.

> **推论** $SAT_\text{3CNF}$ 是 NP-完全问题.

**证明.** 只需证明 $SAT\leq_\text{P}SAT_\text{3CNF}$.

首先，每个布尔表达式都能被转换成 CNF. 高中通用技术课杨老师教我们从真值表写表达式的方法. 例如下面真值表

|  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| y | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
| z | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
| v | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |

那么看结果1的行， $v=\neg x\neg y\neg z+\neg xyz+x\neg yz$ ，这是一个 DNF. 反过来看结果0的行， $\neg v=\neg x\neg yz+\neg xy\neg z+\dots$ ，即 $v=(x+y+\neg z)(x+\neg y+z)\dots$ 就是 CNF. 不过这个算法至少是指数级别的复杂度.

一种多项式复杂度的办法是，先取反得到 $\neg v$ 的表达式，用 De Morgan 和分配律展开为DNF，再非回去. 总之， $SAT\leq_\text{P}SAT_\text{CNF}$.

下面就是把每个长串的“或”拆开，显然在多项式时间内可以将 CNF 转为 3CNF.

$$
a_1\lor\dots\lor a_n=(a_1\lor a_2\lor z_1)\land(\neg z_1\lor a_3\lor z_2)\land\dots\land(\neg z_{n-3}\lor a_{n-1}\lor a_n)
$$

综上 $SAT\leq_\text{P}SAT_\text{3CNF}$. $\blacksquare$

通过分析图灵机的状态，我们得到了第一个 NP-完全问题 $SAT$. 如果 $SAT$ 能以多项式时间归约到某个问题 $A$ ，那么即可证明所有 NP 问题都能以多项式时间归约到 $A$.

> **定理.** $VC$ 是 NP-完全问题.

$VC=\{\langle G,k\rangle:G\text{ 是拥有 }k\text{-顶点覆盖的无向图}\}$

**证明.** 显然它是 NP 问题. 我们证明 $SAT_\text{3CNF}\leq_\text{P}VC$.

根据一条 3-CNF 可满足的逻辑语句，我们构造无向图 $G$. $G$ 包含两部分，第一部分的顶点是所有 $x$ 和 $\neg x$ 并连接，总计 $2n$. 第二部分是所有 3-clique，由逻辑语句中所有由三个变量进行或运算操作的语句构成，总计 $3l$. 两部分中相同的变量进行连接.

![vertex cover](https://notes.sjtu.edu.cn/uploads/upload_6e7c2b1fd8b8ca6a8fa9a0b7ac109c2c.png)

如果可满足，在第一部分中为 true 的顶点进入覆盖；第二部分中，每个 3-clique 都有一个 true 顶点，那么另外两个顶点进入覆盖.

对于第一、第二部分的边，一定有覆盖；对于中间的边 $x_1^1x_1^{2}$ ，若 $x_1$ 为 true，那么 $x_1^1$ 在覆盖中；反之， $x_1^2$ 在覆盖中. 因此 $G$ 存在 $n+2l=k$ -顶点覆盖.

如果 $G$ 有 $n+2l=k$ -顶点覆盖，那么在 $x$ 和 $\neg x$ 中必有一个、 3-clique 中必有2个顶点在覆盖中. 按前面所述规则为每个变量赋值，我们证明这样的赋值能使原来的逻辑表达式为 true.

假设 3-clique 的每个变量都是 false，那么和它们对应的第一部分顶点都不在覆盖中，为了让相应的边被覆盖，这个 3-clique 必须都在覆盖中，矛盾. 因此存在 true 变量，满足该逻辑表达式. $\blacksquare$

## Chap8 空间复杂性

空间可以重复使用，因此我们修改 TM 为双纸带. 第一条有限只读，存放规模为 $n$ 的输入；还有一条无限长纸带，可读可写，我们用第二条纸带上，指针走过位置的大小来定义空间复杂度. 对于非确定性，我们取所有分支中占空间最大的那个. 与时间复杂度类似，我们有 $\textbf{SPACE}(f(n))$ 和 $\textbf{NSPACE}(f(n))$.

> **例** $SAT$ 属于 $\textbf{SPACE}$. 对于输入 $\langle\phi\rangle$ ，图灵机遍历所有变量的取值，它只需线性的空间来记录目前每个变量的真值即可.

> **定理.** (Savitch) 对于任意复杂度函数 $f:\mathcal{N}\mapsto\mathcal{R}^+$ ，如果 $f(n)>n$ ，那么

$$
\textbf{NSPACE}(f(n))\subseteq\textbf{SPACE}(f(n)^2)
$$

**证明思路.** 我们曾经做过将 NTM 转换为 TM，即跑遍所有分支（同样，空间复杂度只对永远停机的 TM 有定义）. 每个分支的空间复杂度为 $O(f(n))$ ，但是可以跑任意多步（假设为 $2^{O(f(n))}$ ），因此分支的层数也是 $2^{O(f(n))}$ ，为了记录分支的位置，至少需要 $2^{O(f(n))}>O(f(n)^2)$ 的空间.

用新的方法，对于 NTM $N$ ，引入递归函数 CANYIELD($c_1,c_2,t$)，表示在 $t$ 步之内，NTM 的状态（configuation）可以从 $c_1$ 转移到 $c_2$. 由于空间有限， $N$ 的所有状态数也有限，令它小于 $2^{df(n)}$.

![canyield](https://notes.sjtu.edu.cn/uploads/upload_b6cd2581b6026dcd71cc3b349e0d5c26.png)

我们设计 TM $M$ 的作用是调用所有的 CANYIELD$(c_\text{st},c_\text{ac},2^{df(n)})$，由于 $N$ 状态数至多为 $2^{df(n)}$ ，函数 CANYIELD 将会递归 $df(n)$ 层，每次需在栈中记录调用参数，并用额外的最多 $O(f(n))$ 空间，因此总空间复杂度 $O(f(n)^2)$. $\blacksquare$

Savitch 向我们保证了 $\textbf{PSPACE}=\textbf{NPSPACE}$.

同时，图灵机在 $O(f(n))$ 时间复杂度之内只能探索至多 $O(f(n))$ 的空间，因此 $\textbf{P}\subset\textbf{NP}\subseteq\textbf{NPSPACE}=\textbf{PSPACE}$.

我们考虑 TM 的 configuation，如果它用了 $O(f(n))$ 的空间，那么最多有 $|Q|\times O(f(n))\times|\Gamma|^{O(f(n))}$ 个 configuration，因此时间复杂度至多为 $O(2^{f(n)})$.

$$
\textbf{P}\subset\textbf{NP}\subseteq\textbf{PSPACE}=\textbf{NPSPACE}\subseteq\textbf{EXPTIME}
$$

> **定义.** $\textbf{PSPACE}$ -complete
>
> $B\in\textbf{PSPACE}$ -complete 当且仅当 $B$ 属于 $\textbf{PSPACE}$ 且任意 $\textbf{PSPACE}$ 中的问题都可以以**多项式时间**归约到 $B$.

若以上的 $B$ 不属于 $\textbf{PSPACE}$ ，它被称为是 $\textbf{PSPACE}$ -hard.

为什么不用**多项式空间复杂度**？因为 trivially 可以归约，直接计算即可.

> **定理.**
>
> $$
> TQBF=\{\langle\phi\rangle:\phi\text{ 是 sentence 且所有量词前置}\land\text{Sat }\phi\}
> $$
>
> 属于 $\textbf{PSPACE}$ -complete.

**证明.** 首先，如果遍历每个变量的值，那么确实需要 $O(f(n))$ 的空间. 下证归约.

参考 $SAT$ 的证明，如果 $A$ 可以被 TM $M$ 多项式空间内确定，那么可以记录下每一刻的 configuration 在一张表格中，表格有 $2^{cn^k}$ 行， $bn^k$ 列. 然而一个多项式时间算法不足以跑完这个程序，以及记录 $2^{cn^k}$ 的时间信息.

因此我们用 Savitch 的思路. 用逻辑变量表示表格中的值，递归构造 $\phi_{c_1,c_2,t}$. 如果 $t=1$ ， $\phi_{c_1,c_2,t}=c_1\equiv c_2\lor c_2\in\text{Next}(c_1)$ ，否则

$$
\phi_{c_1,c_2,t}=\exists m\;[\phi_{c_1,m,\frac{t}{2}}\land \phi_{m,c_2,\frac{t}{2}}]
$$

然而这样一来， $t$ 的表达式长度为 $O(t)$. 由于至多跑 $2^{cn^k}$ 步，表达式长度就是指数的. 将递归式改为

$$
\phi_{c_1,c_2,t}=\exists m\;\forall x\;\forall y\;[((x\equiv c_1\land y\equiv m)\lor(x\equiv m\land y\equiv c_2))\to\phi_{x,y,\frac{t}{2}}]
$$

这样一来，设 $T(t)$ 为 $\phi_{-,-,t}$ 的长度， $T(t)=2cn^k+T(\frac{t}{2})$ 得 $T(2^{cn^k})=O(n^{2k})$ ，可在多项式时间内计算. $\blacksquare$

这里我们介绍另一个 $\textbf{PSPACE}$ -complete 的问题，它和必胜策略有关.

> **定义.** 公平组合游戏
>
> - 游戏有两个人参与，二者轮流做出决策，双方均知道游戏的完整信息；
>
> - 任意一个游戏者在某一确定状态可以作出的决策集合只与当前的状态有关，而与游戏者无关；
>
> - 游戏中的同一个状态不可能多次抵达，游戏以玩家无法行动（即，要么抵达已经走过的状态，要么该状态没有出边）为结束，且游戏一定会在有限步后以非平局结束。

---
