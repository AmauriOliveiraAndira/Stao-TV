# Publicar a atualização STAO

1. Envie os arquivos deste pacote para a raiz do repositório, preservando a pasta `.github/workflows` e substituindo os arquivos existentes. Mantenha `news.json` no repositório.
2. Em Settings → Pages → Build and deployment → Source, selecione **GitHub Actions**.
3. Em Actions, abra **Atualizar notícias e agenda STAO** e clique em Run workflow. O envio para main também inicia a publicação.
4. Aguarde os dois trabalhos ficarem verdes e recarregue a TV uma vez.

A coleta federal ocorre uma vez por dia, aproveitando a execução de notícias a cada duas horas. A TV consulta agenda.json a cada 30 minutos e alterna três obrigações a cada 16 segundos. A execução agendada pode atrasar no GitHub.

São coletados os vencimentos publicados pela Receita Federal para os grupos de rotina contábil configurados no script. Não é uma agenda exaustiva para todos os contribuintes. As datas e códigos específicos são preservados. Se o calendário falhar ou mudar de formato, a execução sinaliza falha na etapa da agenda e conserva os dados anteriores; o painel exclui outros meses e dias vencidos.

A Contabilizei é referência das categorias, e não fonte automática de datas atuais. FGTS e prazos estaduais não publicados pela RFB não fazem parte da coleta federal. agenda_estadual.json preserva somente datas estaduais conferidas individualmente, sem repetição automática. Para novos meses, a agenda federal atualiza automaticamente; a estadual exige validação específica.

Notícias: Agência Brasil (Economia e Últimas), Portal Contábeis, Conselho Federal de Contabilidade Brasil de Fato e Investing.com Brasil. Coleta a cada duas horas, com até 30 manchetes distribuídas entre os feeds, fonte, data e excerto curto. São excluídos itens sem data e com mais de 14 dias. Em falha de uma fonte, preservam-se os itens recentes anteriores dessa fonte.

Tema escuro com letras ampliadas, azul-petróleo e cinzas da STAO. Inclua a pasta assets com logo-stao.png no envio. O painel ajusta a composição 16:9 automaticamente à área útil do navegador, sem rolagem.

Câmbio: as setas ↑, ↓ e → indicam o sinal de pctChange informado pela AwesomeAPI, acompanhado do percentual. Quando a variação não estiver disponível ou a consulta falhar, a seta direcional é removida. A logo original permanece em uma pequena superfície clara para preservar sua leitura.
