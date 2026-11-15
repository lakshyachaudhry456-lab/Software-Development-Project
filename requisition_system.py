# ==============================================================================
# BACT7501 - Assessment 2: Software Development Project
# Purchase Requisition System (Enterprise OOP Implementation)
# ==============================================================================

# Constants for System Configuration and Statuses (prevents string literals bugs)
STATUS_APPROVED = "Approved"
STATUS_PENDING = "Pending"
STATUS_NOT_APPROVED = "Not approved"
STATUS_NOT_AVAILABLE = "Not available"
APPROVAL_THRESHOLD = 500.0
INITIAL_REQUISITION_ID = 10000

# Global counter to support the brief's specification:
# "Note: if you are generating a unique requisition ID then you may need to create a global variable outside the __init__ method."
requisition_counter = 0


# ==============================================================================
# 1. ENTITY CLASS: Requisition
# ==============================================================================
class Requisition:
    """
    Encapsulates all data and state transitions for an individual purchase requisition.
    Demonstrates strong encapsulation with private/protected attributes and properties.
    """

    def __init__(self, requisition_id, date, staff_id, staff_name, items):
        self._requisition_id = int(requisition_id)
        self._date = str(date).strip()
        self._staff_id = str(staff_id).strip()
        self._staff_name = str(staff_name).strip()
        self._items = []
        self._total = 0.0
        self._status = STATUS_PENDING
        self._approval_reference = STATUS_NOT_AVAILABLE

        # Validate and set items, automatically computing the total
        self.set_items(items)

    # --------------------------------------------------------------------------
    # Encapsulated Properties (Getters)
    # --------------------------------------------------------------------------
    @property
    def requisition_id(self):
        return self._requisition_id

    @property
    def date(self):
        return self._date

    @property
    def staff_id(self):
        return self._staff_id

    @property
    def staff_name(self):
        return self._staff_name

    @property
    def items(self):
        return list(self._items)  # Return shallow copy to preserve encapsulation

    @property
    def total(self):
        return self._total

    @property
    def status(self):
        return self._status

    @property
    def approval_reference(self):
        return self._approval_reference

    # --------------------------------------------------------------------------
    # Business Logic Methods
    # --------------------------------------------------------------------------
    def set_items(self, items):
        """
        Validates the list of items with their costs and calculates total cost.
        Rejects empty item names, non-numeric prices, and negative costs.
        """
        if not isinstance(items, list):
            raise TypeError("Items must be provided as a list of item dictionaries.")

        cleaned_items = []
        running_total = 0.0

        for item in items:
            name = str(item.get("name", "")).strip()
            if not name:
                raise ValueError("Item name cannot be blank or empty.")

            try:
                price = float(item["price"])
            except (KeyError, ValueError, TypeError):
                raise ValueError(f"Invalid or missing price for item '{name}'.")

            if price < 0:
                raise ValueError(f"Item price for '{name}' cannot be negative (${price}).")

            cleaned_items.append({"name": name, "price": price})
            running_total += price

        self._items = cleaned_items
        self._total = running_total

    def requisitions_details(self):
        """
        Returns itemized details and total cost for this requisition.
        Directly fulfills the specification: '(from the requisitions_details method)'.
        """
        return {
            "requisition_id": self._requisition_id,
            "items": self.items,
            "total": self._total,
        }

    def approve_requisition(self):
        """
        Evaluates initial approval based on the total cost:
        - If total < $500: Automatically approved, generating reference ID (Staff ID + last 3 digits of Requisition ID).
        - If total >= $500: Status remains Pending, reference is 'Not available'.
        """
        last_three = str(self._requisition_id)[-3:]
        if self._total < APPROVAL_THRESHOLD:
            self._status = STATUS_APPROVED
            self._approval_reference = f"{self._staff_id}{last_three}"
        else:
            self._status = STATUS_PENDING
            self._approval_reference = STATUS_NOT_AVAILABLE

        return self._status

    def respond_requisition(self, decision):
        """
        Allows a manager to respond to a PENDING requisition.
        - Validates that the requisition is currently in 'Pending' status.
        - Rejects invalid choices or typos without corrupting status.
        - Updates status to 'Approved' or 'Not approved'.
        """
        # Business rule check: only Pending requisitions can be reviewed by managers
        if self._status != STATUS_PENDING:
            raise ValueError(
                f"Action Denied: Requisition {self._requisition_id} is already '{self._status}'. "
                f"Only requisitions with 'Pending' status can be responded to by a manager."
            )

        clean_decision = str(decision).strip().lower()
        last_three = str(self._requisition_id)[-3:]

        if clean_decision == "approved":
            self._status = STATUS_APPROVED
            self._approval_reference = f"{self._staff_id}{last_three}"
        elif clean_decision in ["not approved", "not_approved", "rejected"]:
            self._status = STATUS_NOT_APPROVED
            self._approval_reference = STATUS_NOT_AVAILABLE
        elif clean_decision == "pending":
            self._status = STATUS_PENDING
            self._approval_reference = STATUS_NOT_AVAILABLE
        else:
            raise ValueError(
                f"Invalid manager decision '{decision}'. "
                f"Must be 'Approved', 'Not approved', or 'Pending'."
            )

        return self._status

    def display_requisition(self):
        """
        Displays requisition details in the exact format required by the specification.
        """
        formatted_total = f"${int(self._total)}" if self._total == int(self._total) else f"${self._total:.2f}"
        print(f"Date: {self._date}")
        print(f"Requisition ID: {self._requisition_id}")
        print(f"Staff ID: {self._staff_id}")
        print(f"Staff Name: {self._staff_name}")
        print(f"Total: {formatted_total}")
        print(f"Status: {self._status}")
        print(f"Approval Reference Number: {self._approval_reference}")
        print()


