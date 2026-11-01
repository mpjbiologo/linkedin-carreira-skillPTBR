#!/usr/bin/env python3
"""
nota_gancho.py - dá nota para a abertura (as 2 primeiras linhas) de um post de LinkedIn nas cinco coisas que
ganchos fortes têm em comum, e ranqueia vários ganchos entre si.

O que é:  cinco heurísticas locais, calculadas no seu computador só a partir do
texto. Medem propriedades que ganchos que seguram atenção costumam ter: um
tamanho que dá para falar em menos de três segundos, algo concreto, algo em
jogo, o conteúdo na frente e não no fim, e um espectador a quem falar.

O que NÃO é:  um previsor de views. A versão original (em inglês) foi testada
em 74 ganchos reais: separou bem um gancho real de um propositalmente ruim
(AUC 0,83), mas quase não separou os acertos de um criador dos erros do mesmo
criador (AUC 0,56, onde 0,50 é cara ou coroa). Esta adaptação para português
ainda não foi validada em ganchos reais em PT-BR.

Então use para o que ela mede bem: pegar saudação, introdução, gancho sem nada
concreto e gancho que leva cinco segundos para ser dito. Ela não diz qual de
dois ganchos bons vai viralizar; quem decide isso é seu rosto, sua edição, seu
áudio e para quem o Instagram mostra. Confie no gráfico de retenção.

No LinkedIn o "gancho" é o que aparece antes do "...ver mais": cerca de duas
linhas, uns 140 a 210 caracteres. Esta versão aceita até 18 palavras sem
penalidade e acusa as aberturas mais batidas da plataforma.

Cada checagem vai de 0 a 100. Maior é melhor.

Uso
  python3 nota_gancho.py ganchos.txt              # um gancho por linha, ranqueados
  python3 nota_gancho.py --gancho "Recusei uma proposta 30% maior. Foi a melhor decisão do ano."
  python3 nota_gancho.py ganchos.txt --json
"""

import argparse
import json
import re
import statistics
import sys

