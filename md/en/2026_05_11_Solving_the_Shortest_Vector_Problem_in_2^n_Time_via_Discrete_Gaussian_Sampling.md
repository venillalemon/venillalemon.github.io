# Solving the Shortest Vector Problem in 2^n Time via Discrete Gaussian Sampling

*May 11, 2026*

*May 11, 2026*

A reading notes of [ADRS14](https://arxiv.org/pdf/1412.7994)

The main result of the paper: there is an algorithm that, in $2^{n+o(n)}$ time and space, outputs $2^{n/2}$ i.i.d. samples from the discrete Gaussian distribution $D_{L,s}$ over a lattice $L$.

If $s$ is larger than the smoothing parameter, the above time and space complexity becomes $2^{n/2+o(n)}$ .

## Intuition

Given some number of $D_{L,s}$ samples, we want to produce some number of $D_{L,s/2}$ samples (in any case the variance has to shrink by a constant factor, which helps us sample short vectors). For a continuous Gaussian this is easy: sample and divide by $2$ ; but in a lattice, this first requires getting lucky and hitting a vector in $2L$, which happens with probability $\frac{\rho_s(2L)}{\rho_s(L)}$ , and when $s$ is large this is almost $2^{-n}$ .

So we take a different approach: after obtaining many $D_{L,s}$ samples, we bucket them by cosets of $L/2L$, and let vectors that agree $\bmod 2L$ cancel each other. Below, $c\in\{0,1\}^n$ denotes the coset $Bc+2L$ , and we study the distribution of the resulting samples. A sample lies in coset $c$ with probability $\rho_s(c):=\sum_{x\in 2L}\rho_s(Bc+x)$ , so if we have many samples and pair them up within each bucket to form samples of the form $(X,Y)$, the number of samples in coset $c$ is proportional to $\rho_s(c)$ . Then we compute all $\frac{X+Y}{2}$ , hoping the resulting samples follow $D_{L,s/\sqrt{2}}$ .

Look at it again: suppose we independently pick $x,y\sim D_{L,s}$ at random and then do rejection sampling, i.e. discard the cases where $x,y$ lie in different cosets. Then the distribution of $(x+y)/2$ is

$$
\Pr_{X,Y\sim D_{L,s}}\left[\frac{X+Y}{2}=z \mid X\equiv Y\bmod 2L\right]=\Pr_{Z\sim D_{L,s/\sqrt{2}}}[Z=z]
$$

This identity is easy to understand. Consider the sublattice

$$
\overline L=\left\{(x,y):x\equiv y\bmod 2L\right\}\subset L^2
$$

Since $X,Y$ are i.i.d., the joint distribution of $(X,Y)$ is $D_{L^2,s}$ , so the conditional distribution $(X,Y)| X\equiv Y\bmod 2L$ still has parameter $s$, i.e. it follows $D_{\overline L,s}$ . Then apply the rotation to $\overline L\subset L^2$

$$
\sigma:(x,y)\mapsto \left(\frac{x+y}{\sqrt{2}},\frac{x-y}{\sqrt{2}}\right)
$$

The resulting lattice is

$$
\sigma(\overline L)=(\sqrt{2}L)^2.
$$

Hence $\left(\frac{X+Y}{\sqrt{2}},\frac{X-Y}{\sqrt{2}}\right)\sim D_{(\sqrt{2}L)^2,s}$ , and by the properties of the Gaussian, taking the marginal gives

$$
\frac{X+Y}{2}\sim D_{L,s/\sqrt{2}}
$$

Now we know that if we apply rejection sampling to $(X,Y)\sim D_{L^2,s}$ , the resulting $\frac{X+Y}{2}$ follows the distribution we need. In other words, if I can get many samples $(X,Y)$ where the number of samples in coset $c$ is proportional to $\rho_s(c)^2$ , then taking these samples and computing $\frac{X+Y}{2}$ yields something distributed as $D_{L,s/\sqrt{2}}$ .

This differs from the greedy pairing above, where the number of samples in coset $c$ is proportional to $\rho_s(c)$ . An obvious improvement is to not pair them up two by two, but pair each sample with all other samples; but then the number of samples becomes quadratic, going from $N$ to $N^2\sum_c\rho_s^2(c)$ .

## Square Sampler

As said above, we can sample so that the fraction of $(x,y)$ corresponding to a given $c$ among all samples is $\rho_s(c)$. Based on this we need to turn this probability into $\rho_s^2(c)$. Let us abstract a bit: label each $c$ by $1\dots N$, since sampling them works the same way anyway. Suppose each label has probability $p_i$ ; our idea is to do rejection sampling on the labels, i.e. traverse the sample sequence again, and whenever we see this label, select it with probability $p_i$ . There are two problems:

- Here $N\sim 2^n$ , so we would need to sacrifice a huge number of samples to estimate each $p_i$

- If the distribution is very uniform, the sampling produces very few samples. For example, if every label has probability $\frac{1}{N}$ then on average we need about $N^2=2^{2n}$ samples to produce one.

So we need to do rejection sampling with probability **proportional to** $p_i$ ; the best way is to estimate the maximum of these probabilities, $p_{\max}=\max_i{p_i}$ ; at the same time we use properties of the Poisson distribution to record each element's probability information in variables. The following theorem is for estimating $p_{\max}$ ; proof omitted.

Proposition 3.1 — Estimating p_max

There is an algorithm that takes as input $\kappa \ge 1$ (the confidence parameter) and a sequence of $M$ elements from $\{1,\dots,N\}$ and outputs a value $\tilde p_{\max}$ such that, if the input consists of $M \ge \kappa/p_{\max}$ independent samples from the distribution that assigns probability $p_i$ to element $i$, then

$$
p_{\max} \;\le\; \tilde p_{\max} \;\le\; 4 p_{\max}
$$

except with probability at most $C_1 N \log N \exp(-C_2\kappa)$, where $p_{\max} = \max p_i$. The algorithm runs in time $M \cdot \operatorname{poly}(\log \kappa, \log N)$.

Theorem 3.3 is the core theorem.

Theorem 3.3 — Square sampler

There is an algorithm that takes as input $\kappa \ge 2$ (the confidence parameter) and $M$ elements from $\{1,\dots,N\}$ and outputs a sequence of elements from the same set such that

1. the running time is $M \cdot \operatorname{poly}(\log \kappa, \log N)$;

2. each $i \in \{1,\dots,N\}$ appears at least twice as often in the input as in the output; and

3. if the input consists of $M \ge 10\kappa^2 / \max p_i$ independent samples from the distribution that assigns probability $p_i$ to element $i$, then the output is within statistical distance $C_1 M N \log N \exp(-C_2 \kappa)$ of $m$ independent samples with respective probabilities $\mathbf{p}^2$, where $m \ge M \cdot \sum_i p_i^2 / (32 \kappa \max p_i)$ is a random variable.

<details>

<summary>Proof</summary>

The algorithm first runs the procedure from Proposition 3.1 on the first $M/2$ elements from its input sequence, receiving as output $\tilde p_{\max}$. The algorithm then reads the remaining elements in sequence. If it ever reads the last element of the input, it fails. For $j = 1,\dots,M\tilde p_{\max}/4$, the algorithm samples $r$ according to $\operatorname{Pois}(1/\tilde p_{\max})$ and takes the next $r$ unused elements in the input. For $i = 1,\dots,N$, let $a_{i,j}$ be the number of times element $i$ appears in the $j$th such subsequence. For each $i,j$ let $b_{i,j}$ be $1$ with probability $\min\{1,\, a_{i,j}/\kappa\}$ and $0$ otherwise. (To achieve the correct running time, we do not actually explicitly store these values when $a_{i,j} = b_{i,j} = 0$.)

Finally, the algorithm looks through the next $M/6$ elements, one element at a time (or it fails if there are not $M/6$ elements remaining). When it sees element $i$, it adds it to its output if $b_{i,j} = 1$ where $j \ge 1$ is the smallest index such that $b_{i,j}$ is unused (or it fails if there is no unused $b_{i,j}$). $\square$

</details>

An intuitive reading of this: the length $r$ is $\frac{1}{\tilde{p}_{\max}}$ on average, and by properties of the Poisson distribution we get that $a_{ij}$ follows $\mathrm{Pois}\left(\frac{p_i}{\tilde{p}_{\max}}\right)$ (Lemma 2.22). Then roughly speaking, $b_{ij}$ follows a $\mathrm{B}\left(\frac{p_i}{\kappa \tilde{p}_{\max}}\right)$ distribution (Lemma 2.23). So in the last step, each time a sample is read, it is $i$ with probability $p_i$ , and then enters the final output with probability approximately $\frac{p_i}{\kappa \tilde{p}_{\max}}$ , so the final distribution is $p_i^*=\frac{p_i^2}{\kappa \tilde{p}_{\max}}$ , and we get $\frac{M\sum_ip_i^2}{6\kappa \tilde{p}_{\max}}$ samples in expectation; finally apply a Hoeffding bound.

One more key point: why bother with many $a_{ij},b_{ij}$ when they are all i.i.d.? Because we cannot sample directly from the distribution; they serve only as coins.

## Gaussian Combiner

A lemma

Lemma 3.4

Let $\mathcal{L} \subset \mathbb{R}^n$ and $s > 0$. Then for all $\mathbf{y} \in \mathcal{L}$,

$$
\Pr_{(\mathbf{X}_1,\mathbf{X}_2)\sim D^2_{\mathcal{L},s}} \big[(\mathbf{X}_1+\mathbf{X}_2)/2 = \mathbf{y} \;\big|\; \mathbf{X}_1+\mathbf{X}_2 \in 2\mathcal{L}\big] = \Pr_{\mathbf{X}\sim D_{\mathcal{L},s/\sqrt{2}}}\big[\mathbf{X} = \mathbf{y}\big].
$$

Furthermore,

$$
\sum_{\mathbf{c}\in\mathcal{L}/(2\mathcal{L})} \rho_s(\mathbf{c})^2 = \rho_{s/\sqrt{2}}(\mathcal{L})^2.
$$

Next we replace the sampling set $\{1,\dots, N\}$ of Theorem 3.3 with $L/2L=\{c_1,\dots,c_{2^n}\}$. Then $p_i=\frac{\rho_s(c_i)}{\rho_s(L)}$ ; note that here $c$ stands for a coset $c+2L$ ; we have $p_{\max}=\frac{\rho_s(2L)}{\rho_s(L)}$ (fairly obvious).

So we only need to check that the conditions of Theorem 3.3 hold; one can then compute that the required precondition is $M\geq \frac{10\kappa^2\rho_s(L)}{\rho_s(2L)}$ , and the total number of samples obtained is $m\geq M\frac{\rho_s(L)\sum_i\rho_s^2(c_i)}{32\kappa\rho_s(2L)\rho_s^2(L)}=M\frac{\sum_i\rho_s^2(c_i)}{32\kappa\rho_s(2L)\rho_s(L)}$ ; by Lemma 3.4 we have $m\geq M\frac{\rho_{s/\sqrt{2}}^2(L)}{32\kappa\rho_s(2L)\rho_s(L)}$ .

Proposition 3.5

There is an algorithm that takes as input a lattice $\mathcal{L} \subset \mathbb{R}^n$, $\kappa \ge 2$ (the confidence parameter), and a sequence of vectors from $\mathcal{L}$, and outputs a sequence of vectors from $\mathcal{L}$ such that, if the input consists of $M \ge 10\kappa^2 \cdot \rho_s(\mathcal{L})/\rho_s(2\mathcal{L})$ independent samples from $D_{\mathcal{L},s}$ for some $s > 0$, then the output is within statistical distance $M\exp(C_1 n - C_2 \kappa)$ of $m$ independent samples from $D_{\mathcal{L},s/\sqrt{2}}$ where $m$ is a random variable with

$$
m \;\ge\; M \cdot \frac{1}{32\kappa} \cdot \frac{\rho_{s/\sqrt{2}}(\mathcal{L})^2}{\rho_s(\mathcal{L})\,\rho_s(2\mathcal{L})}.
$$

The running time of the algorithm is at most $M \cdot \operatorname{poly}(n, \log \kappa)$.

Note that here we first extract the coset information from the original samples, then do square sampling on the cosets (note that the resulting samples all come from the original samples). Then we traverse the square-sampled output and find samples in the same coset (taken from the original samples) to cancel.

<details>

<summary>Proof of Proposition 3.5</summary>

Let $(\mathbf{X}_1,\dots,\mathbf{X}_M)$ be the input vectors. For each $i$, let $\mathbf{c}_i \in \mathcal{L}/(2\mathcal{L})$ be the coset of $\mathbf{X}_i$. The combiner runs the algorithm from Theorem 3.3 with input $\kappa$ and $(\mathbf{c}_1,\dots,\mathbf{c}_M)$, receiving output $(\mathbf{c}'_1,\dots,\mathbf{c}'_m)$. (Formally, we must encode the cosets as integers in $\{1,\dots,2^n\}$.) Finally, for each $\mathbf{c}'_i$, it chooses a pair of unpaired vectors $\mathbf{X}_j, \mathbf{X}_k$ with $\mathbf{c}_j = \mathbf{c}_k = \mathbf{c}'_i$ and outputs $\mathbf{Y}_i = (\mathbf{X}_j + \mathbf{X}_k)/2$.

The running time of the algorithm follows from Item 1 of Theorem 3.3. Furthermore, we note that by Item 2 of the same theorem, there will always be a pair of indices $j,k$ for each $i$ as above.

To prove correctness, we observe that for $\mathbf{c} \in \mathcal{L}/(2\mathcal{L})$ and $\mathbf{y} \in \mathbf{c}$,

$$
\Pr[\mathbf{X}_i = \mathbf{y}] = \frac{\rho_s(\mathbf{c})}{\rho_s(\mathcal{L})} \cdot \Pr_{\mathbf{X}\sim D_{\mathbf{c},s}}[\mathbf{X} = \mathbf{y}].
$$

In particular, we have that $\Pr[\mathbf{c}_i = \mathbf{c}] = \rho_s(\mathbf{c})/\rho_s(\mathcal{L})$, and $2\mathcal{L}$ is the coset with the highest probability. Then, the cosets $(\mathbf{c}_1,\dots,\mathbf{c}_M)$ satisfy the conditions necessary for Item 3 of Theorem 3.3 with $\max p_i = \rho_s(2\mathcal{L})/\rho_s(\mathcal{L})$.

Applying the theorem, up to statistical distance $M\exp(C_1 n - C_2\kappa)$, we have that the output vectors are independent, and

$$
m \;\ge\; M \cdot \frac{1}{32\kappa} \cdot \frac{\sum_{\mathbf{c}\in\mathcal{L}/(2\mathcal{L})}\rho_s(\mathbf{c})^2} {\rho_s(\mathcal{L})\rho_s(2\mathcal{L})} \;=\; M \cdot \frac{1}{32\kappa} \cdot \frac{\rho_{s/\sqrt{2}}(\mathcal{L})^2}{\rho_s(\mathcal{L})\rho_s(2\mathcal{L})},
$$

where the equality follows from Lemma 3.4. Furthermore, we have $\Pr[\mathbf{c}'_i = \mathbf{c}] = \rho_s(\mathbf{c})^2 / \sum_{\mathbf{c}'} \rho_s(\mathbf{c}')^2$ for any coset $\mathbf{c} \in \mathcal{L}/(2\mathcal{L})$. Therefore, for any $\mathbf{y} \in \mathcal{L}$,

$$
\begin{aligned} \Pr[\mathbf{Y}_i = \mathbf{y}] &= \frac{1}{\sum \rho_s(\mathbf{c})^2} \cdot \sum_{\mathbf{c}\in\mathcal{L}/(2\mathcal{L})} \rho_s(\mathbf{c})^2 \cdot \Pr_{(\mathbf{X}_j,\mathbf{X}_k)\sim D^2_{\mathbf{c},s}} \big[(\mathbf{X}_j+\mathbf{X}_k)/2 = \mathbf{y}\big] \\[2pt] &= \Pr_{(\mathbf{X}_1,\mathbf{X}_2)\sim D^2_{\mathcal{L},s}} \big[(\mathbf{X}_1+\mathbf{X}_2)/2 = \mathbf{y} \;\big|\; \mathbf{X}_1+\mathbf{X}_2 \in 2\mathcal{L}\big]. \end{aligned}
$$

The result then follows from Lemma 3.4. $\square$

</details>

## Reduction from SVP to DGS

## An Exact Gaussian Sampler from [[BLP+13]](https://arxiv.org/pdf/1306.0281)

Here is the original version of the Gaussian sampling lemma.

Lemma 2.3

There is a probabilistic polynomial-time algorithm that, given a basis $\mathbf{B}$ of an $n$ -dimensional lattice $\Lambda = \mathcal{L}(\mathbf{B})$, $\mathbf{c} \in \mathbb{R}^n$, and a parameter $r \ge \|\widetilde{\mathbf{B}}\| \cdot \sqrt{\ln(2n+4)/\pi}$, outputs a sample distributed according to $D_{\Lambda+\mathbf{c},\,r}$.

First consider the case $n=1$: suppose we want to sample from $D_{\mathbb Z+c,r}$ , where $c\in[0,1)$. The natural idea is to sample from a continuous Gaussian and round, then correct the probability error via rejection sampling. Let $Z=\rho_r(c)+\rho_r(c-1)+\int_{-\infty}^{c-1}\rho_r(x)\,\mathrm{d} x+\int_c^{+\infty}\rho_r(x)\,\mathrm{d} x$.

- With probability $\frac{\rho_r(c)}{Z}$ take $c$, with probability $\frac{\rho_r(c-1)}{Z}$ take $c-1$;

- With probability $\int_c^{+\infty}\rho_r(x)\,\mathrm{d} x/Z$ , sample $x$ from the continuous Gaussian on $(c,+\infty)$ , then let $y=c+\lceil x-c\rceil$ (round up), then accept with probability $\frac{\rho_r(y)}{\rho_r(x)}$ ; if rejected, go back to the start.

- With probability $\int_{-\infty}^{c-1}\rho_r(x)\,\mathrm{d} x/Z$ , sample $x$ from the continuous Gaussian on $(-\infty,c-1)$ , then let $y=c+\lfloor x-c\rfloor$ (round down), then accept with probability $\frac{\rho_r(y)}{\rho_r(x)}$ ; if rejected, go back to the start.

For $k> 0$ the probability of getting $y=c+k$ is $\int_{c+k-1}^{c+k}\rho_r(x)\frac{\rho_r(y)}{\rho_r(x)}\,\mathrm{d} x/Z=\frac{\rho_r(y)}{Z}$.

For $k<-1$ the probability of getting $y=c+k$ is $\int_{c+k}^{c+k+1}\rho_r(x)\frac{\rho_r(y)}{\rho_r(x)}\,\mathrm{d} x/Z=\frac{\rho_r(y)}{Z}$.

Moreover, the success probability is $\frac{\rho_r(c+\mathbb Z)}{\rho_r(c)+\rho_r(c-1)+\int_{-\infty}^{c-1}\rho_r(x)\,\mathrm{d} x+\int_c^{+\infty}\rho_r(x)\,\mathrm{d} x}\geq\frac{\rho_r(c+\mathbb Z)}{\rho_r(c+\mathbb Z)+\rho_r(c)+\rho_r(c-1)}\geq\frac{1}{2}$.

Note that this proof does not depend on properties of $\rho_r$ , so any other continuous distribution function works as well.
