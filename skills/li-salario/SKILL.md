---
name: li-salario
description: >-
  Pesquisa a faixa salarial de mercado para um cargo, nível e cidade no Brasil,
  com fontes, compara CLT e PJ e prepara a pessoa para negociar. Use quando
  perguntarem "quanto ganha um X", "qual pretensão salarial eu coloco", "essa
  proposta é boa?", "CLT ou PJ, quanto preciso cobrar", "como negociar
  salário".
---

# li-salario

Salário muda por cidade, porte da empresa, setor e mês. Por isso esta skill
**sempre pesquisa** e cita a fonte, nunca chuta de memória.

## Entrada

Cargo (e sinônimos), nível, cidade/estado, modalidade, regime (CLT/PJ), setor.
Se for para avaliar uma proposta: valor, regime e benefícios oferecidos.

## Fontes, em ordem de confiança

1. **Dados oficiais do Novo Caged (Ministério do Trabalho):** salário de
   admissão informado pelas empresas. O Portal Salário (salario.com.br)
   organiza esses dados por cargo (CBO) e cidade. É a base mais ampla para
   CLT, mas mostra salário de **admissão**, que tende a ser menor que o de
   quem já está no cargo.
2. **Guias salariais de consultorias de recrutamento** (Robert Half, Michael
   Page, Hays e similares): bons para média e alta gerência e tecnologia,
   em grandes centros.
3. **Faixas publicadas nas próprias vagas** (cada vez mais comuns): colete 5 a
   10 vagas parecidas.
4. **Sites de autodeclaração** (Glassdoor, Love Mondays): úteis por empresa,
   mas amostra pequena e sem verificação. Use como complemento.
5. **Pisos de sindicato ou de conselho** da categoria, quando existirem.

Use a busca na web, cite cada fonte com link e data, e mostre a dispersão,
não um número só.

## CLT x PJ

Para comparar, mostre a conta:

- **CLT:** salário + 13º + férias com 1/3 + FGTS (8%) + benefícios (VR/VA,
  plano de saúde, PLR). Em geral o custo anual fica bem acima de 12 salários.
- **PJ:** valor bruto menos impostos (depende do regime: MEI, Simples
  Nacional, anexo e faturamento), contador, e o que deixa de existir (férias
  remuneradas, 13º, FGTS, plano de saúde).
- Regra de bolso comum no mercado: PJ precisa pagar bem mais que o CLT
  equivalente para empatar. Faça a conta com os números da pessoa em vez de
  usar um multiplicador fixo, e diga que não é consultoria contábil.

## Negociação

- **Âncora com pesquisa:** "Pesquisei vagas parecidas em BH e a faixa está
  entre X e Y. Pela minha experiência em Z, busco algo próximo de Y."
- **Negocie o pacote**, não só o salário: modalidade, benefícios, data de
  revisão, bônus, cargo.
- **Peça por escrito** a proposta final antes de pedir demissão do emprego atual.
- **Contraproposta do emprego atual:** ajude a pessoa a pensar no motivo pelo
  qual queria sair, não só no valor.

## Saída

```
SALÁRIO  ·  Analista de Dados Pleno · Belo Horizonte · CLT

FAIXA ENCONTRADA
  Novo Caged (admissão, via Portal Salário, out/2026)   mediana R$ X  ·  Q1-Q3 R$ A-B
  Guia salarial {consultoria} 2026                       R$ C-D
  7 vagas com faixa publicada (out/2026)                 R$ E-F

LEITURA
  Faixa realista para pleno em BH: R$ ... a R$ ...
  Para pedir: R$ ... (topo da faixa, justificado por ...)

SE FOR PJ
  Equivalente aproximado: R$ ... /mês (conta abaixo)

Fontes: [links com data]
```

Diga sempre que é uma estimativa a partir de fontes públicas e que pode variar
por empresa.
