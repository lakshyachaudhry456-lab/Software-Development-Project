# ==============================================================================
# Requisition System - Assessment 2
# ==============================================================================

# Global variable to generate unique requisition IDs starting from 10000
requisition_counter = 0


class RequisitionSystem:
    # Class-level list to track all created requisition objects
    all_requisitions = []

    def __init__(self, date="", staff_id="", staff_name=""):
        """
        Initializes shared data for a requisition.
        """
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.requisition_id = None
        self.items = []
        self.total = 0.0
        self.status = "Pending"
        self.approval_reference = "N/A"

        # Track this instance in the shared list
        RequisitionSystem.all_requisitions.append(self)

    def add_requisition(self, date=None, staff_id=None, staff_name=None, items=None):
        """
        Allows staff to submit basic information and items with costs.
        Calculates and returns the total amount.
        Can be used interactively or with pre-defined parameters.
        """
        global requisition_counter

        # Generate unique Requisition ID (e.g., 10001, 10002)
        requisition_counter += 1
        self.requisition_id = 10000 + requisition_counter

        # If data is passed as arguments (for automated testing)
        if date is not None and staff_id is not None and staff_name is not None and items is not None:
            self.date = date
            self.staff_id = staff_id
            self.staff_name = staff_name
            self.items = items
            self.total = sum(item["price"] for item in items)
        else:
            # Interactive prompt for manual user input
            print("\n--- Enter Requisition Information ---")
            self.date = input("Enter Date (e.g., DD/MM/YYYY): ")
            self.staff_id = input("Enter Staff ID: ")
            self.staff_name = input("Enter Staff Name: ")

            print(f"Requisition ID: {self.requisition_id}")
            self.items = []
            self.total = 0.0

            print("\nAdd Items to Requisition:")
            while True:
                item_name = input("Enter item name: ")
                item_price = float(input("Enter item price ($): "))

                self.items.append({"name": item_name, "price": item_price})
                self.total += item_price

                another = input("Do you want to add another item? (yes/no): ")
                if another.strip().lower() != "yes":
                    break

        # Automatically check initial approval based on total
        self.approve_requisition()
        return self.total

    def requisitions_details(self):
        """
        Alias for add_requisition.
        """
        return self.add_requisition()

    def approve_requisition(self):
        """
        Decides if a requisition is approved based on the total:
        - If total < 500: status is 'Approved' and approval reference is generated.
        - If total >= 500: status is 'Pending' and approval reference is 'N/A'.
        """
        req_id_str = str(self.requisition_id)
        last_three = req_id_str[-3:]

        if self.total < 500:
            self.status = "Approved"
            self.approval_reference = self.staff_id + last_three
        else:
            self.status = "Pending"
            self.approval_reference = "N/A"

        return self.status

    def respond_requisition(self, decision):
        """
        Allows a manager to respond to a pending requisition:
        - 'Approved': updates status to 'Approved' and creates approval reference.
        - 'Not approved': updates status to 'Not approved'.
        - 'Pending': remains 'Pending'.
        """
        clean_decision = decision.strip().lower()
        last_three = str(self.requisition_id)[-3:]

        if clean_decision == "approved":
            self.status = "Approved"
            self.approval_reference = self.staff_id + last_three
            print(f"Manager Response: Requisition {self.requisition_id} has been Approved.")
        elif clean_decision in ["not approved", "not_approved", "rejected"]:
            self.status = "Not approved"
            self.approval_reference = "N/A"
            print(f"Manager Response: Requisition {self.requisition_id} has been Not approved.")
        else:
            self.status = "Pending"
            self.approval_reference = "N/A"
            print(f"Manager Response: Requisition {self.requisition_id} remains Pending.")

        return self.status

    def display_requisition(self):
        """
        Displays details of this single requisition.
        """
        print(f"Date:               {self.date}")
        print(f"Requisition ID:     {self.requisition_id}")
        print(f"Staff ID:           {self.staff_id}")
        print(f"Staff Name:         {self.staff_name}")
        print(f"Total:              ${self.total:.2f}")
        print(f"Status:             {self.status}")
        print(f"Approval Reference: {self.approval_reference}")
        print("Items:")
        for item in self.items:
            print(f"  - {item['name']}: ${item['price']:.2f}")
        print("-" * 40)

    @classmethod
    def display_requisitions(cls):
        """
        Prints information for all requisition objects.
        """
        print("\n" + "=" * 45)
        print("          ALL REQUISITIONS LIST")
        print("=" * 45)
        if not cls.all_requisitions:
            print("No requisitions found.")
            return

        for req in cls.all_requisitions:
            req.display_requisition()
        print("=" * 45 + "\n")

    @classmethod
    def requisition_statistics(cls):
        """
        Calculates and returns statistical summary of all requisitions.
        """
        total_count = len(cls.all_requisitions)
        approved_count = sum(1 for req in cls.all_requisitions if req.status.lower() == "approved")
        pending_count = sum(1 for req in cls.all_requisitions if req.status.lower() == "pending")
        not_approved_count = sum(1 for req in cls.all_requisitions if req.status.lower() == "not approved")

        stats = {
            "total_requisitions": total_count,
            "approved": approved_count,
            "pending": pending_count,
            "not_approved": not_approved_count,
        }

        print("\n" + "=" * 40)
        print("         REQUISITION STATISTICS")
        print("=" * 40)
        print(f"Total Requisitions: {total_count}")
        print(f"Approved:           {approved_count}")
        print(f"Pending:            {pending_count}")
        print(f"Not Approved:       {not_approved_count}")
        print("=" * 40 + "\n")

        return stats


