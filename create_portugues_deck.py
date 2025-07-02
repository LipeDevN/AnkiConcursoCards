import sqlite3
import zipfile
import json
import time
import os
from datetime import datetime

def create_portugues_deck():
    """
    Cria um deck do Anki (.apkg) com as matérias de Língua Portuguesa
    """
    
    # Dados dos cartões - Frente e Verso
    cards_data = [
        # Leitura e Interpretação de Textos
        ("Como diferenciar fato de opinião em um texto?", 
         "**Fato:** Informação objetiva, verificável, indiscutível<br>**Opinião:** Julgamento subjetivo, ponto de vista pessoal, uso de adjetivos valorativos, verbos de opinião (acho, creio, considero)"),
        
        ("O que é intencionalidade discursiva segundo Fiorin e Savioli?", 
         "**Propósito comunicativo** do autor: informar, persuadir, emocionar, divertir. Manifesta-se através de escolhas lexicais, estrutura argumentativa e recursos estilísticos"),
        
        ("Como analisar implícitos e subentendidos?", 
         "**Implícito:** Informação não dita mas deduzível logicamente<br>**Subentendido:** Informação que depende do contexto e intenção do falante. Análise através de pressupostos, inferências e contexto situacional"),
        
        ("Como identificar ideias principais e secundárias?", 
         "**Principal:** Essencial para compreensão, geralmente no tópico frasal<br>**Secundária:** Complementa, exemplifica, detalha a principal. Técnica: eliminar detalhes e ver se o sentido se mantém"),
        
        ("Quais são os recursos de argumentação segundo Orlandi?", 
         "**Argumentos de autoridade, exemplificação, causa/consequência, comparação/contraste, dados estatísticos, argumentação por eliminação, refutação**"),
        
        ("Como funciona a argumentação por Eni Orlandi?", 
         "Processo de **construção de sentidos** através de relações de força, posições ideológicas e formações discursivas que determinam o que pode/deve ser dito"),
        
        ("Recursos argumentativos segundo Koch?", 
         "**Operadores argumentativos** (mas, porém, logo), **modalizadores** (certamente, talvez), **pressupostos**, **polifonia**, **intertextualidade**"),
        
        # Linguagem e Comunicação
        ("O que é situação comunicativa?", 
         "**Contexto** em que ocorre a comunicação: emissor, receptor, código, canal, contexto, finalidade. Determina escolhas linguísticas adequadas"),
        
        ("O que é variação linguística?", 
         "**Diversidade de usos** da língua: regional (dialetos), social (socioletos), situacional (registros), temporal (mudanças históricas)"),
        
        ("Tipos de variação linguística", 
         "**Diatópica:** geográfica<br>**Diastrática:** social<br>**Diafásica:** situacional<br>**Diacrônica:** temporal<br>**Diamésica:** meio (fala/escrita)"),
        
        ("Como a situação comunicativa influencia a linguagem?", 
         "**Formal/informal, técnica/coloquial, objetiva/subjetiva**. Adequação ao interlocutor, propósito, contexto social e meio de comunicação"),
        
        # Gêneros e Tipos Textuais - Marcuschi
        ("Diferença entre gênero e tipo textual segundo Marcuschi?", 
         "**Tipo:** Categoria teórica (narração, descrição, exposição, argumentação, injunção)<br>**Gênero:** Realização concreta (carta, e-mail, reportagem, bula)"),
        
        ("Características dos tipos textuais", 
         "**Narrativo:** sequência temporal, personagens<br>**Descritivo:** simultaneidade, detalhamento<br>**Expositivo:** informação, explicação<br>**Argumentativo:** tese, argumentos<br>**Injuntivo:** instruções, comandos"),
        
        ("O que é intertextualidade segundo Marcuschi?", 
         "**Relação entre textos:** citação, alusão, paráfrase, paródia, pastiche. Diálogo explícito ou implícito com outros textos"),
        
        ("Tipos de intertextualidade", 
         "**Explícita:** citação direta, referência<br>**Implícita:** alusão, paráfrase<br>**Paródica:** ironia, crítica<br>**Estilística:** imitação de estilo"),
        
        ("Características estruturais dos gêneros textuais", 
         "**Composição:** organização textual<br>**Estilo:** escolhas linguísticas<br>**Tema:** conteúdo típico<br>**Função social:** propósito comunicativo"),
        
        # Coesão e Coerência - Koch
        ("O que é coesão textual segundo Koch?", 
         "**Articulação sintático-semântica** entre elementos do texto através de mecanismos linguísticos: referência, substituição, elipse, conjunção"),
        
        ("Tipos de coesão textual", 
         "**Referencial:** anáfora, catáfora<br>**Sequencial:** conectores, operadores<br>**Lexical:** repetição, sinonímia, hiperonímia<br>**Temporal:** advérbios, locuções"),
        
        ("O que é coerência textual?", 
         "**Unidade de sentido** que torna o texto compreensível. Depende de conhecimento de mundo, contexto, inferenciais e continuidade temática"),
        
        ("Fatores de coerência segundo Koch", 
         "**Conhecimento linguístico, enciclopédico, interacional, situacional, continuidade, progressão, não-contradição, articulação**"),
        
        ("Como se manifesta a coesão referencial?", 
         "**Anáfora:** retoma elemento anterior<br>**Catáfora:** antecipa elemento posterior<br>**Pronominal, nominal, verbal, adverbial**"),
        
        # Léxico
        ("Diferença entre sinônimos e antônimos?", 
         "**Sinônimos:** palavras de sentido semelhante (casa/lar)<br>**Antônimos:** sentido oposto (quente/frio). Podem ser graduais, complementares ou conversos"),
        
        ("O que são parônimos e homônimos?", 
         "**Parônimos:** grafia/som semelhantes, sentidos diferentes (ratificar/retificar)<br>**Homônimos:** mesma grafia/som, sentidos diferentes (banco/banco)"),
        
        ("Tipos de homônimos", 
         "**Perfeitos:** grafia e som iguais (canto/canto)<br>**Homógrafos:** grafia igual (colher/colher)<br>**Homófonos:** som igual (cessão/seção)"),
        
        ("Como funciona a substituição lexical?", 
         "**Sinonímia, hiperonímia/hiponímia, meronímia, metáfora, metonímia** para evitar repetição e criar coesão lexical"),
        
        ("Relações semânticas entre palavras", 
         "**Campo semântico:** palavras relacionadas por tema<br>**Família lexical:** mesma raiz<br>**Polissemia:** múltiplos sentidos<br>**Ambiguidade:** duplo sentido"),
        
        # Ortografia - Acordo Ortográfico
        ("Principais mudanças do Acordo Ortográfico", 
         "**Trema:** eliminado (exceto nomes próprios)<br>**Hífen:** novas regras<br>**Acentos:** eliminação de alguns casos<br>**Letras k, w, y:** oficializadas"),
        
        ("Regras de acentuação pós-Acordo", 
         "**Oxítonas:** a(s), e(s), o(s), em, ens<br>**Paroxítonas:** não terminadas em a,e,o,am,em,ens<br>**Proparoxítonas:** todas acentuadas"),
        
        ("Uso do hífen - regras gerais", 
         "**Prefixo + palavra iniciada por h:** anti-higiênico<br>**Vogal igual:** micro-ondas<br>**Sub, sob, ad:** quando palavra inicia por r"),
        
        ("Emprego das letras - casos especiais", 
         "**G/J:** viagem(substantivo)/viajem(verbo)<br>**S/Z:** análise/analisar<br>**X/CH:** enxergar/charque<br>**SC/SÇ:** crescer/cresça"),
        
        ("Regras de emprego de maiúsculas", 
         "**Início de frase, nomes próprios, títulos, siglas, após dois pontos (em citações), pronomes de tratamento**"),
        
        # Figuras de Linguagem - Bechara, Cegalla, Cunha/Cintra
        ("Figuras de linguagem - classificação geral", 
         "**Sintaxe:** elipse, zeugma, hipérbato, pleonasmo<br>**Semântica:** metáfora, metonímia, catacrese<br>**Fonética:** aliteração, assonância<br>**Pensamento:** antítese, paradoxo"),
        
        ("Principais figuras de sintaxe", 
         "**Elipse:** omissão<br>**Zeugma:** omissão de termo já expresso<br>**Hipérbato:** inversão<br>**Pleonasmo:** redundância<br>**Anacoluto:** quebra sintática"),
        
        ("Principais figuras de semântica", 
         "**Metáfora:** comparação implícita<br>**Metonímia:** substituição por contiguidade<br>**Catacrese:** metáfora cristalizada<br>**Sinestesia:** mistura de sensações"),
        
        ("Figuras de pensamento principais", 
         "**Antítese:** oposição<br>**Paradoxo:** contradição aparente<br>**Ironia:** sentido contrário<br>**Hipérbole:** exagero<br>**Eufemismo:** suavização"),
        
        ("Como as figuras criam efeitos de sentido?", 
         "**Expressividade, ênfase, poeticidade, persuasão**. Desvio da norma padrão para criar impacto emocional ou estético"),
        
        # Fonologia - Bechara, Cegalla, Cunha/Cintra
        ("Diferença entre fonema e letra", 
         "**Fonema:** som da fala<br>**Letra/grafema:** representação gráfica. Nem sempre correspondem (casa = 4 letras, 4 fonemas; hora = 4 letras, 3 fonemas)"),
        
        ("Classificação dos fonemas", 
         "**Vogais:** a,e,i,o,u (base das sílabas)<br>**Semivogais:** i,u átonos em ditongos<br>**Consoantes:** demais sons, articulados com obstáculo"),
        
        ("Encontros vocálicos", 
         "**Ditongo:** vogal + semivogal (pai)<br>**Tritongo:** semivogal + vogal + semivogal (Paraguai)<br>**Hiato:** vogais em sílabas diferentes (saída)"),
        
        ("Encontros consonantais", 
         "**Perfeitos:** mesma sílaba (pra-to)<br>**Imperfeitos:** sílabas diferentes (ap-to)<br>**Dígrafos:** duas letras, um som (ch, lh, nh)"),
        
        ("Relação fonema-grafia - casos especiais", 
         "**Som /s/:** s, ss, ç, sc, sç, xc, x<br>**Som /z/:** z, s, x<br>**Som /ʃ/:** x, ch, s<br>**Som /k/:** c, qu, k"),
        
        # Morfologia - Classes de Palavras
        ("Classes de palavras - variáveis", 
         "**Substantivo, adjetivo, pronome, numeral, artigo, verbo** - sofrem flexões de gênero, número, pessoa, tempo, modo"),
        
        ("Classes de palavras - invariáveis", 
         "**Advérbio, preposição, conjunção, interjeição** - não sofrem flexões"),
        
        ("Flexões do substantivo", 
         "**Gênero:** masculino/feminino<br>**Número:** singular/plural<br>**Grau:** aumentativo/diminutivo (sintético/analítico)"),
        
        ("Flexões do adjetivo", 
         "**Gênero/Número:** concordância com substantivo<br>**Grau:** comparativo (igualdade/superioridade/inferioridade), superlativo (absoluto/relativo)"),
        
        ("Classificação dos pronomes", 
         "**Pessoais:** retos, oblíquos, tratamento<br>**Possessivos, demonstrativos, indefinidos, interrogativos, relativos**"),
        
        ("Flexões verbais", 
         "**Modo:** indicativo, subjuntivo, imperativo<br>**Tempo:** presente, pretérito, futuro<br>**Pessoa/Número:** 1ª,2ª,3ª sing/plural<br>**Voz:** ativa, passiva, reflexiva"),
        
        ("Formação de palavras", 
         "**Derivação:** prefixal, sufixal, parassintética, regressiva, imprópria<br>**Composição:** justaposição, aglutinação<br>**Outros:** hibridismo, onomatopeia"),
        
        ("Vozes verbais e conversão", 
         "**Ativa:** sujeito pratica ação<br>**Passiva:** sujeito sofre ação (analítica: ser+particípio; sintética: verbo+se)<br>**Reflexiva:** sujeito pratica e sofre"),
        
        # Sintaxe - Funções Sintáticas
        ("Termos essenciais da oração", 
         "**Sujeito:** ser de quem se declara algo<br>**Predicado:** declaração sobre o sujeito<br>Tipos de sujeito: simples, composto, oculto, indeterminado, inexistente"),
        
        ("Tipos de predicado", 
         "**Nominal:** verbo de ligação + predicativo<br>**Verbal:** verbo intransitivo ou transitivo<br>**Verbo-nominal:** verbo + predicativo"),
        
        ("Termos integrantes da oração", 
         "**Objeto direto/indireto:** complementos verbais<br>**Complemento nominal:** complementa substantivo, adjetivo, advérbio<br>**Agente da passiva:** pratica ação na voz passiva"),
        
        ("Termos acessórios da oração", 
         "**Adjunto adnominal:** modifica substantivo<br>**Adjunto adverbial:** modifica verbo, adjetivo, advérbio<br>**Aposto:** explica termo anterior<br>**Vocativo:** chamamento"),
        
        ("Período composto - coordenação", 
         "**Sindéticas:** com conjunção (aditivas, adversativas, alternativas, conclusivas, explicativas)<br>**Assindéticas:** sem conjunção"),
        
        ("Período composto - subordinação", 
         "**Substantivas:** função de substantivo (subjetiva, objetiva, completiva)<br>**Adjetivas:** função de adjetivo (restritiva/explicativa)<br>**Adverbiais:** função de advérbio"),
        
        # Regência Nominal e Verbal
        ("O que é regência?", 
         "**Relação de dependência** entre termos. Termo regente exige complemento (termo regido) com ou sem preposição"),
        
        ("Regência verbal - verbos transitivos", 
         "**Diretos:** sem preposição (amar alguém)<br>**Indiretos:** com preposição (gostar de algo)<br>**Diretos e indiretos:** dois complementos"),
        
        ("Casos especiais de regência verbal", 
         "**Assistir:** ver (a), ajudar (sem prep.)<br>**Aspirar:** respirar (sem prep.), desejar (a)<br>**Visar:** mirar (sem prep.), objetivar (a)"),
        
        ("Regência nominal - principais casos", 
         "**Adjacente a:** junto<br>**Apto para/a:** capaz<br>**Compatível com:** adequado<br>**Imune a/de:** protegido<br>**Paralelo a:** simultâneo"),
        
        ("Emprego da crase", 
         "**A + A:** preposição + artigo/pronome<br>**Obrigatória:** palavra feminina que pede artigo e termo regente pede preposição<br>**Proibida:** antes de masculino, plural, verbo, pronomes"),
        
        ("Casos especiais de crase", 
         "**Facultativa:** antes de nome próprio feminino, pronome possessivo feminino<br>**Locução:** à moda de, à maneira de, às vezes<br>**Horário:** às duas horas"),
        
        # Concordância Verbal e Nominal
        ("Concordância verbal - regra geral", 
         "**Verbo concorda com o sujeito** em pessoa e número. Sujeito simples: concordância obrigatória"),
        
        ("Concordância com sujeito composto", 
         "**Antes do verbo:** plural<br>**Depois do verbo:** plural ou singular (com núcleo mais próximo)<br>**Pessoas diferentes:** prevalece 1ª sobre 2ª e 3ª"),
        
        ("Casos especiais de concordância verbal", 
         "**Coletivo:** singular<br>**%:** concorda com numeral<br>**Mais de:** plural<br>**Um dos que:** plural<br>**Horas/distância:** plural"),
        
        ("Concordância nominal - regra geral", 
         "**Artigo, adjetivo, numeral, pronome** concordam em gênero e número com substantivo"),
        
        ("Casos especiais de concordância nominal", 
         "**Um adjetivo + vários substantivos:** masculino plural ou com mais próximo<br>**Vários substantivos + um adjetivo:** masculino plural<br>**É bom/é necessário:** invariável sem artigo"),
        
        # Colocação Pronominal
        ("Regras de colocação pronominal", 
         "**Próclise:** antes do verbo (com palavras atrativas)<br>**Ênclise:** depois do verbo (início de frase)<br>**Mesóclise:** meio do verbo (futuro sem atração)"),
        
        ("Palavras que atraem próclise", 
         "**Palavras negativas, pronomes relativos/indefinidos/interrogativos, conjunções subordinativas, advérbios**"),
        
        ("Colocação em locuções verbais", 
         "**Auxiliar + principal:** próclise ao auxiliar ou ênclise ao principal<br>**Com palavra atrativa:** próclise obrigatória ao auxiliar"),
        
        # Conjunções e Pronomes Relativos
        ("Classificação das conjunções coordenativas", 
         "**Aditivas:** e, nem<br>**Adversativas:** mas, porém<br>**Alternativas:** ou<br>**Conclusivas:** logo, portanto<br>**Explicativas:** que, porque"),
        
        ("Classificação das conjunções subordinativas", 
         "**Integrantes:** que, se<br>**Causais:** porque, como<br>**Concessivas:** embora, ainda que<br>**Condicionais:** se, caso<br>**Temporais:** quando, enquanto"),
        
        ("Pronomes relativos - emprego", 
         "**Que:** universal<br>**Qual:** com preposição<br>**Quem:** pessoa<br>**Onde:** lugar<br>**Cujo:** posse<br>**Quanto:** após tanto/todo"),
        
        # Pontuação
        ("Uso da vírgula - regras principais", 
         "**Separar:** elementos de série, vocativo, aposto, adjuntos deslocados<br>**Isolar:** expressões explicativas, orações adjetivas explicativas"),
        
        ("Vírgula - casos proibidos", 
         "**Não separar:** sujeito do predicado, verbo do objeto direto, nome do complemento, termos ligados por preposição essencial"),
        
        ("Uso do ponto e vírgula", 
         "**Separar:** orações coordenadas longas, itens de enumeração complexa, orações com vírgulas internas"),
        
        ("Uso dos dois pontos", 
         "**Introduzir:** citação, enumeração, explicação, consequência<br>**Após verbos dicendi:** ele disse: \"...\""),
        
        ("Uso das aspas", 
         "**Marcar:** citações, estrangeirismos, gírias, ironia, títulos<br>**Destacar:** palavras ou expressões especiais"),
        
        ("Uso do travessão", 
         "**Diálogo:** indicar fala<br>**Aposto/explicação:** isolar termos (substitui vírgula ou parênteses)<br>**Ênfase:** destacar elemento"),
        
        # Análise Textual Avançada
        ("Estratégias de leitura para concursos", 
         "**1ª leitura:** geral, tema, gênero<br>**2ª leitura:** detalhada, argumentos<br>**Marcação:** palavras-chave, conectivos<br>**Síntese:** ideias principais"),
        
        ("Como identificar tese e argumentos", 
         "**Tese:** posição defendida (geralmente início/fim)<br>**Argumentos:** razões que sustentam (conectores: porque, pois, já que)<br>**Contra-argumentos:** refutação"),
        
        ("Análise da progressão textual", 
         "**Tema/rema:** informação conhecida/nova<br>**Progressão:** linear, constante, derivada<br>**Conectores:** articulam relações lógicas"),
        
        ("Identificação de pressupostos", 
         "**Marcadores:** verbos (parar = estava fazendo), advérbios (ainda = continuidade), adjetivos (outro = existe um)"),
        
        ("Efeitos de sentido - análise", 
         "**Escolhas lexicais:** conotação, registro<br>**Estrutura sintática:** ordem, ênfase<br>**Figuras:** expressividade<br>**Pontuação:** ritmo, ênfase")
    ]
    
    # Criar database temporário
    db_path = "collection_portugues.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criar tabelas necessárias para o Anki
    cursor.execute('''
        CREATE TABLE col (
            id INTEGER PRIMARY KEY,
            crt INTEGER NOT NULL,
            mod INTEGER NOT NULL,
            scm INTEGER NOT NULL,
            ver INTEGER NOT NULL,
            dty INTEGER NOT NULL,
            usn INTEGER NOT NULL,
            ls INTEGER NOT NULL,
            conf TEXT NOT NULL,
            models TEXT NOT NULL,
            decks TEXT NOT NULL,
            dconf TEXT NOT NULL,
            tags TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY,
            guid TEXT NOT NULL UNIQUE,
            mid INTEGER NOT NULL,
            mod INTEGER NOT NULL,
            usn INTEGER NOT NULL,
            tags TEXT NOT NULL,
            flds TEXT NOT NULL,
            sfld TEXT NOT NULL,
            csum INTEGER NOT NULL,
            flags INTEGER NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE cards (
            id INTEGER PRIMARY KEY,
            nid INTEGER NOT NULL,
            did INTEGER NOT NULL,
            ord INTEGER NOT NULL,
            mod INTEGER NOT NULL,
            usn INTEGER NOT NULL,
            type INTEGER NOT NULL,
            queue INTEGER NOT NULL,
            due INTEGER NOT NULL,
            ivl INTEGER NOT NULL,
            factor INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            lapses INTEGER NOT NULL,
            left INTEGER NOT NULL,
            odue INTEGER NOT NULL,
            odid INTEGER NOT NULL,
            flags INTEGER NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE revs (
            id INTEGER PRIMARY KEY,
            cid INTEGER NOT NULL,
            usn INTEGER NOT NULL,
            ease INTEGER NOT NULL,
            ivl INTEGER NOT NULL,
            lastIvl INTEGER NOT NULL,
            factor INTEGER NOT NULL,
            time INTEGER NOT NULL,
            type INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE graves (
            usn INTEGER NOT NULL,
            oid INTEGER NOT NULL,
            type INTEGER NOT NULL
        )
    ''')
    
    # Timestamps
    current_time = int(time.time())
    
    # Configuração da coleção
    col_config = {
        "nextPos": 1,
        "estTimes": True,
        "activeDecks": [1],
        "sortType": "noteFld",
        "timeLim": 0,
        "sortBackwards": False,
        "addToCur": True,
        "curDeck": 1,
        "newBury": True,
        "newSpread": 0,
        "dueCounts": True,
        "curModel": str(current_time),
        "collapseTime": 1200
    }
    
    # Modelo de cartão
    model = {
        "sortf": 0,
        "did": 1,
        "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
        "latexPost": "\\end{document}",
        "mod": current_time,
        "usn": 0,
        "vers": [],
        "type": 0,
        "css": ".card {\n font-family: arial;\n font-size: 18px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\n.front {\n background-color: #f0fff0;\n}\n\n.back {\n background-color: #fff5ee;\n}",
        "name": "Língua Portuguesa",
        "flds": [
            {
                "name": "Frente",
                "media": [],
                "sticky": False,
                "rtl": False,
                "ord": 0,
                "font": "Arial",
                "size": 18
            },
            {
                "name": "Verso",
                "media": [],
                "sticky": False,
                "rtl": False,
                "ord": 1,
                "font": "Arial",
                "size": 18
            }
        ],
        "tmpls": [
            {
                "name": "Cartão 1",
                "ord": 0,
                "qfmt": '<div class="front">{{Frente}}</div>',
                "afmt": '<div class="back">{{Frente}}<hr id="answer">{{Verso}}</div>',
                "did": None,
                "bqfmt": "",
                "bafmt": ""
            }
        ],
        "tags": [],
        "id": str(current_time),
        "req": [[0, "any", [0]]]
    }
    
    models = {str(current_time): model}
    
    # Deck
    deck = {
        "desc": "Deck de Língua Portuguesa - Interpretação, Gramática, Sintaxe e Análise Textual",
        "name": "Língua Portuguesa",
        "extendRev": 50,
        "usn": 0,
        "collapsed": False,
        "newToday": [0, 0],
        "timeToday": [0, 0],
        "dyn": 0,
        "extendNew": 10,
        "conf": 1,
        "revToday": [0, 0],
        "lrnToday": [0, 0],
        "id": 1,
        "mod": current_time
    }
    
    decks = {"1": deck}
    
    # Configuração de deck
    deck_config = {
        "name": "Default",
        "replayq": True,
        "lapse": {
            "leechFails": 8,
            "mins": [10],
            "leechAction": 0,
            "mult": 0
        },
        "rev": {
            "perDay": 100,
            "ease4": 1.3,
            "fuzz": 0.05,
            "minSpace": 1,
            "ivlFct": 1,
            "maxIvl": 36500,
            "ease2": 1.2,
            "bury": True,
            "hardFactor": 1.2
        },
        "timer": 0,
        "maxTaken": 60,
        "usn": 0,
        "new": {
            "perDay": 20,
            "delays": [1, 10],
            "separate": True,
            "ints": [1, 4, 7],
            "initialFactor": 2500,
            "bury": True,
            "order": 1
        },
        "mod": 0,
        "id": 1,
        "autoplay": True
    }
    
    deck_configs = {"1": deck_config}
    
    # Inserir dados da coleção
    cursor.execute('''
        INSERT INTO col VALUES (
            1, ?, ?, ?, 11, 0, 0, ?, ?, ?, ?, ?, ''
        )
    ''', (
        current_time,  # crt
        current_time,  # mod
        current_time,  # scm
        current_time,  # ls
        json.dumps(col_config),  # conf
        json.dumps(models),  # models
        json.dumps(decks),  # decks
        json.dumps(deck_configs)  # dconf
    ))
    
    # Inserir notas e cartões
    for i, (front, back) in enumerate(cards_data):
        note_id = current_time + i + 1
        card_id = current_time + i + 1
        
        # Calcular checksum simples
        fields_text = f"{front}\x1f{back}"
        checksum = sum(ord(c) for c in fields_text) % 2**31
        
        # Inserir nota
        cursor.execute('''
            INSERT INTO notes VALUES (
                ?, ?, ?, ?, 0, '', ?, ?, ?, 0, ''
            )
        ''', (
            note_id,
            f"note_{note_id}",  # guid
            int(model["id"]),  # mid
            current_time,  # mod
            fields_text,  # flds
            front,  # sfld (primeiro campo)
            checksum  # csum
        ))
        
        # Inserir cartão
        cursor.execute('''
            INSERT INTO cards VALUES (
                ?, ?, 1, 0, ?, 0, 0, 0, ?, 0, 2500, 0, 0, 0, 0, 0, 0, ''
            )
        ''', (
            card_id,
            note_id,
            current_time,
            i + 1  # due
        ))
    
    conn.commit()
    conn.close()
    
    # Criar arquivo .apkg (zip com database)
    apkg_path = "Lingua_Portuguesa.apkg"
    with zipfile.ZipFile(apkg_path, 'w', zipfile.ZIP_DEFLATED) as apkg:
        apkg.write(db_path, "collection.db")
        
        # Adicionar arquivo de mídia vazio
        apkg.writestr("media", "{}")
    
    # Limpar arquivo temporário
    os.remove(db_path)
    
    print(f"Deck de Língua Portuguesa criado com sucesso: {apkg_path}")
    print(f"Total de cartões: {len(cards_data)}")
    return apkg_path

if __name__ == "__main__":
    create_portugues_deck()
