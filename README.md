# article50-marking-checker

**Is your AI-generated content marked the way the EU AI Act demands?**

A zero-dependency Python CLI that checks files for **machine-readable
marking** of AI-generated content, as required by **Article 50 of the EU AI
Act** (transparency obligations).

What it checks:

| Check | Files | How |
|---|---|---|
| (a) C2PA manifest presence | PNG / JPEG | Parses binary structure for JUMBF/C2PA boxes — PNG `jumb` chunk, JPEG APP11 `JUMBF` / `Common JUMBF` segments, `JUMD`/`C2PA` signatures |
| (b) Watermark / metadata flags | PNG / JPEG | Scans PNG `tEXt`/`iTXt`/`zTXt` chunks and JPEG COM/APP segments for AI markers (`ai-generated`, `c2pa`, `synthetic`, generator tags like `stable diffusion`, `midjourney`, …) |
| (c) Disclosure headers | text files | Looks for machine-readable disclosure markers (`X-AI-Generated`, `Content-Credentials`, `article 50`, …) |

## The problem

Article 50 splits the duty in two:

- **Art. 50(2)** — *providers* of AI systems that generate synthetic content
  must embed machine-readable markings (watermarks / metadata) in the output.
- **Art. 50(4)** — *deployers* who publish AI-generated or manipulated
  content (including deepfakes) must disclose it in a machine-readable way.

**Deadline context:** transparency obligations for providers of certain AI
systems apply from **2 August 2026**; generative AI systems already on the
market get a grace period that ends **2 December 2026** — after that, legacy
systems must carry Article 50 markings too. Every file this tool flags
`FAIL` is a file that would not survive that deadline.

## Install

No dependencies — Python 3.8+ stdlib only.

```bash
git clone https://github.com/Iceman2050/article50-marking-checker.git
cd article50-marking-checker
```

## Usage

```bash
python3 article50_check.py image.png photo.jpg notes.txt
python3 article50_check.py --json assets/        # whole directory, JSON output
```

Exit code `0` = all files pass, `1` = at least one FAIL.

## Example output

```
======================================================================
EU AI ACT - ARTICLE 50 MARKING CHECK
======================================================================
[PASS       ] assets/hero-c2pa.png
              - PNG 'jumb' (JUMBF/C2PA) box present
              duties: Art. 50(2) provider machine-readable marking; Art. 50(4) deployer disclosure (if published)
              note: Strong machine-readable marking found (C2PA/JUMBF or disclosure header).
[PASS (weak)] assets/thumb.jpg
              - JPEG segment 0xFE contains marker 'ai-generated'
              duties: Art. 50(2) provider machine-readable marking (partial)
              note: Only keyword/generator metadata found - consider adding C2PA manifest.
[FAIL       ] assets/old-banner.png
              duties: Art. 50(2) provider machine-readable marking; Art. 50(4) deployer disclosure (if published)
              note: No machine-readable AI marking detected.
======================================================================
3 file(s) checked, 1 FAIL
```

Verdict levels: `PASS` (C2PA/JUMBF manifest or disclosure header),
`PASS (weak)` (keyword/generator metadata only — add a C2PA manifest),
`FAIL` (no machine-readable marking).

## Tests

```bash
python3 -m unittest test_article50_check -v
```

Two test layers, both stdlib-only:

```bash
python3 -m unittest test_article50_check -v   # programmatic fixtures + CLI tests
python3 -m pytest tests/ -q                   # real-file fixtures under tests/fixtures/
```

`tests/fixtures/` holds real binary files: minimal valid PNG with C2PA
JUMBF chunk → PASS; minimal plain PNG → FAIL; minimal JPEG with APP11
JUMBF segment → PASS; minimal plain JPEG (SOI+EOI) → FAIL; text with
disclosure header → PASS; plain text → FAIL — each checked via
`check_file()`, plus Article 50 duty-mapping checks and a CLI run over
the fixtures directory. The legacy root suite additionally covers
`tEXt`-marker PNG → PASS (weak) and CLI exit-code / `--json` tests.

## What this tool does NOT do

- It verifies **presence of markings**, not their cryptographic validity
  (it does not validate C2PA signatures against a trust list).
- It is a compliance *aid*, not legal advice. When in doubt, talk to counsel.

## License

MIT — see [LICENSE](LICENSE).

## Built by Ingenious AI

This tool is built and maintained by **Ingenious AI**. Get early access to our AI security platforms:

- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20DisclosureGuard
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20ModelMinder
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20TermsWatch
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20Vibe-Code%20Audit
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20Rogue-Agent%20Defense
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20BreachHunter
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20ChatBreaker
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20Agent%20Flight%20Recorder
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20Agent%20Auth%20Gateway
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20DomainGuard
- https://wa.me/5016691053?text=Hi%20Ingenious%20AI!%20I%20want%20early%20access%20to%20ContentCraft%20AI


> Built by Ingenious AI with Muse — get free tokens with invite code `2HCQH1`
