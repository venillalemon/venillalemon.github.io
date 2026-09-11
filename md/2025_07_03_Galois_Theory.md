# Galois Theory

A short path 

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

### Exercises

- 1 Let $E$ be a quadratic extension of $F$ and suppose that the characteristic of $F$ is not 2. Prove that $E/F$ is a Galois extension and that there exists $a \in E$ such that $a^2 \in F$ and $E = F(a)$ . Conclude that the complex number field $\mathbb{C}$ has no quadratic extensions.
- 2 Let $E = \mathbb{Q}(\alpha)$ , where $\mathbb{Q}$ is the field of rational numbers and $\alpha$ is a root of $f(x) = x^3 + x^2 - 2x - 1$ . Show that $\alpha^2 - 2$ is also a root of $f(x)$ and that $E/\mathbb{Q}$ is a finite Galois extension.
- 3 Let $F$ be a field of characteristic $p$ , and let $f(x) = x^p - x - c \in F[x]$ be irreducible. Let $E$ be the splitting field of $f(x)$ over $F$ . Determine the Galois group $\text{Gal}(E/F)$ .
- 4 Let $E/F$ be a finite Galois extension, let $G = \text{Gal}(E/F)$ , and let $\alpha \in E$ . Let $G\alpha = \{\alpha_1 = \alpha, \dots, \alpha_r\}$ be the orbit of $\alpha$ under $G$ . Prove that the minimal polynomial of $\alpha$ over $F$ is $\prod_{i=1}^r (x - \alpha_i)$ .
- 5 Let $f_1, \dots, f_n$ be distinct monomorphisms from a field $F$ to a field $K$ . Prove that $f_1, \dots, f_n$ are linearly independent over $K$ . (Hint: Use Dedekind's independence lemma.)
- 6 Let $E/F$ be a finite extension of fields and let $K/F$ be a field extension. Prove that the number of $F$ -embeddings from $E$ into $K$ (i.e., monomorphisms $E \to K$ fixing $F$ pointwise) does not exceed $[E : F]$ . (Hint: Use the previous exercise and the method of proving Proposition 1.4.)
- 7 Prove the Normal Basis Theorem: If $E/F$ is a finite Galois extension, then there exists an element $a \in E$ such that $\{\sigma(a) \mid \sigma \in \text{Gal}(E/F)\}$ is an $F$ -basis of $E$ . (Hint: Use Theorem 10.11 in Appendix II and Dedekind's independence lemma.)
- 8 Find a normal basis for $\mathbb{Q}(\sqrt{2}, \sqrt{3})/\mathbb{Q}$ .
- 9 (Artin's Theorem) Let $G$ be a finite subgroup of the automorphism group of a field $E$ , and let $F = \text{Inv}(G)$ . Prove that $E/F$ is a finite Galois extension and that $\text{Gal}(E/F) = G$ . (Hint: Use Lemma 1.2, Proposition 1.4, and Theorem 1.5.)
- 10 Let $E/F$ be a finite extension of fields. Prove that $|\text{Gal}(E/F)|$ divides $[E : F]$ . (Hint: Use the previous exercise.)
- 11 Let $E/F$ be a finite extension of fields. Prove that $E/F$ is a normal extension if and only if every irreducible polynomial $f(x) \in F[x]$ has all its irreducible factors in $E[x]$ of the same degree. (Hint: Use the isomorphism extension theorem.)

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

We have the following fact from the proof of the fundamental theorem:

> **Corollary 4.** Let $E/F$ be a field extension. **FAE** :
> 
> - $E/F$ is a finite separable normal extension (i.e. Galois extension)
> - $E$ is a separation field of a separable polynomial over $F$
> - $E/F$ is finite and $|\mathrm{Gal}(E/F)|=[E:F]$
> - $G=\mathrm{Gal}(E/F)$ is a finite group and $\mathrm{Inv}(\mathrm{Gal}(E/F))=F$

In fact, every finite extension of a finite field is a Galois extension. This is because $\mathbb{F}_{p^n}$ is the separation field of $x^{p^n}-x$ over $\mathbb{F}_p$ .

Consider $E=\mathbb{F}_{p^n}$ and $F=\mathbb{F}_p$ , we have $E=F(u)$ , and the Frobenius automorphism $\sigma(u)=u^p$ . Thus the Galois group $\mathrm{Gal}(\mathbb{F}_{p^n}/\mathbb{F}_p)\cong C_n=\langle\sigma\rangle$ . Below are examples.

- **Example.** The structure of $G=\mathrm{Gal}(E/F)$ where $E$ is the separation field of $x^5-4$ on $F=\mathbb{Q}$ .
    
    We have $E=\mathbb{Q}(a=\sqrt[5]{4},\omega=e^{\frac{2\pi i}{5}})$ and $|\mathrm{Gal}(E/F)|=[E:F]=[\mathbb{Q}(a)(\omega):\mathbb{Q}(\omega)][\mathbb{Q}(\omega):\mathbb{Q}] = 5\times 4 = 20$ . Since $E$ is a linear space over $F$ , every operation in $\mathrm{Gal}(E/F)$ is uniquely determined by its transformation on $a$ and $i$ .
    
    Consider $\sigma:a\mapsto a,\omega\mapsto\omega^2$ and $\tau=a\mapsto a\omega,\omega\mapsto\omega$ where $\sigma^4=\tau^5=e$ . A way to conpute the group is to use the free group notation with restrictions $\tau^2\sigma=\sigma\tau$ , but we will not do this chore.
    
    Consider $M=F(\omega)$ be an intermediate field, which is a normal extension. Thus $\mathrm{Gal}(E/M)=\langle\tau\rangle\cong C_5$ is a normal subgroup of $\mathrm{Gal}(E/F)$ . (Also a conclusion from Sylow theorems)
    
    Also we have 4-order element, so $\langle \sigma\rangle\cong C_4$ is also a subgroup of $\mathrm{Gal}(E/F)$ . From Sylow theorems, we have the number of the 4-order subgroup $n_2=1\text{ or }5$ .
    
    Then we have $\tau^{-1}\sigma\tau=\tau\sigma$ , thus $\tau^{-1}\sigma^2\tau=\tau^{3}\sigma^2\neq e$ , and $\tau^{-1}\sigma^3\tau=\tau^{2}\sigma^3$ , $\tau^{-1}\sigma^4\tau=\tau^{15}\sigma^4=e$ , so $n_2=5$ .
    
    Consider the 4-order group $G/\langle\tau\rangle$ , which is either $C_4$ or $C_2\times C_2$ .
    

### Exercises

- 1 Let $E/F$ be a finite Galois extension, let $M$ be an intermediate field, let $G = \text{Gal}(E/F)$ , and let $H = \text{Gal}(E/M)$ . Prove that the number of intermediate fields conjugate to $M$ equals $[G : N_G(H)]$ , where $N_G(H)$ is the normalizer of $H$ in $G$ .
- 2 Let $E/F$ be a finite Galois extension with $\text{Gal}(E/F) = A_n$ (the alternating group), $n \geq 4$ . Prove that there is no intermediate field $L$ of $E/F$ such that $[L : F] = 2$ .
- 3 Let $E/F$ be a finite Galois extension and let $p$ be a prime dividing $[E : F]$ . Prove that there exists an intermediate field $L$ of $E/F$ such that $[E : L] = p$ .
- 4 Let $E/F$ be a finite Galois extension. Suppose that for every field $K$ with $F \subsetneq K \subseteq E$ , the extension degree $[K : F]$ is the same. Prove that $[E : F]$ is prime.
- 5 Let $E/F$ be a finite Galois extension with $\text{char}(F) \neq 2$ and $\text{Gal}(E/F) \cong \mathbb{Z}_2 \oplus \mathbb{Z}_2$ . Prove that $E = F(\sqrt{a}, \sqrt{b})$ for some $a, b \in F$ .
- 6 Let $E/F$ be a finite Galois extension. Suppose that $\text{Gal}(E/F)$ is a non-abelian group of order $2p$ where $p$ is an odd prime, and let $L$ be an intermediate field such that $[E : L] = 2$ . Prove that $L/F$ is not a finite Galois extension.
- 7 Write down the Galois correspondence for $E/\mathbb{Q}$ , where $E$ is the splitting field of $x^3 - 3$ over $\mathbb{Q}$ .
- 8 Write down the Galois correspondence for $\mathbb{F}_{2^8}/\mathbb{F}_2$ .
- 9 Let $E = \mathbb{C}(t)$ (the field of rational functions over the complex numbers) and $F = \mathbb{C}(t^3 + t^{-3})$ . Find all intermediate fields of $E/F$ .
- 10 Let $F$ be a field of prime characteristic $p$ , let $E = F(t)$ (the field of rational functions over $F$ ), and let $K = F(t^p - t - 1)$ . Find $\mathrm{Inv}(\mathrm{Gal}(E/K))$ .
- 11 Let $N$ and $M$ be intermediate fields of a finite Galois extension $E/F$ , and suppose that $N$ is the normal closure of $M$ over $F$ (i.e., $N$ is the smallest normal extension of $F$ containing $M$ ). Prove that $\text{Gal}(E/N) = \bigcap_{\sigma \in \text{Gal}(E/F)} \sigma \,\text{Gal}(E/M) \,\sigma^{-1}$ .
- 12 Let $L$ and $M$ be subfields of a field $E$ and suppose that $L/(L \cap M)$ is a finite Galois extension. Prove that $LM/M$ is also a finite Galois extension and that $\text{Gal}(LM/M) \cong \text{Gal}(L/(L \cap M))$ . (Hint: See [FZ] 4.1.8.)

## Galois Groups of Formulas

We say a subgroup $G$ of $S_n$ a **transitive subgroup** if for every pair $(i,j)\in[n]\times[n]$ , there exists $\sigma\in G$ such that $\sigma(i)=j$ . Here is the main theorem concerning the Galois groups of separation fields.

> **Theorem 4.** Let $f(x)\in F[x]$ be a polynomial of degree $n$ and no multiple roots; and let $E$ be the separation field of $f$ over $F$ . Let $S_n$ be the symmetric group of the $n$ roots $r_1,\dots,r_n$ of $f$ . Then
> 
> - $G_f=\mathrm{Gal}(E/F)$ is a subgroup of $S_n$ whose order is $[E:F]$ .
> - An element $\sigma\in S_n$ belongs to $G_f$ iff $\sigma$ reserves all the algebraic relations of all roots, i.e. if $g(r_1,\dots,r_n)=0$ then $g(\sigma(r_1),\dots,\sigma(r_n))=0$ .
> - $f$ is irreducible on $F$ iff $G_f$ is a transitive subgroup of $S_n$ .