# ==============================================================================
# Testing & Verification
# ==============================================================================
if __name__ == "__main__":
    print("==================================================")
    print("    STEP 1: SUBMITTING 5 TEST REQUISITIONS")
    print("==================================================")

    # Requisition 1: Total < $500 (Scenario: Auto-Approved)
    req1 = RequisitionSystem()
    req1.add_requisition(
        date="10/11/2026",
        staff_id="ST101",
        staff_name="Alice Brown",
        items=[{"name": "Printer Paper", "price": 40.0}, {"name": "Toner Cartridge", "price": 120.0}]
    )

    # Requisition 2: Total < $500 (Scenario: Auto-Approved)
    req2 = RequisitionSystem()
    req2.add_requisition(
        date="11/11/2026",
        staff_id="ST102",
        staff_name="Bob Smith",
        items=[{"name": "Desk Lamp", "price": 60.0}, {"name": "Ergonomic Keyboard", "price": 140.0}]
    )

    # Requisition 3: Total >= $500 (Scenario: Initially Pending -> Later Approved by Manager)
    req3 = RequisitionSystem()
    req3.add_requisition(
        date="12/11/2026",
        staff_id="ST103",
        staff_name="Charlie Davis",
        items=[{"name": "Office Desk", "price": 450.0}, {"name": "Office Chair", "price": 250.0}]
    )

    # Requisition 4: Total >= $500 (Scenario: Initially Pending -> Later Not Approved by Manager)
    req4 = RequisitionSystem()
    req4.add_requisition(
        date="13/11/2026",
        staff_id="ST104",
        staff_name="Diana Evans",
        items=[{"name": "MacBook Pro", "price": 2200.0}]
    )

    # Requisition 5: Total >= $500 (Scenario: Initially Pending -> Left as Pending)
    req5 = RequisitionSystem()
    req5.add_requisition(
        date="14/11/2026",
        staff_id="ST105",
        staff_name="Ethan Miller",
        items=[{"name": "Projector", "price": 600.0}, {"name": "HDMI Cable", "price": 30.0}]
    )

    print("\nInitial list of all requisitions submitted:")
    RequisitionSystem.display_requisitions()

    print("\nInitial Statistics before Manager Response:")
    RequisitionSystem.requisition_statistics()

    print("==================================================")
    print("    STEP 2: MANAGER RESPONDING TO PENDING REQUISITIONS (>= $500)")
    print("==================================================")
    # Manager responds to Requisition 3: Approves it
    print("\nManager reviewing Requisition 3 ($700.00):")
    req3.respond_requisition("Approved")

    # Manager responds to Requisition 4: Rejects / Not Approved
    print("\nManager reviewing Requisition 4 ($2200.00):")
    req4.respond_requisition("Not approved")

    # Manager reviews Requisition 5: Leaves it as Pending
    print("\nManager reviewing Requisition 5 ($630.00):")
    req5.respond_requisition("Pending")

    print("\n==================================================")
    print("    STEP 3: FINAL REQUISITIONS AND STATISTICS")
    print("==================================================")
    RequisitionSystem.display_requisitions()
    RequisitionSystem.requisition_statistics()
