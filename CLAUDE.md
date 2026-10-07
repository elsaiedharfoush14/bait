# مصاريف البيت (Bait) — handover for Claude Code

Household-expenses PWA for **Eng. Elsayed Harfoush**'s wife (iPhone). Sister app of «عهدة UUES»
(`C:\Users\United\Downloads\PETTY CASH APP`, repo `elsaiedharfoush14/uues-petty-cash`) — same voice parser,
mic, receipt reader, backup, QR install, offline-safe service worker. Reply to him in **Egyptian Arabic**;
the app's UI speaks to a woman (feminine forms: قولي، ضيفي، صرفتي). Do the work yourself (git / gh / tests).

- Live: https://elsaiedharfoush14.github.io/bait/ — repo `elsaiedharfoush14/bait` (public), Pages from `main` /.
- Currency SAR. He chose: monthly budget (+ optional limit per category). He did NOT choose PDF report /
  month comparison / fixed bills (ask before adding).

## v2026.10.07.1 (2026-10-07) — his request «اعمل المزامنة… وكمّل التطبيق»
Sync, who-spent (`WHO`, `e.by`), fixed monthly bills (`D.bills`, paid = an expense with `bill:id` that month),
6-month chart + last-month compare, smart alerts, photo per expense (IndexedDB `bait`/photos, not synced),
month report A4 pictures + Excel (local `exceljs.min.js`), own categories (`D.cats`), splash + tour, back button
closes sheets (`openOv/closeOv` + history).
**Sync**: Firebase project `bait-sync` (his Google account, created by me with his OK; his own project
«Planning With AI» untouched). Anonymous auth ON, Firestore (eur3, Standard, production mode). One doc per family
`families/{id}` with field `d` = AES-GCM sealed JSON (key only in the phones, passed by QR / link `#join=id.key`),
records merged by `u` (deletions = `{id,del:1,u}`), settings by `setU`. REST only (no SDK): `fbToken`, `pull`, `push`.
**Security rules must be pasted by HIM** (the auto-mode classifier refused me opening the Rules page — don't retry):
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /families/{fid} {
      allow get: if request.auth != null && fid.size() >= 20;
      allow create, update: if request.auth != null && fid.size() >= 20
        && request.resource.data.keys().hasOnly(['d','u'])
        && request.resource.data.d is string && request.resource.data.d.size() < 900000;
    }
  }
}
```
Until then the app shows «مش متزامن» (403) and retries by itself.

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
