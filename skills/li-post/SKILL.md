---
name: li-post
description: >-
  Escreve um post de LinkedIn em português a partir de uma ideia: três
  aberturas de 21 fórmulas com nota, o texto completo e a revisão de clichês
  de IA. Use quando pedirem "escreve um post", "post para o LinkedIn",
  "anuncia meu novo emprego", "quero postar sobre X", "conta minha
  experiência", ou quiserem visibilidade para buscar vaga.
---

# li-post

```bash
python3 nota_gancho.py aberturas.txt              # ranqueia as aberturas
python3 nota_gancho.py --gancho "uma abertura"     # avalia uma
```

## Antes de escrever

1. Leia `~/.claude/carreira/voz.md` se existir (como a pessoa escreve, o que
   nunca diria). Se não existir, peça dois ou três posts ou textos dela.
2. Leia `ganchos.json`: 21 fórmulas com exemplo de carreira.
3. Se a ideia estiver rala, pergunte numa mensagem só: **o que aconteceu, com
   quem, e qual o número ou a consequência**. Post bom tem um fato específico.

## O formato

```
LINHAS 1-2   a abertura. É o que aparece antes do "...ver mais". Um fato.
CORPO        a história ou o argumento, em parágrafos de 1 a 3 linhas.
             Um dado, um exemplo, uma virada.
FECHAMENTO   a lição em uma frase e UMA pergunta específica.
HASHTAGS     até 3, no fim. Ou nenhuma.
```

Tamanho: 600 a 1.300 caracteres funciona para a maioria. Até 3.000 é possível.

## O ciclo

1. **Três aberturas** de fórmulas diferentes de `ganchos.json`.
2. **Dê nota** com `nota_gancho.py`. Abaixo de 50, ainda não há abertura.
3. **Escreva o post** na abertura vencedora, na voz da pessoa.
4. **Rode `/li-humano`.** Post de LinkedIn é onde o texto de IA mais aparece.
5. **Entregue** o post pronto para colar e uma linha dizendo a fórmula e a nota.

## Regras

- **Comece pelo fato, não pela emoção.** "Comecei hoje como Analista de Dados
  na Empresa X" ganha de "Estou muito feliz em compartilhar...".
- **Nada de "broetry"** (uma frase por linha o post inteiro). Parágrafos curtos.
- **Link fora do texto,** no primeiro comentário, se precisar.
- **Uma pergunta específica no fim,** não "Concordam?".
- **Nunca invente** número, cliente, empresa, fala ou resultado. Faltou dado:
  `{{seu dado}}`.
- **Não exponha ninguém:** nada de nome de ex-chefe, empresa difamada ou
  informação confidencial do empregador.
- **Buscando vaga?** Post de "estou disponível" funciona melhor com: cargo-alvo,
  2-3 resultados concretos, cidade/modalidade e um pedido simples ("se souber
  de uma vaga, me indica?"). Sem tom de desespero.
- **Uso de IA:** se a área da pessoa exige declarar uso de IA (alguns
  conselhos profissionais exigem), inclua a linha de declaração.

Nada é publicado. A pessoa cola.
