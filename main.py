from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os


os.environ["GOOGLE_API_KEY"] = 'AIzaSyDrUIYaUuml3TpFBHA4il80bzC3O2pJOeE'


def call_agent(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response


def agente_buscador(peso, altura, idade, sexo, nivel_de_atividade, objetivo):
    buscador = Agent(
        name="agente_buscador",
        model="gemini-2.0-flash",
        description="Agente que busca informações no Google.",
        tools=[google_search],
        instruction="""Você é um nutricionista e precisa calcular a taxa metabólica basal, gasto calórico diário e
                    gasto calórico total de acordo com o peso, altura, idade, sexo, nível de atividade física e objetivo
                    informados abaixo. Utilize a fórmula de Harris-Benedict""")

    entrada_do_agente_buscador = f"peso: {peso}\n" \
                                 f"altura: {altura}\n" \
                                 f"idade: {idade}\n" \
                                 f"sexo: {sexo}\n" \
                                 f"nivel de atividade física: {nivel_de_atividade}\n" \
                                 f"objetivo: {objetivo}\n"
    lancamento = call_agent(buscador, entrada_do_agente_buscador)
    return lancamento


def agente_planejador(values_pacient, alimentos_restritos, qtd_refeicoes):
    planejador = Agent(
        name="agente_planejador",
        model="gemini-2.0-flash",
        instruction="""
        Você é um nutricionista que recebeu a taxa metabólica basal, gasto calórico diário e gasto calórico total de um
        paciente e precisa elaborar uma dieta que seja igual ao Gasto Calórico Total (GCT) e que não inclua os alimentos
        restritos e que contenha a quantidade de refeições diárias informada.
        """,
        description="Agente que planeja posts",
        tools=[google_search]
    )

    entrada_do_agente_planejador = f"Lançamentos buscados: {values_pacient}\n" \
                                   f"alimentos restritos: {alimentos_restritos}\n" \
                                   f"quantidade de refeições: {qtd_refeicoes}\n"
    plano_do_post = call_agent(planejador, entrada_do_agente_planejador)
    return plano_do_post


def salvar_pdf(diet_plan, type):
    if type == "informations":
        file_name = "diets/calculos_usuario.pdf"
    else:
        file_name = "diets/plano_alimentar.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()
    resposta_formatada = diet_plan.replace("\n", "<br/>")  # Substitui quebras de linha por tags HTML <br/>
    paragrafo = Paragraph(resposta_formatada, styles['Normal'])

    doc.build([paragrafo])


print("Bem-vindo ao Planejador de dietas da FRPelissari")
peso = input("Digite seu peso, somente número (ex: 80): ")
while not peso:
    peso = input("Não podemos prosseguir sem essa informação, por favor, digite seu peso, somente número (ex: 80): ")
altura = input("Digite sua altura em cm (ex: 174): ")
while not altura:
    altura = input("Não podemos prosseguir sem essa informação, por favor, digite sua altura em cm (ex: 174): ")
idade = input("Digite sua idade, somente número (ex: 36): ")
while not idade:
    idade = input("Não podemos prosseguir sem essa informação, por favor, digite sua idade, somente número (ex: 36): ")
sexo = int(input("Qual seu sexo?\nDigite 1 para sexo masculino\nDigite 2 para sexo feminino: "))
while not sexo:
    sexo = int(input("Não podemos prosseguir sem essa informação, por favor, qual seu sexo?\n"
                 "Digite 1 para sexo masculino\nDigite 2 para sexo feminino: "))
atividade = int(input("Agora precisamos saber seu nível de atividade física.\n"
                  "Digite 1 para Sedentário: Pouco ou nenhum exercício.\n"
                  "Digite 2 para Levemente Ativo: Exercício leve (1 a 3 dias por semana).\n"
                  "Digite 3 para Moderadamente Ativo: Exercício moderado (3 a 5 dias por semana).\n"
                  "Digite 4 para Muito Ativo: Exercício intenso (6 a 7 dias por semana).\n"
                  "Digite 5 para Extremamente Ativo: Exercício muito intenso ou trabalho físico pesado diário."))
while not atividade:
    atividade = int(input("Não podemos prosseguir sem essa informação, por favor, digite seu nível de atividade física.\n"
                      "Digite 1 para Sedentário: Pouco ou nenhum exercício.\n"
                      "Digite 2 para Levemente Ativo: Exercício leve (1 a 3 dias por semana).\n"
                      "Digite 3 para Moderadamente Ativo: Exercício moderado (3 a 5 dias por semana).\n"
                      "Digite 4 para Muito Ativo: Exercício intenso (6 a 7 dias por semana).\n"
                      "Digite 5 para Extremamente Ativo: Exercício muito intenso ou trabalho físico pesado diário."))
objetivo = int(input("Qual seu objetivo?\nDigite 1 para emagrecimento\nDigite 2 para hipertrofia\nDigite 3 para manutenção."))
while not objetivo:
    objetivo = int(input("Não podemos prosseguir sem essa informação, por favor, qual seu objetivo?\nDigite 1 para "
                     "emagrecimento\nDigite 2 para hipertrofia\nDigite 3 para manutenção."))
restricoes = input("Algum alimento que não gosta ou tem restrição?"
                   "\nDigite aqui (caso não tenha, escreva \"não\"): ")
while not restricoes:
    restricoes = input("Não podemos prosseguir sem essa informação, por favor,\n"
                       "Algum alimento que não gosta ou tem "
                       "restrição?\nDigite aqui (caso não tenha, escreva \"não\"): ")
qtd_refeicoes = int(input("Quantas refeições deseja fazer no dia?\nDigite um número: "))
while not qtd_refeicoes:
    qtd_refeicoes = int(input("Não podemos seguir sem essa informação, por favor, quantas refeições deseja fazer no dia?\n"
                              "Digite um número: "))
list_atividades = ['Nível de Atividade Física',
                   'Sedentário',
                   'Levemente Ativo',
                   'Moderadamente Ativo',
                   'Muito Ativo',
                   'Extremamente Ativo'
                   ]
list_sexo = ['sexo',
             'masculino',
             'feminino'
             ]
list_objetivo = ['objetivo',
                 'emagrecimento',
                 'hipertrofia',
                 'manutenção']
print("Suas informações para a elaboração do seu plano:",
      f"Peso: {peso} Kg",
      f"Altura: {altura} cm",
      f"Idade: {idade} anos",
      f"Sexo: {list_sexo[sexo]}",
      f"Nível de atividade: {list_atividades[atividade]}",
      f"Objetivo: {list_objetivo[objetivo]}",
      f"Restrições: {restricoes}",
      F"Qtd refeições: {qtd_refeicoes}",
      "Vamos iniciar a elaboração do seu plano alimentar, aguarde!",
      sep="\n")

lancamentos_buscados = agente_buscador(peso, altura, idade, list_sexo[sexo], list_atividades[atividade], list_objetivo[objetivo])
print(lancamentos_buscados)

if restricoes == "não":
    restricoes_diet = "Sem nenhuma restrição"
else:
    restricoes_diet = restricoes

diet_plan = agente_planejador(lancamentos_buscados, restricoes_diet, qtd_refeicoes)
salva_pdf = int(input("Gostaria de salvar sua dieta em pdf?\nDigite:\n1 para sim\n2 para não\n"))
if salva_pdf == 1:
    salvar_pdf(lancamentos_buscados, "informations")
    salvar_pdf(diet_plan, "diet_plan")
else:
    print(diet_plan)
