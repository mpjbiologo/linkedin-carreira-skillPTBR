---
name: li-curriculo
description: >-
  Analisa um currículo (PDF, Word ou texto) nos critérios do mercado
  brasileiro, dá nota de 0 a 100, aponta o que corrigir primeiro e reescreve
  as partes fracas sem inventar nada. Use quando pedirem "analisa meu
  currículo", "dá nota pro meu CV", "por que não me chamam", "melhora meu
  currículo", "currículo para a Gupy", ou anexarem um currículo.
---

# li-curriculo

Um script mora nesta pasta e roda:

```bash
python3 curriculo.py meu_curriculo.pdf
python3 curriculo.py meu_curriculo.docx --json
```

Ele lê PDF (com `pypdf` ou `pdftotext`), Word (.docx) e texto, e devolve nota
de 0 a 100 em nove itens, com o que corrigir primeiro. Os critérios e pesos
estão em `criterios.json`.

## Antes de começar

1. Leia `~/.claude/carreira/perfil.md` se existir: cargo-alvo, área, cidade,
   modalidade, senioridade. Se não existir, pergunte numa mensagem só:
   **qual cargo você quer, em que cidade/modalidade, e em que nível** (júnior,
   pleno, sênior, gestão). Grave as respostas no arquivo a partir de
   `templates/perfil-carreira.md`. Currículo bom é currículo para um alvo.
2. Se a pessoa colou uma vaga, a análise é contra a vaga: depois desta skill,
   rode `/li-adaptar`.

## O ciclo

**1. Rode o script** e mostre a tabela de notas.

**2. Leia o currículo inteiro você mesmo.** O script não vê coerência,
progressão de carreira, buracos, nem se o resumo combina com o cargo-alvo.
Acrescente até três observações que só uma leitura humana pega.

**3. Corrija na ordem dos pontos perdidos**, um bloco por vez:

- **Dados pessoais primeiro**, se houver. CPF, RG, data de nascimento, estado
  civil, filhos, religião, endereço completo e foto não são pedidos na triagem,
  expõem a pessoa (LGPD) e abrem espaço para discriminação. Cidade/UF basta.
- **Resumo profissional:** 3 a 4 linhas. Cargo-alvo, anos de experiência, área
  ou setor, duas competências-chave e um resultado. Nada de "busco uma
  oportunidade de crescimento".
- **Experiências:** cada linha no formato **verbo de ação + o que fez +
  ferramenta/método + resultado com número**. "Responsável por atender
  clientes" vira "Atendi {{N}} clientes por mês e reduzi o tempo de resposta
  de {{X}} para {{Y}}".
- **Competências:** as palavras que aparecem nas vagas-alvo (ferramentas,
  métodos, certificações). Uma lista limpa, não 40 itens.
- **Formato:** uma coluna, fonte comum, sem tabelas, ícones nem gráfico de
  "nível de habilidade". PDF gerado a partir do Word ou Docs, não escaneado.

**4. Nunca invente.** Se a reescrita precisa de um número que a pessoa não
deu, use `{{seu número}}` e pergunte. Currículo com informação falsa é motivo
de desclassificação e de demissão por justa causa. Melhorar como a pessoa
conta o que fez: sim. Acrescentar o que ela não fez: nunca.

**5. Rode `/li-humano`** no resumo e nas linhas reescritas.

**6. Rode o script de novo** e mostre a nota antes e depois.

## Regras do mercado brasileiro

- **1 página** até uns 5 anos de experiência; **2 páginas** depois disso.
- **Ordem cronológica inversa**, com mês/ano de início e fim.
- **Sem "pretensão salarial"** no currículo, a não ser que a vaga peça.
- **Sem foto**, a não ser que a vaga peça (algumas áreas, como atendimento ou
  modelo, pedem).
- **Inglês e outros idiomas com nível honesto** (básico, intermediário,
  avançado, fluente). Nível inflado é descoberto na entrevista.
- **Na Gupy e plataformas parecidas:** preencha os campos do formulário
  (experiência, formação, habilidades), não só anexe o PDF. A própria Gupy diz
  que sua ordenação analisa experiência, habilidades e formação em contexto,
  não só palavras soltas. Esconder palavra-chave em letra branca não funciona
  e pode prejudicar.
- **Lacunas:** um período sem trabalho não precisa ser escondido. Uma linha
  honesta ("2023: cuidado familiar" ou "2024: transição de carreira, curso X")
  é melhor que datas maquiadas.

## Saída

```
NOTA DO CURRÍCULO  17/100  ->  84/100 depois das correções

CORRIGIDO
1. Dados pessoais: removidos CPF, estado civil, data de nascimento, endereço
2. Resumo: reescrito para "Analista Administrativo"
3. Experiências: 5 linhas reescritas com verbo de ação, 3 pedem número ({{...}})
4. Clichês: "proativo, dinâmico, comunicativo" trocados por fatos

PRECISO DE VOCÊ
- Quantos clientes você atendia por mês na Empresa ABC?
- Em que ano você entrou e saiu da Empresa ABC?

PRÓXIMO PASSO: /li-vagas para achar vagas, ou /li-adaptar com uma vaga específica.
```

Entregue o currículo reescrito como arquivo Word (.docx) de uma coluna se a
pessoa pedir o arquivo; caso contrário, em texto para colar.
