from sqlalchemy import text 
from controller import get_connection
from datetime import date, datetime
from dateutil.relativedelta import *
import pandas as pd

hoje  = datetime.today()
#mes
mes_atual = date.today().strftime('%Y-%m')
#mes passado
passado = (hoje)+relativedelta(months=-1)
mespassado = passado.strftime('%Y-%m')


# CONSULTAS DO BANCO DE DADOS
#consulta do BD em cima da tabela  select * from HauszMapa.Pedidos.LogPedidos where ParaIdEtapaFlexy = 9
def Quant_entregue():
    engine = get_connection()
    list_entregue = []
    with engine.connect() as conn:
        query_entregue  = (text(f"""
        select COUNT(lg.CodigoPedido) as Quantidade_Entregue from HauszMapa.Pedidos.LogPedidos lg
        JOIN (SELECT CodigoPedido
        ,MAX(IdLog) ultimaetapa
        FROM [HauszMapa].[Pedidos].[LogPedidos]
        WHERE IdUsuarioAlteracao = 'Aplicacao' 
        GROUP BY CodigoPedido) maxlog
        ON maxlog.CodigoPedido = lg.CodigoPedido
        where ParaIdEtapaFlexy = 9 
		AND lg.IdLog = maxlog.ultimaetapa
        AND DataAtualizacao between '{mespassado}-01' and '{mes_atual}-01'
		AND IdUsuarioAlteracao = 'Aplicacao'
        """))
        lista_entreguetotal = conn.execute(query_entregue).all()
        for lista in lista_entreguetotal:
            dict_filtro_hoje = {}
            for keys, values in lista.items():
                dict_filtro_hoje[keys] = values
            list_entregue.append(dict_filtro_hoje)

    return list_entregue

#consulta do BD em cima da tabela  select *  from HauszMapa.Logistica.LogReversaOcorrencia = 1
def Quant_avaria():
    engine = get_connection()
    list_avaria = []
    with engine.connect() as conn:
        query_avaria = (text(f"""
        select count(avarias.Avarias) QuantidadeAvaria from
        (select  DISTINCT lr.CodigoPedido Avarias
		from HauszMapa.Logistica.LogReversaOcorrencia lr
		join(select CodigoPedido, max(IdOcorrencia) ultimaetapa ,max(DataInserido) ultimadata
		from HauszMapa.Logistica.LogReversaOcorrencia 
		where IdCausaOcorrencia = 1
		GROUP BY CodigoPedido) maxlog on maxlog.CodigoPedido = lr.CodigoPedido
		--where lr.IdCausaOcorrencia = 1
		and DataInserido between '{mespassado}-01' and '{mes_atual}-01') avarias
        """))
        lista_avaria = conn.execute(query_avaria).all()
        for lista in lista_avaria:
            dict_avaria = {}
            for keys, values in lista.items():
                dict_avaria[keys] = values
            list_avaria.append(dict_avaria)

    return list_avaria

def Total_Avaria():
  Avarias = Quant_avaria()
  Total_de_Avarias = Avarias[0]['QuantidadeAvaria']

  return Total_de_Avarias

def Total_Entregue():
    Entregue = Quant_entregue()
    TotalEntregue = Entregue[0]['Quantidade_Entregue']

    return TotalEntregue
  
#FIM CONSULTA BANCO DE DADOS

#PLANILHA EXCEL 

class motivo():

  def __init__(self, planilha) -> None:
    self.planilha = self.planilha_excel(planilha)

  
  def planilha_excel(self, planilha):

    df = pd.read_excel(planilha)

    df.columns = ['CODIGO', 'FASE_ATUAL', 'CRIADOR', 'PV_CRIADO','NUMERO_PV','NUMERO_NF','MOTIVO_SOLICITACAO'
    ,'OBSERVACOES_SOLICITACAO','FASE_INICIAL'
    ,'FASE_GESTAO','FASE_CLIENTE','FASE_IMPLANTACAO_REPOSICAO','FASE_SHOW_ROOM'
    ,'PEDIDOS_REPROVADOS','FASE_AJUSTE_FISCAL','FASE_LOCALIZACAO_MERCADORIA','ROTEIRIZACAO_PV_LOCALIZADO'
    ,'SOLICITACAO_COLETA'
    ,'COLETA_APROVADA','COLETA_REPROVADA','SOLICITACAO_REEMBOLSO','ENVIO_EMAIL','CONCLUIDO','SEM_REPOSICAO'
    ,'LOCALIZACAO_MERCADORIA']

    return df


  def contagem_filtramotivo(self, motivo:str =''):  
    if motivo:
      df = self.planilha.query(f'MOTIVO_SOLICITACAO =="{motivo}"')
      contagem = len(df)

    return contagem
        
    
#planilha excel
df_motivo = motivo('relatorio_kpi0707.xlsx')

#motivos
Quantidade_Entregue_Errada = df_motivo.contagem_filtramotivo('Item entregue na quantidade errada')
Item_Entregue_Errado = df_motivo.contagem_filtramotivo('Item entregue errado')
Ausencia_de_Item = df_motivo.contagem_filtramotivo('Item presente na Nota Fiscal mas não foi entregue')