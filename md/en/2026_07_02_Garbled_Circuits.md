# Garbled Circuits

*July 2, 2026*

In a garbled circuit, you (evaluator) see only what the garbler wants you to see. 

To show a value $m$ exactly to whoever holds a secret $k$, publish $H(k)\oplus m$.


## A quick catch-up

Here we describe the various GC constructions and optimizations in a uniform language. If you need the basic concepts, read the next chapter first.

Let the gate being evaluated be $g$ (an AND gate in most optimizations), with its two input wires denoted $\alpha,\beta$ and its output wire denoted $\gamma$; more generally, an arbitrary wire is denoted $\omega$. The label on wire $\omega$ corresponding to bit $x\in\{0,1\}$ is always denoted $L_{\omega,x}$, so the labels of this gate are $L_{\alpha,0},L_{\alpha,1},L_{\beta,0},L_{\beta,1}$ (input) and $L_{\gamma,0},L_{\gamma,1}$ (output). The garbling table is represented as a map, which can also be viewed as a function. The value on a wire is denoted $v$, and random pad bits are always denoted $\lambda$.

<figure style="margin:20px 0">
<svg viewBox="0 0 760 250" style="width:100%;max-width:760px;height:auto;display:block;margin:0 auto" role="img" aria-label="Extension relations among GC constructions">
<defs>
<marker id="gc-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--ink)"/></marker>
<marker id="gc-arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--accent)"/></marker>
<marker id="gc-arrow-faint" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--faint)"/></marker>
</defs>
<g style="stroke:var(--ink);stroke-width:1.4;fill:none">
<line x1="92" y1="195" x2="176" y2="195" marker-end="url(#gc-arrow)"/>
<line x1="328" y1="195" x2="402" y2="195" marker-end="url(#gc-arrow)"/>
</g>
<g style="stroke:var(--accent);stroke-width:1.8;fill:none">
<line x1="488" y1="195" x2="572" y2="195" marker-end="url(#gc-arrow-accent)"/>
<line x1="446" y1="177" x2="524" y2="85" marker-end="url(#gc-arrow-accent)"/>
</g>
<g style="stroke:var(--faint);stroke-width:1.4;fill:none;stroke-dasharray:5 4">
<line x1="561" y1="65" x2="652" y2="65" marker-end="url(#gc-arrow-faint)"/>
<line x1="622" y1="177" x2="700" y2="85" marker-end="url(#gc-arrow-faint)"/>
</g>
<g style="fill:var(--panel);stroke:var(--line);stroke-width:1.2">
<rect x="8" y="177" width="84" height="36" rx="8"/>
<rect x="178" y="177" width="150" height="36" rx="8"/>
<rect x="404" y="177" width="84" height="36" rx="8"/>
<rect x="574" y="177" width="96" height="36" rx="8"/>
<rect x="491" y="47" width="70" height="36" rx="8"/>
<rect x="654" y="47" width="96" height="36" rx="8" style="stroke-dasharray:5 4;stroke:var(--faint)"/>
</g>
<g style="fill:var(--ink);font-size:14px" text-anchor="middle">
<text x="50" y="200">Yao's GC</text>
<text x="253" y="200">+Point-and-Permute</text>
<text x="446" y="200">+FreeXOR</text>
<text x="622" y="200">Half-Gates</text>
<text x="526" y="70">BMR</text>
<text x="702" y="70" style="fill:var(--faint)">?</text>
</g>
<g style="fill:var(--soft);font-size:12px" text-anchor="middle">
<text x="134" y="176">indexing with masked bit</text>
<text x="365" y="176">global secret Δ</text>
<text x="530" y="234" style="fill:var(--accent)">4 ciphertexts to 2 ciphertexts</text>
<text x="470" y="126" text-anchor="end" style="fill:var(--accent)">2 to n parties</text>
<text x="607" y="36" style="fill:var(--faint)">2 ciphertexts</text>
<text x="700" y="140" text-anchor="start" style="fill:var(--faint)">n parties</text>
</g>
</svg>
</figure>

### **Yao's GC**

$$
(\lambda_\alpha\oplus v_\alpha,\lambda_\beta\oplus v_\beta)\to H(L_{\alpha,v_\alpha},L_{\beta,v_\beta},i)\oplus L_{\gamma,g(v_\alpha,v_\beta)}
$$

Additional condition: every label ends with a run of multiple $0$s (proportional to the security parameter), used to determine which label is the correct one.

### **Point-and-Permute**

The random values $\lambda_\omega$ used as masks are held by the Garbler; for gate $g$,

$$
\widehat v_\alpha=v_\alpha\oplus \lambda_\alpha,\ \widehat v_\beta=v_\beta\oplus \lambda_\beta,\ \widehat v_\gamma=g(v_\alpha,v_\beta)\oplus \lambda_\gamma
$$

What the evaluator obtains on wire $\omega$ is $\widehat v_\omega\|L_{\omega,\widehat v_\omega}$: $L_{\omega,x}\in\{0,1\}^\kappa$ is the label, and the leading bit is the masked bit, used to index the table. Garbling proceeds as follows: for all $(\widehat v_\alpha,\widehat v_\beta)\in\{0,1\}^2$,

$$
\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha},\ \widehat v_\beta\|L_{\beta,\widehat v_\beta}
\to
H\left(L_{\alpha,\widehat v_\alpha},L_{\beta,\widehat v_\beta},i\right)\oplus\bigl(\widehat v_\gamma\|L_{\gamma,\widehat v_\gamma}\bigr)
$$

### **FreeXOR**

The garbler chooses a global offset $\Delta\in\{0,1\}^\kappa$, chooses only $L_{\omega,0}$ at random for each wire, and sets $L_{\omega,1}=L_{\omega,0}\oplus\Delta$. Combined with Point-and-Permute, which places the masked bit in the leading position, the evaluator holds on wire $\omega$

$$
\widehat v_\omega\|L_{\omega,\widehat v_\omega}=(0\|L_{\omega,0})\oplus\widehat v_\omega(1\|\Delta).
$$

For an XOR gate $(\alpha,\beta,\gamma)$, the garbler sends nothing and sets

$$
L_{\gamma,0}=L_{\alpha,0}\oplus L_{\beta,0},\qquad\lambda_\gamma=\lambda_\alpha\oplus\lambda_\beta .
$$

The evaluator XORs the two strings it holds:

$$
(\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha})\oplus(\widehat v_\beta\|L_{\beta,\widehat v_\beta})
=(0\|L_{\gamma,0})\oplus(\widehat v_\alpha\oplus\widehat v_\beta)(1\|\Delta)
=(0\|L_{\gamma,0})\oplus(\lambda_\gamma\oplus v_\alpha\oplus v_\beta)(1\|\Delta)
=\widehat v_\gamma\|L_{\gamma,\widehat v_\gamma} .
$$

AND gates are unchanged, still a 4-row table. The cost is that the two labels of every wire differ by the same $\Delta$, so $H$ must still look random on such correlated inputs (correlation robustness).

### **BMR**

The generalization of Point-and-Permute plus FreeXOR to $n$ parties. One Evaluator, multiple Garblers.

**Garble**: Let $P_1$ be the evaluator and $P_2,\dots,P_n$ the garblers. Each garbler $P_i$ chooses a global offset $\Delta^{(i)}$, chooses $L_{\omega,0}^{(i)}$ at random for each wire $\omega$, sets $L_{\omega,1}^{(i)}=L_{\omega,0}^{(i)}\oplus\Delta^{(i)}$, and chooses a pad bit $\lambda_\omega^{(i)}$; the evaluator chooses no labels and contributes no pad bits (except on its own input wires; see Bootstrapping). Thus for $n=2$ this is exactly Point-and-Permute plus FreeXOR: the garbler holds all labels and masks.

For gate $g$, suppose the input wires are $\alpha,\beta$ and the output wire is $\gamma$. Let

$$
\lambda_\alpha:=\bigoplus_{i=2}^{n}\lambda_\alpha^{(i)}.
$$

and for $x\in\{0,1\}$ let

$$
L_{\alpha,x}=L_{\alpha,x}^{(2)}\|\cdots\|L_{\alpha,x}^{(n)},
$$

What the evaluator holds on wire $\alpha$ is still $\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha}$.

Write $\Delta=\Delta^{(2)}\|\cdots\|\Delta^{(n)}$; then $x\|L_{\alpha,x}=(0\|L_{\alpha,0})\oplus x(1\|\Delta)$, the same shape as two-party FreeXOR. An **XOR gate** $(\alpha,\beta,\gamma)$ therefore needs no table: each garbler locally sets $L^{(i)}_{\gamma,0}=L^{(i)}_{\alpha,0}\oplus L^{(i)}_{\beta,0}$, $\lambda^{(i)}_\gamma=\lambda^{(i)}_\alpha\oplus\lambda^{(i)}_\beta$, and the evaluator simply computes $(\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha})\oplus(\widehat v_\beta\|L_{\beta,\widehat v_\beta})=\widehat v_\gamma\|L_{\gamma,\widehat v_\gamma}$; the mask of an input wire is provided only by its owner (see Bootstrapping), the other garblers' shares are treated as $0$, and the equation above still holds. Below we write only the AND gate $g$.

