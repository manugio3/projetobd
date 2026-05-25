import sqlite3

# CRIAR O BANCO
conn = sqlite3.connect('copa_mundo.db')
cursor = conn.cursor()

# DESATIVAR AS CHAVES ESTRANGEIRAS, SE NÃO OS DROPS PODEM TRAVAR
cursor.execute("PRAGMA foreign_keys = OFF")

# APAGAR VISÕES, GATILHOS E TABELAS CASO EXISTAM
cursor.execute("DROP TRIGGER IF EXISTS trg_valida_minutos")
cursor.execute("DROP TABLE IF EXISTS Premio")
cursor.execute("DROP TABLE IF EXISTS Cartoes")
cursor.execute("DROP TABLE IF EXISTS Gol")
cursor.execute("DROP TABLE IF EXISTS Escalacao")
cursor.execute("DROP TABLE IF EXISTS Apita")
cursor.execute("DROP TABLE IF EXISTS Convocacao")
cursor.execute("DROP TABLE IF EXISTS Idioma")
cursor.execute("DROP TABLE IF EXISTS Partida")
cursor.execute("DROP TABLE IF EXISTS Estadio")
cursor.execute("DROP TABLE IF EXISTS Selecao")
cursor.execute("DROP TABLE IF EXISTS Tecnico")
cursor.execute("DROP TABLE IF EXISTS Juiz")
cursor.execute("DROP TABLE IF EXISTS Jogador")
cursor.execute("DROP TABLE IF EXISTS Pessoa")

# REATIVAR AS CHAVES ESTRANGEIRAS PARA OS CREATES
cursor.execute("PRAGMA foreign_keys = ON")

# TABELA PESSOA
cursor.execute('''
CREATE TABLE Pessoa(
    CPF TEXT PRIMARY KEY,
    NOME TEXT NOT NULL,
    NACIONALIDADE TEXT,
    DT_NASC TEXT
)
''')

# TABELA JOGADOR
cursor.execute('''
CREATE TABLE Jogador(
    CPF TEXT PRIMARY KEY,
    N_CAMISA INTEGER,
    POSICAO TEXT,
    CPF_LIDER TEXT,

    FOREIGN KEY(CPF) REFERENCES Pessoa(CPF),
    FOREIGN KEY(CPF_LIDER) REFERENCES Jogador(CPF)
)
''')

# TABELA IDIOMA
cursor.execute('''
CREATE TABLE Idioma(
    CPF_JG TEXT,
    IDIOMA TEXT,

    PRIMARY KEY(CPF_JG, IDIOMA),
    FOREIGN KEY(CPF_JG) REFERENCES Jogador(CPF)
)
''')

# TABELA JUIZ
cursor.execute('''
CREATE TABLE Juiz(
    CPF TEXT PRIMARY KEY,
    CATEGORIA TEXT,

    FOREIGN KEY(CPF) REFERENCES Pessoa(CPF)
)
''')

# TABELA TECNICO
cursor.execute('''
CREATE TABLE Tecnico(
    CPF TEXT PRIMARY KEY,
    SALARIO REAL,

    FOREIGN KEY(CPF) REFERENCES Pessoa(CPF)
)
''')

# TABELA SELECAO
cursor.execute('''
CREATE TABLE Selecao(
    ID INTEGER PRIMARY KEY,
    RANKING_FIFA INTEGER,
    PAIS TEXT,
    CPF_T TEXT UNIQUE NOT NULL,

    FOREIGN KEY(CPF_T) REFERENCES Tecnico(CPF)
)
''')

# TABELA ESTADIO
cursor.execute('''
CREATE TABLE Estadio(
    ID INTEGER PRIMARY KEY,
    NOME TEXT,
    CAPACIDADE INTEGER,
    ENDERECO_CEP TEXT,
    ENDERECO_NUM TEXT,
    ENDERECO_LOGRADOURO TEXT
)
''')

