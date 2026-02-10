import pandas as pd

DEFAULT_EXCLUDED_TABS = {"form responses", "responses"}


def load_sheets_data(sheet_id, client, excluded_tabs=None):
    spreadsheet = client.open_by_key(sheet_id)
    frames = []
    skip_tabs = {
        tab.strip().lower() for tab in (excluded_tabs or DEFAULT_EXCLUDED_TABS)
    }
    for ws in spreadsheet.worksheets():
        if ws.title.strip().lower() in skip_tabs:
            continue
        records = ws.get_all_records()
        if records:
            df = pd.DataFrame(records)
            df["worksheet"] = ws.title
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
