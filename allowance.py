import calendar
import hashlib
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


st.set_page_config(
    page_title="Pierce Family Allowance",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>

/* ===== GLOBAL FONT OVERRIDE ===== */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;800;900&display=swap');

html,
body,
body *,
div,
span,
p,
label,
input,
button,
textarea,
select,
[data-testid="stAppViewContainer"],
[data-testid="stMarkdownContainer"],
[data-testid="stTextInput"],
[data-testid="stRadio"],
[data-testid="stDataFrame"],
[data-testid="stDataEditor"],
.stApp,
.stApp *,
.nav-pill,
.kid-card,
.kid-card *,
.balance-box,
.balance-box *,
.activity-detail-title,
.activity-to-text {
    font-family: 'Roboto', Arial, sans-serif !important;
}

.block-container {
    padding-top: 1.0rem;
    padding-bottom: 2rem;
    max-width: 760px;
}
h1 { white-space: nowrap;
    font-size: 1.6rem !important;
    margin-bottom: .25rem;
}
.kid-card {
    border: 1px solid rgba(128,128,128,.25);
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
}
.kid-header {
    display: flex;
    align-items: center;
    gap: 10px;
}
.big-icon {
    font-size: 2.4rem;
    line-height: 1;
}
.kid-name {
    font-size: 1.35rem;
    font-weight: 800;
}
.balance-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
}
.balance-box {
    border-radius: 16px;
    padding: 10px;
    background: rgba(128,128,128,.08);
}
.balance-label {
    color: #777;
    font-size: .88rem;
}
.balance {
    font-size: 1.25rem;
    font-weight: 800;
}.small-muted {
    color: #777;
    font-size: .9rem;
    margin-top: 4px;
}
div.stButton > button {
    width: 100%;
    border-radius: 14px;
    min-height: 46px;
    font-weight: 700;
}

/* Fixed-width mobile navigation */
.nav-wrap {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 8px;
    width: fit-content;
    max-width: 100%;
    margin: 0.55rem 0 0 0;
    padding: 0;
    flex-wrap: nowrap;
}

.nav-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 38px;
    padding: 0 12px;
    border-radius: 13px;
    border: 1px solid rgba(250,250,250,.28);
    color: white !important;
    text-decoration: none !important;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.01em;
    line-height: 1;
    white-space: nowrap;
    background: transparent;
}

.nav-pill.active {
    background: #2f8cff;
    border-color: #2f8cff;
}

.nav-pill:hover {
    text-decoration: none !important;
    border-color: rgba(250,250,250,.45);
}

.block-container h1 { white-space: nowrap;
    margin-bottom: 0.75rem !important;
}

/* Full width nav divider */
.nav-divider {
    width: 100%;
    height: 3px;
    background: rgba(255,255,255,0.2);
    margin-top: 14px;
    margin-bottom: 22px;
}

@media (max-width: 480px) {
    .nav-wrap {
        gap: 6px;
    }
    .nav-pill {
        height: 36px;
        padding: 0 9px;
        font-size: 0.68rem;
        border-radius: 12px;
    }
}









    
}

/* Activity controls */
.activity-separator {
    width: 100%;
    height: 2px;
    background: rgba(255,255,255,0.14);
    margin: 1.0rem 0 1.05rem 0;
}

/* Main action selector: radio behavior, header-pill visual */
.activity-action-anchor + div [role="radiogroup"] {
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;
    gap: 8px !important;
    width: fit-content !important;
    max-width: 100% !important;
    margin: 0.35rem 0 0.9rem 0 !important;
    padding: 0 !important;
    flex-wrap: nowrap !important;
}

.activity-action-anchor + div [role="radiogroup"] label {
    position: relative !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 38px !important;
    padding: 0 12px !important;
    border-radius: 13px !important;
    border: 1px solid rgba(250,250,250,.28) !important;
    color: white !important;
    background: transparent !important;
    cursor: pointer !important;
    min-width: fit-content !important;
}

.activity-action-anchor + div [role="radiogroup"] label:has(input:checked) {
    background: #2f8cff !important;
    border-color: #2f8cff !important;
}

