import os
import json
from datetime import timedelta
from datetime import datetime

class SistemaEstudo:
    def __init__(self):
        """Inicializa o sistema carregando os dados existentes"""
        self.ARQUIVO_CADASTROS = 'cadastros.json'
        self.ARQUIVO_PLANOS = 'planos_estudo.json'
        self.cadastros = []
        self.planos = {}
        self.usuario_atual = None
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega os dados dos arquivos JSON com tratamento robusto de erros"""
        try:
            # Carrega cadastros
            if os.path.exists(self.ARQUIVO_CADASTROS):
                with open(self.ARQUIVO_CADASTROS, 'r') as f:
                    dados = json.load(f)
                    self.cadastros = dados if isinstance(dados, list) else []
            
            # Carrega planos de estudo
            if os.path.exists(self.ARQUIVO_PLANOS):
                with open(self.ARQUIVO_PLANOS, 'r') as f:
                    dados = json.load(f)
                    self.planos = dados if isinstance(dados, dict) else {}
        
        except (json.JSONDecodeError, IOError) as e:
            print(f"\n⚠️ Erro ao carregar dados: {str(e)}")
            print("Inicializando com dados vazios...\n")
            self.cadastros = []
            self.planos = {}

    def salvar_dados(self):
        """Salva os dados nos arquivos JSON com tratamento de erros"""
        try:
            with open(self.ARQUIVO_CADASTROS, 'w') as f:
                json.dump(self.cadastros, f, indent=4, ensure_ascii=False)
            
            with open(self.ARQUIVO_PLANOS, 'w') as f:
                json.dump(self.planos, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"\n⚠️ Erro ao salvar dados: {str(e)}")

    def limpar_tela(self):
        """Limpa a tela do console de forma cross-platform"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_titulo(self, titulo):
        """Exibe um título formatado"""
        self.limpar_tela()
        print("\n" + "="*50)
        print(titulo.center(50))
        print("="*50 + "\n")

    def validar_email(self, email):
        """Validação básica de formato de email"""
        return '@' in email and '.' in email.split('@')[-1]

    def tela_inicial(self):
        """Exibe o menu inicial do sistema"""
        while True:
            self.mostrar_titulo("SISTEMA DE ESTUDOS PERSONALIZADOS")
            
            print("MENU PRINCIPAL:")
            print("1. Fazer login")
            print("2. Criar novo cadastro")
            print("3. Ver tutorial")
            print("4. Sair do sistema")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                if self.fazer_login():
                    self.menu_principal()
            elif opcao == "2":
                self.criar_cadastro()
            elif opcao == "3":
                self.exibir_tutorial()
            elif opcao == "4":
                print("\nObrigado por usar nosso sistema! Até logo!")
                break
            else:
                print("\n⚠️ Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def fazer_login(self):
        """Gerencia o processo de login com validações"""
        tentativas = 0
        max_tentativas = 3
        
        while tentativas < max_tentativas:
            self.mostrar_titulo("ÁREA DE LOGIN")
            
            email = input("Email: ").strip().lower()
            senha = input("Senha: ").strip()
            
            if not email or not senha:
                print("\n⚠️ Email e senha são obrigatórios!")
                tentativas += 1
                continue
            
            usuario_encontrado = None
            for usuario in self.cadastros:
                if usuario.get('email') == email and usuario.get('senha') == senha:
                    usuario_encontrado = usuario
                    break
            
            if usuario_encontrado:
                print(f"\n✅ Login bem-sucedido! Bem-vindo(a), {usuario_encontrado['nome']}!")
                self.usuario_atual = usuario_encontrado
                input("\nPressione Enter para acessar o menu principal...")
                return True
            
            tentativas += 1
            print(f"\n⚠️ Credenciais incorretas. Tentativas restantes: {max_tentativas - tentativas}")
            input("Pressione Enter para tentar novamente...")
        
        print("\n⚠️ Número máximo de tentativas excedido. Voltando ao menu inicial...")
        input("Pressione Enter para continuar...")
        return False

    def criar_cadastro(self):
        """Gerencia o processo completo de cadastro"""
        self.mostrar_titulo("NOVO CADASTRO")
        
        # Validação do nome
        while True:
            nome = input("Nome completo: ").strip()
            if len(nome.split()) >= 2:
                break
            print("⚠️ Por favor, insira seu nome completo (pelo menos 2 partes).")
        
        # Validação do email
        while True:
            email = input("Email: ").strip().lower()
            if not email:
                print("⚠️ Email é obrigatório!")
                continue
                
            if not self.validar_email(email):
                print("⚠️ Formato de email inválido!")
                continue
                
            if any(u.get('email') == email for u in self.cadastros):
                print("⚠️ Este email já está cadastrado!")
                continue
                
            break
        
        # Validação da senha
        while True:
            senha = input("Crie uma senha (mínimo 6 caracteres): ").strip()
            if len(senha) < 6:
                print("⚠️ Senha muito curta! Mínimo 6 caracteres.")
                continue
            
            confirmacao = input("Confirme a senha: ").strip()
            if senha != confirmacao:
                print("⚠️ As senhas não coincidem!")
                continue
            break
        
        # Coleta informações adicionais
        self.mostrar_titulo("PERSONALIZAÇÃO DO PERFIL")
        
        idade = self.obter_numero("Idade: ", 5, 100)
        horas_estudo = self.obter_numero("Horas disponíveis para estudo por semana: ", 1, 70)
        
        print("\nÁreas de interesse (digite 'fim' para terminar):")
        areas_interesse = []
        while True:
            area = input("> ").strip()
            if area.lower() == 'fim':
                if len(areas_interesse) < 1:
                    print("⚠️ Adicione pelo menos uma área de interesse!")
                    continue
                break
            if area:
                areas_interesse.append(area)
        
        # Cria o novo usuário
        novo_usuario = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'idade': idade,
            'horas_disponiveis': horas_estudo,
            'areas_interesse': areas_interesse,
            'data_cadastro': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.cadastros.append(novo_usuario)
        self.salvar_dados()
        
        print("\n✅ Cadastro realizado com sucesso!")
        print("Iniciando teste diagnóstico para criar seu plano personalizado...")
        input("\nPressione Enter para continuar...")
        
        self.realizar_teste_diagnostico(novo_usuario)
        return True

    def obter_numero(self, mensagem, minimo, maximo):
        """Obtém um número dentro de um intervalo específico com validação"""
        while True:
            try:
                valor = int(input(mensagem))
                if minimo <= valor <= maximo:
                    return valor
                print(f"⚠️ Valor deve estar entre {minimo} e {maximo}!")
            except ValueError:
                print("⚠️ Por favor, digite um número válido.")

    def realizar_teste_diagnostico(self, usuario):
        """Realiza o teste diagnóstico para criar plano de estudos"""
        self.mostrar_titulo("TESTE DIAGNÓSTICO")
        
        print("Responda as questões abaixo para avaliar seu nível atual (1-5):\n")
        
        questoes = [
            "Frequência de estudos atuais: (1-Raramente, 5-Diariamente)",
            "Conhecimento nas áreas de interesse: (1-Iniciante, 5-Avançado)",
            "Objetivo principal com os estudos: (1-Conhecimento geral, 5-Preparação para o ENEM)"
        ]
        
        respostas = []
        for i, questao in enumerate(questoes, 1):
            resposta = self.obter_numero(f"Q{i}: {questao} ", 1, 5)
            respostas.append(resposta)
        
        nivel = sum(respostas) / len(respostas)
        plano = self.gerar_plano_estudo(usuario, nivel)
        
        if 'email' in usuario:
            self.planos[usuario['email']] = plano
            self.salvar_dados()
        
        print("\n✅ Teste concluído! Plano de estudo gerado com sucesso!")
        input("\nPressione Enter para visualizar seu plano...")
        self.mostrar_plano_estudo()

    def gerar_plano_estudo(self, usuario, nivel):
        """Gera um plano de estudo personalizado"""
        semanas = 4  # Plano padrão de 4 semanas
        horas_semana = usuario['horas_disponiveis'] / semanas
        intensidade = round((nivel * usuario['horas_disponiveis']) / 15, 1)
        
        # Distribui as áreas de interesse pelas semanas
        metas_semanais = []
        for semana in range(1, semanas + 1):
            meta = {
                'semana': semana,
                'topicos': [],
                'horas_estimadas': horas_semana,
                'concluida': False,
                'data_inicio': (datetime.now() + timedelta(weeks=semana-1)).strftime("%Y-%m-%d")
            }
            
            # Distribui as áreas de interesse de forma cíclica
            for idx, area in enumerate(usuario['areas_interesse']):
                if idx % semanas == semana - 1:
                    meta['topicos'].append({
                        'area': area,
                        'atividades': [
                            f"Introdução a {area}",
                            f"Exercícios práticos de {area}",
                            f"Revisão de conceitos de {area}"
                        ],
                        'recursos': [
                            f"Livro: Introdução a {area}",
                            f"Site: www.{area.replace(' ', '').lower()}.com.br/exercicios",
                            f"Vídeo: Aulas de {area} no YouTube"
                        ]
                    })
            
            metas_semanais.append(meta)
        
        return {
            'data_criacao': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'nivel_inicial': round(nivel, 1),
            'intensidade': intensidade,
            'duracao_semanas': semanas,
            'metas_semanais': metas_semanais,
            'progresso': 0,
            'ultima_atualizacao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def menu_principal(self):
        """Exibe o menu principal após login"""
        while True:
            self.mostrar_titulo(f"OLÁ, {self.usuario_atual['nome'].upper()}!")
            
            print("MENU PRINCIPAL:")
            print("1. Visualizar plano de estudo")
            print("2. Ver metas semanais")
            print("3. Atualizar progresso")
            print("4. Refazer teste diagnóstico")
            print("5. Sair da conta")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.mostrar_plano_estudo()
            elif opcao == "2":
                self.mostrar_metas_semanais()
            elif opcao == "3":
                self.atualizar_progresso()
            elif opcao == "4":
                self.realizar_teste_diagnostico(self.usuario_atual)
            elif opcao == "5":
                self.usuario_atual = None
                print("\n✅ Logout realizado com sucesso!")
                input("Pressione Enter para voltar ao menu inicial...")
                break
            else:
                print("\n⚠️ Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def mostrar_plano_estudo(self):
        """Exibe o plano de estudo do usuário"""
        if not self.usuario_atual:
            print("\n⚠️ Nenhum usuário logado.")
            return
        
        plano = self.planos.get(self.usuario_atual['email'])
        
        if not plano:
            print("\n⚠️ Nenhum plano de estudo encontrado.")
            return
        
        self.mostrar_titulo("SEU PLANO DE ESTUDO")
        
        print(f"📅 Criado em: {plano['data_criacao']}")
        print(f"🔄 Última atualização: {plano['ultima_atualizacao']}")
        print(f"📊 Nível inicial: {plano['nivel_inicial']}/5.0")
        print(f"⚡ Intensidade: {'⭐' * int(plano['intensidade'])} ({plano['intensidade']})")
        print(f"📈 Progresso geral: {plano['progresso']}%")
        print(f"⏳ Duração total: {plano['duracao_semanas']} semanas")
        print(f"🕒 Horas semanais estimadas: {self.usuario_atual['horas_disponiveis']/plano['duracao_semanas']:.1f}h")
        
        input("\nPressione Enter para ver detalhes...")
        self.mostrar_metas_semanais()

    def mostrar_metas_semanais(self):
        """Exibe as metas semanais do usuário"""
        if not self.usuario_atual:
            print("\n⚠️ Nenhum usuário logado.")
            return
        
        plano = self.planos.get(self.usuario_atual['email'])
        
        if not plano:
            print("\n⚠️ Nenhum plano de estudo encontrado.")
            return
        
        self.mostrar_titulo("METAS SEMANAIS")
        
        for meta in plano['metas_semanais']:
            status = "✅" if meta['concluida'] else "❌"
            print(f"\n📅 Semana {meta['semana']} {status}")
            print(f"⏰ Horas estimadas: {meta['horas_estimadas']:.1f}h")
            print(f"🗓️ Data prevista: {meta['data_inicio']}")
            
            if meta['topicos']:
                print("\n📚 Tópicos:")
                for topico in meta['topicos']:
                    print(f"\n📌 {topico['area']}:")
                    print("📖 Atividades:")
                    for atividade in topico['atividades']:
                        print(f"   • {atividade}")
                    
                    print("\n🔗 Recursos recomendados:")
                    for recurso in topico['recursos']:
                        print(f"   › {recurso}")
            else:
                print("\nNenhum tópico atribuído para esta semana.")
            
            print("\n" + "-"*50)
        
        input("\nPressione Enter para voltar...")

    def atualizar_progresso(self):
        """Permite ao usuário atualizar seu progresso"""
        if not self.usuario_atual:
            print("\n⚠️ Nenhum usuário logado.")
            return
        
        plano = self.planos.get(self.usuario_atual['email'])
        
        if not plano:
            print("\n⚠️ Nenhum plano de estudo encontrado.")
            return
        
        self.mostrar_titulo("ATUALIZAR PROGRESSO")
        
        concluidas = 0
        for meta in plano['metas_semanais']:
            while True:
                resposta = input(f"Semana {meta['semana']} concluída? (s/n): ").lower().strip()
                if resposta in ['s', 'n']:
                    meta['concluida'] = resposta == 's'
                    if meta['concluida']:
                        concluidas += 1
                    break
                print("⚠️ Por favor, digite 's' para sim ou 'n' para não.")
        
        total_semanas = len(plano['metas_semanais'])
        plano['progresso'] = int((concluidas / total_semanas) * 100)
        plano['ultima_atualizacao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.salvar_dados()
        print(f"\n✅ Progresso atualizado! Conclusão geral: {plano['progresso']}%")
        input("\nPressione Enter para voltar...")

    def exibir_tutorial(self):
        """Exibe o tutorial completo do sistema"""
        self.mostrar_titulo("TUTORIAL DO SISTEMA")
        
        print("""
🎯 COMO USAR O SISTEMA:

1. CADASTRO:
   - Forneça seus dados pessoais válidos
   - Informe suas áreas de interesse
   - Realize o teste diagnóstico para gerar seu plano personalizado

2. LOGIN:
   - Acesse com email e senha cadastrados
   - Você tem 3 tentativas para login

3. PLANO DE ESTUDO:
   - Personalizado com base no seu teste
   - Inclui metas semanais com tópicos e atividades
   - Mostra seu progresso geral e recursos recomendados

4. METAS SEMANAIS:
   - Lista de tópicos para cada semana
   - Atividades sugeridas e recursos complementares
   - Horas estimadas de estudo

5. ATUALIZAÇÃO:
   - Marque semanas concluídas para acompanhar progresso
   - Seu progresso é calculado automaticamente
   - Pode refazer o teste para ajustar o plano quando quiser

📝 DICAS:
- Revise seu plano semanalmente
- Ajuste suas horas disponíveis se necessário
- Explore os recursos recomendados
- Mantenha seu progresso atualizado
        """)
        
        input("\nPressione Enter para voltar...")

if __name__ == "__main__":
    sistema = SistemaEstudo()
    sistema.tela_inicial()