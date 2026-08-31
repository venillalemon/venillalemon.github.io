# Dirichlet theorem: using cyclotomic polynomials

*July 18, 2025*

下午从七分厂返回，和大 N 老师聊天提到数论，于是知道了这个证明.

**Thm.** For every fixed $m$, there are infinitely many prime numbers of the form $km+1$ where $k\in\mathbb{Z}$.

**Lem 1.** $n\gt1$, $p$ is prime, if for some $x\neq\pm1$, $p\mid\Phi_n(x)$, then either $p\mid n$, or $p\equiv_n1$.

**Pf. of Lem 1.** If for some $d\mid n(d\lt n)$, $p\mid x^d-1$, then $p\mid (x^d-1,\Phi_n(x))$. Since $\Phi_n(x)$ does not share any roots with $x^d-1$, we have $\Phi_n(x)\mid\frac{x^n-1}{x^d-1}$. Thus $p\mid(x^d-1,\frac{x^n-1}{x^d-1})$, where $\frac{x^n-1}{x^d-1}=\frac{(x^d-1+1)^{\frac{n}{d}}-1}{x^d-1}=A(n^d-1)+\frac{n}{d}$ (note that this requires $x^d\neq1$). Then $p\mid\frac{n}{d}\mid n$.

If not, i.e. for every $d\mid n(d\lt n)$, $p\nmid x^d-1$ that is, $x^d\not\equiv_p1$. So the order of $x$ in $\mathbb{F}_p$ is $n$. Thus, $n\mid p-1$ and the conclusion follows.

**Lem 2.** Let $f\in\mathbb{Z}[x]$ which is not a constant and $f(0)=1$. Then there are infinitely many prime factors in the set $\{f(n):n\in\mathbb{Z}\}$.

**Pf. of Lem 2.** Assume that there are finitely many prime factors, say, $p_1\lt\dots\lt p_k$. Let $f(x)=\sum_{i=0}^na_ix^i$, then we know that for all $i\in[k]$, $p_i\mid f(p_1\dots p_k)$, thus $p_i\mid a_0$. But $a_0=1$, contradiction.

**Pf. of Thm.** Consider the set $S=\{p:p\gt m,p\text{ is prime, and } \exists x\not=\pm1,\;p\mid \Phi_m(x)\}$. Every element $p$ in this set has $p\gt m$, thus $p=1+km$ for some $k\in\mathbb{Z}$. Furthermore, there are infinitely many prime factors in the set $\{\Phi_m(x):x\in\mathbb{Z}\}$ by Lem 2, so there are infinitely many primes in such set $S$.

---
