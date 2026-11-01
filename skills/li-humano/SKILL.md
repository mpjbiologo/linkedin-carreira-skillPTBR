---
name: li-humano
description: >-
  Tira a cara de IA de qualquer texto em português (post, sobre, currículo,
  carta, mensagem): travessões, clichês corporativos e de texto gerado,
  caracteres invisíveis, e dá nota num painel de cinco checagens. Use sempre
  que um texto precisar soar humano, quando pedirem "humaniza", "isso parece
  IA?", "tira o tom de coach", ou antes de entregar qualquer texto das outras
  skills.
---

# li-humano

```bash
python3 humanizar.py rascunho.txt --relatorio      # limpa e mostra o que mudou
python3 detectar.py rascunho.txt                    # nota, cinco checagens
python3 detectar.py antes.txt depois.txt            # prova a diferença
```

Os dois leem `cliches.json`: cerca de 200 palavras e expressões com troca por
português simples, caracteres invisíveis, trocas tipográficas e 20 estruturas
típicas. O bloco `linkedin` traz os clichês da plataforma: "Estou muito feliz em
compartilhar", "agregar valor", "fora da caixa", "mindset", "sair da zona de
conforto", "Concordam?". Edite o arquivo à vontade.

## O que é corrigido automaticamente

1. **Caracteres invisíveis** que teclado não produz.
2. **Tipografia:** travessão vira vírgula, aspas curvas viram retas.
3. **Clichês:** trocados por palavra simples ou apagados.

Depois de rodar, **releia a concordância**: em português a troca de uma
palavra pode desencontrar artigo e adjetivo.

## O que é só apontado (reescreva à mão)

"Não é só X, é Y", "Não é sobre X, é sobre Y", trios de três palavras,
pergunta retórica solta ("O resultado?"), abertura "Estou feliz em anunciar",
uma frase por parágrafo o post inteiro, muro de hashtags, frase motivacional
genérica, gerundismo ("vou estar enviando").

## As cinco checagens

| checagem | mede | cara de máquina |
| --- | --- | --- |
| VARIAÇÃO | variação no tamanho das frases | tudo do mesmo tamanho |
| CONCRETUDE | números e nomes a cada 100 palavras | abstrato, sem dado |
| CLICHÊS | ocorrências do léxico | vocabulário pronto |
| DIGITAIS | invisíveis, travessões, aspas curvas | tipografia perfeita demais |
| VOZ | informalidade, pessoa, estruturas | impessoal, revelações encenadas |

PASSOU exige nota 70+ e nenhuma checagem abaixo de 55. Em currículo, a nota de
VOZ tende a ser baixa (currículo é impessoal de propósito): olhe CLICHÊS e
CONCRETUDE.

## Honestidade

São heurísticas locais, não GPTZero nem Turnitin, e ninguém pode prometer
texto "indetectável". O objetivo é o texto ficar bom de ler e com a voz da
pessoa, não esconder que houve IA.
