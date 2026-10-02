# 🍲 Skollunch Härnösand för Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/ayatollah/skollunch-harnosand?style=for-the-badge&color=blue)](https://github.com/ayatollah/ha-skollunch-harnosand/releases)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/ayabolli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

En Home Assistant-integration som automatiskt hämtar skollunchen för kommunala skolor i Härnösands kommun direkt från [skollunch.supergott.com](https://skollunch.supergott.com).

Integrationen ger dig dagens lunch, nästa skoldags meny (hoppar automatiskt helger till måndag), hela innevarande veckomatsedel samt integrerade kalenderentiteter för både grundskola och gymnasium.

---

## 🚀 Installation via HACS

Klicka på knappen nedan för att öppna repot direkt i din Home Assistant-instans och installera via HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ayatollah&repository=ha-skollunch-harnosand&category=integration)

### Manuell installation via HACS:
1. Öppna **HACS** i Home Assistant.
2. Klicka på menyn med tre prickar uppe till höger och välj **Custom repositories**.
3. Lägg till webbadressen till detta repo: `https://github.com/ayatollah/ha-skollunch-harnosand`
4. Välj kategori **Integration** och klicka på **Add**.
5. Sök upp **Skollunch Härnösand**, klicka på **Download** och starta om Home Assistant.
6. Gå till **Inställningar** -> **Enheter & tjänster** -> **Lägg till integration**, sök efter **Skollunch Härnösand** och bekräfta.

---

## 📊 Entiteter

Integrationen sätter automatiskt upp både sensorer och kalendrar:

### 1. Sensorer

| Entitet | Typ | Beskrivning |
|---|---|---|
| `sensor.skollunch_grundskola` | Sensor | Dagens rätt för förskola samt F–6/låg- och mellanstadie. |
| `sensor.skollunch_gymnasium` | Sensor | Dagens rätt för 7–9/högstadie och gymnasiet. |

#### Attribut på sensorerna:
Varje sensor innehåller rik data för dashboards och automationer:
* `alt_dish`: Dagens vegetariska alternativ.
* `tomorrow_dish`: Nästa skoldags rätt (måndagens meny om det är helg).
* `tomorrow_alt_dish`: Nästa skoldags vegetariska alternativ.
* `tomorrow_date`: Datum för nästa skoldag (`YYYY-MM-DD`).
* `week_number`: Aktuellt veckonummer.
* `week_menu`: Komplett lista med hela veckans rätter (`dayName`, `dateStr`, `dish`, `altDish`).
* `school_type`: `grundskola` eller `gymnasium`.
* `updated_at`: Tidsstämpel för när matsedeln senast synkroniserades.

---

### 2. Kalendrar

| Entitet | Typ | Beskrivning |
|---|---|---|
| `calendar.skollunch_grundskola_kalender` | Kalender | Visar veckans måltider direkt i Home Assistants kalendervy. |
| `calendar.skollunch_gymnasium_kalender` | Kalender | Visar gymnasie- och högstadielunchen i kalendervyn. |

---

## 📅 iCalendar-prenumeration (.ics)

Vill du prenumerera på matsedeln direkt i din mobiltelefon (Apple Kalender, Google Kalender eller Outlook) utanför Home Assistant finns färdiga `.ics`-flöden:

* **Grundskola & Förskola:** `https://skollunch.supergott.com/api/lunch/calendar.ics?school=grundskola`
* **Högstadie & Gymnasium:** `https://skollunch.supergott.com/api/lunch/calendar.ics?school=gymnasium`

---

## 💡 Exempel på användning i Home Assistant

### Dashboard-kort med dagens, morgondagens och veckans mat

Kopiera och klistra in i ett vanligt **Markdown-kort** på din dashboard:

```yaml
type: markdown
title: 🍽️ Skollunch Grundskola
content: >
  ### Idag
  **{{ states('sensor.skollunch_grundskola') }}**
  *🌱 Veg: {{ state_attr('sensor.skollunch_grundskola', 'alt_dish') }}*

  ### Imorgon
  **{{ state_attr('sensor.skollunch_grundskola', 'tomorrow_dish') }}**
  *🌱 Veg: {{ state_attr('sensor.skollunch_grundskola', 'tomorrow_alt_dish') }}*

  ---
  ### Matsedel vecka {{ state_attr('sensor.skollunch_grundskola', 'week_number') }}
  {% for day in state_attr('sensor.skollunch_grundskola', 'week_menu') %}
  **{{ day.dayName }} ({{ day.dateStr }}):** {{ day.dish }}
  {% endfor %}
```

### Kvällsnotis inför morgondagen

```yaml
alias: "Notis: Morgondagens skollunch"
trigger:
  - platform: time
    at: "20:00:00"
condition:
  - condition: time
    weekday:
      - sun
      - mon
      - tue
      - wed
      - thu
action:
  - action: notify.notify
    data:
      title: "Skollunch imorgon"
      message: >
        Imorgon serveras {{ state_attr('sensor.skollunch_grundskola', 'tomorrow_dish') }} i skolan.
```
---

## ℹ️ Om källan
Informationen parsas automatiskt från Härnösands kommuns officiella PDF-matsedlar via webbtjänsten på skollunch.supergott.com. Tjänsten drivs ideellt och har ingen officiell koppling till kommunens förvaltning.

## ☕ Stöd projektet
Underlättar integrationen vardagslogistiken hemma? Bjud gärna på en kaffe!