# Saúde GO - Monitoramento de Indicadores

Solução desenvolvida para o desafio técnico de **Full Stack Developer (Python/Django)** da Minsait.

O projeto consiste em uma plataforma de análise de dados de saúde pública, utilizando uma arquitetura de microsserviços para ingestão, processamento e visualização de indicadores com alta performance.

---

## 🚀 Tecnologias e Ferramentas

* **Backend:** Django Rest Framework (DRF)
* **Frontend:** Django Templates + Apache ECharts 5 (Visualização de Dados)
* **Banco de Dados:** PostgreSQL 15
* **ETL & Dados:** Pandas (Processamento em *chunks*)
* **Infraestrutura:** Docker & Docker Compose

## 🏗️ Arquitetura da Solução

A solução foi desacoplada em dois serviços containerizados principais. Abaixo, o diagrama de fluxo de dados:

```mermaid
graph TD
    User((Usuário Final))
    Files[Pasta /data<br/>CSV, JSON, GeoJSON]

    subgraph "Docker Host (On-Premise)"
        
        subgraph "Dashboard Service (:8001)"
            Dash[Django View]
            Proxy[Proxy Reverso]
            Chart[Apache ECharts]
        end
        
        subgraph "API Service (:8000)"
            API[Django REST Framework]
            ETL[Script de Ingestão]
        end
        
        subgraph "Persistência"
            DB[(PostgreSQL 15)]
        end
    end

    %% Fluxo de Ingestão
    Files -->|Leitura em Batch| ETL
    ETL -->|Normalização & Carga| DB
    
    %% Fluxo de Uso
    User -->|Acessa HTTP| Dash
    Dash -->|Requisita JSON| API
    API -->|Consulta SQL Otimizada| DB
    DB -->|Retorna JSONB| API
    API -.->|Response| Dash
    Dash -->|Renderiza| Chart



1.  **API Service (Porta 8000):**
    * Responsável pela regra de negócios e ingestão de dados (ETL).
    * Utiliza **JSONField** do PostgreSQL com indexação **GIN** para garantir flexibilidade total na estrutura dos indicadores (Schema-less dentro do Relacional), permitindo filtros dinâmicos sem alterar o esquema do banco.
    * Endpoint dedicado para servir arquivos GeoJSON.

2.  **Dashboard Service (Porta 8001):**
    * Aplicação cliente que consome a API.
    * Atua como um **Proxy Reverso** para o Frontend, evitando problemas de CORS e expondo uma interface limpa.
    * Renderização de gráficos responsivos e mapas interativos.

## 🛠️ Como Executar

Como os dados de exemplo já estão incluídos no repositório, o processo é imediato.

### Pré-requisitos
* Docker & Docker Compose instalados.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/sandroarias/Indicadores_da_Sa-de_GO.git
    cd teste_dev_indicadores_go
    ```

2.  **Suba o ambiente (Build & Run):**
    ```bash
    sudo docker compose up --build -d
    ```

3.  **Popule o Banco de Dados (ETL):**
    Este comando lê os CSVs e Metadados da pasta `/data` e os insere no PostgreSQL.
    ```bash
    sudo docker compose run --rm api python manage.py ingest_data
    ```
    *(Aguarde a mensagem "Importação Concluída com Sucesso!")*

4.  **Acesse o Dashboard:**
    👉 **[http://localhost:8001](http://localhost:8001)**

---

## 📊 Funcionalidades Implementadas

### 1. Ingestão de Dados Inteligente
* Script robusto que normaliza diferentes formatos de JSON e CSV.
* Tratamento automático de nomes de colunas variados (ex: "Município", "Cidade", "Mun").

### 2. Visualização de Dados (ECharts)
* **Gráficos Dinâmicos:** Barras, Linhas e Pizza gerados automaticamente com base nos dados disponíveis.
* **Mapa Geoespacial:** Integração com GeoJSON para renderizar o mapa de calor dos municípios de Goiás.
* **Inteligência de Eixos:** O sistema decide automaticamente se o Eixo X deve ser "Ano" ou "Município" baseado na cardinalidade dos dados.

### 3. Filtros em Cascata (Context-Aware)
* Sistema de filtros onde a seleção de um campo (ex: Município "Anápolis") atualiza automaticamente as opções dos outros campos (ex: Categoria "Pireneus"), impedindo combinações inválidas (Zero Results).

### 4. Extras
* **Paginação:** Controle de visualização para grandes volumes de dados.
* **Exportação CSV:** Download dos dados filtrados direto pelo navegador.
* **Docker Healthchecks:** Garantia de que a API só sobe após o Banco estar pronto.

---
Desenvolvido por **Sandro Ospina Arias**