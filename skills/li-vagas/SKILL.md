---
name: li-vagas
description: >-
  Encontra vagas abertas no Brasil que combinam com o currículo e o objetivo da
  pessoa, ranqueia por aderência e diz o que falta para cada uma. Use quando
  pedirem "acha vagas para mim", "quais vagas combinam com meu perfil", "onde
  me candidatar", "vagas de X em Y", ou quando a pessoa está em busca de
  emprego ou recolocação.
---

# li-vagas

A skill de busca. Usa pesquisa na web e o script de aderência de `/li-adaptar`:

```bash
python3 ../li-adaptar/aderencia.py curriculo.pdf vagas/*.txt
```

## Antes de buscar

Leia `~/.claude/carreira/perfil.md`. Se não existir, pergunte numa mensagem só:

1. **Cargo(s)-alvo** (até três nomes, porque o mesmo trabalho tem nomes
   diferentes: "Analista de Dados", "Analista de BI", "Analista de Inteligência
   de Mercado").
2. **Cidade e modalidade** (presencial em X, híbrido, remoto Brasil).
3. **Nível** (estágio, júnior, pleno, sênior, coordenação).
4. **Regime** (CLT, PJ, estágio, temporário, concurso) e o que é inegociável.

E peça o currículo, se ainda não tiver.

## Onde buscar

Use a ferramenta de busca na web desta sessão. Fontes públicas, sem login:

- **Gupy** (portal.gupy.io, a maior parte das vagas de médias e grandes empresas)
- **Vagas.com.br, Catho, InfoJobs, Indeed Brasil**
- **LinkedIn Vagas** (páginas públicas de vaga)
- **Páginas "Trabalhe conosco"** das empresas da cidade ou do setor
- **Programas de estágio e trainee** (Cia de Talentos, empresas grandes)
- **Concursos** (PCI Concursos), se a pessoa considerar setor público
- **Sites de nicho** da área (ex.: Programathor e GeekHunter para tecnologia)

Busque cada cargo-alvo separadamente, com cidade e modalidade. Prefira vagas
publicadas nos últimos 30 dias e confirme que ainda estão abertas.

**Regras inegociáveis:**

- **Nunca faça login no LinkedIn nem em plataforma nenhuma pela pessoa** e nunca
  peça senha.
- **Isso é busca, não raspagem.** Leia algumas dezenas de vagas em ritmo
  humano. Coleta automatizada em volume viola os termos de uso do LinkedIn e
  das plataformas e pode bloquear a conta.
- **Nunca se candidate pela pessoa.** Esta skill encontra e analisa; quem se
  candidata é ela.
- **Desconfie de golpe:** vaga que pede pagamento, "taxa de cadastro", curso
  obrigatório pago, Pix, ou contato só por WhatsApp sem empresa identificável.
  Aponte esses sinais.

## Ranquear

1. Salve o texto de cada vaga em `vagas/NN-empresa-cargo.txt` (título, empresa,
   cidade/modalidade, link e a descrição completa).
2. Rode o script de aderência com todas as vagas.
3. Junte ao número o que o script não vê: **regime, faixa salarial (se
   divulgada), porte e reputação da empresa, distância, data de publicação.**

## Saída

```
VAGAS  ·  Analista de Dados · BH/híbrido ou remoto · pleno/sênior · 14 analisadas

TOP 5
 1. 90%  Analista de Dados Sr · Rede Varejo X · híbrido BH · CLT · publicada há 4 dias
         falta: dbt (diferencial)                                   [link]
 2. 78%  Analista de BI Pleno · Empresa Y · remoto · CLT · R$ 7-9 mil
         falta: Looker, inglês avançado (confira)                   [link]
 ...

DESCARTADAS
 - 3 com aderência abaixo de 40%
 - 1 com sinais de golpe (pede taxa de inscrição)

PADRÃO
 Das 14 vagas, 9 pedem dbt ou Airflow. Vale estudar um dos dois.

PRÓXIMO PASSO: escolha uma e rode /li-adaptar com ela.
```

Grave a lista em `~/.claude/carreira/vagas.md` com data, link e status
("analisada", "candidatado em dd/mm"), para não repetir a busca.

Diga sempre: aderência é estimativa por palavras e requisitos, não garantia de
ser chamado.
