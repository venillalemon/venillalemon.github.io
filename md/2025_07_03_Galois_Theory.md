# Galois Theory

A short path 

## Preliminaries

## Finite Galois extensions

Let $E/F$ be a extension of field $F$. Define

$$
G=\mathrm{Gal}(E/F)=\{\sigma: E\to E \text{ isomorphism} \mid \sigma(a)=a \text{ for all } a\in F\}
$$

Then $G$ is a group under composition of functions, called the Galois group of $E/F$ . Then let

$$
\Omega=\{M\subseteq E \mid M \text{ is a field and } F\subseteq M\subseteq E\}
$$

be the set of intermediate fields of $E/F$ and

$$
\Gamma=\{H\subseteq G \mid H \text{ is a subgroup of } G\}
$$

be the set of subgroups of $G$ . There is a natural correspondence between $\Omega$ and $\Gamma$ given by

$$
\mathrm{Gal}(E/-):\Omega\mapsto\Gamma\text{, where }\mathrm{Gal}(E/-)(M)=\{\sigma \in G \mid \sigma|_M = \mathrm{id}_M\},
$$

and the invariant relation

$$
\mathrm{Inv}(-):\Gamma\mapsto\Omega\text{, where }\mathrm{Inv}(-)(H)=\{x\in E \mid \sigma(x)=x \text{ for all } \sigma\in H\}.
$$

Recall that we have no restrictions on the extension $E/F$ , so the Galois group $G$ can be infinite. We have the following:

> **Theorem 1. (Galois Correspondence)** Let $E/F$ be any field extension, and we have $G=\mathrm{Gal}(E/F)$ , $\Omega$ the set of intermediate fields of $E/F$ and $\Gamma$ the set of subgroups of $G$ . Then we have the following properties:
> 
> - If $F\subseteq M_1\subseteq M_2 \subseteq E$ are intermediate fields, then $\mathrm{Gal}(E/M_2)\subseteq \mathrm{Gal}(E/M_1)$ ;
>     
>     if $H_1\subseteq H_2 \subseteq G$ are subgroups, then $\mathrm{Inv}(H_2)\subseteq \mathrm{Inv}(H_1)$ .
>     
> - For all intermediate field $M\in \Omega$ , we have $\mathrm{Inv}(\mathrm{Gal}(E/M))\supseteq M$ ;
>     
>     for all subgroup $H\in \Gamma$ , we have $\mathrm{Gal}(E/\mathrm{Inv}(H))\supseteq H$ .
>     
> - For all intermediate field $M\in \Omega$ , we have $\mathrm{Gal}(E/\mathrm{Inv}(\mathrm{Gal}(E/M)))=\mathrm{Gal}(E/M)$ ;
>     
>     for all subgroup $H\in \Gamma$ , we have $\mathrm{Inv}(\mathrm{Gal}(E/\mathrm{Inv}(H)))=\mathrm{Inv}(H)$ .
>     

The proof is tedious thus omitted. Here we provide an example where $M\subsetneq\mathrm{Inv}(\mathrm{Gal}(E/M))$ .

<details>

<summary>Example</summary>

$F=\mathbb{Q}$ , $E=\mathbb{Q}(\sqrt[3]{2})$ which is not a normal extension. Consider $M=\mathbb{Q}$ and the only automorphism of $E/M$ is the identical automorphism. So $\mathrm{Inv}(\mathrm{Gal}(E/M))=E\supsetneq M$ .

</details>

> **Theorem 2. (Artin)** Let $H\subseteq \mathrm{Aut}(F)$ be an finite subgroup, then $[F:\mathrm{Inv}(H)]\leq|H|$ .
> 
<details>

<summary>Proof</summary>

Let $n=|H|$ , and the goal is to prove that every $n+1$ elements in $F$ are $\mathrm{Inv}(H)$ - linearly dependent. We enumerate $H=\{f_0=e,f_1,f_2,\dots,f_{n-1}\}$  , we consider the following linear equation system, for arbitrary $n+1$ elements $u_0,\dots,u_n$ :

$$
\sum_{j=0}^{n}f_i(u_j)x_j=0,\quad\forall\; 0\leq i<n
$$