WORD_RE = re.compile(r"[A-Za-zÀ-ÿ0-9$%'’-]+")
NUMBER_RE = re.compile(
    r"R\$\s?\d[\d.]*(?:,\d+)?"                          # dinheiro
    r"|\b\d[\d.,]*\s?"                                   # um número, com ou
    r"(?:%|kg\b|g\b|mg\b|ml\b|kcal\b|x\b|h\b|horas?\b|min\b|minutos?\b"  # sem unidade
    r"|dias?\b|semanas?\b|meses\b|m[eê]s\b|anos?\b|colheres?\b|copos?\b|xícaras?\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)(?<![.!?:] )\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Gancho falado diz os números em voz alta. "Duas colheres" é tão concreto
# quanto "2 colheres". "Um" e "primeiro" ficam de fora: são enchimento mais
# vezes do que quantidade.
SPOKEN_NUMBERS = {
    "zero", "dois", "duas", "três", "tres", "quatro", "cinco", "seis", "sete",
    "oito", "nove", "dez", "onze", "doze", "quinze", "vinte", "trinta",
    "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa",
    "cem", "cento", "duzentos", "trezentos", "quinhentos", "mil", "milhão",
    "milhões", "dúzia", "metade", "meio", "meia", "dobro", "triplo",
}
MONEY_WORDS = {
    "reais", "real", "conto", "contos", "pila", "centavos", "por cento",
    "salário", "caloria", "calorias", "kcal", "gramas", "grama", "quilos",
    "quilo", "litro", "litros", "colher", "colheres", "xícara", "copo",
}

# Palavras que colocam algo em jogo. Um gancho sem nenhuma é uma afirmação;
# com uma, é um motivo para continuar assistindo.
STAKES = {
    "pare", "para", "nunca", "errado", "errada", "erro", "erros", "errei",
    "perdi", "perde", "perder", "custa", "custou", "falha", "falhou",
    "ninguém", "ninguem", "não", "nao", "nem", "jamais", "corta", "cortar",
    "cortou", "trava", "travando", "atrapalha", "sabota", "engana", "mentira",
    "verdade", "segredo", "escondido", "pior", "piores", "odeio", "desperdiça",
    "desperdício", "golpe", "vilão", "vilã", "culpa", "culpado", "problema",
    "risco", "perigo", "cuidado", "alerta", "arrependo", "deveria", "ainda",
    "já", "só", "sem", "versus", "vs", "mas", "porém", "antes", "até",
    "em vez", "troca", "trocar", "substitui", "barato", "caro", "grátis",
    "fome", "inchaço", "cansaço", "compulsão", "ataque", "beliscar",
    "proibido", "liberado", "pode", "posso", "mito", "mitos", "realmente",
    "recusei", "recusou", "demitido", "demitida", "demiti", "demissão", "layoff", "desempregado",
    "desempregada", "rejeitado", "rejeitada", "reprovado", "reprovada", "proposta", "promoção",
    "promovido", "promovida", "salário", "aumento", "currículos", "entrevista", "entrevistas",
    "vaga", "vagas", "melhor", "contratei", "contratado", "contratada", "pedi", "saí", "larguei",
}

# Aberturas que gastam o primeiro segundo sem dizer nada.
WEAK_OPENERS = [
    "então", "entao", "bom", "olá", "ola", "oi", "oie", "gente", "galera",
    "pessoal", "fala", "e aí", "e ai", "hoje", "basicamente", "sinceramente",
    "olha só", "seguinte", "tipo", "é o seguinte", "eu queria", "eu quero",
    "eu vou", "vou te", "vou falar", "vim falar", "vem comigo", "bora",
    "você sabia", "voce sabia", "vocês sabiam", "já pensou", "neste vídeo",
    "nesse vídeo", "no vídeo de hoje", "no vídeo", "existe", "isso é",
    "uma das", "muita gente", "muitas pessoas", "bem-vindo", "bem vindo",
    "tudo bem", "boa tarde", "bom dia", "boa noite",
]

# Imperativos que merecem a primeira posição.
IMPERATIVES = {
    "pare", "para", "copia", "copie", "salva", "salve", "apaga", "tenta",
    "tente", "olha", "olhe", "veja", "lê", "leia", "use", "usa", "faz",
    "faça", "troca", "troque", "coma", "come", "beba", "bebe", "experimente",
    "nunca", "sempre", "evite", "corta", "corte", "começa", "comece",
    "repara", "anota", "anote", "presta",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:para de rolar|pare de rolar|n[aã]o passa|n[aã]o pula|espera,? n[aã]o)"),
     "Abre com \"para de rolar\". Pedir atenção mostra que você ainda não conquistou."),
    (re.compile(r"(?i)\b(?:n(?:este|esse|o) v[ií]deo(?: de hoje)?|no reel de hoje|hoje eu vou (?:te )?(?:mostrar|ensinar|falar)|vou te mostrar como|vim (?:te )?falar)\b"),
     "Introdução de vídeo. Apague e comece pelo conteúdo."),
    (re.compile(r"(?i)^\s*(?:oi|ol[aá]|oie|e a[ií]|fala,?|bom dia|boa tarde|boa noite|tudo bem|gente,|galera,|pessoal,)"),
     "Saudação. Ninguém abriu o feed para ser cumprimentado."),
    (HASHTAG_RE,
     "Hashtag no gancho. Hashtag vai no fim da legenda, se for."),
    (re.compile(r"(?i)^\s*(?:estou (?:muito )?feliz|tenho o prazer|[eé] com (?:grande|muita) (?:alegria|satisfa[cç][aã]o)|feliz em (?:anunciar|compartilhar))"),
     "Abertura \"Estou feliz em anunciar\". Comece pelo fato, não pela emoção."),
    (re.compile(r"(?i)^\s*(?:hoje (?:eu )?(?:quero|vim) (?:compartilhar|falar)|gostaria de compartilhar|vou compartilhar)"),
     "Abertura que anuncia em vez de dizer. Apague e comece pelo que você ia compartilhar."),
    (re.compile(r"(?i)\b(?:concorda\??|o que voc[eê]s acham\??|comenta a[ií])\s*$"),
     "Pergunta genérica no gancho. Guarde a pergunta para o fim, e faça uma específica."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "R$ 1.200" é uma palavra quando falado, então aqui também.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d)", "", text))


def low_words(text):
    return [w.lower().strip("'’") for w in words(text)]


