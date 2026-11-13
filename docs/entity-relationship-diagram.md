# Entity-relationship diagram

Source: hand-drawn "Data modeling" sketch + the current models in `users/`, `accounts/`,
`transactions/`. Entities marked *planned* exist only on paper so far.

```mermaid
erDiagram
    USER ||--o{ ACCOUNT : owns
    USER ||--o{ BUDGET : "sets (planned)"
    ACCOUNT ||--o{ TRANSACTION : "account"
    ACCOUNT |o--o{ TRANSACTION : "source_account"
    ACCOUNT |o--o{ TRANSACTION : "destination_account"
    CATEGORY |o--o{ TRANSACTION : "classifies (planned)"
    CATEGORY ||--o{ BUDGET : "limits (planned)"

    USER {
        int id PK
        string username UK
        string email UK
        string password "hash"
        string first_name
        string last_name
        string base_currency "default BGN"
        bool is_active
        datetime date_joined
    }
    ACCOUNT {
        int id PK
        int user_id FK
        string name
        string type "checking | savings | credit | investment"
        decimal balance "12,2 - may be negative"
        string currency "ISO 4217, 3 chars"
        bool is_active
    }
    TRANSACTION {
        int id PK
        int account_id FK
        date date
        string type "income | expense | transfer | adjustment"
        decimal amount "10,2"
        string description
        string category "currently free text"
        int source_account_id FK "nullable, transfers"
        int destination_account_id FK "nullable, transfers"
    }
    CATEGORY {
        int id PK
        string name "planned"
        string kind "income | expense (planned)"
    }
    BUDGET {
        int id PK
        int user_id FK
        int category_id FK
        decimal amount_limit
        date period_start
        date period_end
    }
```

## Notes from the sketch
- Account types: **checking** (everyday money, bills, groceries, subscriptions, transfers),
  **savings** (future use, emergency, goals, interest), **investment** (stocks, bonds, ETFs;
  value changes with the market), **credit** (borrowed money; balance is what you owe).
- Transaction effect on balance: income `+`, expense `−`, transfer `− / +` across two
  accounts, adjustment `±`. A transfer is **not** spending.

## Open design questions (to decide myself)
- The sketch has `Transaction → ExpenseType → ExpenseCategory`. Is a two-level hierarchy
  needed, or is one `Category` (with an income/expense kind, maybe a self-referencing
  parent) enough? The diagram above shows the simpler option only as a placeholder.
- Should categories be global, per-user, or both (defaults + user-defined)?
- For transfers: is `account` the same as `source_account`? Is one row or two rows per
  transfer easier to keep consistent and to report on?
- Should `Account.balance` be stored (fast reads, must be kept in sync) or computed from
  transactions with `aggregate` (always correct, slower)?
- Should `Transaction.amount` be constrained to `> 0` at the database level (`CheckConstraint`)?
