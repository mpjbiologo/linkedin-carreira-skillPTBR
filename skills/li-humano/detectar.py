#!/usr/bin/env python3
"""
detectar.py - painel de cinco checagens que dá nota para o quanto um texto em
português parece escrito por máquina.

O que é:  cinco heurísticas locais inspiradas nos sinais que detectores
públicos de IA medem: variação no tamanho das frases, concretude, vocabulário
de clichê, marcas tipográficas e voz. Tudo é calculado no seu computador a
partir do texto. Nada é enviado para lugar nenhum.

O que NÃO é:  GPTZero, Originality, Copyleaks, Winston ou Turnitin. Não chama
esses serviços e não promete o veredito deles. Corrigir o que este painel mede
costuma mexer nos números deles, porque medem as mesmas coisas; essa é a única
afirmação honesta.

Observação: humanizar melhora a leitura e deixa o texto com a sua voz; não é
para esconder que houve IA. Alguns conselhos profissionais exigem declarar o
uso de IA em comunicações; confira as regras da sua área.

Cada checagem devolve uma nota HUMANA de 0 a 100. Maior é melhor.

Uso
  python3 detectar.py rascunho.txt
  python3 detectar.py rascunho.txt --json
  python3 detectar.py antes.txt depois.txt      # compara dois textos
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "cliches.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ']+")
# Marcas de fala informal do português brasileiro: fazem o papel que as
# contrações ("don't", "it's") fazem no inglês. Os limiares de pronome e de
# informalidade são mais baixos que no original porque o português omite o
# sujeito ("atendo" em vez de "eu atendo").
INFORMAL = re.compile(
    r"\b(?:pra|pro|pras|pros|t[aá]|t[oô]|n[eé]|c[eê]|vc|vcs|tava|tavam|tamo|bora|"
    r"a gente|t[aá] bom|daí|aí|tipo|beleza|demais|olha|cara|gente|num|dum|duma|"
    r"t[ií]nhamos|t[eê]m|pq|tbm|tb)\b",
    re.IGNORECASE)
PRONOUNS = re.compile(
    r"\b(eu|me|mim|meu|minha|meus|minhas|comigo|n[oó]s|nosso|nossa|a gente|"
    r"voc[eê]|voc[eê]s|vc|seu|sua|seus|suas|te|ti|contigo)\b", re.IGNORECASE)
NUMBERS = re.compile(
    r"\b\d[\d.,]*%?|R\$\s?\d|\b(?:dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|doze|"
    r"quinze|vinte|trinta|quarenta|cinquenta|cem|duzentos|quinhentos|mil|metade|d[uú]zia)\b",
    re.IGNORECASE)
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b", re.MULTILINE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def term_pattern(find):
    body = re.escape(find).replace(r"\ ", r"\s+")
    left = r"\b" if re.match(r"\w", find) else ""
    right = r"\b" if re.search(r"\w$", find) else ""
    return re.compile(left + body + right, re.IGNORECASE)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """Gente varia muito o tamanho das frases. Modelo escreve igual."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "curto demais para julgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variação {cv:.2f} em {len(lens)} frases (ideal 0,55+)"


def check_specificity(text):
    """Números, nomes, coisas concretas. Clichê é abstrato."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais para julgar"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} marcadores concretos, {density:.1f} a cada 100 palavras (ideal 4+)"


def check_slop(text, lex):
    """Densidade de clichês do léxico."""
    w = words(text)
    if not w:
        return 50.0, "vazio"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        n = len(term_pattern(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} clichês, {density:.1f} a cada 100 palavras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que o teclado do celular não produz."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisível(is), {em} travessão(ões), {curly} aspa(s) curva(s), "
              f"{ellip} reticência(s) de 1 caractere, {nbsp} espaço(s) rígido(s)")
    return score, detail


def check_voice(text, lex):
    """Informalidade, pessoa e as estruturas que modelos adoram."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais para julgar"
    per100 = 100 / len(w)
    informal = len(INFORMAL.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells, names = 0, []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(informal, human=1.5, machine=0.0) * 0.35
             + scale(person, human=5.0, machine=0.5) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("marcadores-iguais")
    detail = (f"{informal:.1f} marcas de fala informal, {person:.1f} pronomes pessoais "
              f"a cada 100 palavras, {tells} estrutura(s) de IA")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIAÇÃO", "CONCRETUDE", "CLICHÊS", "DIGITAIS", "VOZ"]


def run(text, lex):
    results = {
        "VARIAÇÃO": check_burstiness(text),
        "CONCRETUDE": check_specificity(text),
        "CLICHÊS": check_slop(text, lex),
        "DIGITAIS": check_fingerprint(text),
        "VOZ": check_voice(text, lex),
    }
    scores = [results[c][0] for c in CHECKS]
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASSOU" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "SINALIZADO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PAINEL DE DETECÇÃO DE IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<11} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<11} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA HUMANA':<11} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASSOU":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Sinal mais fraco: {weakest}. Corrija esse primeiro.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota para o quanto um texto parece de máquina.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou -")
    ap.add_argument("compare", nargs="?", help="segundo arquivo, para comparar antes/depois")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexico", "--lexicon", dest="lexico", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexico, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "fonte": name,
            "checagens": {k: {"nota": round(v[0], 1), "detalhe": v[1]} for k, v in results.items()},
            "nota_humana": round(overall, 1),
            "veredito": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["nota_humana"] - a["nota_humana"]
        print(f"  {a['nota_humana']:.1f} {a['veredito']}  ->  "
              f"{b['nota_humana']:.1f} {b['veredito']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["veredito"] == "PASSOU" else 1)


if __name__ == "__main__":
    main()
