from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import requests
import base64
from io import BytesIO
import os
import csv

# Tokens
TOKEN = '8165076390:AAE9HE6ucif9TC3pyQ6RG8Z5jo0s6WAevDs'
ACCESS_TOKEN = 'APP_USR-7514101082488981-082921-2d88735b8909c11e425f5857451ae1dd-594134460'

# Produtos disponíveis
sabores = {
    'Bolo de Fuba': {'250g': 6.20, '500g': 10, '1kg': 18},
    'Bolo Formigueiro': {'250g': 7.50, '500g': 12, '1kg': 20},
    'Bolo de Cenoura': {'250g': 4.00, '500g': 7, '1kg': 12},
    'Bolo de Coco com fuba': {'250g': 7.20, '500g': 12, '1kg': 22},
    'Bolo de Limao': {'250g': 6, '500g': 9, '1kg': 15},
    'Torta de Morango': {'250g': 15, '500g': 27, '1kg': 50}
}

CSV_PATH = "pedidos.csv"
TXT_PATH = "pedidos.txt"

if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["UserID", "Nome", "Horário", "Sabor", "Quantidade", "Valor"])

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(sabor, callback_data=f'sabor_{sabor}')] for sabor in sabores]
    await update.message.reply_text("🍰 Escolha o sabor do bolo:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = query.from_user.id

    if data.startswith('sabor_'):
        sabor = data.split('_')[1]
        user_data[uid] = {'sabor': sabor}
        quantidades = sabores[sabor]
        buttons = [[InlineKeyboardButton(f"{q} - R${v}", callback_data=f'quant_{q}')] for q, v in quantidades.items()]
        await query.edit_message_text(f"🍰 *{sabor}*\nEscolha a quantidade:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith('quant_'):
        quantidade = data.split('_')[1]
        sabor = user_data[uid]['sabor']
        valor = sabores[sabor][quantidade]
        user_data[uid].update({'quantidade': quantidade, 'valor': valor})

        # Cria cobrança Pix
        pix_data = {
            "transaction_amount": float(valor),
            "description": f"{sabor} - {quantidade}",
            "payment_method_id": "pix",
            "payer": {
                "email": "anonimo@email.com",
                "first_name": "Cliente",
                "last_name": "Telegram"
            }
        }
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post("https://api.mercadopago.com/v1/payments", json=pix_data, headers=headers)
        res = response.json()

        copia_e_cola = res['point_of_interaction']['transaction_data']['qr_code']
        qr_base64 = res['point_of_interaction']['transaction_data']['qr_code_base64']
        qr_img = BytesIO(base64.b64decode(qr_base64))
        qr_img.seek(0)

        await query.edit_message_text(
            f"✅ Pedido:\n*{sabor}* - *{quantidade}* - *R${valor}*\n\n"
            f"💸 Copie o código Pix abaixo ou escaneie o QR Code:\n"
            f"`{copia_e_cola}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Já paguei", callback_data="paguei")]])
        )
        await context.bot.send_photo(chat_id=uid, photo=qr_img)

    elif data == 'paguei':
        await query.edit_message_text("🔎 Verificando pagamento, aguarde...")

        try:
            pagamentos = requests.get(
                "https://api.mercadopago.com/v1/payments/search",
                headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
                params={"sort": "date_created", "criteria": "desc", "limit": 10}
            ).json()

            pago = False
            if 'results' in pagamentos:
                for pagamento in pagamentos['results']:
                    if (
                        pagamento["status"] == "approved" and
                        pagamento["transaction_amount"] == user_data[uid]['valor'] and
                        user_data[uid]['sabor'] in pagamento["description"]
                    ):
                        pago = True
                        break

            if pago:
                await query.edit_message_text("✅ Pagamento confirmado!\nAgora, envie seu *nome* (apelido ou identificador):", parse_mode="Markdown")
                context.user_data['esperando_nome'] = True
            else:
                await query.edit_message_text("🚫 Pagamento *não localizado* ainda.\nAguarde 1 minutinho e clique novamente em 'Já paguei'.", parse_mode="Markdown")
        except Exception as e:
            await query.edit_message_text(f"❌ Erro ao verificar pagamento.\n{e}")

async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    texto = update.message.text

    if context.user_data.get('esperando_nome'):
        user_data[uid]['nome'] = texto
        context.user_data['esperando_nome'] = False
        context.user_data['esperando_horario'] = True

        botoes = [[InlineKeyboardButton(f"{h}:00", callback_data=f'horario_{h}')] for h in range(9, 17)]
        await update.message.reply_text("⏰ Escolha o horário de retirada:", reply_markup=InlineKeyboardMarkup(botoes))

async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if query.data.startswith('horario_'):
        hora = query.data.split('_')[1]
        user_data[uid]['horario'] = f"{hora}:00"
        dados = user_data[uid]

        resumo = (
            f"✅ Pedido confirmado!\n\n"
            f"🍰 *Sabor:* {dados['sabor']}\n"
            f"📦 *Quantidade:* {dados['quantidade']}\n"
            f"💰 *Valor:* R${dados['valor']}\n"
            f"📛 *Nome:* {dados['nome']}\n"
            f"🕒 *Retirada:* {dados['horario']}"
        )
        await query.edit_message_text(resumo, parse_mode="Markdown")

        with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([uid, dados['nome'], dados['horario'], dados['sabor'], dados['quantidade'], dados['valor']])

        with open(TXT_PATH, mode="a", encoding="utf-8") as f:
            f.write(f"\n---\nID: {uid}\nNome: {dados['nome']}\nRetirada: {dados['horario']}\nProduto: {dados['sabor']} - {dados['quantidade']} - R${dados['valor']}\n")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(horario, pattern=r'^horario_'))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_mensagem))
    print("✅ Bot rodando...")
    app.run_polling()
