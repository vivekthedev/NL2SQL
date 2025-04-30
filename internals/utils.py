import sqlite3
from typing import Annotated, Any, Union

from pydantic import BaseModel, Field
from typing_extensions import TypeAlias


class Success(BaseModel):
    """Response when SQL could be successfully generated."""

    sql_query: str
    explanation: str = Field(
        "", description="Explanation of the SQL query, as markdown"
    )

class InvalidRequest(BaseModel):
    """Response the user input didn't include enough information to generate SQL."""

    error_message: str


Response: TypeAlias = Union[Success, InvalidRequest]


def get_table_schema(path):
    """Get the schema of the database tables."""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    md_lines = ["# Database Schema\n"]

    md_lines.append("\n")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        md_lines.append(f"## Table: `{table_name}`")
        md_lines.append("\n")
        md_lines.append(
            "| Column Name | Data Type | Not Null | Default Value | Primary Key |"
        )
        md_lines.append("\n")
        md_lines.append(
            "|-------------|-----------|----------|---------------|-------------|"
        )
        md_lines.append("\n")

        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            col_name, col_type, notnull, dflt_value, pk = (
                col[1],
                col[2],
                col[3],
                col[4],
                col[5],
            )
            md_lines.append(
                f"| `{col_name}` | {col_type} | {bool(notnull)} | {dflt_value if dflt_value is not None else ''} | {bool(pk)} |"
            )
            md_lines.append("\n")

    md_lines.append("\n")
    md_lines.append("## End of Schema")
    return "".join(md_lines)
