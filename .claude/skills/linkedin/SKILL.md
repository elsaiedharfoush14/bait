---
name: linkedin
description: Write and publish LinkedIn posts, value-adding comments, and a new Headline/About for Eng. Elsayed via the Composio connector. Use when he asks for a LinkedIn post, comment, or profile rewrite (بوست لينكدإن، كومنت، ظبط البروفايل).
---

# LinkedIn via Composio

Source: `Vidaaieg/claude-linkedin-composio-prompts` (Steven Ayman — Vida AI).

## Setup (once)
1. Needs the **Composio** connector in Claude (check with `ToolSearch` "composio linkedin").
   Missing → tell him to add it from the Connectors settings; don't fake it.
2. Ask Composio to connect LinkedIn → give him the login link, he logs in once.
3. Company page posting needs him to be **Admin** on that page; otherwise personal profile only.

## Hard rules
- **Never publish or comment without his explicit «انشر» / pick.** Always show the final text first.
- Few actions per day — bursts look automated and LinkedIn notices.
- Profile (Headline/About) can't be edited by external tools: give the text, he pastes it.
- If a post link can't be read, ask him to paste the post text.

## 1. Repurpose content → post
Input: reel/video script or idea (+ optional company page name).
- A first line that stops the scroll (strong, no clickbait)
- Short lines, lots of white space (mobile)
- One clear lesson/result, with a concrete number/example if given
- End with a question inviting comments
- 3–5 relevant hashtags, under 1,300 characters, founder's voice
- Too corporate → «make it sound more like me talking».
Show → wait for «انشر» → post on personal profile [+ company page].

## 2. Comments with real value (not "Great post!")
Input: post link or text + who he is (e.g. engineer / founder of …).
- 3 options, each a different angle: practical tip, short personal experience, or smart follow-up question
- 2–4 sentences, natural, not salesy; no generic praise, no emoji spam, no pitching
Wait for his pick → post only that one under the post.

## 3. Headline + About
Input: current Headline, About, what he does / who he helps, who to attract (clients / recruiters / partners), language.
1. 3 headline options (≤220 chars): who he helps + result + proof if possible
2. New About (≤2,600 chars): strong first 2 lines, what he does, results/proof, who it's for, clear CTA
3. Show as Before → After.