Then each garbler $P_i$ locally computes $H(L^{(i)}_{\alpha,\widehat v_\alpha},L^{(i)}_{\beta,\widehat v_\beta},\mathrm{id})$, where all $\widehat v_\alpha,\widehat v_\beta\in\{0,1\}$ must be enumerated.

Next, all parties run an MPC protocol to obtain the output of a circuit, repeated once for every $\widehat v_\alpha,\widehat v_\beta\in\{0,1\}$. The circuit inputs are garbler $P_i$'s shares (the evaluator holds $\lambda^{(1)}$ only on its own input wires, and inputs it as well) $\lambda_\alpha^{(i)},\lambda_\beta^{(i)},\lambda_\gamma^{(i)},L_{\gamma,0}^{(i)},L_{\gamma,1}^{(i)},H(L^{(i)}_{\alpha,\widehat v_\alpha},L^{(i)}_{\beta,\widehat v_\beta},\mathrm{id})$, and the circuit computes

$$
\chi=g(\lambda_\alpha\oplus\widehat v_\alpha,\lambda_\beta\oplus\widehat v_\beta)\oplus\lambda_\gamma=g\left(\bigoplus_{i=2}^{n}\lambda_\alpha^{(i)}\oplus\widehat v_\alpha,\bigoplus_{i=2}^{n}\lambda_\beta^{(i)}\oplus\widehat v_\beta\right)\oplus\bigoplus_{i=2}^{n}\lambda_\gamma^{(i)}
$$

and

$$
e_{\widehat v_\alpha,\widehat v_\beta}=\bigl(\chi\|L_{\gamma,\chi}\bigr)\oplus\left(\bigoplus_{i=2}^{n} H(L^{(i)}_{\alpha,\widehat v_\alpha},L^{(i)}_{\beta,\widehat v_\beta},\mathrm{id})\right)
$$

and places it at position $(\widehat v_\alpha,\widehat v_\beta)$ of the table.

**Evaluate**: For this gate $g$, the evaluator holds $\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha}$ and $\widehat v_\beta\|L_{\beta,\widehat v_\beta}$, whose leading bits are exactly $\widehat v_\alpha,\widehat v_\beta$. Looking up position $(\widehat v_\alpha,\widehat v_\beta)$ in the table yields $e_{\widehat v_\alpha,\widehat v_\beta}$.

By the garbling procedure, we obtain

$$
\widehat v_\gamma\|L_{\gamma,\widehat v_\gamma}=\chi\|L_{\gamma,\chi}=e_{\widehat v_\alpha,\widehat v_\beta}\oplus\left(\bigoplus_{i=2}^{n} H(L^{(i)}_{\alpha,\widehat v_\alpha},L^{(i)}_{\beta,\widehat v_\beta},\mathrm{id})\right)
$$

where

$$
\widehat v_\gamma=\chi=g(\lambda_\alpha\oplus\widehat v_\alpha,\lambda_\beta\oplus\widehat v_\beta)\oplus\lambda_\gamma
$$

This matches exactly the definition of $\widehat v_\gamma$ as $v_\gamma\oplus\lambda_\gamma$, so the equation above says exactly that $v_\gamma=g(v_\alpha,v_\beta)$.

**Bootstrapping**: For an input wire $\omega$, its owner $P_{j_\omega}$ broadcasts $\widehat v_\omega=v_\omega\oplus \lambda_\omega^{(j_\omega)}$. Note that the definition has changed here; we do not use $\widehat v_\omega=v_\omega\oplus \lambda_\omega$ because that would require an extra round of communication.

> For the reason above, different masking rules must also be set for different wires during Garbling. Specifically,
>
> $$
> \lambda_\omega = \begin{cases} \lambda_\omega^{(j_\omega)} & \omega \in \mathsf{Input} \\ \lambda_\omega^{(2)} \oplus \cdots \oplus \lambda_\omega^{(n)} & \text{otherwise} \end{cases}
> $$
>
> An intuitive explanation: the mask exists so that those who should not see the plaintext cannot see it (the leading bit of the string the evaluator obtains is the plaintext plus the mask; without the mask it would see the plaintext directly)
>
> For an input wire $\omega$, $P_{j_\omega}$ already knows the plaintext, so the goal is that no subset of the remaining $n-1$ parties can recover the plaintext. Hence it suffices for the mask to be provided entirely by $j_\omega$. (If $P_{j_\omega}$ is corrupted, the corrupted parties already learn the plaintext through it, so no protection is needed.)
>
> For internal wires, all garblers need to participate in sharing the mask, so as to ensure that no subset can recover the plaintext.

Then everyone obtains $\widehat v_\omega$, and each garbler sends $L_{\omega,\widehat v_\omega}^{(i)}$ to the evaluator, which concatenates them into

$$
\widehat v_\omega\|L_{\omega,\widehat v_\omega}=\widehat v_\omega\|L_{\omega,\widehat v_\omega}^{(2)}\|\cdots\|L_{\omega,\widehat v_\omega}^{(n)}.
$$

Then Evaluation can start directly.

### **Half-Gates**

Write what the evaluator holds on wire $\omega$ as $\widehat v_\omega\|L_{\omega,\widehat v_\omega}$. Following FreeXOR,

$$
x\|L_{\omega,x}=(0\|L_{\omega,0})\oplus x(1\|\Delta),
$$

$g,g'$ are two different tweaks for the same AND gate.

**Garble.**

The garbler already holds $\Delta,L_{\alpha,0},L_{\beta,0},\lambda_\alpha,\lambda_\beta$. Split the AND as

$$
v_\alpha v_\beta=v_\alpha\lambda_\beta\oplus v_\alpha\widehat v_\beta :=v_G\oplus v_E,
$$

The Garbler knows $\lambda_\beta$ and the Evaluator knows $\widehat v_\beta$. The outputs of the two halves can be viewed as two ordinary wires $G,E$, with masks $\lambda_G,\lambda_E$ and labels $W_{G,x},W_{E,x}\in\{0,1\}^\kappa$,

$$
x\|W_{G,x}=(0\|W_{G,0})\oplus x(1\|\Delta),\qquad x\|W_{E,x}=(0\|W_{E,0})\oplus x(1\|\Delta).
$$

> The Garbler expects the Evaluator to obtain $\widehat v_G\|W_{G,\widehat v_G}=(\lambda_G\|W_{G,\lambda_G})\oplus v_G(1\|\Delta)$ and $\widehat v_E\|W_{E,\widehat v_E}=(\lambda_E\|W_{E,\lambda_E})\oplus v_E(1\|\Delta)$, and then a direct XOR yields 
> 
> $$
> \widehat v_\gamma\|L_{\gamma,\widehat{v}_\gamma}=(\widehat v_G\|W_{G,\widehat v_G})\oplus(\widehat v_E\|W_{E,\widehat v_E}),
> $$
> 
> That is, we must ensure
> 
> $$
> L_{\gamma,0}=W_{G,0}\oplus W_{E,0},\quad\lambda_\gamma=\lambda_G\oplus\lambda_E.
> $$

In the derivation below, we repeatedly use the formula from the Point-and-Permute section:

$$
\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha},\ \widehat v_\beta\|L_{\beta,\widehat v_\beta}
\to
H\left(L_{\alpha,\widehat v_\alpha},L_{\beta,\widehat v_\beta},i\right)\oplus\bigl(\widehat v_\gamma\|L_{\gamma,\widehat v_\gamma}\bigr)
$$

Except that what we do is apply it to the two half gates, substitute the values of the two masked bits at the inputs, and then, by choosing the label values cleverly, send one fewer ciphertext. We will use the following relations:

$$
\widehat v_G=(\widehat v_\alpha\oplus\lambda_\alpha)\lambda_\beta\oplus\lambda_G,\\
\widehat v_E=(\widehat v_\alpha\oplus\lambda_\alpha)\widehat v_\beta\oplus\lambda_E.
$$

Generator half. Here the Garbler wants the Evaluator to obtain $\widehat v_G$ from $\widehat v_\alpha$, and the Garbler knows all the other variables in $\widehat v_G=(\widehat v_\alpha\oplus\lambda_\alpha)\lambda_\beta\oplus\lambda_G$. So $H$ is used to mask $\widehat v_G$:

$$
\begin{aligned}
(\widehat v_\alpha=0)&\to H(L_{\alpha,0},g)\oplus(\widehat v_G\|W_{G,\widehat v_G})=H(L_{\alpha,0},g)\oplus(\lambda_G\|W_{G,\lambda_G})\oplus\lambda_\alpha\lambda_\beta(1\|\Delta),\\
(\widehat v_\alpha=1)&\to H(L_{\alpha,1},g)\oplus(\widehat v_G\|W_{G,\widehat v_G})=H(L_{\alpha,1},g)\oplus(\lambda_G\|W_{G,\lambda_G})\oplus(1\oplus\lambda_\alpha)\lambda_\beta(1\|\Delta).
\end{aligned}
$$

Set

$$
\lambda_G\|W_{G,\lambda_G}=H(L_{\alpha,0},g)\oplus\lambda_\alpha\lambda_\beta(1\|\Delta),
$$

Then the first row $=0$, and it suffices to send

$$
T_G=H(L_{\alpha,0},g)\oplus H(L_{\alpha,1},g)\oplus\lambda_\beta(1\|\Delta).
$$

