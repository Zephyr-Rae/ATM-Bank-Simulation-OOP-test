import streamlit as st

import gallinero_bank_auth
import gallinero_bank_storage
import gallinero_bank_transactions
import gallinero_bank_analysis
import gallinero_bank_utils
import gallinero_bank_numpad


st.set_page_config(page_title="RAEGAL Bank", page_icon="🏦", layout="wide")

MENU_ITEMS = ["🏠 Dashboard", "💰 Deposit", "🏧 Withdraw", "📜 Transaction History", "📊 Transaction Analysis", "⚙️ Account Settings"]


# ==========================================
# THEME (cream + serif branding + olive pill nav)
# ==========================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Inter:wght@400;500;600&display=swap');

    :root {
        --bg: #F7F1E4; --surface: #FFFDF8; --card: #F1E6CF;
        --accent: #93A06A; --accent-hover: #7C8B57; --accent-tint: #EEF1E2;
        --text: #2B2620; --text-muted: #7A7266; --border: #D9C7A0;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--text); }
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { font-family: 'Fraunces', serif; color: var(--text); }
    p, span, label, div { color: var(--text); }

    [data-testid="stAppViewContainer"] { background-color: var(--bg); }
    [data-testid="stHeader"] { background-color: transparent; }
    [data-testid="stSidebar"] { background-color: var(--bg); border-right: 1px solid var(--border); }
    [data-testid="stSidebar"] * { color: var(--text); }
    [data-testid="stSidebar"] h1 { font-size: 1.5rem; }

    /* Default (action) buttons outside the sidebar: solid olive pill */
    .stButton > button {
        background-color: var(--accent); color: #FFFFFF !important; border: none;
        border-radius: 999px; padding: 0.5rem 1.5rem; font-weight: 600;
        transition: background-color 0.15s ease;
    }
    .stButton > button:hover { background-color: var(--accent-hover); color: #FFFFFF !important; }
    .stButton > button p { color: #FFFFFF !important; }

    /* Sidebar nav + logout pills: uppercase, small, outlined by default */
    [data-testid="stSidebar"] .stButton > button {
        text-transform: uppercase; letter-spacing: 0.03em; font-size: 0.8rem;
        background-color: var(--surface); color: var(--text) !important;
        border: 1px solid var(--border); border-radius: 999px; font-weight: 600;
    }
    [data-testid="stSidebar"] .stButton > button p { color: var(--text) !important; }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: var(--accent-tint); border-color: var(--accent);
    }

    /* Active nav item = primary type = solid olive fill */
    [data-testid="stSidebar"] button[kind="primary"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
        background-color: var(--accent) !important; color: var(--text) !important; border: none !important;
    }
    [data-testid="stSidebar"] button[kind="primary"] p,
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p { color: var(--text) !important; }
    [data-testid="stSidebar"] button[kind="primary"]:hover,
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"]:hover { background-color: var(--accent-hover) !important; }

    [data-testid="stMetric"] {
        background-color: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--accent);
        border-radius: 8px; padding: 1rem 1.2rem;
    }
    [data-testid="stMetricLabel"] { color: var(--text-muted) !important; }
    [data-testid="stMetricValue"] { font-family: 'Fraunces', serif; color: var(--text) !important; }

    .stTabs [data-baseweb="tab"] { font-family: 'Fraunces', serif; font-weight: 600; color: var(--text-muted); }
    .stTabs [aria-selected="true"] { color: var(--accent-hover) !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: var(--accent); }

    .stTextInput input, .stNumberInput input {
        background-color: var(--surface); color: var(--text) !important; border-radius: 8px; border: 1px solid var(--border);
    }
    .stTextInput input::placeholder { color: var(--text-muted); opacity: 1; }
    .stTextInput input:focus, .stNumberInput input:focus { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
    .stTextInput label, .stNumberInput label, .stSelectbox label { color: var(--text) !important; font-weight: 500; }

    .stSelectbox [data-baseweb="select"] { background-color: var(--surface); border-radius: 8px; border: 1px solid var(--border); }
    .stSelectbox [data-baseweb="select"] * { color: var(--text) !important; }

    /* --- NUMPAD BUTTON STYLES --- */

    /* Standard Digit Buttons (Cream fill + tan border) */
    div[data-element-id*="numpad"] button {
        background-color: #F1E6CF !important;
        border: 2px solid #A89B8C !important;
        border-radius: 16px !important;
        color: #2B2620 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    div[data-element-id*="numpad"] button:hover {
        background-color: #E8DAC2 !important;
        border-color: #7C8B57 !important;
    }

    /* Red Backspace Button */
    button[data-testid*="backspace"] {
        background-color: #E29578 !important;
        border: 2px solid #C86D51 !important;
        color: #FFFFFF !important;
    }

    button[data-testid*="backspace"]:hover {
        background-color: #D47B5A !important;
    }

    /* Green Confirm Button */
    button[data-testid*="confirm"] {
        background-color: #93A06A !important;
        border: 2px solid #7C8B57 !important;
        color: #FFFFFF !important;
    }

    button[data-testid*="confirm"]:hover {
        background-color: #7C8B57 !important;
    }
    
    [data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 8px; }
    hr, [data-testid="stDivider"] { border-color: var(--border); }
    [data-testid="stAlert"] { border-radius: 8px; }

    .sidebar-label { font-size: 0.75rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--text-muted); font-weight: 600; margin: 0.5rem 0 0.4rem 0; }
    .account-type { font-style: italic; color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.2rem; }
    </style>
""", unsafe_allow_html=True)


#SESSION STATE

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None

if "menu" not in st.session_state:
    st.session_state.menu = MENU_ITEMS[0]


st.title("𑣲.RAEGAL BANK— ᨳଓ .")
st.caption("Secure Digital Banking System")


#LOGIN / REGISTRATION

if not st.session_state.logged_in:

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Welcome Back")

        username = st.text_input("Username", key="login_username")
        pin = st.text_input("PIN", type="password", key="login_pin")

        if st.button("Login", use_container_width=True):
            account, message = gallinero_bank_auth.login_account(username, pin)

            if account is not None:
                st.session_state.logged_in = True
                st.session_state.account = account
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    with register_tab:
        st.subheader("Create Your RAEGAL Bank Account")

        name = st.text_input("Full Name", key="register_name")
        username = st.text_input("Username", key="register_username")
        account_number = st.text_input("Account Number", key="register_account")
        pin = st.text_input("Create 4-Digit PIN", type="password", key="register_pin")
        confirm_pin = st.text_input("Confirm PIN", type="password", key="register_confirm_pin")
        account_type = st.selectbox("Account Type", ["Savings Account", "Student Account"])
        starting_balance = st.number_input("Starting Balance", min_value=0.0, step=100.0, format="%.2f")

        if st.button("Create Account", use_container_width=True):
            account, message = gallinero_bank_auth.register_account(
                name, username, account_number, pin, confirm_pin, account_type, starting_balance
            )

            if account is not None:
                st.success(message)
                st.info("Your account has been created. Please use the Login tab.")
            else:
                st.error(message)


# LOGGED-IN BANKING APPLICATION
else:
    account = st.session_state.account

    st.sidebar.title("𑣲. RAEGAL BANK — ᨳଓ .")

    st.sidebar.markdown(f'<div class="account-type">{account.get_account_type()}</div>', unsafe_allow_html=True)
    st.sidebar.write(f"**Username:** {account.username}")
    st.sidebar.write(f"**Account Name:** {account.account_name}")
    st.sidebar.write(f"**Account Number:** {account.account_number}")

    st.sidebar.divider()

    #NAV PILLS
    st.sidebar.markdown('<div class="sidebar-label">Menu</div>', unsafe_allow_html=True)

    for item in MENU_ITEMS:
        is_active = st.session_state.menu == item
        if st.sidebar.button(
            item, key=f"nav_{item}", use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.menu = item
            st.rerun()

    menu = st.session_state.menu

    st.sidebar.divider()

    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.account = None
        st.session_state.menu = MENU_ITEMS[0]
        st.rerun()

    #DASHBOARD
    if menu == "🏠 Dashboard":
        st.header(f"👋 Welcome, {account.account_name}")
        st.subheader("Account Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Current Balance", gallinero_bank_utils.format_currency(account.check_balance()))
        col2.metric("Account Type", account.get_account_type())
        col3.metric("Account Number", account.account_number)

        st.divider()
        st.info("Select a banking service from the menu on the left.")

    #DEPOSIT
    elif menu == "💰 Deposit":
        st.header("💰 Deposit Money")
        st.write(
            f"Current Balance:"
            f" **{gallinero_bank_utils.format_currency(account.check_balance())}**"
        )

        amount = st.number_input(
            "Deposit Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="deposit_amount",
        )

        def process_deposit():
            dep_amount = st.session_state.get("deposit_amount", 0.0)
            if not gallinero_bank_utils.is_valid_amount(dep_amount):
                st.error("Invalid deposit amount.")
            else:
                success = account.deposit(dep_amount)
                if success:
                    gallinero_bank_storage.update_account(account)
                    gallinero_bank_transactions.record_transaction(
                        account, "Deposit", dep_amount
                    )
                    # Clear keypad buffer
                    st.session_state["deposit_numpad_digits"] = ""
                    st.session_state["deposit_amount"] = 0.0
                    st.success("Deposit successful.")

        gallinero_bank_numpad.render_numpad(
            "deposit", on_confirm=process_deposit
        )

    #WITHDRAW
    elif menu == "🏧 Withdraw":
        st.header("🏧 Withdraw Money")
        st.write(
            f"Available Balance:"
            f" **{gallinero_bank_utils.format_currency(account.check_balance())}**"
        )

        amount = st.number_input(
            "Withdrawal Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="withdraw_amount",
        )

        def process_withdrawal():
            with_amount = st.session_state.get("withdraw_amount", 0.0)
            if not gallinero_bank_utils.is_valid_amount(with_amount):
                st.error("Invalid withdrawal amount.")
            elif with_amount > account.check_balance():
                st.error("Insufficient balance.")
            else:
                success = account.withdraw(with_amount)
                if success:
                    gallinero_bank_storage.update_account(account)
                    gallinero_bank_transactions.record_transaction(
                        account, "Withdraw", with_amount
                    )
                    st.session_state["withdraw_numpad_digits"] = ""
                    st.session_state["withdraw_amount"] = 0.0
                    st.success("Withdrawal successful.")

        gallinero_bank_numpad.render_numpad(
            "withdraw", on_confirm=process_withdrawal
        )


    #TRANSACTION HISTORY
    elif menu == "📜 Transaction History":
        st.header("📜 Transaction History")

        transactions = gallinero_bank_transactions.get_transactions()
        transactions = [t for t in transactions if t.get("account_number") == account.account_number]

        if transactions:
            display_data = [
                {
                    "Timestamp": t.get("timestamp", "N/A"),
                    "Transaction": t.get("transaction", "N/A"),
                    "Amount": gallinero_bank_utils.format_currency(t.get("amount", 0)),
                    "Balance After": gallinero_bank_utils.format_currency(t.get("balance_after", 0)),
                }
                for t in transactions
            ]
            st.dataframe(display_data, use_container_width=True, hide_index=True)
        else:
            st.info("No transaction history available.")

    #TRANSACTION ANALYSIS
    elif menu == "📊 Transaction Analysis":
        st.header("📊 Transaction Analysis")

        result = gallinero_bank_analysis.analyze_transactions(account.account_number)

        st.subheader("1. Transaction Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", result["total_transactions"])
        col2.metric("Deposits", result["deposits"])
        col3.metric("Withdrawals", result["withdrawals"])

        st.divider()

        st.subheader("2. Money Flow Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Deposited", gallinero_bank_utils.format_currency(result["total_deposited"]))
        col2.metric("Total Withdrawn", gallinero_bank_utils.format_currency(result["total_withdrawn"]))
        col3.metric("Net Cash Flow", gallinero_bank_utils.format_currency(result["net_cash_flow"]))

        st.divider()

        st.subheader("3. Account Activity Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Largest Transaction", gallinero_bank_utils.format_currency(result["largest_transaction"]))
        col2.metric("Average Transaction", gallinero_bank_utils.format_currency(result["average_transaction"]))
        col3.metric("Latest Transaction", result["latest_transaction"])

        st.caption(f"Latest Activity: {result['latest_timestamp']}")

    #ACCOUNT SETTINGS
    elif menu == "⚙️ Account Settings":
        st.header("⚙️ Account Settings")

        username_tab, pin_tab = st.tabs(["Change Username", "Change PIN"])

        with username_tab:
            st.write(f"Current Username: **{account.username}**")
            new_username = st.text_input("New Username", key="new_username")

            if st.button("Update Username", use_container_width=True):
                success, message = gallinero_bank_auth.change_username(account, new_username)

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        with pin_tab:
            current_pin = st.text_input("Current PIN", type="password", key="current_pin_input")
            new_pin = st.text_input("New PIN", type="password", key="new_pin_input")
            confirm_new_pin = st.text_input("Confirm New PIN", type="password", key="confirm_new_pin_input")

            if st.button("Update PIN", use_container_width=True):
                success, message = gallinero_bank_auth.change_pin(account, current_pin, new_pin, confirm_new_pin)

                if success:
                    st.success(message)
                else:
                    st.error(message)

"""
######### Learning Signature #########
Programmed by: Clarissa Rae D. Gallinero
Date Submitted: September 9, 2026

Program Description: This program defines the base Account class (shared
balance, PIN, and account-number logic) and two subclasses, SavingsAccount
and StudentAccount, that inherit everything from Account and only override
get_account_type() to identify which kind of account it is.
Reflection: I learned how to customize buttons and colors! And of course lists and the like.

AI Usage
[ ] No AI Assistance - Completed independently without AI.
[/] AI as Support Tool - Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner - Used AI to design, structure, or co-create significant code.
"""
                    
