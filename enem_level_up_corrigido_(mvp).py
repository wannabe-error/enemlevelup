import os
import json
import random
from datetime import datetime, timedelta
from collections import defaultdict

class SistemaEstudoENEM:
    def __init__(self):
        """Inicializa o sistema de estudos para o ENEM"""
        self.ARQUIVO_USUARIOS = 'usuarios.json'
        self.ARQUIVO_PLANOS = 'planos_estudo.json'
        self.ARQUIVO_SIMULADOS = 'banco_simulados.json'
        self.ARQUIVO_DESEMPENHO = 'desempenho.json'
        self.ARQUIVO_CONQUISTAS = 'conquistas.json'

        self.usuarios = []
        self.planos = {}
        self.simulados = {"questoes": [], "proximo_id": 1} # Estrutura inicial para banco_simulados.json
        self.desempenho = {}
        self.conquistas = {}
        self.usuario_atual = None

        self.carregar_dados()
        self.inicializar_simulados()
        self.inicializar_conquistas()

    def carregar_dados(self):
        """Carrega todos os dados dos arquivos JSON"""
        try:
            if os.path.exists(self.ARQUIVO_USUARIOS):
                with open(self.ARQUIVO_USUARIOS, 'r') as f: self.usuarios = json.load(f) # Linha 25

            if os.path.exists(self.ARQUIVO_PLANOS):
                with open(self.ARQUIVO_PLANOS, 'r') as f: self.planos = json.load(f) # Linha 28

            # Carrega o banco de simulados com tratamento de erro (linhas condensadas)
            if os.path.exists(self.ARQUIVO_SIMULADOS): # Linha 30
                with open(self.ARQUIVO_SIMULADOS, 'r') as f: # Linha 31
                    try: self.simulados = json.load(f) # Linha 32
                    except json.JSONDecodeError: self.simulados = {"questoes": [], "proximo_id": 1} # Linha 33
            else: self.simulados = {"questoes": [], "proximo_id": 1} # Linha 34
            self.simulados.setdefault('questoes', []); self.simulados.setdefault('proximo_id', len(self.simulados['questoes']) + 1) # Linha 35 (Condensada)
            # Linha 36 (Removida, lógica em setdefault)

            if os.path.exists(self.ARQUIVO_DESEMPENHO):
                with open(self.ARQUIVO_DESEMPENHO, 'r') as f: self.desempenho = json.load(f) # Linha 39

            if os.path.exists(self.ARQUIVO_CONQUISTAS):
                with open(self.ARQUIVO_CONQUISTAS, 'r') as f: self.conquistas = json.load(f) # Linha 42

        except (json.JSONDecodeError, IOError) as e: # Linha 44 (Original linha 37)
            print(f"Erro ao carregar dados: {e}") # Linha 45
            self.usuarios = []; self.planos = {}; self.desempenho = {}; self.conquistas = {} # Linha 46
            self.simulados = {"questoes": [], "proximo_id": 1} # Linha 47 (Adicionado para consistência)

    def salvar_dados(self):
        """Salva todos os dados nos arquivos JSON (linhas condensadas)"""
        try:
            with open(self.ARQUIVO_USUARIOS, 'w') as f: json.dump(self.usuarios, f, indent=4) # Linha 50
            with open(self.ARQUIVO_PLANOS, 'w') as f: json.dump(self.planos, f, indent=4) # Linha 51
            with open(self.ARQUIVO_SIMULADOS, 'w') as f: json.dump(self.simulados, f, indent=4) # Linha 52 (NOVO)
            with open(self.ARQUIVO_DESEMPENHO, 'w') as f: json.dump(self.desempenho, f, indent=4) # Linha 53
            with open(self.ARQUIVO_CONQUISTAS, 'w') as f: json.dump(self.conquistas, f, indent=4) # Linha 54
        except IOError as e: print(f"Erro ao salvar dados: {e}") # Linha 55

    def inicializar_simulados(self):
        """Inicializa o banco de simulados se não existir. (Otimizado)"""
        if not os.path.exists(self.ARQUIVO_SIMULADOS): # Linha 59
            self.simulados = {"questoes": [], "proximo_id": 1} # Linha 60 (Descondensada)
            with open(self.ARQUIVO_SIMULADOS, 'w') as f: # Linha 61 (Descondensada)
                json.dump(self.simulados, f, indent=4) # Linha 62 (Descondensada)
        # O carregamento do simulado existente é feito em carregar_dados()

    def inicializar_conquistas(self):
        """Inicializa o sistema de conquistas se não existir"""
        if not os.path.exists(self.ARQUIVO_CONQUISTAS):
            self.conquistas = {
                "conquistas": [
                    {"nome": "Iniciante", "descricao": "Completou o cadastro", "pontos": 10, "tipo": "cadastro"},
                    {"nome": "Primeiros Passos", "descricao": "Completou o teste diagnóstico", "pontos": 20, "tipo": "diagnostico"},
                    {"nome": "Estudante Dedicado", "descricao": "Completou 1 semana de estudos", "pontos": 30, "tipo": "plano"},
                    {"nome": "Simulador", "descricao": "Realizou o primeiro simulado", "pontos": 40, "tipo": "simulado"},
                    {"nome": "Persistente", "descricao": "Manteve 7 dias consecutivos de estudo", "pontos": 50, "tipo": "frequencia"},
                    {"nome": "Mestre em Matemática", "descricao": "Acertou 80% em um simulado de Matemática.", "pontos": 60, "tipo": "area", "area": "Matemática"},
                    {"nome": "Redator Nota 1000", "descricao": "Acertou 90% em um simulado de Redação.", "pontos": 70, "tipo": "area", "area": "Redação"}
                ],
                "niveis": [
                    {"nivel": 1, "pontos_necessarios": 0},
                    {"nivel": 2, "pontos_necessarios": 100},
                    {"nivel": 3, "pontos_necessarios": 300},
                    {"nivel": 4, "pontos_necessarios": 600},
                    {"nivel": 5, "pontos_necessarios": 1000}
                ]
            }
            with open(self.ARQUIVO_CONQUISTAS, 'w') as f:
                json.dump(self.conquistas, f, indent=4)

    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_titulo(self, titulo):
        """Exibe um título formatado"""
        self.limpar_tela()
        print("\n" + "="*50)
        print(titulo.center(50))
        print("="*50 + "\n")

    def validar_email(self, email):
        """Valida o formato do email"""
        return '@' in email and '.' in email.split('@')[-1]

    def obter_numero(self, mensagem, minimo, maximo):
        """Obtém um número dentro de um intervalo"""
        while True:
            try:
                numero = int(input(mensagem))
                if minimo <= numero <= maximo:
                    return numero
                print(f"Digite um número entre {minimo} e {maximo}")
            except ValueError:
                print("Digite um número válido.")

    def tela_inicial(self):
        """Tela principal do sistema"""
        while True:
            self.mostrar_titulo("SISTEMA DE ESTUDOS PARA O ENEM")

            print("1. Fazer login")
            print("2. Criar conta")
            print("3. Admin (Adicionar Questões)") # Nova opção para o administrador
            print("4. Sair")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                if self.fazer_login():
                    self.menu_principal()
            elif opcao == "2":
                self.cadastrar_usuario()
            elif opcao == "3":
                self.menu_administrador() # Chama o menu de administrador (renomeado de mostrar_sobre)
            elif opcao == "4":
                print("\nObrigado por usar nosso sistema! Boa sorte no ENEM!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def menu_administrador(self): # Renomeado de mostrar_sobre
        """Menu exclusivo para o administrador adicionar, editar e ver questões."""
        senha = input("Digite a senha de administrador: ") # Linha 241
        if senha == "Cesar@2025": # Linha 242
            while True: # Linha 243
                self.mostrar_titulo("MENU DO ADMINISTRADOR") # Linha 244
                print("1. Adicionar Nova Questão") # Linha 245
                print("2. Editar Questão") # Nova opção para editar (linha 246)
                print("3. Excluir Questão") # Nova opção para excluir (linha 247)
                print("4. Visualizar Banco de Questões") # Linha 248 (Antiga 2)
                print("5. Voltar") # Linha 249 (Antiga 3)
                escolha = input("\nEscolha uma opção: ").strip() # Linha 250

                if escolha == '1': self.adicionar_questao() # Linha 251 (Condensada)
                elif escolha == '2': self.editar_questao() # Linha 252 (Condensada)
                elif escolha == '3': self.excluir_questao() # Linha 253 (Condensada)
                elif escolha == '4': self.visualizar_banco_questoes() # Linha 254 (Condensada)
                elif escolha == '5': break # Linha 255 (Condensada)
                else: print("\nOpção inválida. Tente novamente."); input("Pressione Enter para continuar...") # Linha 256 (Condensada)
                # Linha 257 (Removida)
                # Linha 258 (Removida)
                # Linha 259 (Removida)
                # Linha 260 (Removida)
                # Linha 261 (Removida)
                # Linha 262 (Removida)
                # Linha 263 (Removida)
        else: # Linha 264
            print("\nSenha de administrador incorreta.") # Linha 265
            input("Pressione Enter para continuar...") # Linha 266

    def cadastrar_usuario(self):
        """Processo completo de cadastro e onboarding"""
        self.mostrar_titulo("CRIAR CONTA")

        # Dados básicos
        nome = input("Nome completo: ").strip()
        while len(nome.split()) < 2:
            print("Por favor, digite seu nome completo.")
            nome = input("Nome completo: ").strip()

        email = input("E-mail: ").strip().lower()
        while not self.validar_email(email) or any(u['email'] == email for u in self.usuarios):
            if not self.validar_email(email):
                print("E-mail inválido. Digite novamente.")
            else:
                print("Este e-mail já está cadastrado.")
            email = input("E-mail: ").strip().lower()

        senha = input("Crie uma senha (mínimo 6 caracteres): ").strip()
        while len(senha) < 6:
            print("Senha muito curta. Mínimo 6 caracteres.")
            senha = input("Crie uma senha: ").strip()

        # Informações acadêmicas
        serie = input("Série/Ano (ex: 3º EM): ").strip()
        escola = input("Nome da escola: ").strip()
        idade = self.obter_numero("Idade: ", 10, 30)

        # Áreas de interesse
        print("\nÁreas de interesse (digite 'fim' para terminar):")
        areas_interesse = []
        while True:
            area = input("> ").strip()
            if area.lower() == 'fim':
                if len(areas_interesse) < 1:
                    print("Adicione pelo menos uma área!")
                    continue
                break
            if area:
                areas_interesse.append(area)

        # Cria o usuário
        novo_usuario = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "serie": serie,
            "escola": escola,
            "idade": idade,
            "areas_interesse": areas_interesse,
            "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pontuacao": 0,
            "nivel": 1
        }

        self.usuarios.append(novo_usuario)
        self.salvar_dados()

        # Onboarding
        print("\n✅ Cadastro realizado com sucesso!")
        input("Pressione Enter para o tutorial rápido...")
        self.mostrar_tutorial_onboarding()

        # Teste diagnóstico
        print("\nVamos agora realizar um teste diagnóstico rápido...")
        input("Pressione Enter para começar...")
        self.realizar_teste_diagnostico(novo_usuario)

        self.usuario_atual = novo_usuario
        self.menu_principal()

    def mostrar_tutorial_onboarding(self):
        """Tutorial rápido da plataforma"""
        self.mostrar_titulo("TUTORIAL RÁPIDO")

        print("""
Bem-vindo ao Sistema de Estudos para o ENEM!

Aqui você terá acesso a:

1. PLANO DE ESTUDOS PERSONALIZADO
   - Baseado no seu nível atual
   - Com metas semanais realistas
   - Focado nas áreas que você mais precisa

2. SIMULADOS ADAPTATIVOS
   - Questões no formato ENEM
   - Cronometrados como no dia da prova
   - Feedback imediato após cada questão

3. ACOMPANHAMENTO DE DESEMPENHO
   - Gráficos de evolução
   - Identificação de pontos fortes e fracos
   - Sugestões de melhoria

4. GAMIFICAÇÃO
   - Pontos por atividades completadas
   - Conquistas e medalhas
   - Ranking com outros estudantes

Vamos começar com um teste diagnóstico para conhecer seu nível atual!
        """)

        input("\nPressione Enter para continuar...")

    def realizar_teste_diagnostico(self, usuario):
        """Teste diagnóstico inicial mais completo"""
        self.mostrar_titulo("TESTE DIAGNÓSTICO")

        print("Responda as questões abaixo para avaliarmos seu nível inicial:\n")

        # Seleciona questões de diferentes áreas (agora puxa do novo formato)
        questoes = self.simulados.get('questoes', []) # Linha 357

        if not questoes: # Adicionado para evitar erro se não houver questões
            print("Não há questões disponíveis para o teste diagnóstico.")
            input("Pressione Enter para continuar...")
            return

        # Seleciona 10 questões aleatórias (ou o máximo disponível)
        questoes_teste = random.sample(questoes, min(10, len(questoes))) # Linha 363
        acertos = 0
        desempenho_areas = {}

        for i, questao in enumerate(questoes_teste, 1):
            self.mostrar_titulo(f"QUESTÃO {i}/{len(questoes_teste)}") # Ajustado total de questões

            print(f"\n{questao['enunciado']}") # Mudado de 'pergunta' para 'enunciado'
            for idx, opcao in enumerate(questao['alternativas']): # Mudado de 'opcoes' para 'alternativas'
                print(f"{idx+1}. {opcao}")

            resposta = input("\nSua resposta (1-5): ").strip() # Agora 5 opções (A-E)
            while resposta not in ['1', '2', '3', '4', '5']: # Validação para 5 opções
                print("Opção inválida. Digite 1, 2, 3, 4 ou 5.")
                resposta = input("Sua resposta (1-5): ").strip()

            # Converte a resposta do usuário para A, B, C, D, E para comparação
            resposta_convertida = chr(65 + int(resposta) - 1)

            if resposta_convertida == questao['resposta_correta']: # Mudado para 'resposta_correta'
                print("\n✅ Correto!")
                acertos += 1
                # Atualiza desempenho por área
                if questao['area'] not in desempenho_areas:
                    desempenho_areas[questao['area']] = {'acertos': 0, 'total': 0}
                desempenho_areas[questao['area']]['acertos'] += 1
            else:
                print(f"\n❌ Incorreto! A resposta correta era: {questao['resposta_correta']}")

            # Atualiza total por área
            if questao['area'] not in desempenho_areas:
                desempenho_areas[questao['area']] = {'acertos': 0, 'total': 0}
            desempenho_areas[questao['area']]['total'] += 1

            input("\nPressione Enter para próxima questão...")

        # Salva o resultado do teste diagnóstico
        email = usuario['email']
        if email not in self.desempenho:
            self.desempenho[email] = {}

        percentual = (acertos / len(questoes_teste)) * 100 # Ajustado para o número real de questões no teste

        if percentual >= 70:
            nivel = "Avançado"
        elif percentual >= 50:
            nivel = "Intermediário"
        else:
            nivel = "Básico"

        self.desempenho[email]['diagnostico_inicial'] = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pontuacao": acertos,
            "total_questoes": len(questoes_teste), # Ajustado
            "percentual": percentual,
            "nivel": nivel,
            "desempenho_areas": desempenho_areas
        }

        # Atualiza gamificação
        if 'gamificacao' not in self.desempenho[email]:
            self.desempenho[email]['gamificacao'] = {'pontos': 0, 'conquistas': []}

        # Conquista por completar teste diagnóstico
        self.adicionar_conquista(email, "diagnostico")

        self.salvar_dados()

        # Mostra resultado
        self.mostrar_resultado_diagnostico(email)

        # Cria plano de estudo inicial
        self.gerar_plano_estudo(usuario, nivel, desempenho_areas)

        input("\nPressione Enter para ver seu plano de estudos...")

    def mostrar_resultado_diagnostico(self, email):
        """Mostra o resultado do teste diagnóstico de forma detalhada"""
        resultado = self.desempenho[email]['diagnostico_inicial']

        self.mostrar_titulo("RESULTADO DO DIAGNÓSTICO")
        print(f"\n📊 Pontuação: {resultado['pontuacao']}/{resultado['total_questoes']} ({resultado['percentual']:.1f}%)")
        print(f"📈 Nível identificado: {resultado['nivel']}")

        print("\n🔍 Desempenho por área:")
        for area, dados in resultado['desempenho_areas'].items():
            if dados['total'] > 0: # Evita divisão por zero
                percentual = (dados['acertos'] / dados['total']) * 100
                print(f"\n{area}:")
                print(f"Acertos: {dados['acertos']}/{dados['total']} ({percentual:.1f}%)")
                if percentual >= 70:
                    print("Status: Ponto forte 💪")
                elif percentual >= 50:
                    print("Status: Médio desempenho 🔄")
                else:
                    print("Status: Ponto fraco 📚")
            else:
                print(f"\n{area}: Nenhuma questão respondida.")

    def gerar_plano_estudo(self, usuario, nivel, desempenho_areas):
        """Gera um plano de estudo personalizado com base no desempenho"""
        email = usuario['email']

        # Define intensidade baseada no nível
        if nivel == "Avançado":
            horas_semana = 10
            semanas = 12
        elif nivel == "Intermediário":
            horas_semana = 8
            semanas = 16
        else:  # Básico
            horas_semana = 6
            semanas = 20

        # Ordena áreas por desempenho (da menor para maior)
        areas_ordenadas = sorted(desempenho_areas.items(),
                                key=lambda x: (x[1]['acertos']/x[1]['total']) if x[1]['total'] > 0 else 0) # Evita divisão por zero

        # Cria metas semanais
        metas_semanais = []
        for semana in range(1, semanas + 1):
            meta = {
                "semana": semana,
                "topicos": [],
                "horas": horas_semana,
                "concluida": False,
                "data_inicio": (datetime.now() + timedelta(weeks=semana-1)).strftime("%Y-%m-%d")
            }

            # Distribui as áreas de interesse com foco nas mais fracas
            for i, (area, _) in enumerate(areas_ordenadas):
                if semana % len(areas_ordenadas) == i % len(areas_ordenadas):
                    meta['topicos'].append({
                        "area": area,
                        "objetivos": self.gerar_objetivos_estudo(area, nivel),
                        "recursos": self.gerar_recursos_estudo(area),
                        "prioridade": "Alta" if i < len(areas_ordenadas)/2 else "Média"
                    })

            metas_semanais.append(meta)

        # Cria o plano completo
        plano = {
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nivel_inicial": nivel,
            "duracao_semanas": semanas,
            "horas_semanais": horas_semana,
            "metas_semanais": metas_semanais,
            "progresso": 0,
            "ultima_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "desempenho_inicial": desempenho_areas
        }

        self.planos[email] = plano
        self.salvar_dados()

        print("\n✅ Seu plano de estudo personalizado foi gerado com sucesso!")
        return plano

    def gerar_objetivos_estudo(self, area, nivel):
        """Gera objetivos de estudo baseados na área e nível"""
        objetivos = []

        if nivel == "Básico":
            objetivos.extend([
                f"Compreender conceitos básicos de {area}",
                f"Resolver exercícios introdutórios de {area}",
                f"Assistir videoaulas sobre fundamentos de {area}"
            ])
        elif nivel == "Intermediário":
            objetivos.extend([
                f"Rever tópicos intermediários de {area}",
                f"Praticar exercícios de {area} com médio grau de dificuldade",
                f"Analisar questões de {area} de anos anteriores do ENEM"
            ])
        else:  # Avançado
            objetivos.extend([
                f"Aprofundar conhecimentos em tópicos complexos de {area}",
                f"Resolver questões desafiadoras de {area}",
                f"Elaborar resumos e mapas mentais sobre {area}"
            ])

        return objetivos

    def gerar_recursos_estudo(self, area):
        """Gera recursos recomendados para cada área"""
        recursos = [
            f"Livro didático de {area}",
            f"Lista de exercícios de {area} do ENEM",
            f"Playlist de videoaulas sobre {area}",
            f"Resumos e mapas mentais de {area}",
            f"Aplicativos de estudo para {area}"
        ]
        return recursos

    def adicionar_conquista(self, email, tipo_conquista, area=None):
        """Adiciona uma conquista ao usuário se ele ainda não a possui"""
        conquista = None

        # Busca a conquista pelo tipo e área (se aplicável)
        for c in self.conquistas['conquistas']:
            if c['tipo'] == tipo_conquista:
                if tipo_conquista == "area":
                    if c['area'] == area:
                        conquista = c
                        break
                else:
                    conquista = c
                    break

        if conquista and conquista['nome'] not in [c['nome'] for c in self.desempenho[email]['gamificacao']['conquistas']]:
            self.desempenho[email]['gamificacao']['pontos'] += conquista['pontos']
            self.desempenho[email]['gamificacao']['conquistas'].append({
                "nome": conquista['nome'],
                "descricao": conquista['descricao'],
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            print(f"\n🏆 Conquista desbloqueada: {conquista['nome']} (+{conquista['pontos']} pontos)")
            self.verificar_nivel(email)

    def verificar_nivel(self, email):
        """Verifica se o usuário subiu de nível"""
        pontos = self.desempenho[email]['gamificacao']['pontos']
        nivel_atual = next((u['nivel'] for u in self.usuarios if u['email'] == email), 1)

        for nivel in sorted(self.conquistas['niveis'], key=lambda x: x['nivel'], reverse=True):
            if pontos >= nivel['pontos_necessarios'] and nivel['nivel'] > nivel_atual:
                # Atualiza nível do usuário
                for usuario in self.usuarios:
                    if usuario['email'] == email:
                        usuario['nivel'] = nivel['nivel']
                        break

                print(f"\n🎉 Parabéns! Você subiu para o nível {nivel['nivel']}!")
                self.salvar_dados()
                break

    def verificar_conquistas(self):
        """Verifica se o usuário atingiu alguma conquista"""
        if not self.usuario_atual:
            return

        email = self.usuario_atual['email']

        # Verifica conquistas de frequência
        if 'ultimo_acesso' in self.desempenho.get(email, {}):
            ultimo_acesso = datetime.strptime(self.desempenho[email]['ultimo_acesso'], "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - ultimo_acesso).days == 1:
                # Usuário acessou no dia seguinte
                if 'dias_consecutivos' not in self.desempenho[email]:
                    self.desempenho[email]['dias_consecutivos'] = 1
                else:
                    self.desempenho[email]['dias_consecutivos'] += 1

                if self.desempenho[email]['dias_consecutivos'] >= 7:
                    self.adicionar_conquista(email, "frequencia")
            else:
                self.desempenho[email]['dias_consecutivos'] = 1

        self.desempenho[email]['ultimo_acesso'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.salvar_dados()

    def fazer_login(self):
        """Realiza o processo de login"""
        tentativas = 0
        max_tentativas = 3

        while tentativas < max_tentativas:
            self.mostrar_titulo("LOGIN")

            email = input("E-mail: ").strip().lower()
            senha = input("Senha: ").strip()

            usuario = next((u for u in self.usuarios if u['email'] == email and u['senha'] == senha), None)

            if usuario:
                self.usuario_atual = usuario
                print(f"\nBem-vindo(a) de volta, {usuario['nome']}!")

                # Atualiza último acesso e verifica conquistas
                self.verificar_conquistas()

                input("Pressione Enter para continuar...")
                return True

            tentativas += 1
            print(f"\nCredenciais incorretas. Tentativas restantes: {max_tentativas - tentativas}")
            input("Pressione Enter para tentar novamente...")

        print("\nNúmero máximo de tentativas excedido.")
        return False

    def menu_principal(self):
        """Menu principal após login"""
        while True:
            self.mostrar_titulo(f"OLÁ, {self.usuario_atual['nome'].split()[0].upper()}!")

            print("1. Meu Plano de Estudo")
            print("2. Realizar Simulados")
            print("3. Ver Meu Desempenho")
            print("4. Gamificação e Recompensas")
            print("5. Relatórios")
            print("6. Revisão Final ENEM")
            print("7. Sair")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.menu_plano_estudo()
            elif opcao == "2":
                self.menu_simulados()
            elif opcao == "3":
                self.menu_desempenho()
            elif opcao == "4":
                self.menu_gamificacao()
            elif opcao == "5":
                self.menu_relatorios()
            elif opcao == "6":
                self.revisao_final_enem()
            elif opcao == "7":
                self.usuario_atual = None
                print("\nVocê saiu da sua conta.")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def menu_plano_estudo(self):
        """Menu do plano de estudos"""
        email = self.usuario_atual['email']
        plano = self.planos.get(email, {})

        while True:
            self.mostrar_titulo("MEU PLANO DE ESTUDO")

            if not plano:
                print("\nVocê ainda não tem um plano de estudos.")
                print("Deseja gerar um plano agora?")
                opcao = input("(S/N): ").strip().lower()
                if opcao == 's':
                    if 'diagnostico_inicial' in self.desempenho.get(email, {}):
                        self.gerar_plano_estudo(
                            self.usuario_atual,
                            self.desempenho[email]['diagnostico_inicial']['nivel'],
                            self.desempenho[email]['diagnostico_inicial']['desempenho_areas']
                        )
                        plano = self.planos.get(email, {})
                    else:
                        print("\nVocê precisa realizar o teste diagnóstico primeiro.")
                        input("Pressione Enter para voltar...")
                        return
                else:
                    return

            semanas_concluidas = sum(1 for meta in plano['metas_semanais'] if meta.get('concluida', False))
            progresso = (semanas_concluidas / plano['duracao_semanas']) * 100

            print(f"\n📅 Plano de Estudo - {plano['nivel_inicial']}")
            print(f"⏳ Progresso: {progresso:.1f}%")
            print(f"📆 Duração: {plano['duracao_semanas']} semanas")
            print(f"⏱️ Horas semanais: {plano['horas_semanais']}h")

            print("\n1. Visualizar plano completo")
            print("2. Marcar semana como concluída")
            print("3. Atualizar plano")
            print("4. Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.visualizar_plano_completo()
            elif opcao == "2":
                self.marcar_semana_concluida()
            elif opcao == "3":
                self.atualizar_plano_estudo()
            elif opcao == "4":
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def visualizar_plano_completo(self):
        """Mostra o plano de estudo completo"""
        email = self.usuario_atual['email']
        plano = self.planos.get(email, {})

        self.mostrar_titulo("PLANO DE ESTUDO COMPLETO")

        if not plano:
            print("Plano de estudo não encontrado.")
            input("Pressione Enter para voltar...")
            return

        for semana in plano['metas_semanais']:
            print(f"\n📆 Semana {semana['semana']} - {semana['data_inicio']}")
            print(f"⏱️ Horas previstas: {semana['horas']}h")
            print(f"✅ Concluída: {'Sim' if semana.get('concluida', False) else 'Não'}")

            print("\nTópicos:")
            for topico in semana['topicos']:
                print(f"\n🔹 {topico['area']} ({topico['prioridade']})")
                print("Objetivos:")
                for objetivo in topico['objetivos']:
                    print(f"- {objetivo}")
                print("Recursos:")
                for recurso in topico['recursos']:
                    print(f"- {recurso}")

        input("\nPressione Enter para voltar...")

    def marcar_semana_concluida(self):
        """Marca uma semana do plano como concluída"""
        email = self.usuario_atual['email']
        plano = self.planos.get(email, {})

        self.mostrar_titulo("MARCAR SEMANA CONCLUÍDA")

        if not plano:
            print("Plano de estudo não encontrado.")
            input("Pressione Enter para voltar...")
            return

        # Mostra semanas não concluídas
        semanas_pendentes = [s for s in plano['metas_semanais'] if not s.get('concluida', False)]

        if not semanas_pendentes:
            print("Todas as semanas já foram concluídas!")
            input("Pressione Enter para voltar...")
            return

        print("\nSemanas pendentes:")
        for semana in semanas_pendentes:
            print(f"{semana['semana']}. Semana {semana['semana']} - {semana['data_inicio']}")

        try:
            num_semana = int(input("\nNúmero da semana a marcar como concluída: "))
            semana = next(s for s in semanas_pendentes if s['semana'] == num_semana)

            # Confirmação
            print(f"\nVocê está marcando a Semana {num_semana} como concluída.")
            confirmacao = input("Confirmar? (S/N): ").strip().lower()

            if confirmacao == 's':
                semana['concluida'] = True
                plano['progresso'] = (sum(1 for s in plano['metas_semanais'] if s.get('concluida', False)) / plano['duracao_semanas']) * 100
                plano['ultima_atualizacao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.salvar_dados()

                # Verifica conquista de semana concluída (linha otimizada)
                self.adicionar_conquista(email, "plano") # Linha 865

                print("\n✅ Semana marcada como concluída com sucesso!")
            else:
                print("\nOperação cancelada.")

        except (ValueError, StopIteration):
            print("\nNúmero de semana inválido.")

        input("Pressione Enter para voltar...")

    def visualizar_banco_questoes(self): # Renomeado de verificar_semanas_consecutivas (Linhas 878-895)
        """Exibe todas as questões disponíveis no banco de simulados."""
        self.mostrar_titulo("BANCO DE QUESTÕES") # Linha 880
        questoes_disponiveis = self.simulados.get('questoes', []) # Linha 881
        if not questoes_disponiveis: # Linha 882
            print("Nenhuma questão cadastrada no banco.") # Linha 883
            input("\nPressione Enter para continuar...") # Linha 884
            return # Linha 885

        for questao in questoes_disponiveis: # Linha 887
            print(f"\nID: {questao['id']} | Área: {questao['area']} | Nível: {questao['nivel']}") # Linha 888
            print(f"Enunciado: {questao['enunciado']}") # Linha 889
            for i, alt in enumerate(questao['alternativas']): # Linha 890
                print(f"  {chr(65+i)}. {alt}") # Linha 891
            print(f"Resposta Correta: {questao['resposta_correta']}") # Linha 892
            print("-" * 30) # Linha 893
        input("\nPressione Enter para voltar...") # Linha 894

    def atualizar_plano_estudo(self):
        """Permite atualizar o plano de estudos"""
        email = self.usuario_atual['email']
        plano = self.planos.get(email, {})

        self.mostrar_titulo("ATUALIZAR PLANO DE ESTUDO")

        if not plano:
            print("Plano de estudo não encontrado.")
            input("Pressione Enter para voltar...")
            return

        print("\nO que deseja atualizar?")
        print("1. Adicionar nova semana") # Esta opção agora informa que a função foi movida
        print("2. Alterar carga horária semanal")
        print("3. Regerar plano completo")
        print("4. Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print("\nFunção 'Adicionar nova semana' foi movida para o menu Admin.") # Linha 916
            input("Pressione Enter para continuar...") # Linha 917
        elif opcao == "2":
            self.alterar_carga_horaria()
        elif opcao == "3":
            self.regenerar_plano_completo()
        elif opcao == "4":
            return
        else:
            print("\nOpção inválida.")
            input("Pressione Enter para continuar...")

    def adicionar_questao(self): # Renomeado de adicionar_semana_plano (Linhas 930-970)
        """Adiciona uma nova questão ao banco de simulados. (Apenas com senha de administrador)"""
        self.mostrar_titulo("ADICIONAR NOVA QUESTÃO") # Linha 932
        area = input("Área (Linguagens, Matemática, Ciências da Natureza, Ciências Humanas, Redação): ").strip().title() # Linha 933
        nivel = input("Nível (Fácil, Médio, Difícil): ").strip().title() # Linha 934
        enunciado = input("Enunciado da questão: ").strip() # Linha 935
        alternativas = [] # Linha 936
        print("Digite as 5 alternativas (A, B, C, D, E):") # Linha 937
        for i in range(5): # Linha 938
            alt = input(f"Alternativa {chr(65+i)}: ").strip() # Linha 939
            alternativas.append(alt) # Linha 940
        while True: # Linha 941
            resposta_correta = input("Resposta correta (A, B, C, D ou E): ").strip().upper() # Linha 942
            if resposta_correta in ['A', 'B', 'C', 'D', 'E']: break # Linha 943
            print("Resposta inválida. Use A, B, C, D ou E.") # Linha 944

        question_id = f"Q{self.simulados['proximo_id']}" # Linha 946
        self.simulados['proximo_id'] += 1 # Linha 947
        nova_questao = {"id": question_id, "area": area, "nivel": nivel, # Linha 948
                        "enunciado": enunciado, "alternativas": alternativas, # Linha 949
                        "resposta_correta": resposta_correta} # Linha 950
        self.simulados['questoes'].append(nova_questao) # Linha 951
        self.salvar_dados() # Linha 952
        print("\nQuestão adicionada com sucesso!") # Linha 953
        input("Pressione Enter para continuar...") # Linha 954
        # Linhas vazias para manter a contagem de linhas original da função
        # Linha 955
        # Linha 956
        # Linha 957
        # Linha 958
        # Linha 959
        # Linha 960
        # Linha 961
        # Linha 962
        # Linha 963
        # Linha 964
        # Linha 965
        # Linha 966
        # Linha 967
        # Linha 968
        # Linha 969
        # Linha 970

    def alterar_carga_horaria(self):
        """Altera a carga horária semanal do plano"""
        email = self.usuario_atual['email']
        plano = self.planos.get(email, {})

        self.mostrar_titulo("ALTERAR CARGA HORÁRIA")

        if not plano:
            print("Plano de estudo não encontrado.")
            input("Pressione Enter para voltar...")
            return

        print(f"\nCarga horária atual: {plano['horas_semanais']} horas/semana")
        nova_carga = self.obter_numero("Nova carga horária semanal (1-20): ", 1, 20)

        # Atualiza todas as semanas não concluídas
        for semana in plano['metas_semanais']:
            if not semana.get('concluida', False):
                semana['horas'] = nova_carga

        plano['horas_semanais'] = nova_carga
        plano['ultima_atualizacao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.salvar_dados()

        print("\n✅ Carga horária atualizada com sucesso!")
        input("Pressione Enter para voltar...")

    def regenerar_plano_completo(self):
        """Regenera o plano de estudos com base no desempenho atual"""
        email = self.usuario_atual['email']

        self.mostrar_titulo("REGERAR PLANO DE ESTUDO")

        if 'diagnostico_inicial' not in self.desempenho.get(email, {}):
            print("Você precisa ter realizado o teste diagnóstico para gerar um plano.")
            input("Pressione Enter para voltar...")
            return

        confirmacao = input("\n⚠️ Isso substituirá seu plano atual. Continuar? (S/N): ").strip().lower()
        if confirmacao != 's':
            print("Operação cancelada.")
            input("Pressione Enter para voltar...")
            return

        self.gerar_plano_estudo(
            self.usuario_atual,
            self.desempenho[email]['diagnostico_inicial']['nivel'],
            self.desempenho[email]['diagnostico_inicial']['desempenho_areas']
        )

        print("\n✅ Plano de estudo regenerado com sucesso!")
        input("Pressione Enter para voltar...")

    def menu_simulados(self):
        """Menu de simulados"""
        while True:
            self.mostrar_titulo("SIMULADOS ENEM")

            print("1. Realizar Novo Simulado")
            print("2. Visualizar Banco de Questões") # Agora mostra todas as questões
            print("3. Simulados por Área")
            print("4. Simulado Completo (ENEM)")
            print("5. Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.selecionar_tipo_simulado()
            elif opcao == "2":
                self.visualizar_banco_questoes() # Chama a função que exibe todas as questões
            elif opcao == "3":
                self.realizar_simulado_por_area()
            elif opcao == "4":
                self.realizar_simulado_completo()
            elif opcao == "5":
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def selecionar_tipo_simulado(self):
        """Permite selecionar o tipo de simulado"""
        self.mostrar_titulo("SELECIONAR TIPO DE SIMULADO")

        print("1. Simulado por Área")
        print("2. Simulado Completo (ENEM)")
        print("3. Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            self.realizar_simulado_por_area()
        elif opcao == "2":
            self.realizar_simulado_completo()
        elif opcao == "3":
            return
        else:
            print("\nOpção inválida.")
            input("Pressione Enter para continuar...")

    def realizar_simulado_por_area(self):
        """Realiza um simulado por área específica"""
        self.mostrar_titulo("SIMULADO POR ÁREA")

        questoes_disponiveis = self.simulados.get('questoes', [])
        areas_unicas = sorted(list(set(q['area'] for q in questoes_disponiveis)))

        if not areas_unicas:
            print("Não há questões cadastradas para realizar um simulado por área.")
            input("\nPressione Enter para voltar...")
            return

        print("Áreas disponíveis:\n")
        for i, area in enumerate(areas_unicas, 1):
            print(f"{i}. {area}")

        try:
            opcao = int(input("\nSelecione a área: ").strip())
            area_selecionada = areas_unicas[opcao-1]

            questoes_da_area = [q for q in questoes_disponiveis if q['area'] == area_selecionada]

            if not questoes_da_area:
                print(f"Não há questões para a área de {area_selecionada}.")
                input("\nPressione Enter para voltar...")
                return

            num_questoes = self.obter_numero(f"Quantas questões de {area_selecionada} você deseja? (Máx: {len(questoes_da_area)}): ", 1, len(questoes_da_area))
            duracao_min = self.obter_numero(f"Duração do simulado em minutos (Mín: 1, Máx: {num_questoes*5}): ", 1, num_questoes*5) # Linha 1095 (NOVO)

            simulado_questoes = random.sample(questoes_da_area, num_questoes)

            simulado_info = {
                "titulo": f"Simulado de {area_selecionada}",
                "questoes": num_questoes,
                "duracao": duracao_min, # Usa a duração definida pelo usuário
                "dificuldade": "Variada",
                "questoes_lista": simulado_questoes
            }

            print(f"\nVocê selecionou: {simulado_info['titulo']}")
            confirmacao = input("Iniciar simulado agora? (S/N): ").strip().lower()

            if confirmacao == 's':
                self.executar_simulado(area_selecionada, simulado_info)

        except (ValueError, IndexError):
            print("\nOpção inválida.")
            input("Pressione Enter para voltar...")

    def realizar_simulado_completo(self):
        """Realiza um simulado completo no formato ENEM"""
        self.mostrar_titulo("SIMULADO COMPLETO - ENEM")

        # Cria um simulado completo com questões de todas as áreas
        simulado = {
            "titulo": "Simulado Completo ENEM",
            "questoes": 45,
            "duracao": 270,  # 4h30min como no ENEM (será sobrescrito)
            "dificuldade": "Variada",
            "questoes_lista": []
        }

        # Seleciona questões de todas as áreas (agora puxa do novo formato)
        all_available_questions = self.simulados.get('questoes', []) # Linha 690
        if not all_available_questions: # Adicionado para evitar erro se não houver questões
            print("Não há questões suficientes para gerar o simulado completo.")
            input("Pressione Enter para voltar...")
            return

        # Seleciona um número de questões para o simulado completo
        num_to_sample = min(simulado['questoes'], len(all_available_questions)) # Linha 695
        simulado['questoes_lista'] = random.sample(all_available_questions, num_to_sample) # Linha 696

        if not simulado['questoes_lista']: # Linha 698
            print("Não há questões suficientes para gerar o simulado.") # Linha 699
            input("Pressione Enter para voltar...") # Linha 700
            return # Linha 701

        duracao_min = self.obter_numero(f"Duração do simulado em minutos (Mín: 1, Máx: {num_to_sample*5}): ", 1, num_to_sample*5) # Linha 1114 (NOVO)
        simulado['duracao'] = duracao_min # Linha 1115 (NOVO)

        print("\nEste simulado contém:")
        print(f"- {len(simulado['questoes_lista'])} questões")
        print(f"- Duração: {simulado['duracao']} minutos") # Atualizado para mostrar duração definida pelo usuário
        print("\nO simulado será cronometrado como no dia do ENEM.")

        confirmacao = input("\nIniciar simulado agora? (S/N): ").strip().lower()
        if confirmacao == 's':
            self.executar_simulado("ENEM Completo", simulado)

    def executar_simulado(self, area, simulado):
        """Executa um simulado e salva os resultados com cronômetro."""
        email = self.usuario_atual['email']
        questoes = simulado['questoes_lista']
        total_questoes_simulado = len(questoes)
        acertos = 0
        desempenho_areas = defaultdict(lambda: {'acertos': 0, 'total': 0})
        respostas_usuario = {} # Inicializa o dicionário de respostas

        self.mostrar_titulo(f"SIMULADO: {simulado['titulo']}")
        print(f"Área: {area} | Duração: {simulado['duracao']} minutos\n")

        input("Pressione Enter para começar...")

        inicio = datetime.now()

        for i, questao in enumerate(questoes, 1):
            tempo_decorrido_seg = (datetime.now() - inicio).total_seconds()
            tempo_restante_seg = simulado['duracao'] * 60 - tempo_decorrido_seg

            if tempo_restante_seg <= 0:
                self.mostrar_titulo("TEMPO ESGOTADO!")
                print("\nSeu tempo para o simulado acabou.")
                break # Sai do loop do simulado

            min_restantes = int(tempo_restante_seg // 60)
            seg_restantes = int(tempo_restante_seg % 60)

            self.mostrar_titulo(f"Questão {i}/{total_questoes_simulado} | Tempo Restante: {min_restantes:02d}:{seg_restantes:02d}")

            print(f"\n{questao['enunciado']}")
            for idx, opcao in enumerate(questao['alternativas']):
                print(f"{idx+1}. {opcao}")

            while True:
                resposta = input("\nSua resposta (1-5): ").strip().upper()
                if resposta in ['1', '2', '3', '4', '5']:
                    respostas_usuario[questao['id']] = resposta
                    desempenho_areas[questao['area']]['total'] += 1
                    resposta_convertida = chr(65 + int(resposta) - 1)
                    if resposta_convertida == questao['resposta_correta']:
                        acertos += 1
                        desempenho_areas[questao['area']]['acertos'] += 1
                        print("✅ Correto!")
                    else:
                        print(f"❌ Incorreto! A resposta correta era: {questao['resposta_correta']}")
                    input("Pressione Enter para a próxima questão...")
                    break
                else:
                    print("Resposta inválida. Por favor, digite 1, 2, 3, 4 ou 5.")

        tempo_gasto = (datetime.now() - inicio).total_seconds() / 60
        total_questoes_respondidas = len(respostas_usuario) # Ajusta total de questões para as respondidas
        percentual = (acertos / total_questoes_respondidas) * 100 if total_questoes_respondidas > 0 else 0

        # Salva o resultado
        resultado = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "area": area,
            "titulo": simulado['titulo'],
            "pontuacao": acertos,
            "total_questoes": total_questoes_respondidas, # Usa o número de respondidas
            "percentual": percentual,
            "tempo_gasto": tempo_gasto,
            "desempenho_areas": dict(desempenho_areas)
        }

        if 'simulados' not in self.desempenho[email]:
            self.desempenho[email]['simulados'] = []
        self.desempenho[email]['simulados'].append(resultado)

        # Adiciona conquista de primeiro simulado
        if len(self.desempenho[email]['simulados']) == 1:
            self.adicionar_conquista(email, "simulado")

        # Verifica conquistas por área
        for area, dados in desempenho_areas.items():
            if dados['total'] > 0 and (dados['acertos'] / dados['total']) >= 0.8:
                self.adicionar_conquista(email, "area", area)

        self.salvar_dados()

        # Mostra resultado
        self.mostrar_resultado_simulado(resultado)

        input("\nPressione Enter para voltar...")

    def mostrar_resultado_simulado(self, resultado):
        """Mostra o resultado de um simulado"""
        self.mostrar_titulo("RESULTADO DO SIMULADO")

        print(f"\n📊 Pontuação: {resultado['pontuacao']}/{resultado['total_questoes']} ({resultado['percentual']:.1f}%)")
        print(f"⏱️ Tempo gasto: {resultado['tempo_gasto']:.1f} minutos")

        print("\n🔍 Desempenho por área:")
        for area, dados in resultado['desempenho_areas'].items():
            if dados['total'] > 0: # Evita divisão por zero
                percentual = (dados['acertos'] / dados['total']) * 100
                erros = dados['total'] - dados['acertos'] # Calcula erros
                print(f"\n{area}:")
                print(f"  Acertos: {dados['acertos']}/{dados['total']} ({percentual:.1f}%)")
                print(f"  Erros: {erros}/{dados['total']}") # Exibe erros
            else:
                print(f"\n{area}: Nenhuma questão respondida.")

        # Compara com desempenho anterior
        email = self.usuario_atual['email']
        if 'simulados' in self.desempenho[email] and len(self.desempenho[email]['simulados']) > 1:
            anterior = self.desempenho[email]['simulados'][-2]
            diferenca = resultado['percentual'] - anterior['percentual']

            print("\n📈 Comparação com o simulado anterior:")
            print(f"Diferença: {diferenca:+.1f}%")
            if diferenca > 5:
                print("Melhora significativa! Continue assim! 🎉")
            elif diferenca > 0:
                print("Pequena melhora. Você está no caminho certo! 👍")
            elif diferenca == 0:
                print("Desempenho estável. Tente variar seus métodos de estudo.")
            else:
                print("Queda de desempenho. Reveja os tópicos mais difíceis.")

    def ver_simulados_anteriores(self):
        """Mostra os resultados de simulados anteriores"""
        email = self.usuario_atual['email']

        if email not in self.desempenho or 'simulados' not in self.desempenho[email] or not self.desempenho[email]['simulados']:
            print("Nenhum simulado realizado ainda.")
            input("Pressione Enter para voltar...")
            return

        self.mostrar_titulo("MEUS SIMULADOS ANTERIORES") # Título mais específico

        for i, simulado in enumerate(self.desempenho[email]['simulados'], 1):
            print(f"\nSIMULADO {i} - {simulado['data']}")
            print(f"Tipo: {simulado['titulo']}")
            print(f"Resultado: {simulado['pontuacao']}/{simulado['total_questoes']} ({simulado['percentual']:.1f}%)")
            print(f"Tempo: {simulado['tempo_gasto']:.1f} minutos")
            # Exibe desempenho por área para simulados anteriores
            if 'desempenho_areas' in simulado: # Linha 1017 (NOVO)
                print("  Desempenho por Área:") # Linha 1018 (NOVO)
                for area, dados in simulado['desempenho_areas'].items(): # Linha 1019 (NOVO)
                    if dados['total'] > 0: # Linha 1020 (NOVO)
                        perc = (dados['acertos'] / dados['total']) * 100 # Linha 1021 (NOVO)
                        erros = dados['total'] - dados['acertos'] # Linha 1022 (NOVO)
                        print(f"    - {area}: Acertos {dados['acertos']}/{dados['total']} ({perc:.1f}%), Erros {erros}/{dados['total']}") # Linha 1023 (NOVO)
            print("-"*30)

        input("\nPressione Enter para voltar...")

    def menu_desempenho(self):
        """Menu de análise de desempenho"""
        email = self.usuario_atual['email']

        if 'diagnostico_inicial' not in self.desempenho.get(email, {}):
            print("\nVocê precisa realizar o teste diagnóstico primeiro.")
            input("Pressione Enter para voltar...")
            return

        while True:
            self.mostrar_titulo("MEU DESEMPENHO")

            diag = self.desempenho[email]['diagnostico_inicial']

            print(f"\n📊 Seu desempenho inicial: {diag['percentual']:.1f}%")

            if 'simulados' in self.desempenho[email] and self.desempenho[email]['simulados']:
                ultimo = self.desempenho[email]['simulados'][-1]
                print(f"📈 Último simulado: {ultimo['percentual']:.1f}%")
                print(f"📅 Data: {ultimo['data']}")
            else:
                print("\nVocê ainda não realizou simulados.")

            print("\n1. Ver evolução detalhada")
            print("2. Ver pontos fortes e fracos")
            print("3. Ver comparação com outros alunos")
            print("4. Sugestões de melhoria")
            print("5. Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.ver_evolucao_desempenho()
            elif opcao == "2":
                self.ver_pontos_fortes_fracos()
            elif opcao == "3":
                self.ver_comparacao_alunos()
            elif opcao == "4":
                self.sugestoes_melhoria()
            elif opcao == "5":
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def ver_evolucao_desempenho(self):
        """Mostra gráfico de evolução do desempenho"""
        email = self.usuario_atual['email']

        self.mostrar_titulo("EVOLUÇÃO DO DESEMPENHO")

        if 'diagnostico_inicial' not in self.desempenho.get(email, {}) or \
           'simulados' not in self.desempenho.get(email, {}) or \
           not self.desempenho[email]['simulados']:
            print("\nDados insuficientes para mostrar evolução.")
            input("Pressione Enter para voltar...")
            return

        # Simula um gráfico simples no console
        diag = self.desempenho[email]['diagnostico_inicial']
        simulados = self.desempenho[email]['simulados']

        print("\n📈 Progresso ao longo do tempo:\n")

        # Linha do tempo
        datas = [diag['data']] + [s['data'] for s in simulados]
        percentuais = [diag['percentual']] + [s['percentual'] for s in simulados]

        max_perc = max(percentuais)
        min_perc = min(percentuais)
        escala = 50  # Número de caracteres para a escala

        print("Percentual (%)")
        for i, (data, perc) in enumerate(zip(datas, percentuais)):
            # Normaliza para a escala
            pos = int((perc - min_perc) / (max_perc - min_perc) * escala) if max_perc > min_perc else escala
            print(f"{data[:10]}: {' ' * pos}◉ {perc:.1f}%")

        print("\nLegenda:")
        print("◉ Teste diagnóstico")
        print("◉ Simulados realizados")

        input("\nPressione Enter para voltar...")

    def ver_pontos_fortes_fracos(self):
        """Identifica pontos fortes e fracos do aluno"""
        email = self.usuario_atual['email']

        self.mostrar_titulo("PONTOS FORTES E FRACOS")

        if 'diagnostico_inicial' not in self.desempenho.get(email, {}):
            print("\nVocê ainda não realizou o teste diagnóstico.")
            input("Pressione Enter para voltar...")
            return

        desempenho = self.desempenho[email]['diagnostico_inicial']['desempenho_areas']

        # Se houver simulados, atualiza o desempenho com os dados mais recentes
        if 'simulados' in self.desempenho[email] and self.desempenho[email]['simulados']:
            for simulado in self.desempenho[email]['simulados']:
                if 'desempenho_areas' in simulado:
                    for area, dados in simulado['desempenho_areas'].items():
                        if area not in desempenho:
                            desempenho[area] = {'acertos': 0, 'total': 0}
                        desempenho[area]['acertos'] += dados['acertos']
                        desempenho[area]['total'] += dados['total']

        # Ordena áreas por desempenho
        areas_ordenadas = sorted(desempenho.items(),
                                key=lambda x: (x[1]['acertos']/x[1]['total']) if x[1]['total'] > 0 else 0) # Evita divisão por zero

        print("\nSeus pontos fortes:")
        for area, dados in areas_ordenadas[-3:]:  # Top 3 melhores desempenhos
            if dados['total'] > 0: # Evita divisão por zero
                percentual = (dados['acertos'] / dados['total']) * 100
                if percentual >= 70:
                    print(f"\n⭐ {area}: {percentual:.1f}% de acertos")

        print("\n\nÁreas que precisam de mais atenção:")
        for area, dados in areas_ordenadas[:3]:  # Top 3 piores desempenhos
            if dados['total'] > 0: # Evita divisão por zero
                percentual = (dados['acertos'] / dados['total']) * 100
                if percentual < 50:
                    print(f"\n⚠️ {area}: {percentual:.1f}% de acertos")

        input("\nPressione Enter para voltar...")

    def ver_comparacao_alunos(self):
        """Mostra comparação com outros alunos"""
        self.mostrar_titulo("COMPARAÇÃO COM OUTROS ALUNOS")

        if len(self.usuarios) < 2:
            print("\nNão há alunos suficientes para comparação.")
            input("Pressione Enter para voltar...")
            return

        # Coleta dados de todos os alunos
        dados_alunos = []
        for usuario in self.usuarios:
            email = usuario['email']
            if email in self.desempenho and 'diagnostico_inicial' in self.desempenho[email]:
                dados = {
                    'nome': usuario['nome'],
                    'nivel': self.desempenho[email]['diagnostico_inicial']['nivel'],
                    'percentual': self.desempenho[email]['diagnostico_inicial']['percentual']
                }

                if 'simulados' in self.desempenho[email] and self.desempenho[email]['simulados']:
                    dados['ultimo_simulado'] = self.desempenho[email]['simulados'][-1]['percentual']

                dados_alunos.append(dados)

        if len(dados_alunos) < 2:
            print("\nNão há dados suficientes para comparação.")
            input("Pressione Enter para voltar...")
            return

        # Ordena por desempenho no último simulado (se disponível)
        if 'ultimo_simulado' in dados_alunos[0]:
            dados_alunos.sort(key=lambda x: x['ultimo_simulado'], reverse=True)
            print("\n🏆 Ranking de desempenho (último simulado):\n")
            for i, aluno in enumerate(dados_alunos[:10], 1):  # Top 10
                print(f"{i}. {aluno['nome']}: {aluno['ultimo_simulado']:.1f}%")
        else:
            # Se não houver simulados, ordena pelo diagnóstico inicial
            dados_alunos.sort(key=lambda x: x['percentual'], reverse=True)
            print("\n🏆 Ranking de desempenho (teste diagnóstico):\n")
            for i, aluno in enumerate(dados_alunos[:10], 1):  # Top 10
                print(f"{i}. {aluno['nome']}: {aluno['percentual']:.1f}%")

        # Mostra posição do usuário atual
        for pos, aluno in enumerate(dados_alunos, 1):
            if aluno['nome'] == self.usuario_atual['nome']:
                print(f"\nSua posição: {pos}º")
                break

        input("\nPressione Enter para voltar...")

    def sugestoes_melhoria(self):
        """Oferece sugestões de melhoria baseadas no desempenho"""
        email = self.usuario_atual['email']

        self.mostrar_titulo("SUGESTÕES DE MELHORIA")

        if 'diagnostico_inicial' not in self.desempenho.get(email, {}):
            print("\nVocê precisa realizar o teste diagnóstico primeiro.")
            input("Pressione Enter para voltar...")
            return

        desempenho = self.desempenho[email]['diagnostico_inicial']['desempenho_areas']

        # Se houver simulados, atualiza o desempenho com os dados mais recentes
        if 'simulados' in self.desempenho[email] and self.desempenho[email]['simulados']:
            for simulado in self.desempenho[email]['simulados']:
                if 'desempenho_areas' in simulado:
                    for area, dados in simulado['desempenho_areas'].items():
                        if area not in desempenho:
                            desempenho[area] = {'acertos': 0, 'total': 0}
                        desempenho[area]['acertos'] += dados['acertos']
                        desempenho[area]['total'] += dados['total']

        # Identifica áreas com desempenho abaixo de 50%
        areas_fracas = [area for area, dados in desempenho.items()
                        if dados['total'] > 0 and (dados['acertos'] / dados['total']) < 0.5]

        if not areas_fracas:
            print("\nSeu desempenho está bom em todas as áreas! Continue assim!")
            print("Sugestão: Tente desafios mais difíceis para melhorar ainda mais.")
            input("\nPressione Enter para voltar...")
            return

        print("\nCom base no seu desempenho, sugerimos focar nas seguintes áreas:")
        for area in areas_fracas[:3]:  # Limita a 3 áreas para não sobrecarregar
            print(f"\n📚 {area}:")

            # Sugestões específicas por área
            if "Matemática" in area:
                print("- Pratique exercícios básicos diariamente")
                print("- Assista videoaulas explicativas sobre os conceitos fundamentais")
                print("- Resolva questões de provas anteriores do ENEM")
            elif "Linguagens" in area or "Redação" in area:
                print("- Leia textos variados diariamente (notícias, artigos, literatura)")
                print("- Pratique a escrita regularmente")
                print("- Estude a estrutura da redação dissertativa-argumentativa")
            elif "Ciências" in area:
                print("- Crie mapas mentais para organizar os conceitos")
                print("- Relacione os conceitos com situações do cotidiano")
                print("- Faça resumos com suas próprias palavras")
            elif "Humanas" in area:
                print("- Assista documentários sobre os temas estudados")
                print("- Relacione os eventos históricos com o contexto atual")
                print("- Crie linhas do tempo para visualizar a sequência de eventos")

        print("\n💡 Dica geral: Dedique pelo menos 1 hora por dia para revisar essas áreas!")
        input("\nPressione Enter para voltar...")

    def menu_gamificacao(self):
        """Menu de gamificação e recompensas"""
        while True:
            self.mostrar_titulo("GAMIFICAÇÃO")

            email = self.usuario_atual['email']
            pontos = self.desempenho.get(email, {}).get('gamificacao', {}).get('pontos', 0)
            nivel = next((u['nivel'] for u in self.usuarios if u['email'] == email), 1)

            print(f"🏅 Seus pontos: {pontos}")
            print(f"🌟 Seu nível: {nivel}")

            # Progresso para próximo nível
            niveis = sorted(self.conquistas['niveis'], key=lambda x: x['nivel'])
            if nivel < len(niveis):
                pontos_prox_nivel = niveis[nivel]['pontos_necessarios']
                print(f"\n⬜{'⬛' * int((pontos/pontos_prox_nivel)*10)}{'⬜' * (10 - int((pontos/pontos_prox_nivel)*10))}")
                print(f"Faltam {max(0, pontos_prox_nivel - pontos)} pontos para o próximo nível")

            print("\n1. Minhas Conquistas")
            print("2. Ranking")
            print("3. Recompensas")
            print("4. Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.mostrar_conquistas()
            elif opcao == "2":
                self.mostrar_ranking()
            elif opcao == "3":
                self.mostrar_recompensas()
            elif opcao == "4":
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def mostrar_conquistas(self):
        """Mostra as conquistas do usuário"""
        email = self.usuario_atual['email']
        conquistas_usuario = self.desempenho.get(email, {}).get('gamificacao', {}).get('conquistas', [])

        self.mostrar_titulo("MINHAS CONQUISTAS")

        if not conquistas_usuario: print("Você ainda não desbloqueou conquistas. Continue estudando!"); input("\nPressione Enter para voltar..."); return # Linha 1060 (Condensada)

        for i, conquista in enumerate(conquistas_usuario, 1):
            print(f"\n{i}. {conquista['nome']}")
            print(f"   {conquista['descricao']}")
            print(f"   Desbloqueada em: {conquista['data']}")

        # Mostra conquistas não desbloqueadas
        print("\n\nConquistas disponíveis:")
        for conquista in self.conquistas['conquistas']:
            if conquista['nome'] not in [c['nome'] for c in conquistas_usuario]:
                print(f"\n🔒 {conquista['nome']}")
                print(f"   {conquista['descricao']}")

        input("\nPressione Enter para voltar...")

    def mostrar_ranking(self):
        """Mostra o ranking de usuários"""
        self.mostrar_titulo("RANKING DE USUÁRIOS")

        # Cria lista de usuários com pontos
        ranking = []
        for usuario in self.usuarios:
            email = usuario['email']
            pontos = self.desempenho.get(email, {}).get('gamificacao', {}).get('pontos', 0)
            ranking.append({
                "nome": usuario['nome'],
                "pontos": pontos,
                "nivel": usuario['nivel']
            })

        # Ordena por pontos (decrescente)
        ranking.sort(key=lambda x: x['pontos'], reverse=True)

        print("\n🏆 TOP 10:\n")
        for i, usuario in enumerate(ranking[:10], 1):
            print(f"{i}. {usuario['nome']} - {usuario['pontos']} pontos (Nível {usuario['nivel']})")

        # Mostra posição do usuário atual
        email_atual = self.usuario_atual['email']
        for pos, usuario in enumerate(ranking, 1):
            if usuario['nome'] == self.usuario_atual['nome']:
                print(f"\nSua posição: {pos}º")
                break

        input("\nPressione Enter para voltar...")

    def mostrar_recompensas(self):
        """Mostra as recompensas disponíveis"""
        self.mostrar_titulo("RECOMPENSAS")

        email = self.usuario_atual['email']
        pontos = self.desempenho.get(email, {}).get('gamificacao', {}).get('pontos', 0)

        print("\n🎁 Recompensas disponíveis:\n")
        print("1. Simulado Premium - 100 pontos")
        print("2. Material Exclusivo - 200 pontos")
        print("3. Aula com Tutor - 500 pontos")
        print("4. Certificado de Excelência - 1000 pontos")

        opcao = input("\nEscolha uma recompensa para resgatar (ou 0 para voltar): ").strip()

        if opcao == "1":
            self.resgatar_recompensa(email, 100, "Simulado Premium")
        elif opcao == "2":
            self.resgatar_recompensa(email, 200, "Material Exclusivo")
        elif opcao == "3":
            self.resgatar_recompensa(email, 500, "Aula com Tutor")
        elif opcao == "4":
            self.resgatar_recompensa(email, 1000, "Certificado de Excelência")
        elif opcao == "0":
            return
        else:
            print("\nOpção inválida.")
            input("Pressione Enter para continuar...")

    def resgatar_recompensa(self, email, custo, recompensa):
        """Resgata uma recompensa se o usuário tiver pontos suficientes"""
        pontos = self.desempenho[email]['gamificacao']['pontos']

        if pontos >= custo:
            self.desempenho[email]['gamificacao']['pontos'] -= custo
            print(f"\n✅ Recompensa resgatada: {recompensa}!")

            # Adiciona aos itens resgatados
            if 'recompensas' not in self.desempenho[email]['gamificacao']:
                self.desempenho[email]['gamificacao']['recompensas'] = []

            self.desempenho[email]['gamificacao']['recompensas'].append({
                "nome": recompensa,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            self.salvar_dados()
        else:
            print("\n⚠️ Pontos insuficientes para resgatar esta recompensa.")

        input("Pressione Enter para continuar...")

    def menu_relatorios(self):
        """Menu de relatórios para pais e professores"""
        while True:
            self.mostrar_titulo("RELATÓRIOS")

            print("1. Relatório para Pais")
            print("2. Relatório para Professores")
            print("3. Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.gerar_relatorio_pais()
            elif opcao == "2":
                self.gerar_relatorio_professores()
            elif opcao == "3":
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def gerar_relatorio_pais(self):
        """Gera um relatório simplificado para pais"""
        email = self.usuario_atual['email']
        usuario = next(u for u in self.usuarios if u['email'] == email)
        plano = self.planos.get(email, {})
        desempenho = self.desempenho.get(email, {})

        self.mostrar_titulo("RELATÓRIO PARA PAIS")

        print(f"\n📝 Relatório de {usuario['nome']}")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}")

        print("\n📊 DESEMPENHO GERAL:")
        if 'diagnostico_inicial' in desempenho and 'simulados' in desempenho:
            # Progresso desde o diagnóstico
            perc_inicial = desempenho['diagnostico_inicial']['percentual']
            ultimo_simulado = desempenho['simulados'][-1]['percentual'] if desempenho['simulados'] else 0
            print(f"Evolução: {perc_inicial:.1f}% → {ultimo_simulado:.1f}%")

            if ultimo_simulado > perc_inicial + 5:
                print("Tendência: Melhora significativa 📈")
            elif ultimo_simulado > perc_inicial:
                print("Tendência: Pequena melhora ↗️")
            elif ultimo_simulado == perc_inicial:
                print("Tendência: Estabilidade ↔️")
            else:
                print("Tendência: Queda de desempenho 📉")
        else:
            print("Dados de desempenho ainda não disponíveis.")

        print("\n📚 PLANO DE ESTUDO:")
        if plano:
            semanas_concluidas = sum(1 for meta in plano['metas_semanais'] if meta.get('concluida', False))
            print(f"Progresso: {semanas_concluidas}/{plano['duracao_semanas']} semanas concluídas")
            print(f"Horas semanais recomendadas: {plano['horas_semanais']}h")
        else:
            print("Plano de estudo ainda não gerado.")

        print("\n🏅 CONQUISTAS:")
        if 'gamificacao' in desempenho and 'conquistas' in desempenho['gamificacao']:
            print(f"Total: {len(desempenho['gamificacao']['conquistas'])} conquistas")
            print(f"Última conquista: {desempenho['gamificacao']['conquistas'][-1]['nome']}"
                  if desempenho['gamificacao']['conquistas'] else "Nenhuma conquista ainda")
        else:
            print("Nenhuma conquista registrada.")

        print("\n📌 RECOMENDAÇÕES:")
        if plano and 'diagnostico_inicial' in desempenho:
            areas_fracas = [area for area, dados in desempenho['diagnostico_inicial']['desempenho_areas'].items()
                           if dados['total'] > 0 and (dados['acertos']/dados['total']) < 0.5] # Evita divisão por zero
            if areas_fracas:
                print("Áreas que precisam de mais atenção:")
                for area in areas_fracas[:3]:
                    print(f"- {area}")
            else:
                print("Continue mantendo o bom desempenho em todas as áreas!")

        input("\nPressione Enter para voltar...")

    def gerar_relatorio_professores(self):
        """Gera um relatório detalhado para professores"""
        email = self.usuario_atual['email']
        usuario = next(u for u in self.usuarios if u['email'] == email)
        desempenho = self.desempenho.get(email, {})

        self.mostrar_titulo("RELATÓRIO PARA PROFESSORES")

        print(f"\n👨‍🎓 Aluno: {usuario['nome']}")
        print(f"🏫 Escola: {usuario['escola']}")
        print(f"📅 Série: {usuario['serie']}")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}")

        print("\n📊 DESEMPENHO DETALHADO:")
        if 'diagnostico_inicial' in desempenho:
            print("\n🔍 Teste Diagnóstico Inicial:")
            diag = desempenho['diagnostico_inicial']
            print(f"Pontuação: {diag['pontuacao']}/{diag['total_questoes']}")
            print(f"Percentual: {diag['percentual']:.1f}%")
            print(f"Nível: {diag['nivel']}")

            print("\nÁreas de conhecimento:")
            for area, dados in diag['desempenho_areas'].items():
                if dados['total'] > 0: # Evita divisão por zero
                    perc = (dados['acertos'] / dados['total']) * 100
                    print(f"\n{area}:")
                    print(f"Acertos: {dados['acertos']}/{dados['total']} ({perc:.1f}%)")
                    if perc >= 70:
                        print("Status: Ponto forte")
                    elif perc >= 50:
                        print("Status: Médio desempenho")
                    else:
                        print("Status: Ponto fraco")
                else:
                    print(f"\n{area}: Nenhuma questão respondida.")

        if 'simulados' in desempenho and desempenho['simulados']:
            print("\n📝 Histórico de Simulados:")
            for i, simulado in enumerate(desempenho['simulados'], 1):
                print(f"\nSimulado {i}:")
                print(f"Data: {simulado['data']}")
                print(f"Área: {simulado['area']}")
                print(f"Pontuação: {simulado['pontuacao']}/{simulado['total_questoes']}")
                print(f"Percentual: {simulado['percentual']:.1f}%")

        print("\n📌 ANÁLISE PEDAGÓGICA:")
        if 'diagnostico_inicial' in desempenho and 'simulados' in desempenho:
            # Sugere estratégias de ensino baseadas no desempenho
            areas_fracas = [area for area, dados in desempenho['diagnostico_inicial']['desempenho_areas'].items()
                          if dados['total'] > 0 and (dados['acertos']/dados['total']) < 0.5] # Evita divisão por zero

            if areas_fracas:
                print("\nÁreas que necessitam de reforço:")
                for area in areas_fracas:
                    print(f"- {area}")

                print("\nSugestões de abordagem:")
                print("- Priorizar exercícios práticos nas áreas de dificuldade")
                print("- Utilizar materiais visuais e exemplos concretos")
                print("- Dividir conceitos complexos em partes menores")
            else:
                print("\nO aluno demonstra bom desempenho em todas as áreas.")
                print("Sugestões:")
                print("- Propor desafios mais complexos")
                print("- Estimular o aprofundamento em tópicos de interesse")

        input("\nPressione Enter para voltar...")

    def revisao_final_enem(self):
        """Prepara revisão final para o ENEM"""
        email = self.usuario_atual['email']

        self.mostrar_titulo("REVISÃO FINAL PARA O ENEM")

        if 'diagnostico_inicial' not in self.desempenho.get(email, {}):
            print("\nVocê precisa realizar o teste diagnóstico primeiro.")
            input("Pressione Enter para voltar...")
            return

        # Verifica se o aluno já tem um plano de estudos
        if email not in self.planos:
            print("\nVocê ainda não tem um plano de estudos.")
            input("Pressione Enter para voltar...")
            return

        print("\nEste módulo prepara uma revisão intensiva para o ENEM com base no seu desempenho.")
        print("Vamos criar um plano de revisão personalizado para os últimos 30 dias antes da prova.")

        # Pega as áreas com menor desempenho
        desempenho = self.desempenho[email]['diagnostico_inicial']['desempenho_areas']

        # Se houver simulados, atualiza o desempenho com os dados mais recentes
        if 'simulados' in self.desempenho[email] and self.desempenho[email]['simulados']:
            for simulado in self.desempenho[email]['simulados']:
                if 'desempenho_areas' in simulado:
                    for area, dados in simulado['desempenho_areas'].items():
                        if area not in desempenho:
                            desempenho[area] = {'acertos': 0, 'total': 0}
                        desempenho[area]['acertos'] += dados['acertos']
                        desempenho[area]['total'] += dados['total']

        # Ordena áreas por desempenho (da menor para maior)
        areas_ordenadas = sorted(desempenho.items(),
                                key=lambda x: (x[1]['acertos']/x[1]['total']) if x[1]['total'] > 0 else 0) # Evita divisão por zero

        print("\n📌 Com base no seu desempenho, sugerimos o seguinte cronograma:")

        # Cria um plano de revisão de 30 dias
        dias_revisao = 30
        horas_diarias = 2

        print("\n📅 Cronograma de Revisão (últimos 30 dias antes do ENEM):")
        for dia in range(1, dias_revisao + 1):
            # Prioriza as áreas mais fracas nos primeiros dias
            if dia <= len(areas_ordenadas):
                area = areas_ordenadas[dia-1][0]
            else:
                # Depois revisa todas as áreas ciclicamente
                area = areas_ordenadas[(dia-1) % len(areas_ordenadas)][0]

            print(f"\nDia {dia}: Revisão de {area}")
            print(f"- {horas_diarias} horas de estudo")
            print("- Resolução de questões do ENEM")
            print("- Revisão de resumos e mapas mentais")

        print("\n📝 Sugestões para a semana da prova:")
        print("- Reduza a carga de estudo nos últimos 2 dias")
        print("- Revise apenas fórmulas e conceitos essenciais")
        print("- Descanse bem na véspera da prova")
        print("- Prepare todos os materiais necessários com antecedência")

        input("\nPressione Enter para voltar...")

    def excluir_questao(self): # Nova função para excluir questões (Linhas 1121-1140)
        """Exclui uma questão do banco de simulados pelo ID."""
        self.mostrar_titulo("EXCLUIR QUESTÃO") # Linha 1123
        questoes_disponiveis = self.simulados.get('questoes', []) # Linha 1124
        if not questoes_disponiveis: print("Nenhuma questão cadastrada para excluir."); input("\nPressione Enter para continuar..."); return # Linha 1125 (Condensada)


        self.visualizar_banco_questoes() # Mostra as questões para facilitar a escolha do ID
        questao_id = input("\nDigite o ID da questão a ser excluída: ").strip() # Linha 1131

        questao_encontrada = False # Linha 1133
        for i, q in enumerate(questoes_disponiveis): # Linha 1134
            if q['id'] == questao_id: # Linha 1135
                confirmacao = input(f"Tem certeza que deseja excluir a questão '{q['enunciado']}'? (S/N): ").strip().lower() # Linha 1136
                if confirmacao == 's': # Linha 1137
                    del self.simulados['questoes'][i] # Linha 1138
                    self.salvar_dados() # Linha 1139
                    print("Questão excluída com sucesso!") # Linha 1140
                else: print("Exclusão cancelada.") # Linha 1141
                questao_encontrada = True; break # Linha 1142
        if not questao_encontrada: print("ID da questão não encontrado."); input("\nPressione Enter para continuar...") # Linha 1144 (Condensada)
        # Linha 1145 (Removida)

    def editar_questao(self): # Nova função para editar questões (Linhas 1146-1200)
        """Edita uma questão existente no banco de simulados pelo ID."""
        self.mostrar_titulo("EDITAR QUESTÃO") # Linha 1148
        questoes_disponiveis = self.simulados.get('questoes', []) # Linha 1149
        if not questoes_disponiveis: print("Nenhuma questão cadastrada para editar."); input("\nPressione Enter para continuar..."); return # Linha 1150 (Condensada)


        self.visualizar_banco_questoes() # Mostra as questões para facilitar a escolha do ID
        questao_id = input("\nDigite o ID da questão a ser editada: ").strip() # Linha 1156

        questao_encontrada = None # Linha 1158
        for q in questoes_disponiveis: # Linha 1159
            if q['id'] == questao_id: questao_encontrada = q; break # Linha 1160

        if questao_encontrada: # Linha 1162
            print("\n--- Editando Questão ---"); print(f"ID: {questao_encontrada['id']}") # Linha 1163 (Condensada)
            # Linha 1164 (Removida)

            # Edita área
            nova_area = input(f"Nova Área (atual: {questao_encontrada['area']}): ").strip().title() # Linha 1166
            if nova_area: questao_encontrada['area'] = nova_area # Linha 1167

            # Edita nível
            novo_nivel = input(f"Novo Nível (atual: {questao_encontrada['nivel']}): ").strip().title() # Linha 1169
            if novo_nivel: questao_encontrada['nivel'] = novo_nivel # Linha 1170

            # Edita enunciado
            novo_enunciado = input(f"Novo Enunciado (atual: {questao_encontrada['enunciado']}): ").strip() # Linha 1172
            if novo_enunciado: questao_encontrada['enunciado'] = novo_enunciado # Linha 1173

            # Edita alternativas
            print("\nEdite as alternativas (deixe em branco para manter a atual):") # Linha 1175
            novas_alternativas = [] # Linha 1176
            for i, alt in enumerate(questao_encontrada['alternativas']): # Linha 1177
                nova_alt = input(f"Alternativa {chr(65+i)} (atual: {alt}): ").strip() # Linha 1178
                novas_alternativas.append(nova_alt if nova_alt else alt) # Linha 1179
            questao_encontrada['alternativas'] = novas_alternativas # Linha 1180

            # Edita resposta correta
            while True: # Linha 1182
                nova_resposta = input(f"Nova Resposta Correta (atual: {questao_encontrada['resposta_correta']}): ").strip().upper() # Linha 1183
                if not nova_resposta: break # Se vazio, mantém a atual
                if nova_resposta in ['A', 'B', 'C', 'D', 'E']: # Linha 1185
                    questao_encontrada['resposta_correta'] = nova_resposta; break # Linha 1186
                print("Resposta inválida. Use A, B, C, D ou E.") # Linha 1187

            self.salvar_dados() # Linha 1189
            print("\nQuestão editada com sucesso!") # Linha 1190
        else: print("ID da questão não encontrado."); input("\nPressione Enter para continuar...") # Linha 1191 (Condensada)
        # Linha 1192 (Removida)
        # Linha 1193 (Removida)

    def iniciar(self):
        """Inicia o sistema"""
        self.tela_inicial()

# Ponto de entrada do programa
if __name__ == "__main__":
    sistema = SistemaEstudoENEM()
    sistema.iniciar()
