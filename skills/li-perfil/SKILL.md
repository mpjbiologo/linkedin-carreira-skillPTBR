---
name: li-perfil
description: >-
  Dá nota de 0 a 100 para um perfil de LinkedIn numa rubrica de 13 itens
  (título, sobre, experiências, competências, foto, recomendações, URL,
  preferências de vaga) e reescreve o que perde pontos, para o mercado
  brasileiro. Use quando pedirem "analisa meu LinkedIn", "nota pro meu
  perfil", "melhora meu título", "reescreve meu sobre", "recrutador não me
  acha", ou colarem o perfil.
---

# li-perfil

O perfil do LinkedIn tem dois leitores: a **busca** (recrutadores procurando
por cargo, competência e cidade) e a **pessoa** que abre o perfil e decide em
poucos segundos se vale chamar. Esta skill otimiza para os dois.

## Entrada

Peça para a pessoa colar o texto do perfil (ou o PDF que o LinkedIn gera em
"Mais > Salvar como PDF") e prints do topo. Leia também
`~/.claude/carreira/perfil.md` para saber o cargo-alvo. Não faça login no
LinkedIn pela pessoa.

## Dê a nota

Leia `rubrica.json`. Treze itens, 100 pontos. Avalie todos, mostre a tabela,
dê o total. Seja honesto: a maioria fica entre 30 e 50 na primeira vez.

```
NOTA DO PERFIL  42/100

  título              3/12   "Analista na Empresa X"
  sobre (abertura)    2/9    "Profissional dinâmico e apaixonado por..."
  experiência atual   5/12   cargo e empresa, sem resultados
  competências        3/9    "Pacote Office" e "Trabalho em equipe" no topo
  ...
```

## Reescreva, na ordem dos pontos perdidos

**1. Título (220 caracteres).** É o campo que mais pesa na busca. Formato:
`{Cargo-alvo} | {2-3 competências buscadas} | {setor ou diferencial}`. Dê três
opções. Para quem está em transição, o cargo-alvo vem primeiro, com honestidade
("Analista de Dados em formação | SQL, Power BI | ex-Administrativo").

**2. Sobre.** As duas primeiras linhas aparecem antes de "ver mais": o que a
pessoa faz, para quem, e um resultado. Depois: principais resultados com
números, competências (que viram palavra-chave de busca), o que busca agora e
como falar com ela. Primeira pessoa. Até uns 1.500 caracteres.

**3. Experiência atual e as duas anteriores.** Uma linha de escopo e 3 a 5
marcadores com verbo de ação, ferramenta e resultado. Pode reaproveitar o
currículo (rode `/li-curriculo` antes, se ainda não rodou).

**4. Competências.** As três primeiras = as três pelas quais quer ser
contratada. Tire as genéricas do topo.

**5. Preferências de vaga e localização.** Configure cargos, modalidade e
cidades em "Tenho interesse em". O selo "Open to work" público é escolha
pessoal: ajuda a ser achado, mas algumas pessoas preferem deixar visível só
para recrutadores. Explique as duas opções.

**6. URL, foto, capa, destaque, recomendações.** Ajustes rápidos. Para
recomendações, escreva um pedido curto que a pessoa pode mandar ao ex-gestor
citando um projeto específico.

## Regras

- **Nunca invente** cargo, resultado ou certificação. Faltou número: `{{seu número}}`.
- **Coerência com o currículo:** cargos, empresas e datas iguais nos dois.
  Recrutador compara.
- **Nada de dados pessoais desnecessários** no Sobre (idade, estado civil).
- Passe todo texto reescrito por `/li-humano`.

## Saída

Tabela de notas, depois os textos prontos para colar na ordem de correção, e a
nova nota no fim, honesta. Se chegou a 82 e não a 98, diga 82 e o que falta
(geralmente recomendações e atividade, que não se resolvem reescrevendo).

Nada é alterado no LinkedIn por esta skill. A pessoa cola cada campo.
