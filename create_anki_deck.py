import sqlite3
import zipfile
import json
import time
import os
from datetime import datetime

def create_anki_deck():
    """
    Cria um deck do Anki (.apkg) com as matérias de Engenharia de Software
    """
    
    # Dados dos cartões - Frente e Verso
    cards_data = [
        # Fundamentos de Engenharia de Software
        ("O que são Fundamentos de Engenharia de Software?", 
         "Conjunto de princípios, práticas e metodologias para desenvolvimento sistemático de software de qualidade, incluindo processos, ferramentas e técnicas para gestão do ciclo de vida do software."),
        
        # Análise de Sistemas
        ("O que são Técnicas de Especificação de Requisitos?", 
         "Métodos para identificar, documentar e validar necessidades dos usuários e do sistema, incluindo requisitos funcionais e não-funcionais."),
        
        ("Quais as diferenças entre Ciclo de Vida Tradicional e Ágil?", 
         "**Tradicional (Cascata):** Fases sequenciais, documentação extensa, mudanças difíceis.<br>**Ágil:** Iterativo e incremental, colaboração contínua, adaptação a mudanças, entrega frequente."),
        
        # Orientação a Objetos
        ("O que são Objetos e Classes?", 
         "**Classe:** Modelo/template que define atributos e métodos.<br>**Objeto:** Instância de uma classe, entidade concreta com estado e comportamento específicos."),
        
        ("O que é Encapsulamento?", 
         "Princípio que oculta detalhes internos de implementação, expondo apenas interface necessária. Controla acesso através de modificadores (private, protected, public)."),
        
        ("O que são Associações e Ligações?", 
         "**Associação:** Relacionamento estático entre classes.<br>**Ligação:** Relacionamento dinâmico entre objetos em tempo de execução."),
        
        ("O que é Herança?", 
         "Mecanismo que permite criar novas classes baseadas em classes existentes, herdando atributos e métodos. Promove reutilização de código."),
        
        ("O que é Polimorfismo?", 
         "Capacidade de objetos de diferentes classes responderem de forma diferente à mesma mensagem/método. Tipos: sobrecarga e sobrescrita."),
        
        ("O que são Coesão e Acoplamento?", 
         "**Coesão:** Grau de relacionamento entre elementos dentro de um módulo (alta coesão é desejável).<br>**Acoplamento:** Grau de dependência entre módulos (baixo acoplamento é desejável)."),
        
        # Padrão MVC
        ("O que é o Padrão MVC?", 
         "**Model:** Dados e lógica de negócio.<br>**View:** Interface do usuário e apresentação.<br>**Controller:** Controla fluxo entre Model e View, processa requisições."),
        
        ("O que é Inversão de Controle (IoC)?", 
         "Princípio onde o controle de criação e gerenciamento de objetos é transferido para um framework ou container externo."),
        
        ("O que é Injeção de Dependências?", 
         "Técnica para implementar IoC, onde dependências são fornecidas externamente ao objeto, ao invés de serem criadas internamente."),
        
        # Testes de Software
        ("Quais são os Fundamentos de Testes?", 
         "Processo de verificação e validação para encontrar defeitos, garantir qualidade e atender requisitos. Inclui planejamento, execução e análise."),
        
        ("Quais são os Tipos de Testes?", 
         "**Funcionais:** Caixa preta, requisitos.<br>**Não-funcionais:** Performance, segurança.<br>**Estruturais:** Caixa branca, código.<br>**Níveis:** Unitário, integração, sistema, aceitação."),
        
        ("O que é Automação de Testes Funcionais?", 
         "Uso de ferramentas para executar testes automaticamente, verificando funcionalidades sem intervenção manual. Ex: Selenium, TestNG."),
        
        ("O que são Testes Unitários em Java?", 
         "Testes de menor granularidade que verificam componentes individuais. Ferramentas: JUnit, Mockito. Características: rápidos, isolados, repetíveis."),
        
        # Git e Integração Contínua
        ("O que é Integração Contínua com GIT?", 
         "Prática de integrar mudanças frequentemente no repositório principal, com builds e testes automatizados. Ferramentas: Jenkins, GitLab CI, GitHub Actions."),
        
        # Java - Linguagem
        ("Quais são as principais características do Java?", 
         "Orientado a objetos, multiplataforma (JVM), gerenciamento automático de memória, fortemente tipado, seguro, robusto."),
        
        ("O que são Web Services em Java?", 
         "**JAX-RS:** API para REST services.<br>**REST:** Arquitetura stateless com HTTP.<br>**SOAP:** Protocolo baseado em XML para troca de mensagens."),
        
        ("O que são JDBC e JPA?", 
         "**JDBC:** API Java para acesso direto a bancos relacionais.<br>**JPA:** Especificação para mapeamento objeto-relacional, implementada por Hibernate, EclipseLink."),
        
        ("Como tratar e logar erros em Java?", 
         "**Try-catch-finally** para tratamento.<br>**Throws** para propagação.<br>**Logging:** SLF4J, Logback, Log4j para registro de eventos e erros."),
        
        ("O que são Servlets?", 
         "Classes Java que processam requisições HTTP no servidor, parte da especificação Java EE. Executam no container web (Tomcat, Jetty)."),
        
        ("O que são Streams em Java 8+?", 
         "API para processamento funcional de coleções de dados. Operações: filter, map, reduce, collect. Suporte a programação funcional com lambdas."),
        
        ("Conceitos de Programação Funcional em Java", 
         "**Lambda expressions:** (x) -> x * 2<br>**Method references:** String::valueOf<br>**Functional interfaces:** Function, Predicate, Consumer<br>**Immutabilidade e funções puras**"),
        
        # Bancos de Dados
        ("O que são Bancos de Dados Relacionais?", 
         "Sistemas que organizam dados em tabelas relacionadas, seguindo modelo relacional com chaves primárias e estrangeiras."),
        
        ("O que é Mapeamento Físico e Lógico?", 
         "**Lógico:** Estrutura conceitual independente de SGBD.<br>**Físico:** Implementação específica com índices, partições, otimizações de armazenamento."),
        
        ("O que são Diagramas E-R?", 
         "Diagramas Entidade-Relacionamento que modelam dados através de entidades, atributos e relacionamentos. Base para design de banco de dados."),
        
        # Tecnologias Web
        ("O que é o Protocolo HTTP?", 
         "Protocolo de comunicação stateless para transferência de hipertexto. Métodos: GET, POST, PUT, DELETE. Status codes: 200, 404, 500, etc."),
        
        ("O que é XML?", 
         "eXtensible Markup Language - formato para estruturação e transporte de dados, auto-descritivo, hierárquico."),
        
        ("O que é Java EE?", 
         "Plataforma empresarial Java com APIs para desenvolvimento de aplicações distribuídas: Servlets, JSP, EJB, JPA, JAX-RS."),
        
        ("O que é EJB 3?", 
         "Enterprise Java Beans - componentes server-side para lógica de negócio. Tipos: Session Beans, Message-Driven Beans."),
        
        ("O que é Oracle PL/SQL?", 
         "Linguagem procedural da Oracle que estende SQL com estruturas de controle, funções, procedures e packages."),
        
        ("O que é JSF2?", 
         "JavaServer Faces - framework para construção de interfaces web baseadas em componentes, com managed beans e navegação."),
        
        # JBoss EAP
        ("O que é JBoss EAP 7.4+?", 
         "Red Hat JBoss Enterprise Application Platform - servidor de aplicação Java EE/Jakarta EE com alta disponibilidade e clustering."),
        
        ("Principais características do JBoss EAP", 
         "**Instalação:** Standalone/Domain mode<br>**Configuração:** XML configs, CLI<br>**Administração:** Management console<br>**Clustering e load balancing**"),
        
        # Microserviços e Containers
        ("O que são Microserviços?", 
         "Arquitetura que decompõe aplicação em serviços pequenos, independentes e especializados, comunicando via APIs."),
        
        ("O que é Docker?", 
         "Plataforma de containerização que empacota aplicações com suas dependências em containers portáteis e leves."),
        
        ("Vantagens dos Containers", 
         "Portabilidade, isolamento, eficiência de recursos, escalabilidade, consistência entre ambientes, deploy rápido."),
        
        # Integração de Sistemas
        ("O que são REST APIs?", 
         "Architectural style para web services usando HTTP, stateless, com recursos identificados por URLs e operações via métodos HTTP."),
        
        ("REST vs Web Services SOAP", 
         "**REST:** Simples, JSON/XML, HTTP, stateless<br>**SOAP:** Protocolo complexo, XML, envelope/header/body, pode ser stateful"),
        
        # Frontend
        ("O que é HTML5?", 
         "Linguagem de marcação para estruturação de páginas web com novos elementos semânticos, APIs e suporte multimídia."),
        
        ("O que é JavaScript?", 
         "Linguagem de programação interpretada para web, dinâmica, orientada a objetos e funcional. Executa no browser e servidor (Node.js)."),
        
        ("O que é TypeScript?", 
         "Superset do JavaScript que adiciona tipagem estática, interfaces, generics e compile-time checking."),
        
        ("O que é CSS?", 
         "Cascading Style Sheets - linguagem para estilização de páginas web, controla layout, cores, fontes e responsividade."),
        
        # Frameworks Modernos
        ("O que é Quarkus?", 
         "Framework Java nativo para Kubernetes, otimizado para GraalVM e containers, com startup rápido e baixo consumo de memória."),
        
        ("Vantagens do Quarkus", 
         "**Performance:** Startup rápido<br>**Memória:** Baixo footprint<br>**Developer Experience:** Live reload<br>**Cloud Native:** Kubernetes-ready"),
        
        ("O que é Kubernetes?", 
         "Plataforma de orquestração de containers que automatiza deploy, scaling e gerenciamento de aplicações containerizadas."),
        
        ("Principais conceitos do Kubernetes", 
         "**Pods:** Unidade básica<br>**Services:** Exposição de rede<br>**Deployments:** Gerenciamento de réplicas<br>**ConfigMaps/Secrets:** Configurações"),
        
        ("O que são Bancos NoSQL?", 
         "Bancos não-relacionais que oferecem flexibilidade de schema. Tipos: Documento (MongoDB), Chave-Valor (Redis), Coluna (Cassandra), Grafo (Neo4j)."),
        
        # Complementos importantes
        ("Diferenças entre JPA e Hibernate", 
         "**JPA:** Especificação Java para ORM (interface).<br>**Hibernate:** Implementação popular do JPA com recursos adicionais como cache de segundo nível, lazy loading avançado."),
        
        ("O que são Metodologias Ágeis principais?", 
         "**Scrum:** Sprints, Product Owner, Scrum Master.<br>**Kanban:** Fluxo contínuo, limitação WIP.<br>**XP:** Pair programming, TDD, refactoring."),
        
        ("Princípios SOLID em OO", 
         "**S**ingle Responsibility<br>**O**pen/Closed<br>**L**iskov Substitution<br>**I**nterface Segregation<br>**D**ependency Inversion"),
        
        ("O que é TDD (Test Driven Development)?", 
         "Metodologia: Red (teste falha) → Green (código mínimo) → Refactor (melhoria). Garante cobertura e design testável."),
        
        ("Comandos Git essenciais para CI", 
         "**git clone, pull, push**<br>**git branch, checkout, merge**<br>**git add, commit**<br>**git rebase, cherry-pick**<br>**Hooks para automação**"),
        
        ("Padrões de Design comuns em Java", 
         "**Singleton:** Instância única<br>**Factory:** Criação de objetos<br>**Observer:** Notificação de mudanças<br>**Strategy:** Algoritmos intercambiáveis"),
        
        ("Java EE vs Jakarta EE", 
         "**Java EE:** Oracle, até versão 8<br>**Jakarta EE:** Eclipse Foundation, versão 9+, namespace javax → jakarta"),
        
        ("O que é Spring Framework?", 
         "Framework Java para IoC/DI, AOP, MVC web, dados, segurança. Alternativa/complemento ao Java EE/Jakarta EE."),
        
        ("Conceitos de REST API Design", 
         "**Recursos como substantivos**<br>**HTTP methods semânticos**<br>**Status codes apropriados**<br>**HATEOAS, versionamento**<br>**Idempotência**"),
        
        ("Diferenças entre SQL e NoSQL", 
         "**SQL:** ACID, schema fixo, relacionamentos, SQL<br>**NoSQL:** BASE, schema flexível, escalabilidade horizontal, APIs específicas"),
        
        ("O que é DevOps e CI/CD?", 
         "**DevOps:** Cultura de colaboração Dev+Ops<br>**CI:** Integração contínua<br>**CD:** Continuous Delivery/Deployment<br>**Pipeline automatizado**"),
        
        ("Arquitetura de Microserviços - Desafios", 
         "**Complexidade de rede**<br>**Distributed transactions**<br>**Service discovery**<br>**Monitoring e logging**<br>**Data consistency**"),
        
        ("Docker - Comandos essenciais", 
         "**docker build, run, pull, push**<br>**docker-compose up/down**<br>**Dockerfile:** FROM, COPY, RUN, EXPOSE<br>**Volumes e networks**"),
        
        ("Kubernetes - Objetos principais", 
         "**Pod:** Container(s) co-localizados<br>**Service:** Load balancer interno<br>**Ingress:** Acesso externo<br>**Namespace:** Isolamento lógico"),
        
        ("Design Patterns para Microserviços", 
         "**API Gateway:** Ponto de entrada único<br>**Circuit Breaker:** Falhas em cascata<br>**Saga:** Transações distribuídas<br>**CQRS:** Command Query separation"),
        
        ("Princípios de Clean Code", 
         "**Nomes expressivos**<br>**Funções pequenas**<br>**Sem comentários desnecessários**<br>**DRY - Don't Repeat Yourself**<br>**Testes limpos**"),
        
        ("O que é Oracle PL/SQL - Estruturas", 
         "**Procedures e Functions**<br>**Packages:** Agrupamento lógico<br>**Triggers:** Eventos automáticos<br>**Cursors:** Processamento linha a linha<br>**Exception handling**"),
        
        ("JSF2 - Componentes principais", 
         "**Managed Beans:** @ManagedBean<br>**Facelets:** Template engine<br>**Navigation:** faces-config.xml<br>**Validators e Converters**<br>**Ajax support**"),
        
        ("JBoss EAP - Modos de execução", 
         "**Standalone:** Servidor único<br>**Domain:** Múltiplos servidores gerenciados<br>**Host Controller:** Gerencia domain<br>**Management CLI:** jboss-cli.sh"),
        
        ("Monitoramento de aplicações Java", 
         "**JMX:** Java Management Extensions<br>**APM:** Application Performance Monitoring<br>**Logs estruturados**<br>**Métricas (CPU, memória, GC)**<br>**Health checks**")
    ]
    
    # Criar database temporário
    db_path = "collection.db"
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
        "css": ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\n.front {\n background-color: #f0f8ff;\n}\n\n.back {\n background-color: #f5f5f5;\n}",
        "name": "Engenharia de Software",
        "flds": [
            {
                "name": "Frente",
                "media": [],
                "sticky": False,
                "rtl": False,
                "ord": 0,
                "font": "Arial",
                "size": 20
            },
            {
                "name": "Verso",
                "media": [],
                "sticky": False,
                "rtl": False,
                "ord": 1,
                "font": "Arial",
                "size": 20
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
        "desc": "Deck de Engenharia de Software - Fundamentos, Java, Bancos de Dados e Tecnologias Web",
        "name": "Engenharia de Software",
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
    apkg_path = "Engenharia_de_Software.apkg"
    with zipfile.ZipFile(apkg_path, 'w', zipfile.ZIP_DEFLATED) as apkg:
        apkg.write(db_path, "collection.db")
        
        # Adicionar arquivo de mídia vazio
        apkg.writestr("media", "{}")
    
    # Limpar arquivo temporário
    os.remove(db_path)
    
    print(f"Deck criado com sucesso: {apkg_path}")
    print(f"Total de cartões: {len(cards_data)}")
    return apkg_path

if __name__ == "__main__":
    create_anki_deck()
