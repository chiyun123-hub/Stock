create table if not exists market_data (
    ticker text not null,
    date date not null,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume bigint,
    primary key (ticker, date)
);

create table if not exists model_runs (
    id uuid primary key default gen_random_uuid(),
    ticker text not null,
    trained_at timestamptz not null default now(),
    features jsonb,
    metrics jsonb
);

create table if not exists backtest_results (
    id uuid primary key default gen_random_uuid(),
    model_run_id uuid references model_runs(id),
    ticker text not null,
    period_start date not null,
    period_end date not null,
    direction_accuracy double precision,
    cumulative_return double precision,
    max_drawdown double precision
);