.activity-action-anchor + div [role="radiogroup"] label > div:first-child,
.activity-action-anchor + div [role="radiogroup"] label p,
.activity-action-anchor + div [role="radiogroup"] label span {
    display: none !important;
}

.activity-action-anchor + div [role="radiogroup"] label::after {
    font-size: 0.66rem !important; font-weight: 800 !important;
    font-weight: 800 !important;
    letter-spacing: 0.01em !important;
    line-height: 1 !important;
    text-transform: uppercase !important;
    color: white !important;
}

.activity-action-anchor + div [role="radiogroup"] label:nth-child(1)::after {
    content: "TRANSFER";
}

.activity-action-anchor + div [role="radiogroup"] label:nth-child(2)::after {
    content: "BONUS";
}

.activity-action-anchor + div [role="radiogroup"] label:nth-child(3)::after {
    content: "ADJUSTMENT";
}

/* Detail selectors: compact pill radios instead of dropdowns */
.detail-radio-anchor + div [role="radiogroup"] {
    display: flex !important;
    gap: 8px !important;
    margin: 0.25rem 0 0.75rem 0 !important;
}

.detail-radio-anchor + div [role="radiogroup"] label {
    border: 1px solid rgba(250,250,250,.24) !important;
    border-radius: 12px !important;
    padding: 0.35rem 0.7rem !important;
    background: rgba(128,128,128,.08) !important;
    cursor: pointer !important;
}

.detail-radio-anchor + div [role="radiogroup"] label:has(input:checked) {
    background: #2f8cff !important;
    border-color: #2f8cff !important;
}

.detail-radio-anchor + div [role="radiogroup"] label > div:first-child {
    display: none !important;
}

.detail-radio-anchor + div [role="radiogroup"] label p {
    font-size: 0.82rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
}

/* Tighten the detail form without enclosing it in a weird bubble */
.activity-detail-title {
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: rgba(255,255,255,.72);
    margin: 0 0 0.55rem 0;
    text-transform: uppercase;
}

.activity-to-text {
    margin: -0.25rem 0 0.65rem 0;
    font-size: 0.92rem;
}

@media (max-width: 480px) {
    .activity-action-anchor + div [role="radiogroup"] {
        gap: 6px !important;
    }
    .activity-action-anchor + div [role="radiogroup"] label {
        height: 36px !important;
        padding: 0 9px !important;
        border-radius: 12px !important;
    }
    .activity-action-anchor + div [role="radiogroup"] label::after {
        font-size: 0.68rem !important;
    }
}


/* ===== ACTIVITY TAB FINAL OVERRIDES ===== */
.activity-separator {
    width: 100%;
    height: 2px;
    background: rgba(255,255,255,0.16);
    margin: 0.85rem 0 0.85rem 0;
}

.activity-detail-title {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: rgba(255,255,255,.66);
    margin: 0 0 0.45rem 0;
    text-transform: uppercase;
}

.activity-to-text {
    margin: -0.35rem 0 0.45rem 0;
    font-size: 0.84rem;
}

/* less bulky form widgets */
div[data-testid="stTextInput"] input {
    min-height: 38px !important;
    height: 38px !important;
}
div[data-testid="stRadio"] > label,
div[data-testid="stTextInput"] > label {
    padding-bottom: 0.22rem !important;
}

/* MAIN ACTION RADIO: make it visually match header nav-pill exactly */
.activity-action-anchor + div [role="radiogroup"] {
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;
    gap: 8px !important;
    width: fit-content !important;
    max-width: 100% !important;
    margin: 0.25rem 0 0.75rem 0 !important;
    padding: 0 !important;
    flex-wrap: nowrap !important;
}

.activity-action-anchor + div [role="radiogroup"] label {
    position: relative !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 38px !important;
    padding: 0 12px !important;
    border-radius: 13px !important;
    border: 1px solid rgba(250,250,250,.28) !important;
    color: white !important;
    background: transparent !important;
    cursor: pointer !important;
    min-width: fit-content !important;
    width: fit-content !important;
    white-space: nowrap !important;
    box-sizing: border-box !important;
}

