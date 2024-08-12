# **Google Shopping Price Tracker**

### **Descrição do Projeto**
Este projeto consiste em uma ferramenta automatizada para pesquisa de preços no Google Shopping, desenvolvida com Selenium WebDriver e integrada ao Google Sheets API. A aplicação permite buscar produtos, analisar preços e atualizar uma planilha do Google com os resultados. Essa solução foi projetada para ajudar na tomada de decisão ao encontrar as melhores ofertas de produtos, excluindo opções que contêm termos proibidos ou estão em domínios não confiáveis.

### **Funcionalidades**
- **Pesquisa Automatizada:** Realiza buscas automáticas de produtos no Google Shopping.
- **Filtragem Avançada:** Exclui resultados que contenham termos proibidos e verifica a confiabilidade do domínio.
- **Integração com Google Sheets:** Atualiza uma planilha do Google com os preços e links das ofertas encontradas.
- **Registro de Data/Hora:** Anexa a data e hora da última atualização para referência.

### **Tecnologias Utilizadas**
- **Python:** Linguagem de programação principal.
- **Selenium WebDriver:** Utilizado para automação de navegação na web.
- **Google Sheets API:** Para leitura e atualização de dados em uma planilha do Google.
- **OAuth 2.0:** Implementado para autenticação segura na API do Google.

### **Como Executar o Projeto**
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seuusuario/google-shopping-price-tracker.git
   cd google-shopping-price-tracker
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuração do Google API:**
   - Baixe as credenciais `client_secret.json` da sua conta Google e coloque na raiz do projeto.
   - Na primeira execução, o script solicitará autorização para acessar sua conta Google e criará um arquivo `token.json` para autenticações futuras.

4. **Executando o Script:**
   ```bash
   python main.py
   ```
   Isso iniciará o WebDriver, buscará os produtos na planilha Google Sheets configurada e atualizará a planilha com os preços encontrados.

### **Estrutura do Projeto**
- **`main.py:`** Contém o fluxo principal do script, lidando com a autenticação, busca de produtos e atualização da planilha.
- **`requirements.txt:`** Lista as dependências do projeto.
- **`utils.py:`** Funções auxiliares como verificação de termos proibidos, filtragem de resultados e manipulação da API do Google Sheets.
- **`client_secret.json:`** Arquivo de credenciais (não incluído no repositório) para acesso à API do Google.

### **Contribuições**
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias ou novos recursos.

### **Licença**
Este projeto é licenciado sob a [MIT License](LICENSE).