def check_length(text):
    """O gancho precisa chegar antes do polegar mexer. Uns dois segundos."""
    n = len(words(text))
    chars = len(text.strip())
    if 5 <= n <= 18:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 18) * 8)
    if chars > 210:                       # passa do "...ver mais" no celular
        score -= 15
    return clamp(score), f"{n} palavras, {chars} caracteres (ideal 5-18 palavras, até ~200 caracteres antes do \"ver mais\")"


def check_specificity(text):
    """Uma coisa concreta vale mais que três abstratas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = low_words(text)
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} marcador(es) concreto(s)" + (f": {found}" if found else
                   " - nenhum número, nome ou quantidade, nada verificável"))


def check_stakes(text):
    """Tensão, custo, negação. Algo que o espectador pode perder."""
    low = low_words(text)
    joined = " ".join(low)
    hits = {x for x in low if x in STAKES}
    hits |= {s for s in STAKES if " " in s and s in joined}
    markers = sorted(hits)
    if re.search(r"R\$\s?\d", text):
        markers.append("um preço")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensão" + (f": {', '.join(markers[:4])}" if markers else
                                              " - nada está em jogo nesta frase")
    return clamp(score), detail


def check_frontload(text):
    """A palavra interessante não pode estar na posição nove."""
    w = words(text)
    if not w:
        return 0.0, "vazio"
    low = [x.lower().strip("'’") for x in w]
    opener = " ".join(low[:3])
    penalty, hit_opener = 0, None
    for weak in WEAK_OPENERS:
        if opener.startswith(weak + " ") or opener == weak or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base, where = 30.0, "nenhuma palavra de impacto na frase"
    elif payload <= 3:
        base, where = 100.0, f"impacto na palavra {payload + 1}"
    elif payload <= 6:
        base, where = 70.0, f"impacto na palavra {payload + 1}, dá para puxar para a frente"
    else:
        base, where = 40.0, f"impacto na palavra {payload + 1}, tarde demais"
    detail = where + (f"; abertura fraca \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Falando com um espectador, ou solto no ar."""
    low = text.lower()
    w = low_words(text)
    if re.search(r"\b(voc[eê]|vc|seu|sua|seus|suas|te|tu|contigo)\b", low):
        return 100.0, "fala com o espectador"
    if w and w[0] in IMPERATIVES:
        return 90.0, f"abre com imperativo (\"{w[0]}\")"
    if re.search(r"\b(eu|meu|minha|meus|minhas|me|a gente|nós|nosso|nossa)\b", low):
        return 70.0, "primeira pessoa, sem espectador"
    return 35.0, "terceira pessoa, ninguém na sala"


CHECKS = ["TAMANHO", "CONCRETUDE", "TENSÃO", "IMPACTO", "DESTINO"]


def run(text):
    results = {
        "TAMANHO": check_length(text),
        "CONCRETUDE": check_specificity(text),
        "TENSÃO": check_stakes(text),
        "IMPACTO": check_frontload(text),
        "DESTINO": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # A pior propriedade limita o gancho: basta uma ruim para o polegar seguir.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FORTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "FRACO")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nNOTA DO GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<11} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<11} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA':<11} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  ELIMINATÓRIO  {f}", file=out)
    if verdict != "FORTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Ponto mais fraco: {weakest}. Corrija esse e rode de novo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["gancho"] if len(r["gancho"]) <= 62 else r["gancho"][:59] + "..."
        print(f"{mark} {r['nota']:5.1f} {r['veredito']:<6} {hook}", file=out)
        print(f"        mais fraco: {r['mais_fraco']} ({r['checagens'][r['mais_fraco']]['nota']:.0f})", file=out)
        for f in r["eliminatorios"]:
            print(f"        eliminatório: {f}", file=out)
    print("\nUse o primeiro. Se o primeiro está abaixo de 50, nenhum destes é a abertura.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota a aberturas de post de LinkedIn em cinco propriedades.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo com um gancho por linha, ou -")
    ap.add_argument("--gancho", "--hook", dest="gancho", help="avalia um único gancho")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.gancho:
        lines = [args.gancho]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("nada para avaliar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "gancho": line,
            "checagens": {k: {"nota": round(v[0], 1), "detalhe": v[1]} for k, v in results.items()},
            "mais_fraco": min(CHECKS, key=lambda c: results[c][0]),
            "eliminatorios": flags,
            "nota": round(overall, 1),
            "veredito": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["nota"]))

    sys.exit(0 if max(p["nota"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
