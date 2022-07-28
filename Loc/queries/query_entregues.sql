select COUNT(lg.CodigoPedido) as Quantidade_Entregue from HauszMapa.Pedidos.LogPedidos lg
        JOIN (SELECT CodigoPedido
        ,MAX(IdLog) ultimaetapa
        FROM [HauszMapa].[Pedidos].[LogPedidos]
        WHERE IdUsuarioAlteracao = 'Aplicacao' 
        GROUP BY CodigoPedido) maxlog
        ON maxlog.CodigoPedido = lg.CodigoPedido
        where ParaIdEtapaFlexy = 9 
		AND lg.IdLog = maxlog.ultimaetapa
        AND MONTH(GETDATE()) - MONTH(DataAtualizacao) = 1
		AND IdUsuarioAlteracao = 'Aplicacao'