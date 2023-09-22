# This code was done a collaboration done by Ralph Matthew V. Sabuco and Trixie Mae E. Herras.

import tkinter as tk
from tkinter import simpledialog, messagebox #import simpledialog and messagebox for widgets and text display
import csv #import csv in order to save and load the data

font1 = ("Helvetica", 9, "bold") #create and modify the text's font and design
font2 = ("Helvetica", 9)

#display a message using messagebox that
messagebox.showinfo("Address Book", "Welcome to the Address Book!\n\nClick 'OK' to proceed to the Adress Book.\n\nCreated by Trixie Mae E. Herras and Ralph Matthew V. Sabuco")

class AddressBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Address Book")  #title of the window
        self.root.configure(background="Light Grey") #change the background of the window to light grey
        self.root.resizable(False, False) #make the window not resizeable

        self.fname_label = tk.Label(root, text="First Name:", font=font1, bg="Light Grey")  #first name label
        self.fname_label.grid(row=0, column=0, sticky=tk.W) #adjust the row, column and position (aligns the value to W= West)
        self.fname_entry = tk.Entry(root, width=41) #entry (yung pinaglalagyan ng contact input/entry widget)
        self.fname_entry.grid(row=0, column=1, sticky=tk.W)

        self.lname_label = tk.Label(root, text="Last Name:", font=font1, bg="Light Grey")  #last name label
        self.lname_label.grid(row=1, column=0, sticky=tk.W)
        self.lname_entry = tk.Entry(root, width=41) #modified the width to 41 characters. this will display 41 charcs in the entry
        self.lname_entry.grid(row=1, column=1, sticky=tk.W)

        self.ad_label = tk.Label(root, text="Address:", font=font1, bg="Light Grey")  #address label
        self.ad_label.grid(row=2, column=0, sticky=tk.W)
        self.ad_entry = tk.Entry(root, width=41)
        self.ad_entry.grid(row=2, column=1, sticky=tk.W)

        self.cnumber_label = tk.Label(root, text="Contact Number (+63) :", font=font1, bg="Light Grey")  #contact number label
        self.cnumber_label.grid(row=3, column=0, sticky=tk.W)
        self.cnumber_entry = tk.Entry(root, width=41)
        self.cnumber_entry.grid(row=3, column=1, sticky=tk.W)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact, font=font1 ,fg="Dark green", activebackground="Light Green")  #add contact button
        self.add_button.grid(row=4, column=0, columnspan=1, sticky=tk.EW) #sticks the button to both east and west. occupy the width in both sides para pantay

        self.edit_button = tk.Button(root, text="Edit Contact", command=self.edit_contact,font=font1,fg="Dark green", activebackground="Light Green")  #edit contact button
        self.edit_button.grid(row=4, column=1, columnspan=1, sticky=tk.EW)

        self.search_button = tk.Button(root, text="Search Address Book", command=self.search_address_book,font=font1, fg="Dark blue", activebackground="Light blue")  #search button
        self.search_button.grid(row=5, column=0, columnspan=1, sticky=tk.EW)

        self.view_button = tk.Button(root, text="View Contacts", command=self.view_contacts,font=font1, fg="Dark blue", activebackground="Light blue")  #view contacts button
        self.view_button.grid(row=5, column=1, columnspan=1, sticky=tk.EW)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact, font=font1, fg="Maroon", activebackground="Red")  #delete contact button
        self.delete_button.grid(row=6, column=0, columnspan=1, sticky=tk.EW)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit, font=font1, fg="Maroon", activebackground="Red")  #exit button
        self.exit_button.grid(row=6, column=1, columnspan=1, sticky=tk.EW)

        self.contacts_entry = tk.Text(root, height=20, width=54,font=font2) #contacts entry widget inside the address book window
        self.contacts_entry.grid(row=8, columnspan=2, rowspan=10, padx=10, pady=10)

        self.contacts = []  #list to store contacts
        self.load_contacts()  #load contacts from file

        self.display_contacts() #display loaded contacts in the contacts_entry

    def show_message(self, title, message): #allow to show the messages/notif from the messagebox
        messagebox.showinfo(title, message)

    def add_contact(self): #add contact
        first_name = self.fname_entry.get() #declare the variables
        last_name = self.lname_entry.get()
        address = self.ad_entry.get()
        contact_number = self.cnumber_entry.get()

        # set the conditions for fname,lname and cnumber. this validates the input before receiving/accepting it
        if first_name and last_name and address and contact_number: #fname, lname and cn should have values to proceed
            if contact_number.isdigit() and len(contact_number) == 10 and contact_number[0] == '9': #the cnumber should be a 10-digit number that start with 9 and should only be digits
                if not any(char.isdigit() for char in first_name) and not any(char.isdigit() for char in last_name): #first and last name should be characters and will not be accepted if numeric
                    self.contacts.append([first_name, last_name, address, contact_number]) #accept if all conditions are met
                    contact_count = len(self.contacts) #count the entry
                    contact_info = f"Entry #{contact_count}:\nFirst Name: {first_name}\nLast Name: {last_name}\n\n" #creates formatted string that contains the var: entry numm fname and lname
                    self.contacts_entry.insert(tk.END, contact_info) #Inserts it to the end of the text in contact_info
                    self.clear_entries() #clear the previously accepted entry
                    self.save_contacts()  # Save contacts after adding a new contact
                else:
                    messagebox.showerror("Error", "First name and last name cannot contain numeric digits.")
            else:
                messagebox.showerror("Error",
                                     "Contact number must be a 10-digit number starting with '9' and contain only digits.")
        else:
            messagebox.showerror("Error", "Please fill in all the fields.")

    def edit_contact(self): #Edit contact
        entry_number = self.prompt_entry_number()
        if entry_number is None:
            return

        if entry_number < 1 or entry_number > len(self.contacts): #set conditions for the entry number
            messagebox.showerror("Error", "Invalid entry number.")
            return

        contact = self.contacts[entry_number - 1] #zero-based for contacts
        new_first_name = simpledialog.askstring("Edit Contact", "Enter new First Name:", initialvalue=contact[0]) #show initial value that can be edited to be new
        new_last_name = simpledialog.askstring("Edit Contact", "Enter new Last Name:", initialvalue=contact[1])
        new_address = simpledialog.askstring("Edit Contact", "Enter new Address:", initialvalue=contact[2])
        new_contact_number = simpledialog.askstring("Edit Contact", "Enter new Contact Number:",
                                                    initialvalue=contact[3])

        if new_first_name and new_last_name and new_address and new_contact_number: #set conditions that follows add contacts
            if new_contact_number.isnumeric():
                if not any(char.isdigit() for char in new_first_name) and not any(
                        char.isdigit() for char in new_last_name):
                    self.contacts[entry_number - 1] = [new_first_name, new_last_name, new_address, new_contact_number]
                    self.save_contacts()  # Save contacts after editing a contact
                    self.refresh_contact_list()  # Refresh the contact list in the GUI
                    messagebox.showinfo("Success", "Contact edited successfully.")
                else:
                    messagebox.showerror("Error", "First name and last name cannot contain numeric digits.")
            else:
                messagebox.showerror("Error", "Contact number must be numeric.")
        else:
            messagebox.showerror("Error", "Please fill in all the fields.")

    def prompt_entry_number(self): #Entry number. This allows
        try:
            entry_number = int(simpledialog.askstring("Entry Number", "Enter the entry number:"))
            return entry_number
        except ValueError:
            messagebox.showerror("Error", "Invalid entry number.")
            return None

    def delete_contact(self): #delete contact. allow the user to have 2 choices, delete a specific contact or all contacts
        choice = simpledialog.askstring("Delete",
                                        "Enter 'contact' to delete a contact or 'all' to delete all contacts.")
        if choice == 'contact': #deletes contact
            confirmation = messagebox.askyesno("Delete a contact", "Are you sure you want to delete a contact?")
            if confirmation: #confirms decisions
                entry_number = self.prompt_entry_number()
                if entry_number is None:
                    return

                if entry_number < 1 or entry_number > len(self.contacts):
                    messagebox.showerror("Error", "Invalid entry number.")
                    return

                contact = self.contacts[entry_number - 1]
                self.contacts.remove(contact)
                self.contacts_entry.delete('1.0', tk.END)  #clear the deleted contact to contacts_entry
                for i, contact in enumerate(self.contacts, start=1):
                    contact_info = f"Entry #{i}:\nFirst Name: {contact[0]}\nLast Name: {contact[1]}\n\n"
                    self.contacts_entry.insert(tk.END, contact_info)
                self.save_contacts()  #save contacts after deleting a contact
                messagebox.showinfo("Success", "Contact deleted successfully.")
        elif choice == 'all': #deletes all contact
            confirmation = messagebox.askyesno("Delete All Entries", "Are you sure you want to delete all entries?")
            if confirmation: #confirmation
                self.contacts = []
                self.contacts_entry.delete('1.0', tk.END)
                self.save_contacts()
                messagebox.showinfo("Success", "All entries have been deleted.")

    def refresh_contact_list(self): #refresh contact_list of the contacts_entry
        self.contacts_entry.delete('1.0', tk.END)  #clear the contacts_entry. 1 is the start and tk.END is the end. it is 1.0 because .0 refers to first character in the first line
        for i, contact in enumerate(self.contacts, start=1):
            contact_info = f"Entry #{i}:\nFirst Name: {contact[0]}\nLast Name: {contact[1]}\n\n"
            self.contacts_entry.insert(tk.END, contact_info)

    def view_contacts(self):  # view contacts
        if not self.contacts:  # show error if no contact is found
            messagebox.showinfo("Address Book", "No contacts found.")
            return

        contacts_window = tk.Toplevel(self.root)  # make a separate contact window once view contact button is clicked
        contacts_window.title("Contacts")
        contacts_window.geometry("450x510")
        contacts_window.configure(background="Light Grey")
        contacts_window.resizable(False, False)  # make the window not resizable

        total_entries = len(self.contacts)  # show the current no of entries
        exceed_msg = f"Current number of entries: {total_entries}"

        total_label = tk.Label(contacts_window, text=exceed_msg, font=font1, background="Light Grey")
        total_label.pack(pady=10)

        contacts_entry = tk.Text(contacts_window, height=40, width=60, font=font2)
        contacts_entry.pack()

        contacts_info = "Address Book\n\n"  # display contact info
        for i, contact in enumerate(self.contacts, start=1):
            contacts_info += f"Entry #{i}:\n"  # += is used to build larger strings and modifies existing strings in place
            contacts_info += f"First Name: {contact[0]}\n"
            contacts_info += f"Last Name: {contact[1]}\n"
            contacts_info += f"Address: {contact[2]}\n"
            contacts_info += f"Contact Number: 0{contact[3]}\n\n"

        contacts_entry.insert(tk.END, contacts_info)

    def search_address_book(self):  # search address book
        if not self.contacts:  # display error message if no contact found
            messagebox.showinfo("Address Book", "No contacts found.")
            return

        search_option = self.prompt_search_option()
        if search_option is None:
            return

        search_value = self.prompt_search_value()
        if search_value is None:
            return

        matching_contacts = []
        if search_option == "a":
            matching_contacts = [contact for contact in self.contacts if search_value.lower() in contact[0].lower()]
        elif search_option == "b":
            matching_contacts = [contact for contact in self.contacts if search_value.lower() in contact[1].lower()]
        elif search_option == "c":
            matching_contacts = [contact for contact in self.contacts if search_value.lower() in contact[2].lower()]
        elif search_option == "d":
            matching_contacts = [contact for contact in self.contacts if search_value.lower() in contact[3].lower()]

        if matching_contacts:
            contacts_info = "Search Results\n\n"
            for i, contact in enumerate(matching_contacts, start=1):
                contacts_info += f"{i}. First Name: {contact[0]}\n"
                contacts_info += f"   Last Name: {contact[1]}\n"
                contacts_info += f"   Address: {contact[2]}\n"
                contacts_info += f"   Contact Number: {contact[3]}\n\n"
            messagebox.showinfo("Address Book", contacts_info)
        else:
            messagebox.showinfo("Address Book", "No matching contacts found.")

    def prompt_search_option(self): #search options
        search_option = simpledialog.askstring("Search Option",
                                               "Enter the search option:\n(a) by first name\n(b) by last name\n(c) by address\n(d) by contact number")
        if search_option.lower() in ["a", "b", "c", "d"]:
            return search_option.lower()
        else:
            messagebox.showerror("Error", "Invalid search option.")
            return None

    def prompt_search_value(self): #search value
        search_value = simpledialog.askstring("Search Value", "Enter the search value:")
        if search_value:
            return search_value.lower()
        else:
            messagebox.showerror("Error", "Invalid search value.") #if no match, show error
            return None

    def display_contacts(self): #display contact in the contacts_widget widget below
        self.contacts_entry.delete('1.0', tk.END)  # Clear the contacts_entry
        for i, contact in enumerate(self.contacts, start=1):
            contact_info = f"Entry #{i}:\nFirst Name: {contact[0]}\nLast Name: {contact[1]}\n\n"
            self.contacts_entry.insert(tk.END, contact_info)

    def get_selected_contacts(self): #get selected contact
        selected_contacts = []
        selected_text = self.contacts_entry.get(tk.SEL_FIRST, tk.SEL_LAST) #first and last
        if selected_text:
            selected_lines = selected_text.split("\n") #split into newline character
            for line in selected_lines:
                contact_index = int(line.split(".")[0]) - 1
                if 0 <= contact_index < len(self.contacts):
                    selected_contacts.append(self.contacts[contact_index])
        return selected_contacts

    def clear_entries(self): #this clears the entries from fname, lname, address and cnumber entry
        self.fname_entry.delete(0, tk.END)
        self.lname_entry.delete(0, tk.END)
        self.ad_entry.delete(0, tk.END)
        self.cnumber_entry.delete(0, tk.END)

    def save_contacts(self): #save contacts to address book csv
        try:
            with open('address_book.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.contacts)
            messagebox.showinfo("Success", "Contacts saved successfully.")
        except IOError:
            messagebox.showerror("Error", "Failed to save contacts.")

    def load_contacts(self): #load contacts from address book csv upon running
        try:
            with open("address_book.csv", 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                self.contacts = [row for row in csvreader]
            self.show_message("Success", "Contacts loaded successfully.")
        except IOError:
            messagebox.showerror("Error", "Failed to load contacts.")

if __name__ == "__main__":
    root = tk.Tk()
    address_book = AddressBookGUI(root)
    root.mainloop()
