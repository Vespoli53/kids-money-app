# Pierce Family Allowance

A Streamlit family allowance tracker backed by PostgreSQL/Supabase.

## Configuration

Set these values in Streamlit Community Cloud secrets (or in an ignored local
`.streamlit/secrets.toml` file):

```toml
DATABASE_URL = "postgresql://..."
APP_PIN = "..."
```

Never commit `secrets.toml`; it is intentionally ignored by Git.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run allowance.py
```

## Supabase schema updates

Database DDL belongs in `supabase/migrations`, not in the Streamlit app. Apply
the migrations with the Supabase CLI after linking the project:

```powershell
supabase db push
```

The app stores the Hustle bucket as the legacy database value `Invest` so it
also remains compatible before the included migration is applied.
