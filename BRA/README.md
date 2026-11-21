# Brazil — the 2022 census

The Censo Demográfico 2022, by IBGE, the Instituto Brasileiro de Geografia e Estatística. Reference date: the night of
31 July to 1 August 2022 (unconfirmed on an IBGE page: ibge.gov.br answered 403; see `provenance.json`).

- `counts.csv`: Brasil, its 27 Unidades da Federação (26 states and the Distrito Federal) and their 5,570 municípios,
  with the population collected, imputed and in total, from IBGE's workbook *População coletada e imputada no Censo
  Demográfico 2022, por Município e UF*. Read from the workbook's cells, not typed. Each município carries its 7-digit
  IBGE code (`ibge_code`: COD. UF followed by COD. MUNIC) and its UF's code (`uf_code`).
- `columns.csv`: what each column holds, with IBGE's own column headings as labels.
- `provenance.json`: the workbook, its digest, the licence as found (no IBGE terms could be read) and the checks:
  collected plus imputed equals the total on all 5,598 rows, each UF's municípios sum to it, and the UFs sum to
  Brasil's 203,080,756.

These are the *Primeiros Resultados* of 22 December 2023 (second count, 27 October 2023): totals only, not by sex or age.

Cite as: Instituto Brasileiro de Geografia e Estatística (IBGE), Censo Demográfico 2022, População e Domicílios,
Primeiros Resultados (22 de dezembro de 2023): População coletada e imputada, por Município e UF.
