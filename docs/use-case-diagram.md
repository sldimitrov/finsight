# Use-case diagram

Source: the "FinSight MVP" sketch (5 modules). Use cases marked *(planned)* are not built yet.
Mermaid has no native use-case diagram, so this one uses a flowchart: the actor on the left
and the use cases as rounded nodes grouped by module.

```mermaid
flowchart LR
    User(["👤 User"])
    Guest(["👤 Guest"])

    subgraph M1["① User management"]
        UC1(["Register (planned)"])
        UC2(["Log in / log out"])
        UC3(["Update profile (planned)"])
        UC4(["Set base currency (planned)"])
    end

    subgraph M2["② Account management"]
        UC5(["Create account"])
        UC6(["View own accounts"])
        UC7(["View account details"])
        UC8(["Update account"])
        UC9(["Deactivate account"])
    end

    subgraph M3["③ Transaction management"]
        UC10(["Add income / expense"])
        UC11(["List transactions"])
        UC12(["View transaction details"])
        UC13(["Filter transactions"])
        UC14(["Delete transaction"])
    end

    subgraph M4["④ Category management (planned)"]
        UC15(["Create / edit category"])
        UC16(["Assign category to transaction"])
    end

    subgraph M5["⑤ Financial overview (planned)"]
        UC17(["Total assets / liabilities"])
        UC18(["Income & expenses for period"])
        UC19(["Spending by category"])
        UC20(["Compare months"])
    end

    Guest --- UC1
    Guest --- UC2
    User --- UC2 & UC3 & UC4
    User --- UC5 & UC6 & UC7 & UC8 & UC9
    User --- UC10 & UC11 & UC12 & UC13 & UC14
    User --- UC15 & UC16
    User --- UC17 & UC18 & UC19 & UC20

    UC10 -. "«include» update balance" .-> UC7
    UC14 -. "«include» undo balance" .-> UC7
```

Note: every use case of a logged-in user is limited to **their own data** (data isolation).
