import tkinter as tk
import requests
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import PhotoImage
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
database_api = os.getenv('DATABASE_API')

def submit_data():
    # Collect patient information
    full_name = full_name_entry.get()
    patient_no = patient_entry.get()
    invoice_no = invoice_entry.get()
    email = email_entry.get()
    mobile_number = mobile_entry.get()
    
    # Collect billing information
    amount = amount_label_spinbox.get()
    net_paid = net_paid_spinbox.get()
    amount_outstanding = amount_outstanding_entry.get()
    date_issued = date_entry.get()
    due_date = date_due_entry.get()
    days_overdue = days_overdue_entry.get()
    invoice_status = invoice_status_dropbox.get()
    
    # Collect admin information
    assigned_to = assigned_entry.get()
    debt_collector = debt_collector_dropbox.get()
    invoice_link = Invoice_Link_entry.get()
    credit_note_reason = credit_note_reason_entry.get("1.0", 'end-1c')
    

    # Prepare the data payload
    data = {
        "data": [
            {
                "Bill to": full_name,
                "Patient Number": patient_no,
                "Invoice Number": invoice_no,
                "Email": email,
                "Mobile#": mobile_number,
                "Amount": amount,
                "Net Amount Paid": net_paid,
                "Amount Outstanding": amount_outstanding,
                "Date Issued": date_issued,
                "Due Date": due_date,
                "Days Overdue": days_overdue,
                "Invoice Status": invoice_status,
                "Assigned To": assigned_to,
                "Debt Collector": debt_collector,
                "Invoice Link": invoice_link,
                "Credit Note Reason": credit_note_reason,
            }
        ]
    }

    # Send the data to the SheetDB API
    response = requests.post(database_api, json=data)
    print(response.status_code)
    print(response.json())

def update_outstanding(*args):
    try:
        # Retrieve the values from the amount and net paid fields
        amount = float(amount_label_spinbox.get())
        net_paid = float(net_paid_spinbox.get())
        
        # Calculate outstanding amount
        outstanding = amount - net_paid
        
        # Update the outstanding amount entry field
        amount_outstanding_entry.configure(state='normal')
        amount_outstanding_entry.delete(0, 'end')
        amount_outstanding_entry.insert(0, f"{outstanding:.2f}")
        amount_outstanding_entry.configure(state='readonly')
    except ValueError:
        amount_outstanding_entry.configure(state='normal')
        amount_outstanding_entry.delete(0, 'end')
        amount_outstanding_entry.insert(0, "Invalid input")
        amount_outstanding_entry.configure(state='readonly')

# Function to calculate days overdue
def calculate_days_overdue(*args):
    try:
        due_date = datetime.strptime(date_due_entry.get(), '%d/%m/%Y')
        days_overdue = (datetime.now().date() - due_date.date()).days

        # Update the days overdue entry field
        days_overdue_entry.configure(state='normal')
        days_overdue_entry.delete(0, 'end')
        days_overdue_entry.insert(0, str(days_overdue))
        days_overdue_entry.configure(state='readonly')
    except ValueError:
        days_overdue_entry.configure(state='normal')
        days_overdue_entry.delete(0, 'end')
        days_overdue_entry.insert(0, "Invalid input")
        days_overdue_entry.configure(state='readonly')

# Function to update the color label based on status selection
def update_invoice_status_color(event):
    status = invoice_status_dropbox.get()
    if status == "Paid":
        status_color_label.configure(bg='green')
    elif status == "Unpaid":
        status_color_label.configure(bg='red')
    elif status == "Partially Paid":
        status_color_label.configure(bg='yellow')
    else:
        status_color_label.configure(bg='white')

# Setting up windows canvas
window = tk.Tk()
window.title("Billing Automation Software - by SamsCo Tech")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Adding a Scrollable Canvas
canvas = tk.Canvas(window, highlightthickness=0)
canvas.configure(width=window.winfo_screenwidth())
scrollbar = tk.Scrollbar(window, orient='vertical', command=canvas.yview)
scrollable_frame = tk.Frame(canvas)
scrollable_frame.grid(row=0, column=0, padx=20, pady=20)

# Enable scrolling with the middle mouse button
canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

frame = scrollable_frame

# Font size
large_font = ("Helvetica", 12)

# Load the image
try:
    logo_image = PhotoImage(file="logo1.png")
except Exception as e:
    logo_image = None

# Packing
# Removed frame packing since the entire window is now scrollable

# Image canvas
# image_frame = tk.LabelFrame(frame, font=("Helvetica", 20, "bold"))
# image_frame.grid(row=0, column=0, padx=20, pady=10)
# if logo_image:
#     logo_label = tk.Label(image_frame, image=logo_image)
#     logo_label.grid(row=0, column=0)

# Patient section
patient_info_frame = tk.LabelFrame(frame, text="Patient Billing Information", font=("Helvetica", 20, "bold"))
patient_info_frame.grid(row=1, column=0, padx=20, pady=10)

# Labels patient information section
full_name_label = tk.Label(patient_info_frame, text="Full Name", font=large_font)
full_name_label.grid(row=0, column=0)
full_name_entry = tk.Entry(patient_info_frame, font=large_font, width=20)
full_name_entry.grid(row=1, column=0)

patient_no_label = tk.Label(patient_info_frame, text="Patient No.", font=large_font)
patient_no_label.grid(row=0, column=1)
patient_entry = tk.Entry(patient_info_frame, font=large_font, width=20)
patient_entry.grid(row=1, column=1)

