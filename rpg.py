import random


class Jogador:
    def __init__(self):
        self.nome = "Aventureiro"
        self.hp_max = 100
        self.hp = self.hp_max
        self.ouro = 40
        self.xp = 0
        self.nivel = 1
        self.xp_proximo = 40
        self.arma = {"nome": "Adaga Velha", "dano": 9, "preco": 0}
        self.armadura = {"nome": "Roupas Comuns", "defesa": 3, "preco": 0}
        self.pocoes = 2
        self.dias = 1
        self.vitorias = 0


jogador = Jogador()

ARMAS = [
    {"nome": "Espada Curta de Ferro", "dano": 16, "preco": 75},
    {"nome": "Machado de Batalha", "dano": 24, "preco": 160},
    {"nome": "Espada Longa de Aco", "dano": 35, "preco": 320},
    {"nome": "Lamina do Guardiao", "dano": 50, "preco": 580},
    {"nome": "Espada Runica Ancestral", "dano": 70, "preco": 950},
]

ARMADURAS = [
    {"nome": "Colete de Couro", "defesa": 8, "preco": 65},
    {"nome": "Cota de Malha", "defesa": 15, "preco": 150},
    {"nome": "Armadura de Placas", "defesa": 26, "preco": 310},
    {"nome": "Armadura do Cavaleiro", "defesa": 40, "preco": 560},
    {"nome": "Armadura Elfica Encantada", "defesa": 55, "preco": 900},
]

INIMIGOS = {
    "floresta": [
        {"nome": "Goblin Escoteiro", "hp": 35, "dano": 8, "ouro": (12, 22), "xp": (10, 18)},
        {"nome": "Goblin Guerreiro", "hp": 50, "dano": 12, "ouro": (18, 30), "xp": (15, 25)},
        {"nome": "Lobo das Sombras", "hp": 40, "dano": 11, "ouro": (10, 20), "xp": (12, 20)},
    ],
    "masmorra": [
        {"nome": "Goblin Elite", "hp": 70, "dano": 16, "ouro": (30, 50), "xp": (25, 40)},
        {"nome": "Orc Mercenario", "hp": 90, "dano": 20, "ouro": (40, 65), "xp": (30, 50)},
        {"nome": "Esqueleto Guerreiro", "hp": 65, "dano": 18, "ouro": (25, 45), "xp": (22, 38)},
        {"nome": "Troll da Caverna", "hp": 130, "dano": 26, "ouro": (60, 100), "xp": (50, 80)},
    ],
}


def limpar_tela():
    print("\n" * 4)


def pausa():
    input("\nPressione ENTER para continuar...")


def separador():
    print("=" * 65)


def mostrar_status():
    separador()
    print("                CRONICAS DE ELDORIA")
    separador()
    print(f"Nome: {jogador.nome}")
    print(f"Nivel: {jogador.nivel}")
    print(f"HP: {jogador.hp}/{jogador.hp_max}")
    print(f"Ouro: {jogador.ouro}")
    print(f"XP: {jogador.xp}/{jogador.xp_proximo}")
    print(f"Pocoes: {jogador.pocoes}")
    print(f"Arma: {jogador.arma['nome']} | Dano: {jogador.arma['dano']}")
    print(f"Armadura: {jogador.armadura['nome']} | Defesa: {jogador.armadura['defesa']}")
    print(f"Vitorias: {jogador.vitorias}")
    print(f"Dias: {jogador.dias}")
    separador()


def ganhar_xp(quantidade):
    jogador.xp += quantidade

    while jogador.xp >= jogador.xp_proximo:
        jogador.xp -= jogador.xp_proximo
        jogador.nivel += 1
        jogador.hp_max += 18
        jogador.hp = jogador.hp_max
        jogador.xp_proximo = int(jogador.xp_proximo * 1.45)

        print("\n" + "*" * 65)
        print("              LEVEL UP!")
        print("*" * 65)
        print(f"Voce alcancou o nivel {jogador.nivel}.")
        print(f"Seu HP maximo agora e {jogador.hp_max}.")
        print("Seu HP foi restaurado!")
        print("*" * 65)


def criar_inimigo(area):
    base = random.choice(INIMIGOS[area])
    fator = 1 + (jogador.nivel - 1) * 0.12
    hp = int(base["hp"] * fator)

    return {
        "nome": base["nome"],
        "hp": hp,
        "hp_max": hp,
        "dano": int(base["dano"] * fator),
        "ouro": base["ouro"],
        "xp": base["xp"],
    }


def derrotar_inimigo(inimigo):
    ouro = random.randint(*inimigo["ouro"])
    xp = random.randint(*inimigo["xp"])

    jogador.ouro += ouro
    jogador.vitorias += 1

    print()
    separador()
    print(f"VOCE DERROTOU {inimigo['nome'].upper()}!")
    print(f"Ouro recebido: {ouro}")
    print(f"XP recebido: {xp}")
    separador()

    ganhar_xp(xp)

    if random.random() < 0.25:
        jogador.pocoes += 1
        print("\nVoce encontrou uma Pocao de Cura!")


