# THE DAILY PICTURE — Friday 20 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Reki120/news-image-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Reki120/news-image-20261120/reward.svg)](https://make.fun/c/news-image-20261120)

One image that sums up the world news of **Friday 20 November 2026**, drawn as a
newspaper front page. The lead story: **Russia hits Kyiv bridges; missiles cross
into Poland** — overnight strikes killed 8 people and injured 28 across nine
regions of Ukraine, while two missiles and a drone violated Poland's airspace.
Around it, the day in brief: Estonia closes its border with Russia for at least
six months as Moscow cries "Iron Curtain"; the EU–UK summit in Brussels agrees a
youth mobility scheme for up to 100,000 young people a year each way; US Senate
Republicans block (51–48) a move to end the Iran war; stocks fall a fifth
straight day on AI-valuation doubts (S&P 500 about −2%, Nikkei −4.8%) despite
Anthropic's record IPO debut (+17%); COP31 negotiators in Antalya drop any call
to phase out fossil fuels; Kenya discharges its last Ebola patient, 37 days
after its first case; and Haiti's police say 34 suspected gang members were
killed.

The image is drawn programmatically with Python + Pillow (`draw_entry.py`) —
no external images, no network — and is fully deterministic: two runs produce
byte-identical PNG output (1024×1024, under 1 MiB).

## Run it

```sh
python3 draw_entry.py   # draws entry.png (1024x1024) next to the script
node main.ts            # validates entry.png, copies it to /output/entry.png
```

Set `MAKEFUN_OUTPUT_DIR` to copy somewhere else:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts
```

`main.ts` (Node 22, standard library only) checks the PNG signature, the IHDR
chunk (length, type, CRC-32, 1024×1024, bit depth 8, colour type 2 or 6), walks
every chunk verifying each CRC, requires a final IEND with no trailing bytes,
enforces the 1 MiB limit, then copies atomically (temp file + rename) and
re-checks the copied size.

## License

MIT — see [LICENSE](LICENSE).

---

Entered on make.fun (https://make.fun/?ref=rwf799wr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards.
