# Scoops & Stats

A PySide6 desktop app with an embedded Matplotlib chart and a cheerful summer
theme. CSV loading is intentionally left as a placeholder for your own data
handling.

## Run

```powershell
uv sync
uv run python main.py
```

The app loads its separate stylesheet from `style.qss`.

Replace the placeholder GitHub URL in the About dialog and implement
`IceCreamChartWindow.load_csv_placeholder()` in `main.py` when you are ready
to connect your CSV data.