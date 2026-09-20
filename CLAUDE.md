# Notes repo conventions

Source of truth is `md/`; `files/*.html` is built with

```bash
python3 _tools/md2html.py md/<name>.md
```

Rebuild after every edit to a `.md`.

## Scope

- Questions, discussion, “为什么”, “啥意思”, derivations, and fact-checking are read-only. Answer in chat; do not edit `md/`.
- Edit only when explicitly asked.
- Change only the requested span. Do not rewrite neighbouring text.
- The user may edit concurrently. Re-read the target span immediately before editing and preserve intervening changes.
- Keep existing headings unless told otherwise.
- Report every changed span and location after editing.

## Markdown

- Inline math: `$...$`
- Display math:

```markdown
$$
...
$$
```

- Do not introduce `\(...\)` or `\[...\]`.
- Use `aligned` inside `$$...$$` when multiline equations are needed.

## Goal

Write protocol notes that are:

1. self-contained;
2. unambiguous;
3. logically complete;
4. concise.

Preferred order:

> **motivation → mathematical objects → protocol → claim → correctness → security → optional cost**

The reader should be able to reconstruct exactly what the protocol does without guessing any notation or missing logical step.

## Self-contained and unambiguous

This is mandatory.

A reader must never have to guess what a symbol, term, object, primitive, or operation means. Before using something, either it has already been clearly defined nearby, or define it immediately before first use.

Do not make the reader reinterpret notation that has already been learned.

### Stable notation

Once a base symbol is introduced, its subscript structure is fixed.

If the note introduces

$$
X,\qquad X_i,\qquad\text{or}\qquad X_{i,j},
$$

later occurrences of the same base symbol must keep that same subscript structure.

For example, after introducing

$$
X_{i,j},
$$

do not later write

$$
X_{i,j,k}.
$$

If an additional index is genuinely necessary, introduce a different symbol and define it explicitly.

Likewise, if $X$ was introduced without a subscript, do not later turn it into $X_i$ merely to attach extra information.

The reader should learn the shape of a symbol once and never need to reconsider what that symbol denotes.

### Party shares

Parenthesized superscripts are reserved for party shares.

If

$$
X=\bigoplus_{i=1}^n X^{(i)},
$$

then $X^{(i)}$ denotes the share of $X$ held by party $P_i$.

This convention does not change the underlying object's subscript structure. For example, if $M_\omega$ is already defined, then

$$
M_\omega^{(i)}
$$

means party $P_i$'s share of that same object.

Do not use parenthesized superscripts for unrelated meanings.

A symbol should therefore have a stable visual grammar:

$$
\underbrace{X}_{\text{object}}
\quad
\underbrace{_{\omega}}_{\text{fixed subscript structure, if any}}
\quad
\underbrace{^{(i)}}_{\text{party share, if any}}.
$$

Do not later add new indices, bracket arguments, arrows, or decorations to the same base symbol unless that notation was part of its definition from the beginning.

If a genuinely different object needs a different structure, give it a different symbol.

### Local self-containment

At every point, all notation needed to understand the next line should already be available.

Before writing a formula, check:

> Can the reader assign one exact meaning to every symbol and index in this formula?

If not, define the missing object first.

Do not rely on expert convention when two reasonable interpretations are possible.

If a detail is unnecessary and may confuse the reader, omit it. If omitting it makes the logic incomplete, include it and define it precisely.

## High information density

Do not write large prose blocks.

Every sentence should do at least one useful job:

- motivate a construction;
- define an object;
- state who holds something;
- describe an action;
- state a claim;
- explain correctness;
- explain security.

Delete sentences that only repeat, transition, emphasize, or summarize without adding information.

Prefer formulas whenever they express the information more precisely.

Prefer

$$
x=x^{(1)}\oplus x^{(2)},
$$

where $P_i$ holds $x^{(i)}$,

over a paragraph explaining the same relation verbally.

Prefer

$$
P_i\longrightarrow P_j:
\qquad
(m_1,m_2)
$$

over prose saying that $P_i$ sends two previously computed values.

Do not repeat a displayed equation in words.

Use prose only for information the formula does not express clearly.

