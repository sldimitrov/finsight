# Algorithm: balance update on create / delete

Based on `accounts/views.py` → `create_transaction` and `transactions/views.py` →
`delete_transaction`. Both run inside `transaction.atomic`: either the transaction row
**and** the balance change are saved, or neither is.

## Create transaction

```mermaid
flowchart TD
    A([Start: POST /accounts/&lt;id&gt;/transactions/create/]) --> B{Logged in?}
    B -- No --> B1[Redirect to login] --> Z([End])
    B -- Yes --> C{Account exists,<br/>belongs to user<br/>and is active?}
    C -- No --> C1[404 Not Found] --> Z
    C -- Yes --> D{Form valid?}
    D -- No --> D1[Re-render form with errors] --> Z
    D -- Yes --> E[[BEGIN atomic]]
    E --> F[Save Transaction row]
    F --> G{Type?}
    G -- income --> H1["balance = balance + amount"]
    G -- expense --> H2["balance = balance − amount"]
    G -- other --> H3[No balance change]
    H1 & H2 & H3 --> I[Save account balance]
    I --> J[[COMMIT]]
    J --> K[Redirect to account details] --> Z
    F -. error .-> R[[ROLLBACK: nothing saved]] --> Z
    I -. error .-> R
```

## Delete transaction (undo its effect)

```mermaid
flowchart TD
    A([Start: /transactions/&lt;id&gt;/delete/]) --> B{Transaction exists<br/>and belongs to user?}
    B -- No --> B1[404 Not Found] --> Z([End])
    B -- Yes --> C{POST?}
    C -- No --> C1[Show confirmation page] --> Z
    C -- Yes --> E[[BEGIN atomic]]
    E --> F[Delete Transaction row]
    F --> G{Type?}
    G -- income --> H1["balance = balance − amount"]
    G -- expense --> H2["balance = balance + amount"]
    G -- other --> H3[No balance change]
    H1 & H2 & H3 --> I[Save account balance]
    I --> J[[COMMIT]]
    J --> K[Redirect to transaction list] --> Z
    F -. error .-> R[[ROLLBACK: row and balance unchanged]] --> Z
    I -. error .-> R
```

Delete is the exact inverse of create, so create followed by delete leaves the balance
where it started. That's a property worth testing and mentioning in the coursework.
