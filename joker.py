import random
import requests

HF_API_KEY = "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"
HF_NLI_MODEL = "facebook/bart-large-mnli"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_NLI_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

DEFAULT_WISSEN = 30

PROMIS = [
    {"name": "Harald Lesch", "themen": {"Physik": 90, "Astronomie": 95, "Chemie": 75}},
    {"name": "Mai Thi Nguyen-Kim", "themen": {"Chemie": 95, "Biologie": 85, "Wissenschaft": 90}},
    ...
]

def frage_thema_bestimmen(frage, labels):
    payload = {"inputs": frage, "parameters": {"candidate_labels": labels}}
    response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    themen = response.json()["labels"]
    return themen[0]

def passende_promis(thema, anzahl=3):
    kandidaten = [p for p in PROMIS if thema in p["themen"]]
    if len(kandidaten) < anzahl:
        andere = [p for p in PROMIS if p not in kandidaten]
        kandidaten += random.sample(andere, anzahl - len(kandidaten))
    return random.sample(kandidaten, anzahl)

def gib_antwort(frage, richtige_antwort, falsche_antworten, wissen_prozent):
    korrekt = random.random() < wissen_prozent / 100
    return richtige_antwort if korrekt else random.choice(falsche_antworten)

def telefonjoker(frage, richtige_antwort, falsche_antworten):
    labels = ["Chemie", "Physik", "Politik", "Sport", "Biologie", "Gesundheit", "Internet",
              "Astronomie", "Wissenschaft", "Musik", "Medien", "Umwelt", "Mode", "Literatur",
              "Satire", "Gesellschaft", "Technik", "Wirtschaft"]
    thema = frage_thema_bestimmen(frage, labels)
    print(f"[Thema erkannt: {thema}]")

    kandidaten = passende_promis(thema)

    ergebnisse = []
    for person in kandidaten:
        wissen = person["themen"].get(thema, DEFAULT_WISSEN)
        antwort = gib_antwort(frage, richtige_antwort, falsche_antworten, wissen)
        ergebnisse.append({
            "name": person["name"],
            "thema": thema,
            "wissen": wissen,
            "antwort": antwort
        })

    return ergebnisse
