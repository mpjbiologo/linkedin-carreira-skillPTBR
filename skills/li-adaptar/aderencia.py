#!/usr/bin/env python3
"""
aderencia.py - compara um currículo com uma ou várias vagas e mostra quais
requisitos aparecem no currículo, quais faltam e qual vaga tem mais aderência.

Como funciona:
  1. Separa a vaga em blocos: requisitos (obrigatórios), diferenciais
     (desejáveis) e atividades, pelos títulos que as vagas brasileiras usam
     ("Requisitos e qualificações", "Diferenciais", "Responsabilidades"...).
  2. Quebra cada bloco em itens e tira os termos-chave de cada item
     (ferramentas, siglas, áreas, formações), ignorando palavras genéricas.
  3. Procura cada termo no currículo sem diferenciar acento, maiúscula ou
     plural. Um item conta como coberto quando a maioria dos termos aparece.
  4. Aderência = 70% requisitos + 20% diferenciais + 10% atividades.
  5. Separa os requisitos "de conferência" (anos de experiência, idioma,
     CNH, modalidade, cidade) para você checar à mão.

O que NÃO é:  a ordenação da Gupy ou de qualquer plataforma. Elas usam modelos
que entendem contexto e sinônimos. Isto é uma lista de checagem honesta: mostra
o que a vaga pede e o que o seu texto não diz. Para cada termo faltando, a
pergunta é "eu tenho isso?". Se tem, escreva. Se não tem, NÃO invente:
informação falsa no currículo é motivo de desclassificação e de demissão.

Uso
  python3 aderencia.py curriculo.pdf vaga.txt
  python3 aderencia.py curriculo.docx vaga1.txt vaga2.txt vaga3.txt   # ranking
  python3 aderencia.py curriculo.pdf vagas/*.txt --json
"""

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
import zipfile


def ler_texto(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        import html
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
        xml = re.sub(r"</w:p>", "\n", xml)
        return html.unescape(re.sub(r"<[^>]+>", "", xml))
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
        except ImportError:
            try:
                return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                                      text=True, check=True).stdout
            except (FileNotFoundError, subprocess.CalledProcessError):
                sys.exit("Não consegui ler o PDF. Instale `pypdf` ou exporte como .docx/.txt.")
    return open(path, encoding="utf-8", errors="ignore").read()


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def raiz(w):
    """Normalização simples: minúscula, sem acento, sem plural comum, e prefixo
    de 6 letras para palavras longas (aproxima "automatizar" de "automatizei")."""
    w = sem_acento(w.lower()).strip(".,/-")
    for suf, rep in (("coes", "cao"), ("soes", "sao"), ("ais", "al"), ("eis", "el"), ("ores", "or"),
                     ("ns", "m"), ("es", "e"), ("s", "")):
        if len(w) > 4 and w.endswith(suf):
            w = w[: -len(suf)] + rep
            break
    if len(w) >= 7 and w.isalpha():
        return w[:6]
    return w


STOP = set("""
a o as os um uma uns umas e ou de do da dos das em no na nos nas por pelo pela pelos pelas para pra
com sem sob sobre entre ate que se ao aos à às como mais menos muito bem ser estar ter haver seu sua
seus suas nosso nossa voce voces sera sao esta isso este esta ja tambem alem outro outra outros outras
qualquer cada todo toda todos todas onde quando qual quais area areas experiencia experiencias
conhecimento conhecimentos vivencia vivencias dominio solido solida bom boa boas bons forte fortes
avancado avancada intermediario intermediaria basico basica desejavel diferencial diferenciais
obrigatorio obrigatoria requisito requisitos necessario necessaria capacidade habilidade habilidades
facilidade perfil profissional profissionais atuacao atuar trabalho trabalhar equipe equipes time
grande grandes pessoa pessoas candidato candidata buscamos procuramos voce vai ira ira fazer atividade
atividades responsabilidade responsabilidades rotina rotinas demais empresa empresas cliente clientes
nivel completo completa cursando superior formacao graduacao ensino tecnico tecnica principal
principais similar similares relacionado relacionada correlata correlatas afins semelhante diversos
ano anos mes meses minimo afins afim comprovada comprovado previa previo gostar gosta interesse sera plus
""".split())
GENERICOS = {"comunicacao", "organizacao", "proatividade", "proativo", "lideranca", "dinamismo",
             "relacionamento", "interpessoal", "analitico", "analitica", "raciocinio", "logico", "foco",
             "resultado", "resultados", "autonomia", "colaboracao", "flexibilidade", "criatividade",
             "resiliencia", "comprometimento", "senso", "dono", "urgencia", "ingles", "espanhol"}

