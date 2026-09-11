import streamlit as st


def _digits_key(context):
    return f"{context}_numpad_digits"


def _amount_key(context):
    return f"{context}_amount"


def _amount_from_digits(digits):

    if digits == "":
        return 0.0

    return int(digits) / 100


def _press_digit(context, digit):

    digits = st.session_state.get(_digits_key(context), "")

    if len(digits) < 9:
        digits += digit

    st.session_state[_digits_key(context)] = digits
    st.session_state[_amount_key(context)] = _amount_from_digits(digits)


def _press_backspace(context):

    digits = st.session_state.get(_digits_key(context), "")
    digits = digits[:-1]

    st.session_state[_digits_key(context)] = digits
    st.session_state[_amount_key(context)] = _amount_from_digits(digits)


def render_numpad(context, on_confirm=None):
    """Draws a 3-column numeric keypad with custom button keys."""
    with st.container(key=f"{context}_numpad"):
        rows = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

        for row in rows:
            cols = st.columns(3)
            for col, digit in zip(cols, row):
                col.button(
                    digit,
                    key=f"{context}_num_{digit}",
                    use_container_width=True,
                    on_click=_press_digit,
                    args=(context, digit),
                )

        # Bottom Row: Backspace | 0 | Confirm
        col1, col2, col3 = st.columns(3)

        col1.button(
            "⌫",
            key=f"{context}_backspace",
            use_container_width=True,
            on_click=_press_backspace,
            args=(context,),
        )

        col2.button(
            "0",
            key=f"{context}_num_0",
            use_container_width=True,
            on_click=_press_digit,
            args=(context, "0"),
        )

        # Green confirmation action button
        col3.button(
            "✔",
            key=f"{context}_confirm",
            use_container_width=True,
            on_click=on_confirm,
        )
        
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