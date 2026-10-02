# 🍲 Skollunch Härnösand för Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/ayatollah/skollunch-harnosand?style=for-the-badge&color=blue)](https://github.com/ayatollah/skollunch-harnosand/releases)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/ayabolli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

En anpassad Home Assistant-integration som automatiskt hämtar dagens skollunch och vegetariska alternativ för kommunala skolor i Härnösands kommun direkt från [skollunch.supergott.com](https://skollunch.supergott.com).

Inga krångliga inställningar eller formulär – installera integrationen så skapas sensorer för både grundskola och gymnasium direkt.

---

## 🚀 Installation via HACS

Klicka på knappen nedan för att öppna repot direkt i din Home Assistant-instans och lägga till det i HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ayatollah&repository=skollunch-harnosand&category=integration)

### Manuell installation via HACS:
1. Öppna **HACS** i Home Assistant.
2. Klicka på menyn med tre prickar uppe till höger och välj **Custom repositories**.
3. Lägg till webbadressen till detta repo: `https://github.com/ayatollah/skollunch-harnosand`
4. Välj kategori **Integration** och klicka på **Add**.
5. Sök upp **Skollunch Härnösand**, klicka på **Download** och starta om Home Assistant.
6. Gå till **Inställningar** -> **Enheter & tjänster** -> **Lägg till integration**, sök efter **Skollunch Härnösand** och bekräfta.

---

## 📊 Sensorer och Entiteter

Integrationen skapar automatiskt två sensorer:

| Sensor | Entitets-ID | Beskrivning |
|---|---|---|
| 🍎 **Skollunch Grundskola** | `sensor.skollunch_grundskola` | Dagens rätt för förskolor och F–6/låg- och mellanstadie. |
| 🍗 **Skollunch Gymnasium** | `sensor.skollunch_gymnasium` | Dagens rätt för 7–9 och Härnösands gymnasium. |

### Attribut på sensorerna:
Varje sensor har följande attribut (`attributes`):
- `alt_dish`: Dagens vegetariska alternativ (eller specialrätt om angivet).
- `school_type`: Skoltyp (`grundskola` eller `gymnasium`).
- `updated_at`: Tidsstämpel för när matsedeln senast synkroniserades från kommunens PDF.

---

## 💡 Exempel på användning

### 1. Dashboard-kort (Entities / Markdown)
Visa dagens rätt och vegetariska alternativ snyggt på kylskåpsplattan:

```yaml
type: markdown
title: 🍽️ Veckans Skollunch
content: >
  ### Idag
  **{{ states('sensor.skollunch_grundskola') }}**
  *🌱 Veg: {{ state_attr('sensor.skollunch_grundskola', 'alt_dish') }}*

  ### Imorgon
  **{{ state_attr('sensor.skollunch_grundskola', 'tomorrow_dish') }}**
  *🌱 Veg: {{ state_attr('sensor.skollunch_grundskola', 'tomorrow_alt_dish') }}*

  ---
  ### Hela vecka {{ state_attr('sensor.skollunch_grundskola', 'week_number') }}
  {% for day in state_attr('sensor.skollunch_grundskola', 'week_menu') %}
  **{{ day.dayName }} ({{ day.dateStr }}):** {{ day.dish }}
  {% endfor %}
```

### 2. Morgonnotis via högtalare / TTS
Säg vad det blir för lunch vid frukostbordet kl 07:15 på vardagar:

```yaml
alias: "TTS: Dagens skollunch"
trigger:
  - platform: time
    at: "07:15:00"
condition:
  - condition: time
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri
  - condition: not
    conditions:
      - condition: state
        entity_id: sensor.skollunch_grundskola
        state: "Ingen skollunch idag"
action:
  - action: tts.speak
    target:
      entity_id: tts.google_se
    data:
      media_player_entity_id: media_player.kokshogtalare
      message: >
        God morgon! Idag serveras det {{ states('sensor.skollunch_grundskola') }} i skolan.
```

### ℹ️ Om källan

Informationen parsas automatiskt från Härnösands kommuns officiella PDF-matsedlar via backend-tjänsten på skollunch.supergott.com. Tjänsten drivs som ett ideellt projekt och har ingen officiell koppling till kommunens förvaltning.

### ☕ Stöd projektet
Underlättar integrationen vardagslogistiken hemma? Bjud gärna på en kaffe!


