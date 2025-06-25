# Web Scraping de sites de eventos e exibição em interface web - Trabalho de Web Scraping

Este repositório contém algoritmos para realização de webscraping de sites de eventos e exibição dos eventos coletados em uma interface web.

Os algoritmos foram desenvolvidos durante a disciplina de Tópicos Especiais em Gerência de Dados.

## Visão geral de funcionamento

Para o scraping foram desenvolvidos 3 crawlers, cada um para um site diferente de eventos.

Os resultados de cada crawler foram salvos em arquivos JSON.

Esses resultados foram utilizados em uma aplicação React, que os traduz para cartões em uma aplicação web que exibem informações sobre os eventos.

## Preparando ambiente

### Dependências react

O app react está na pasta [app-react-ts](./app-react-ts/).

Instale as dependências com `npm install`.

### Dependências python

Instale as dependências com o comando:

```
pip install -r requirements.txt
```

#### Chrome Driver

O Selenium, para realizar operações no Chrome, precisa do Chrome for Testing (conhecido também como chromedriver).

Baixe [aqui](https://googlechromelabs.github.io/chrome-for-testing/).

## Execução

### React

Entre na pasta [app-react-ts](./app-react-ts/) e execute `npm run dev`.

### Python

Para aproveitar scripts da pasta `utils` no seu script, execute seu script como módulo.

Exemplo:

`python -m sites.blueticket.scripts`

## Boas práticas aos desenvolvedores

### React

- Formate o código corretamente chamando `npm run format`

### Python

- Adicionem dependências ao requirements.txt;
- Usem a pasta `prints` para salvar prints que possam ser úteis para debug durante seus testes;`
- Podemos criar utilitários e colocá-los na pasta `utils`;