invoice_label = tk.Label(patient_info_frame, text="Invoice No.", font=large_font)
invoice_label.grid(row=0, column=2)
invoice_entry = tk.Entry(patient_info_frame, font=large_font, width=20)
invoice_entry.grid(row=1, column=2)

email_label = tk.Label(patient_info_frame, text="Email", font=large_font)
email_label.grid(row=0, column=3)
email_entry = tk.Entry(patient_info_frame, font=large_font, width=20)
email_entry.grid(row=1, column=3)

mobile_label = tk.Label(patient_info_frame, text="Mobile Number", font=large_font)
mobile_label.grid(row=2, column=0)
mobile_entry = tk.Entry(patient_info_frame, font=large_font, width=20)
mobile_entry.grid(row=3, column=0)

for widget in patient_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Billing section area
billing_section = tk.LabelFrame(frame, text="Billing Information", font=("Helvetica", 20, "bold"))
billing_section.grid(row=2, column=0, sticky="news", padx=20, pady=10)

amount_label = tk.Label(billing_section, text="Amount ($)", font=large_font)
amount_label.grid(row=0, column=0)
amount_label_spinbox = tk.Entry(billing_section, font=large_font, width=20, justify='right')
amount_label_spinbox.grid(row=1, column=0)

net_paid_label = tk.Label(billing_section, text="Net Amount Paid ($)", font=large_font)
net_paid_label.grid(row=0, column=1)
net_paid_spinbox = tk.Entry(billing_section, font=large_font, width=20, justify='right')
net_paid_spinbox.grid(row=1, column=1)

amount_outstanding_label = tk.Label(billing_section, text="Amount Outstanding ($)", font=large_font)
amount_outstanding_label.grid(row=0, column=2)
amount_outstanding_entry = tk.Entry(billing_section, font=large_font, width=20, justify='right', state='readonly')
amount_outstanding_entry.grid(row=1, column=2)

# Update the outstanding amount data in real time
amount_label_spinbox.bind("<KeyRelease>", update_outstanding)
net_paid_spinbox.bind("<KeyRelease>", update_outstanding)
net_paid_spinbox.bind("<KeyRelease>", update_outstanding)

# Date issued and due date fields
date_issued_label = tk.Label(billing_section, text="Date Issued", font=large_font)
date_issued_label.grid(row=2, column=0)
date_entry = DateEntry(billing_section, font=large_font, width=20, background='blue', foreground='white', borderwidth=5, date_pattern='dd/MM/yyyy')
date_entry.grid(row=3, column=0)

due_date_label = tk.Label(billing_section, text="Due Date", font=large_font)
due_date_label.grid(row=2, column=1)
date_due_entry = DateEntry(billing_section, font=large_font, width=20, background='blue', foreground='white', borderwidth=5, date_pattern='dd/MM/yyyy')
date_due_entry.grid(row=3, column=1)

# Track changes in the date fields
date_due_entry.bind("<FocusOut>", calculate_days_overdue)

# Days overdue field
days_overdue_label = tk.Label(billing_section, text="Days Overdue", font=large_font)
days_overdue_label.grid(row=2, column=2)
days_overdue_entry = tk.Entry(billing_section, font=large_font, width=20, justify='right', state='readonly')
days_overdue_entry.grid(row=3, column=2)

# Invoice status section
invoice_status_label = tk.Label(billing_section, text="Invoice Status", font=large_font)
invoice_status_label.grid(row=4, column=0)
invoice_status_dropbox = ttk.Combobox(billing_section, values=["Paid", "Unpaid", "Partially Paid"], font=large_font, state='readonly')
invoice_status_dropbox.grid(row=5, column=0)

# Color indicator label for status
status_color_label = tk.Label(billing_section, width=20, bg='white', justify='right')
status_color_label.grid(row=5, column=1)

# Bind the event to change color when selection changes
invoice_status_dropbox.bind("<<ComboboxSelected>>", update_invoice_status_color)

for widget in billing_section.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Admin Information section
admin_section = tk.LabelFrame(frame, text="Admin Information", font=("Helvetica", 20, "bold"))
admin_section.grid(row=3, column=0, sticky="news", padx=20, pady=10)

invoice_sent_via = tk.Label(admin_section, text="**Invoice Sent Via Email**", font=large_font)
invoice_sent_via.grid(row=1, column=0)
assigned_label = tk.Label(admin_section, text="Assigned To", font=large_font)
assigned_label.grid(row=2, column=0)
assigned_entry = tk.Entry(admin_section, font=large_font, width=20)
assigned_entry.grid(row=3, column=0)

debt_collector_label = tk.Label(admin_section, text="Debt Collector", font=large_font)
debt_collector_label.grid(row=2, column=1)
debt_collector_dropbox = ttk.Combobox(admin_section, values=["Yes", "No"], font=large_font, state='readonly')
debt_collector_dropbox.grid(row=3, column=1)

Invoice_Link_label = tk.Label(admin_section, text="Invoice Link", font=large_font)
Invoice_Link_label.grid(row=2, column=2)
Invoice_Link_entry = tk.Entry(admin_section, font=large_font, width=20)
Invoice_Link_entry.grid(row=3, column=2)

credit_note_reason_label = tk.Label(admin_section, text="Credit Note Reason", font=large_font)
credit_note_reason_label.grid(row=5, column=0)
credit_note_reason_entry = tk.Text(admin_section, font=large_font, width=20, height=5)
credit_note_reason_entry.grid(row=6, column=0)

button = tk.Button(frame, text="Enter data", command=submit_data)
button.grid(row=4, column=0, sticky="news", padx=20, pady=10)


for widget in admin_section.winfo_children():
    widget.grid_configure(padx=10, pady=5)

window.mainloop()