and this equation is bound to have non-zero solutions, because there are $n+1$ equations and $n$ variables. Note that the first equation is exactly $\sum_j u_jx_j=0$ , so the next goal is to pick a non-zero solution $x=(a_0,\dots,a_n)$ and prove that all $a_j$ ’s are all in $\mathrm{Inv}(H)$ . We pick the solution with the least Hamming weight, and then suppose $a_0=1$ (permuting and scaling) . If $a_j\notin\mathrm{Inv}(H)$ , let $f_k(a_j)\not=a_j$ . Then we have

$$
\sum_{j=0}^{n}f_kf_i(u_j)f_k(a_j)=0,\quad\forall\; 0\leq i<n
$$

and the multiplication triggers a permutation in the order of the $n+1$ equations. So $(f_k(a_0)=1,\dots, f_k(a_n))$ is also a non-zero solution of the above equation; if some $a_j=0$ , then $f_k(a_j)=0$ . As a result, the solution $(0,a_1-f_k(a_1),\dots,a_n-f_k(a_n))$ has a Hamming weight less then $(1,a_1,\dots,a_n)$ , a contradiction.

</details>

## Fundamental Theorem of Galois Theory

Two intermediate fields $M,M’$ of the field extension $E/F$ is **conjugate** if there exists $\sigma\in\mathrm{Gal}(E/F)$ such that $M’=\sigma(M)$ . We have from definition that, for all $\sigma\in\mathrm{Gal}(E/F)$ , if $M=\mathrm{Inv}(H)$ ,

$$
\sigma(M)=\mathrm{Inv}(\sigma H\sigma^{-1});
$$

and if $H=\mathrm{Gal}(E/M)$ ,

$$
\sigma H\sigma^{-1}=\mathrm{Gal}(E/\sigma M).
$$

