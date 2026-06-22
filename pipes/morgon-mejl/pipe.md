---
name: morgon-mejl
schedule: 0 8 * * 1-5
enabled: false
---

Hämta mina olästa mejl från Gmail via API.
Använd credentials från .env-filen.

Lista de tre viktigaste mejlen med:
- Avsändare
- Ämne
- Två meningars sammandrag

Ignorera automatiska bekräftelsemejl och nyhetsbrev.

Skriv resultatet till ./output/mejl-idag.md