# TABELA PARTIDA
cursor.execute('''
CREATE TABLE Partida(
    MATCH_ID INTEGER PRIMARY KEY,
    DATA TEXT,
    FASE TEXT,
    PUBLICO INTEGER,
    PLACAR_A INTEGER,
    PLACAR_B INTEGER,
    ID_ESTADIO INTEGER NOT NULL,
    ID_TIME_A INTEGER NOT NULL,
    ID_TIME_B INTEGER NOT NULL,

    FOREIGN KEY(ID_ESTADIO) REFERENCES Estadio(ID),
    FOREIGN KEY(ID_TIME_A) REFERENCES Selecao(ID),
    FOREIGN KEY(ID_TIME_B) REFERENCES Selecao(ID),

    CHECK(ID_TIME_A <> ID_TIME_B)
)
''')

# TABELA APITA
cursor.execute('''
CREATE TABLE Apita(
    CPF_J TEXT,
    MATCH_ID_P INTEGER,

    PRIMARY KEY(CPF_J, MATCH_ID_P),

    FOREIGN KEY(CPF_J) REFERENCES Juiz(CPF),
    FOREIGN KEY(MATCH_ID_P) REFERENCES Partida(MATCH_ID)
)
''')

# TABELA ESCALACAO
cursor.execute('''
CREATE TABLE Escalacao(
    CPF_JG TEXT,
    MATCH_ID_P INTEGER,
    ID_S INTEGER NOT NULL,
    SITUACAO TEXT,
    MIN_JOGADOS INTEGER,

    PRIMARY KEY(CPF_JG, MATCH_ID_P),

    FOREIGN KEY(CPF_JG) REFERENCES Jogador(CPF),
    FOREIGN KEY(MATCH_ID_P) REFERENCES Partida(MATCH_ID),
    FOREIGN KEY(ID_S) REFERENCES Selecao(ID)
)
''')

# TABELA GOL
cursor.execute('''
CREATE TABLE Gol(
    CPF_JG TEXT NOT NULL,
    MINUTO INTEGER,
    TIPO TEXT,
    MATCH_ID_P INTEGER NOT NULL,

    PRIMARY KEY(CPF_JG, MINUTO, MATCH_ID_P),

    FOREIGN KEY(CPF_JG) REFERENCES Jogador(CPF),
    FOREIGN KEY(MATCH_ID_P) REFERENCES Partida(MATCH_ID)
)
''')

# TABELA CARTOES
cursor.execute('''
CREATE TABLE Cartoes(
    CPF_JG TEXT NOT NULL,
    MATCH_ID_P INTEGER NOT NULL,
    CARTOES_TIPO TEXT,

    PRIMARY KEY(CPF_JG, MATCH_ID_P, CARTOES_TIPO),

    FOREIGN KEY(CPF_JG) REFERENCES Jogador(CPF),
    FOREIGN KEY(MATCH_ID_P) REFERENCES Partida(MATCH_ID)
)
''')

# TABELA CONVOCAÇÃO
cursor.execute('''
CREATE TABLE Convocacao(
    CPF_JG TEXT,
    ID_S INTEGER,
    DATA TEXT,

    PRIMARY KEY(CPF_JG, ID_S, DATA),

    FOREIGN KEY(CPF_JG) REFERENCES Jogador(CPF),
    FOREIGN KEY(ID_S) REFERENCES Selecao(ID)
)
''')

# TABELA PREMIO 
cursor.execute('''
CREATE TABLE Premio(
    COD INTEGER PRIMARY KEY,
    NOME TEXT,
    DESCRICAO TEXT,
    CPF_JG TEXT NOT NULL,
    ID_S INTEGER NOT NULL,

    FOREIGN KEY(CPF_JG) REFERENCES Jogador(CPF),
    FOREIGN KEY(ID_S) REFERENCES Selecao(ID)
)
''')

conn.commit()
print("Banco criado com sucesso de forma 100% consistente!")

