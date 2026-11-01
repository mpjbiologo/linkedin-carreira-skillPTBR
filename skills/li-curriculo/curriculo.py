#!/usr/bin/env python3
"""
curriculo.py - dá nota de 0 a 100 a um currículo nos critérios que mais pesam
no mercado brasileiro e aponta o que corrigir primeiro.

Lê .txt, .md, .docx e .pdf (PDF precisa de `pypdf` ou do programa `pdftotext`;
se nenhum estiver instalado, exporte o currículo como .txt ou .docx).

O que mede (cada item tem peso; o total é 100):
  LEITURA        o texto sai do arquivo? PDF feito de imagem, colunas e
                 caracteres estranhos atrapalham os sistemas de triagem
  TAMANHO        1 a 2 páginas (aprox. 300 a 900 palavras)
  CONTATO        e-mail, telefone, cidade/UF e LinkedIn
  DADOS PESSOAIS nada de CPF, RG, data de nascimento, estado civil, filhos,
                 religião, foto (LGPD e risco de discriminação)
  SEÇÕES         resumo, experiência, formação, competências, idiomas
  RESULTADOS     linhas de experiência com número, %, R$, prazo ou volume
  VERBOS         experiências que começam com ação ("Implantei", "Reduzi")
                 e não com "Responsável por"
  CLICHÊS        "proativo", "dinâmico", "busco crescimento profissional"
  DATAS          cada experiência com período (mês/ano ou ano)

O que NÃO é:  a ordenação da Gupy, da Kenoby ou de qualquer sistema real.
Essas plataformas usam modelos próprios que leem contexto, não só palavras.
Isto mede boas práticas que ajudam tanto o sistema quanto a pessoa que lê.
Nota alta não garante entrevista; nota baixa costuma explicar silêncio.

Uso
  python3 curriculo.py meu_curriculo.pdf
  python3 curriculo.py meu_curriculo.docx --json
"""

import argparse
import json
import os
import re
import subprocess
import sys
import zipfile


