# The World Today — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/qiyuequkanhai/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/qiyuequkanhai/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page for the make.fun `news-image-20261121` bounty,
generated from scratch with pure Python standard library code. The image
is drawn entirely in code (a hand-built 5x7 bitmap font, a drawn night
skyline over Kyiv, and a small bar chart of Friday's market falls) —
no external images, no network at build time.

## Stories on the front page

All facts were verified against reporting published on 21 November 2026.

1. **Lead — Russia's biggest November barrage hits Ukraine; missiles
   land in Poland.** Russia fired 404 drones and 111 missiles at Ukraine
   overnight on 19–20 November, its biggest strike package of the month.
   At least eight people were killed in Kyiv, where three bridges were
   damaged. Two missiles and a jet-powered drone came down inside Poland;
   Prime Minister Donald Tusk called it a deliberate provocation.
   (Sources: AP, CBS News, France 24, SOFX, Majik Morning Brief.)
2. **World Court finds Myanmar guilty of genocide.** In a landmark 9–6
   judgment on 19 November, the International Court of Justice held
   Myanmar responsible for genocide against the Rohingya — the first
   time the court has found a state responsible for committing genocide —
   and ordered reparations and a safe, voluntary return.
   (Sources: Human Rights Watch, UN News, The Hindu.)
3. **AI sell-off pushes the S&P 500 into correction.** US stocks fell
   sharply on Friday as a sell-off in AI and chip shares pushed the
   S&P 500 down 3.7% into correction territory; the Nasdaq slid about
   5%. Anthropic, which debuted on Wall Street this week near a
   $2 trillion market value after the biggest IPO in history, stumbled
   in early trading. (Sources: The New York Times, One Turn News.)
4. **Climate talks run past deadline in Antalya.** The COP31 UN climate
   summit ran into overtime as nearly 200 nations failed to agree on a
   final deal; a new draft dropped explicit promises to move away from
   coal, oil and gas. (Sources: One Turn News, The Climate Watch.)
5. **UK and EU sign biggest post-Brexit deal.** Prime Minister Andy
   Burnham and EU leaders signed three agreements in Brussels on food
   exports, carbon markets and youth mobility; most food checks end in
   2028. (Sources: The New York Times, Daily Perspective.)
6. **Briefs — Shenzhen summit; Peru quake.** Trump, Xi and Putin met for
   90 minutes in Shenzhen and signed a four-point peace declaration that
   said nothing about Ukraine. A magnitude 6.8 earthquake shook central
   Peru; no deaths or major damage were reported.
   (Sources: RTHK, Kalinga TV, The Hindu.)

## How to run

```sh
# 1. Render the front page (writes entry.png, 1024x1024, pure stdlib)
python3 tools/build_image.py

# 2. Copy it to the make.fun output directory
MAKEFUN_OUTPUT_DIR=/path/to/out python3 main.py
```

`main.py` only copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.
Running it twice produces byte-identical output.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qvhhz6jz&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
