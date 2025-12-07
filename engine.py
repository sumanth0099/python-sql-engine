# engine.py
from typing import Any, Dict
from storage import Storage, TableNotFound
from parser import parse, SQLParseError

class ExecutionError(Exception):
    pass

def _coerce_value(v: Any):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if s == '':
        return None
    # try int then float
    try:
        if '.' in s:
            return float(s)
        return int(s)
    except Exception:
        return s

def _compare(left, op, right):
    if isinstance(right, (int, float)):
        try:
            left_num = None if left is None else float(left)
            left = left_num
        except Exception:
            pass

    # handle None comparisons
    if left is None:
        if right is None:
            if op == '=':
                return True
            elif op == '!=':
                return False
            else:
                return False
        else:
            return op == '!='

    try:
        if op == '=':
            return left == right
        if op == '!=':
            return left != right
        if op == '>':
            return left > right
        if op == '<':
            return left < right
        if op == '>=':
            return left >= right
        if op == '<=':
            return left <= right
    except TypeError:
        raise ExecutionError(f"Type error comparing {left!r} {op} {right!r}")
    raise ExecutionError(f"Unsupported operator: {op}")

class Engine:
    def __init__(self, storage: Storage):
        self.storage = storage

    def execute(self, sql: str) -> Dict[str, Any]:
        try:
            q = parse(sql)
        except SQLParseError as e:
            raise ExecutionError(f"Parse error: {e}")

        tbl_name = q['from']
        try:
            tbl = self.storage.get_table(tbl_name)
        except TableNotFound as e:
            raise ExecutionError(str(e))

        cols = tbl['columns']
        rows = tbl['rows']

        # Apply WHERE (single condition)
        filtered = []
        if q['where']:
            w = q['where']
            if w['col'] not in cols:
                raise ExecutionError(f"Column '{w['col']}' not found in table '{tbl_name}'")
            for r in rows:
                raw_left = r.get(w['col'])
                left = _coerce_value(raw_left)
                right = w['val']
                res = _compare(left, w['op'], right)
                if res:
                    filtered.append(r)
        else:
            filtered = rows

        # Aggregation COUNT
        select = q['select']
        if len(select) == 1 and select[0].upper().startswith('COUNT'):
            inside = select[0][select[0].find('(')+1: select[0].rfind(')')].strip()
            if inside == '*':
                cnt = len(filtered)
            else:
                if inside not in cols:
                    raise ExecutionError(f"Column '{inside}' not found for COUNT()")
                cnt = 0
                for r in filtered:
                    v = r.get(inside)
                    if v is not None and str(v).strip() != '':
                        cnt += 1
            return {'columns': ['count'], 'rows': [[cnt]]}

        # Projection
        if select == ['*']:
            out_cols = cols
        else:
            out_cols = []
            for c in select:
                if '(' in c and ')' in c:
                    raise ExecutionError(f"Unsupported function in SELECT: {c}")
                if c not in cols:
                    raise ExecutionError(f"Column '{c}' not found in table '{tbl_name}'")
                out_cols.append(c)

        out_rows = [[r.get(c) for c in out_cols] for r in filtered]
        return {'columns': out_cols, 'rows': out_rows}
