# Trabalho Web Scrapping

## Preparando ambiente

### Dependências python

Instale as dependências com o comando:

```
pip install -r requirements.txt
```

### Chrome Driver

O Selenium, para realizar operações no Chrome, precisa do Chrome for Testing (conhecido também como chromedriver).

Baixe [aqui](https://googlechromelabs.github.io/chrome-for-testing/).

### Execução

Para aproveitar scripts da pasta `utils` no seu script, execute seu script como módulo.

Exemplo:

`python -m sites.blueticket.scripts`

## Boas práticas aos desenvolvedores

- Adicionem dependências ao requirements.txt;
- Usem a pasta `prints` para salvar prints que possam ser úteis para debug durante seus testes;`
- Podemos criar utilitários e colocá-los na pasta `utils`;