# Player_Hell Writeup

*June 7, 2026*

*SJTU CTF 2026 线上赛*

## `task.py`

```python
import os
import signal
import sys
import secrets
import sympy
from flag import flag

N = 512
BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def is_prime(n):
    if n < 2:
        return False
    for p in BASES:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in BASES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        ok = False
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                ok = True
                break
        if not ok:
            return False
    return True

def ring_mul(a, b, q):
    r = [0] * N
    for i in range(N):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(N):
            bj = b[j]
            if bj:
                k = (i + j) % N
                r[k] = (r[k] + ai * bj) % q
    return r

def encode(msg):
    v = int.from_bytes(msg, "big")
    out = [0] * N
    for k in range(len(msg) * 8):
        out[N - 1 - k] = (v >> k) & 1
    return out

def main():
    signal.alarm(150)
    print("send q (62 <= bit_length(q) <= 64, is_prime(q) must hold, sympy.isprime(q) must NOT):", flush=True)
    try:
        q = int(sys.stdin.readline().strip())
    except Exception:
        print("bad input")
        return
    if not (62 <= q.bit_length() <= 64):
        print("bit_length out of range")
        return
    if not is_prime(q):
        print("q failed is_prime")
        return
    if sympy.isprime(q):
        print("q is actually prime, not accepted")
        return
    pw = secrets.token_bytes(64)
    s = encode(pw)
    a = [secrets.randbelow(q) for _ in range(N)]
    e = [secrets.randbelow(8) - 4 for _ in range(N)]
    b = [(x + y) % q for x, y in zip(ring_mul(a, s, q), e)]
    print(f"n = {N}")
    print(f"A = {a}")
    print(f"b = {b}")
    sys.stdout.flush()
    print("password (hex)? ", end="", flush=True)
    guess = sys.stdin.readline().strip().lower()
    if guess == pw.hex():
        print(flag)
    else:
        print("wrong")

main()
```

## 思路

服务端给出环

$$
R_q = \mathbb{Z}_q[x] / (x^{512} - 1) \cong \mathbb{Z}_q^{512}
$$

上的 Ring-LWE-like 样本：

$$
a\in R_q,
\quad
b = a \cdot s + e,
\quad\text{where all } s_i \in \{0, 1\},
\quad e_i \in \{-4, -3, \ldots, 3\}.
$$

目标是从公开的 $a, b$ 恢复二进制多项式 $s$ 。环 $\mathbb{Z}_q[x] / (x^{N} - 1)$ 上的多项式 $f(x)=\sum_{i\in [N-1]}a_ix^i$ 在文中也用向量 $\mathbf f=\begin{bmatrix}a_0\\ a_1\\ \vdots\\ a_{N-1}\end{bmatrix}$ 表示。

服务端要求提交一个能通过固定 bases Miller-Rabin、但实际为合数的 $q$, 使用著名强伪素数：

$$
q = 3825123056546413051
= 149491 \cdot 747451 \cdot 34233211.
$$

代码中选择因子 $p = 34233211$ ，因为较小的 $p$ 可以明显加速 LLL，且 $p \mid q$ ，原方程自动投影为：

$$
b = a \cdot s + e \bmod{(p,\ x^{512} - 1)}.
$$

我们不直接恢复 512 个 bit，而是递归计算：

$$
s_1=s \bmod (x - 1)
\rightarrow s_2=s \bmod (x^2 - 1)
\rightarrow \cdots
\rightarrow s_{512}=s \bmod (x^{512} - 1).
$$

注意到 $s_i\in \mathbb Z_q[x]/(x^i-1)$, 因此 $s_i$ 也可以被写作一个 $i$ 维的向量 $\mathbf s_i$ 。且由于 $s=s_{512}$ 是 0-1 系数，有 $\|\mathbf s_{k}\|_\infty\leq\frac{512}{k}$.

## Bootstrap: $\bmod (x - 1)$

模 $x - 1$ ：

$$
b(1) = a(1) \cdot s_1 + e(1) \pmod p.
$$

其中需要满足

$$
-4 \cdot 512 \le e(1) \le 3 \cdot 512.
$$

因此直接枚举 $s_1$ 再检查 $e(1)$ 是否在范围内，就可以恢复 $s_1$ 的值。

## Lift: $\bmod (x^{k} - 1)\to\bmod (x^{2k} - 1)$

假设已经知道

$$
s_k = s \bmod (x^{k} - 1).
$$

