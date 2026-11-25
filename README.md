# Painel de repetição de exames · RED 8

Análise executiva da repetição de exames laboratoriais pagos à RED 8, com pedidos de **janeiro a outubro de 2026 (10 meses)**.

**Abrir o painel:** abra o arquivo `index.html` no navegador. Ele funciona sozinho, sem internet e sem instalar nada, porque os dados já estão dentro do arquivo.

## Abas

| Aba | O que mostra |
|---|---|
| **Eletivos** | Atendimentos Externo + Ambulatório. Repetição em até 1, 3, 6 ou 10 meses, por exame, quem pede (mesmo médico × outro médico) e cenários de economia. |
| **Urgência e Internação** | Repetição em até 6 h, 24 h, 72 h ou 7 dias, com a área onde acontece (CTI/UCI, pronto-socorro, enfermarias), os exames, e cenários de economia. |
| **Médicos (eletivos)** | Médicos com 100 pacientes ou mais, comparados por repetições por paciente e por custo. |

## Como os números são calculados

- **Repetição:** o mesmo exame (mesmo código) pedido de novo para o mesmo paciente (mesmo número SAME) em outro pedido. O primeiro exame nunca conta.
- **Fase:** tempo desde o exame anterior do mesmo paciente.
- **Valores:** soma do valor pago à RED 8 (valor corrigido quando a planilha tem essa coluna). **Não são médias.**
- **"Por ano":** soma dos 10 meses × 12/10. "No período" é a soma dos 10 meses.
- **Fora da conta:** pedidos excluídos. Repetições de exames feitos antes de janeiro/2026 não aparecem.

**Atenção:** o valor é um teto. Parte da repetição é clinicamente necessária, como tratamento oncológico, exames seriados no PS e rotina de CTI.

## Arquivos

- `index.html` — o painel, com os dados agregados embutidos (sem nome de paciente).
- `logos/` — logos da São Cristóvão Saúde e da São Cristóvão Medicina Diagnóstica.
- `scripts/` — scripts Python usados para gerar os números a partir das planilhas de repasse. As planilhas originais não estão no repositório.
