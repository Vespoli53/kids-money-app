-- Apply schema changes once during deployment, never from a Streamlit rerun.
-- The app continues writing the legacy value "Invest" for compatibility and
-- presents Invest, Investment, and Hustle as "Hustle" in the UI.

begin;

alter table public.ledger
    drop constraint if exists ledger_bucket_check;

alter table public.ledger
    add constraint ledger_bucket_check
    check (
        (from_bucket is null or from_bucket in ('Spend', 'Save', 'Give', 'Hustle', 'Invest', 'Investment'))
        and
        (to_bucket is null or to_bucket in ('Spend', 'Save', 'Give', 'Hustle', 'Invest', 'Investment'))
    ) not valid;

alter table public.ledger
    drop constraint if exists ledger_transfer_rules;

alter table public.ledger
    add constraint ledger_transfer_rules
    check (
        (
            entry_type = 'Transfer'
            and amount > 0
            and from_bucket in ('Spend', 'Save', 'Give', 'Hustle', 'Invest', 'Investment')
            and to_bucket in ('Spend', 'Save', 'Give', 'Hustle', 'Invest', 'Investment')
            and from_bucket <> to_bucket
        )
        or
        (
            entry_type in ('Allowance', 'Bonus', 'Adjustment')
            and from_bucket is null
            and to_bucket in ('Spend', 'Save', 'Give', 'Hustle', 'Invest', 'Investment')
            and amount <> 0
        )
    ) not valid;

-- Supports the allowance status lookup and the newest-first ledger screen.
create index if not exists ledger_allowance_date_idx
    on public.ledger (entry_date desc)
    where entry_type = 'Allowance';

create index if not exists ledger_entry_ts_idx
    on public.ledger (entry_ts desc, entry_date desc);

commit;
