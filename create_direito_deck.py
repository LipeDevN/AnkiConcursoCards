import sqlite3
import zipfile
import json
import time
import os
from datetime import datetime

def create_direito_deck():
    """
    Cria um deck do Anki (.apkg) com as matérias de Direito
    """
    
    # Dados dos cartões - Frente e Verso
    cards_data = [
        # Constituição Federal - Princípios Fundamentais
        ("Quais são os fundamentos da República Federativa do Brasil (Art. 1º)?", 
         "I - soberania;<br>II - cidadania;<br>III - dignidade da pessoa humana;<br>IV - valores sociais do trabalho e da livre iniciativa;<br>V - pluralismo político"),
        
        ("Qual a forma de governo e sistema político do Brasil (Art. 1º)?", 
         "**República Federativa** constituída em união indissolúvel dos Estados, Municípios e Distrito Federal, **Estado Democrático de Direito**"),
        
        ("De onde emana todo poder segundo a CF/88 (Art. 1º)?", 
         "Todo poder emana do **povo**, que o exerce por meio de representantes eleitos ou **diretamente**, nos termos da Constituição"),
        
        ("Quais são os objetivos fundamentais da República (Art. 3º)?", 
         "I - construir sociedade livre, justa e solidária;<br>II - garantir desenvolvimento nacional;<br>III - erradicar pobreza e marginalização;<br>IV - promover bem de todos, sem discriminação"),
        
        ("Como o Brasil se relaciona internacionalmente (Art. 4º)?", 
         "**Princípios:** independência nacional, prevalência dos direitos humanos, autodeterminação dos povos, não-intervenção, igualdade entre Estados, defesa da paz, solução pacífica de conflitos, repúdio ao terrorismo e racismo"),
        
        # Direitos e Garantias Fundamentais
        ("Quais são os direitos fundamentais no caput do Art. 5º?", 
         "**Vida, liberdade, igualdade, segurança e propriedade** são invioláveis para brasileiros e estrangeiros residentes no País"),
        
        ("O que significa o princípio da igualdade (Art. 5º)?", 
         "Todos são **iguais perante a lei**, sem distinção de qualquer natureza. **Igualdade formal** (perante a lei) e **material** (tratamento desigual para situações desiguais)"),
        
        ("Quando a casa é asilo inviolável (Art. 5º, XI)?", 
         "**Durante o dia:** somente com consentimento do morador ou ordem judicial<br>**Durante a noite:** somente com consentimento do morador<br>**Exceção:** flagrante delito ou desastre"),
        
        ("O que são os remédios constitucionais?", 
         "**Habeas Corpus:** liberdade de locomoção<br>**Habeas Data:** informações pessoais<br>**Mandado de Segurança:** direito líquido e certo<br>**Mandado de Injunção:** norma regulamentadora<br>**Ação Popular:** patrimônio público"),
        
        ("Quais são os direitos sociais (Art. 6º)?", 
         "**Educação, saúde, alimentação, trabalho, moradia, transporte, lazer, segurança, previdência social, proteção à maternidade e à infância, assistência aos desamparados**"),
        
        ("Principais direitos dos trabalhadores (Art. 7º)", 
         "**Salário mínimo, 13º salário, férias, FGTS, seguro-desemprego, licença maternidade/paternidade, jornada de 8h diárias e 44h semanais, adicional noturno, adicional de periculosidade**"),
        
        ("O que é direito de greve (Art. 9º)?", 
         "É assegurado o **direito de greve**, competindo aos trabalhadores decidir sobre oportunidade de exercê-lo e sobre os interesses que devam por meio dele defender"),
        
        # Organização do Estado
        ("Como se organiza politicamente a República Federativa do Brasil (Art. 18)?", 
         "União, Estados, Distrito Federal e Municípios, todos **autônomos**, nos termos da Constituição"),
        
        ("Quais são os bens da União (Art. 20)?", 
         "**Terras devolutas, lagos/rios/águas, ilhas fluviais/lacustres, praias, mar territorial, recursos minerais, cavidades naturais subterrâneas**"),
        
        ("O que compete privativamente à União (Art. 22)?", 
         "**Direito civil, comercial, penal, processual, eleitoral, aeronáutico, espacial, do trabalho; desapropriação; águas, energia, telecomunicações; sistema monetário**"),
        
        ("O que é competência comum (Art. 23)?", 
         "União, Estados, DF e Municípios têm competência comum para: **saúde, educação, cultura, meio ambiente, patrimônio histórico, assistência pública**"),
        
        ("O que compete aos Estados (Art. 25)?", 
         "Competências **remanescentes** (não privativas da União nem dos Municípios). Podem incorporar-se entre si, subdividir-se ou desmembrar-se"),
        
        ("O que compete aos Municípios (Art. 30)?", 
         "**Assuntos de interesse local, suplementar legislação federal/estadual, transporte local, organizar e prestar serviços públicos locais**"),
        
        # Organização dos Poderes
        ("Como são organizados os Poderes da União (Art. 2º)?", 
         "**Legislativo, Executivo e Judiciário**, independentes e harmônicos entre si"),
        
        ("Como se compõe o Poder Legislativo (Art. 44)?", 
         "**Congresso Nacional:** Câmara dos Deputados (513 deputados, 4 anos) + Senado Federal (81 senadores, 8 anos)"),
        
        ("Quais são as funções típicas do Congresso Nacional (Art. 48)?", 
         "**Legislar** sobre as matérias de competência da União e **fiscalizar** os atos do Poder Executivo"),
        
        ("Quais são as competências exclusivas do Congresso (Art. 49)?", 
         "**Aprovar tratados, autorizar guerra/paz, fixar efetivos das Forças Armadas, aprovar estado de defesa/sítio, sustar atos normativos exorbitantes**"),
        
        ("O que é o processo legislativo ordinário?", 
         "**Iniciativa → Discussão → Votação → Sanção/Veto → Promulgação → Publicação**<br>Casa iniciadora → Casa revisora → Presidente da República"),
        
        ("Quem pode iniciar leis (Art. 61)?", 
         "**Deputado, Senador, Comissões, Presidente da República, STF, Tribunais Superiores, PGR, cidadãos (iniciativa popular)**"),
        
        ("Como funciona o veto presidencial (Art. 66)?", 
         "**15 dias** para sancionar ou vetar. Veto pode ser **total ou parcial**. Congresso pode **derrubar o veto** por maioria absoluta em sessão conjunta"),
        
        ("Quais são os crimes de responsabilidade do Presidente (Art. 85)?", 
         "Atos que **atentem contra a Constituição** e, especialmente, contra: existência da União, livre exercício dos Poderes, exercício dos direitos políticos, segurança interna, probidade administrativa, lei orçamentária, decreto judicial"),
        
        ("Como funciona o processo de impeachment?", 
         "**Câmara autoriza** (2/3) → **Senado julga** (2/3) → **Presidente do STF preside**<br>Perda do cargo + inabilitação para funções públicas por 8 anos"),
        
        ("Quais são os Ministérios de Estado?", 
         "**Auxiliares diretos** do Presidente. Requisitos: brasileiro nato/naturalizado, maior de 21 anos, exercício direitos políticos"),
        
        ("Como se organiza o Poder Judiciário (Art. 92)?", 
         "**STF, CNJ, STJ, TST, TSE, STM, TRFs, TRTs, TREs, TJs, TJMs**"),
        
        ("Quais são as competências do STF (Art. 102)?", 
         "**Guarda da Constituição**<br>**Originária:** ADI, ADC, ADPF, crimes de autoridades<br>**Recursal:** RE quando há questão constitucional"),
        
        ("O que é súmula vinculante?", 
         "**Súmula aprovada por 2/3 do STF**, após reiteradas decisões sobre matéria constitucional, com **efeito vinculante** para demais órgãos do Judiciário e Administração"),
        
        # Defesa do Estado e Instituições Democráticas
        ("O que é estado de defesa (Art. 136)?", 
         "**Decreto do Presidente** para preservar/restabelecer ordem pública/paz social ameaçadas por instabilidade institucional. **Localização restrita, prazo máximo 30 dias, prorrogável por mais 30**"),
        
        ("O que é estado de sítio (Art. 137)?", 
         "**Comoção grave** ou **ineficácia do estado de defesa** ou **declaração de guerra/agressão estrangeira**. Decreto após autorização do Congresso"),
        
        ("Quais são as Forças Armadas (Art. 142)?", 
         "**Exército, Marinha e Aeronáutica**. Destinam-se à **defesa da Pátria, garantia dos poderes constitucionais e, por iniciativa destes, da lei e da ordem**"),
        
        ("Quais são os órgãos de segurança pública (Art. 144)?", 
         "**Polícia Federal, Rodoviária Federal, Ferroviária Federal, Civis, Militares e Corpos de Bombeiros Militares**"),
        
        ("Qual a função da Polícia Federal?", 
         "**Crimes contra a ordem política/social, crimes interestaduais/internacionais, tráfico de drogas, contrabando, crimes contra bens da União**"),
        
        # Ordem Social
        ("Qual o objetivo da ordem social (Art. 193)?", 
         "Tem como **base o primado do trabalho** e como **objetivo o bem-estar e a justiça sociais**"),
        
        ("Quais são os princípios da seguridade social (Art. 194)?", 
         "**Universalidade, uniformidade, seletividade, irredutibilidade, equidade, diversidade da base de financiamento**"),
        
        ("Como se divide a seguridade social?", 
         "**Saúde** (universal e gratuita)<br>**Previdência** (contributiva)<br>**Assistência Social** (independe de contribuição)"),
        
        ("Princípios do SUS (Art. 198)", 
         "**Descentralização, atendimento integral, participação da comunidade**"),
        
        ("Quais são os princípios da educação?", 
         "**Igualdade, liberdade, pluralismo, gratuidade do ensino público, valorização dos profissionais, gestão democrática, padrão de qualidade**"),
        
        ("Como se organiza o ensino no Brasil?", 
         "**União:** ensino superior, normas gerais<br>**Estados/DF:** ensino fundamental e médio<br>**Municípios:** educação infantil e fundamental"),
        
        # Constituição Estadual RS
        ("Quais são os princípios fundamentais do RS?", 
         "**Cidadania, dignidade humana, valores sociais do trabalho, livre iniciativa, pluralismo político**. Estado democrático de direito"),
        
        ("Como se organiza administrativamente o RS?", 
         "**Estado unitário** dividido em **Regiões Funcionais de Planejamento** para descentralização administrativa"),
        
        ("Quais são os símbolos do RS?", 
         "**Bandeira, Brasão, Hino**. Lei estadual pode criar outros símbolos"),
        
        ("Como funciona a Assembleia Legislativa do RS?", 
         "**55 deputados estaduais**, mandato de 4 anos, pode ser reeleito. Mesa Diretora renovada a cada 2 anos"),
        
        ("Quais são os direitos sociais específicos do RS?", 
         "**Educação, saúde, trabalho, moradia, transporte, segurança, previdência social, lazer, maternidade, infância, assistência aos desamparados**"),
        
        # Lei de Improbidade Administrativa
        ("O que é improbidade administrativa (Lei 8.429/92)?", 
         "**Atos desonestos** que violam princípios da Administração Pública, causando **lesão ao patrimônio público** ou **enriquecimento ilícito**"),
        
        ("Quais são os tipos de atos de improbidade?", 
         "**Tipo I:** Enriquecimento ilícito<br>**Tipo II:** Dano ao erário<br>**Tipo III:** Violação aos princípios (incluindo lesão à moralidade, impessoalidade, legalidade, lealdade às instituições)"),
        
        ("Quais são as sanções por improbidade?", 
         "**Perda da função, suspensão dos direitos políticos, multa civil, proibição de contratar com o Poder Público, ressarcimento ao erário**"),
        
        ("Qual o prazo prescricional da ação de improbidade?", 
         "**8 anos** após o término do exercício de mandato, de cargo em comissão ou de função de confiança"),
        
        ("Quem pode propor ação de improbidade?", 
         "**Ministério Público** ou **pessoa jurídica interessada**. Qualquer pessoa pode **representar** à autoridade administrativa ou ao MP"),
        
        # Lei Maria da Penha
        ("O que é violência doméstica segundo a Lei Maria da Penha?", 
         "Qualquer ação ou omissão baseada no **gênero** que cause **morte, lesão, sofrimento físico, sexual ou psicológico** e dano moral ou patrimonial"),
        
        ("Quais são os tipos de violência doméstica?", 
         "**Física:** ofensas à integridade corporal<br>**Psicológica:** dano emocional<br>**Sexual:** constrangimento sexual<br>**Patrimonial:** danos aos bens<br>**Moral:** calúnia, difamação, injúria"),
        
        ("Quais são as medidas protetivas de urgência?", 
         "**Afastamento do agressor, proibição de aproximação/contato, suspensão do porte de armas, prestação de alimentos provisórios**"),
        
        ("Como funciona o atendimento à mulher vítima?", 
         "**Atendimento multidisciplinar** (assistência social, jurídica, médica, psicológica). **Política pública de prevenção**"),
        
        ("Principais inovações da Lei Maria da Penha", 
         "**Criação dos Juizados de Violência Doméstica, medidas protetivas, equipe multidisciplinar, não aplicação da Lei 9.099/95**"),
        
        # Estatuto da Igualdade Racial
        ("O que é o Estatuto da Igualdade Racial (Lei 12.288/10)?", 
         "Conjunto de **medidas antidiscriminatórias** destinadas a assegurar à **população negra** efetivação da igualdade de oportunidades"),
        
        ("O que são ações afirmativas segundo o Estatuto?", 
         "**Programas e medidas especiais** adotados pelo Estado e pela iniciativa privada para **corrigir desigualdades raciais** e promover igualdade de oportunidades"),
        
        ("Quais são os direitos fundamentais da população negra?", 
         "**Saúde, educação, cultura, esporte, lazer, trabalho, moradia, meios de comunicação, acesso à justiça, outros direitos**"),
        
        ("Como funciona o acesso ao ensino superior?", 
         "**Reserva de vagas** em universidades públicas e **programas de financiamento** estudantil para população negra"),
        
        ("O que são comunidades quilombolas?", 
         "**Grupos étnico-raciais** com trajetória histórica própria, relações territoriais específicas e **ancestralidade negra** relacionada à resistência à opressão"),
        
        # Estatuto da Pessoa Idosa
        ("Quem é considerado idoso (Lei 10.741/03)?", 
         "**Pessoa com idade igual ou superior a 60 anos**"),
        
        ("Quais são os direitos fundamentais do idoso?", 
         "**Vida, liberdade, dignidade, alimentos, saúde, educação, cultura, esporte, lazer, profissionalização, trabalho, previdência, assistência social, habitação, transporte**"),
        
        ("Como funciona a prioridade no atendimento?", 
         "**Prioridade absoluta** na elaboração e execução de políticas públicas. **Atendimento preferencial** em órgãos públicos e privados"),
        
        ("O que são crimes contra o idoso?", 
         "**Discriminação, abandono, exposição a perigo, apropriação de bens, coação**. Penas aumentadas quando vítima é idosa"),
        
        ("Quais são as medidas de proteção ao idoso?", 
         "**Encaminhamento aos pais/responsável, orientação/apoio/acompanhamento temporários, matrícula obrigatória em escola, tratamento especializado**"),
        
        # Estatuto da Criança e Adolescente
        ("Quem são criança e adolescente segundo o ECA?", 
         "**Criança:** até 12 anos incompletos<br>**Adolescente:** entre 12 e 18 anos"),
        
        ("Qual é o princípio fundamental do ECA?", 
         "**Proteção integral** e **prioridade absoluta**. Crianças e adolescentes são **sujeitos de direitos**"),
        
        ("Quais são os direitos fundamentais?", 
         "**Vida, saúde, liberdade, dignidade, convivência familiar, educação, cultura, esporte, lazer, profissionalização, proteção no trabalho**"),
        
        ("O que é o Sistema de Garantia de Direitos?", 
         "**Conselho Tutelar, Conselhos de Direitos, Ministério Público, Defensoria Pública, Poder Judiciário**"),
        
        ("Quais são as medidas socioeducativas?", 
         "**Advertência, obrigação de reparar o dano, prestação de serviços à comunidade, liberdade assistida, semiliberdade, internação**"),
        
        ("O que são medidas de proteção?", 
         "**Encaminhamento aos pais, orientação/apoio/acompanhamento, matrícula em escola, inclusão em programa oficial, requisição de tratamento**"),
        
        # LGPD
        ("O que é a LGPD (Lei 13.709/18)?", 
         "Lei que regula **tratamento de dados pessoais** por pessoa natural ou jurídica de direito público ou privado"),
        
        ("O que são dados pessoais?", 
         "**Informação relacionada a pessoa natural identificada ou identificável**"),
        
        ("O que são dados pessoais sensíveis?", 
         "**Origem racial/étnica, convicção religiosa, opinião política, saúde, vida sexual, dado genético/biométrico**"),
        
        ("Quais são os princípios da LGPD?", 
         "**Finalidade, adequação, necessidade, livre acesso, qualidade dos dados, transparência, segurança, prevenção, não discriminação, responsabilização**"),
        
        ("Quais são as bases legais para tratamento?", 
         "**Consentimento, cumprimento de obrigação legal, execução de políticas públicas, estudos por órgão de pesquisa, execução de contrato, exercício regular de direitos, proteção da vida, tutela da saúde, interesse legítimo, proteção do crédito**"),
        
        ("Quais são os direitos do titular?", 
         "**Confirmação, acesso, correção, anonimização/bloqueio/eliminação, portabilidade, informação sobre compartilhamento, revogação do consentimento**"),
        
        ("O que é a ANPD?", 
         "**Autoridade Nacional de Proteção de Dados** - órgão da administração pública federal que faz parte da Presidência da República"),
        
        ("Quais são as sanções da LGPD?", 
         "**Advertência, multa simples (até 2% do faturamento, limitada a R$ 50 milhões), multa diária, publicização da infração, bloqueio dos dados, eliminação dos dados**"),
        
        # Decreto Estadual 48.598/2011
        ("O que dispõe o Decreto 48.598/2011?", 
         "**Inclusão da temática de gênero, raça e etnia** nos concursos públicos do Estado do Rio Grande do Sul"),
        
        ("Como deve ser a inclusão nos concursos?", 
         "**Conteúdo programático** deve incluir temas relacionados a **igualdade de gênero, igualdade racial e étnica**"),
        
        ("Qual o objetivo do decreto?", 
         "**Sensibilizar servidores públicos** para questões de **discriminação, preconceito e promoção da igualdade**"),
        
        ("A quem se aplica o decreto?", 
         "**Administração Pública Direta e Indireta** do Estado do Rio Grande do Sul"),
        
        ("Como deve ser implementado?", 
         "**Editais de concurso** devem prever expressamente a inclusão dos temas no conteúdo programático e/ou nas provas")
    ]
    
    # Criar database temporário
    db_path = "collection_direito.db"
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
        "css": ".card {\n font-family: arial;\n font-size: 18px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\n.front {\n background-color: #fff8dc;\n}\n\n.back {\n background-color: #f0f8ff;\n}",
        "name": "Direito Constitucional e Legislação",
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
        "desc": "Deck de Direito - Constituição Federal, Estadual/RS, Leis Especiais e Estatutos",
        "name": "Direito Constitucional e Legislação",
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
    apkg_path = "Direito_Constitucional_Legislacao.apkg"
    with zipfile.ZipFile(apkg_path, 'w', zipfile.ZIP_DEFLATED) as apkg:
        apkg.write(db_path, "collection.db")
        
        # Adicionar arquivo de mídia vazio
        apkg.writestr("media", "{}")
    
    # Limpar arquivo temporário
    os.remove(db_path)
    
    print(f"Deck de Direito criado com sucesso: {apkg_path}")
    print(f"Total de cartões: {len(cards_data)}")
    return apkg_path

if __name__ == "__main__":
    create_direito_deck()
