# BACT7501 Software Development Project - Assessment 2
## Comprehensive Software Development Life Cycle (SDLC) & Technical Report

**Student Name:** Lakshaya Chaudhry  
**Course Code:** BACT7501  
**Project Title:** Enterprise Object-Oriented Purchase Requisition System  
**Repository Link:** [https://github.com/lakshyachaudhry456-lab/Software-Development-Project](https://github.com/lakshyachaudhry456-lab/Software-Development-Project)  

---

## 1. Academic Integrity Declaration
> "The work presented in this assessment is to the best of my knowledge original, except as acknowledged in the text, and the material has not already been submitted, either in whole or in part, for any academic award at this or any other tertiary institution. I promise not to share this assessment in part or whole with any other student at Whitecliffe or outside this campus."

---

## 2. GitHub Repository & Commit Progression

A dedicated Git repository was maintained throughout development to record the incremental evolution of the codebase from an initial procedural migration to a mature, multi-class object-oriented architecture.

- **Public Repository URL:**  
  `https://github.com/lakshyachaudhry456-lab/Software-Development-Project`

### Commit Progression & Design Analysis

| Commit # | Summary | What Changes Were Made | Why Necessary | Software Design Principle(s) |
|---|---|---|---|---|
| **Commit 1** | Initial Requisition Prototype | Created initial `RequisitionSystem` class, `__init__` constructor, `add_requisition` and `approve_requisition` methods with a global counter. | Migrated procedural functions from Assessment 1 to establish baseline OOP functionality. | **Encapsulation:** Grouped related staff attributes and operations into an initial class structure. |
| **Commit 2** | Manager Response & Aggregate Statistics | Implemented `respond_requisition()`, bulk display, and `requisition_statistics()`. Added 5 scenario tests. | Enabled management review workflows for high-value requests and provided organizational oversight. | **Separation of Concerns:** Separated data entry from administrative decision-making and reporting. |
| **Commit 3** | Exact Output Formatting & Input Validation | Standardized console output strings, added `try-except` validation for item prices, and synchronized status transitions. | Met exact rubric specifications and prevented fatal runtime crashes on malformed user input. | **Defensive Programming:** Handled non-numeric inputs and edge-case boundaries gracefully. |
| **Commit 4** | Two-Class Architectural Refactoring & Assertions | Separated entity (`Requisition`) from system manager (`RequisitionSystem`), added property encapsulation, status constants, boundary testing, and 10 assertion unit tests. | Addressed code review feedback: prevented overturning approved requisitions, fixed unsubmitted object registration, and introduced rigorous testing. | **Single Responsibility Principle (SRP) & Data Hiding:** Clear decoupling between entity data management and system orchestration. |

---

## 3. Detailed Software Development Life Cycle (SDLC) Application

The solution was engineered following an iterative Waterfall/Agile-hybrid SDLC model, ensuring that each phase was backed by rigorous analysis, design documentation, and empirical verification.

```
+---------------+      +------------------+      +----------------+
|  1. Planning  | ---> |  2. Analysis     | ---> |   3. Design    |
+---------------+      +------------------+      +----------------+
                                                         |
+---------------+      +------------------+              |
| 6. Maintenance|<---  |  5. Testing      | <------------+
| & Deployment  |      |  (10 Assertions) |      | 4. Implementation|
+---------------+      +------------------+      +------------------+
```

### Stage 1: Planning
- **Problem Statement:** Organizations require an auditable, transparent procurement workflow where low-value purchases are auto-approved to minimize administrative bottlenecks, while high-value purchases ($\ge \$500$) are routed for managerial sign-off.
- **Architectural Scope:** Evolve beyond monolithic procedural scripts into an extensible, two-tier object-oriented architecture:
  1. An independent **`Requisition`** entity modeling domain attributes and state transitions.
  2. A **`RequisitionSystem`** controller orchestrating sequential identity allocation, interactive I/O, persistence, and reporting.
- **Feasibility & Trade-offs:** Evaluated whether to store requisitions within a single class or decouple entity from controller. A decoupled two-class design was chosen because it cleanly adheres to the Single Responsibility Principle and eliminates state leakage.

### Stage 2: Requirements Analysis
- **Functional Requirements:**
  1. *Staff Data Entry:* Capture date, staff ID, staff name, and itemized lists of items with individual costs.
  2. *Sequential Identity:* Assign unique sequential requisition IDs starting from `10001` exclusively upon valid submission.
  3. *Automated Rule-Based Approval:*
     - If total cost $< \$500$: Automatically assign `Approved` status and generate reference (`StaffID + last 3 digits of RequisitionID`).
     - If total cost $\ge \$500$: Default to `Pending` status with reference `Not available`.
  4. *Managerial Review Restrictions:*
     - Managers may only review and update requisitions that are currently `Pending`.
     - An already `Approved` or `Not approved` requisition cannot be overturned.
     - Unrecognized or misspelled inputs (e.g., `"Aproved"`) must be rejected without altering existing state.
  5. *Live Statistics Synchronization:* Report total submitted, approved, pending, and not approved counts. Updating a pending requisition dynamically decrements pending and increments approved or not approved counts.
- **Non-Functional Requirements:**
  - *Data Integrity:* Prevent negative prices, blank names, or direct mutation of private attributes.
  - *Zero Regression:* Automated unit tests with explicit assertions must pass on every build.

### Stage 3: System & Object-Oriented Design

#### Architectural Class Structure
```
+-------------------------------------------------------------+
|                        Requisition                          |
+-------------------------------------------------------------+
| - _requisition_id: int                                      |
| - _date: str                                                |
| - _staff_id: str                                            |
| - _staff_name: str                                          |
| - _items: list[dict]                                        |
| - _total: float                                             |
| - _status: str                                              |
| - _approval_reference: str                                  |
+-------------------------------------------------------------+
| + set_items(items: list): void                              |
| + requisitions_details(): dict                              |
| + approve_requisition(): str                                |
| + respond_requisition(decision: str): str                   |
| + display_requisition(): void                               |
+-------------------------------------------------------------+
                               ^
                               | manages 1..*
+-------------------------------------------------------------+
|                     RequisitionSystem                       |
+-------------------------------------------------------------+
| - _requisitions: list[Requisition]                          |
+-------------------------------------------------------------+
| + add_requisition(date, staff_id, staff_name, items): Req   |
| + find_requisition(requisition_id: int): Requisition        |
| + respond_to_requisition(id: int, decision: str): str       |
| + display_requisitions(): void                              |
| + requisition_statistics(): dict                            |
+-------------------------------------------------------------+
```

#### State Transition Logic
```
       [ Submission ]
             |
             v
      Total < $500?
      /           \
   (Yes)          (No)
    /               \
   v                 v
[ Approved ]    [ Pending ]
 (Terminal)          |
                     +---> Manager: "Approved"     ---> [ Approved ] (Terminal)
                     +---> Manager: "Not approved" ---> [ Not approved ] (Terminal)
                     +---> Manager: "Pending"      ---> [ Pending ] (Unchanged)
```

### Stage 4: Implementation
- **Status Constants:** Defined `STATUS_APPROVED`, `STATUS_PENDING`, `STATUS_NOT_APPROVED`, and `STATUS_NOT_AVAILABLE` as module-level constants to eliminate brittle string literal duplication.
- **True Encapsulation:** Protected all core instance variables (`_status`, `_total`, `_approval_reference`) behind read-only `@property` getters, preventing external tampering.
- **Defensive Data Handling:** The `set_items()` method enforces non-empty strings, validates float conversions, and rejects negative values before total calculation.

### Stage 5: Testing & Debugging Strategy

To satisfy rigorous code execution criteria, testing was expanded beyond terminal print statements into an automated test harness (`run_unit_tests()`) with explicit `assert` statements covering boundary conditions and negative scenarios.

#### Automated Test Suite (10 Assertions)
| # | Test Scenario | Input Data | Expected Result | Assertion Verified |
|---|---|---|---|:---:|
| 1 | Zero-Cost Boundary | Item cost = $0.00 | Status: `Approved` ($0 < $500) | `assert r.status == "Approved"` |
| 2 | Boundary: $499.99 | Item cost = $499.99 | Status: `Approved`, Ref generated | `assert r.status == "Approved"` |
| 3 | Boundary: Exactly $500.00 | Item cost = $500.00 | Status: `Pending`, Ref `Not available` | `assert r.status == "Pending"` |
| 4 | Boundary: $500.01 | Item cost = $500.01 | Status: `Pending`, Ref `Not available` | `assert r.status == "Pending"` |
| 5 | Multi-Item Aggregation | Mouse ($25.50) + Keyboard ($74.50) | Total = $100.00, Status: `Approved` | `assert r.total == 100.0` |
| 6 | Overturn Protection | Manager attempts to reject $100 Approved req | Raises `ValueError` ("Action Denied") | Handled via `try-except` |
| 7 | Typo Handling | Manager submits misspelled `"Aproved"` | Raises `ValueError`, status stays `Pending` | Handled via `try-except` |
| 8 | Valid Approval Response | Manager approves Pending $500 req | Status: `Approved`, Ref: `T03003` | `assert r.status == "Approved"` |
| 9 | Valid Rejection Response | Manager rejects Pending $500.01 req | Status: `Not approved`, Ref `Not available`| `assert r.status == "Not approved"` |
| 10 | Negative Input Validation | Item cost = -$50.00 | Raises `ValueError` ("cannot be negative") | Handled via `try-except` |

#### Main 5-Scenario Demonstration
The program subsequently executes the 5 required real-world scenarios utilizing itemized product descriptions and prices:
- **Req 1 (ID 10001, $450):** Paper ($50) + Toner ($400) $\rightarrow$ `Approved`, Ref: `FN19001`
- **Req 2 (ID 10002, $490):** Keyboard ($140) + Chair ($350) $\rightarrow$ `Approved`, Ref: `FN02002`
- **Req 3 (ID 10003, $1000):** Motorized Standing Desk ($1000) $\rightarrow$ Initially `Pending` $\rightarrow$ Left as `Pending`
- **Req 4 (ID 10004, $3500):** Database Server Hardware ($3500) $\rightarrow$ Initially `Pending` $\rightarrow$ Manager marks `Not approved`
- **Req 5 (ID 10005, $850):** 4K Projector ($800) + Mount ($50) $\rightarrow$ Initially `Pending` $\rightarrow$ Manager marks `Approved`, Ref: `FN33005`

### Stage 6: Deployment & Maintenance
- **Packaging:** Standalone Python script executable in any Python 3.8+ environment without external pip dependencies.
- **Future Roadmap:**
  - Graphical User Interface (GUI) binding using Tkinter.
  - Persistent SQLite database integration replacing in-memory storage.
  - Role-Based Access Control (RBAC) separating Staff and Manager login permissions.

---

## 4. Error and Challenge Log (Screenshots & Explanations)

*Note: Timestamped full-screen screenshots showing the computer date and time must be inserted below each description.*

```
+-------------------------------------------------------------------------+
|                                                                         |
|                [ INSERT FULL-SCREEN TIMESTAMPED SCREENSHOT ]            |
|                                                                         |
|  (Ensure terminal traceback AND system taskbar clock/date are visible) |
+-------------------------------------------------------------------------+
```

### Challenge / Error 1: UnboundLocalError with Module-Level Variable
- **Screenshot Placeholder 1:**  
  *(Insert full-screen screenshot of `error1_unbound_local.py` execution showing the traceback)*
- **1. What the error was:**  
  `UnboundLocalError: cannot access local variable 'requisition_counter' where it is not associated with a value`.
- **2. What caused it:**  
  Inside the `add_requisition` method, `requisition_counter = requisition_counter + 1` was executed. Because Python encountered an assignment, it treated `requisition_counter` as a local function variable rather than reading the module-level global variable.
- **3. How it was solved:**  
  Added the `global requisition_counter` statement at the beginning of the method to inform the Python interpreter to modify the global variable.

---

### Challenge / Error 2: TypeError on Direct Integer Slicing
- **Screenshot Placeholder 2:**  
  *(Insert full-screen screenshot of `error2_int_subscript.py` execution showing the traceback)*
- **1. What the error was:**  
  `TypeError: 'int' object is not subscriptable`.
- **2. What caused it:**  
  When constructing the approval reference string (`self.staff_id + self.requisition_id[-3:]`), the `requisition_id` was stored as an integer (`10001`). Python integer types do not support slice indexing.
- **3. How it was solved:**  
  Explicitly converted `self.requisition_id` to a string before slicing: `str(self.requisition_id)[-3:]`, enabling string concatenation with `self.staff_id`.

---

### Challenge / Error 3: ValueError During Item Cost Input
- **Screenshot Placeholder 3:**  
  *(Insert full-screen screenshot of `error3_value_error.py` execution showing the traceback)*
- **1. What the error was:**  
  `ValueError: could not convert string to float: '$150'`.
- **2. What caused it:**  
  Staff members frequently typed symbols (such as `$`) or non-numeric words when prompted for item prices. The unchecked `float(input())` call immediately crashed the program.
- **3. How it was solved:**  
  Encapsulated input parsing in a `try...except ValueError` validation loop that reprompts the user until a valid positive numerical amount is entered.

---

## 5. Critical Reflection on Object-Oriented Principles

1. **Separation of Concerns & Modularity:**  
   The initial prototype combined entity data storage and collection management into a single monolithic class. By refactoring into `Requisition` (entity) and `RequisitionSystem` (service controller), each class now has a single, well-defined reason to change. The `Requisition` class knows only how to validate its items and transition its internal status; the `RequisitionSystem` class manages collection indexing, ID generation, and reporting.

2. **Data Encapsulation & Immutability:**  
   Transitioning internal attributes to protected members (`_total`, `_status`, `_approval_reference`) accessible only via read-only properties guarantees that business rules cannot be bypassed. External scripts cannot arbitrarily modify a status from `Pending` to `Approved` without invoking `respond_requisition()`, ensuring that audit reference codes are always generated in lockstep with status changes.

3. **Defensive Design & Robustness:**  
   Code review highlighted that early drafts permitted managers to overturn auto-approved items and allowed typos to silently reset statuses. Enforcing state preconditions (`if self._status != STATUS_PENDING: raise ValueError`) and validating against explicit constants protects data integrity under real-world usage.
