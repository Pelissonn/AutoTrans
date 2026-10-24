-- Script do banco MySQL do AutoTrans.
-- O projeto usa SQLite por padrão (backend/instance/autotrans.db). Para usar MySQL:
--   1) execute este script;  2) execute popular_banco.sql (dados de demonstração)
--   3) no backend/.env: DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/autotrans_db
-- As tabelas espelham as Models (backend/models/).

CREATE DATABASE IF NOT EXISTS autotrans_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE autotrans_db;

CREATE TABLE IF NOT EXISTS categorias (
	nome VARCHAR(100) NOT NULL, 
	descricao VARCHAR(255), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (nome)
);

CREATE TABLE IF NOT EXISTS usuarios (
	nome VARCHAR(120) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	senha_hash VARCHAR(255) NOT NULL, 
	foto_url VARCHAR(500), 
	is_admin BOOL NOT NULL, 
	aceitou_termos BOOL NOT NULL, 
	data_aceite_termos DATETIME, 
	data_criacao DATETIME NOT NULL, 
	data_atualizacao DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS materiais (
	categoria_id INTEGER NOT NULL, 
	conteudo TEXT NOT NULL, 
	url VARCHAR(255), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(categoria_id) REFERENCES categorias (id)
);

CREATE TABLE IF NOT EXISTS questoes (
	categoria_id INTEGER NOT NULL, 
	enunciado TEXT NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(categoria_id) REFERENCES categorias (id)
);

CREATE TABLE IF NOT EXISTS simulados (
	usuario_id INTEGER NOT NULL, 
	categoria_id INTEGER NOT NULL, 
	titulo VARCHAR(150) NOT NULL, 
	pontuacao_max FLOAT NOT NULL, 
	data_realizacao DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id), 
	FOREIGN KEY(categoria_id) REFERENCES categorias (id)
);

CREATE TABLE IF NOT EXISTS alternativas (
	questao_id INTEGER NOT NULL, 
	texto VARCHAR(255) NOT NULL, 
	correta BOOL NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(questao_id) REFERENCES questoes (id)
);

CREATE TABLE IF NOT EXISTS favoritos (
	usuario_id INTEGER NOT NULL, 
	questao_id INTEGER NOT NULL, 
	data_criacao DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_favorito_usuario_questao UNIQUE (usuario_id, questao_id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id), 
	FOREIGN KEY(questao_id) REFERENCES questoes (id)
);

CREATE TABLE IF NOT EXISTS resultados (
	simulado_id INTEGER NOT NULL, 
	nota FLOAT NOT NULL, 
	data_resultado DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (simulado_id), 
	FOREIGN KEY(simulado_id) REFERENCES simulados (id)
);

CREATE TABLE IF NOT EXISTS itens_simulado (
	simulado_id INTEGER NOT NULL, 
	questao_id INTEGER NOT NULL, 
	alternativa_escolhida_id INTEGER, 
	acerto BOOL NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(simulado_id) REFERENCES simulados (id), 
	FOREIGN KEY(questao_id) REFERENCES questoes (id), 
	FOREIGN KEY(alternativa_escolhida_id) REFERENCES alternativas (id)
);
