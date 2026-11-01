---
name: li-comentario
description: >-
  Escreve comentários em posts de LinkedIn que soam como um profissional com
  opinião, não como robô, e ajudam a pessoa a ser vista por recrutadores e
  gestores da área. Use quando colarem um post pedindo comentário, "comenta
  isso", "o que eu respondo aqui", ou quiserem um lote para a rotina diária
  de interação.
---

# li-comentario

Para quem busca vaga, comentar bem em posts de gestores e empresas da área
rende mais visibilidade que postar. Um comentário bom é visto por todo mundo
que lê aquele post, e leva até o seu perfil.

## Entrada

A pessoa cola o post (texto ou print) e diz quem escreveu. Não varra o feed
com navegador e não publique nada.

## Os tipos de comentário

| tipo | quando | formato |
| --- | --- | --- |
| **Acrescentar um dado** | você tem um número ou experiência que reforça | "Na Empresa X, vimos o mesmo: ..." |
| **O caso que faltou** | o post está certo mas incompleto | "Vale até {condição}." |
| **Discordar com respeito** | você pensa diferente | concorde no que der, depois a divergência |
| **A pergunta de verdade** | o post pulou a parte difícil | uma pergunta específica |
| **A experiência** | você já viveu aquilo | o que aconteceu, em duas frases |
| **Parabéns que diz algo** | anúncio de vaga, promoção, lançamento | parabéns + uma coisa específica |

## Regras

- **Uma a três frases.**
- **Nunca abra com** "Excelente post!", "Parabéns pelo conteúdo!", "Top!",
  "Concordo plenamente". São invisíveis.
- **Diga a coisa específica.** Se o comentário serve em qualquer post, é ruído.
- **Nunca peça vaga em comentário** ("tem vaga pra mim?"). Comente bem por
  algumas semanas; se fizer sentido, mande uma mensagem depois.
- **Em post de vaga:** se a pessoa vai se candidatar, uma linha com cargo +
  um resultado relevante funciona melhor que "Tenho interesse!".
- **Respeito sempre.** Discordar de ideia, nunca da pessoa.

## Saída

Duas opções de tipos diferentes, rotuladas, e qual você postaria e por quê.
Passe as duas por `/li-humano`.

## Modo lote

Para a rotina diária, peça 5 a 10 posts numa mensagem só e devolva um
comentário para cada. Anote em `~/.claude/carreira/historico.md` quem já
recebeu comentário na semana.
