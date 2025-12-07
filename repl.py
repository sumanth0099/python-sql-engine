# repl.py
from storage import Storage
from engine import Engine, ExecutionError

PROMPT = '> '

def format_table(columns, rows):
    if not columns:
        return "(no columns)"
    widths = [len(str(c)) for c in columns]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell) if cell is not None else ''))
    sep = '  '
    header = sep.join(str(c).ljust(widths[i]) for i, c in enumerate(columns))
    lines = [header]
    for row in rows:
        line = sep.join((str(cell) if cell is not None else '').ljust(widths[i]) for i, cell in enumerate(row))
        lines.append(line)
    return '\n'.join(lines)

def repl():
    storage = Storage()
    engine = Engine(storage)

    print("Mini SQL REPL — type 'exit' or 'quit' to leave.")
    print("Note:To load csv file through name it should be in root directory")
    print("sample is an csv file which is already in root directory")
    print("You can try entering name as sample.csv")
    csv_file = input("Enter CSV filename to load: ").strip()

    try:
        tblname, rcount, ccount = storage.load_csv(csv_file)
        print(f"Loaded table '{tblname}' ({rcount} rows, {ccount} cols)")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return

    print("You can now enter SQL queries.")
    print("Example:-SELECT * FROM employees;")
    print()

    while True:
        try:
            s = input(PROMPT).strip()
        except EOFError:
            print()
            break

        if not s:
            continue

        if s.lower() in ('exit', 'quit'):
            print("Bye!")
            break

        # Extra: Allow loading more CSVs using .load
        if s.startswith('.load'):
            parts = s.split()
            if len(parts) < 2:
                print("Usage: .load <path> [tablename]")
                continue
            path = parts[1]
            name = parts[2] if len(parts) >= 3 else None
            try:
                tblname, rcount, ccount = storage.load_csv(path, name)
                print(f"Loaded table '{tblname}' ({rcount} rows, {ccount} cols)")
            except Exception as e:
                print(f"Error loading CSV: {e}")
            continue

        # Show loaded tables
        if s.startswith('.tables'):
            for t in storage.list_tables():
                print(t)
            continue

        # Show schema of a table
        if s.startswith('.schema'):
            parts = s.split()
            if len(parts) < 2:
                print('Usage: .schema <table>')
                continue
            tbl = parts[1]
            try:
                cols = storage.schema(tbl)
                print(', '.join(cols))
            except Exception as e:
                print(e)
            continue

        # If not command → treat as SQL
        try:
            res = engine.execute(s)
            cols = res['columns']
            rows = res['rows']
            print(format_table(cols, rows))
        except ExecutionError as e:
            print(f"Execution error: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    repl()
