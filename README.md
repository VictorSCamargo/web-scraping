# Trabalho Web Scrapping

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

- Adicionem dependências ao requirements.txt;
- Usem a pasta `prints` para salvar prints que possam ser úteis para debug durante seus testes;`
- Podemos criar utilitários e colocá-los na pasta `utils`;