SEC = [
    ("diferenciais", r"(?i)^\s*(?:diferenciais?|desej[aá]ve(?:l|is)|ser[aá] um (?:diferencial|plus)|plus|b[oô]nus|n[aã]o obrigat[oó]rio)"),
    ("requisitos", r"(?i)^\s*(?:requisitos|pr[eé]-?requisitos|qualifica[cç][oõ]es|o que (?:esperamos|buscamos|precisamos)|voc[eê] precisa ter|obrigat[oó]rio|perfil desejado|para essa vaga|exig[eê]ncias)"),
    ("atividades", r"(?i)^\s*(?:responsabilidades|atribui[cç][oõ]es|atividades|o que voc[eê] (?:vai|ir[aá]) fazer|principais desafios|desafios|descri[cç][aã]o)"),
    ("ignorar", r"(?i)^\s*(?:benef[ií]cios|o que oferecemos|sobre (?:a|n[oó]s)|quem somos|etapas|informa[cç][oõ]es adicionais|local de trabalho|remunera[cç][aã]o|jornada)"),
]

CONFERIR = [
    ("anos de experiência", re.compile(r"(?i)\b(\d+)\s*\+?\s*anos? de (?:experi[eê]ncia|atua[cç][aã]o|viv[eê]ncia)")),
    ("idioma", re.compile(r"(?i)\b(?:ingl[eê]s|espanhol|franc[eê]s|alem[aã]o|mandarim)\b[^.\n;]{0,30}")),
    ("CNH", re.compile(r"(?i)\bCNH\b[^.\n;]{0,15}|\bcarteira de motorista\b")),
    ("modalidade/local", re.compile(r"(?i)\b(?:100% )?(?:presencial|h[ií]brido|remoto|home ?office)\b[^.\n;]{0,40}")),
    ("disponibilidade", re.compile(r"(?i)\bdisponibilidade (?:para|de) [^.\n;]{3,40}")),
    ("registro em conselho", re.compile(r"(?i)\b(?:CRN|CRM|CREA|CRF|COREN|CRP|CREFITO|CRC|OAB|CREF|CRO)\b[^.\n;]{0,20}|registro ativo no conselho[^.\n;]{0,20}")),
]

TOKEN = re.compile(r"[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9+#./-]*")


def blocos(vaga):
    atual, out = "requisitos" if not any(re.search(rx, vaga, re.M) for _, rx in SEC[:3]) else "intro", {}
    for linha in vaga.replace("\r", "").split("\n"):
        l = linha.strip()
        if not l:
            continue
        mudou = False
        for nome, rx in SEC:
            if re.match(rx, l) and len(l) < 70:
                atual, mudou = nome, True
                break
        if mudou:
            continue
        out.setdefault(atual, []).append(l)
    return out


def itens(linhas):
    res = []
    for l in linhas:
        l = re.sub(r"^\s*(?:[-•▪●◦*–]|\d+[.)])\s*", "", l)
        for parte in re.split(r"[;]|\.\s+(?=[A-ZÀ-Ý])", l):
            parte = parte.strip(" .")
            if len(parte.split()) >= 1:
                res.append(parte)
    return res


def termos(item):
    toks = TOKEN.findall(item)
    out = []
    for t in toks:
        r = raiz(t)
        cheio = sem_acento(t.lower()).strip(".,/-")
        if len(r) < 2 or r.isdigit() or r in STOP or cheio in STOP:
            continue
        if r in GENERICOS or cheio in GENERICOS or any(g.startswith(r) for g in GENERICOS | STOP if len(r) == 6):
            continue
        out.append((t, r))
    # remove duplicados mantendo ordem
    vistos, final = set(), []
    for t, r in out:
        if r not in vistos:
            vistos.add(r)
            final.append((t, r))
    return final


