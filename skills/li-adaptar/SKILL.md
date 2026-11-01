---
name: li-adaptar
description: >-
  Compara o currículo com uma vaga específica, mostra a aderência e o que a
  vaga pede que o currículo não diz, e adapta resumo, experiências,
  competências e carta de apresentação para aquela vaga sem inventar nada. Use
  quando colarem uma vaga e pedirem "adapta meu currículo", "tenho chance?",
  "o que falta para essa vaga", "faz uma carta para essa vaga".
---

# li-adaptar

```bash
python3 aderencia.py curriculo.pdf vaga.txt                 # item por item
python3 aderencia.py curriculo.pdf vaga1.txt vaga2.txt      # ranking de vagas
```

O script separa a vaga em requisitos, diferenciais e atividades, tira os
termos-chave de cada item e procura no currículo (sem diferenciar acento,
plural ou maiúscula). Mostra o que está coberto, o que falta e o que você
precisa conferir à mão (anos de experiência, idioma, CNH, modalidade, cidade,
registro em conselho).

**Não é a ordenação da Gupy nem de plataforma nenhuma.** Elas usam modelos que
entendem contexto. Isto é uma lista de checagem: mostra o que a vaga pede e o
seu texto não diz.

## O ciclo

1. **Pegue a vaga inteira** (colada ou o texto da página). Salve em `vaga.txt`.
2. **Rode o script** e mostre o resultado.
3. **Para cada termo faltando, pergunte:** "Você tem isso?" Em lote, numa
   mensagem só. Três respostas possíveis:
   - **Tenho e não escrevi:** entra no currículo, com um exemplo concreto.
   - **Tenho parecido:** escreva o que tem, com o nome real ("Looker Studio",
     não "Power BI" se a pessoa não usou Power BI). Pode citar a semelhança na
     carta.
   - **Não tenho:** não entra. Se for requisito obrigatório, diga com clareza
     que é um ponto fraco e se ainda vale se candidatar.
4. **Adapte, sem reescrever a vida da pessoa:**
   - Título do currículo com o nome do cargo da vaga (se for o mesmo cargo).
   - Resumo com as 2 ou 3 competências que a vaga mais repete.
   - Reordene os marcadores: o que a vaga pede primeiro vai primeiro.
   - Use as palavras da vaga quando forem verdade ("gestão de stakeholders" em
     vez de "falar com outras áreas", se é isso que a pessoa fazia).
5. **Rode o script de novo** e mostre a aderência antes e depois.
6. **Carta de apresentação**, se pedirem: até 4 parágrafos curtos. Por que essa
   empresa (algo específico dela), o resultado mais parecido com o que a vaga
   pede, como a pessoa resolve o requisito mais difícil, e fechamento. Passe
   por `/li-humano`.

## Quando vale se candidatar

- **Aderência 70%+ e nenhum requisito eliminatório faltando:** candidate-se.
- **50 a 70%:** vale se o que falta é diferencial, ou se a pessoa compensa com
  algo forte. Diga isso.
- **Abaixo de 50%:** provavelmente não. Melhor gastar a energia em vagas mais
  próximas (`/li-vagas`). Diga isso com gentileza e com clareza.

Requisito "eliminatório" de verdade: registro em conselho, CNH quando dirigir é
a função, formação exigida por lei, idioma quando o trabalho é nele. "5 anos de
experiência" muitas vezes é flexível; "inglês fluente" para atendimento
internacional não é.

## Nunca

- Nunca acrescente ferramenta, cargo, certificação ou resultado que a pessoa
  não confirmou. Informação falsa em currículo é motivo de desclassificação e
  de demissão.
- Nunca esconda palavra-chave em texto branco ou letra minúscula.
- Nunca copie a descrição da vaga como se fosse experiência.

## Saída

```
ADERÊNCIA  ·  Analista de Dados Sênior (Varejo)   68% -> 90%

ANTES      requisitos 5/6 · diferenciais 1/3
CONFIRMADO POR VOCÊ   varejo (5 anos), automação em Python
NÃO TEM               dbt (diferencial, não impede)
CONFERIR              4 anos de experiência (você tem 5) · inglês intermediário (você: avançado) · híbrido em BH (ok)

MUDANÇAS
- Resumo: "Analista de dados com 5 anos em varejo..." (+ previsão de demanda)
- Experiência 1: marcador de automação subiu para o topo
- Competências: + "modelagem preditiva" (você confirmou)

VEREDITO  candidate-se. O único item faltando é diferencial.
```
