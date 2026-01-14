# 📓 Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-05-12

### 🎉 Added

- Initial release of `recordsql`, a SQL query builder built on top of `expressQL`
- Support for:
  - `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WITH`
  - `INNER`, `LEFT`, `RIGHT`, and `FULL` joins
  - `COUNT`, `EXISTS`, and `ON CONFLICT` clauses
- Fluent, composable Pythonic API for building SQL queries
- Placeholder-based query parameterization for security
- CTE (Common Table Expression) chaining with `WITH` syntax
- Query modifiers like `ORDER_BY`, `LIMIT`, and `OFFSET`
- Utility types: `cols()`, `col()`, `text()`, and `num()`

### 🧪 Examples

- Demonstrative usage of `recordsql` in `main.py`
- Output preview using `.placeholder_pair()` method for SQL + parameters

---

