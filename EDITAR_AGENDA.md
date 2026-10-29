# Editar a agenda STAO

Edite agenda_regras.json no GitHub. A próxima publicação gera a agenda a partir dessa tabela, sem coletar centenas de códigos da Receita Federal.

## Rotinas do escritório

| Regra mensal | Rotina |
| --- | --- |
| 1º dia útil | Solicitar lançamentos às empresas — horas extras, comissões e relógio de ponto |
| 1º dia útil | Iniciar fechamento dos motoristas TransPaludetto |
| 1º dia útil | Iniciar fechamento da folha de pagamento |
| 5º dia útil | Último dia para enviar a folha de pagamento às empresas |
| 12º dia útil | Enviar guia do MEI |
| Dia 20 | Enviar os parcelamentos |

Os prazos acima são internos, não representam vencimentos legais. A contagem exclui sábados, domingos e feriados nacionais de data fixa. Sábados não entram no 5º dia útil interno; não é uma regra de cálculo do prazo legal de pagamento de salários. Acrescente feriados locais, religiosos, Carnaval, Corpus Christi e dias de fechamento adotados pelo escritório em extra_holidays, com datas no formato AAAA-MM-DD.

## Campos da tabela

- name: texto curto mostrado na TV.
- kind: Escritório ou Fiscal.
- rule: business para dia útil; calendar para dia do mês; last_business para último dia útil.
- day: número do dia útil ou do dia do mês. Use 0 em last_business.
- adjust: none mantém a data; before antecipa para dia útil; after prorroga para dia útil.
- detail: complemento curto. Use números, como 1º, 5º, 12º e 20.
- months: opcional; por exemplo [1, 4, 7, 10] para meses de pagamento trimestral.
- enabled: false desativa uma linha sem apagá-la.

Para uma data avulsa, adicione em dated_items:

```json
{"date":"2026-11-10","name":"Reunião do escritório","kind":"Escritório","detail":"Às 9h"}
```

As datas fiscais vêm somente das regras de pagamento selecionadas do artigo da Contabilizei, atualizado em 2024: DAS/PGDAS-D, DAS MEI, folha, PIS/Cofins e IRPJ/CSLL. Declarações com regras antigas no artigo, obrigações específicas e ICMS por enquadramento estadual foram excluídos. Não é uma agenda fiscal completa; ajuste a tabela às empresas e a eventuais prorrogações. Impostos usam o mesmo calendário configurado; feriados locais/religiosos devem ser cadastrados pelo responsável.

O gerador prepara o mês atual e o próximo e o painel exibe os próximos vencimentos, incluindo rotinas do início do mês seguinte. Datas passadas somem da TV. A agenda alterna três registros por vez.
