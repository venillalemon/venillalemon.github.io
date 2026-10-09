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

## Writing guide

The rules for writing or reviewing a protocol section (notation grammar, section order, density, final checklist) live in the `protocol-notes` skill. Load it with `/protocol-notes` before writing, rewriting, or checking any protocol note in `md/`; do not write a protocol section without it.
