# Untyped Lambda Calculus

*June 24, 2024*

## Lambda Terms

An intuitive thought: for $x$, $x^2+1$ can be a function or merely a number.

Thus we distinguish them, by denoting the function by $\lambda x.x^2+1$.

***Definition 1.*** Let $V$ be an infinite variable set $\{x,y,z,\dots\}$, $\Lambda$ be a set of Lambda terms.

(1) If $u\in V$, then $u\in \Lambda$.

(2)(juxtaposition for application) If $M,N\in \Lambda$, then $(M\;N)\in\Lambda$.

(3) If $x\in V$, $N\in \Lambda$, then $(\lambda x.N)\in\Lambda$.

Or in short, $\Lambda=V|(\Lambda\Lambda)|(\lambda V.\Lambda)$.

***Definition 2.*** Subterms.

(1) $\text{Sub}(x)=\{x\}$, for $x\in V$

(2) $\text{Sub}(M\;N)=\text{Sub}(M)\cup\text{Sub}(N)\cup\{(M\;N)\}$

(3) $\text{Sub}(\lambda x.M)=\text{Sub}(M)\cup\{(\lambda x.M)\}$

proper: sub but not $\equiv$.

**Reflexivity and Transitivity**

$\equiv$ says that two $\lambda$ -terms are exactly the same.

Tree of $(y(\lambda x.(xz)))$

(a: application, l: lambda)

```
  y
 /
a     x
 \   /
  l-a
     \
      z

```

***Notation 3.***

- It's recommended that you should not omit the parentheses.

- Application is left-associative, with $MNL$ denoting $((MN)L)$

- Abstruction is right-associative, with $\lambda xy.M$ denoting $(\lambda x.(\lambda y.M))$

- Application takes precedence over abstraction, with $\lambda x. MN$ denoting $\lambda x.(MN)$

***Definition 4.*** $FV(·)$

(1) $FV(x)=\{x\}$

(2) $FV(MN)=FV(M)\cup FV(N)$

(3) $FV(\lambda x.M)=FV(M)\setminus\{x\}$

## $\alpha$ -Substitution

***Definition 5.*** $=_\alpha$, or in modulo $\alpha$, $\equiv$

$x[x:=N]\equiv N$

To be noticed especially, $[\lambda y.M](x:=N)\equiv\lambda z.(M[y:=z][x:=N])$, where $z\notin FV(N)$.

Besides, $L[x:=M][y:=N]\equiv L[y:=N][x:=M[y:=N]]$ **when $x\notin FV(N)$ **

$=_\alpha$ implies a *renaming* of bound variables and an isoporphism between expression trees.

## $\beta$ -Reduction

***Definition 6.*** $\to_\beta$, one-step reduction (1) $(\lambda x.M)N\to_\beta M[x:=N]$ (2) (Compatibility) $M\to_\beta N$ implies that $ML\to_\beta NL$, $LM\to_\beta LN$, $\lambda x.M\to_\beta\lambda x.N$

$(\lambda x.M)N$ is called a *reducible expression*, or a *redex*; $M[x:=N]$ is called a *contractum* of the redex.

***Definition 7.*** $\twoheadrightarrow_{\beta}$, zero- or multi-step reduction

$M\equiv M_0\to_\beta M_1\to_\beta\dots\to_\beta M_n\equiv N$

Reflexive and Transitive

***Definition 8.*** $\beta$ -equality, $=_\beta$

$M\equiv M_0-_\beta M_1-_\beta\dots-_\beta M_n\equiv N$

with the arrows either leftwards or rightwards.

***Example 9.*** $(\lambda x.xy)z\to_\beta zy\leftarrow_\beta (\lambda x.zx)y$

$=_\beta$ is an equivalence relation.

***Definition 10.*** $\beta$ -normal form

(1) $M$ is in $\beta$ -normal form if $M$ has no redex.

(2) $M$ is $\beta$ -normalizable if there exists $N$ such that $M\twoheadrightarrow_\beta N$ and $N$ is in $\beta$ -normal form.

***Lemma 11.*** If $M$ is in $\beta$ -normal form, then $M\twoheadrightarrow_\beta N$ implies $M\equiv N$.

***Astounding Example*** "Reduction"

Let $N=\lambda x.xxx$. $NN\to_\beta NNN\to_\beta\dots$, an infinite reduction path.

Let $M=(\lambda u.v)((\lambda x.xx)(\lambda x.xx))$. From one hand, reducing $\lambda u.v$ first yields $v$. From the other hand, reducing $(\lambda x.xx)(\lambda x.xx)$ first yields $(\lambda x.xx)(\lambda x.xx)$.

Thus $M$ has both a $\beta$ -normal form and an infinite reduction path.

***Definition 12.*** A $\lambda$ -term $M$ is

(1) weakly normalising, if there is an $N$ such that $M\twoheadrightarrow_\beta N$ and $N$ is in $\beta$ -normal form.

(2) strongly normalising, if every reduction path starting from $M$ is finite.

$M$ is weakly normalising. And since the reductiong cannot go on indefinitely, strong->weak.

***Theorem 13.(Church-Rosser)*** If $M\twoheadrightarrow_\beta N_1$ and $M\twoheadrightarrow_\beta N_2$, then there is a $\lambda$ -term L s.t. $N_1\twoheadrightarrow_\beta L$ and $N_2\twoheadrightarrow_\beta L$.

(For a given group $G$, if $N_1\lhd G,N_2\lhd G$ then $N_1\lhd N_1N_2$ and $N_1\cap N_2\lhd N_2\lhd G$.)

***Corollary 14.*** If $M=_\beta N$ then there is $L$ s.t. $M\twoheadrightarrow_\beta L$ and $N\twoheadrightarrow_\beta L$.

**(induction on the length of the reduction path, using CR Thm)**

## Fixed Point Thms

***Theorem 15.*** (Fixed Point Thm) For any $\lambda$ -term $F$, there is a $\lambda$ -term $X$ s.t. $X=_\beta FX$.

***Proof.*** Take $X\equiv(\lambda x.F(xx))(\lambda x.F(xx))\to_\beta F(\lambda x.F(xx))(\lambda x.F(xx))\equiv FX$.

$X\equiv(\lambda x.F(xx))(\lambda x.F(xx))\leftarrow_\beta \lambda y.(\lambda x.y(xx))(\lambda x.y(xx))F:\equiv LF$

Thus $LF\to_\beta X\to_\beta FX\leftarrow_\beta FLF$, and $LF=_\beta FLF$.

Key: Make $X$ into sth. like $X=_\beta\dots X\dots$, and let $L=\lambda u.\dots u\dots$

We have $Y$ -combiantor

$$
L\equiv\lambda f.(\lambda x.f(xx))(\lambda x.f(xx))\equiv\lambda f.(\lambda x.xx)(\lambda x.f(xx))
$$

, s.t. $LF=_\beta F(LF)$ is the fixed point of $F$.

A demo for factorial:

```cpp
void f(int n, const std::function<int(int)> &g) {
    cout << g(n) << endl;
}

int main() {
    f(10, [](const auto &f) {
        return [&](const auto &x) {
            return x(x);
        }([&](const auto &x) -> std::function<int(int)> {
            return f([&](const int &n) {
                return x(x)(n);
            });
        });
    }([](const auto &f) {
        return [=](const int &n) {
            return n == 0 ? 1 : 2 * f(n - 1) + 3 ;
        };
    }));
    return 0;
}
```

---
