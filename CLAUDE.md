# مصاريف البيت (Bait) — handover for Claude Code

Household-expenses PWA for **Eng. Elsayed Harfoush**'s wife (iPhone). Sister app of «عهدة UUES»
(`C:\Users\United\Downloads\PETTY CASH APP`, repo `elsaiedharfoush14/uues-petty-cash`) — same voice parser,
mic, receipt reader, backup, QR install, offline-safe service worker. Reply to him in **Egyptian Arabic**;
the app's UI speaks to a woman (feminine forms: قولي، ضيفي، صرفتي). Do the work yourself (git / gh / tests).

- Live: https://elsaiedharfoush14.github.io/bait/ — repo `elsaiedharfoush14/bait` (public), Pages from `main` /.
- Currency SAR. He chose: monthly budget (+ optional limit per category). He did NOT choose PDF report /
  month comparison / fixed bills (ask before adding).

## Files
`index.html` (whole app) · `sw.js` (`CACHE='bait-vN'`, never answers empty → «النت مش واصل» page) ·
`version.json` · `manifest.webmanifest` · `icon-*.png`, `apple-touch-icon.png`, `maskable-512.png` (house + «ر.س» coin) ·
`qr-install.png` (→ `…/bait/?i=1`, made with `E:\Work\Automation_Tools\petty_cash_app\qrgen.py`, check with jsQR).

## Release (all three, then push, then `gh run list --repo elsaiedharfoush14/bait --limit 1` once)
`APP_VER` in index.html · `version.json` · `CACHE` in sw.js (N+1). Commit email `332831565+elsaiedharfoush14@users.noreply.github.com`.

## Data
`localStorage['bait_v1']` = `{expenses:{id:{id,date,cat,amount,memo,t}}, budget, budgets:{'YYYY-MM':n}, limits:{cat:n}}`;
`bait_bk` = last backup time (weekly backup screen), `bait_bk_snooze`. Phone-only; ask for a backup file to debug.

## Voice
`parseSpeech()` = petty-cash number engine (Egyptian number words, «ونص», formal «ستة عشر»), label = words before
the amount (kept as `memo`), `catOf()` via `CATS[].w` keywords (never put «ميه» in a category — it is 100);
«امبارح / النهارده / يوم 3 [أكتوبر]» date the items around them (`itemDate`, relative to the month on screen).
Mic: iPhone `ar-SA` (iOS has no ar-EG), stays on until tapped, adds on stop or on spoken «ضيفيها».

## Test
`python E:\Work\Automation_Tools\bait_app\savesrv.py` → http://localhost:8766 (POST /save → bait_app\out);
built-in browser mobile preset; fake SpeechRecognition; iPhone checks via an iframe with an iPhone userAgent.