def combate(area):
    inimigo = criar_inimigo(area)

    print(f"\nUM {inimigo['nome'].upper()} APARECEU!")
    print(f"HP do inimigo: {inimigo['hp']}/{inimigo['hp_max']}")
    separador()

    while inimigo["hp"] > 0 and jogador.hp > 0:
        print(f"\nSeu HP: {jogador.hp}/{jogador.hp_max}")
        print(f"{inimigo['nome']} HP: {inimigo['hp']}/{inimigo['hp_max']}")
        print("\n1 - Atacar\n2 - Usar Pocao\n3 - Tentar Fugir")

        escolha = input("\nEscolha: ")

        if escolha == "1":
            dano = jogador.arma["dano"] + random.randint(1, 7)
            inimigo["hp"] -= dano
            print(f"\nVoce atacou com {jogador.arma['nome']}.")
            print(f"Dano causado: {dano}")

            if inimigo["hp"] <= 0:
                derrotar_inimigo(inimigo)
                pausa()
                return

        elif escolha == "2":
            if jogador.pocoes <= 0:
                print("\nVoce nao possui Pocoes de Cura!")
                continue

            if jogador.hp >= jogador.hp_max:
                print("\nSeu HP ja esta cheio!")
                continue

            cura = random.randint(35, 55)
            recuperado = min(cura, jogador.hp_max - jogador.hp)
            jogador.hp += recuperado
            jogador.pocoes -= 1

            print("\nVoce bebeu uma Pocao de Cura.")
            print(f"HP recuperado: {recuperado}")

        elif escolha == "3":
            if random.random() < 0.65:
                print("\nVoce conseguiu escapar!")
                pausa()
                return

            print("\nVoce tentou fugir, mas o inimigo impediu!")

        else:
            print("\nOpcao invalida!")
            continue

        if inimigo["hp"] > 0:
            dano_bruto = inimigo["dano"] + random.randint(-2, 4)
            defesa = jogador.armadura["defesa"] // 2
            dano = max(1, dano_bruto - defesa)
            jogador.hp = max(0, jogador.hp - dano)

            print(f"\nO {inimigo['nome']} atacou!")
            print(f"Dano recebido: {dano}")


def comprar_item(itens, atributo, titulo):
    limpar_tela()
    print(titulo)
    separador()

    for indice, item in enumerate(itens, 1):
        print(
            f"{indice} - {item['nome']} | "
            f"{atributo.capitalize()}: {item[atributo]} | "
            f"Preco: {item['preco']}"
        )

    print("\n0 - Voltar")

    try:
        escolha = int(input("\nEscolha: "))
    except ValueError:
        print("Digite um numero.")
        pausa()
        return

    if escolha == 0:
        return

    if not 1 <= escolha <= len(itens):
        print("Opcao invalida.")
        pausa()
        return

    item = itens[escolha - 1]

    if jogador.ouro < item["preco"]:
        print("\nOuro insuficiente!")
        pausa()
        return

    jogador.ouro -= item["preco"]

    if atributo == "dano":
        jogador.arma = item.copy()
    else:
        jogador.armadura = item.copy()

    print(f"\nVoce equipou: {item['nome']}")
    pausa()


def comprar_pocao():
    limpar_tela()
    print("LOJA")
    separador()
    print("Pocao de Cura - 25 ouro")
    print(f"Voce possui: {jogador.ouro} ouro")

    if input("\nComprar? (s/n): ").lower() == "s":
        if jogador.ouro >= 25:
            jogador.ouro -= 25
            jogador.pocoes += 1
            print("\nPocao comprada!")
        else:
            print("\nVoce nao possui ouro suficiente!")

    pausa()


def loja():
    while True:
        limpar_tela()
        print("             LOJA DO FERREIRO")
        separador()
        print(f"Ouro: {jogador.ouro}\n")
        print("1 - Comprar Arma")
        print("2 - Comprar Armadura")
        print("3 - Comprar Pocao")
        print("4 - Voltar")

        escolha = input("\nEscolha: ")

        if escolha == "1":
            comprar_item(ARMAS, "dano", "LOJA DE ARMAS")
        elif escolha == "2":
            comprar_item(ARMADURAS, "defesa", "LOJA DE ARMADURAS")
        elif escolha == "3":
            comprar_pocao()
        elif escolha == "4":
            return
        else:
            print("Opcao invalida.")
            pausa()


def taverna():
    rumores = [
        "Viajante: Dizem que existe um troll nas profundezas da masmorra.",
        "Mercador: Os goblins estao ficando cada vez mais organizados.",
        "Bebado: Eu vi luzes estranhas perto da torre antiga.",
        "Cacador: A floresta esta muito perigosa ultimamente.",
    ]

    while True:
        limpar_tela()
        print("             TAVERNA DO JAVALI DORMINHOCO")
        separador()
        print("1 - Descansar - 15 ouro")
        print("2 - Ouvir rumores")
        print("3 - Voltar")

        escolha = input("\nEscolha: ")

        if escolha == "1":
            if jogador.ouro >= 15:
                jogador.ouro -= 15
                jogador.hp = jogador.hp_max
                jogador.dias += 1
                print("\nVoce descansou na taverna.")
                print("Seu HP foi completamente restaurado.")
            else:
                print("\nVoce nao possui ouro suficiente.")
            pausa()

        elif escolha == "2":
            print(f"\n{random.choice(rumores)}")
            pausa()

        elif escolha == "3":
            return
        else:
            print("Opcao invalida.")
            pausa()


