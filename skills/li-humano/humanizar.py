#!/usr/bin/env python3
"""
humanizar.py - tira a "cara de IA" de um rascunho em português.

Três passadas, nesta ordem:

  1. INVISÍVEIS   apaga ou normaliza caracteres que um teclado humano nunca
                  produz: espaços de largura zero, word joiners, hífens
                  ocultos, BOM, caracteres de tag Unicode, espaços rígidos.
                  Sobrevivem ao copiar e colar e são o sinal mais mecânico de
                  texto gerado.
  2. TIPOGRAFIA   travessão -> vírgula, meia-risca -> hífen, aspas curvas ->
                  retas, reticências de um caractere -> três pontos, marcador -> hífen.
  3. CLICHÊS      troca o léxico de cliches.json por palavras simples,
                  mantendo maiúsculas e sem mexer em links.

Estruturas ("não é só X, é Y", trios, muro de hashtags) são APONTADAS, nunca
reescritas automaticamente: mudar o formato de uma frase exige julgamento, e
isso é trabalho do modelo, não de uma regex.

Depois de rodar, releia a concordância: trocar "robusta" por "forte" é seguro,
mas uma substituição pode deixar artigo e adjetivo desencontrados.

Uso
  python3 humanizar.py rascunho.txt
  python3 humanizar.py rascunho.txt --relatorio
  python3 humanizar.py rascunho.txt -o limpo.txt --relatorio
  python3 humanizar.py rascunho.txt --json
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "cliches.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def term_pattern(find):
    """Regex para um termo do léxico. Só exige limite de palavra nas pontas
    que são letras: "além disso," termina em vírgula e não tem \\b depois."""
    body = re.escape(find).replace(r"\ ", r"\s+")
    left = r"\b" if re.match(r"\w", find) else ""
    right = r"\b" if re.search(r"\w$", find) else ""
    return re.compile(left + body + right, re.IGNORECASE)


def _cp(spec):
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"nome": entry["cp"] + " " + entry["name"], "qtd": n,
                         "acao": "apagar" if entry["action"] == "delete" else "virar espaço"})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"nome": "outros caracteres invisíveis de formatação", "qtd": len(stray),
                     "acao": "apagar"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"nome": f"{ch} {entry['name']}", "qtd": n, "para": entry["to"].strip() or "(espaço)"})
        if ch == "—":
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)       # 5–10 -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)             # usada como travessão
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex):
    """Troca clichês. Os mais longos primeiro, para frases ganharem de palavras."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"], key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern = term_pattern(entry["find"])
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"termo": entry["find"], "troca": entry["replace"] or "(apagado)",
                     "qtd": len(found), "familia": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpeza depois de apagar: sobra pontuação órfã ("sistema. ." ou linha
    # começando com vírgula), e isso fica pior que o clichê.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:!?]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)
    text = re.sub(r"[ \t]+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = text.replace("...", "\x00ELL\x00")
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r",\s*(também|então|ainda|basicamente|no fim)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"nome": s["name"], "qtd": len(found), "correcao": s["fix"]})
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "nome": f"Frases todas do mesmo tamanho (variação {cv:.2f})",
                "qtd": len(lens),
                "correcao": "Quebre uma frase no meio. Deixe outra ficar longa. Máquina escreve tudo igual.",
            })
    return flags


def restore_capitals(original, text):
    """Apagar uma abertura deixa a palavra seguinte em minúscula. Só corrige
    para quem já escreve com maiúscula no início de frase: um estilo todo em
    minúsculas é escolha, não defeito."""
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*([A-Za-zÀ-ÿ])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))\s*([a-zà-ÿ])",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisiveis": inv,
        "tipografia": typo,
        "cliches": lexi,
        "estruturas": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = (sum(h["qtd"] for h in report["invisiveis"])
             + sum(h["qtd"] for h in report["tipografia"])
             + sum(h["qtd"] for h in report["cliches"]))

    head("RELATÓRIO DE HUMANIZAÇÃO")
    print(f"{total} marcas de máquina removidas, "
          f"{len(report['estruturas'])} estruturas apontadas para reescrever", file=out)

    if report["invisiveis"]:
        head("1. CARACTERES INVISÍVEIS")
        for h in report["invisiveis"]:
            print(f"  {h['qtd']:>3}x  {h['nome']}  -> {h['acao']}", file=out)
    if report["tipografia"]:
        head("2. TIPOGRAFIA")
        for h in report["tipografia"]:
            print(f"  {h['qtd']:>3}x  {h['nome']}  -> {h['para']}", file=out)
    if report["cliches"]:
        head("3. CLICHÊS")
        for h in report["cliches"]:
            print(f"  {h['qtd']:>3}x  {h['termo']}  -> {h['troca']}   [{h['familia']}]", file=out)
    if report["estruturas"]:
        head("4. ESTRUTURAS  (não corrigidas sozinhas - reescreva você)")
        for h in report["estruturas"]:
            print(f"  {h['qtd']:>3}x  {h['nome']}\n        {h['correcao']}", file=out)
    if not any(report.values()):
        head("LIMPO")
        print("  Nada para tirar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Tira a cara de IA de um rascunho em português.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou -")
    ap.add_argument("-o", "--saida", "--out", dest="saida", help="grava o texto limpo aqui")
    ap.add_argument("--relatorio", "--report", dest="relatorio", action="store_true",
                    help="mostra o que mudou (no stderr)")
    ap.add_argument("--json", action="store_true", help="emite {texto, relatorio} em JSON")
    ap.add_argument("--lexico", "--lexicon", dest="lexico", default=LEX, help="caminho do cliches.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexico)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"texto": clean, "relatorio": report}, indent=2, ensure_ascii=False))
        return
    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"gravado em {args.saida}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.relatorio:
        render_report(report)


if __name__ == "__main__":
    main()