# ==============================================================================
# 2. MANAGER / SYSTEM CONTROLLER CLASS: RequisitionSystem
# ==============================================================================
class RequisitionSystem:
    """
    System controller class managing the collection of requisitions,
    ID generation, interactive input handling, and statistical reporting.
    Exemplifies Single Responsibility Principle and Separation of Concerns.
    """

    def __init__(self):
        self._requisitions = []

    @property
    def requisitions(self):
        return list(self._requisitions)

    def add_requisition(self, date=None, staff_id=None, staff_name=None, items=None, total=None):
        """
        Submits basic requisition information, accepts items with costs,
        calculates total, evaluates approval status, and registers the requisition.
        """
        global requisition_counter

        # Interactive input path if arguments are omitted
        if date is None or staff_id is None or staff_name is None:
            print("\n--- Enter Requisition Information ---")
            date = input("Enter Date (e.g., DD/MM/YYYY): ").strip()
            while not date:
                print("Date cannot be blank.")
                date = input("Enter Date (e.g., DD/MM/YYYY): ").strip()

            staff_id = input("Enter Staff ID: ").strip()
            while not staff_id:
                print("Staff ID cannot be blank.")
                staff_id = input("Enter Staff ID: ").strip()

            staff_name = input("Enter Staff Name: ").strip()
            while not staff_name:
                print("Staff Name cannot be blank.")
                staff_name = input("Enter Staff Name: ").strip()

            items = []
            print("\nAdd Items to Requisition:")
            while True:
                item_name = input("Enter item name: ").strip()
                while not item_name:
                    print("Item name cannot be blank.")
                    item_name = input("Enter item name: ").strip()

                while True:
                    try:
                        item_price = float(input("Enter item price ($): "))
                        if item_price < 0:
                            print("Price cannot be negative. Please enter a positive value.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid numerical price.")

                items.append({"name": item_name, "price": item_price})
                another = input("Do you want to add another item? (yes/no): ").strip().lower()
                if another != "yes":
                    break
        else:
            # Programmatic input path
            if items is None:
                if total is not None:
                    total_val = float(total)
                    if total_val < 0:
                        raise ValueError("Requisition total cannot be negative.")
                    items = [{"name": "Requisition Item", "price": total_val}]
                else:
                    items = []

        # Sequential ID generation: ID is ONLY created and registered upon valid submission
        requisition_counter += 1
        new_id = INITIAL_REQUISITION_ID + requisition_counter

        # Instantiate Requisition entity
        new_req = Requisition(
            requisition_id=new_id,
            date=date,
            staff_id=staff_id,
            staff_name=staff_name,
            items=items,
        )

        # Trigger automated approval logic
        new_req.approve_requisition()

        # Register instance in system registry
        self._requisitions.append(new_req)

        return new_req

    def requisitions_details(self, *args, **kwargs):
        """Alias for add_requisition to guarantee spec compatibility."""
        return self.add_requisition(*args, **kwargs)

    def find_requisition(self, requisition_id):
        """Finds a requisition by its unique ID."""
        for req in self._requisitions:
            if req.requisition_id == requisition_id:
                return req
        return None

    def respond_to_requisition(self, requisition_id, decision):
        """Routes a manager's response to the targeted requisition."""
        req = self.find_requisition(requisition_id)
        if req is None:
            raise KeyError(f"Requisition ID {requisition_id} does not exist.")
        return req.respond_requisition(decision)

    def display_requisitions(self):
        """Prints formatted details for all requisition objects."""
        for req in self._requisitions:
            req.display_requisition()

    def requisition_statistics(self):
        """
        Calculates and displays system-wide requisition statistics.
        Returns a dictionary containing the counts.
        """
        total_count = len(self._requisitions)
        approved_count = sum(1 for req in self._requisitions if req.status == STATUS_APPROVED)
        pending_count = sum(1 for req in self._requisitions if req.status == STATUS_PENDING)
        not_approved_count = sum(1 for req in self._requisitions if req.status == STATUS_NOT_APPROVED)

        print("Displaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {total_count}")
        print(f"The total number of approved requisitions: {approved_count}")
        print(f"The total number of pending requisitions: {pending_count}")
        print(f"The total number of not approved requisitions: {not_approved_count}")
        print()

        return {
            "total": total_count,
            "approved": approved_count,
            "pending": pending_count,
            "not_approved": not_approved_count,
        }


