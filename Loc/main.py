from consultas import Total_Entregue, Total_Avaria, Quantidade_Entregue_Errada, Item_Entregue_Errado, Ausencia_de_Item


#////////////////    CARD PERCENTUAL AVARIAS / ENTREGUE (TAXA) ////////////////
def Percentual_Avarias_Entregues():

  TaxaAvarias_Entregues = Total_Avaria() / Total_Entregue()

  TaxaAvarias_Entregues = "{:.2%}".format(TaxaAvarias_Entregues)

  return TaxaAvarias_Entregues

#/////////////////  CARD COM PERCENTUAL DE FALHAS DE SEPARAÇÃO LOGISTICA     ///////////////////
def Falhas_Separacao():

  Soma_todosmotivos = Quantidade_Entregue_Errada + Item_Entregue_Errado + Ausencia_de_Item

  FalhaSeparacao_Taxa = Soma_todosmotivos / Total_Entregue()
  
  FalhaSeparacao_Taxa = "{:.2%}".format(FalhaSeparacao_Taxa)

  return FalhaSeparacao_Taxa

def FalhaSeparacao_Avarias():
  Soma_todosmotivos = Quantidade_Entregue_Errada + Item_Entregue_Errado + Ausencia_de_Item + Total_Avaria()

  Taxa_FalhaSeparacao_Avaria = Soma_todosmotivos / Total_Entregue()

  Taxa_FalhaSeparacao_Avaria = "{:.2%}".format(Taxa_FalhaSeparacao_Avaria)

  return Taxa_FalhaSeparacao_Avaria


print(Falhas_Separacao())