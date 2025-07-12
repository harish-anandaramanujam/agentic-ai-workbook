import gradio as gr
from accounts import Account

# Initialize global account variable
account = None

def create_account(account_id: str, initial_deposit: float):
    global account
    try:
        account = Account(account_id, initial_deposit)
        return f"Account {account_id} created with initial deposit of {initial_deposit}."
    except ValueError as e:
        return str(e)

def deposit_funds(amount: float):
    if account is None:
        return "No account found. Please create an account first."
    try:
        account.deposit(amount)
        return f"Deposited {amount}. Current balance: {account.balance}"
    except ValueError as e:
        return str(e)

def withdraw_funds(amount: float):
    if account is None:
        return "No account found. Please create an account first."
    try:
        account.withdraw(amount)
        return f"Withdrew {amount}. Current balance: {account.balance}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol: str, quantity: int):
    if account is None:
        return "No account found. Please create an account first."
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} of {symbol}. Current balance: {account.balance}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol: str, quantity: int):
    if account is None:
        return "No account found. Please create an account first."
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} of {symbol}. Current balance: {account.balance}"
    except ValueError as e:
        return str(e)

def get_portfolio():
    if account is None:
        return "No account found. Please create an account first."
    return account.get_holdings()

def get_profit_loss():
    if account is None:
        return "No account found. Please create an account first."
    profit_loss = account.get_profit_or_loss()
    return f"Profit or Loss: {profit_loss}"

def get_transaction_history():
    if account is None:
        return "No account found. Please create an account first."
    return account.get_transaction_history()

# Gradio interface setup
with gr.Blocks() as demo:
    gr.Markdown("## Trading Simulation Account Management")

    with gr.Tab("Create Account"):
        account_id_input = gr.Textbox(label="Account ID")
        initial_deposit_input = gr.Number(label="Initial Deposit")
        create_account_button = gr.Button("Create Account")
        create_account_output = gr.Textbox(label="Output")
        create_account_button.click(create_account, [account_id_input, initial_deposit_input], create_account_output)
        
    with gr.Tab("Deposit Funds"):
        amount_input_deposit = gr.Number(label="Amount to Deposit")
        deposit_button = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Output")
        deposit_button.click(deposit_funds, [amount_input_deposit], deposit_output)

    with gr.Tab("Withdraw Funds"):
        amount_input_withdraw = gr.Number(label="Amount to Withdraw")
        withdraw_button = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Output")
        withdraw_button.click(withdraw_funds, [amount_input_withdraw], withdraw_output)

    with gr.Tab("Buy Shares"):
        symbol_input_buy = gr.Textbox(label="Symbol")
        quantity_input_buy = gr.Number(label="Quantity")
        buy_button = gr.Button("Buy")
        buy_output = gr.Textbox(label="Output")
        buy_button.click(buy_shares, [symbol_input_buy, quantity_input_buy], buy_output)

    with gr.Tab("Sell Shares"):
        symbol_input_sell = gr.Textbox(label="Symbol")
        quantity_input_sell = gr.Number(label="Quantity")
        sell_button = gr.Button("Sell")
        sell_output = gr.Textbox(label="Output")
        sell_button.click(sell_shares, [symbol_input_sell, quantity_input_sell], sell_output)

    with gr.Tab("View Portfolio"):
        portfolio_button = gr.Button("Get Portfolio")
        portfolio_output = gr.Textbox(label="Portfolio")
        portfolio_button.click(get_portfolio, [], portfolio_output)

    with gr.Tab("Profit or Loss"):
        profit_loss_button = gr.Button("Get Profit or Loss")
        profit_loss_output = gr.Textbox(label="Profit or Loss")
        profit_loss_button.click(get_profit_loss, [], profit_loss_output)

    with gr.Tab("Transaction History"):
        transaction_history_button = gr.Button("Get Transaction History")
        transaction_history_output = gr.Textbox(label="Transaction History")
        transaction_history_button.click(get_transaction_history, [], transaction_history_output)

# Launch the Gradio demo
demo.launch()