> **Theorem 3. (Fundamental Theorem of Galois Theory)** Let $E/F$ be a finite Galois extension, and $G=\mathrm{Gal}(E/F)$ . Then we have
> 
> - $\mathrm{Gal}(E/-)$ and $\mathrm{Inv}(-)$ are inverse of each other, i.e. $\mathrm{Inv}(\mathrm{Gal}(E/M))=M$ and $\mathrm{Gal}(E/\mathrm{Inv}(H))=H$ for every $M$ and $H$ .
> - The subgroups $H$ and $H’$ of $G$ are conjugate iff the intermediate fields $\mathrm{Inv}(H)$ and $\mathrm{Inv}(H’)$ are conjugate. Especially, $H\triangleleft G$ iff $\mathrm{Inv}(H)/F$ is a normal extension, where $\mathrm{Gal}(\mathrm{Inv}(H)/F)\cong G/H$ .
> - The intermediate fields $M$ and $M’$ are conjugate iff $\mathrm{Gal}(E/M)$ and $\mathrm{Gal}(E/M')$ are conjugate subgroups of $G$ . Especially,  $M/F$ is a normal extension iff $\mathrm{Gal}(E/M)\triangleleft G$ , where $\mathrm{Gal}(E/F)/\mathrm{Gal}(E/M)\cong \mathrm{Gal}(M/F)$ .
<details>

<summary>Proof</summary>

TODO

</details>

We have the following fact from the proof of the fundamental theorem. The Galois extension is defined as separable normal extension.

> **Corollary 4.** Let $E/F$ be a field extension. **FAE**:
> 
> - $E/F$ is a finite Galois extension;
> - $E$ is a splitting field of a separable polynomial over $F$;
> - $E/F$ is finite and $|\mathrm{Gal}(E/F)|=[E:F]$;
> - $G=\mathrm{Gal}(E/F)$ is a finite group and $\mathrm{Inv}(\mathrm{Gal}(E/F))=F$.

In fact, every finite extension of a finite field is a Galois extension. This is because $\mathbb{F}_{p^n}$ is the splitting field of $x^{p^n}-x$ over $\mathbb{F}_p$ .

Consider $E=\mathbb{F}_{p^n}$ and $F=\mathbb{F}_p$ , we have $E=F(u)$ , and the Frobenius automorphism $\sigma(u)=u^p$ . Thus the Galois group $\mathrm{Gal}(\mathbb{F}_{p^n}/\mathbb{F}_p)\cong C_n=\langle\sigma\rangle$ . Below are examples.

<details>

<summary>Example</summary>

We compute the structure of $G=\mathrm{Gal}(E/F)$ where $E$ is the splitting field of $x^5-4$ on $F=\mathbb{Q}$ .
    
We have $E=\mathbb{Q}(a=\sqrt[5]{4},\omega=e^{\frac{2\pi i}{5}})$ and $|\mathrm{Gal}(E/F)|=[E:F]=[\mathbb{Q}(a)(\omega):\mathbb{Q}(\omega)][\mathbb{Q}(\omega):\mathbb{Q}] = 5\times 4 = 20$ . Since $E$ is a linear space over $F$ , every operation in $\mathrm{Gal}(E/F)$ is uniquely determined by its transformation on $a$ and $i$ .

Consider $\sigma:a\mapsto a,\omega\mapsto\omega^2$ and $\tau=a\mapsto a\omega,\omega\mapsto\omega$ where $\sigma^4=\tau^5=e$ . A way to conpute the group is to use the free group notation with restrictions $\tau^2\sigma=\sigma\tau$ , but we will not do this chore.

From Sylow theorems, $\langle\tau\rangle\cong C_5$ is a normal subgroup of $\mathrm{Gal}(E/F)$ . Also we have 4-order element, so $\langle \sigma\rangle\cong C_4$ is also a subgroup of $\mathrm{Gal}(E/F)$ .

Let $N=\langle\tau\rangle$ and $H=\langle\sigma\rangle$ . Then

$$
N\cap H=\{e\},\quad |NH|=|N||H|=20=|G|\quad\Longrightarrow\quad G=N\rtimes H .
$$

The action of $H$ on $N$ by conjugation:

$$
\varphi_\sigma(\tau)=\sigma\tau\sigma^{-1}=\tau^2 ,
$$

so $\varphi:H\to\mathrm{Aut}(N)\cong\mathbb{Z}_5^*$ , $\sigma\mapsto 2$ , is an isomorphism, and

$$
G\cong C_5\rtimes_{\varphi}C_4=\mathbb{Z}_5\rtimes\mathbb{Z}_5^*.
$$

Equivalently, $G$ acts on the indices of the roots $a\omega^x$ by affine maps of $\mathbb{Z}_5$ , $\tau:x\mapsto x+1$ and $\sigma:x\mapsto 2x$ , so

$$
G\cong\mathrm{AGL}(1,5)=\{x\mapsto kx+l\ :\ k\in\mathbb{Z}_5^*,\ l\in\mathbb{Z}_5\}\cong\left\{\begin{pmatrix}k&l\\0&1\end{pmatrix}\right\}\le\mathrm{GL}_2(\mathbb{Z}_5) .
$$

</details>

## Galois Groups of Formulas

We say a subgroup $G$ of $S_n$ a **transitive subgroup** if for every pair $(i,j)\in[n]\times[n]$ , there exists $\sigma\in G$ such that $\sigma(i)=j$ . Here is the main theorem concerning the Galois groups of splitting fields.

> **Theorem 5.** Let $f(x)\in F[x]$ be a polynomial of degree $n$ and no multiple roots; and let $E$ be the splitting field of $f$ over $F$ . Let $S_n$ be the symmetric group of the $n$ roots $r_1,\dots,r_n$ of $f$ . Then
> 
> - $G_f=\mathrm{Gal}(E/F)$ is a subgroup of $S_n$ whose order is $[E:F]$ .
> - An element $\sigma\in S_n$ belongs to $G_f$ iff $\sigma$ reserves all the algebraic relations of all roots, i.e. for all $g\in F[x_1,\dots,x_n]$, if $g(r_1,\dots,r_n)=0$ then $g(\sigma(r_1),\dots,\sigma(r_n))=0$ .
> - $f$ is irreducible on $F$ iff $G_f$ is a transitive subgroup of $S_n$ .

### Pure Equations

We now apply Theorem 5 to the equations $x^n-1$ and $x^n-a$ ; both facts are used in the proof of necessity in the next section. Throughout, $n\geq 2$ , $\operatorname{char}F$ is $0$ or coprime to $n$ , so that $x^n-1$ has $n$ distinct roots in its splitting field, and these roots form a cyclic group of order $n$ . A generator $\omega$ of this group is a **primitive $n$-th root of unity**. Write $\mathbb{Z}_n^*$ for the unit group of $\mathbb{Z}_n$ , and $\Phi_n(x)$ for the $n$-th cyclotomic polynomial, i.e. the polynomial whose roots are exactly the primitive $n$-th roots of unity.

> **Fact 6.** Let $f(x)=x^n-1\in F[x]$ . Then $G_f$ is isomorphic to a subgroup of $\mathbb{Z}_n^*$ , hence abelian. Moreover $G_f\cong\mathbb{Z}_n^*$ iff $\Phi_n(x)$ is irreducible over $F$ .

<details>

<summary>Proof</summary>

The splitting field is $E=F(\omega)$ , so $\sigma\in G_f$ is determined by $\sigma(\omega)$ . Since $\sigma(\omega)$ is again a root of $x^n-1$ of order $n$ , we have $\sigma(\omega)=\omega^k$ with $k\in\mathbb{Z}_n^*$ . The map

$$
G_f\to\mathbb{Z}_n^*,\qquad \sigma\mapsto k
$$

is a group homomorphism, since $\sigma\tau(\omega)=\sigma(\omega^l)=\omega^{kl}$ , and it is injective, since $k=1$ forces $\sigma=e$ . Hence $G_f$ is isomorphic to a subgroup of $\mathbb{Z}_n^*$ .

By Corollary 4, $|G_f|=[F(\omega):F]$ is the degree of the minimal polynomial of $\omega$ over $F$ , which divides $\Phi_n(x)$ . So $|G_f|=\deg\Phi_n=|\mathbb{Z}_n^*|$ iff $\Phi_n(x)$ is irreducible over $F$ . Over $\mathbb{Q}$ , $\Phi_n(x)$ is irreducible.

</details>

> **Fact 7.** Let $\omega\in F$ and $g(x)=x^n-a$ with $0\neq a\in F$ . Then $G_g$ is a cyclic group of order $m$ with $m\mid n$ , and $G_g$ is cyclic of order $n$ iff $g(x)$ is irreducible over $F$ .

<details>

<summary>Proof</summary>

Let $\alpha$ be one root of $g$ . The roots of $g$ are $\alpha,\alpha\omega,\dots,\alpha\omega^{n-1}$ , distinct since $a\neq0$ , so the splitting field is $E=F(\alpha)$ and $\sigma\in G_g$ is determined by $\sigma(\alpha)=\alpha\omega^k$ . The map

$$
G_g\to\mathbb{Z}_n,\qquad \sigma\mapsto k
$$

is a group homomorphism, since $\sigma$ fixes $\omega$ and $\sigma\tau(\alpha)=\sigma(\alpha\omega^l)=\alpha\omega^{k+l}$ , and it is injective. Hence $G_g$ is isomorphic to a subgroup of the cyclic group $\mathbb{Z}_n$ , i.e. cyclic of order $m\mid n$ .

Under this embedding, $G_g$ moves $\alpha$ to exactly $m$ of the $n$ roots, so $G_g$ is transitive on the roots iff $m=n$ . By Theorem 5, this is iff $g(x)$ is irreducible over $F$ .

</details>

### The General Equation

Let $t_1,\dots,t_n$ be indeterminates over $F$ . The **general equation of degree $n$** is

$$
f(x)=x^n-t_1x^{n-1}+t_2x^{n-2}-\cdots+(-1)^nt_n\in F(t_1,\dots,t_n)[x].
$$

A formula for the roots of a degree-$n$ equation in terms of its coefficients and radicals is the same as a solution of $f$ by radicals over $F(t_1,\dots,t_n)$ .

> **Theorem 8.** $G_f\cong S_n$ .

<details>

<summary>Proof</summary>

Let $x_1,\dots,x_n$ be indeterminates, $K=F(x_1,\dots,x_n)$ , and $s_1,\dots,s_n$ the elementary symmetric polynomials in the $x_i$ , so that

$$
\prod_{i=1}^n(x-x_i)=x^n-s_1x^{n-1}+s_2x^{n-2}-\cdots+(-1)^ns_n .
$$

Then $K$ is the splitting field of this polynomial over $F(s_1,\dots,s_n)$ . Every permutation of $x_1,\dots,x_n$ extends to an automorphism of $K$ fixing $F(s_1,\dots,s_n)$ , so with Theorem 5

$$
S_n\leq\mathrm{Gal}(K/F(s_1,\dots,s_n))\leq S_n .
$$

Since $s_1,\dots,s_n$ are algebraically independent over $F$ , $t_i\mapsto s_i$ is an isomorphism $F(t_1,\dots,t_n)\to F(s_1,\dots,s_n)$ sending $f$ to $\prod(x-x_i)$ . Hence the splitting field of $f$ over $F(t_1,\dots,t_n)$ is isomorphic to $K$ , and $G_f\cong S_n$ .

</details>

## Galois' Theorem on Solvability by Radicals

An extension $K/F$ is a **radical extension** if $K=F(\alpha)$ for some $\alpha$ with $\alpha^n\in F$, i.e. $K$ is obtained from $F$ by adjoining one root $\alpha=\sqrt[n]{a}$ of some $a\in F$. A **radical tower** over $F$ is a tower of fields

$$
F=K_0\subseteq K_1\subseteq\cdots\subseteq K_m,\qquad K_{i+1}=K_i(\alpha_i),\ \alpha_i^{n_i}\in K_i,
$$

in which every step $K_{i+1}/K_i$ is a radical extension. A polynomial $f(x)\in F[x]$ is **solvable by radicals** over $F$ if its splitting field over $F$ is contained in the top field $K_m$ of some radical tower over $F$.

A group $G$ is **solvable** if there is a chain of subgroups

$$
G=G_0\triangleright G_1\triangleright\cdots\triangleright G_m=\{e\}
$$

such that every quotient $G_i/G_{i+1}$ is abelian.

> **Theorem 9. (Galois)** Let $F$ be a field of characteristic $0$ , let $f(x)\in F[x]$ , and let $E$ be the splitting field of $f$ over $F$ . Then $f$ is solvable by radicals over $F$ iff $\mathrm{Gal}(E/F)$ is a solvable group.

### Proof of sufficiency

> **Lemma 10.** Let $p$ be a prime number. Let $F$ be a field whose character is not $p$ or $0$, and $F$ contains $\omega$ such that $\omega^p=1$. Let $E/F$ be a $p$-order Galois extension and $\mathrm{Gal}(E/F)=\langle\sigma\rangle$. Then there exists $z\in E$ such that $E=F(z)$ and $z^p\in F$.

<details>

<summary>Proof</summary>

From Theorem 10.11 we know $E=F(c)$ for some $c\notin F$. Consider

$$
(\omega^i,c)=\sum_{j=0}^{p-1}\omega^{ji}(\sigma^j)c,
$$

where $\sigma\in\mathrm{Gal}(E/F)$ is an $F$-invariant field isomorphism. Notice that

$$
\sigma(1,c)=(1,c)
$$

we know $(1,c)$ is in the invariant field of $\mathrm{Gal}(E/F)$. Since $E/F$ is a Galois extension, we have $(1,c)\in F$. Also, from the character of $F$ we have

$$
\sum_{i=0}^{p-1}(\omega^i,c)=\sum_{j=0}^{p-1}\sum_{i=0}^{p-1}\omega^{ji}(\sigma^j)c=pc\in E\setminus F,
$$

thus there exists $1\leq i\leq p-1$ such that $(\omega^i,c)\neq 0$ (otherwise $pc=(1,c)\in F$). Let $z$ be such $(\omega^i,c)\neq0$,

$$
\sigma(z)=\sum_{j=0}^{p-1}\omega^{(j-1)i}(\sigma^{j})c=\omega^{-1}z
$$

because $\sigma^p$ is identity isomorphism of $E$. Consider $\mathrm{Gal}(E/F(z))\leq\mathrm{Gal}(E/F)$, and we have for every $\sigma^i\in\mathrm{Gal}(E/F)$, $\sigma^i(z)=z$ if and only if $p\mid i$. So we have $\mathrm{Gal}(E/F(z))=\{e\}$. From the fundamental theorem we know $E=F(z)$.

</details>

**Sufficiency.**

Now let $G=\mathrm{Gal}(E/F)$ be solvable and $N=|G|$. We use the fact that in characteristic $0$ every finite extension is separable, so finite normal extensions are Galois. Since $\operatorname{char}F=0$, the roots of $x^N-1$ are distinct and form a cyclic group; let $\omega$ be a generator, i.e. a primitive $N$-th root of unity, and put

$$
F'=F(\omega),\qquad E'=E(\omega).
$$

Then $F'/F$ is a radical extension since $\omega^N=1\in F$, and $E'$ is the splitting field of $f$ over $F'$, so $E'/F'$ is a Galois extension by Corollary 4.

Let $H=\mathrm{Gal}(E'/F')$. Every $\sigma\in H$ fixes $F$ and permutes the roots of $f$, hence $\sigma(E)=E$ and $\sigma|_E\in G$. The restriction $\sigma\mapsto\sigma|_E$ is a group homomorphism $H\to G$, injective because $E'=E(\omega)$ and $\sigma$ fixes $\omega$. So $H$ is isomorphic to a subgroup of $G$, and in particular $|H|$ divides $N$. A subgroup of a solvable group is solvable: if $G=G_0\triangleright\cdots\triangleright G_m=\{e\}$ has abelian quotients, then $H\cap G_{i+1}\triangleleft H\cap G_i$ and $(H\cap G_i)/(H\cap G_{i+1})\hookrightarrow G_i/G_{i+1}$ is abelian. Hence $H$ is solvable.

By Theorem 9.7, the chain of the finite solvable group $H$ can be refined so that every quotient is cyclic of prime order. So we may assume

$$
H=H_0\triangleright H_1\triangleright\cdots\triangleright H_m=\{e\},\qquad H_i/H_{i+1}\cong C_{p_i},\ p_i\text{ prime}.
$$

Put $M_i=\mathrm{Inv}(H_i)$. By Theorem 3 applied to the Galois extension $E'/F'$,

$$
F'=M_0\subseteq M_1\subseteq\cdots\subseteq M_m=E',\qquad \mathrm{Gal}(E'/M_i)=H_i.
$$

Since $E'$ is also the splitting field of $f$ over $M_i$, the extension $E'/M_i$ is Galois with group $H_i$. Apply Theorem 3 to $E'/M_i$: as $H_{i+1}\triangleleft H_i$, the extension $M_{i+1}/M_i$ is normal, hence Galois because $\operatorname{char}F=0$, and

$$
\mathrm{Gal}(M_{i+1}/M_i)\cong H_i/H_{i+1}\cong C_{p_i},\qquad [M_{i+1}:M_i]=p_i.
$$

Finally $p_i$ divides $|H|$, hence $N$, so $\omega^{N/p_i}\in F'\subseteq M_i$ is a primitive $p_i$-th root of unity, and Lemma 10 gives $z_i\in M_{i+1}$ with $M_{i+1}=M_i(z_i)$ and $z_i^{p_i}\in M_i$. Therefore

$$
F\subseteq F(\omega)=M_0\subseteq M_1\subseteq\cdots\subseteq M_m=E'\supseteq E
$$

is a radical tower over $F$ whose top field contains the splitting field $E$ of $f$, i.e. $f$ is solvable by radicals.

### Proof of necessity

> **Lemma 11.** Let $E/F$ be a finite separable extension and $E=K_m$ the top field of a radical tower $F=K_0\subseteq\cdots\subseteq K_m$ , $K_{i+1}=K_i(\alpha_i)$ , $\alpha_i^{n_i}\in K_i$ . Then there is a finite extension $N/E$ such that $N/F$ is Galois and $N$ is the top field of a radical tower over $F$ with the same exponents $n_i$ . (In particular, if every $n_i=2$ , so is the tower for $N$ .)

<details>

<summary>Proof</summary>

Let $N$ be the splitting field over $F$ of the minimal polynomials of $\alpha_0,\dots,\alpha_{m-1}$ . It is finite, normal, and separable since $E/F$ is, hence Galois. Let $\mathrm{Gal}(N/F)=\{\sigma_1,\dots,\sigma_r\}$ . The roots of the minimal polynomial of $\alpha_i$ are exactly the conjugates $\sigma_j(\alpha_i)$ , so

$$
N=F\bigl(\sigma_j(\alpha_i)\ :\ 1\leq j\leq r,\ 0\leq i<m\bigr).
$$

Adjoin these generators one at a time in the order $\sigma_1(\alpha_0),\dots,\sigma_1(\alpha_{m-1}),\ \sigma_2(\alpha_0),\dots,\sigma_r(\alpha_{m-1})$ . When $\sigma_j(\alpha_i)$ is adjoined, the current field $L$ already contains $\sigma_j(\alpha_0),\dots,\sigma_j(\alpha_{i-1})$ , hence $\sigma_j(K_i)$ , and

$$
\sigma_j(\alpha_i)^{n_i}=\sigma_j(\alpha_i^{n_i})\in\sigma_j(K_i)\subseteq L .
$$

So every step is a radical extension with exponent $n_i$ , and the resulting tower from $F$ to $N$ is a radical tower.

</details>

**Necessity.**

Suppose $f$ is solvable by radicals over $F$ . By definition, the splitting field $E$ of $f$ lies in the top field of some radical tower $F=K_0\subseteq\cdots\subseteq K_r$ . This top field need not be normal over $F$ , so we replace the tower: $K_r/F$ is separable since $\operatorname{char}F=0$ , and Lemma 11 gives a radical tower

$$
F=F_0\subseteq F_1\subseteq\cdots\subseteq F_{m+1},\qquad F_{i+1}=F_i(d_i),\quad d_i^{n_i}\in F_i ,
$$

whose top field $F_{m+1}\supseteq K_r\supseteq E$ is Galois over $F$ . Only this tower is used below.

Let $n=n_0n_1\cdots n_m$ . Since $\operatorname{char}F=0$ , $x^n-1$ is separable, so some extension of $F_{m+1}$ contains a primitive $n$-th root of unity $\omega$ . Adjoin $\omega$ at the bottom of the tower:

$$
F\subseteq F_0(\omega)=F(\omega)\subseteq F_1(\omega)\subseteq\cdots\subseteq F_{m+1}(\omega),\qquad F_{i+1}(\omega)=F_i(\omega)(d_i).
$$

$F_{m+1}(\omega)/F$ is Galois: if $F_{m+1}$ is the splitting field of $g$ over $F$ , then $F_{m+1}(\omega)$ is the splitting field of $g(x)(x^n-1)$ , separable since $\operatorname{char}F=0$ (Corollary 4). Every step of the tower is Galois with abelian group:

$$
\mathrm{Gal}(F(\omega)/F)\hookrightarrow\mathbb{Z}_n^*\ \ \text{(Fact 6)},\qquad
\mathrm{Gal}(F_{i+1}(\omega)/F_i(\omega))\ \text{cyclic}\ \ \text{(Fact 7)},
$$

the latter because $d_i^{n_i}\in F_i(\omega)$ , $\omega^{n/n_i}\in F_i(\omega)$ is a primitive $n_i$-th root of unity, and $F_{i+1}(\omega)$ is the splitting field of $x^{n_i}-d_i^{n_i}$ over $F_i(\omega)$ (a step with $d_i=0$ is trivial and may be dropped).

Put $G=\mathrm{Gal}(F_{m+1}(\omega)/F)$ and $G_i=\mathrm{Gal}(F_{m+1}(\omega)/F_i(\omega))$ . Theorem 3, applied to $F_{m+1}(\omega)/F$ and to each $F_{m+1}(\omega)/F_i(\omega)$ , turns the tower into

$$
G\triangleright G_0\triangleright G_1\triangleright\cdots\triangleright G_{m+1}=\{e\},\qquad
G/G_0\cong\mathrm{Gal}(F(\omega)/F),\quad G_i/G_{i+1}\cong\mathrm{Gal}(F_{i+1}(\omega)/F_i(\omega)),
$$

with all quotients abelian, so $G$ is solvable.

Finally $E\subseteq F_{m+1}(\omega)$ and $E/F$ is Galois, so by Theorem 3

$$
\mathrm{Gal}(E/F)\cong G/\mathrm{Gal}(F_{m+1}(\omega)/E).
$$

A quotient $G/K$ of a solvable group is solvable: $G_{i+1}K/K\triangleleft G_iK/K$ , and each quotient $(G_iK/K)/(G_{i+1}K/K)$ is a homomorphic image of $G_i/G_{i+1}$ , hence abelian. Therefore $\mathrm{Gal}(E/F)$ is solvable.