# INSERIR PESSOAS
pessoas = [
    ('111', 'Vinicius Junior', 'Brasil', '2000-07-12'),
    ('112', 'Rodrygo Goes', 'Brasil', '2001-01-09'),
    ('113', 'Endrick', 'Brasil', '2006-07-21'),
    ('114', 'Alisson Becker', 'Brasil', '1992-10-02'),
    ('115', 'Marquinhos', 'Brasil', '1994-05-14'),
    ('211', 'Lionel Messi', 'Argentina', '1987-06-24'),
    ('212', 'Julian Alvarez', 'Argentina', '2000-01-31'),
    ('213', 'Emiliano Martinez', 'Argentina', '1992-09-02'),
    ('214', 'Enzo Fernandez', 'Argentina', '2001-01-17'),
    ('311', 'Kylian Mbappe', 'Franca', '1998-12-20'),
    ('312', 'Ousmane Dembele', 'Franca', '1997-05-15'),
    ('313', 'Mike Maignan', 'Franca', '1995-07-03'),
    ('901', 'Carlo Ancelotti', 'Brasil', '1959-06-10'),
    ('902', 'Lionel Scaloni', 'Argentina', '1978-05-16'),
    ('903', 'Didier Deschamps', 'Franca', '1968-10-15'),
    ('990', 'Wilton Pereira Sampaio', 'Brasil', '1981-09-07'),
    ('991', 'Michael Oliver', 'Inglaterra', '1985-02-20')
]
cursor.executemany('INSERT INTO Pessoa VALUES(?,?,?,?)', pessoas)

# INSERIR JOGADORES 
jogadores = [
    ('111', 7, 'Atacante', None),
    ('112', 10, 'Atacante', '111'),
    ('113', 9, 'Atacante', '111'),
    ('114', 1, 'Goleiro', None),
    ('115', 4, 'Zagueiro', None),
    ('211', 10, 'Atacante', None),
    ('212', 9, 'Atacante', '211'),
    ('213', 1, 'Goleiro', None),
    ('214', 8, 'Meio Campo', None),
    ('311', 10, 'Atacante', None),
    ('312', 11, 'Atacante', None),
    ('313', 1, 'Goleiro', None)
]
cursor.executemany('INSERT INTO Jogador VALUES(?,?,?,?)', jogadores)

# IDIOMAS
idiomas = [
    ('111', 'Portugues'), ('111', 'Espanhol'),
    ('211', 'Espanhol'),  ('311', 'Frances'), ('311', 'Espanhol')
]
cursor.executemany('INSERT INTO Idioma VALUES(?,?)', idiomas)

# JUÍZES
juizes = [('990', 'FIFA PRO'), ('991', 'FIFA Elite')]
cursor.executemany('INSERT INTO Juiz VALUES(?,?)', juizes)

# TÉCNICOS
tecnicos = [('901', 800000), ('902', 1200000), ('903', 1500000)]
cursor.executemany('INSERT INTO Tecnico VALUES(?,?)', tecnicos)

# SELEÇÕES
selecoes = [
    (1, 5, 'Brasil', '901'),
    (2, 1, 'Argentina', '902'),
    (3, 2, 'Franca', '903')
]
cursor.executemany('INSERT INTO Selecao VALUES(?,?,?,?)', selecoes)

# ESTÁDIOS
estadios = [
    (1, 'Maracana', 78000, '22021001', '100', 'Av Maracana'),
    (2, 'Lusail Stadium', 88000, '00000000', '1', 'Lusail Avenue')
]
cursor.executemany('INSERT INTO Estadio VALUES(?,?,?,?,?,?)', estadios)

# PARTIDAS 
partidas = [
    (1, '2026-06-12', 'Grupos', 75000, 3, 1, 1, 1, 3),
    (2, '2026-06-28', 'Semi Final', 85000, 2, 0, 2, 1, 2),
    (3, '2026-06-25', 'Grupos', 68000, 1, 2, 2, 2, 3),
    (4, '2026-07-19', 'Final', 88000, 4, 2, 2, 1, 3)
]
cursor.executemany('INSERT INTO Partida VALUES(?,?,?,?,?,?,?,?,?)', partidas)

# APITA
apita = [('991', 1), ('990', 2), ('991', 3), ('990', 4)]
cursor.executemany('INSERT INTO Apita VALUES(?,?)', apita)

