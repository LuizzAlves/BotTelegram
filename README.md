## Bot de Vendas Anônimo no Telegram

Bem-vindo ao repositório do **Bot de Vendas Anônimo no Telegram**, criado para facilitar a venda de bolos de forma rápida, segura e sem exposição de dados pessoais.

---

### 🎯 Objetivo

Desenvolver uma solução automatizada para:

* Exibir um catálogo dinâmico de produtos (bolos) com sabores e tamanhos.
* Gerar pedidos por meio de conversas no Telegram.
* Integrar pagamentos via Pix usando QR Code.
* Manter anonimato do cliente.
* Registrar e gerenciar pedidos em um arquivo CSV.

---

### 🚀 Funcionalidades

1. **Catálogo Atualizável**

   * Produtos (bolos) com sabores, tamanhos e preços configuráveis semana a semana.

2. **Fluxo de Pedido**

   * Interação em chat: escolha de sabor, quantidade, informamento de vulgo e horário de retirada.

3. **Pagamento via Pix**

   * Geração de QR Code Pix com valor dinâmico.
   * Integração com Mercado Pago (WalletConnect) para criação de cobranças.
   * Verificação manual de pagamento (botão "Já paguei") e confirmação automática.

4. **Registro de Pedidos**

   * Logging de pedidos em um arquivo CSV com detalhes: data, hora, produto, valor, usuário (vulgo).

5. **Notificações**

   * Mensagem de confirmação no Telegram após validação do pagamento.

---

### 🛠️ Tech Stack

* **Linguagem**: Python 3.13.3
* **Biblioteca Telegram**: `python-telegram-bot` v20.8
* **Gateway de Pagamento**: Mercado Pago API (Pix via WalletConnect)
* **Banco de Dados Leve**: CSV para registro de pedidos

---

### ⚙️ Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/bot-vendas-telegram.git
   cd bot-vendas-telegram
   ```
2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
4. Configure variáveis de ambiente (arquivo `.env`):

   ```dotenv
   TELEGRAM_TOKEN=seu_token_do_bot
   MP_ACCESS_TOKEN=seu_access_token_mercadopago
   ```

---

### 🚀 Uso

1. Inicie o bot:

   ```bash
   python bot.py
   ```
2. No Telegram, procure pelo seu bot e inicie uma conversa.
3. Siga as instruções para visualizar o catálogo e fazer um pedido.
4. Utilize o botão **Já paguei** após efetuar o Pix para validar o pagamento.

---

### 📈 Roadmap

* [ ] Painel web para administração de produtos e pedidos.
* [ ] Integração automática de confirmação de Pix via Webhook.
* [ ] Multi-idiomas para expandir a base de clientes.
* [ ] Relatórios e gráficos de vendas diários e semanais.

---

### 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos:

1. Fork este repositório.
2. Crie uma branch com a sua feature: `git checkout -b minha-feature`
3. Commit suas alterações: `git commit -m 'Adiciona nova feature'`
4. Push para a branch: `git push origin minha-feature`
5. Abra um Pull Request.

---

Obrigado por utilizar o Bot de Vendas Anônimo no Telegram! Qualquer dúvida ou sugestão, abra uma issue.
