# Skapa egna pipes i Screenpipe

> Pipes är Screenpipes superkraft — schemalagda mini-agenter som gör saker automatiskt åt dig.
> Den här guiden tar dig från noll till din första egna pipe.

---

## Vad är en pipe?

En pipe är en liten textfil som Screenpipe läser och kör automatiskt.

Du skriver i filen:
- **När** ska den köras (varje timme, varje dag klockan 08:00, precis 13:37...)
- **Vad** ska den göra (sammanfatta din dag, skicka en notis, hämta dina mejl...)

Det är allt. Ingen kompilering, inget bygge. En textfil.

---

## Var sparar man pipes?

Pipes bor i en speciell mapp på din dator:

**Windows:**
```
C:\Users\DITT_NAMN\.screenpipe\pipes\
```

**Linux / macOS:**
```
~/.screenpipe/pipes/
```

Varje pipe är en egen mapp med en fil som heter `pipe.md`.

---

## Strukturen i en pipe-mapp

```
~/.screenpipe/pipes/
└── min-pipe/
    ├── pipe.md      ← den viktigaste filen
    ├── .env         ← API-nycklar och hemligheter (om du behöver det)
    └── output/      ← här hamnar pipe-resultaten
```

---

## Hur ser en pipe.md ut?

```yaml
---
name: min-pipe
schedule: every 30m
enabled: true
---

Kolla vad jag jobbat med de senaste 30 minuterna.
Skriv en kort summering till ./output/
```

Överst har vi **YAML-frontmatter** (inställningarna, mellan `---`).
Under det har vi **prompten** — instruktionerna till AI:n.

---

## Schemaläggning — när ska pipen köras?

| Format | Exempel | Förklaring |
|--------|---------|------------|
| Intervall | `every 30m` | Var 30:e minut |
| Intervall | `every 2h` | Varannan timme |
| En gång om dagen | `daily` | En gång per dag |
| Cron-syntax | `0 8 * * 1-5` | Vardag klockan 08:00 |
| Cron-syntax | `37 13 * * *` | Varje dag klockan 13:37 |
| Manuell | `manual` | Körs bara när du triggar den själv |

> **Cron-syntax** följer standarden `minut timme dag månad veckodag`.
> Det är exakt samma som Linux cron — känner du den, kan du det här.

---

## Hantera dina pipes

Via terminalen:

```bash
# Lista alla installerade pipes
npx -y screenpipe@latest pipe list

# Aktivera en pipe
npx -y screenpipe@latest pipe enable min-pipe

# Stäng av en pipe
npx -y screenpipe@latest pipe disable min-pipe

# Kör en pipe manuellt (för att testa)
npx -y screenpipe@latest pipe run min-pipe

# Visa loggar
npx -y screenpipe@latest pipe logs min-pipe
```

---

## Exempel 1 — 13:37 leet-notis ⏰

Den viktigaste pipen. Den bevisar att du förstår cron-syntax och har prioritet.

Skapa mappen och filen:

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\.screenpipe\pipes\leet-time"
```

**Linux / macOS:**
```bash
mkdir -p ~/.screenpipe/pipes/leet-time
```

Skapa filen `pipe.md` i den mappen med följande innehåll:

```yaml
---
name: leet-time-reminder
schedule: 37 13 * * *
enabled: true
---

Det är 13:37. Skicka en desktop-notis med titeln "1337"
och texten "Det är leet-tid. Fortsätt vara elit."

Summera sedan vad jag jobbat med de senaste 30 minuterna
och lägg till det i notisen.
```

Aktivera den:
```bash
npx -y screenpipe@latest pipe enable leet-time-reminder
```

Klockan 13:37 dyker det upp en notis. 🫡

---

## Exempel 2 — Morgonsummering av Gmail 📧

Den här pipen summerar dina mejl varje morgon. Den kräver en Google API-nyckel.

### Steg 1 — Skaffa Google API-åtkomst

1. Gå till [console.cloud.google.com](https://console.cloud.google.com)
2. Skapa ett nytt projekt (eller välj ett befintligt)
3. Aktivera **Gmail API**
4. Gå till **Credentials → Create Credentials → OAuth 2.0 Client ID**
5. Välj "Desktop app"
6. Ladda ner `credentials.json`

### Steg 2 — Skapa pipe-mappen

```bash
mkdir -p ~/.screenpipe/pipes/morgon-mejl
```

### Steg 3 — Lägg API-nyckeln i .env

Skapa filen `.env` i pipe-mappen:

```env
GMAIL_CLIENT_ID=ditt-client-id-här
GMAIL_CLIENT_SECRET=din-client-secret-här
GMAIL_REFRESH_TOKEN=din-refresh-token-här
```

> **Viktigt:** `.env`-filen delas aldrig med Screenpipe-servern och lämnar aldrig din dator.
> Lägg **aldrig** in denna fil i ett publikt git-repo.

### Steg 4 — Skapa pipe.md

```yaml
---
name: morgon-mejl
schedule: 0 8 * * 1-5
enabled: true
---