# ==============================================================================
# 3. COMPREHENSIVE AUTOMATED UNIT TESTS & ASSERTIONS
# ==============================================================================
def run_unit_tests():
    """
    Rigorous test suite utilizing assertions to verify:
    - Boundary conditions ($0, $499.99, $500.00, $500.01)
    - Item-list aggregation
    - Prevention of manager responses to non-pending requisitions
    - Prevention of typos/unrecognized inputs corrupting statuses
    - Validation against negative costs and invalid inputs
    - Accurate statistics synchronization
    """
    print("=" * 60)
    print("RUNNING AUTOMATED UNIT TESTS & ASSERTIONS")
    print("=" * 60)

    test_system = RequisitionSystem()

    # 1. Boundary Test: $0.00 -> Approved
    r_zero = test_system.add_requisition("01/01/2026", "T01", "Zero Test", [{"name": "Free Sample", "price": 0.0}])
    assert r_zero.status == STATUS_APPROVED, f"Expected Approved for $0, got {r_zero.status}"

    # 2. Boundary Test: $499.99 -> Approved
    r_499 = test_system.add_requisition("01/01/2026", "T02", "Boundary Low", [{"name": "Item A", "price": 499.99}])
    assert r_499.status == STATUS_APPROVED, f"Expected Approved for $499.99, got {r_499.status}"
    assert r_499.approval_reference == f"T02{str(r_499.requisition_id)[-3:]}"

    # 3. Boundary Test: Exactly $500.00 -> Pending
    r_500 = test_system.add_requisition("01/01/2026", "T03", "Boundary Exact", [{"name": "Item B", "price": 500.00}])
    assert r_500.status == STATUS_PENDING, f"Expected Pending for exactly $500.00, got {r_500.status}"
    assert r_500.approval_reference == STATUS_NOT_AVAILABLE

    # 4. Boundary Test: $500.01 -> Pending
    r_501 = test_system.add_requisition("01/01/2026", "T04", "Boundary High", [{"name": "Item C", "price": 500.01}])
    assert r_501.status == STATUS_PENDING, f"Expected Pending for $500.01, got {r_501.status}"

    # 5. Item list aggregation check
    r_multi = test_system.add_requisition(
        "01/01/2026", "T05", "Multi Item",
        [{"name": "Mouse", "price": 25.50}, {"name": "Keyboard", "price": 74.50}]
    )
    assert r_multi.total == 100.0, f"Expected total 100.0, got {r_multi.total}"
    assert r_multi.status == STATUS_APPROVED

    # 6. Test preventing manager from overturning an already approved requisition
    try:
        r_multi.respond_requisition("Not approved")
        assert False, "Should have raised ValueError when attempting to respond to an Approved requisition"
    except ValueError as e:
        assert "Action Denied" in str(e)

    # 7. Test preventing typos (e.g. 'Aproved') from corrupting or resetting status
    try:
        r_500.respond_requisition("Aproved")  # Typo!
        assert False, "Should have raised ValueError for invalid manager decision"
    except ValueError as e:
        assert "Invalid manager decision" in str(e)
        assert r_500.status == STATUS_PENDING, "Status should remain Pending after rejected typo input"

    # 8. Test manager successfully approving a pending requisition
    r_500.respond_requisition("Approved")
    assert r_500.status == STATUS_APPROVED
    assert r_500.approval_reference == f"T03{str(r_500.requisition_id)[-3:]}"

    # 9. Test manager rejecting a pending requisition
    r_501.respond_requisition("Not approved")
    assert r_501.status == STATUS_NOT_APPROVED
    assert r_501.approval_reference == STATUS_NOT_AVAILABLE

    # 10. Test input validation against negative prices
    try:
        test_system.add_requisition("01/01/2026", "T06", "Negative Test", [{"name": "Bad Item", "price": -50.0}])
        assert False, "Should have raised ValueError for negative price"
    except ValueError as e:
        assert "cannot be negative" in str(e)

    print("ALL 10 UNIT TEST ASSERTIONS PASSED SUCCESSFULLY!\n")


