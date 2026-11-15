# ==============================================================================
# Requisition System - Assessment 2: Task 1
# ==============================================================================

# Global variable to generate unique requisition IDs starting from 10000
requisition_counter = 0


class RequisitionSystem:
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

    def add_requisition(self):
        """
        Allows staff to submit basic information and items with costs.
        Calculates and returns the total amount.
        """
        global requisition_counter

        print("\n--- Enter Requisition Information ---")
        self.date = input("Enter Date (e.g., DD/MM/YYYY): ")
        self.staff_id = input("Enter Staff ID: ")
        self.staff_name = input("Enter Staff Name: ")

        # Generate unique Requisition ID (e.g., 10001, 10002)
        requisition_counter += 1
        self.requisition_id = 10000 + requisition_counter
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

        print(f"\nTotal Amount: ${self.total:.2f}")
        return self.total

    def requisitions_details(self):
        """
        Alias for add_requisition if referred by that name.
        """
        return self.add_requisition()

    def approve_requisition(self):
        """
        Decides if a requisition is approved based on the total:
        - If total <= 500: status is 'Approved' and approval reference is generated.
        - If total > 500: status is 'Pending' and approval reference is 'N/A'.
        """
        req_id_str = str(self.requisition_id)
        last_three = req_id_str[-3:]

        if self.total <= 500:
            self.status = "Approved"
            self.approval_reference = self.staff_id + last_three
        else:
            self.status = "Pending"
            self.approval_reference = "N/A"

        print(f"\nStatus: {self.status}")
        print(f"Approval Reference: {self.approval_reference}")
        return self.status

    def display_requisition(self):
        """
        Displays all details of the requisition.
        """
        print("\n" + "=" * 35)
        print("       REQUISITION DETAILS")
        print("=" * 35)
        print(f"Date:               {self.date}")
        print(f"Requisition ID:     {self.requisition_id}")
        print(f"Staff ID:           {self.staff_id}")
        print(f"Staff Name:         {self.staff_name}")
        print(f"Total:              ${self.total:.2f}")
        print(f"Status:             {self.status}")
        print(f"Approval Reference: {self.approval_reference}")
        print("-" * 35)
        print("Items:")
        for item in self.items:
            print(f"  - {item['name']}: ${item['price']:.2f}")
        print("=" * 35 + "\n")


# ==============================================================================
# Main Execution / Demonstration
# ==============================================================================
if __name__ == "__main__":
    print("Welcome to the Requisition System Prototype!")

    # Creating an instance of RequisitionSystem
    req = RequisitionSystem()
    req.add_requisition()
    req.approve_requisition()
    req.display_requisition()
