
pacientes = []
medicos = []
consultas = []

def mostrar_menu():
    """Exibe o menu principal e retorna a opção válida"""
    while True:
        print("\n=== HOSPITAL DAS CLÍNICAS ===")
        print("1. Cadastrar Paciente")
        print("2. Cadastrar Médico")
        print("3. Agendar Consulta")
        print("4. Listar Pacientes")
        print("5. Listar Médicos")
        print("6. Listar Consultas")
        print("7. Estatísticas")
        print("0. Sair")
        
        try:
            opcao = int(input("\nOpção: "))
            if 0 <= opcao <= 7:
                return opcao
            print("Opção inválida! Tente novamente.")
        except ValueError:
            print("Digite um número válido!")

def validar_entrada(texto, tipo=str, validador=None):
    """Função genérica para validação de entradas"""
    while True:
        entrada = input(texto).strip()
        try:
            if tipo != str:
                entrada = tipo(entrada)
            if validador and not validador(entrada):
                raise ValueError
            return entrada
        except ValueError:
            print("Entrada inválida! Tente novamente.")

def cadastrar_paciente():
    """Cadastra um novo paciente"""
    print("\n--- NOVO PACIENTE ---")
    
    cpf = validar_entrada("CPF (11 dígitos): ", 
                         validador=lambda x: x.isdigit() and len(x) == 11)
    
    if any(p['cpf'] == cpf for p in pacientes):
        print("Paciente já cadastrado!")
        return
    
    paciente = {
        'cpf': cpf,
        'nome': validar_entrada("Nome: ", validador=lambda x: x.replace(" ", "").isalpha()),
        'idade': validar_entrada("Idade: ", int, lambda x: x > 0),
        'sexo': validar_entrada("Sexo (M/F/O): ", str.upper, lambda x: x in ['M', 'F', 'O']),
        'telefone': input("Telefone: "),
        'endereco': input("Endereço: ")
    }
    
    pacientes.append(paciente)
    print(f"\nPaciente {paciente['nome']} cadastrado!")

def cadastrar_medico():
    """Cadastra um novo médico"""
    print("\n--- NOVO MÉDICO ---")
    
    crm = validar_entrada("CRM: ", validador=lambda x: x.isdigit() and len(x) >= 5)
    
    if any(m['crm'] == crm for m in medicos):
        print("Médico já cadastrado!")
        return
    
    medico = {
        'crm': crm,
        'nome': validar_entrada("Nome: ", validador=lambda x: x.replace(" ", "").isalpha()),
        'especialidade': input("Especialidade: "),
        'carga_horaria': validar_entrada("Carga horária (h/semana): ", int, lambda x: 0 < x <= 80)
    }
    
    medicos.append(medico)
    print(f"\nDr. {medico['nome']} cadastrado!")

def agendar_consulta():
    """Agenda uma nova consulta"""
    if not pacientes or not medicos:
        print("Cadastre pacientes e médicos primeiro!")
        return
    
    print("\n--- NOVA CONSULTA ---")
    
    # Selecionar paciente
    print("\nPacientes:")
    for i, p in enumerate(pacientes, 1):
        print(f"{i}. {p['nome']} ({p['cpf']})")
    
    idx_pac = validar_entrada("\nSelecione o paciente: ", int, 
                            lambda x: 1 <= x <= len(pacientes)) - 1
    
    # Selecionar médico
    print("\nMédicos:")
    for i, m in enumerate(medicos, 1):
        print(f"{i}. Dr. {m['nome']} - {m['especialidade']}")
    
    idx_med = validar_entrada("\nSelecione o médico: ", int, 
                            lambda x: 1 <= x <= len(medicos)) - 1
    
    # Data e hora
    data = validar_entrada("Data (DD/MM/AAAA): ", 
                          validador=lambda x: len(x) == 10 and x[2] == '/' and x[5] == '/')
    hora = validar_entrada("Hora (HH:MM): ", 
                          validador=lambda x: len(x) == 5 and x[2] == ':')
    
    # Verificar conflito
    medico = medicos[idx_med]
    if any(c['medico']['crm'] == medico['crm'] and 
           c['data'] == data and c['hora'] == hora for c in consultas):
        print("Horário já agendado!")
        return
    
    consulta = {
        'paciente': pacientes[idx_pac],
        'medico': medico,
        'data': data,
        'hora': hora,
        'realizada': False
    }
    
    consultas.append(consulta)
    print("\nConsulta agendada com sucesso!")

def listar_dados(tipo):
    """Lista pacientes, médicos ou consultas"""
    itens = pacientes if tipo == 'pacientes' else \
            medicos if tipo == 'medicos' else \
            consultas
    
    if not itens:
        print(f"Nenhum {'paciente' if tipo == 'pacientes' else 'médico' if tipo == 'medicos' else 'consulta'} cadastrado!")
        return
    
    print(f"\n--- {tipo.upper()} ---")
    for i, item in enumerate(itens, 1):
        print(f"\n{i}.")
        if tipo == 'pacientes':
            print(f"Nome: {item['nome']}\nCPF: {item['cpf']}\nIdade: {item['idade']}")
        elif tipo == 'medicos':
            print(f"Nome: Dr. {item['nome']}\nCRM: {item['crm']}\nEspecialidade: {item['especialidade']}")
        else:
            status = "Realizada" if item['realizada'] else "Agendada"
            print(f"Paciente: {item['paciente']['nome']}\nMédico: Dr. {item['medico']['nome']}")
            print(f"Data: {item['data']} {item['hora']}\nStatus: {status}")

def mostrar_estatisticas():
    """Exibe estatísticas do hospital"""
    print("\n--- ESTATÍSTICAS ---")
    print(f"\nPacientes: {len(pacientes)}")
    print(f"Médicos: {len(medicos)}")
    print(f"Consultas: {len(consultas)}")
    
    if pacientes:
        media_idade = sum(p['idade'] for p in pacientes) / len(pacientes)
        print(f"\nMédia de idade: {media_idade:.1f} anos")
        
        sexos = {'M': 0, 'F': 0, 'O': 0}
        for p in pacientes:
            sexos[p['sexo']] += 1
        
        print("\nDistribuição por sexo:")
        for s, qtd in sexos.items():
            if qtd: print(f"{s}: {qtd} ({qtd/len(pacientes):.1%})")
    
    if medicos:
        especialidades = {}
        for m in medicos:
            especialidades[m['especialidade']] = especialidades.get(m['especialidade'], 0) + 1
        
        print("\nEspecialidades médicas:")
        for esp, qtd in especialidades.items():
            print(f"{esp}: {qtd} ({qtd/len(medicos):.1%})")

def main():
    """Função principal do sistema"""
    print("Bem-vindo ao Sistema do Hospital das Clínicas")
    
    while True:
        op = mostrar_menu()
        
        if op == 1: cadastrar_paciente()
        elif op == 2: cadastrar_medico()
        elif op == 3: agendar_consulta()
        elif op == 4: listar_dados('pacientes')
        elif op == 5: listar_dados('medicos')
        elif op == 6: listar_dados('consultas')
        elif op == 7: mostrar_estatisticas()
        elif op == 0: break
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()