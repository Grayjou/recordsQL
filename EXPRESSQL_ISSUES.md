# Issues to Report to expressQL

This document tracks test cases that were skipped or failed in recordsQL due to limitations in the expressQL library. These should be reported as issues or feature requests to the expressQL project.

## 1. NULL Value Handling

**Issue:** The expressQL library cannot handle `None` (NULL) values in comparisons.

**Error:** `TypeError: float() argument must be a string or a real number, not 'NoneType'`

**Location:** `expressQL/validators.py:9` in the `is_number()` function

**Impact:** Cannot create queries with NULL checks, which are common in SQL:
```python
# This fails:
email = col("email")
query = DELETE().FROM("users").WHERE(email == None)
```

**Expected SQL Output:**
```sql
DELETE FROM "users" WHERE email IS NULL
```

**Skipped Tests:**
- `tests/test_delete.py::TestDeleteAdvanced::test_delete_with_null_check`
- `tests/test_exists.py::TestExistsAdvanced::test_exists_with_null_check`
- `tests/test_update.py::TestUpdateAdvanced::test_update_null_value`

**Suggested Fix:**
The `is_number()` function in expressQL should handle None values gracefully:
```python
def is_number(s):
    """
    Check if the string s can be converted to a float.
    This is a simple check and does not cover all edge cases.
    """
    if s is None:
        return False
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False
```

Or better yet, add explicit NULL handling in SQLExpression:
```python
def __eq__(self, other):
    if other is None:
        # Return a special IS NULL condition
        return SQLCondition(f"{self.expression_value} IS NULL", [], True)
    # ... existing logic
```

## 2. set_expr() API Unclear

**Issue:** The `set_expr()` function API is not well documented and appears to take only one argument, but use cases suggest it should take multiple arguments.

**Current Signature:** `set_expr()` takes 1 positional argument

**Expected Use Case:**
```python
from recordsQL import UPDATE, set_expr, col

# Want to increment a value
query = UPDATE("products").SET(stock=set_expr("stock + ?", 10)).WHERE(
    col("id") == 1
)
```

**Expected SQL Output:**
```sql
UPDATE "products" SET stock = stock + ? WHERE id = ?
-- Parameters: [10, 1]
```

**Skipped Tests:**
- `tests/test_update.py::TestUpdateAdvanced::test_update_increment_value`

**Suggested Fix:**
Document the correct API for `set_expr()` or add support for expression-based SET clauses with placeholders.

## 3. Column Selection in SELECT Queries

**Observation (Not a Bug):** When using `cols()` to create column references, passing them to `SELECT()` doesn't include them in the SQL output.

**Current Behavior:**
```python
name, age, email = cols("name", "age", "email")
query = SELECT(name, age, email).FROM("users")
# Outputs: SELECT * FROM "users"
```

**Workaround:**
Use string column names instead:
```python
query = SELECT("name", "age", "email").FROM("users")
# Outputs: SELECT name, age, email FROM "users"
```

**Impact:** This is unexpected behavior but has a simple workaround. The `cols()` function creates SQLExpression objects that are meant for WHERE clauses, not for column selection.

**Suggested Enhancement:**
Either:
1. Make `SELECT()` accept SQLExpression column objects and extract their names, OR
2. Clearly document that `cols()` is only for WHERE/HAVING clauses and that SELECT should use string column names

## 4. Float to Integer Conversion in num()

**Observation (Not a Bug):** The `num()` function rounds floating-point numbers to integers.

**Current Behavior:**
```python
threshold = num(99.99)
print(threshold)  # Num(99)
```

**Impact:** Cannot use precise decimal values in queries when using `num()`.

**Workaround:** Use the value directly:
```python
price = col("price")
query = SELECT().FROM("products").WHERE(price > 99.99)
# This works fine
```

**Suggested Enhancement:**
Document this behavior clearly, or modify `num()` to preserve decimal precision:
```python
def num(value):
    """Create a numeric SQL expression."""
    if isinstance(value, float):
        return Num(value)  # Preserve float
    return Num(int(value))
```

## 5. GROUP BY with SQLExpression Objects

**Observation (Not a Bug):** Similar to SELECT, GROUP BY requires string column names, not SQLExpression objects from `cols()`.

**Current Behavior:**
```python
department = col("department")
query = SELECT("department").FROM("employees").GROUP_BY(department)
# Outputs: SELECT department FROM "employees" GROUP BY *
```

**Workaround:**
```python
query = SELECT("department").FROM("employees").GROUP_BY("department")
# Outputs: SELECT department FROM "employees" GROUP BY department
```

**Suggested Enhancement:**
Make GROUP BY (and HAVING, ORDER BY) accept SQLExpression objects and extract their column names.

## Summary

The main critical issue is **#1 (NULL handling)**, which prevents common SQL patterns from working. The other issues are either:
- Missing documentation (set_expr API)
- API design choices that could be improved (column selection, GROUP BY)
- Intentional behavior that needs documentation (num() rounding)

## Reproduction

To reproduce these issues:
1. Clone recordsQL: `git clone https://github.com/Grayjou/recordsQL.git`
2. Install dependencies: `poetry install`
3. Run the full test suite: `poetry run pytest tests/ -v`
4. Check the skipped tests for expressQL limitations

## Environment

- Python: 3.8.1+
- expressQL: ^0.2.4
- recordsQL: 0.1.0
