---
name: li-plano
description: >-
  Monta o plano semanal de carreira no LinkedIn: candidaturas, contatos,
  posts e comentários, com metas realistas e acompanhamento. Use quando
  pedirem "organiza minha busca de emprego", "plano para me recolocar",
  "o que faço essa semana no LinkedIn", "rotina de busca de vaga", ou
  quiserem crescer na área.
---

# li-plano

A sala de controle. Junta as outras skills numa semana que dá para cumprir.

## Entrada

Leia `~/.claude/carreira/perfil.md`, `vagas.md` e `historico.md` se existirem.
Senão, pergunte: objetivo (recolocação, promoção, transição, visibilidade),
tempo disponível por semana, e se a pessoa está empregada (busca discreta) ou não.

## O plano padrão de recolocação (umas 5 horas por semana)

| bloco | quanto | skill |
| --- | --- | --- |
| **Candidaturas boas** | 5 a 10 por semana, só aderência 60%+ | `/li-vagas`, `/li-adaptar` |
| **Contatos** | 5 mensagens por semana para pessoas da área (ex-colegas, gestores, recrutadores do setor) | escreva com a pessoa |
| **Comentários** | 15 minutos, 3 a 5 dias por semana | `/li-comentario` |
| **Post** | 1 por semana ou a cada 15 dias | `/li-post` |
| **Revisão** | 30 minutos na sexta: o que respondeu, o que ajustar | esta skill |

Qualidade ganha de volume: 8 candidaturas adaptadas rendem mais que 80
genéricas. Diga isso se a pessoa estiver disparando currículo em massa.

**Busca discreta (empregado):** sem selo público de "Open to work", preferências
visíveis só para recrutadores, nada de post sobre busca de vaga, e cuidado com
candidaturas para a própria empresa ou concorrentes diretos.

## Mensagens para contatos

Curtas (3 a 4 frases), específicas, sem pedir vaga de cara: o que tem em
comum, uma pergunta sobre a área ou a empresa, e um pedido pequeno ("15
minutos de conversa?"). Duas tentativas, no máximo. Nunca automatize
mensagens: viola os termos do LinkedIn e pode restringir a conta.

## Acompanhamento

Mantenha `~/.claude/carreira/vagas.md` com: vaga, link, data da candidatura,
etapa, próximo passo. Na revisão de sexta, olhe a taxa de resposta:

- **Muitas candidaturas, nenhuma resposta:** problema de currículo ou de alvo
  (`/li-curriculo`, `/li-adaptar`).
- **Respostas, mas para na entrevista:** `/li-entrevista`.
- **Ninguém vê o perfil:** `/li-perfil` e mais comentários.

## Saída

```
SEMANA DE 03/11  ·  recolocação  ·  5h

SEG  30 min  /li-vagas: 10 vagas novas, escolher 4
TER  45 min  /li-adaptar nas 2 melhores + candidatura
QUA  20 min  3 mensagens para contatos + comentários
QUI  45 min  /li-adaptar nas outras 2 + candidatura
SEX  30 min  revisão + post da semana (/li-post)

METAS  4 candidaturas adaptadas · 3 contatos · 10 comentários · 1 post
```

Grave em `~/.claude/carreira/plano.md`. Nada é enviado nem publicado pela skill.
