# /marketing write-post — Blog post / LinkedIn post

## Purpose
Write a piece of content that the target reads all the way through and that converts.

## Input
- Topic · format (SEO blog / LinkedIn) · target persona · desired CTA
- Ideally: a slot from the current content plan

## Steps
1. Load the tone of voice (`marketing/brand/`), the positioning, and what we have already
   written on the topic (`marketing/content/index.md` + `blog/`).
2. **Angle**: start from the reader's problem, not from the product. For SMBs: simple
   language, zero unexplained acronyms. For partners: revenue and differentiation.
3. **Blog structure**: hook (real problem) → development with data/examples (cited source)
   → our point of view → single CTA. Title + meta description for SEO, natural keyword,
   scannable H2/H3. **LinkedIn**: hook in the first line, short paragraphs,
   one single idea, closing CTA.
4. **Verify claims**: every statement about features → shipped (zone `prodotto`); every
   security recommendation → we follow it ourselves too (zone `compliance`); every number
   → source.
5. Classify `tier: 🟢` only if it contains no internal data; otherwise it stays 🟡 and is
   not published until it has been redacted.
6. Update `content/index.md`; actual publication follows PREPARE → APPROVE → EXECUTE.

## Output format
```markdown
---
zone: marketing
tier: 🟢
type: blog-post
persona: {…}
keyword: {…}
status: draft            # draft → review → published
---
# {Title}
{meta-description}
{body}
**CTA**: {…}
```

## Destination
Zone `marketing` → `blog/{slug}.md`. Commit (admin): `[marketing] content: {slug}`.

## Handoff
Technical post → co-sign `cto`/`ceo` if it adds credibility · enablement → `sales`.
