# parser.py
import re
COMPARE_OPS = ['>=', '<=', '!=', '=', '<', '>']

class SQLParseError(Exception):
    pass

def _strip_semicolon(s: str) -> str:
    return s.strip().rstrip(';').strip()

def parse(sql: str):
    if not sql or not sql.strip():
        raise SQLParseError("Empty query")

    s = _strip_semicolon(sql)
    s_clean = s.strip()

    where_part = None
    where_match = re.search(r'\bWHERE\b', s_clean, flags=re.IGNORECASE)
    if where_match:
        where_part = s_clean[where_match.end():].strip()
        s_before_where = s_clean[:where_match.start()].strip()
    else:
        s_before_where = s_clean

    m_from = re.search(r'\bFROM\b\s+([^\s;]+)', s_before_where, flags=re.IGNORECASE)
    if not m_from:
        raise SQLParseError("Missing FROM clause")
    table = m_from.group(1).strip()

    m_select = re.search(r'^\s*\bSELECT\b\s+(.+?)\s+\bFROM\b', s_before_where, flags=re.IGNORECASE | re.DOTALL)
    if not m_select:
        raise SQLParseError("Malformed SELECT clause")
    select_part = m_select.group(1).strip()

    if select_part == '*':
        select_cols = ['*']
    else:
        parts = []
        buf = ''
        depth = 0
        for ch in select_part:
            if ch == ',' and depth == 0:
                parts.append(buf.strip())
                buf = ''
            else:
                buf += ch
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth = max(0, depth - 1)
        if buf.strip():
            parts.append(buf.strip())
        select_cols = parts

    # Parse WHERE single condition
    where = None
    if where_part:
        # remove trailing semicolon if any:
        where_part = where_part.rstrip(';').strip()
        op = None
        for o in COMPARE_OPS:
            if o in where_part:
                op = o
                break
        if not op:
            raise SQLParseError("Unsupported or missing operator in WHERE clause")
        left, right = where_part.split(op, 1)
        col = left.strip()
        val_raw = right.strip()
        # handle quoted strings
        if (val_raw.startswith("'") and val_raw.endswith("'")) or (val_raw.startswith('"') and val_raw.endswith('"')):
            val = val_raw[1:-1]
        else:
            # try to parse number
            try:
                if '.' in val_raw:
                    val = float(val_raw)
                else:
                    val = int(val_raw)
            except Exception:
                # fallback to raw string
                val = val_raw
        where = {'col': col, 'op': op, 'val': val}

    return {'select': select_cols, 'from': table, 'where': where}