目标是恢复下一层的 $s_{2k}=s\pmod{x^{2k}-1}\in\mathbb Z_q^{2k}$, 令 $s_{2k}=\begin{bmatrix} \text{first}\\\text{second} \end{bmatrix}$.

模 $x^{k} - 1$ 时有 $x^{k} = 1$ ，所以

$$
s_k = \text{first} + \text{second}.
$$

模 $x^{k} + 1$ 时有 $x^{k} = -1$ 。我们发现，只要知道

$$
d_k = \text{first} - \text{second}=s_{2k}\bmod {(x^{k}+1)}.
$$

就能求出 $\text{first}, \text{second}$, 进而得到 $s_{2k}$.

这里有 $d_k=s_{2k}\bmod{(x^k+1)}$, 因此要搜索的 $\mathbf d_k$ 满足 $\|\mathbf d_k\|_\infty\leq\frac{512}{2k}$. 不过这样搜索次数仍然是

$$
\sum_{k=1,2,4,\cdots,256}\left(2\cdot\frac{512}{2k}+1\right)^{k}\geq3^{256}
$$

不可接受，于是考虑利用其他关系。

那么 $d_k$ 满足什么关系呢？根据给出的 LWE 方程，有

$$
b_k = a_k \cdot d_k + e_k
\pmod{(p,\ x^{k} + 1)}
$$

其中 $b_k=b\bmod {(x^k+1)},\;e_k=e\bmod {(x^k+1)},\;a_k=a\bmod {(x^k+1)}$. 而模 $x^{k} + 1$ 的乘法是 negacyclic 卷积, 将乘法写成矩阵得

$$
\mathbf b_k =\mathbf A_k \cdot \mathbf d_k +\mathbf e_k \pmod p.
$$

下面我们需要给 $e_k$ 系数一个共同的 bound. 我们有 $e_k=e\bmod {(x^k+1)}=e\bmod {(x^{2k}-1)}\bmod {(x^k+1)}$ ，第一步 $\bmod {(x^{2k}-1)}$ 让每个系数 bound 是原来的 $\frac{512}{2k}$ 倍，因此每个系数都在 $\left[\frac{-4\cdot512}{2k},\frac{3\cdot512}{2k}\right]$ ；第二步是系数相减，因此有

$$
\|\mathbf e_k\|_\infty \le 7 \cdot \frac{512}{2k}.
$$

## Kannan embedding 恢复差分

重写方程

$$
\mathbf b_k =\mathbf A_k \cdot \mathbf x +\mathbf e_k \pmod p.
$$

可以看作是一个 CVP 问题，对于给定格点 $t = \begin{bmatrix}0 \\ b_k\end{bmatrix}$, 求它在格

$$
L = \left\{\begin{bmatrix}\text{SCALE} \cdot \mathbf x \\ \mathbf A \mathbf x + p\mathbf h\end{bmatrix}: \mathbf x \in \mathbb{Z}^n, \mathbf h \in \mathbb{Z}^m\right\}=\mathcal{L}\left(\begin{bmatrix}\text{SCALE} \cdot \mathbf I_n &0\\ \mathbf A &p\mathbf I_m\end{bmatrix}\right)
$$

下的最近向量，然后恢复出 $\mathbf x$.

这里加入 $\text{SCALE}$ 是因为我们还想要约束 $\mathbf x$ 的范数。我们要求的最近向量就是 $\begin{bmatrix}\text{SCALE} \cdot \mathbf d_k \\ \mathbf A \mathbf d_k + p\mathbf h\end{bmatrix}$, 和目标向量相差 $\begin{bmatrix}\text{SCALE} \cdot \mathbf d_k \\ \mathbf e_k\end{bmatrix}$, 因此最好让 $\text{SCALE}=7$. 下面我们仍然保留 $\text{SCALE}$.

对上面的 CVP 问题进行 Kannan 嵌入得到新的格，它的基是：

$$
\mathbf B =
\begin{bmatrix}
\text{SCALE} \cdot \mathbf I_n & 0 & 0 \\
\mathbf A & p \cdot \mathbf I_m & \mathbf b_k \\
0 & 0 & M
\end{bmatrix}.
$$

因此 $L$ 上的 CVP 被转化成了 $\mathcal L(B)$ 上的 SVP (尽管范数并不完全对上).

我们希望这个最短向量是

