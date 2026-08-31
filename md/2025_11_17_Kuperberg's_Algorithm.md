# Kuperberg's Algorithm

*November 17, 2025*

In this article we denote $D_N=\langle x,y\mid x^N=y^2=yxyx=1\rangle$ . Or equivalently we have $xy=yx^{N-1}$  and $yx=x^{N-1}y$ .

We use $D_N=\{y^tx^s:t\in\{0,1\},s\in\mathbb{Z}_N\}$ .

All the subgroups of $D_N$  is either a rotational group $\langle x^d\rangle$ , or a dihedral group $\langle x^d,yx^s\rangle$ , where $d\mid N$  and $0\le s< d$ .

For instance, when $d=N$ , the subgroup is $\langle yx^s\rangle\cong C_2$ .

> **Definition.** Dihedral Hidden Subgroup Problem
>
> Given $N$  and a subgroup $H=\langle yx^d\rangle$  a function $f$  which is stable on every right (or left) coset of $H\le D_N$ .
>
> The goal is to output $d$ .

**Kuperberg’s Algorithm** for $N=2^n$

**Step1.** Create the uniform superposition over $D_N$ .

Take initial state $|0\rangle|0\rangle$ , the first state is of $n$  qubits and the second is of $1$  qubits. Then we apply QFT on $\mathbb{Z}_N$

$$
\begin{align*}
F_N:|x\rangle\mapsto\frac{1}{\sqrt{N}}\sum_{k=0}^{N-1}e^{\frac{2\pi ikx}{N}}|k\rangle
\end{align*}
$$

to both register and obtain

$$
\begin{align*}
\frac{1}{\sqrt{2N}}\sum_{s\in \mathbb{Z}_N}\sum_{t\in\{0,1\}}|s\rangle|t\rangle
\end{align*}
$$

which is recognized as a ‘constant pure state’ in Hilbert space $\mathbb{C}[D_N]$ .

**Step 2. **Compute $f$  and obtain.

$$
\begin{align*}
\frac{1}{\sqrt{2N}}\sum_{s\in \mathbb{Z}_N}\sum_{t\in\{0,1\}}|s\rangle|t\rangle|f(y^tx^s)\rangle
\end{align*}
$$

**Step 3.** Measure the third register and record the output.

Suppose we measured the result $r$ , there are $2$  possible $(s,t)$  ’s satisfying $f(y^tx^s)=r$ . To conclude, if $f(x^s)=r$  then $f(y^tx^{s+d})=r$ . So the remaining state is proportional to

$$
\begin{align*}
|s\rangle|0\rangle+|(s+d)\text{ mod }N\rangle|1\rangle
\end{align*}
$$

for some $s$ .

**Step 4. **Apply QFT on the first register, obtaining

$$
\begin{align*}
\sum_{k=0}^{N-1}e^{\frac{2\pi iks}{N}}|k\rangle|0\rangle+\sum_{k=0}^{N-1}e^{\frac{2\pi ik(s+d)}{N}}|k\rangle|1\rangle\propto\sum_{k=0}^{N-1}|k\rangle\left(|0\rangle+e^{\frac{2\pi ikd}{N}}|1\rangle\right)
\end{align*}
$$

**Step 5. **Measure the first register and record it, we have

$$
\begin{align*}
|0\rangle+e^{\frac{2\pi ikd}{N}}|1\rangle:=|\psi_k\rangle
\end{align*}
$$

for some $k$ .

Now we have to ponder on this state. If $k=2^{n-1}=\frac{N}{2}$ , then the state is exactly $|0\rangle+(-1)^d|1\rangle$ . By measuring on the basis $\{|+\rangle,|-\rangle\}$  we know the parity of $d$ .

The trick is as follows:

[![](https://notes.sjtu.edu.cn/uploads/upload_9faef2db6f86bfc41961d849075c8412.png)](https://notes.sjtu.edu.cn/uploads/upload_9faef2db6f86bfc41961d849075c8412.png)