/* hide native radio dot and native Streamlit text */
.activity-action-anchor + div [role="radiogroup"] label > div:first-child,
.activity-action-anchor + div [role="radiogroup"] label p,
.activity-action-anchor + div [role="radiogroup"] label span,
.activity-action-anchor + div [role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
    display: none !important;
}

.activity-action-anchor + div [role="radiogroup"] label:has(input:checked) {
    background: #2f8cff !important;
    border-color: #2f8cff !important;
}

.activity-action-anchor + div [role="radiogroup"] label:hover {
    border-color: rgba(250,250,250,.45) !important;
}

/* fake labels so size/style is exactly controlled */
.activity-action-anchor + div [role="radiogroup"] label::after {
    font-size: 0.66rem !important; font-weight: 800 !important;
    font-weight: 800 !important;
    letter-spacing: 0.01em !important;
    line-height: 1 !important;
    text-transform: uppercase !important;
    color: white !important;
    font-family: inherit !important;
    white-space: nowrap !important;
}
.activity-action-anchor + div [role="radiogroup"] label:nth-of-type(1)::after { content: "TRANSFER"; }
.activity-action-anchor + div [role="radiogroup"] label:nth-of-type(2)::after { content: "BONUS"; }
.activity-action-anchor + div [role="radiogroup"] label:nth-of-type(3)::after { content: "ADJUSTMENT"; }

/* detail/kid radios: compact pills, no dropdowns */
.detail-radio-anchor + div [role="radiogroup"],
.kid-radio-anchor + div [role="radiogroup"] {
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;
    gap: 6px !important;
    width: fit-content !important;
    max-width: 100% !important;
    margin: 0.12rem 0 0.5rem 0 !important;
    padding: 0 !important;
    flex-wrap: wrap !important;
}
.detail-radio-anchor + div [role="radiogroup"] label,
.kid-radio-anchor + div [role="radiogroup"] label {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 31px !important;
    padding: 0.24rem 0.58rem !important;
    border-radius: 11px !important;
    border: 1px solid rgba(250,250,250,.24) !important;
    background: rgba(128,128,128,.08) !important;
    cursor: pointer !important;
    white-space: nowrap !important;
}
.detail-radio-anchor + div [role="radiogroup"] label:has(input:checked),
.kid-radio-anchor + div [role="radiogroup"] label:has(input:checked) {
    background: #2f8cff !important;
    border-color: #2f8cff !important;
}
.detail-radio-anchor + div [role="radiogroup"] label > div:first-child,
.kid-radio-anchor + div [role="radiogroup"] label > div:first-child {
    display: none !important;
}
.detail-radio-anchor + div [role="radiogroup"] label p,
.detail-radio-anchor + div [role="radiogroup"] label span,
.kid-radio-anchor + div [role="radiogroup"] label p,
.kid-radio-anchor + div [role="radiogroup"] label span {
    font-size: 0.66rem !important; font-weight: 800 !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
}

@media (max-width: 480px) {
    .activity-action-anchor + div [role="radiogroup"] { gap: 6px !important; }
    .activity-action-anchor + div [role="radiogroup"] label {
        height: 36px !important;
        padding: 0 9px !important;
        border-radius: 12px !important;
    }
    .activity-action-anchor + div [role="radiogroup"] label::after {
        font-size: 0.68rem !important;
    }
    .detail-radio-anchor + div [role="radiogroup"] label,
    .kid-radio-anchor + div [role="radiogroup"] label {
        min-height: 30px !important;
        padding: 0.22rem 0.52rem !important;
    }
}


div.stButton > button {
    background: rgba(0, 200, 0, 0.18) !important;
    border: 1px solid rgba(0, 200, 0, 0.35) !important;
    color: white !important;
}
div.stButton > button:hover {
    background: rgba(0, 200, 0, 0.28) !important;
    border-color: rgba(0, 200, 0, 0.55) !important;
}


