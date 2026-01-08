CREATE TABLE IF NOT EXISTS maker_sheet_rows (
  id BIGSERIAL PRIMARY KEY,
  sheet_name TEXT NOT NULL,
  row_data JSONB NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_maker_sheet_rows_sheet_name
  ON maker_sheet_rows(sheet_name);
