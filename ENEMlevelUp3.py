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
        self.simulados = {}
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
                with open(self.ARQUIVO_USUARIOS, 'r') as f:
                    self.usuarios = json.load(f)
            
            if os.path.exists(self.ARQUIVO_PLANOS):
                with open(self.ARQUIVO_PLANOS, 'r') as f:
                    self.planos = json.load(f)
            
            if os.path.exists(self.ARQUIVO_DESEMPENHO):
                with open(self.ARQUIVO_DESEMPENHO, 'r') as f:
                    self.desempenho = json.load(f)
            
            if os.path.exists(self.ARQUIVO_CONQUISTAS):
                with open(self.ARQUIVO_CONQUISTAS, 'r') as f:
                    self.conquistas = json.load(f)
                    
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar dados: {e}")
            self.usuarios = []
            self.planos = {}
            self.desempenho = {}
            self.conquistas = {}

    def salvar_dados(self):
        """Salva todos os dados nos arquivos JSON"""
        try:
            with open(self.ARQUIVO_USUARIOS, 'w') as f:
                json.dump(self.usuarios, f, indent=4)
            
            with open(self.ARQUIVO_PLANOS, 'w') as f:
                json.dump(self.planos, f, indent=4)
                
            with open(self.ARQUIVO_DESEMPENHO, 'w') as f:
                json.dump(self.desempenho, f, indent=4)
                
            with open(self.ARQUIVO_CONQUISTAS, 'w') as f:
                json.dump(self.conquistas, f, indent=4)
                
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")

    def inicializar_simulados(self):
        """Inicializa o banco de simulados se não existir"""
        if os.path.exists(self.ARQUIVO_SIMULADOS):
            with open(self.ARQUIVO_SIMULADOS, 'r') as f:
                self.simulados = json.load(f)
        else:
            # Banco de simulados mais completo com todas as áreas do ENEM
            self.simulados = {
                "Matemática e suas Tecnologias": [
                    {
                        "titulo": "Matemática Básica",
                        "questoes": 10,
                        "duracao": 30,
                        "dificuldade": "Fácil",
                        "questoes_lista": [
                            {"pergunta": "Quanto é 2 + 2?", "opcoes": ["3", "4", "5", "6"], "resposta": 1, "area": "Aritmética"},
                            {"pergunta": "Qual o valor de π (pi) aproximadamente?", "opcoes": ["3.14", "2.71", "1.41", "1.61"], "resposta": 0, "area": "Geometria"}
                        ]
                    },
                    {
                        "titulo": "Álgebra e Funções",
                        "questoes": 15,
                        "duracao": 45,
                        "dificuldade": "Médio",
                        "questoes_lista": [
                            {"pergunta": "Qual é a raiz da equação 2x + 5 = 15?", "opcoes": ["5", "10", "7.5", "20"], "resposta": 0, "area": "Álgebra"},
                            {"pergunta": "Qual é o vértice da parábola y = x² - 4x + 3?", "opcoes": ["(2, -1)", "(1, 0)", "(0, 3)", "(-1, 8)"], "resposta": 0, "area": "Funções"}
                        ]
                    }
                ],
                "Linguagens, Códigos e suas Tecnologias": [
                    {
                        "titulo": "Gramática Básica",
                        "questoes": 10,
                        "duracao": 30,
                        "dificuldade": "Fácil",
                        "questoes_lista": [
                            {"pergunta": "Qual alternativa contém um verbo no pretérito perfeito?", "opcoes": ["Eu estudo", "Eu estudava", "Eu estudei", "Eu estudarei"], "resposta": 2, "area": "Gramática"},
                            {"pergunta": "Qual a função da vírgula na frase: 'Ana, venha aqui!'?", "opcoes": ["Separar itens", "Indicar vocativo", "Separar orações", "Indicar elipse"], "resposta": 1, "area": "Pontuação"}
                        ]
                    },
                    {
                        "titulo": "Interpretação de Texto",
                        "questoes": 15,
                        "duracao": 45,
                        "dificuldade": "Médio",
                        "questoes_lista": []
                    }
                ],
                "Ciências da Natureza e suas Tecnologias": [
                    {
                        "titulo": "Biologia Celular",
                        "questoes": 10,
                        "duracao": 30,
                        "dificuldade": "Médio",
                        "questoes_lista": [
                            {"pergunta": "Qual organela é responsável pela produção de energia na célula?", "opcoes": ["Núcleo", "Mitocôndria", "Ribossomo", "Lisossomo"], "resposta": 1, "area": "Biologia Celular"}
                        ]
                    },
                    {
                        "titulo": "Química Básica",
                        "questoes": 15,
                        "duracao": 45,
                        "dificuldade": "Médio",
                        "questoes_lista": []
                    }
                ],
                "Ciências Humanas e suas Tecnologias": [
                    {
                        "titulo": "História do Brasil",
                        "questoes": 10,
                        "duracao": 30,
                        "dificuldade": "Médio",
                        "questoes_lista": [
                            {"pergunta": "Em que ano o Brasil foi descoberto?", "opcoes": ["1492", "1500", "1502", "1498"], "resposta": 1, "area": "História"}
                        ]
                    },
                    {
                        "titulo": "Geografia Humana",
                        "questoes": 15,
                        "duracao": 45,
                        "dificuldade": "Médio",
                        "questoes_lista": []
                    }
                ],
                "Redação": [
                    {
                        "titulo": "Estrutura da Redação",
                        "questoes": 5,
                        "duracao": 15,
                        "dificuldade": "Fácil",
                        "questoes_lista": [
                            {"pergunta": "Quantos parágrafos deve ter uma redação do ENEM?", "opcoes": ["3", "4", "5", "Não há regra"], "resposta": 1, "area": "Estrutura"},
                            {"pergunta": "Qual é a estrutura básica de uma redação dissertativa-argumentativa?", "opcoes": ["Introdução, Desenvolvimento e Conclusão", "Tese, Argumentos e Proposta", "Ambas as anteriores", "Nenhuma das anteriores"], "resposta": 2, "area": "Estrutura"}
                        ]
                    }
                ]
            }
            with open(self.ARQUIVO_SIMULADOS, 'w') as f:
                json.dump(self.simulados, f, indent=4)

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
                    {"nome": "Mestre em Matemática", "descricao": "Acertou 80% em um simulado de Matemática", "pontos": 60, "tipo": "area", "area": "Matemática"},
                    {"nome": "Redator Nota 1000", "descricao": "Acertou 90% em um simulado de Redação", "pontos": 70, "tipo": "area", "area": "Redação"}
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
            print("3. Sobre o sistema")
            print("4. Sair")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                if self.fazer_login():
                    self.menu_principal()
            elif opcao == "2":
                self.cadastrar_usuario()
            elif opcao == "3":
                self.mostrar_sobre()
            elif opcao == "4":
                print("\nObrigado por usar nosso sistema! Boa sorte no ENEM!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def mostrar_sobre(self):
        """Mostra informações sobre o sistema"""
        self.mostrar_titulo("SOBRE O SISTEMA")
        
        print("""
Sistema de Estudos para o ENEM - Versão 1.0

Este sistema foi desenvolvido para ajudar estudantes a se prepararem 
para o Exame Nacional do Ensino Médio (ENEM) de forma personalizada.

Principais funcionalidades:
- Teste diagnóstico inicial
- Plano de estudos adaptativo
- Simulados cronometrados
- Acompanhamento de desempenho
- Sistema de gamificação
- Relatórios para pais e professores

Desenvolvido com Python 3
© 2023 Todos os direitos reservados
        """)
        
        input("\nPressione Enter para voltar...")

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
        
        # Seleciona questões de diferentes áreas
        questoes = []
        for area in self.simulados.values():
            for simulado in area:
                questoes.extend(simulado['questoes_lista'])
        
        # Seleciona 10 questões aleatórias
        questoes_teste = random.sample(questoes, min(10, len(questoes)))
        acertos = 0
        desempenho_areas = {}
        
        for i, questao in enumerate(questoes_teste, 1):
            self.mostrar_titulo(f"QUESTÃO {i}/10")
            
            print(f"\n{questao['pergunta']}")
            for idx, opcao in enumerate(questao['opcoes']):
                print(f"{idx+1}. {opcao}")
            
            resposta = input("\nSua resposta (1-4): ").strip()
            while resposta not in ['1', '2', '3', '4']:
                print("Opção inválida. Digite 1, 2, 3 ou 4.")
                resposta = input("Sua resposta (1-4): ").strip()
            
            if int(resposta)-1 == questao['resposta']:
                print("\n✅ Correto!")
                acertos += 1
                # Atualiza desempenho por área
                if questao['area'] not in desempenho_areas:
                    desempenho_areas[questao['area']] = {'acertos': 0, 'total': 0}
                desempenho_areas[questao['area']]['acertos'] += 1
            else:
                print(f"\n❌ Incorreto! A resposta correta era: {questao['opcoes'][questao['resposta']]}")
            
            # Atualiza total por área
            if questao['area'] not in desempenho_areas:
                desempenho_areas[questao['area']] = {'acertos': 0, 'total': 0}
            desempenho_areas[questao['area']]['total'] += 1
            
            input("\nPressione Enter para próxima questão...")
        
        # Salva o resultado do teste diagnóstico
        email = usuario['email']
        if email not in self.desempenho:
            self.desempenho[email] = {}
        
        percentual = (acertos / 10) * 100
        
        if percentual >= 70:
            nivel = "Avançado"
        elif percentual >= 50:
            nivel = "Intermediário"
        else:
            nivel = "Básico"
        
        self.desempenho[email]['diagnostico_inicial'] = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pontuacao": acertos,
            "total_questoes": 10,
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
            percentual = (dados['acertos'] / dados['total']) * 100
            print(f"\n{area}:")
            print(f"Acertos: {dados['acertos']}/{dados['total']} ({percentual:.1f}%)")
            if percentual >= 70:
                print("Status: Ponto forte 💪")
            elif percentual >= 50:
                print("Status: Médio desempenho 🔄")
            else:
                print("Status: Ponto fraco 📚")

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
                                key=lambda x: (x[1]['acertos']/x[1]['total']))
        
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
                
                # Verifica conquista de semana concluída
                semanas_consecutivas = self.verificar_semanas_consecutivas(email)
                if semanas_consecutivas >= 1:
                    self.adicionar_conquista(email, "plano")
                
                print("\n✅ Semana marcada como concluída com sucesso!")
            else:
                print("\nOperação cancelada.")
        
        except (ValueError, StopIteration):
            print("\nNúmero de semana inválido.")
        
        input("Pressione Enter para voltar...")

    def verificar_semanas_consecutivas(self, email):
        """Verifica quantas semanas consecutivas foram concluídas"""
        plano = self.planos.get(email, {})
        if not plano:
            return 0
        
        semanas_concluidas = sorted([s['semana'] for s in plano['metas_semanais'] if s.get('concluida', False)])
        
        if not semanas_concluidas:
            return 0
        
        consecutivas = 1
        for i in range(1, len(semanas_concluidas)):
            if semanas_concluidas[i] == semanas_concluidas[i-1] + 1:
                consecutivas += 1
            else:
                break
        
        return consecutivas

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
        print("1. Adicionar nova semana")
        print("2. Alterar carga horária semanal")
        print("3. Regerar plano completo")
        print("4. Voltar")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            self.adicionar_semana_plano()
        elif opcao == "2":
            self.alterar_carga_horaria()
        elif opcao == "3":
            self.regenerar_plano_completo()
        elif opcao == "4":
            return
        else:
            print("\nOpção inválida.")
            input("Pressione Enter para continuar...")

    def adicionar_semana_plano(self):
        """Adiciona uma nova semana ao plano de estudos"""
        email = self.usuario_atual['email']
        plano = self.planos.get(email, {})
        
        self.mostrar_titulo("ADICIONAR SEMANA AO PLANO")
        
        if not plano:
            print("Plano de estudo não encontrado.")
            input("Pressione Enter para voltar...")
            return
        
        nova_semana = {
            "semana": len(plano['metas_semanais']) + 1,
            "topicos": [],
            "horas": plano['horas_semanais'],
            "concluida": False,
            "data_inicio": (datetime.now() + timedelta(weeks=len(plano['metas_semanais']))).strftime("%Y-%m-%d")
        }
        
        # Seleciona áreas com base no desempenho atual
        if 'diagnostico_inicial' in self.desempenho.get(email, {}):
            desempenho = self.desempenho[email]['diagnostico_inicial']['desempenho_areas']
            areas_ordenadas = sorted(desempenho.items(), key=lambda x: (x[1]['acertos']/x[1]['total']))
            
            for i, (area, _) in enumerate(areas_ordenadas):
                if nova_semana['semana'] % len(areas_ordenadas) == i % len(areas_ordenadas):
                    nova_semana['topicos'].append({
                        "area": area,
                        "objetivos": self.gerar_objetivos_estudo(area, plano['nivel_inicial']),
                        "recursos": self.gerar_recursos_estudo(area),
                        "prioridade": "Alta" if i < len(areas_ordenadas)/2 else "Média"
                    })
        
        plano['metas_semanais'].append(nova_semana)
        plano['duracao_semanas'] += 1
        plano['ultima_atualizacao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.salvar_dados()
        
        print("\n✅ Nova semana adicionada ao plano com sucesso!")
        input("Pressione Enter para voltar...")

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
            print("2. Meus Simulados Anteriores")
            print("3. Simulados por Área")
            print("4. Simulado Completo (ENEM)")
            print("5. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.selecionar_tipo_simulado()
            elif opcao == "2":
                self.ver_simulados_anteriores()
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
        
        print("Áreas disponíveis:\n")
        for i, area in enumerate(self.simulados.keys(), 1):
            print(f"{i}. {area}")
        
        try:
            opcao = int(input("\nSelecione a área: ").strip())
            area = list(self.simulados.keys())[opcao-1]
            
            print(f"\nSimulados disponíveis para {area}:")
            for i, simulado in enumerate(self.simulados[area], 1):
                print(f"\n{i}. {simulado['titulo']}")
                print(f"   Questões: {simulado['questoes']}")
                print(f"   Duração: {simulado['duracao']} minutos")
                print(f"   Dificuldade: {simulado['dificuldade']}")
            
            opcao_simulado = int(input("\nSelecione o simulado: ").strip())
            simulado = self.simulados[area][opcao_simulado-1]
            
            print(f"\nVocê selecionou: {simulado['titulo']}")
            confirmacao = input("Iniciar simulado agora? (S/N): ").strip().lower()
            
            if confirmacao == 's':
                self.executar_simulado(area, simulado)
        
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
            "duracao": 270,  # 4h30min como no ENEM
            "dificuldade": "Variada",
            "questoes_lista": []
        }
        
        # Seleciona questões de todas as áreas
        for area in self.simulados.values():
            for simulado_area in area:
                if simulado_area['questoes_lista']:
                    simulado['questoes_lista'].extend(random.sample)
                    simulado_area['questoes_lista'], 
                    min(5, len(simulado_area['questoes_lista']))
        
        if not simulado['questoes_lista']:
            print("Não há questões suficientes para gerar o simulado.")
            input("Pressione Enter para voltar...")
            return
        
        print("\nEste simulado contém:")
        print(f"- {len(simulado['questoes_lista'])} questões")
        print(f"- Duração: {simulado['duracao']} minutos (4h30min)")
        print("\nO simulado será cronometrado como no dia do ENEM.")
        
        confirmacao = input("\nIniciar simulado agora? (S/N): ").strip().lower()
        if confirmacao == 's':
            self.executar_simulado("ENEM Completo", simulado)

    def executar_simulado(self, area, simulado):
        """Executa um simulado e salva os resultados"""
        email = self.usuario_atual['email']
        questoes = simulado['questoes_lista']
        total_questoes = len(questoes)
        acertos = 0
        desempenho_areas = defaultdict(lambda: {'acertos': 0, 'total': 0})
        
        self.mostrar_titulo(f"SIMULADO: {simulado['titulo']}")
        print(f"Área: {area} | Duração: {simulado['duracao']} minutos\n")
        
        input("Pressione Enter para começar...")
        
        inicio = datetime.now()
        
        for i, questao in enumerate(questoes, 1):
            self.mostrar_titulo(f"Questão {i}/{total_questoes}")
            
            print(f"\n{questao['pergunta']}")
            for idx, opcao in enumerate(questao['opcoes']):
                print(f"{idx+1}. {opcao}")
            
            resposta = input("\nSua resposta (1-4): ").strip()
            while resposta not in ['1', '2', '3', '4']:
                print("Opção inválida. Digite 1, 2, 3 ou 4.")
                resposta = input("Sua resposta (1-4): ").strip()
            
            if int(resposta)-1 == questao['resposta']:
                print("\n✅ Correto!")
                acertos += 1
                # Atualiza desempenho por área
                desempenho_areas[questao['area']]['acertos'] += 1
            else:
                print(f"\n❌ Incorreto! A resposta correta era: {questao['opcoes'][questao['resposta']]}")
            
            # Atualiza total por área
            desempenho_areas[questao['area']]['total'] += 1
            
            input("\nPressione Enter para próxima questão...")
        
        tempo_gasto = (datetime.now() - inicio).total_seconds() / 60  # em minutos
        percentual = (acertos / total_questoes) * 100
        
        # Salva o resultado
        resultado = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "area": area,
            "titulo": simulado['titulo'],
            "pontuacao": acertos,
            "total_questoes": total_questoes,
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
            percentual = (dados['acertos'] / dados['total']) * 100
            print(f"\n{area}:")
            print(f"Acertos: {dados['acertos']}/{dados['total']} ({percentual:.1f}%)")
        
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
        
        self.mostrar_titulo("MEUS SIMULADOS")
        
        for i, simulado in enumerate(self.desempenho[email]['simulados'], 1):
            print(f"\nSIMULADO {i} - {simulado['data']}")
            print(f"Tipo: {simulado['titulo']}")
            print(f"Resultado: {simulado['pontuacao']}/{simulado['total_questoes']} ({simulado['percentual']:.1f}%)")
            print(f"Tempo: {simulado['tempo_gasto']:.1f} minutos")
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
                                key=lambda x: (x[1]['acertos']/x[1]['total']))
        
        print("\nSeus pontos fortes:")
        for area, dados in areas_ordenadas[-3:]:  # Top 3 melhores desempenhos
            percentual = (dados['acertos'] / dados['total']) * 100
            if percentual >= 70:
                print(f"\n⭐ {area}: {percentual:.1f}% de acertos")
        
        print("\n\nÁreas que precisam de mais atenção:")
        for area, dados in areas_ordenadas[:3]:  # Top 3 piores desempenhos
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
        
        if not conquistas_usuario:
            print("Você ainda não desbloqueou conquistas. Continue estudando!")
            input("\nPressione Enter para voltar...")
            return
        
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
                           if (dados['acertos']/dados['total']) < 0.5]
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
                perc = (dados['acertos'] / dados['total']) * 100
                print(f"\n{area}:")
                print(f"Acertos: {dados['acertos']}/{dados['total']} ({perc:.1f}%)")
                if perc >= 70:
                    print("Status: Ponto forte")
                elif perc >= 50:
                    print("Status: Médio desempenho")
                else:
                    print("Status: Ponto fraco")
        
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
                          if (dados['acertos']/dados['total']) < 0.5]
            
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
                                key=lambda x: (x[1]['acertos']/x[1]['total']))
        
        print("\n📌 Com base no seu desempenho, sugerimos o seguinte cronograma:")
        
        # Cria um plano de revisão de 30 dias
        dias_revisao = 30
        horas_diarias = 2
        
        # Distribui as áreas mais fracas nos primeiros dias
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

    def iniciar(self):
        """Inicia o sistema"""
        self.tela_inicial()

# Ponto de entrada do programa
if __name__ == "__main__":
    sistema = SistemaEstudoENEM()
    sistema.iniciar()