/* Detail labels styling - match .activity-detail-title */
div[data-testid="stRadio"] > label,
div[data-testid="stTextInput"] > label {
    text-transform: uppercase !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.05em !important;
    color: rgba(255,255,255,.66) !important;
    margin: 0 0 0.45rem 0 !important;
}
div[data-testid="stRadio"] > label p,
div[data-testid="stTextInput"] > label p,
div[data-testid="stRadio"] > label span,
div[data-testid="stTextInput"] > label span {
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.05em !important;
    color: rgba(255,255,255,.66) !important;
    text-transform: uppercase !important;
}


div.stButton > button {
    font-family: 'Roboto', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.04em !important;
}




/* ===== SAVE BUTTON FINAL OVERRIDE: nav-pill shape/text, green color ===== */
div.stButton {
    width: fit-content !important;
    max-width: 100% !important;
}

div.stButton > button,
div.stButton > button[kind],
div.stButton > button[data-testid="baseButton-secondary"],
div.stButton > button[data-testid="baseButton-primary"] {
    width: fit-content !important;
    min-width: fit-content !important;
    max-width: 100% !important;
    min-height: 38px !important;
    height: 38px !important;
    padding: 0 12px !important;
    border-radius: 13px !important;
    border: 1px solid rgba(0, 200, 0, 0.35) !important;
    background: rgba(0, 200, 0, 0.18) !important;
    color: white !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    line-height: 1 !important;
    white-space: nowrap !important;
}

div.stButton > button:hover,
div.stButton > button[kind]:hover,
div.stButton > button[data-testid="baseButton-secondary"]:hover,
div.stButton > button[data-testid="baseButton-primary"]:hover {
    background: rgba(0, 200, 0, 0.28) !important;
    border-color: rgba(0, 200, 0, 0.55) !important;
    color: white !important;
}

div.stButton > button p,
div.stButton > button span,
div.stButton > button div,
div.stButton > button [data-testid="stMarkdownContainer"],
div.stButton > button [data-testid="stMarkdownContainer"] p {
    font-family: 'Roboto', Arial, sans-serif !important;
    font-size: 0.76rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.01em !important;
    line-height: 1 !important;
    text-transform: uppercase !important;
    color: white !important;
    margin: 0 !important;
    padding: 0 !important;
    white-space: nowrap !important;
}

@media (max-width: 480px) {
    div.stButton > button,
    div.stButton > button[kind],
    div.stButton > button[data-testid="baseButton-secondary"],
    div.stButton > button[data-testid="baseButton-primary"] {
        height: 36px !important;
        min-height: 36px !important;
        padding: 0 9px !important;
        border-radius: 12px !important;
    }
    div.stButton > button p,
    div.stButton > button span,
    div.stButton > button div,
    div.stButton > button [data-testid="stMarkdownContainer"],
    div.stButton > button [data-testid="stMarkdownContainer"] p {
        font-size: 0.68rem !important;
    }
}


/* Selected kid balance preview on Activity tab */
.selected-kid-balances {
    display: flex;
    gap: 8px;
    margin: 0.10rem 0 0.70rem 0;
    flex-wrap: nowrap;
}
.selected-kid-balance-box {
    border-radius: 11px;
    padding: 7px 10px;
    background: rgba(128,128,128,.08);
    border: 1px solid rgba(250,250,250,.12);
    min-width: 92px;
}
.selected-kid-balance-label {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: rgba(255,255,255,.66);
    line-height: 1;
    margin-bottom: 5px;
}
.selected-kid-balance-value {
    font-size: 0.92rem;
    font-weight: 800;
    color: white;
    line-height: 1;
}


/* PIN entry */
.pin-title {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: rgba(255,255,255,.66);
    margin: 0.25rem 0 0.45rem 0;
    text-transform: uppercase;
}
div[data-testid="stTextInput"]:has(input[aria-label="PIN"]) {
    max-width: 150px !important;
}
div[data-testid="stTextInput"]:has(input[aria-label="PIN"]) input {
    width: 150px !important;
    min-height: 38px !important;
    height: 38px !important;
    text-align: center !important;
}