# ---------------------------------------------------------------- leitura
def ler_texto(path):
    """Devolve (texto, paginas_ou_None, metodo)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
        xml = re.sub(r"</w:p>", "\n", xml)
        xml = re.sub(r"<w:tab/>", "\t", xml)
        txt = re.sub(r"<[^>]+>", "", xml)
        import html
        return html.unescape(txt), None, "docx"
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            r = PdfReader(path)
            return "\n".join((p.extract_text() or "") for p in r.pages), len(r.pages), "pypdf"
        except ImportError:
            pass
        try:
            out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True)
            pages = out.stdout.count("\f") or None
            return out.stdout, pages, "pdftotext"
        except (FileNotFoundError, subprocess.CalledProcessError):
            sys.exit("Não consegui ler o PDF. Instale `pypdf` (pip install pypdf) ou exporte como .docx/.txt.")
    return open(path, encoding="utf-8", errors="ignore").read(), None, "texto"


# ---------------------------------------------------------------- padrões
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
FONE = re.compile(r"(?:\+?55\s?)?\(?\b\d{2}\)?\s?9?\d{4}[-.\s]?\d{4}\b")
LINKEDIN = re.compile(r"linkedin\.com/in/[\w-]+", re.I)
UF = r"(?:AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)"
CIDADE = re.compile(r"\b[A-ZÀ-Ý][\wÀ-ÿ' ]{2,30}\s?[-/,]\s?" + UF + r"\b")

PESSOAIS = [
    ("CPF", re.compile(r"\bCPF\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"), "FALHA"),
    ("RG", re.compile(r"\bRG\b[:\s]*[\d.\-xX]{5,}"), "FALHA"),
    ("data de nascimento / idade", re.compile(r"(?i)\b(?:data de nascimento|nascid[oa] em|nascimento:|\d{2}\s?anos de idade|idade:)"), "ATENÇÃO"),
    ("estado civil", re.compile(r"(?i)\b(?:estado civil|solteir[oa]|casad[oa]|divorciad[oa]|vi[uú]v[oa])\b"), "ATENÇÃO"),
    ("filhos", re.compile(r"(?i)\b(?:filhos?:|\d\s+filhos?|sem filhos)\b"), "ATENÇÃO"),
    ("religião", re.compile(r"(?i)\breligi[aã]o\b"), "ATENÇÃO"),
    ("endereço completo", re.compile(r"(?i)\b(?:rua|av\.|avenida|travessa|alameda)\s+[^\n,]{2,40},?\s*n?º?\s*\d+|\bCEP\b[:\s]*\d{5}-?\d{3}"), "ATENÇÃO"),
    ("nome dos pais", re.compile(r"(?i)\b(?:filiação|nome d[ao] (?:m[aã]e|pai))\b"), "ATENÇÃO"),
    ("foto", re.compile(r"(?i)\bfoto\b"), "ATENÇÃO"),
    ("PIS / título de eleitor / CTPS", re.compile(r"(?i)\b(?:PIS|PASEP|t[ií]tulo de eleitor|CTPS)\b"), "FALHA"),
]

SECOES = {
    "resumo": r"(?im)^\s*(?:resumo(?: profissional)?|perfil(?: profissional)?|sobre(?: mim)?|objetivo|apresenta[cç][aã]o)\b",
    "experiência": r"(?im)^\s*(?:experi[eê]ncias?(?: profissiona(?:l|is))?|hist[oó]rico profissional|trajet[oó]ria)\b",
    "formação": r"(?im)^\s*(?:forma[cç][aã]o(?: acad[eê]mica)?|escolaridade|educa[cç][aã]o)\b",
    "competências": r"(?im)^\s*(?:compet[eê]ncias|habilidades|conhecimentos|hard skills|ferramentas|qualifica[cç][oõ]es)\b",
    "idiomas": r"(?im)^\s*idiomas?\b|\b(?:ingl[eê]s|espanhol)\s*[:\-–]",
}

ACAO = {
    "implantei", "implementei", "reduzi", "aumentei", "criei", "desenvolvi", "liderei", "coordenei",
    "gerenciei", "conduzi", "estruturei", "otimizei", "automatizei", "negociei", "entreguei", "lancei",
    "reestruturei", "economizei", "expandi", "treinei", "capacitei", "atendi", "elaborei", "planejei",
    "organizei", "analisei", "construí", "construi", "conquistei", "dobrei", "triplei", "ampliei",
    "padronizei", "migrei", "integrei", "supervisionei", "atuei", "realizei", "executei", "fiz",
    "implantação", "implementação", "redução", "aumento", "criação", "desenvolvimento", "liderança",
    "coordenação", "gestão", "condução", "estruturação", "otimização", "automação", "negociação",
    "lançamento", "treinamento", "capacitação", "elaboração", "planejamento", "análise", "atendimento",
    "implantar", "implementar", "reduzir", "aumentar", "criar", "desenvolver", "liderar", "coordenar",
    "gerenciar", "conduzir", "elaborar", "planejar", "analisar", "atender", "realizar", "executar",
    "prescrevi", "acompanhei", "orientei", "avaliei", "ministrei", "publiquei", "vendi", "prospectei",
}
PASSIVO = re.compile(r"(?i)^\s*(?:respons[aá]vel (?:por|pel[ao]s?)|auxiliar (?:em|n[ao])|aux[ií]lio|atividades:|fun[cç][oõ]es:)")

CLICHES = [
    "proativo", "proativa", "proatividade", "dinâmico", "dinâmica", "comunicativo", "comunicativa",
    "trabalho em equipe", "facilidade de aprendizado", "fácil aprendizado", "multitarefa", "perfeccionista",
    "pontual", "responsável e dedicado", "dedicado", "dedicada", "esforçado", "esforçada",
    "busco oportunidade", "busco uma oportunidade", "crescimento profissional", "agregar valor",
    "pensar fora da caixa", "fora da caixa", "sinergia", "resiliente", "apaixonado por", "apaixonada por",
    "focado em resultados", "focada em resultados", "orientado a resultados", "orientada a resultados",
    "boa comunicação", "relacionamento interpessoal", "vontade de aprender", "colocar em prática",
]

RESULTADO = re.compile(r"\d+\s?%|R\$\s?\d|\b\d[\d.,]*\s?(?:mil|milh[oõ]es|k\b|clientes|pacientes|pessoas|projetos|unidades|lojas|vendas|horas|dias|meses|anos|[aá]reas|equipes|funcion[aá]rios|colaboradores|cidades|pa[ií]ses|produtos|contratos|alunos|turmas|leads|relat[oó]rios|bases|sistemas|processos)\b|\b(?:dobr|tripl|reduz|aument|cresc|economi)\w*\b[^.\n]{0,40}\d", re.I)
DATA_RANGE = re.compile(r"(?i)\b(?:(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\w*\.?\s*(?:de\s*)?|\d{2}/)?(?:19|20)\d{2}\s*(?:-|–|—|a|até)\s*(?:(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\w*\.?\s*(?:de\s*)?|\d{2}/)?(?:(?:19|20)\d{2}|atual|hoje|o momento|presente)")
BULLET = re.compile(r"(?m)^\s*(?:[-•▪●◦*–]|\d+[.)])\s+(.+)$")
WEIRD = re.compile(r"[-\U0001F300-\U0001FAFF☀-➿]")


def norm(w):
    return w.lower().strip(".,;:!?()\"'")


def analisar(texto, paginas=None, metodo="texto"):
    t = texto.replace("\r", "")
    palavras = re.findall(r"[A-Za-zÀ-ÿ0-9]+", t)
    n = len(palavras)
    checks = []

    def add(nome, peso, nota, status, detalhe):
        checks.append({"item": nome, "peso": peso, "pontos": round(peso * nota, 1),
                       "status": status, "detalhe": detalhe})

    # LEITURA
    weird = len(WEIRD.findall(t))
    pipes = t.count("|") + t.count("\t") * 0.3
    if n < 80:
        msg = (f"só {n} palavras extraídas: provavelmente PDF de imagem ou layout que o sistema não lê. Gere um PDF a partir do Word/Docs, sem imagem"
               if metodo in ("pypdf", "pdftotext") else f"só {n} palavras: texto curto demais para um currículo")
        add("LEITURA", 10, 0 if metodo in ("pypdf", "pdftotext") else 0.5, "FALHA" if metodo in ("pypdf", "pdftotext") else "ATENÇÃO", msg)
    elif weird > 5 or pipes > 25:
        add("LEITURA", 10, 0.5, "ATENÇÃO", f"{weird} ícone(s)/caractere(s) especial(is) e sinais de colunas/tabelas. Layout de uma coluna, sem ícones, lê melhor")
    else:
        add("LEITURA", 10, 1, "OK", "texto extraído limpo")

    # TAMANHO
    est_pag = paginas or max(1, round(n / 450))
    if 300 <= n <= 950 and est_pag <= 2:
        add("TAMANHO", 8, 1, "OK", f"{n} palavras, ~{est_pag} página(s)")
    elif n < 300:
        add("TAMANHO", 8, 0.5, "ATENÇÃO", f"{n} palavras: curto. Detalhe resultados das experiências recentes")
    else:
        add("TAMANHO", 8, 0.4, "ATENÇÃO", f"{n} palavras, ~{est_pag} página(s): passe de 2 páginas só com muita senioridade. Resuma experiências com mais de 10 anos")

    # CONTATO
    tem = {"e-mail": bool(EMAIL.search(t)), "telefone": bool(FONE.search(t)),
           "cidade/UF": bool(CIDADE.search(t)), "LinkedIn": bool(LINKEDIN.search(t))}
    falta = [k for k, v in tem.items() if not v]
    add("CONTATO", 8, sum(tem.values()) / 4, "OK" if not falta else ("ATENÇÃO" if len(falta) < 3 else "FALHA"),
        "completo" if not falta else "faltando: " + ", ".join(falta))

    # DADOS PESSOAIS
    achados = [(nome, st) for nome, rx, st in PESSOAIS if rx.search(t)]
    if not achados:
        add("DADOS PESSOAIS", 12, 1, "OK", "nenhum dado pessoal desnecessário")
    else:
        grave = any(st == "FALHA" for _, st in achados)
        add("DADOS PESSOAIS", 12, 0 if grave else max(0, 1 - 0.25 * len(achados)),
            "FALHA" if grave else "ATENÇÃO",
            "remova: " + ", ".join(nome for nome, _ in achados) + ". Não são pedidos na triagem, expõem você (LGPD) e abrem espaço para discriminação")

    # SEÇÕES
    secs = {k: bool(re.search(rx, t)) for k, rx in SECOES.items()}
    falta = [k for k, v in secs.items() if not v]
    add("SEÇÕES", 10, sum(secs.values()) / len(secs), "OK" if not falta else "ATENÇÃO",
        "todas presentes" if not falta else "não encontrei: " + ", ".join(falta) + " (use títulos claros)")

    # RESULTADOS e VERBOS (nos marcadores; se não houver marcadores, nas linhas)
    linhas = [b.strip() for b in BULLET.findall(t)]
    if len(linhas) < 3:
        linhas = [l.strip() for l in t.split("\n") if 4 <= len(l.split()) <= 45]
    linhas = [l for l in linhas if not EMAIL.search(l) and not any(rx.search(l) for _, rx, _ in PESSOAIS)
              and not re.match(r"(?i)\s*(?:busco|objetivo)", l)]
    comres = [l for l in linhas if RESULTADO.search(l)]
    taxa = len(comres) / max(len(linhas), 1)
    add("RESULTADOS", 20, min(1, taxa / 0.4), "OK" if taxa >= 0.4 else ("ATENÇÃO" if taxa >= 0.15 else "FALHA"),
        f"{len(comres)} de {len(linhas)} linhas de experiência têm número, %, R$ ou volume (ideal: 40%+)")

    acao = [l for l in linhas if norm(l.split()[0]) in ACAO] if linhas else []
    passivo = [l for l in linhas if PASSIVO.match(l)]
    taxa_a = len(acao) / max(len(linhas), 1)
    st = "OK" if taxa_a >= 0.5 and not passivo else ("ATENÇÃO" if taxa_a >= 0.2 else "FALHA")
    add("VERBOS DE AÇÃO", 12, min(1, taxa_a / 0.5) * (0.8 if passivo else 1), st,
        f"{len(acao)} de {len(linhas)} linhas começam com ação" + (f"; {len(passivo)} com \"Responsável por\"/\"Auxiliar\"" if passivo else ""))

    # CLICHÊS
    low = t.lower()
    cl = sorted({c for c in CLICHES if re.search(r"\b" + re.escape(c) + r"\b", low)})
    add("CLICHÊS", 8, max(0, 1 - 0.2 * len(cl)), "OK" if not cl else ("ATENÇÃO" if len(cl) < 4 else "FALHA"),
        "nenhum" if not cl else f"{len(cl)}: " + ", ".join(cl[:6]) + ". Troque por um fato que prove a qualidade")

    # DATAS
    ranges = DATA_RANGE.findall(t)
    if secs["experiência"] and len(ranges) == 0:
        add("DATAS", 12, 0, "FALHA", "nenhum período (mês/ano - mês/ano) encontrado nas experiências")
    elif len(ranges) < 2:
        add("DATAS", 12, 0.6, "ATENÇÃO", f"{len(ranges)} período(s) encontrado(s). Coloque início e fim em cada experiência")
    else:
        add("DATAS", 12, 1, "OK", f"{len(ranges)} períodos encontrados")

    total = round(sum(c["pontos"] for c in checks))
    fix = sorted([c for c in checks if c["status"] != "OK"], key=lambda c: c["pontos"] - c["peso"])
    return {"nota": total, "palavras": n, "paginas_estimadas": est_pag, "itens": checks,
            "corrigir_primeiro": [c["item"] for c in fix[:3]],
            "exemplos_sem_resultado": [l for l in linhas if l not in comres][:3]}


def bar(v, w=20):
    f = round(v * w)
    return "#" * f + "." * (w - f)


def render(a, nome):
    head = f"NOTA DO CURRÍCULO  ·  {nome}  ·  {a['palavras']} palavras"
    print("\n" + head + "\n" + "=" * max(62, len(head)))
    for c in a["itens"]:
        print(f"  {c['status']:<7} {c['item']:<15} {bar(c['pontos'] / c['peso'])} {c['pontos']:>4}/{c['peso']:<3}")
        print(f"  {'':<7} {'':<15} {c['detalhe']}")
    print("-" * 62)
    print(f"  NOTA  {a['nota']}/100")
    if a["corrigir_primeiro"]:
        print(f"  Corrija primeiro: {', '.join(a['corrigir_primeiro'])}")
    if a["exemplos_sem_resultado"]:
        print("\n  Linhas que pedem um número (só se for verdade):")
        for l in a["exemplos_sem_resultado"]:
            print(f"   - {l[:100]}")
    print("\n  Heurística local. Não é a ordenação de nenhuma plataforma real.\n")


def main():
    ap = argparse.ArgumentParser(description="Nota de currículo para o mercado brasileiro.")
    ap.add_argument("arquivo", help=".pdf, .docx, .txt ou .md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    texto, pags, metodo = ler_texto(args.arquivo)
    a = analisar(texto, pags, metodo)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a, os.path.basename(args.arquivo))


if __name__ == "__main__":
    main()
