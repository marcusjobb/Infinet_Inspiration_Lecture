---
name: kalender-pamiannelse
schedule: 0 8 * * 1-5
enabled: false
---

Hämta dagens händelser från Google Calendar via API.
Använd credentials från .env-filen och kalender-ID från GOOGLE_CALENDAR_ID.

Om det finns möten idag:
- Visa en lista med tid, namn och plats
- Skicka en notis för det närmaste mötet

Om det inte finns möten: skicka inga notiser, skriv bara till ./output/

Skriv resultatet till ./output/agenda-idag.md
