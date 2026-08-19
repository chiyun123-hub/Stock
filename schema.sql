-- Drop the pre-existing predictions table (different schema: prediction_date/
-- target_date/direction/confidence, FK to `stocks`) before recreating ours.
drop table if exists predictions cascade;

create table if not exists predictions (
    id bigint generated always as identity primary key,
    date date not null,
    ticker text not null,
    prediction text not null,
    reason text,
    created_at timestamptz not null default now(),
    unique (date, ticker)
);