# ESCALAÇÕES 
escalacoes = [
    ('111', 1, 1, 'Titular', 90), ('112', 1, 1, 'Titular', 90), ('115', 1, 1, 'Titular', 90),
    ('311', 1, 3, 'Titular', 90),
    ('111', 2, 1, 'Titular', 90), ('113', 2, 1, 'Titular', 90), 
    ('211', 2, 2, 'Titular', 90), ('214', 2, 2, 'Titular', 75),
    ('212', 3, 2, 'Titular', 90), ('311', 3, 3, 'Titular', 90), ('312', 3, 3, 'Titular', 90),
    ('111', 4, 1, 'Titular', 90), ('112', 4, 1, 'Titular', 90), ('113', 4, 1, 'Titular', 30),
    ('311', 4, 3, 'Titular', 90)
]
cursor.executemany('INSERT INTO Escalacao VALUES(?,?,?,?,?)', escalacoes)

# GOLS 
gols = [
    ('111', 12, 'Normal', 1), ('112', 44, 'Normal', 1), ('111', 75, 'Falta', 1), ('311', 30, 'Penalti', 1),
    ('111', 60, 'Normal', 2), ('113', 89, 'Normal', 2),
    ('212', 40, 'Normal', 3), ('311', 15, 'Normal', 3), ('312', 70, 'Normal', 3),
    ('111', 10, 'Normal', 4), ('111', 55, 'Normal', 4), ('112', 23, 'Normal', 4), ('113', 88, 'Normal', 4),
    ('311', 40, 'Penalti', 4), ('311', 82, 'Normal', 4)
]
cursor.executemany('INSERT INTO Gol VALUES(?,?,?,?)', gols)

# CARTÕES
cartoes = [
    ('115', 1, 'Amarelo'),
    ('214', 2, 'Amarelo'),
    ('311', 4, 'Amarelo')
    
]
cursor.executemany('INSERT INTO Cartoes VALUES(?,?,?)', cartoes)

# CONVOCAÇÕES 
convocacoes = [
    ('111', 1, '2026-05-15'), ('112', 1, '2026-05-15'), ('113', 1, '2026-05-15'), 
    ('114', 1, '2026-05-15'), ('115', 1, '2026-05-15'),
    ('211', 2, '2026-05-15'), ('212', 2, '2026-05-15'), ('213', 2, '2026-05-15'), ('214', 2, '2026-05-15'),
    ('311', 3, '2026-05-15'), ('312', 3, '2026-05-15'), ('313', 3, '2026-05-15')
]
cursor.executemany('INSERT INTO Convocacao VALUES(?,?,?)', convocacoes)

# PRÊMIOS
premios = [
    (1, 'Bola de Ouro', 'Melhor jogador do torneio', '111', 1),
    (2, 'Chuteira de Ouro', 'Artilheiro isolado', '311', 3), 
    (3, 'Luva de Ouro', 'Melhor Goleiro', '114', 1) 
]
cursor.executemany('INSERT INTO Premio VALUES(?,?,?,?,?)', premios)

conn.commit()
print("Banco de dados criado e alimentado com sucesso de forma 100% consistente!\n")


# TRIGGER
cursor.execute('''
CREATE TRIGGER trg_valida_minutos
BEFORE INSERT ON Escalacao
FOR EACH ROW
BEGIN
    SELECT CASE 
        WHEN NEW.MIN_JOGADOS < 0 OR NEW.MIN_JOGADOS > 120 THEN
            RAISE(ABORT, 'Erro de Regra de Negócio: Minutos jogados inválidos para uma partida!')
    END;
END;
''')
conn.commit()

# CONSULTAS EXIGIDAS PELAS ESPECIFICAÇÕES

print("1. [Group by/Having] - Quantidade de gols por jogador que fez mais de 2 gols:")
cursor.execute('''
    SELECT CPF_JG, COUNT(*) AS total_gols
    FROM Gol
    GROUP BY CPF_JG
    HAVING COUNT(*) > 2
''')
print(cursor.fetchall(), "\n")