def analisar(cv, vaga):
    cv_raizes = {raiz(t) for t in TOKEN.findall(cv)}
    cv_flat = " " + " ".join(raiz(t) for t in TOKEN.findall(cv)) + " "
    b = blocos(vaga)
    resultado, pesos = {}, {"requisitos": 0.7, "diferenciais": 0.2, "atividades": 0.1}
    for sec in ("requisitos", "diferenciais", "atividades"):
        lista = []
        for it in itens(b.get(sec, [])):
            tt = termos(it)
            if not tt:
                continue
            achou = [t for t, r in tt if r in cv_raizes or (" " + r + " ") in cv_flat]
            falta = [t for t, r in tt if t not in achou]
            cob = len(achou) / len(tt)
            alternativas = bool(re.search(r"(?i)\bou\b|/", it))
            coberto = (len(achou) >= 1) if alternativas else (cob >= 0.5)
            lista.append({"item": it, "coberto": coberto, "cobertura": round(cob, 2),
                          "tem": achou, "falta": falta})
        resultado[sec] = lista
    nota, peso_usado = 0.0, 0.0
    for sec, w in pesos.items():
        if resultado[sec]:
            nota += w * sum(i["coberto"] for i in resultado[sec]) / len(resultado[sec])
            peso_usado += w
    aderencia = round(100 * nota / peso_usado) if peso_usado else 0
    conferir = []
    for nome, rx in CONFERIR:
        for m in rx.finditer(vaga):
            conferir.append({"tipo": nome, "trecho": m.group(0).strip()})
    faltando = []
    for sec in ("requisitos", "diferenciais"):
        for i in resultado[sec]:
            for f in i["falta"]:
                if f not in faltando:
                    faltando.append(f)
    return {"aderencia": aderencia, "blocos": resultado, "conferir": conferir[:8],
            "termos_faltando": faltando[:20]}


def titulo(path, vaga):
    primeira = next((l.strip() for l in vaga.split("\n") if l.strip()), os.path.basename(path))
    return primeira[:70]


def render_uma(a, nome):
    print(f"\nADERÊNCIA  ·  {nome}\n" + "=" * 70)
    for sec, rot in (("requisitos", "REQUISITOS"), ("diferenciais", "DIFERENCIAIS"), ("atividades", "ATIVIDADES")):
        lst = a["blocos"][sec]
        if not lst:
            continue
        ok = sum(i["coberto"] for i in lst)
        print(f"\n  {rot}  {ok}/{len(lst)} cobertos")
        for i in lst:
            marca = "✔" if i["coberto"] else "✖"
            print(f"   {marca} {i['item'][:80]}")
            if not i["coberto"] and i["falta"]:
                print(f"       não aparece no currículo: {', '.join(i['falta'][:6])}")
    if a["conferir"]:
        print("\n  CONFIRA À MÃO")
        for c in a["conferir"]:
            print(f"   - {c['tipo']}: \"{c['trecho']}\"")
    print("-" * 70)
    print(f"  ADERÊNCIA ESTIMADA  {a['aderencia']}%")
    print("  Para cada termo faltando: você tem isso? Se sim, escreva com um exemplo.")
    print("  Se não, não invente. Lista de checagem, não a ordenação de nenhuma plataforma.\n")


def main():
    ap = argparse.ArgumentParser(description="Aderência entre currículo e vaga(s).")
    ap.add_argument("curriculo")
    ap.add_argument("vagas", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    cv = ler_texto(args.curriculo)
    res = []
    for v in args.vagas:
        txt = ler_texto(v)
        a = analisar(cv, txt)
        a["vaga"] = titulo(v, txt)
        a["arquivo"] = v
        res.append(a)
    res.sort(key=lambda r: -r["aderencia"])
    if args.json:
        print(json.dumps(res if len(res) > 1 else res[0], indent=2, ensure_ascii=False))
        return
    if len(res) == 1:
        render_uma(res[0], res[0]["vaga"])
        return
    print("\nRANKING DE VAGAS POR ADERÊNCIA\n" + "=" * 70)
    for i, r in enumerate(res, 1):
        req = r["blocos"]["requisitos"]
        ok = sum(x["coberto"] for x in req)
        print(f" {'->' if i == 1 else '  '} {r['aderencia']:>3}%  {r['vaga']}")
        print(f"         requisitos {ok}/{len(req)}  ·  faltando: {', '.join(r['termos_faltando'][:5]) or '-'}")
    print("\nRode com uma vaga só para ver item por item. Aderência é estimativa, não garantia.\n")


if __name__ == "__main__":
    main()
