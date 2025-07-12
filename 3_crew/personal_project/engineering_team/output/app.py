import gradio as gr
from accounts import Account, get_share_price

account = None

def create_account(username, initial_deposit):
    global account
    account = Account(username, initial_deposit)
    return f"Account for {username} created with initial deposit ${initial_deposit:.2f}."

def deposit_funds(amount):
    global account
    account.deposit(amount)
    return f"Deposited: ${amount:.2f}. Current balance: ${account.balance:.2f}."

def withdraw_funds(amount):
    global account
    try:
        account.withdraw(amount)
        return f"Withdrew: ${amount:.2f}. Current balance: ${account.balance:.2f}."
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    global account
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. Current balance: ${account.balance:.2f}."
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    global account
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. Current balance: ${account.balance:.2f}."
    except ValueError as e:
        return str(e)

def report_holdings():
    global account
    return account.report_holdings()

def report_profit_loss():
    global account
    return f"Current profit/loss: ${account.report_profit_loss():.2f}."

def list_transactions():
    global account
    return account.list_transactions()

with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Management")
    username = gr.Textbox(label="Username")
    initial_deposit = gr.Number(label="Initial Deposit", value=1000)
    create_btn = gr.Button("Create Account")
    create_output = gr.Textbox(label="Creation Output", interactive=False)

    deposit_amount = gr.Number(label="Deposit Amount")
    deposit_btn = gr.Button("Deposit Funds")
    deposit_output = gr.Textbox(label="Deposit Output", interactive=False)

    withdraw_amount = gr.Number(label="Withdraw Amount")
    withdraw_btn = gr.Button("Withdraw Funds")
    withdraw_output = gr.Textbox(label="Withdrawal Output", interactive=False)

    symbol = gr.Textbox(label="Stock Symbol (AAPL, TSLA, GOOGL)")
    buy_quantity = gr.Number(label="Buy Quantity")
    buy_btn = gr.Button("Buy Shares")
    buy_output = gr.Textbox(label="Buy Output", interactive=False)

    sell_quantity = gr.Number(label="Sell Quantity")
    sell_btn = gr.Button("Sell Shares")
    sell_output = gr.Textbox(label="Sell Output", interactive=False)

    holdings_btn = gr.Button("Report Holdings")
    holdings_output = gr.Textbox(label="Current Holdings", interactive=False)
    
    profit_loss_btn = gr.Button("Report Profit/Loss")
    profit_loss_output = gr.Textbox(label="Profit/Loss", interactive=False)

    transactions_btn = gr.Button("List Transactions")
    transactions_output = gr.Textbox(label="Transactions", interactive=False)

    create_btn.click(create_account, inputs=[username, initial_deposit], outputs=create_output)
    deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
    withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    buy_btn.click(buy_shares, inputs=[symbol, buy_quantity], outputs=buy_output)
    sell_btn.click(sell_shares, inputs=[symbol, sell_quantity], outputs=sell_output)
    holdings_btn.click(report_holdings, outputs=holdings_output)
    profit_loss_btn.click(report_profit_loss, outputs=profit_loss_output)
    transactions_btn.click(list_transactions, outputs=transactions_output)

demo.launch()