print("2. [Junção interna] - Nome do jogador e o prêmio que ele ganhou:")
cursor.execute('''
    SELECT P.NOME, PR.NOME
    FROM Premio PR
    INNER JOIN Pessoa P ON PR.CPF_JG = P.CPF
''')
print(cursor.fetchall(), "\n")

print("3. [Junção externa] - Nome das pessoas e seus respectivos salários de técnico (se houver):")
cursor.execute('''
    SELECT P.NOME, T.SALARIO
    FROM Pessoa P
    LEFT OUTER JOIN Tecnico T ON P.CPF = T.CPF
''')
print(cursor.fetchall(), "\n")

print("4. [Semi junção] - Jogadores que possuem pelo menos um prêmio cadastrado:")
cursor.execute('''
    SELECT J.CPF, P.NOME 
    FROM Jogador J
    JOIN Pessoa P ON J.CPF = P.CPF
    WHERE EXISTS (
        SELECT 1 FROM Premio PR WHERE PR.CPF_JG = J.CPF
    )
''')
print(cursor.fetchall(), "\n")

print("5. [Anti-junção] - Jogadores que nunca foram advertidos com cartões:")
cursor.execute('''
    SELECT J.CPF, P.NOME
    FROM Jogador J
    JOIN Pessoa P ON J.CPF = P.CPF
    WHERE NOT EXISTS (
        SELECT 1 FROM Cartoes C WHERE C.CPF_JG = J.CPF
    )
''')
print(cursor.fetchall(), "\n")

print("6. [Subconsulta do tipo escalar] - Partidas com público acima da média de todos os jogos:")
cursor.execute('''
    SELECT MATCH_ID, PUBLICO 
    FROM Partida 
    WHERE PUBLICO > (SELECT AVG(PUBLICO) FROM Partida)
''')
print(cursor.fetchall(), "\n")

print("7. [Subconsulta do tipo linha] - Localizar partida idêntica às condições de placar exato de Copa (3x1):")
cursor.execute('''
    SELECT MATCH_ID, FASE 
    FROM Partida 
    WHERE (PLACAR_A, PLACAR_B) = (SELECT 3, 1)
''')
print(cursor.fetchall(), "\n")

print("8. [Subconsulta do tipo tabela] - Nome dos jogadores que atuam como 'Atacante':")
cursor.execute('''
    SELECT NOME 
    FROM Pessoa 
    WHERE CPF IN (SELECT CPF FROM Jogador WHERE POSICAO = 'Atacante')
''')
print(cursor.fetchall(), "\n")

print("9. [Operação de conjunto] - CPFs únicos de todos que são Técnicos ou Juízes:")
cursor.execute('''
    SELECT CPF FROM Tecnico
    UNION
    SELECT CPF FROM Juiz
''')
print(cursor.fetchall(), "\n")


# VALIDAÇÃO FINAL
print('========== PLACAR DOS CONFRONTOS ==========')
for linha in cursor.execute('''
SELECT P.MATCH_ID, SA.PAIS, P.PLACAR_A, SB.PAIS, P.PLACAR_B, P.FASE
FROM Partida P
JOIN Selecao SA ON P.ID_TIME_A = SA.ID
JOIN Selecao SB ON P.ID_TIME_B = SB.ID
'''):
    print(f"Jogo {linha[0]} ({linha[5]}): {linha[1]} {linha[2]} x {linha[4]} {linha[3]}")

print('\n========== QUADRO DE PRÊMIOS ==========')
for linha in cursor.execute('''
SELECT PR.NOME, PE.NOME, S.PAIS
FROM Premio PR
JOIN Pessoa PE ON PE.CPF = PR.CPF_JG
JOIN Selecao S ON S.ID = PR.ID_S
'''):
    print(f"Prêmio: {linha[0]} | Ganhador: {linha[1]} ({linha[2]})")

print('\n========================================')
print('🏆 BRASIL CAMPEÃO DO MUNDO DE 2026! 🏆')
print('========================================')

conn.close()
