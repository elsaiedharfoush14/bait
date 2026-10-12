# Token kit — توفير التوكنز أوتوماتيك (كل المشاريع، الحسابين)

## التركيب (مرة على كل جهاز / كل حساب)
```
git clone https://github.com/elsaiedharfoush14/bait   (أو git pull لو موجود)
python bait\claude-kit\install.py          # Windows
python3 bait/claude-kit/install.py         # Mac/Linux
```
اختياري: `pip install pillow` (تصغير السكرين شوت). بعدها اقفل Claude Code وافتحه، واتأكد بـ `/hooks` و `/agents`.
التحديث: `git pull` ثم نفس الأمر. لو مش عايز الموديل الافتراضي يتغيّر: `--no-model`.

## بيعمل إيه
| الجزء | الفايدة |
|---|---|
| `hooks/read_guard.py` | يمنع قراية ملف كبير كله (>1500 سطر / 80KB) ويخلّي Claude يقرا الجزء اللي محتاجه بس؛ يمنع الملفات المضغوطة `.min.js`؛ يصغّر أي سكرين شوت أكبر من 1280px |
| `agents/digest.md` (Haiku) | الملفات الكبيرة، اللوجات، PDF، Excel، تصديرات PLC (XML/SCL/ST)، مجموعة سكرين شوتات → ملخص قصير بأرخص موديل |
| `agents/implementer.md` (Sonnet) | التعديلات الواضحة والمتكررة (بلوكات PLC، تاجات HMI، تشغيل الاختبارات) |
| `skills/token-saver` | قواعد اختيار الأداة والموديل، تحجيم المخرجات، ممنوع التكرار والانتظار في لوب |
| `CLAUDE.user.md` | 6 سطور بتتحط في `~/.claude/CLAUDE.md` فتشتغل في كل مشروع من غير ما تطلب |
| settings | `model: opusplan` (Opus وقت التخطيط، Sonnet وقت التنفيذ)، حد لمخرجات MCP والأوامر |
| `audit.py` | `python ~/.claude/kit/audit.py` → حجم CLAUDE.md، السكيلز المتشابهة، عدد سيرفرات MCP |

## قياس
`npx ccusage@latest daily` (صرف كل يوم) · `/context` · `/usage`.