$$
\mathbf B\begin{bmatrix}
\mathbf d_k\\\mathbf h\\-1
\end{bmatrix}
=\begin{bmatrix}
\text{SCALE}\cdot \mathbf d_k\\\mathbf A\mathbf d_k-p\mathbf h-\mathbf b_k\\-M
\end{bmatrix}
=\begin{bmatrix}
\text{SCALE}\cdot \mathbf d_k\\\mathbf e_k\\-M
\end{bmatrix}.
$$

或者

$$
\mathbf B\begin{bmatrix}
\mathbf -d_k\\\mathbf -h\\1
\end{bmatrix}
=\begin{bmatrix}
-\text{SCALE}\cdot \mathbf d_k\\\mathbf -A\mathbf d_k+p\mathbf h+\mathbf b_k\\M
\end{bmatrix}
=\begin{bmatrix}
-\text{SCALE}\cdot \mathbf d_k\\-\mathbf e_k\\M
\end{bmatrix}.
$$

这样求出 $\mathbf d_k$ 之后，还需要检验 $\text{first}=\frac{\mathbf s_k+\mathbf d_k}2,\text{second}=\frac{\mathbf s_k-\mathbf d_k}2$ 的每个分量是否都在 $\left[0,\frac{512}{2k}\right]$ 里面，且是整数。

然后直接 LLL 计算 SVP 即可。

## 剪枝

若某个 $\mathbf s_k$ 分量为 $0$ 或为 $2 \cdot \frac{512}{2k}$ ，则只能拆成：

$$
0 = 0 + 0,
\qquad
2 \cdot \frac{512}{2k}
= \frac{512}{2k} + \frac{512}{2k}.
$$

对应差分（即 $\mathbf d_k$ 的对应分量）必为 $0$ ，无需求解。

以及可以根据格的维数删掉一些行，让 LLL 更快结束，实测几乎没有得到过不符合要求的解。

剪枝后运行结果

```
x^1 - 1 -> x^2 - 1: 1 variables, 3 dimensions
x^2 - 1 -> x^4 - 1: 2 variables, 5 dimensions
x^4 - 1 -> x^8 - 1: 4 variables, 9 dimensions
x^8 - 1 -> x^16 - 1: 8 variables, 17 dimensions
x^16 - 1 -> x^32 - 1: 16 variables, 33 dimensions
x^32 - 1 -> x^64 - 1: 32 variables, 65 dimensions
x^64 - 1 -> x^128 - 1: 64 variables, 129 dimensions
x^128 - 1 -> x^256 - 1: 117 variables, 185 dimensions
x^256 - 1 -> x^512 - 1: 128 variables, 207 dimensions
```

## `exploit.py`

