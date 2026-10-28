# Publicar atualização STAO

1. Extraia o ZIP e envie os arquivos à raiz do repositório, incluindo assets e .github/workflows. No Mac, Command + Shift + ponto mostra a pasta .github.
2. Em Settings → Pages → Source, mantenha GitHub Actions.
3. Execute Actions → Atualizar notícias e agenda STAO → Run workflow e aguarde atualizar e publicar ficarem verdes.
4. Reabra o painel na TV uma vez para carregar este código novo.

Notícias: até 100 manchetes únicas dos últimos 14 dias, de BBC News Brasil, Portal Contábeis, CFC, Brasil de Fato, Investing.com Brasil e Jovem Pan. A Agência Brasil foi removida.

O GitHub consulta os feeds a cada 10 minutos (minutos 7, 17, 27, 37, 47 e 57). O agendamento pode atrasar no GitHub. A TV verifica o JSON a cada minuto e mostra cada notícia por 20 segundos. Consultas não reiniciam a posição do rodízio. Os avisos de rotação e tempo de troca estão ocultos; fonte, data e contador permanecem.

A coleta federal da agenda continua diária e exibe três obrigações por vez, com troca a cada 16 segundos. Prazos estaduais precisam de validação específica em agenda_estadual.json. Falhas preservam a última coleta; datas de meses passados são excluídas da tela.

Tema escuro, logo original em assets/logo-stao.png, fontes ampliadas e ajuste proporcional à tela. Clima e agenda têm as bordas alinhadas. Setas do câmbio indicam o sinal da variação percentual informada pela AwesomeAPI.
