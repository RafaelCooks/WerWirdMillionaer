import random
import requests

TELEFONJOKER_PERSONEN = [
    "Albert Einstein",
    "Mama",
    "Papa",
    "Harald Lesch"
]

SICHERHEITSTEXTE = [
    "Ich bin mir ziemlich sicher, es ist",
    "Ich glaube, es ist",
    "Hmm... vielleicht ist es",
    "Ganz klar: Es ist",
    "Ich würde sagen, es ist"
]

# --- Telefonjoker ---
def telefonjoker(personenname, richtige_antwort, falsche_antworten):
    wissen = random.randint(75, 100)  # Zufällige Sicherheit
    korrekt = random.random() < wissen / 100
    antwort = richtige_antwort if korrekt else random.choice(falsche_antworten)
    sicherheit = random.choice(SICHERHEITSTEXTE)

    return {
        "name": personenname,
        "antwort": antwort,
        "sicherheit": sicherheit,
        "wissen": wissen
    }

# --- 50:50 Joker ---
def joker_50_50(richtige_antwort, falsche_antworten):
    # Wähle zufällig eine der drei falschen Antworten
    falsch_geblieben = random.choice(falsche_antworten)
    return [richtige_antwort, falsch_geblieben]

# --- Publikumsjoker ---
def publikumsjoker(richtige_antwort, falsche_antworten):
    # Gesamtstimmen (z. B. 100 Personen im Publikum)
    gesamt = 100

    # Richtigkeitsquote zwischen 30 % und 90 %
    richtig_anteil = random.randint(30, 90)
    stimmen_richtig = int(gesamt * (richtig_anteil / 100))

    # Verteile restliche Stimmen zufällig auf falsche Antworten
    rest_stimmen = gesamt - stimmen_richtig
    verteilung = [0, 0, 0]
    for _ in range(rest_stimmen):
        verteilung[random.randint(0, 2)] += 1

    # Antworten mischen (wie im Spiel)
    antworten = [richtige_antwort] + falsche_antworten
    random.shuffle(antworten)

    # Ergebnis-Zuordnung
    ergebnis = {}
    for i, antwort in enumerate(antworten):
        if antwort == richtige_antwort:
            ergebnis[antwort] = stimmen_richtig
        else:
            idx = [a for a in antworten if a != richtige_antwort].index(antwort)
            ergebnis[antwort] = verteilung[idx]

    return ergebnis  # Dict: Antwort → Stimmenanzahl