```python
from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from fpylll import IntegerMatrix, LLL

Q = 3825123056546413051
N = 512

P = 34233211
SCALE = 5
SAMPLE_SLACK = 16
LARGE_LATTICE_THRESHOLD = 192
LARGE_LATTICE_OFFSET = -50

def center_mod(value: int, modulus: int = Q) -> int:
    value %= modulus
    return value - modulus if value > modulus // 2 else value

def ring_mul(a: Sequence[int], b: Sequence[int]) -> List[int]:
    """Multiply in Z_Q[x] / (x^N - 1)."""
    out = [0] * N
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[(i + j) % N] += ai * bj
    return [value % Q for value in out]

def fold(poly: Sequence[int], size: int, modulus: int) -> List[int]:
    """Reduce a polynomial modulo x^size - 1."""
    out = [0] * size
    for i, value in enumerate(poly):
        out[i % size] += value
    return [value % modulus for value in out]

def project_minus(poly: Sequence[int], size: int) -> List[int]:
    """Reduce modulo x^(2*size) - 1 and then map x^size to -1."""
    reduced = fold(poly, 2 * size, P)
    return [(reduced[i] - reduced[i + size]) % P for i in range(size)]

def negacyclic_matrix(poly: Sequence[int]) -> List[List[int]]:
    """Return the matrix for multiplication by poly modulo x^m + 1."""
    size = len(poly)
    return [
        [
            center_mod(
                poly[row - column]
                if row >= column
                else -poly[size + row - column],
                P,
            )
            for column in range(size)
        ]
        for row in range(size)
    ]

def mat_vec_mul(matrix: Sequence[Sequence[int]], vector: Sequence[int]) -> List[int]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]

def build_embedding_basis(
    matrix: Sequence[Sequence[int]],
    target: Sequence[int],
) -> IntegerMatrix:
    """
    Build the Kannan embedding of

        {(SCALE*d, A*d + P*k) : d, k in Z}.
    """
    samples = len(matrix)
    variables = len(matrix[0])
    dimension = variables + samples
    basis = IntegerMatrix(dimension + 1, dimension + 1)

    for variable in range(variables):
        basis[variable, variable] = SCALE
        for sample in range(samples):
            basis[variable, variables + sample] = matrix[sample][variable]

    for sample in range(samples):
        basis[variables + sample, variables + sample] = P

    for column, value in enumerate(target):
        basis[dimension, column] = value
    basis[dimension, dimension] = 1
    return basis

def recover_initial_weight(a: Sequence[int], b: Sequence[int]) -> List[int]:
    a_sum = sum(a) % Q
    b_sum = sum(b) % Q
    candidates = [
        weight
        for weight in range(N + 1)
        if -4 * N <= center_mod(b_sum - a_sum * weight) <= 3 * N
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"expected one initial weight, got {candidates}")
    return candidates

def choose_sample_count(size: int, variables: int) -> int:
    samples = min(size, variables + SAMPLE_SLACK)
    if variables + samples <= LARGE_LATTICE_THRESHOLD:
        return samples
    return min(size, max(1, variables + LARGE_LATTICE_OFFSET))

def decode_split(
    parent: Sequence[int],
    active_columns: Sequence[int],
    active_difference: Sequence[int],
    child_bound: int,
) -> Optional[Tuple[List[int], List[int], List[int]]]:
    """Recover children u, v from parent = u + v and difference = u - v."""
    difference = [0] * len(parent)
    for column, value in zip(active_columns, active_difference):
        difference[column] = value

    first = []
    second = []
    for total, delta in zip(parent, difference):
        if (total + delta) % 2:
            return None
        left = (total + delta) // 2
        right = (total - delta) // 2
        if not (0 <= left <= child_bound and 0 <= right <= child_bound):
            return None
        first.append(left)
        second.append(right)
    return first, second, difference

def recover_difference(
    a: Sequence[int],
    b: Sequence[int],
    parent: Sequence[int],
    size: int,
) -> List[int]:
    """
    Lift s modulo x^size - 1 to s modulo x^(2*size) - 1.

    Projecting modulo x^size + 1 gives a small-secret equation for
    difference = first_half - second_half.
    """
    child_bound = N // (2 * size)
    a_minus = project_minus(a, size)
    b_minus = project_minus(b, size)
    matrix = negacyclic_matrix(a_minus)

    active_columns = [
        column
        for column, total in enumerate(parent)
        if total not in (0, 2 * child_bound)
    ]
    if not active_columns:
        return [value // 2 for value in parent] * 2

    samples = choose_sample_count(size, len(active_columns))
    reduced_matrix = [
        [matrix[row][column] for column in active_columns]
        for row in range(samples)
    ]
    target = (
        [0] * len(active_columns)
        + [center_mod(value, P) for value in b_minus[:samples]]
    )

    basis = build_embedding_basis(reduced_matrix, target)
    LLL.reduction(basis, delta=0.99)

    for row in basis:
        if abs(row[-1]) != 1:
            continue
        sign = -1 if row[-1] > 0 else 1
        scaled_difference = [
            sign * row[column]
            for column in range(len(active_columns))
        ]
        if any(value % SCALE for value in scaled_difference):
            continue

        split = decode_split(
            parent,
            active_columns,
            [value // SCALE for value in scaled_difference],
            child_bound,
        )
        if split is None:
            continue

        first, second, difference = split
        residual = [
            center_mod(rhs - lhs, P)
            for rhs, lhs in zip(b_minus, mat_vec_mul(matrix, difference))
        ]
        if all(abs(value) <= 7 * child_bound for value in residual):
            print(
                f"x^{size} - 1 -> x^{2 * size} - 1: "
                f"{len(active_columns)} variables, {basis.nrows} dimensions"
            )
            return first + second

    raise RuntimeError("Kannan embedding did not produce a valid split")

def solve(a: Sequence[int], b: Sequence[int]) -> Tuple[List[int], List[int]]:
    """Recover the binary secret s and the original error e."""
    if len(a) != N or len(b) != N:
        raise ValueError(f"a and b must each contain {N} coefficients")

    secret = recover_initial_weight(a, b)
    size = 1
    while size < N:
        secret = recover_difference(a, b, secret, size)
        size *= 2

    error = [
        center_mod(rhs - lhs)
        for rhs, lhs in zip(b, ring_mul(a, secret))
    ]
    if any(value < -4 or value > 3 for value in error):
        raise RuntimeError("recovered secret does not reproduce a valid error")
    return secret, error
```
