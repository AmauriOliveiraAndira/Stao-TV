# Publicar atualização STAO

1. Extraia o ZIP e envie os arquivos à raiz do repositório, incluindo assets e .github/workflows. No Mac, Command + Shift + ponto mostra a pasta .github.
2. Em Settings → Pages → Source, mantenha GitHub Actions.
3. Execute Actions → Atualizar notícias e agenda STAO → Run workflow e aguarde atualizar e publicar ficarem verdes.
4. Reabra o painel na TV uma vez para carregar este código novo.

Notícias: até 100 manchetes únicas dos últimos 14 dias, de BBC News Brasil, Portal Contábeis, CFC, Brasil de Fato, Investing.com Brasil e Jovem Pan. A Agência Brasil foi removida.

O GitHub consulta os feeds a cada 10 minutos (minutos 7, 17, 27, 37, 47 e 57). O agendamento pode atrasar no GitHub. A TV verifica o JSON a cada minuto e mostra cada notícia por 20 segundos. Consultas não reiniciam a posição do rodízio. Os avisos de rotação e tempo de troca estão ocultos; fonte, data e contador permanecem.

A agenda agora é resumida e gerada a partir de agenda_regras.json. Envie esse arquivo e consulte EDITAR_AGENDA.md para editar rotinas, datas e feriados locais. A coleta detalhada da Receita Federal foi substituída pela tabela de pagamentos selecionados da Contabilizei e rotinas internas.

Tema escuro, logo original em assets/logo-stao.png, fontes ampliadas e ajuste proporcional à tela. Clima e agenda têm as bordas alinhadas. Setas do câmbio indicam o sinal da variação percentual informada pela AwesomeAPI.

A publicação usa os JSONs gerados diretamente, sem git commit/push durante a execução. A última coleta é recuperada do site antes de atualizar, preservando a acumulação de notícias e a conferência diária da agenda.

A TV exibe somente a semana atual e a seguinte (segunda a domingo), incluindo os vencimentos já ocorridos na semana atual. A janela muda automaticamente a cada semana. Gazeta do Povo incluída nas fontes de notícias.
