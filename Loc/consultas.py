#Você deve importar as seguintes bibliotecas para funcionar o codigo!
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

#Class Planilha excel
class motivo():

  def __init__(self, planilha) -> None:
    self.planilha = self.planilha_excel(planilha)
  #recebe planilha e trata colunas
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

#Essas funções tem uma base de consulta no MYSQL, e estamos acessando os valores totais retornados delas.  
def Total_Avaria():
  Avarias = QuantidadeAvarias()
  Total_de_Avarias = Avarias[0]['QuantidadeAvaria']

  return Total_de_Avarias

def Total_Entregue():
    Entregue = QuantidadeEntregue()
    TotalEntregue = Entregue[0]['Quantidade_Entregue']

    return TotalEntregue

print(df_motivo.soma_motivos())