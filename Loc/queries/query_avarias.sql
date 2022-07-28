select count(avarias.Avarias) QuantidadeAvaria from
        (select  DISTINCT lr.CodigoPedido Avarias
		from HauszMapa.Logistica.LogReversaOcorrencia lr
		join(select CodigoPedido, max(IdOcorrencia) ultimaetapa ,max(DataInserido) ultimadata
		from HauszMapa.Logistica.LogReversaOcorrencia 
		where IdCausaOcorrencia = 1
		GROUP BY CodigoPedido) maxlog on maxlog.CodigoPedido = lr.CodigoPedido
		--where lr.IdCausaOcorrencia = 1
		where MONTH(getdate()) - month(DataInserido) = 1) as avarias


		--funcionalidade month(getdate()) filtrar meses apartir de uma data