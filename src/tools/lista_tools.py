from src.tools.consultar_historico import consultar_historico_paciente
from src.tools.verificar_interacoes import verificar_interacoes_medicamentosas
from src.tools.agendar_teleconsulta import agendar_teleconsulta
from src.tools.buscar_exames import buscar_exames_paciente
from src.tools.registrar_sintoma import registrar_sintoma_vital

# Centralizamos a lista aqui para evitar importações circulares
tools_disponiveis = [
    consultar_historico_paciente, 
    verificar_interacoes_medicamentosas, 
    agendar_teleconsulta,
    buscar_exames_paciente,
    registrar_sintoma_vital
]