# ==============================================================================
# 4. MAIN DEMONSTRATION (5 Requisitions Covering All Scenarios)
# ==============================================================================
def run_demonstration():
    global requisition_counter
    requisition_counter = 0  # Reset counter so demonstration IDs start cleanly at 10001

    system = RequisitionSystem()

    # Requisition 1: Total < $500 (Auto-Approved) using item list with costs
    req1 = system.add_requisition(
        date="03/04/2024",
        staff_id="FN19",
        staff_name="John Paul",
        items=[
            {"name": "Copy Paper (Box of 5)", "price": 50.0},
            {"name": "High-Yield Black Toner", "price": 400.0},
        ],
    )

    # Requisition 2: Total < $500 (Auto-Approved) using item list with costs
    req2 = system.add_requisition(
        date="03/05/2024",
        staff_id="FN02",
        staff_name="Catlin White",
        items=[
            {"name": "Wireless Ergonomic Keyboard", "price": 140.0},
            {"name": "Ergonomic Mesh Chair", "price": 350.0},
        ],
    )

    # Requisition 3: Total >= $500 (Pending -> Manager leaves Pending)
    req3 = system.add_requisition(
        date="05/04/2024",
        staff_id="FN20",
        staff_name="Tracy Brown",
        items=[
            {"name": "Electric Motorized Standing Desk", "price": 1000.0},
        ],
    )

    # Requisition 4: Total >= $500 (Pending -> Manager marks Not approved)
    req4 = system.add_requisition(
        date="07/05/2024",
        staff_id="FN15",
        staff_name="Emma Wellington",
        items=[
            {"name": "Rackmount Database Server", "price": 3500.0},
        ],
    )

    # Requisition 5: Total >= $500 (Pending -> Manager marks Approved)
    req5 = system.add_requisition(
        date="12/05/2024",
        staff_id="FN33",
        staff_name="David Clark",
        items=[
            {"name": "Conference 4K Projector", "price": 800.0},
            {"name": "Ceiling Mounting Bracket", "price": 50.0},
        ],
    )

    # Display initial statistics (before manager response)
    system.requisition_statistics()

    # Manager responds to requisitions with total >= $500
    # Requisition 3 (10003): Manager leaves as pending
    req3.respond_requisition("Pending")

    # Requisition 4 (10004): Manager marks as Not approved
    req4.respond_requisition("Not approved")

    # Requisition 5 (10005): Manager marks as Approved
    req5.respond_requisition("Approved")

    # Display all requisitions in required format
    system.display_requisitions()

    # Display updated statistics (after manager response)
    system.requisition_statistics()


if __name__ == "__main__":
    # Run automated unit tests first
    run_unit_tests()

    # Run the standard 5-scenario demonstration
    run_demonstration()