## Writing a protocol

### 1. Motivation

State briefly:

- what is already available;
- what is missing;
- what this protocol should produce.

Do not start with machinery or background.

### 2. Mathematical objects

Define exactly the objects needed by the protocol.

For every object, make clear when relevant:

- what it means;
- who holds it;
- whether it is public or secret;
- what relation it satisfies.

Every symbol must be defined before first use.

Do not name one-use intermediate values unless the name makes the logic clearer.

### 3. Protocol

Write actions in execution order.

Use numbered steps when there is more than one meaningful action.

Each step should make clear:

1. who acts;
2. what is computed locally;
3. what is sent, broadcast, or opened;
4. what another party receives or learns.

Show important messages explicitly:

$$
P_i\longrightarrow P_j:
\qquad
m.
$$

Do not write vague statements such as:

> The parties exchange the necessary values.

If an earlier primitive is reused, first state the exact functionality currently needed, then show that the earlier primitive provides that functionality.

### 4. Claim

State exactly what the protocol has produced.

For example:

$$
z^{(1)}\oplus z^{(2)}=xy.
$$

Do not leave the output implicit.

### 5. Correctness

Show why the claim holds.

Usually one short identity plus one sentence is enough:

$$
z^{(1)}\oplus z^{(2)}
=
\cdots
=
xy.
$$

Do not expand routine algebra unless the intermediate step is necessary to understand why the protocol works.

### 6. Security

Explain only the relevant security argument.

State concretely:

- what the adversary sees;
- what it does not know;
- what randomness, assumption, primitive, or check prevents leakage or cheating.

Do not replace the explanation with a label such as “this is malicious secure”.

Keep correctness and security separate.

### 7. Cost

Optional.

Include only when requested or already relevant.

Keep it short and derive it directly from the protocol.

## Language

For Chinese notes, use Chinese prose with standard English cryptographic terminology when the English term is clearer.

Keep terms such as:

`correlated OT`, `sharing`, `share`, `MAC`, `key`, `party`, `malicious`, `semi-honest`, `authenticated`, `opening`, `commit`, `hash`, `abort`, `preprocessing`, `setup`, `bit`.

Write `bit`, not “比特”.

Write `party`, not “参与方”, “各方”, “每方”, “所有人”.

Write `sender`, `receiver`, not “发送方”, “接收方”.

Use `prover` and `verifier` only for zero-knowledge proofs and interactive proofs. In MPC, name the checking party by its index ($P_i$) or write “其他 party”; do not write “验证方” or `verifier`.

When a technical term may be unfamiliar, explain it at first use.

Do not introduce terminology merely because it sounds standard or sophisticated.

Section headings stay in English unless explicitly told otherwise.

## Do not

Unless explicitly requested:

- do not add unrelated background;
- do not add variants or generalizations;
- do not add optimizations;
- do not add cost analysis;
- do not add extra security discussion;
- do not introduce unexplained notation;
- do not change a symbol's subscript structure after it has been introduced;
- do not use parenthesized superscripts for meanings other than party shares;
- do not write large prose blocks;
- do not repeat formulas in prose;
- do not turn a simple identity into a long derivation;
- do not use code-internal names as mathematical terminology.

If something is unnecessary and may confuse the reader, leave it out.

If omitting something makes the logic incomplete, include it and define it precisely.

## Code versus protocol

Explain the mathematical protocol first.

If implementation differs, describe the implementation difference separately and cite `file.h`: `function`.

Do not let code-internal notation leak into the mathematical description unless it is genuinely useful.

## Final check

Before finishing, verify:

- Is the motivation clear?
- Is the subsection self-contained?
- Does every symbol have one stable meaning and one stable shape?
- Is every subscript structure fixed from first use?
- Are parenthesized superscripts used only for party shares?
- Could any notation reasonably be interpreted in two ways?
- Is it clear who holds each private value?
- Does every protocol step say who computes and communicates what?
- Is the final claim explicit?
- Is correctness justified?
- Is security justified?
- Can any sentence be deleted without losing information?
- Can any prose be replaced by a clearer formula?
- Did I add anything unnecessary?
- Did I rebuild the HTML?
