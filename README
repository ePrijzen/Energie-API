# Energie-API

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

## Inleiding

De Energie-API is het centrale punt van het ePrijzen-project. Met deze API kun je real-time energieprijzen ophalen en verbinding maken met een SQLite-database.

## Functionaliteiten

- **Real-time prijsinformatie ophalen**: Haal de meest actuele energieprijzen op via een gestandaardiseerde API.
- **Database-integratie**: Slaat gegevens op in een SQLite-database voor verdere verwerking en analyse.

## Installatie

Je kunt deze repository op drie manieren gebruiken: met de Poetry package manager, als Docker-container, of met de Pixi package manager.

### Optie 1: Poetry

1. **Kloon de repository:**
   ```bash
   git clone https://github.com/ePrijzen/energie-api.git
   cd energie-api
   ```

2. **Installeer Poetry:**
   Zorg ervoor dat je [Poetry](https://python-poetry.org/docs/#installation) geïnstalleerd hebt.

3. **Installeer de afhankelijkheden:**
   ```bash
   poetry install
   ```

4. **Voer de applicatie uit:**
   ```bash
   poetry run python main.py
   ```

### Optie 2: Docker en Poetry

1. **Installeer Docker:**
   Zorg ervoor dat Docker op je systeem is geïnstalleerd. [Download Docker](https://docs.docker.com/get-docker/)

2. **Bouw de Docker-container:**
   ```bash
   docker build -t energie-api .
   ```

3. **Start de container:**
   ```bash
   docker run -d -p 8000:8000 energie-api
   ```

4. **Open de API in je browser:**
   Ga naar `http://localhost:8000` om de API te gebruiken.

### Optie 3: Pixi

1. **Kloon de repository:**
   ```bash
   git clone https://github.com/ePrijzen/energie-api.git
   cd energie-api
   ```

2. **Installeer Pixi:**
   Volg de installatie-instructies op de [Pixi website](https://pixi.js.org/).

3. **Installeer de afhankelijkheden:**
   ```bash
   pixi install
   ```

4. **Start de applicatie:**
   ```bash
   pixi run start
   ```

## Gebruik

Voorbeelden van hoe je de API kunt gebruiken om prijsinformatie op te halen:

```bash
curl -X GET http://localhost:8000/prices
```

## Contactinformatie

Voor vragen of ondersteuning, neem contact op met:

- **Theo van der Sluijs**
  - **Website:** [itheo.tech](https://itheo.tech)
  - **E-mail:** [theo@vandersluijs.nl](mailto:theo@vandersluijs.nl)
  - **GitHub:** [tvdsluijs](https://github.com/tvdsluijs)

## Licentie

Dit project is gelicentieerd onder de MIT-licentie. Zie het [LICENSE-bestand](https://github.com/ePrijzen/energie-api/blob/main/LICENSE) voor meer details.