/* Hide Streamlit header (deploy + menu) */
header {visibility: hidden;}
div[data-testid="stToolbar"] {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_engine():
    db_url = st.secrets.get("DATABASE_URL", "")
    if not db_url:
        st.error("DATABASE_URL is missing from .streamlit/secrets.toml.")
        st.stop()
    return create_engine(db_url, pool_pre_ping=True)


def run_query(sql, params=None):
    engine = get_engine()
    with engine.begin() as conn:
        return conn.execute(text(sql), params or {})



def get_auth_token():
    app_pin = str(st.secrets.get("APP_PIN", "")).strip()
    return hashlib.sha256(f"kids-money-app::{app_pin}".encode("utf-8")).hexdigest()[:24]


def require_pin():
    app_pin = str(st.secrets.get("APP_PIN", "")).strip()

    if not app_pin:
        st.error("APP_PIN is missing from Streamlit secrets.")
        st.stop()

    auth_token = get_auth_token()
    current_token = str(st.query_params.get("auth", "")).strip()

    if st.session_state.get("pin_authenticated", False) or current_token == auth_token:
        st.session_state.pin_authenticated = True
        if current_token != auth_token:
            st.query_params["auth"] = auth_token
        return

    st.markdown("<h1>PIERCE FAMILY ALLOWANCE</h1>", unsafe_allow_html=True)
    st.markdown('<div class="pin-title">ENTER PIN</div>', unsafe_allow_html=True)

    entered_pin = st.text_input(
        "PIN",
        type="password",
        label_visibility="collapsed",
        placeholder="PIN",
        key="pin_entry",
    )

    if st.button("ENTER", key="pin_enter_button"):
        if entered_pin == app_pin:
            st.session_state.pin_authenticated = True
            st.session_state.pop("pin_entry", None)
            st.query_params["auth"] = auth_token
            st.rerun()
        else:
            st.warning("Incorrect PIN.")

    st.stop()


def load_kids():
    engine = get_engine()
    query = """
        select
            kid_id::text as kid_id,
            display_order,
            name,
            icon,
            twice_monthly_allowance as allowance,
            save_percent
        from public.kids
        where is_active = true
        order by display_order, name
    """
    return pd.read_sql(query, engine)


def load_balances():
    engine = get_engine()
    query = """
        select
            kid_id::text as kid_id,
            display_order,
            name,
            icon,
            twice_monthly_allowance as allowance,
            save_percent,
            spend_balance,
            save_balance,
            0::numeric as investment_balance
        from public.kid_balances
        order by display_order, name
    """
    return pd.read_sql(query, engine)


def load_ledger():
    engine = get_engine()
    query = """
        select
            l.entry_id::text as entry_id,
            l.entry_ts as timestamp,
            l.entry_date,
            k.name as kid_name,
            l.entry_type,
            l.amount,
            coalesce(l.from_bucket, '') as from_bucket,
            coalesce(l.to_bucket, '') as to_bucket,
            coalesce(l.comment, '') as comment
        from public.ledger l
        join public.kids k
            on k.kid_id = l.kid_id
        order by l.entry_ts desc, l.entry_date desc
    """
    return pd.read_sql(query, engine)


def save_kids(edited_df):
    existing = load_kids()
    existing_ids = set(existing["kid_id"].astype(str))

    for _, row in edited_df.iterrows():
        kid_id = str(row.get("kid_id", "")).strip()
        name = str(row.get("name", "")).strip() or "Kid"
        icon = str(row.get("icon", "")).strip() or "🧒"
        display_order = int(row.get("display_order", 0) or 0)
        allowance = float(row.get("allowance", 0) or 0)
        save_percent = float(row.get("save_percent", 0) or 0)

        if kid_id and kid_id in existing_ids:
            run_query(
                """
                update public.kids
                set
                    display_order = :display_order,
                    name = :name,
                    icon = :icon,
                    twice_monthly_allowance = :allowance,
                    save_percent = :save_percent
                where kid_id = :kid_id
                """,
                {
                    "kid_id": kid_id,
                    "display_order": display_order,
                    "name": name,
                    "icon": icon,
                    "allowance": allowance,
                    "save_percent": save_percent,
                },
            )
        else:
            run_query(
                """
                insert into public.kids (
                    display_order, name, icon, twice_monthly_allowance, save_percent
                )
                values (
                    :display_order, :name, :icon, :allowance, :save_percent
                )
                """,
                {
                    "display_order": display_order,
                    "name": name,
                    "icon": icon,
                    "allowance": allowance,
                    "save_percent": save_percent,
                },
            )


def add_ledger(kid, entry_type, amount, from_bucket=None, to_bucket=None, comment=""):
    amount = float(amount)

    if amount == 0:
        return False

    run_query(
        """
        insert into public.ledger (
            entry_date, kid_id, entry_type, amount, from_bucket, to_bucket, comment
        )
        values (
            current_date, :kid_id, :entry_type, :amount, :from_bucket, :to_bucket, :comment
        )
        """,
        {
            "kid_id": str(kid["kid_id"]),
            "entry_type": entry_type,
            "amount": round(amount, 2),
            "from_bucket": from_bucket,
            "to_bucket": to_bucket,
            "comment": comment or "",
        },
    )

    return True


def is_allowance_day(d):
    # Sunday = 6 in Python's weekday() convention.
    return d.weekday() == 6


def allowance_periods_due():
    engine = get_engine()

    with engine.begin() as conn:
        last_posted = conn.execute(
            text("select max(period_date) from public.allowance_postings")
        ).scalar()

    today = date.today()

    if last_posted is None:
        # Start with the most recent allowance date on or before today.
        check = today
        while not is_allowance_day(check):
            check -= timedelta(days=1)
        return [check]

    start = last_posted + timedelta(days=1)
    periods = []
    d = start

    while d <= today:
        if is_allowance_day(d):
            periods.append(d)
        d += timedelta(days=1)

    return periods


def auto_post_allowance_on_open():
    periods = allowance_periods_due()

    for period in periods:
        run_query(
            "select public.post_allowance_for_period(:period_date)",
            {"period_date": period},
        )

    return periods


def get_current_page():
    params = st.query_params
    page = params.get("page", "HOME")
    if isinstance(page, list):
        page = page[0] if page else "HOME"
    page = str(page).upper()
    valid_pages = {"HOME", "ACTIVITY", "FAMILY SETTINGS", "LEDGER"}
    return page if page in valid_pages else "HOME"


def render_nav(current_page):
    nav_items = [
        ("HOME", "HOME"),
        ("ACTIVITY", "ACTIVITY"),
        ("FAMILY SETTINGS", "FAMILY SETTINGS"),
        ("LEDGER", "LEDGER"),
    ]

    links = []
    for label, page_name in nav_items:
        active = " active" if current_page == page_name else ""
        href_page = page_name.replace(" ", "%20")
        auth_part = ""
        if st.session_state.get("pin_authenticated", False):
            auth_part = f"&auth={get_auth_token()}"
        links.append(f'<a class="nav-pill{active}" href="?page={href_page}{auth_part}" target="_self">{label}</a>')

    st.markdown(f'<div class="nav-wrap">{"".join(links)}</div>', unsafe_allow_html=True)


def parse_amount(value):
    cleaned = str(value or "").replace("$", "").replace(",", "").strip()
    if cleaned == "":
        return 0.0
    try:
        return round(float(cleaned), 2)
    except ValueError:
        return None



def render_selected_kid_balances(kid_id):
    current = balances[balances["kid_id"].astype(str) == str(kid_id)]
    if current.empty:
        spend = 0.0
        save = 0.0
    else:
        spend = float(current.iloc[0]["spend_balance"])
        save = float(current.iloc[0]["save_balance"])

    st.markdown(
        f"""
        <div class="selected-kid-balances">
            <div class="selected-kid-balance-box">
                <div class="selected-kid-balance-label">Spend</div>
                <div class="selected-kid-balance-value">${spend:,.2f}</div>
            </div>
            <div class="selected-kid-balance-box">
                <div class="selected-kid-balance-label">Save</div>
                <div class="selected-kid-balance-value">${save:,.2f}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kid_picker(kids, label="Which kid?"):
    kid_labels = [f"{row.icon} {row.name}" for row in kids.itertuples()]
    selected_label = st.selectbox(label, kid_labels)
    return kids.iloc[kid_labels.index(selected_label)]


# Require PIN before loading data or posting allowance.
require_pin()

# Auto-post silently on app open after successful PIN entry.
auto_post_allowance_on_open()

kids = load_kids()
balances = load_balances()

st.markdown("<h1>PIERCE FAMILY ALLOWANCE</h1>", unsafe_allow_html=True)

page = get_current_page()
render_nav(page)
st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)


if page == "HOME":
    for _, kid in balances.iterrows():
        spend = float(kid["spend_balance"])
        save = float(kid["save_balance"])
        investment = float(kid.get("investment_balance", 0) or 0)

        st.markdown(
            f"""
            <div class="kid-card">
                <div class="kid-header">
                    <div class="big-icon">{kid['icon']}</div>
                    <div>
                        <div class="kid-name">{kid['name']}</div>
                        <div class="small-muted">${float(kid['allowance']):,.2f} weekly</div>
                    </div>
                </div>
                <div class="balance-row">
                    <div class="balance-box">
                        <div class="balance-label">Spend</div>
                        <div class="balance">${spend:,.2f}</div>
                    </div>
                    <div class="balance-box">
                        <div class="balance-label">Save</div>
                        <div class="balance">${save:,.2f}</div>
                    </div>
                    <div class="balance-box">
                        <div class="balance-label">Investment</div>
                        <div class="balance">${investment:,.2f}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


elif page == "ACTIVITY":
    

    if "activity_action" not in st.session_state:
        st.session_state.activity_action = None

    if st.session_state.pop("activity_saved", False):
        st.success("Transaction saved.")

    if kids.empty:
        st.warning("Add at least one kid in Family Settings first.")
    else:
        action_options = ["TRANSFER", "BONUS", "ADJUSTMENT"]

        index = None
        if st.session_state.activity_action:
            index = action_options.index(st.session_state.activity_action.upper())

        st.markdown('<div class="activity-action-anchor"></div>', unsafe_allow_html=True)
        selected_action = st.radio(
            "Action",
            action_options,
            index=index,
            horizontal=True,
            label_visibility="collapsed",
            key="activity_action_radio",
        )

        action = selected_action.title() if selected_action else None
        st.session_state.activity_action = action

        if action:
            st.markdown('<div class="activity-separator"></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="activity-detail-title">{action}</div>', unsafe_allow_html=True)

            kid_labels = [f"{row.icon} {row.name}" for row in kids.itertuples()]
            st.markdown('<div class="kid-radio-anchor"></div>', unsafe_allow_html=True)
            selected_kid_label = st.radio(
                "Kid",
                kid_labels,
                horizontal=True,
                key=f"{action.lower()}_kid_radio",
            )
            kid = kids.iloc[kid_labels.index(selected_kid_label)]
            render_selected_kid_balances(kid["kid_id"])

            if action == "Transfer":
                st.markdown('<div class="detail-radio-anchor"></div>', unsafe_allow_html=True)
                from_bucket = st.radio(
                    "From",
                    ["Spend", "Save"],
                    horizontal=True,
                    key="transfer_from_bucket_radio",
                )
                to_bucket = "Save" if from_bucket == "Spend" else "Spend"
                st.markdown(f'<div class="activity-to-text">To: <strong>{to_bucket}</strong></div>', unsafe_allow_html=True)

                amount_text = st.text_input("Amount", key="transfer_amount_text", placeholder="0.00")
                amount = parse_amount(amount_text)
                comment = st.text_input("Comment", value="", key="transfer_comment")

                if st.button("SAVE"):
                    if amount is None:
                        st.warning("Enter a valid amount.")
                    elif add_ledger(kid, "Transfer", amount, from_bucket=from_bucket, to_bucket=to_bucket, comment=comment):
                        st.session_state.activity_saved = True
                        st.session_state.activity_action = None
                        for key in ["activity_action_radio", "transfer_amount_text", "transfer_comment", "transfer_kid_radio"]:
                            st.session_state.pop(key, None)
                        st.rerun()
                    else:
                        st.warning("Enter an amount before saving.")

            elif action == "Bonus":
                st.markdown('<div class="detail-radio-anchor"></div>', unsafe_allow_html=True)
                bucket = st.radio(
                    "Bucket",
                    ["Spend", "Save"],
                    horizontal=True,
                    key="bonus_bucket_radio",
                )

                amount_text = st.text_input("Amount", key="bonus_amount_text", placeholder="0.00")
                amount = parse_amount(amount_text)
                comment = st.text_input("Comment", value="", key="bonus_comment")

                if st.button("SAVE"):
                    if amount is None:
                        st.warning("Enter a valid amount.")
                    elif add_ledger(kid, "Bonus", amount, to_bucket=bucket, comment=comment):
                        st.session_state.activity_saved = True
                        st.session_state.activity_action = None
                        for key in ["activity_action_radio", "bonus_amount_text", "bonus_comment", "bonus_kid_radio"]:
                            st.session_state.pop(key, None)
                        st.rerun()
                    else:
                        st.warning("Enter an amount before saving.")

            elif action == "Adjustment":
                st.markdown('<div class="detail-radio-anchor"></div>', unsafe_allow_html=True)
                bucket = st.radio(
                    "Bucket",
                    ["Spend", "Save"],
                    horizontal=True,
                    key="adjustment_bucket_radio",
                )

                amount_text = st.text_input("Amount — use negative to reduce", key="adjustment_amount_text", placeholder="0.00")
                amount = parse_amount(amount_text)
                comment = st.text_input("Comment", value="", key="adjustment_comment")

                if st.button("SAVE"):
                    if amount is None:
                        st.warning("Enter a valid amount.")
                    elif add_ledger(kid, "Adjustment", amount, to_bucket=bucket, comment=comment):
                        st.session_state.activity_saved = True
                        st.session_state.activity_action = None
                        for key in ["activity_action_radio", "adjustment_amount_text", "adjustment_comment", "adjustment_kid_radio"]:
                            st.session_state.pop(key, None)
                        st.rerun()
                    else:
                        st.warning("Enter a positive or negative amount before saving.")

elif page == "FAMILY SETTINGS":
    
    
    edit_kids = kids.copy().drop(columns=[col for col in ["kid_id", "save_percent"] if col in kids.columns])
    edited = st.data_editor(
        edit_kids,
        hide_index=True,
        width="stretch",
        column_config={
                        "display_order": st.column_config.NumberColumn("Order", min_value=0, step=1),
            "name": st.column_config.TextColumn("Name"),
            "icon": st.column_config.TextColumn("Icon"),
            "allowance": st.column_config.NumberColumn(
                "Allowance",
                min_value=0.0,
                step=1.0,
                format="$%.2f",
            ),
                    },
        disabled=["kid_id"],
    )

    if st.button("SAVE"):
        save_kids(edited)
        st.success("Family settings saved.")
        st.rerun()


elif page == "LEDGER":
    

    ledger = load_ledger()

    if ledger.empty:
        st.info("No ledger entries yet.")
    else:
        kid_filter = st.selectbox(
            "Filter kid",
            ["All"] + [f"{row.icon} {row.name}" for row in kids.itertuples()],
            label_visibility="collapsed",
        )

        show = ledger.copy()

        if kid_filter != "All":
            selected_name = kid_filter.split(" ", 1)[1]
            show = show[show["kid_name"] == selected_name]

        ledger_display = show[["entry_date", "kid_name", "entry_type", "amount", "from_bucket", "to_bucket", "comment"]].rename(
            columns={
                "entry_date": "Date",
                "kid_name": "Kid",
                "entry_type": "Activity",
                "amount": "Amount",
                "from_bucket": "From",
                "to_bucket": "To",
                "comment": "Comment",
            }
        )

        st.dataframe(
            ledger_display,
            width="stretch",
            hide_index=True,
        )