def trabalhar():
    trabalhos = [
        "Voce ajudou a carregar mercadorias no mercado.",
        "Voce patrulhou os arredores da vila.",
        "Voce ajudou o ferreiro durante o dia.",
        "Voce cacou coelhos e vendeu a carne.",
    ]

    ganho = random.randint(10, 22)
    jogador.ouro += ganho
    jogador.dias += 1

    limpar_tela()
    print(random.choice(trabalhos))
    print(f"\nVoce recebeu {ganho} ouro.")
    pausa()


def inventario():
    limpar_tela()
    print("             INVENTARIO")
    separador()
    print(f"Arma equipada: {jogador.arma['nome']}")
    print(f"Dano: {jogador.arma['dano']}\n")
    print(f"Armadura equipada: {jogador.armadura['nome']}")
    print(f"Defesa: {jogador.armadura['defesa']}\n")
    print(f"Pocoes: {jogador.pocoes}")
    print(f"Vitorias: {jogador.vitorias}")
    print(f"Dias de aventura: {jogador.dias}")
    print(f"Nivel: {jogador.nivel}")
    print(f"XP: {jogador.xp}/{jogador.xp_proximo}")
    print(f"\nOuro: {jogador.ouro}")
    pausa()


def falar_com_anciao():
    limpar_tela()
    print("             O ANCIÃO DE RIVERMOOR")
    separador()
    print('\n"Os goblins estao atacando nossas estradas."')
    print('\n"Fortaleca seu equipamento antes de entrar na masmorra."')
    print('\n"A masmorra e perigosa demais para aventureiros inexperientes."')
    print("\nVoce precisa chegar ao nivel 3 antes de entrar na masmorra.")
    pausa()


def explorar_floresta():
    limpar_tela()
    print("             FLORESTA SOMBRIA")
    separador()
    print("\nVoce entra na floresta.")
    print("As arvores bloqueiam a luz do sol.")
    print("Um galho se quebra atras de voce...")
    pausa()
    combate("floresta")


def entrar_masmorra():
    limpar_tela()
    print("             MASMORRA ANTIGA")
    separador()

    if jogador.nivel < 3:
        print("\nA entrada da masmorra esta protegida por uma energia sombria.")
        print("\nVoce precisa estar no nivel 3.")
        pausa()
        return

    print("\nVoce desce lentamente pelas escadas.")
    print("O cheiro de morte toma conta do local.")
    print("Algo enorme se move nas sombras...")
    pausa()
    combate("masmorra")


def introducao():
    limpar_tela()
    separador()
    print("                  CRONICAS DE ELDORIA")
    print("                       RPG")
    separador()
    print("\nReino de Eldoria - Ano 427")
    print("\nVoce chega a pequena vila de Rivermoor.")
    print("\nDurante semanas, goblins tem atacado as estradas.")
    print("\nMercadores desapareceram.")
    print("\nCacadores encontraram criaturas nas profundezas da floresta.")
    print("\nRumores dizem que uma antiga masmorra voltou a despertar.")
    print("\nVoce possui uma velha adaga, 40 moedas de ouro e duas pocões.")
    print("\nSua aventura esta prestes a comecar.")
    pausa()


def vila():
    opcoes = {
        "1": explorar_floresta,
        "2": entrar_masmorra,
        "3": loja,
        "4": taverna,
        "5": trabalhar,
        "6": inventario,
        "7": falar_com_anciao,
    }

    while jogador.hp > 0:
        limpar_tela()
        mostrar_status()
        print("\nVoce esta na vila de Rivermoor.\n")
        print("1 - Explorar a Floresta")
        print("2 - Entrar na Masmorra")
        print("3 - Loja do Ferreiro")
        print("4 - Taverna")
        print("5 - Trabalhar")
        print("6 - Inventario")
        print("7 - Falar com o Anciao")
        print("8 - Sair do jogo")

        escolha = input("\nEscolha: ")

        if escolha == "8":
            print("\nObrigado por jogar CRONICAS DE ELDORIA!")
            return

        acao = opcoes.get(escolha)

        if acao:
            acao()
            if escolha in ("1", "2") and jogador.hp > 0:
                pausa()
        else:
            print("\nOpcao invalida!")
            pausa()


def game_over():
    limpar_tela()
    separador()
    print("                    GAME OVER")
    separador()
    print("\nVoce caiu em combate nas terras de Eldoria.")
    print(f"\nNivel alcancado: {jogador.nivel}")
    print(f"Vitorias: {jogador.vitorias}")
    print(f"Ouro: {jogador.ouro}")
    print("\nSua lenda termina aqui...")
    separador()


def main():
    introducao()
    vila()

    if jogador.hp <= 0:
        game_over()


if __name__ == "__main__":
    main()