Hämta mina olästa mejl från Gmail via API.
Använd credentials från .env-filen.

Lista de tre viktigaste mejlen med:
- Avsändare
- Ämne
- Två meningars sammandrag

Ignorera automatiska bekräftelsemejl och nyhetsbrev.

Skriv resultatet till ./output/mejl-idag.md
```

---

## Exempel 3 — Google Kalender-påminnelse 📅

Samma princip som Gmail — den här pipen hämtar dagens möten och påminner dig.

> **OBS:** Google Workspace-konton (företag/skola) kräver att administratören aktiverar API-åtkomst.
> Har du ett privat Google-konto funkar det direkt med samma steg som Gmail ovan.

### Skapa pipe-mappen

```bash
mkdir -p ~/.screenpipe/pipes/kalender-pamiannelse
```

### .env

```env
GOOGLE_CLIENT_ID=ditt-client-id-här
GOOGLE_CLIENT_SECRET=din-client-secret-här
GOOGLE_REFRESH_TOKEN=din-refresh-token-här
GOOGLE_CALENDAR_ID=primary
```

### pipe.md

```yaml
---
name: kalender-pamiannelse
schedule: 0 8 * * 1-5
enabled: true
---

Hämta dagens händelser från Google Calendar via API.
Använd credentials från .env-filen och kalender-ID från GOOGLE_CALENDAR_ID.

Om det finns möten idag:
- Visa en lista med tid, namn och plats
- Skicka en notis för det närmaste mötet

Om det inte finns möten: skicka inga notiser, skriv bara till ./output/

Skriv resultatet till ./output/agenda-idag.md
```

---

## Exempel 4 — Outlook Kalender (privat konto) 📆

Microsoft erbjuder ett gratis API för privata Outlook/Hotmail-konton via Microsoft Graph.

### Skaffa API-åtkomst

1. Gå till [portal.azure.com](https://portal.azure.com) och logga in med ditt privata Microsoft-konto
2. Gå till **App registrations → New registration**
3. Välj "Personal Microsoft accounts only"
4. Under **API permissions** — lägg till `Calendars.Read`
5. Skapa en **Client secret** och kopiera värdet

### .env

```env
MS_CLIENT_ID=ditt-app-id-här
MS_CLIENT_SECRET=din-client-secret-här
MS_REFRESH_TOKEN=din-refresh-token-här
```

### pipe.md

```yaml
---
name: outlook-pamiannelse
schedule: 0 8 * * 1-5
enabled: true
---

Hämta dagens händelser från Microsoft Outlook Calendar
via Microsoft Graph API (https://graph.microsoft.com/v1.0/me/calendar/events).
Använd credentials från .env-filen.

Lista händelserna med tid och namn.
Skicka en notis för det närmaste mötet om det finns ett.

Skriv resultatet till ./output/outlook-idag.md
```

---

## Tips och bra att veta

**Pipes körs en i taget.**
Screenpipe har en inbyggd kö — om en pipe körs när en annan ska starta, väntar den andra.

**Ändrar du pipe.md startar Screenpipe om den automatiskt.**
Du behöver inte starta om Screenpipe — den övervakar filerna.

**Debugga med pipe logs.**
Går något fel? Kolla loggarna:
```bash
npx -y screenpipe@latest pipe logs PIPE-NAMN
```

**Output-mappen skapas automatiskt.**
Du behöver inte skapa `output/`-mappen för hand.

---

## Nästa steg

Nu har du verktygen. Det enda begränsningen är vad du kan formulera i ord.

Testa att modifiera ett av exemplen ovan och gör det till ditt eget.
Lycka till! 🚀
