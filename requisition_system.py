# ==============================================================================
# Requisition System - Assessment 2: Task 1
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
        self.approval_reference = "Not available"

        # Track this instance in the shared list
        RequisitionSystem.all_requisitions.append(self)

    def add_requisition(self, date=None, staff_id=None, staff_name=None, items=None, total=None):
        """
        Allows staff to submit basic information and items with costs.
        Calculates and returns the total amount.
        Can be used interactively or with parameters for testing.
        """
        global requisition_counter

        # Generate unique Requisition ID (e.g., 10001, 10002)
        requisition_counter += 1
        self.requisition_id = 10000 + requisition_counter

        # If data is passed as arguments (for testing/direct input)
        if date is not None and staff_id is not None and staff_name is not None:
            self.date = date
            self.staff_id = staff_id
            self.staff_name = staff_name
            if items is not None:
                self.items = items
                self.total = sum(item["price"] for item in items)
            elif total is not None:
                self.items = [{"name": "Requisition Items", "price": total}]
                self.total = total
        else:
            # Interactive prompt for user input
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

        # Automatically decide approval status based on total
        self.approve_requisition()
        return self.total

    def requisitions_details(self):
        """
        Alias for add_requisition.
        """
        return self.add_requisition()

    def approve_requisition(self):
        """
        Decides if a requisition is approved or not based on total:
        - If total < 500: status is 'Approved' with Approval Reference Number.
        - If total >= 500: status is 'Pending' and Approval Reference is 'Not available'.
        """
        req_id_str = str(self.requisition_id)
        last_three = req_id_str[-3:]

        if self.total < 500:
            self.status = "Approved"
            self.approval_reference = self.staff_id + last_three
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

        return self.status

    def respond_requisition(self, decision):
        """
        Allows a manager to respond to a pending requisition:
        - 'Approved': updates status to 'Approved' and assigns Approval Reference Number.
        - 'Not approved': updates status to 'Not approved' and Reference is 'Not available'.
        - 'Pending': status remains 'Pending' and Reference is 'Not available'.
        """
        clean_decision = decision.strip().lower()
        last_three = str(self.requisition_id)[-3:]

        if clean_decision == "approved":
            self.status = "Approved"
            self.approval_reference = self.staff_id + last_three
        elif clean_decision in ["not approved", "not_approved", "rejected"]:
            self.status = "Not approved"
            self.approval_reference = "Not available"
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

        return self.status

    def display_requisition(self):
        """
        Displays requisition information in the required output format.
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
        Prints information for all the requisition objects.
        """
        for req in cls.all_requisitions:
            req.display_requisition()

    @classmethod
    def requisition_statistics(cls):
        """
        Tracks and displays statistical information:
        - Total number of requisitions submitted
        - Total number of approved requisitions
        - Total number of pending requisitions
        - Total number of not approved requisitions
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

    # Requisition 3: Total >= $500 (Pending)
    req3 = RequisitionSystem()
    req3.add_requisition(date="05/04/2024", staff_id="FN20", staff_name="Tracy Brown", total=1000)

    # Requisition 4: Total >= $500 (Pending)
    req4 = RequisitionSystem()
    req4.add_requisition(date="07/05/2024", staff_id="FN15", staff_name="Emma Wellington", total=3500)

    # Requisition 5: Total >= $500 (Pending)
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
