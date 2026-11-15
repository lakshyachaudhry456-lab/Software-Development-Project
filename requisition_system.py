# ==============================================================================
# BACT7501 - Assessment 2: Software Development Project
# Task 1: Purchase Requisition System (OOP Prototype)
# ==============================================================================

# Global counter for generating unique requisition IDs starting from 10000
requisition_counter = 0


class RequisitionSystem:
    """
    Encapsulates all functionality and data for a purchase requisition,
    including data entry, automatic approval checks, manager responses,
    display, and statistical tracking.
    """

    # Class-level list to track all created requisition objects
    all_requisitions = []

    def __init__(self, date="", staff_id="", staff_name=""):
        """
        Initializes shared data attributes for the requisition instance.
        """
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.requisition_id = None
        self.items = []
        self.total = 0.0
        self.status = "Pending"
        self.approval_reference = "Not available"

        # Register instance in the shared collection
        RequisitionSystem.all_requisitions.append(self)

    def add_requisition(self, date=None, staff_id=None, staff_name=None, items=None, total=None):
        """
        Submits basic requisition information, accepts items with their cost,
        computes the total, automatically triggers approval evaluation,
        and returns the total amount.
        """
        global requisition_counter

        # Increment global counter and assign unique Requisition ID
        requisition_counter += 1
        self.requisition_id = 10000 + requisition_counter

        # Programmatic input (used for testing and automated runs)
        if date is not None and staff_id is not None and staff_name is not None:
            self.date = str(date).strip()
            self.staff_id = str(staff_id).strip()
            self.staff_name = str(staff_name).strip()

            if items is not None and isinstance(items, list):
                self.items = items
                self.total = sum(float(item.get("price", 0.0)) for item in items)
            elif total is not None:
                self.total = float(total)
                self.items = [{"name": "Requisition Items", "price": self.total}]
            else:
                self.items = []
                self.total = 0.0
        else:
            # Interactive input for staff
            print("\n--- Enter Requisition Information ---")
            self.date = input("Enter Date (e.g., DD/MM/YYYY): ").strip()
            self.staff_id = input("Enter Staff ID: ").strip()
            self.staff_name = input("Enter Staff Name: ").strip()

            print(f"Requisition ID: {self.requisition_id}")
            self.items = []
            self.total = 0.0

            print("\nAdd Items to Requisition:")
            while True:
                item_name = input("Enter item name: ").strip()
                while not item_name:
                    print("Item name cannot be empty.")
                    item_name = input("Enter item name: ").strip()

                # Edge case handling: Validate numeric and non-negative price
                while True:
                    try:
                        item_price = float(input("Enter item price ($): "))
                        if item_price < 0:
                            print("Price cannot be negative. Please enter a valid amount.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid numerical price.")

                self.items.append({"name": item_name, "price": item_price})
                self.total += item_price

                another = input("Do you want to add another item? (yes/no): ").strip().lower()
                if another != "yes":
                    break

        # Automatically determine initial approval status based on total
        self.approve_requisition()
        return self.total

    def requisitions_details(self, *args, **kwargs):
        """
        Alias for add_requisition to match specification naming.
        """
        return self.add_requisition(*args, **kwargs)

    def approve_requisition(self):
        """
        Decides if a requisition is approved based on the total:
        - If total < 500: status is 'Approved' and approval reference number is generated.
        - If total >= 500: status is 'Pending' and approval reference is 'Not available'.
        """
        req_id_str = str(self.requisition_id)
        last_three = req_id_str[-3:]

        if self.total < 500:
            self.status = "Approved"
            self.approval_reference = f"{self.staff_id}{last_three}"
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

        return self.status

    def respond_requisition(self, decision):
        """
        Allows a manager to respond to a pending requisition:
        - 'Approved': updates status to 'Approved' and generates approval reference number.
        - 'Not approved': updates status to 'Not approved' and reference remains 'Not available'.
        - 'Pending': leaves status as 'Pending' and reference as 'Not available'.
        """
        clean_decision = str(decision).strip().lower()
        last_three = str(self.requisition_id)[-3:]

        if clean_decision == "approved":
            self.status = "Approved"
            self.approval_reference = f"{self.staff_id}{last_three}"
        elif clean_decision in ["not approved", "not_approved", "rejected"]:
            self.status = "Not approved"
            self.approval_reference = "Not available"
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

        return self.status

    def display_requisition(self):
        """
        Displays a single requisition matching the exact specification output format.
        """
        formatted_total = f"${int(self.total)}" if self.total == int(self.total) else f"${self.total:.2f}"
        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: {formatted_total}")
        print(f"Status: {self.status}")
        print(f"Approval Reference Number: {self.approval_reference}")
        print()

    @classmethod
    def display_requisitions(cls):
        """
        Prints formatted information for all requisition objects.
        """
        for req in cls.all_requisitions:
            req.display_requisition()

    @classmethod
    def requisition_statistics(cls):
        """
        Aggregates and displays statistical information:
        - The total number of requisitions submitted
        - The total number of approved requisitions
        - The total number of pending requisitions
        - The total number of not approved requisitions
        Returns a dictionary containing the counts.
        """
        total_count = len(cls.all_requisitions)
        approved_count = sum(1 for req in cls.all_requisitions if req.status.lower() == "approved")
        pending_count = sum(1 for req in cls.all_requisitions if req.status.lower() == "pending")
        not_approved_count = sum(1 for req in cls.all_requisitions if req.status.lower() == "not approved")

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
# Program Testing
# ==============================================================================
if __name__ == "__main__":
    # --------------------------------------------------------------------------
    # 1. Create at least 5 requisition instances covering different scenarios
    # --------------------------------------------------------------------------

    # Requisition 1: Total < $500 (Auto-Approved)
    req1 = RequisitionSystem()
    req1.add_requisition(date="03/04/2024", staff_id="FN19", staff_name="John Paul", total=450)

    # Requisition 2: Total < $500 (Auto-Approved)
    req2 = RequisitionSystem()
    req2.add_requisition(date="03/05/2024", staff_id="FN02", staff_name="Catlin White", total=490)

    # Requisition 3: Total >= $500 (Initially Pending)
    req3 = RequisitionSystem()
    req3.add_requisition(date="05/04/2024", staff_id="FN20", staff_name="Tracy Brown", total=1000)

    # Requisition 4: Total >= $500 (Initially Pending)
    req4 = RequisitionSystem()
    req4.add_requisition(date="07/05/2024", staff_id="FN15", staff_name="Emma Wellington", total=3500)

    # Requisition 5: Total >= $500 (Initially Pending)
    req5 = RequisitionSystem()
    req5.add_requisition(date="12/05/2024", staff_id="FN33", staff_name="David Clark", total=850)

    # --------------------------------------------------------------------------
    # 2. Display initial requisition statistics
    # --------------------------------------------------------------------------
    RequisitionSystem.requisition_statistics()

    # --------------------------------------------------------------------------
    # 3. Manager responds to requisitions greater than $499
    # --------------------------------------------------------------------------
    # Requisition 3: Manager leaves as pending
    req3.respond_requisition("Pending")

    # Requisition 4: Manager marks as Not approved
    req4.respond_requisition("Not approved")

    # Requisition 5: Manager marks as Approved
    req5.respond_requisition("Approved")

    # --------------------------------------------------------------------------
    # 4. Display all requisitions and updated statistics
    # --------------------------------------------------------------------------
    RequisitionSystem.display_requisitions()
    RequisitionSystem.requisition_statistics()