Evaluator half. Here the Garbler wants the Evaluator to obtain $\widehat v_E$ from $\widehat v_\beta$, so $H$ is used to mask $\widehat v_E$:

$$
\begin{aligned}
(\widehat v_\beta=0)&\to H(L_{\beta,0},g')\oplus(\widehat v_E\|W_{E,\widehat v_E})=H(L_{\beta,0},g')\oplus(\lambda_E\|W_{E,\lambda_E}),\\
(\widehat v_\beta=1)&\to H(L_{\beta,1},g')\oplus(\widehat v_E\|W_{E,\widehat v_E})=H(L_{\beta,1},g')\oplus(\lambda_E\|W_{E,\lambda_E})\oplus{\color{red}(\lambda_\alpha\oplus\widehat v_\alpha)(1\|\Delta)}.
\end{aligned}
$$

All of the above is derived from the Point-and-Permute formula. The attentive reader will notice that the Garbler does not know the value of $\widehat v_\alpha$ (the red term), which means we cannot follow the Point-and-Permute scheme exactly. Instead, we observe that the red term is in fact equal to:

$$
(\lambda_\alpha\oplus\widehat v_\alpha)(1\|\Delta)=v_\alpha(1\|\Delta)={\color{#12A06A}(\lambda_\alpha\|L_{\alpha,\lambda_\alpha})}\oplus{\color{#3D8BFD}(\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha})},
$$

The garbler knows the first term, and the evaluator holds the second. So the following is the correct way to generate the table:

$$
\begin{aligned}
(\widehat v_\beta=0)&\to H(L_{\beta,0},g')\oplus(\widehat v_E\|W_{E,\widehat v_E})=H(L_{\beta,0},g')\oplus(\lambda_E\|W_{E,\lambda_E}),\\
(\widehat v_\beta=1)&\to H(L_{\beta,1},g')\oplus(\widehat v_E\|W_{E,\widehat v_E})=H(L_{\beta,1},g')\oplus(\lambda_E\|W_{E,\lambda_E})\oplus{\color{#12A06A}(\lambda_\alpha\|L_{\alpha,\lambda_\alpha})}.
\end{aligned}
$$

The Evaluator then assembles it itself after receiving it. For details, see the Evaluate paragraph below.

Set

$$
\lambda_E\|W_{E,\lambda_E}=H(L_{\beta,0},g'),
$$

Then the first row $=0$, and it suffices to send

$$
T_E=H(L_{\beta,0},g')\oplus H(L_{\beta,1},g')\oplus{\color{#12A06A}(\lambda_\alpha\|L_{\alpha,\lambda_\alpha})}.
$$

Output wire $v_\gamma=v_G\oplus v_E$; following FreeXOR, set

$$
\lambda_\gamma=\lambda_G\oplus\lambda_E,\qquad L_{\gamma,0}=W_{G,0}\oplus W_{E,0}.
$$

Finally the Garbler sends the two ciphertexts $(T_G,T_E)$ to the Evaluator as the garbling table.

**Evaluate.**

The evaluator holds $\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha}$, $\widehat v_\beta\|L_{\beta,\widehat v_\beta}$ and $(T_G,T_E)$, and computes

$$
\begin{aligned}
U_G&=H(L_{\alpha,\widehat v_\alpha},g)\oplus\widehat v_\alpha T_G,\\
U_E&=H(L_{\beta,\widehat v_\beta},g')\oplus\widehat v_\beta T_E\oplus {\color{#3D8BFD}\widehat v_\beta(\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha})}{\;\gets \text{if }\widehat v_\beta=1\text{, add it yourself}}
\end{aligned}
$$

and uses $U_G\oplus U_E$ as the label on wire $\gamma$.

**Correctness.**

Generator half:

$$
U_G=\begin{cases}
H(L_{\alpha,0},g)=(\lambda_G\|W_{G,\lambda_G})\oplus\lambda_\alpha\lambda_\beta(1\|\Delta), & \widehat v_\alpha=0,\\
H(L_{\alpha,1},g)\oplus T_G=(\lambda_G\|W_{G,\lambda_G})\oplus(1\oplus\lambda_\alpha)\lambda_\beta(1\|\Delta), & \widehat v_\alpha=1,
\end{cases}
$$

In both cases this is $(\lambda_G\|W_{G,\lambda_G})\oplus v_G(1\|\Delta)=\widehat v_G\|W_{G,\widehat v_G}$.

Evaluator half:

$$
U_E=\begin{cases}
\lambda_E\|W_{E,\lambda_E}, & \widehat v_\beta=0,\\
(\lambda_E\|W_{E,\lambda_E})\oplus(\lambda_\alpha\|L_{\alpha,\lambda_\alpha})\oplus(\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha})=(\lambda_E\|W_{E,\lambda_E})\oplus v_\alpha(1\|\Delta), & \widehat v_\beta=1,
\end{cases}
$$

In both cases this is $(\lambda_E\|W_{E,\lambda_E})\oplus v_E(1\|\Delta)=\widehat v_E\|W_{E,\widehat v_E}$.

Combined, this is the same as the XOR gate of FreeXOR:

$$
U_G\oplus U_E
=(0\|L_{\gamma,0})\oplus(\widehat v_G\oplus\widehat v_E)(1\|\Delta)
=(0\|L_{\gamma,0})\oplus(\lambda_\gamma\oplus v_\alpha v_\beta)(1\|\Delta)
=\widehat v_\gamma\|L_{\gamma,\widehat v_\gamma} .
$$

**Security.** The evaluator has only $\widehat v_\alpha\|L_{\alpha,\widehat v_\alpha}$ and $\widehat v_\beta\|L_{\beta,\widehat v_\beta}$. $H(L_{\alpha,1\oplus\widehat v_\alpha},g)$ in $T_G$ and $H(L_{\beta,1\oplus\widehat v_\beta},g')$ in $T_E$ are hashes of labels it does not have, and they mask $\lambda_\beta(1\|\Delta)$ and $\lambda_\alpha\|L_{\alpha,\lambda_\alpha}$ respectively. The labels it does not have differ from the labels it has by $\Delta$, and $\lambda_\beta(1\|\Delta)$ also appears directly in $T_G$, so $H$ is required to still look random on values of the form $H(L\oplus\Delta,g)\oplus(1\|\Delta)$ (circular correlation robustness), the same requirement as for FreeXOR. The two half gates use different tweaks, so the hash of the same string is never used twice.

**Cost.** Each AND gate sends $2(\kappa+1)$ bits, and the evaluator computes $H$ twice; XOR gates remain free.

## Garbled Circuits

A **garbling scheme** consists of four algorithms; the first is non-deterministic while others are deterministic:

- $\mathsf{Garble}$: $(\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f)$

- $\mathsf{Encode}$: $\mathcal{X} \leftarrow \mathsf{Encode}(e, {x})$

- $\mathsf{Eval}$: $\mathcal{Y} \leftarrow \mathsf{Eval}(\mathcal{F}, \mathcal{X})$

- $\mathsf{Decode}$: $\{{y},\bot\} \leftarrow \mathsf{Decode}(d, \mathcal{Y})$

**Correctness:** For all $f, (\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f), {x}$,

$$
\mathsf{Decode}(d, \mathsf{Eval}(\mathcal{F}, \mathsf{Encode}(e, {x}))) = f({x})
$$

Intuitive security goals:

- **Obliviousness**: $\mathcal{F}, \mathcal{X}$ reveals nothing about $x$. This is about preventing the evaluator from gaining the input.

- **Authenticity**: Given $\mathcal{F}, \mathcal{X}$ it is of negligible probability for all PPT adversaries to find $\mathcal{Y}'\not=\mathsf{Eval}(\mathcal{F},\mathcal{X})$ that decodes to a value (not a $\bot$). This is about preventing the evaluator from forging the result.

- **Output simulatability**: $\mathcal{Y}$ can be efficiently computed by $f(x)$ and $d$.

Here is a scheme of **outsourcing computation:** suppose Alice uses Bob’s computation resources to compute $f(x)$. First Alice generates $(\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f)$; then sends $\mathcal{F}$ to Bob, and keeps $e,d$ herself. When she wants to compute, she has $\mathcal{X} \leftarrow \mathsf{Encode}(e, {x})$ and sends $\mathcal{X}$ to Bob, where Bob computes $\mathcal{Y} \leftarrow \mathsf{Eval}(\mathcal{F}, \mathcal{X})$ and returns to Alice. Then Alice can decode.

Note that Alice should generate a garbled circuit on different inputs and the same boolean circuit. If we use the same GC for different computation tasks, then a honest-but-curious party would know some relations of the two inputs through comparing the encoded $\mathcal{X}$; or some information about $e$. We should always keep in mind that the encoding algorithm is deterministic.

### Formal definition of the security goals

**Obliviousness.** For $b = 0, 1$, we have experiment $\mathsf{Exp}_b$:

- Adversary submits $(f, \mathbf{x}^{(0)}, \mathbf{x}^{(1)})$

- Challenger computes:

$$
(\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f), \quad \mathcal{X} \leftarrow \mathsf{Encode}(e, \mathbf{x}^{(b)})
$$

and sends $(\mathcal{F}, \mathcal{X})$ to adversary.

- Adversary outputs $\hat{b} \in \{0,1\}$, let $W_b$ be the event that the adversary outputs $1$.

A garbling scheme is oblivious iff for every PPT adversary, the game has a negligible advantage defined by $|\Pr[W_0] - \Pr[W_1]|$.

**Output Simulatability.** A garbling scheme is output simulatable if there exists an efficient deterministic algorithm $\mathsf{Reverse}$ such that for every $f$, every $(\mathcal{F}, e, d) \leftarrow \mathsf{Garble}(f)$, and every ${x}$:

$$
\mathsf{Eval}(\mathcal{F}, \mathsf{Encode}(e, \mathbf{x})) = \mathsf{Reverse}(d, f(\mathbf{x})).
$$

### $\texttt{Garble0}$: an implementation of garbling scheme

Suppose the boolean circuit has $n$ variables and $m$ outputs. The below $e$ is called a **projective input encoding**, where the encoding process is for every bit, use one value out of two.

$$
\begin{align*}
e&=((X_1^0,X_1^1),\dots,(X_n^0,X_n^1))\\
\mathcal{X}&=(X_1^{x_1},\dots,X_n^{x_n})\\
d&=((Y_1^0,Y_1^1),\dots,(Y_m^0,Y_m^1))\\
\mathcal{Y}&=(Y_1,\dots,Y_m)
\end{align*}
$$

where $x$ is the input and $\mathcal{Y}$ is the garbled output. The decoding algorithm is to compare each $Y_j$ to the pair $(Y_j^0,Y_j^1)$.

Our goal is to establish the algorithm $\mathsf{Eval}$ that with input $\mathcal{F}$ and $\mathcal{X}$ carries out the garbled output.

The garbled circuit $\mathcal{F}$ consists of a function for each gate $g$, which we will denote by $\mathsf{GateEval}_g$ satisfying

$$
\mathsf{GateEval}(\mathcal{G},I_1^u,I_2^v)=O^{g(u,v)}
$$

where $I_i^x$ ‘s are the garbled values of input wires and $O^y$ are that of the output wire. For example an AND gate, we have $\mathsf{GateEval}(I_1^u,I_2^v)=O^{\mathbf{1}[u=1\land v=1]}$. The encoding $\mathcal{G}$ for this gate is called a **garbled encoding**, which should be used together with a **garbled evaluation algorithm** $\mathsf{GateEval}$.

### Implementation of garbled encoding

This implementation entails a public key encryption scheme. We index each wire by $I$ and each wire $i$ corresponds to two public keys $(k_i^0,k_i^1)$ as the **private encoding**. Then consider one gate with inputs wires $i,j$ and output wire $t$.

$$
E^{(a,b)}=\mathsf{Enc}_{k_i^a}(\mathsf{Enc}_{k_j^b}(k_t^{g(a,b)}\|000\dots00))
$$

where the length of the trailing zeros is the security parameter $\lambda$. And the garbled circuit is the tuple

$$
\mathcal{G}=(i,j,t,E^{(0,0)},E^{(0,1)},E^{(1,0)},E^{(1,1)})
$$

with the evaluation algorithm

$$
\begin{align*}
\mathsf{GateEval}(\mathcal{G},X,Y)=
&\;\mathbf{for}\;a\in\{0,1\},b\in\{0,1\}:\\
&\quad\mathbf{if}\;\mathsf{Dec}_{k_j^Y}(\mathsf{Dec}_{k_i^X}(E^{(a,b)}))\text{ end with }\lambda\; 0\text{'s}\\
&\quad\quad\mathbf{return}\;\mathsf{Dec}_{k_j^Y}(\mathsf{Dec}_{k_i^X}(E^{(a,b)}))
\end{align*}
$$

This algorithm is obviously correct, but requires computations for all $4$ possibilities. Below we propose the point-and-permute method to make it more efficient.

(In fact this method has a constant complexity for all gates; if we construct a big look-up table for the whole circuit, the total time will be exponential!)

### More efficient

We have $T=\{0,1\}^\ell$ be our set of **tokens** and $I$ is the finite set of identifiers that each gate has a unique identifier $i\in I$. And $H:T\times T\times I\mapsto T$ a hash function. For each wire, the garbling process generates $(X^0,X^1,r)$ as the **private encoding** such that $X^i$ begins with $i$. Then consider the gate $i$ with its input private encodings $(A^0,A^1,r),(B^0,B^1,s)$ and the output private encodings $(C^0,C^1,t)$. We set for $a,b\in\{0,1\}$,

$$
E^{(a,b)}=H(A^{a},B^b,i)\oplus C^{g(a\oplus r,b\oplus s)\oplus t}.
$$

Note that And we define the garbled encoding

$$
\mathcal{G}=(i,E^{(0,0)},E^{(0,1)},E^{(1,0)},E^{(1,1)})
$$

with the garbled evaluation algorithm

$$
\mathsf{GateEval}(\mathcal{G},X,Y)=H(X,Y,i)\oplus E^{(a,b)}
$$

where $a$ is the first bit of $X$ and $b$ is the first bit of $Y$.

This is just like the above scheme where the double encryption is realized by the hash function and the XOR operation. So we can also introduce such a **point-and-permute** method into the scheme above. Suppose $E^{(a,b)}=\mathsf{Enc}_{k_i^a}(\mathsf{Enc}_{k_j^b}(k_t^{g(a,b)}))$, and the table is

$$
E^{(1,0)},E^{(1,1)},E^{(0,0)},E^{(0,1)}
$$

So we let the $k_i^a$ begin by $1-a$ and $k_j^b$ begin by $b$, the evaluator would know from the keys which entry to decode. Note that this method only supports $4$ out of $|S_4|=24$ permutations.

The correctness of the algorithm is one line of formula. When computing, if the first input wire has value $u$, then the corresponding encoding is $X^u:=A^{u\oplus r}$, and the same for the second input and the output, say, $Y^v:=B^{v\oplus s}$ and $Z^w:=C^{w\oplus t}$. Then we have

$$
\mathsf{GateEval}(\mathcal{G},X^u,Y^v)=H(A^{u\oplus r},B^{v\oplus s},i)\oplus E^{(u\oplus r,v\oplus s)}=C^{g(u,v)\oplus t}=Z^{g(u,v)}.
$$

The random bit here is used to mask the true value. Imagine you send $A^u,B^v$ directly, the evaluator immediately knows the hidden value because $A^u$ has the first bit $u$, and the same as $B^v$.

### The full protocol

$$
\begin{align*}&\text{Garbler},\left(x^{(0)}_i\right)_{i=0}^{k-1}&&&\text{Evaluator},\left(x^{(1)}_i\right)_{i=k}^{n-1}\\&\mathcal{F}=\{\mathcal{G}_i\}_{i=0}^{t-1}, \quad e=((X_1^0,X_1^1),\ldots,(X_n^0,X_n^1)), \quad d=((Y_1^0,Y_1^1),\ldots,(Y_m^0,Y_m^1))&\xrightarrow{\mathcal{F},\;\left(X_i^{x^{(0)}_i}\right)_{i=0}^{k-1}}&&\\&e&\xleftrightarrow{\text{1-out-of-2 }\mathbf{OT}}&&\left(X_i^{x^{(1)}_i}\right)_{i=k}^{n-1}\\&y=\mathsf{Decode}\left(d,\mathcal{Y}\right)&\xleftarrow{\mathcal{Y}}&&\mathcal{Y}=\mathsf{Eval}\left(\mathcal{F},\left(X_i^{x_i}\right)_{i=0}^{n-1}\right)\text{, runs }\mathsf{GateEval}\text{ on each gate}\\\end{align*}
$$

### Why OT?

Here is a more direct version: the garbler sends the full $(X_i^0,X_i^1)$ and let the evaluator choose one from the pair. Thus the garbler will not know what the evaluator chooses; so the problem is, why do we mask the other value from the evaluator in the protocol $\texttt{Garble0}$?

For one AND gate $x_1\land x_2$, where $x_1$ is from the garbler and $x_2$ is from the evaluator. Now suppose the evaluator gets both $X_2^0$ and $X_2^1$, and the evaluator would secretly compute the garbled output with the garbled circuit, using different values of $x_2$. If the garbled output are different, the evaluator knows that $x_1=1$.

### FreeXOR

The garbler uses a global difference $\Delta$ and let for every wire, $X^0\oplus\Delta=X^1$. For one XOR gate, let the labels of the input/output gates be $A^0,A^1=A^0\oplus \Delta,B^0,B^1=B^0\oplus \Delta,C^0=A^0\oplus B^0,C^1=C^0\oplus \Delta$. Then if the two inputs are $x,y$ then $A^{x}\oplus B^y=A^0\oplus B^0\oplus x\Delta\oplus y\Delta=C^{0}\oplus (x\oplus y)\Delta=C^{x\oplus y}$.

The evaluator cannot have access to $\Delta$ and the reason is the same as **Why OT**. Now communication is $0$ per XOR and $4\kappa$ per AND; verification is $0$ per XOR and $\kappa$ per AND.

### 3-party protocol against 1 malicious adversary

We consider a 3-party setting where $P_1$ and $P_2$ hold private inputs (a partition of the $n$ input bits), and an additional party $P_3$ acts as an evaluator. The goal is to compute $f(x)$ while tolerating 1 malicious adversary.

High-level idea: $P_1$ and $P_2$ jointly generate the *same* garbled circuit $\mathcal{F}$ (using shared randomness) and send it to $P_3$ together with *commitments/hashes* to the wire tokens. Each of $P_1$ and $P_2$ then “opens” only the tokens corresponding to its own input bits, in a way that lets $P_3$ evaluate but not learn the raw input bits.

Protocol sketch (for a fixed circuit $f$):

A compact “message-flow” diagram (aligned):

$$
\begin{align*}P_1(x^{(1)}) && P_2(x^{(2)}) && P_3 \\(\mathcal{F},e,d) \leftarrow \mathsf{Garble}(f;G(s))\,,\; \{C_i^{(b)}\}_{i,b}& \xrightarrow{\;\mathcal{F},\,\{C_i^{(b)}\}\; }& (\mathcal{F},e,d) \leftarrow \mathsf{Garble}(f;G(s))\,,\; \{C_i^{(b)}\}_{i,b}& \xrightarrow{\;\mathcal{F},\,\{C_i^{(b)}\}\; }& \text{check and store }\mathcal{F},\{C_i^{(b)}\} \\(i,a_i, X_i, r_i)_{i\in I_1}& \xrightarrow{\text{open own inputs}}&&& \text{check } C_i^{(a_i)} = H_1(X_i,r_i) \\&& (i,a_i, X_i, r_i)_{i\in I_2}& \xrightarrow{\text{open own inputs}}& \text{check } C_i^{(a_i)} = H_1(X_i,r_i) \\y \leftarrow \mathsf{Decode}(d,\mathcal{Y})& \xleftarrow{\;\mathcal{Y}\; } & y \leftarrow \mathsf{Decode}(d,\mathcal{Y})& \xleftarrow{\;\mathcal{Y}\; } & \mathcal{Y} \leftarrow \mathsf{Eval}(\mathcal{F},\mathcal{X})\end{align*}
$$

Here, $e = ((X_1^{(0)}, X_1^{(1)}), \dots, (X_n^{(0)}, X_n^{(1)}))$, and the tuple list $\{C_i^{(b)}\}$ is generated by randomly choosing $(b_i)_{i=1}^n$ and $(r_i^{(b)})_{i\in[n],b\in\{0,1\}}$ and computing $C_i^{(b)}=H_1(X_i^{(b \oplus b_i)}, r_i^{(b)})$.

Then $P_1,P_2$ sends their known bits in the encoded value $X_i=X_i^{(x_i)},a_i=x_i\oplus b_i,r_i=r_i^{(a_i)}$.

Note that the output of the two garblers are expected to be the same, since they use the same PRG $G$ and the same seed $s$.

Why this helps against a malicious party:

- If one of $P_1$ or $P_2$ tries to cheat by sending inconsistent garbling information, $P_3$ detects it because it receives two versions and checks equality.

- If a party tries to cheat by sending an invalid wire token, the hash/commitment check fails.

- The random “swap” bits $b_i$ hide which of the two tokens corresponds to 0/1 for each wire, so $P_3$ can evaluate without learning the underlying input bits.

[BitGC: Garbled Circuits with 1 Bit per Gate](https://app.notion.com/p/BitGC-Garbled-Circuits-with-1-Bit-per-Gate-33fd71e335be804dad33e13a61e02702?pvs=21)

## Malicious Security for Garbled Circuits

Let $G$ be the garbler with input $x$, let $E$ be the evaluator with input $y$, and let $f$ be the agreed Boolean circuit. Let $\mathcal{F}$ denote the garbled circuit. The semi-honest Yao protocol only guarantees security when

$$
\mathcal{F}\leftarrow\mathsf{Garble}(f)
$$

is honestly generated by $G$.

### What a malicious garbler can do

- **Garbling a wrong circuit.** Let $f'\ne f$ be a circuit chosen by $G$. A malicious $G$ can send

$$
\mathcal{F}'\leftarrow\mathsf{Garble}(f'),\qquad
f(x,y)\longrightarrow f'(x,y).
$$

For example, choosing $f'(x,y)=y_1$ reveals the first input bit of $E$. Since $E$ sees only labels and ciphertexts, it cannot test whether $\mathcal{F}'$ garbles $f$ or $f'$.

- **Selective failure.** For an input bit $y_i$ of $E$, let $L_i^0,L_i^1$ be its two input labels. The honest OT is

$$
G:(L_i^0,L_i^1),\qquad E:y_i\longmapsto L_i^{y_i}.
$$

A malicious $G$ replaces $L_i^1$ by an invalid label $\bot$:

$$
G:(L_i^0,\bot),\qquad
\Pr[\mathsf{abort}=1\mid y_i]=y_i.
$$

Thus the abort event reveals $y_i$. The same attack applies to one row of a garbled gate.

- **Input inconsistency.** Suppose $G$ prepares $s$ garbled circuits and uses input $x^{(j)}$ in the $j$-th copy. We additionally need

$$
x^{(1)}=x^{(2)}=\cdots=x^{(s)}.
$$

### Cut-and-choose

Let $s$ be an even integer and let $[s]=\{1,\dots,s\}$. For the $j$-th garbled circuit, let $\tau_j$ be its garbling randomness and let $\mathcal{F}_j$ be the circuit. Let $J\subset[s]$ be the check set with $|J|=s/2$, and let $I=[s]\setminus J$ be the evaluation set. For $j\in I$, let $z_j$ be the output of $\mathcal{F}_j$, and let $z$ be the final output.

$$
\begin{align*}
&\text{Garbler }G(x)&&&\text{Evaluator }E(y)\\
&\left\{\mathcal{F}_j\leftarrow\mathsf{Garble}(f;\tau_j)\right\}_{j\in[s]}
&&\xrightarrow{\quad\{\mathcal{F}_j\}_{j\in[s]}\quad}&\\
&&&\xleftarrow{\quad J\quad}&J\leftarrow_R\{S\subset[s]:|S|=s/2\}\\
&\{\tau_j\}_{j\in J}
&&\xrightarrow{\quad\{\tau_j\}_{j\in J}\quad}&
\forall j\in J:\ \mathcal{F}_j\stackrel{?}{=}\mathsf{Garble}(f;\tau_j)\\
&\text{input labels for }x,\ j\in I
&&\xrightarrow{\quad\text{labels}\quad}&\\
&\text{input-label pairs for }y,\ j\in I
&&\xleftrightarrow{\quad\mathbf{OT}\quad}&
\text{selected labels for }y\\
&&&&z_j\leftarrow\mathsf{Eval}(\mathcal{F}_j),\quad j\in I\\
&&&&z\leftarrow\mathsf{majority}\{z_j:j\in I\}.
\end{align*}
$$

Let $B\subseteq[s]$ be the set of incorrectly garbled circuits and let $b=|B|$. The adversary succeeds only if no bad circuit is checked and a majority of the evaluation circuits are bad:

$$
B\cap J=\varnothing,\qquad |B\cap I|>\frac{|I|}{2}=\frac{s}{4}.
$$

For a fixed $B$ with $s/4<b\leq s/2$,

$$
\Pr[B\cap J=\varnothing]
=\frac{\binom{s-b}{s/2-b}}{\binom{s}{s/2}}.
$$

This probability decreases exponentially in $s$.

We should not abort merely because the evaluated copies disagree. For a one-bit output, suppose one bad circuit computes

$$
f'(x,y)=f(x,y)\oplus y_1.
$$

Then

$$
\mathsf{abort}=1
\quad\Longleftrightarrow\quad
f'(x,y)\ne f(x,y)
\quad\Longleftrightarrow\quad
y_1=1,
$$

which is another selective-failure channel. Majority ignores a minority of bad circuits.

The protocol must also enforce input consistency:

$$
\forall j,k\in I:\qquad x^{(j)}=x^{(k)}.
$$

This is done by committing to the input labels and proving the equality across copies.

Finally, the OT itself must resist selective failure. One solution is committing OT. Another is a $k$-probe-resistant encoding, where $k$ is the maximal number of corrupted OT positions. Let $m$ be the input length, let $\ell$ be the encoded length, and let $A\in\mathbb{F}_2^{m\times\ell}$ be a public matrix. For the real input $y\in\mathbb{F}_2^m$, sample an encoded input $\widehat y\in\mathbb{F}_2^\ell$ uniformly subject to

$$
A\widehat y=y.
$$

Let $U_t$ denote the uniform distribution over $\mathbb{F}_2^t$. The matrix is chosen such that, for every $S\subseteq[\ell]$ with $|S|\leq k$,

$$
\widehat y_S\mid(A\widehat y=y)\ \equiv\ U_{|S|}.
$$

Therefore the outcomes of at most $k$ corrupted OTs are independent of $y$.

### Authenticated garbling: WRK

**Sharing.**

Let $G$ be the garbler and $E$ the evaluator. For a wire $\omega$, let $v_\omega\in\mathbb F_2$ be its true value. The two parties hold random mask shares $\lambda_\omega^{(G)}$ and $\lambda_\omega^{(E)}$ respectively, and define

$$
\lambda_\omega=\lambda_\omega^{(G)}\oplus\lambda_\omega^{(E)},\qquad
\widehat v_\omega=v_\omega\oplus\lambda_\omega.
$$

$G$ holds a global offset $\Delta^{(G)}\in\mathbb F_2^\kappa$. It chooses $L_{\omega,0}$ for each wire and sets

$$
L_{\omega,1}=L_{\omega,0}\oplus\Delta^{(G)}.
$$

Hence the state $E$ holds on wire $\omega$ is

$$
\left(\widehat v_\omega,L_{\omega,\widehat v_\omega}\right).
$$

where $\widehat v_\omega$ is the masked bit, not $v_\omega$; this pair $(\widehat v_\omega,L_{\omega,\widehat v_\omega})$ is all the information $E$ holds on wire $\omega$, consistent with the convention from Point-and-Permute at the very beginning that "a label is a pair".

The two parties also hold global MAC keys $\Delta^{(G)}$ and $\Delta^{(E)}$ respectively. $\Delta^{(G)}$ here is **the same object** as the label offset in the FreeXOR sense above—WRK is designed so that $G$'s label offset also serves as the MAC key used when "$G$ authenticates a value held by $E$", so that two separate global offsets need not be maintained. $\Delta^{(E)}$, by contrast, is purely a MAC key: $E$ does not garble, so there is no corresponding label structure to reuse. The mask share $\lambda_\omega^{(G)}$ held by $G$ is authenticated by $E$:

$$
M_\omega^{(G)}
=K_\omega^{(E)}\oplus\lambda_\omega^{(G)}\Delta^{(E)}.
$$

The mask share $\lambda_\omega^{(E)}$ held by $E$ is authenticated by $G$:

$$
M_\omega^{(E)}
=K_\omega^{(G)}\oplus\lambda_\omega^{(E)}\Delta^{(G)}.
$$

The superscript indicates the holder; the subscript $\omega$ indicates that these values belong to wire $\omega$. A lot of overloaded notation follows: $M_g$ denotes the MAC associated with gate $g$ (a Latin letter), $M_\omega$ denotes the MAC associated with wire $\omega$ (a Greek letter), and $M_{g,p,q}$ denotes the MAC associated with gate $g$ with inputs $p,q\in\{0,1\}$ respectively. In the WRK protocol, every shared value $x$ must be authenticated in the following form:

$$
x=x^{(G)}\oplus x^{(E)},\quad
M_x^{(G)}
=K_x^{(E)}\oplus x^{(G)}\Delta^{(E)},\quad
M_x^{(E)}
=K_x^{(G)}\oplus x^{(E)}\Delta^{(G)}.
$$

Above we have already shared the mask $\lambda_\omega$ of each wire; later we will also share $\lambda_\alpha\lambda_\beta$, which is associated with the gate, hence the subscript $g$; and we will share $r_{g,p,q}$, which is associated with the gate's two input values, hence the subscript $g,p,q$.

If $G$ flips $\lambda_\omega^{(G)}$, it must also compute

$$
M_\omega^{(G)}\oplus\Delta^{(E)}.
$$

Since $G$ does not know $\Delta^{(E)}$, a forgery succeeds with probability $2^{-\kappa}$. The other direction is analogous.

**Garbling.**

Consider an AND gate $g$ with input wires $\alpha,\beta$ and output wire $\gamma$.

For the row selected by masked input bits $(p,q)$, let $r_{g,p,q}$ denote the masked output that this row should produce. Then

$$
\begin{aligned}
r_{g,p,q}
&=(p\oplus\lambda_\alpha)(q\oplus\lambda_\beta)
  \oplus\lambda_\gamma\\
&=pq\oplus p\lambda_\beta\oplus q\lambda_\alpha
  \oplus\lambda_\alpha\lambda_\beta\oplus\lambda_\gamma.
\end{aligned}
$$

The only nonlinear term is $\lambda_\alpha\lambda_\beta$. We assume that preprocessing can already provide an authenticated sharing of $t=\lambda_\alpha\lambda_\beta$—this sharing comes from $\mathcal F_{\mathrm{pre}}$ in the preprocessing phase (an OT-extension-based, TinyOT-style authenticated AND triple generation protocol). This is the **only** source of nonlinear / OT cost in the whole protocol: once these triples are obtained, all remaining online computation consists of linear XOR combinations.

$$
t=t^{(G)}\oplus t^{(E)},\quad
M_g^{(G)}
=K_g^{(E)}\oplus t^{(G)}\Delta^{(E)},\quad
M_g^{(E)}
=K_g^{(G)}\oplus t^{(E)}\Delta^{(G)}.
$$

From this the two parties obtain sharings of $r_{g,p,q}$:

$$
\begin{aligned}
r_{g,p,q}^{(G)}
&=pq
  \oplus p\lambda_\beta^{(G)}
  \oplus q\lambda_\alpha^{(G)}
  \oplus t^{(G)}
  \oplus\lambda_\gamma^{(G)},\\
r_{g,p,q}^{(E)}
&=p\lambda_\beta^{(E)}
  \oplus q\lambda_\alpha^{(E)}
  \oplus t^{(E)}
  \oplus\lambda_\gamma^{(E)}.
\end{aligned}
$$

For this sharing to be authenticated, for each row $(p,q)$ the two parties must respectively hold

$$
\begin{aligned}
M_{g,p,q}^{(G)}
&=K_{g,p,q}^{(E)}\oplus r_{g,p,q}^{(G)}\Delta^{(E)},\\
M_{g,p,q}^{(E)}
&=K_{g,p,q}^{(G)}\oplus r_{g,p,q}^{(E)}\Delta^{(G)}.
\end{aligned}
$$

How do we obtain $M_{g,p,q}^{(G)},M_{g,p,q}^{(E)},K_{g,p,q}^{(G)},K_{g,p,q}^{(E)}$ satisfying these conditions? The answer is to combine the keys and MACs each party already has.

$$
\begin{aligned}
M_{g,p,q}^{(G)}
&=pM_\beta^{(G)}
  \oplus qM_\alpha^{(G)}
  \oplus M_g^{(G)}
  \oplus M_\gamma^{(G)},\\
M_{g,p,q}^{(E)}
&=pM_\beta^{(E)}
  \oplus qM_\alpha^{(E)}
  \oplus M_g^{(E)}
  \oplus M_\gamma^{(E)},\\
K_{g,p,q}^{(G)}
&=pK_\beta^{(G)}
  \oplus qK_\alpha^{(G)}
  \oplus K_g^{(G)}
  \oplus K_\gamma^{(G)},\\
K_{g,p,q}^{(E)}
&=pK_\beta^{(E)}
  \oplus qK_\alpha^{(E)}
  \oplus K_g^{(E)}
  \oplus K_\gamma^{(E)}
  \oplus pq\Delta^{(E)}.
\end{aligned}
$$


Let $g$ be the gate identifier and $H$ the hash function used for garbling. To avoid accidentally reusing the same hash query across different gates, or across different rows of the same gate, $(g,p,q)$ is explicitly fed into the hash as a tweak (rather than vaguely writing "one $H_g$ per gate"). For each row $(p,q)$, $G$ computes

$$
Q_{g,p,q}
=L_{\gamma,0}
 \oplus K_{g,p,q}^{(G)}
 \oplus r_{g,p,q}^{(G)}\Delta^{(G)},
$$

and then fills the following four values into the Garbling table:

$$
C_{g,p,q}
=H\left(L_{\alpha,p},L_{\beta,q},g\|p\|q\right)
 \oplus
 \left(
 r_{g,p,q}^{(G)}
 \mathbin\|M_{g,p,q}^{(G)}
 \mathbin\|Q_{g,p,q}
 \right),
\qquad (p,q)\in\mathbb F_2^2.
$$

**Evaluation.**

$E$ holds $(p,L_{\alpha,p})$ and $(q,L_{\beta,q})$, so it can only decrypt row $(p,q)$, obtaining $r_{g,p,q}^{(G)}, M_{g,p,q}^{(G)}, Q_{g,p,q}.$ It first checks

$$
M_{g,p,q}^{(G)}
\stackrel{?}{=}
K_{g,p,q}^{(E)}\oplus r_{g,p,q}^{(G)}\Delta^{(E)}.
$$

If the check passes, $E$ computes the masked bit on the output wire

$$
\widehat v_\gamma
=r_{g,p,q}^{(G)}\oplus r_{g,p,q}^{(E)}
$$

and the corresponding label

$$
\begin{aligned}
Q_{g,p,q}\oplus M_{g,p,q}^{(E)}
&=L_{\gamma,0}
  \oplus K_{g,p,q}^{(G)}
  \oplus r_{g,p,q}^{(G)}\Delta^{(G)}\\
&\quad\oplus K_{g,p,q}^{(G)}
  \oplus r_{g,p,q}^{(E)}\Delta^{(G)}\\
&=L_{\gamma,0}
  \oplus\left(r_{g,p,q}^{(G)}\oplus r_{g,p,q}^{(E)}\right)\Delta^{(G)}\\
&=L_{\gamma,\widehat v_\gamma}.
\end{aligned}
$$

Hence the output state of the AND gate is still

$$
\left(\widehat v_\gamma,L_{\gamma,\widehat v_\gamma}\right).
$$

If a malicious $G$ changes $r_{g,p,q}^{(G)}$, it must also forge $M_{g,p,q}^{(G)}$ without knowing $\Delta^{(E)}$. Moreover, $Q_{g,p,q}$ yields the correct output label only when combined with $M_{g,p,q}^{(E)}$ held by $E$.

This only shows that the opened row cannot be tampered with, but $G$ can perfectly well stuff garbage into the rows that are **not opened**—why does this not constitute selective failure? The key is that the index of the opened row is exactly the $(\widehat v_\alpha,\widehat v_\beta)$ that $E$ actually holds, and $\lambda_\alpha^{(E)}$ in $\widehat v_\alpha=v_\alpha\oplus\lambda_\alpha^{(G)}\oplus\lambda_\alpha^{(E)}$ (and likewise $\lambda_\beta^{(E)}$) is hidden from $G$ and uniformly random. Therefore, whatever the true inputs $v_\alpha,v_\beta$ are, from the malicious $G$'s view the opened row is uniformly distributed over $\mathbb F_2^2$: the probability that $G$ corrupting one row causes an abort is always $1/4$, independent of the true input values. This is exactly the property needed to rule out selective failure attacks; otherwise the authenticity argument would be incomplete.

**Free-XOR.**

As before, we require

$$
L_{\gamma,0}=L_{\alpha,0}\oplus L_{\beta,0},\quad \lambda_\gamma=\lambda_\alpha\oplus\lambda_\beta.
$$

Then

$$
L_{\alpha,p}\oplus L_{\beta,q}=L_{\gamma,p\oplus q}.
$$

**Bootstrapping.**

As in BMR, the question is how $E$ obtains the initial state $(\widehat v_\omega,L_{\omega,\widehat v_\omega})$ on an input wire $\omega$. Since $\lambda_\omega$ is shared, the owner of the input must first obtain the mask share from the other party, and this share must carry a MAC.

If $\omega$ is an input wire of $G$, $E$ sends $(\lambda_\omega^{(E)},M_\omega^{(E)})$ to $G$, and $G$ checks

$$
M_\omega^{(E)}\stackrel{?}{=}K_\omega^{(G)}\oplus\lambda_\omega^{(E)}\Delta^{(G)},
$$

then computes $\widehat v_\omega=v_\omega\oplus\lambda_\omega^{(G)}\oplus\lambda_\omega^{(E)}$ and sends $(\widehat v_\omega,L_{\omega,\widehat v_\omega})$ to $E$. All a malicious $G$ can do here is change $\widehat v_\omega$, which is equivalent to switching to a different input of its own and does not constitute an attack.

If $\omega$ is an input wire of $E$, it is the other way around: $G$ sends $(\lambda_\omega^{(G)},M_\omega^{(G)})$ to $E$, $E$ checks it using $K_\omega^{(E)},\Delta^{(E)}$, then computes $\widehat v_\omega$ and sends it to $G$, and $G$ replies with $L_{\omega,\widehat v_\omega}$. $G$ obtains only the masked bit, and $\lambda_\omega^{(E)}$ is hidden from it, so $v_\omega$ is not leaked. If $G$ replies with a wrong label, the rows $E$ decrypts at subsequent gates cannot pass the MAC check, which can only lead to an abort, and whether an abort occurs is independent of $v_\omega$, so there is no selective failure.

**Output.**

For an output wire $\omega$, $E$ already holds $\widehat v_\omega$. $G$ sends $(\lambda_\omega^{(G)},M_\omega^{(G)})$ to $E$, and $E$ checks it and computes

$$
v_\omega=\widehat v_\omega\oplus\lambda_\omega^{(G)}\oplus\lambda_\omega^{(E)}.
$$

If $G$ also needs the output, $E$ symmetrically sends $(\widehat v_\omega,\lambda_\omega^{(E)},M_\omega^{(E)})$ to $G$.

Note that $G$ can already send these to $E$ during Garbling; one can say that if the goal is only for the Evaluator to learn the result, the opening requires no Online communication.

### WRK in $n$ parties

Let $P_1$ be the evaluator and $P_2,\dots,P_n$ the garblers. The two-party case corresponds to $P_1=E$, $P_2=G$.

Notation follows the earlier conventions: superscript $(i)$ denotes the holder, and the subscript denotes which wire / gate the value belongs to. The only addition is the **authentication direction**: in the two-party case "who authenticates whom" need not be written (there is only one other party), but with $n$ parties it must be, so we add $i\to j$ to the subscript, meaning "$P_i$'s share, authenticated by $P_j$ using $\Delta^{(j)}$". Thus

$$
M^{(G)}_{x}=K^{(E)}_{x}\oplus x^{(G)}\Delta^{(E)}
\qquad\longrightarrow\qquad
M^{(i)}_{i\to j,\,x}=K^{(j)}_{i\to j,\,x}\oplus x^{(i)}\Delta^{(j)} .
$$

**Sharing.**

Each party $P_i$ holds a global $\Delta^{(i)}\in\mathbb F_2^\kappa$. For $i\ge 2$ it is both a label offset and a MAC key (exactly the same dual role as $\Delta^{(G)}$ in the two-party case); $\Delta^{(1)}$ is purely a MAC key, since the evaluator does not garble.

For a wire $\omega$,

$$
\lambda_\omega=\bigoplus_{i=1}^{n}\lambda^{(i)}_\omega,\qquad
\widehat v_\omega=v_\omega\oplus\lambda_\omega,
$$

each garbler $P_i\ (i\ge 2)$ chooses its own $L^{(i)}_{\omega,0}$ and sets $L^{(i)}_{\omega,1}=L^{(i)}_{\omega,0}\oplus\Delta^{(i)}$. Note that the $n-1$ sets of labels share **the same** $\widehat v_\omega$ as their index—this is the only mechanism gluing the label domains of the garblers together. The state of $P_1$ on wire $\omega$ is

$$
\left(\widehat v_\omega,\ L^{(2)}_{\omega,\widehat v_\omega},\ \dots,\ L^{(n)}_{\omega,\widehat v_\omega}\right).
$$

**Authentication.**

Every shared value $x=\bigoplus_{i=1}^n x^{(i)}$ must have, for **every ordered pair** $i\ne j$,

$$
M^{(i)}_{i\to j,\,x}=K^{(j)}_{i\to j,\,x}\oplus x^{(i)}\Delta^{(j)},
$$

for a total of $n(n-1)$ pieces of material. $P_i$ holds the MAC, $P_j$ holds the key. The forgery argument is unchanged: to flip one bit of $x^{(i)}$, $P_i$ must compute $M^{(i)}_{i\to j,x}\oplus\Delta^{(j)}$ without knowing $\Delta^{(j)}$, which succeeds with probability $2^{-\kappa}$.

**Key lemma.** Rearranging the equation above gives: for any $j$, the parties already hold, with **zero communication**, an XOR sharing of $x\Delta^{(j)}$,

$$
x\,\Delta^{(j)}
=\underbrace{\left(x^{(j)}\Delta^{(j)}\oplus\bigoplus_{i\ne j}K^{(j)}_{i\to j,\,x}\right)}_{P_j\ \text{holds}}
\ \oplus\ \bigoplus_{i\ne j}\underbrace{M^{(i)}_{i\to j,\,x}}_{P_i\ \text{holds}} .
$$

This lemma is the pivot of the whole generalization. In the two-party case $G$ itself knows $r^{(G)}$ and $\Delta^{(G)}$ and can multiply them directly; with $n$ parties no party knows $r$, but the MAC material itself already provides a sharing of this product for free. The pair $Q_{g,p,q}$ and $M^{(E)}_{g,p,q}$ from earlier is exactly the two shares of this lemma for $n=2$.

**Garbling.**

The row value of AND gate $g$ is defined as before:

$$
r_{g,p,q}=(p\oplus\lambda_\alpha)(q\oplus\lambda_\beta)\oplus\lambda_\gamma
=pq\oplus p\lambda_\beta\oplus q\lambda_\alpha\oplus\lambda_\alpha\lambda_\beta\oplus\lambda_\gamma .
$$

The nonlinear term $t=\lambda_\alpha\lambda_\beta$ is still given an authenticated sharing by $\mathcal F_{\mathrm{pre}}$, except that now

$$
\lambda_\alpha\lambda_\beta=\Big(\bigoplus_i\lambda^{(i)}_\alpha\Big)\Big(\bigoplus_j\lambda^{(j)}_\beta\Big)
=\bigoplus_{i,j}\lambda^{(i)}_\alpha\lambda^{(j)}_\beta ,
$$

the diagonal terms are computed locally, and for the $\binom n2$ cross terms each pair runs one OT. This is still the only source of nonlinear / OT cost.

Fix a designated party $P_{i_0}$ to take on the public term $pq$ (in the two-party section above, $i_0=G$). Each party's shares and authentication material are linear combinations of existing material:

$$
\begin{aligned}
r^{(i)}_{g,p,q}
&=[\,i=i_0\,]\,pq
 \oplus p\lambda^{(i)}_\beta
 \oplus q\lambda^{(i)}_\alpha
 \oplus t^{(i)}
 \oplus\lambda^{(i)}_\gamma,\\[2pt]
M^{(i)}_{i\to j,\,g,p,q}
&=pM^{(i)}_{i\to j,\,\beta}
 \oplus qM^{(i)}_{i\to j,\,\alpha}
 \oplus M^{(i)}_{i\to j,\,g}
 \oplus M^{(i)}_{i\to j,\,\gamma},\\[2pt]
K^{(j)}_{i\to j,\,g,p,q}
&=pK^{(j)}_{i\to j,\,\beta}
 \oplus qK^{(j)}_{i\to j,\,\alpha}
 \oplus K^{(j)}_{i\to j,\,g}
 \oplus K^{(j)}_{i\to j,\,\gamma}
 \oplus[\,i=i_0\,]\,pq\,\Delta^{(j)} .
\end{aligned}
$$

The placement of the final $pq\Delta^{(j)}$ correction term follows the same reasoning as in the two-party case: the public constant is added only to $P_{i_0}$'s share, so only the keys that authenticate $P_{i_0}$ need to be shifted accordingly.

The goal is for $P_1$ to recover the output label of **every** garbler

$$
L^{(j)}_{\gamma,\widehat v_\gamma}=L^{(j)}_{\gamma,0}\oplus r_{g,p,q}\,\Delta^{(j)},\qquad j\ge 2 .
$$

Split the right-hand side into $n$ shares using the key lemma. Merging $L^{(j)}_{\gamma,0}$ into $P_j$'s own share gives

$$
Q^{(j)}_{g,p,q}
=L^{(j)}_{\gamma,0}
 \oplus r^{(j)}_{g,p,q}\Delta^{(j)}
 \oplus\bigoplus_{i\ne j}K^{(j)}_{i\to j,\,g,p,q},
$$

The remaining $n-1$ shares are the MACs themselves, i.e. $M^{(i)}_{i\to j,\,g,p,q}$ held by $P_i$. $Q^{(j)}$ is still computable by $P_j$ **purely locally**: it holds all of $L^{(j)}_{\gamma,0},r^{(j)},\Delta^{(j)}$ and those $n-1$ keys. In the two-party case only one term $K^{(G)}_{E\to G,\,g,p,q}$ remains in the sum, reducing to the original $Q_{g,p,q}$.

So each garbler $P_i\ (i\ge2)$ sends one ciphertext per row $(p,q)$, masking all the material it produces with its own labels:

$$
C^{(i)}_{g,p,q}
=H\!\left(L^{(i)}_{\alpha,p},L^{(i)}_{\beta,q},\,g\|p\|q\right)
\oplus
\left(
r^{(i)}_{g,p,q}
\ \big\|\ Q^{(i)}_{g,p,q}
\ \big\|\ \left(M^{(i)}_{i\to j,\,g,p,q}\right)_{j\ne i}
\right).
$$

The two indices here have different meanings and must be kept apart: the superscript $i$ of $C$ is "who sent it", $n-1$ ciphertexts in total; the $j$ in the inner $M^{(i)}_{i\to j}$ is "whose label it is used to complete", $n-1$ terms in total. $P_1$'s own share $M^{(1)}_{1\to j,\,g,p,q}$ is available locally and need not be transmitted.

> Comparison with BMR: structurally this is BMR's "one label segment per garbler, concatenated and handed to a single evaluator", but BMR needs to run a generic MPC to generate the table, whereas here, since $\lambda_\alpha\lambda_\beta$ has already been handled in preprocessing, every entry of the table is just an XOR of local values, and the garbling phase involves no interactive computation.

**Evaluation.**

$P_1$ takes $(p,q)=(\widehat v_\alpha,\widehat v_\beta)$ and decrypts each $C^{(i)}_{g,p,q}$ using the $L^{(i)}_{\alpha,p},L^{(i)}_{\beta,q}$ it holds. The other rows cannot be opened: as long as there exists one honest garbler $P_i$, $P_1$ lacks $L^{(i)}_{\alpha,1\oplus\widehat v_\alpha}$, so security still holds under all-but-one corruption.

**Verification.** For each $i\ge 2$, after locally computing $K^{(1)}_{i\to 1,\,g,p,q}$, check

$$
M^{(i)}_{i\to 1,\,g,p,q}
\stackrel{?}{=}
K^{(1)}_{i\to 1,\,g,p,q}\oplus r^{(i)}_{g,p,q}\Delta^{(1)} .
$$

**Masked bit.**

$$
\widehat v_\gamma=\bigoplus_{i=1}^{n} r^{(i)}_{g,p,q}.
$$

**Label.** For each $j\ge 2$, sum the $n$ shares (the keys cancel term by term):

$$
\begin{aligned}
Q^{(j)}_{g,p,q}\oplus\bigoplus_{i\ne j}M^{(i)}_{i\to j,\,g,p,q}
&=L^{(j)}_{\gamma,0}
 \oplus r^{(j)}_{g,p,q}\Delta^{(j)}
 \oplus\bigoplus_{i\ne j}K^{(j)}_{i\to j,\,g,p,q}\\
&\quad\oplus\bigoplus_{i\ne j}\left(K^{(j)}_{i\to j,\,g,p,q}\oplus r^{(i)}_{g,p,q}\Delta^{(j)}\right)\\
&=L^{(j)}_{\gamma,0}\oplus\Big(\bigoplus_{i=1}^{n} r^{(i)}_{g,p,q}\Big)\Delta^{(j)}\\
&=L^{(j)}_{\gamma,\widehat v_\gamma}.
\end{aligned}
$$

So the state returns to $\left(\widehat v_\gamma,\{L^{(j)}_{\gamma,\widehat v_\gamma}\}_{j\ge2}\right)$. For $n=2$ only $M^{(E)}_{E\to G,\,g,p,q}$ remains in the sum, which is exactly the three-line derivation earlier.

**Two changes in security.** First, the selective failure argument carries over: the index $(\widehat v_\alpha,\widehat v_\beta)$ of the opened row contains an honest party's $\lambda^{(i)}_\alpha,\lambda^{(i)}_\beta$, which are uniformly random to the corrupted parties, so the probability that tampering with a row causes an abort is always $1/4$, independent of the true inputs. Second, $P_1$ can only verify MACs in the $j=1$ direction; it cannot verify the cross MACs $M^{(i)}_{i\to j}$ with $j\ne 1$ (it does not know $K^{(j)}_{i\to j}$). If a corrupted $P_i$ flips one bit of one of them, $P_j$'s output label becomes wrong, with the consequence that the row decrypted at the next gate fails the MAC check and the protocol aborts—this is likewise independent of the true values, so it is only an abort and not selective failure.

**Free-XOR.**

$$
L^{(i)}_{\gamma,0}=L^{(i)}_{\alpha,0}\oplus L^{(i)}_{\beta,0},\quad
\lambda^{(i)}_\gamma=\lambda^{(i)}_\alpha\oplus\lambda^{(i)}_\beta,
$$

MACs and keys are XORed term by term in sync. The $\Delta^{(i)}$ must be **mutually independent and secret**: if all garblers shared one global $\Delta$, then any single corrupted garbler colluding with $P_1$ could obtain both labels on some wire, and obliviousness would immediately fail.

**Bootstrapping.**

Let input wire $\omega$ belong to $P_k$. Every other party $P_i\ (i\ne k)$ sends $(\lambda^{(i)}_\omega,M^{(i)}_{i\to k,\,\omega})$ to $P_k$, and $P_k$ checks each one

$$
M^{(i)}_{i\to k,\,\omega}\stackrel{?}{=}K^{(k)}_{i\to k,\,\omega}\oplus\lambda^{(i)}_\omega\Delta^{(k)} ,
$$

then broadcasts $\widehat v_\omega=v_\omega\oplus\bigoplus_i\lambda^{(i)}_\omega$; finally each garbler $P_j\ (j\ge2)$ sends $L^{(j)}_{\omega,\widehat v_\omega}$ to $P_1$. Two flights in total, and the first step is independent of the input value and can be moved into preprocessing.

If the value on this wire is eventually public, all $n$ shares of $\lambda_\omega$ can be opened in advance; afterwards, as soon as $v_\omega$ appears, each garbler immediately computes $\widehat v_\omega$ locally and sends the label directly, saving the middle round.

**Output.**

For an output wire $\omega$, each garbler $P_j\ (j\ge2)$ sends $(\lambda^{(j)}_\omega,M^{(j)}_{j\to 1,\,\omega})$ to $P_1$, and $P_1$ checks them and computes

$$
v_\omega=\widehat v_\omega\oplus\bigoplus_{i=1}^{n}\lambda^{(i)}_\omega .
$$

As in the two-party case, this material is independent of the inputs and can be sent already in the garbling phase, so if only the evaluator needs to learn the result, the opening requires no online communication.

**Cost.**

Each authenticated bit requires $n(n-1)$ MACs/keys. The ciphertext payload per AND gate, per row, per garbler is $1+n\kappa$ bits (one bit for $r^{(i)}$, one $\kappa$ for $Q^{(i)}$, and $n-1$ cross MACs), so the total communication per AND gate is

$$
4(n-1)(1+n\kappa)=\Theta(n^2\kappa).
$$

XOR gates are free. The real dominant cost is in preprocessing: authenticated AND triple generation among the $\binom n2$ pairs.

It should be emphasized that this $n^2$ is not $\binom n2$ independent two-party WRK instances glued together—that would fail, because if a separate two-party protocol were run for each $(P_i,P_1)$, its mask would only be $\lambda^{(i)}\oplus\lambda^{(1)}$, and $P_1$ colluding with $P_i$ could recover all true values on that circuit. A single $n$-out-of-$n$ mask $\lambda_\omega=\bigoplus_i\lambda^{(i)}_\omega$ must be used, and this immediately forces every row to be produced jointly by all parties. The two indices here range over different objects: $n-1$ label domains $\times$ $n$ share holders.

