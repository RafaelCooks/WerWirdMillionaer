import random
import requests  # Wird aktuell nicht genutzt, evtl. für zukünftige Erweiterungen

# ============================================
# 🧠 Telefonjoker – Gesprächspartnerliste
# ============================================

TELEFONJOKER_PERSONEN = [
    "Albert Einstein",
    "Mama",
    "Papa",
    "Harald Lesch"
]

# Mögliche Formulierungen zur Antwortsicherheit
SICHERHEITSTEXTE = [
    "Ich bin mir ziemlich sicher, es ist",
    "Ich glaube, es ist",
    "Hmm... vielleicht ist es",
    "Ganz klar: Es ist",
    "Ich würde sagen, es ist"
]

# ============================================
# 📞 Telefonjoker – Antwort generieren
# ============================================

def telefonjoker(personenname, richtige_antwort, falsche_antworten):
    """
    Simuliert eine Telefonjoker-Antwort.
    
    - Es wird zufällig entschieden, ob die Antwort korrekt ist (mit hoher Wahrscheinlichkeit).
    - Gibt Antworttext, Sicherheitssatz und Name der Person zurück.
    """
    wissen = random.randint(75, 100)  # Prozentual: wie wahrscheinlich kennt die Person die richtige Antwort?
    korrekt = random.random() < wissen / 100  # Zufällig richtig je nach 'Wissen'
    
    # Wähle die Antwort (richtig oder zufällig falsch)
    antwort = richtige_antwort if korrekt else random.choice(falsche_antworten)
    
    # Sicherheitstext auswählen
    sicherheit = random.choice(SICHERHEITSTEXTE)

    return {
        "name": personenname,
        "antwort": antwort,
        "sicherheit": sicherheit,
        "wissen": wissen
    }

# ============================================
# ➗ 50:50 Joker – zwei falsche entfernen
# ============================================

def joker_50_50(richtige_antwort, falsche_antworten):
    """
    Gibt die richtige Antwort + eine zufällig ausgewählte falsche Antwort zurück.
    Wird genutzt, um zwei von vier Antwortmöglichkeiten zu entfernen.
    """
    falsch_geblieben = random.choice(falsche_antworten)  # Eine falsche bleibt
    return [richtige_antwort, falsch_geblieben]

# ============================================
# 📊 Publikumsjoker – Stimmenverteilung simulieren
# ============================================

def publikumsjoker(richtige_antwort, falsche_antworten):
    """
    Simuliert die Verteilung von Publikumsstimmen.
    
    - Richtige Antwort erhält zwischen 30 % und 90 % der Stimmen.
    - Die restlichen Stimmen werden zufällig auf falsche Antworten verteilt.
    - Die Antworten werden gemischt, damit die Reihenfolge unvorhersehbar ist.
    """
    gesamt = 100  # Gesamtanzahl der Stimmen (z. B. 100 Personen)

    # Wieviel Prozent stimmen für die richtige Antwort?
    richtig_anteil = random.randint(30, 90)
    stimmen_richtig = int(gesamt * (richtig_anteil / 100))

    # Verteile übrige Stimmen zufällig auf 3 falsche Antworten
    rest_stimmen = gesamt - stimmen_richtig
    verteilung = [0, 0, 0]
    for _ in range(rest_stimmen):
        verteilung[random.randint(0, 2)] += 1  # Zufällige Zuteilung

    # Antworten mischen (für zufällige Anordnung im Diagramm)
    antworten = [richtige_antwort] + falsche_antworten
    random.shuffle(antworten)

    # Erstelle Ergebnis-Dictionary: Antwort → Stimmenanzahl
    ergebnis = {}
    for i, antwort in enumerate(antworten):
        if antwort == richtige_antwort:
            ergebnis[antwort] = stimmen_richtig
        else:
            # Verteile Stimmen auf die falschen Antworten anhand Index
            idx = [a for a in antworten if a != richtige_antwort].index(antwort)
            ergebnis[antwort] = verteilung[idx]

    return ergebnis  # Beispiel: {"A": 62, "B": 19, "C": 11, "D": 8}
