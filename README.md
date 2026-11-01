# LinkedIn Carreira Skill (PT-BR)

Dez skills do Claude para **carreira e LinkedIn no mercado brasileiro**, em
português. Grátis, licença MIT, sem cadastro, sem chave de API, nada para
conectar à sua conta do LinkedIn.

Analisa currículo, dá nota ao perfil, mostra onde melhorar, procura vagas que
combinam com você, adapta o currículo para cada vaga, prepara para a entrevista
e pesquisa salário com fonte. E também escreve posts e comentários que não soam
como robô.

**Nada é enviado sem você.** As skills analisam e escrevem. Você revisa, se
candidata e publica.

Estrutura inspirada no [linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)
de Jake Schincariol (MIT). A parte de carreira (currículo, vagas, aderência,
entrevista, salário) é nova e foi escrita para o Brasil.

## Instalar

No Claude Code:

```
/plugin marketplace add mpjbiologo/linkedin-carreira-skillPTBR
/plugin install linkedin-carreira
```

Ou à mão:

```bash
git clone https://github.com/mpjbiologo/linkedin-carreira-skillPTBR.git
cp -r linkedin-carreira-skillPTBR/skills/li-* ~/.claude/skills/
```

Sem Claude Code? Cole qualquer `SKILL.md` no começo de uma conversa no app do
Claude e anexe seu currículo. Você perde os scripts automáticos, mas as
instruções funcionam.

Primeiro passo: copie `templates/perfil-carreira.md` para
`~/.claude/carreira/perfil.md` e preencha (cargo-alvo, cidade, nível), ou diga
ao Claude "preenche meu perfil de carreira".

## As dez

| comando | o que faz |
| --- | --- |
| `/li-curriculo` | Nota de 0 a 100 para o currículo (PDF, Word ou texto) em 9 critérios, aponta dados pessoais que não deveriam estar lá (LGPD) e reescreve sem inventar. |
| `/li-adaptar` | Compara currículo e vaga, mostra a aderência item por item e adapta resumo, experiências e carta para aquela vaga. |
| `/li-vagas` | Busca vagas públicas (Gupy, Vagas, Catho, LinkedIn, sites das empresas), ranqueia por aderência e aponta sinais de golpe. |
| `/li-perfil` | Nota do perfil numa [rubrica de 13 itens](skills/li-perfil/rubrica.json) e reescrita de título, sobre, experiências e competências. |
| `/li-entrevista` | Perguntas prováveis, respostas STAR com suas histórias reais, pretensão salarial, perguntas difíceis e simulação. |
| `/li-salario` | Faixa salarial com fontes (Novo Caged, guias salariais, vagas com faixa), conta CLT x PJ e roteiro de negociação. |
| `/li-post` | Post em português com três aberturas de [21 fórmulas](skills/li-post/ganchos.json), com nota. |
| `/li-comentario` | Comentários que dizem algo, para ser visto por gestores e recrutadores da área. |
| `/li-plano` | Plano semanal de busca de vaga: candidaturas, contatos, comentários, post e revisão. |
| `/li-humano` | Tira a cara de IA e o tom de coach do texto em português. |

## Os scripts que rodam

Sem internet, nada é enviado. Rodam no seu computador.

```bash
python3 skills/li-curriculo/curriculo.py meu_curriculo.pdf
python3 skills/li-adaptar/aderencia.py meu_curriculo.pdf vaga.txt
python3 skills/li-adaptar/aderencia.py meu_curriculo.pdf vagas/*.txt     # ranking
python3 skills/li-post/nota_gancho.py aberturas.txt
python3 skills/li-humano/humanizar.py post.txt -o limpo.txt --relatorio
python3 skills/li-humano/detectar.py post.txt limpo.txt
```

Ler PDF precisa de `pypdf` (`pip install pypdf`) ou do programa `pdftotext`.
Word e texto funcionam sem nada.

Exemplo, currículo:

```
NOTA DO CURRÍCULO  ·  cv.txt
  FALHA   DADOS PESSOAIS   0/12   remova: CPF, data de nascimento, estado civil, filhos, endereço completo
  FALHA   RESULTADOS       0/20   0 de 5 linhas de experiência têm número, %, R$ ou volume
  FALHA   VERBOS DE AÇÃO   0/12   3 com "Responsável por"/"Auxiliar"
  FALHA   CLICHÊS          0/8    proativo, dinâmico, comunicativo, agregar valor...
  NOTA  17/100
```

Exemplo, aderência a uma vaga:

```
  REQUISITOS  6/6 cobertos
  DIFERENCIAIS  2/3 cobertos
   ✖ Conhecimento em dbt
       não aparece no currículo: dbt
  CONFIRA À MÃO
   - anos de experiência: "4 anos de experiência"
   - modalidade/local: "Híbrido"
  ADERÊNCIA ESTIMADA  90%
```

## Honestidade sobre os limites

- **Não é a Gupy.** Plataformas como a Gupy usam modelos próprios que leem
  contexto (a própria Gupy diz que sua ordenação analisa experiências,
  habilidades e formação, e não é um filtro eliminatório automático). Os
  scripts daqui medem boas práticas e cobertura de requisitos. Nota alta não
  garante entrevista; nota baixa costuma explicar o silêncio.
- **Nada é inventado.** Nenhuma experiência, ferramenta, certificação ou número
  entra no seu currículo sem você confirmar. Faltou dado: `{{seu número}}`.
  Informação falsa em currículo é motivo de desclassificação e de demissão.
- **Sem raspagem e sem automação no LinkedIn.** A busca de vagas lê páginas
  públicas em ritmo humano, nunca faz login por você, nunca se candidata por
  você e nunca manda mensagem automática. Automação viola os termos do LinkedIn
  e pode restringir a conta.
- **Salário é estimativa** a partir de fontes públicas, citadas com data. Varia
  por empresa. A conta CLT x PJ não é consultoria contábil.
- **O detector de IA é local**, não GPTZero nem Turnitin.

## Arquivos

```
skills/li-curriculo/curriculo.py     nota do currículo (PDF/DOCX/TXT), LGPD, resultados, verbos, clichês
skills/li-curriculo/criterios.json   os 9 critérios e pesos
skills/li-adaptar/aderencia.py       currículo x vaga, item por item, e ranking de várias vagas
skills/li-perfil/rubrica.json        rubrica de 100 pontos para perfil de LinkedIn
skills/li-post/ganchos.json          21 fórmulas de abertura com exemplos de carreira
skills/li-post/nota_gancho.py        nota da abertura do post
skills/li-humano/cliches.json        ~200 clichês (bloco LinkedIn), 20 estruturas
skills/li-humano/humanizar.py        limpeza automática
skills/li-humano/detectar.py         painel de cinco checagens
templates/perfil-carreira.md         seu objetivo de carreira. Preencha primeiro.
templates/voz.md                     como você escreve, para posts e comentários
```

## Créditos

Marcos de Paula Júnior ([@mpjbiologo](https://github.com/mpjbiologo)). Estrutura
inspirada em [linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill),
de Jake Schincariol (MIT). Feito com apoio de IA (Claude) e revisado pelo autor.

## Licença

MIT. Veja [LICENSE](LICENSE).
