import tkinter as tk
from tkinter import ttk, messagebox, StringVar
import customtkinter
import db

# Initialize the app window
app = customtkinter.CTk()
app.title("MOVIE TICKET BOOKING SYSTEM")
app.geometry('1000x1000')
app.config(bg='#18161D')
app.resizable(False, False)

# Fonts
font1 = ('Arial', 25, 'bold')
font2 = ('Arial', 13, 'bold')
font3 = ('Arial', 18, 'bold')

# Function to update treeview with tickets
def add_to_treeview():
    conn = db.connect_to_database()
    tickets = db.get_tickets(conn)
    conn.close()
    tree.delete(*tree.get_children())
    for ticket in tickets:
        if ticket[2] > 0:
            tree.insert('', tk.END, values=ticket)

# Reservation UI display
def reservation(name, movie, quantity, price):
    total_price = price * quantity

    frame = customtkinter.CTkFrame(
        app, bg_color='#18161D', fg_color='#292933',
        corner_radius=10, border_width=2, border_color='#0f0',
        width=200, height=130
    )
    frame.place(x=390, y=450)

    customtkinter.CTkLabel(frame, font=font3, text=f'Name: {name}', text_color='#fff', bg_color='#18161D').place(x=10, y=10)
    customtkinter.CTkLabel(frame, font=font3, text=f'Movie: {movie}', text_color='#fff', bg_color='#18161D').place(x=10, y=50)
    customtkinter.CTkLabel(frame, font=font3, text=f'Total: {total_price}', text_color='#fff', bg_color='#18161D').place(x=10, y=90)

    return total_price

# Book button handler
def book():
    customer_name = name_entry.get()
    selected_item = tree.focus()

    if not selected_item:
        messagebox.showerror('Error', 'Choose a ticket to book')
        return

    if not customer_name:
        messagebox.showerror('Error', 'Enter Customer name')
        return

    row = tree.item(selected_item)['values']
    if len(row) < 4:
        messagebox.showerror('Error', 'Ticket data is incomplete')
        return

    ticket_id = row[0]
    movie_name = row[1]
    available_tickets = row[2]
    ticket_price = row[3]

    try:
        booked_quantity = int(variable.get())
    except ValueError:
        messagebox.showerror('Error', 'Invalid number of tickets')
        return

    if booked_quantity > available_tickets:
        messagebox.showerror('Error', 'Not enough tickets')
        return

    # Update DB
    conn = db.connect_to_database()
    db.update_quantity(conn, ticket_id, booked_quantity)
    conn.close()

    add_to_treeview()
    total_price = reservation(customer_name, movie_name, booked_quantity, ticket_price)

    # Save to file
    with open('Ticket.txt', 'a') as file:
        file.write(f'Customer Name: {customer_name}\n')
        file.write(f'Movie Name: {movie_name}\n')
        file.write(f'Total: {total_price}$\n======================\n')

    messagebox.showinfo('Success', 'Tickets are booked')
    print(f'Success: Booked {booked_quantity} tickets for {movie_name}')

# UI Elements
ticket_label = customtkinter.CTkLabel(app, font=font1, text='Available Films', text_color='#fff', bg_color='#18161D')
ticket_label.place(x=360, y=20)

name_label = customtkinter.CTkLabel(app, font=font3, text='Customer name:', text_color='#fff', bg_color='#18161D')
name_label.place(x=330, y=300)

name_entry = customtkinter.CTkEntry(app, font=font3, text_color='#000', fg_color='#fff',
                                    border_color='#AA04A7', border_width=2, width=160)
name_entry.insert(0, "Enter your name")
name_entry.place(x=490, y=300)

number_label = customtkinter.CTkLabel(app, font=font3, text='No. of Tickets:', text_color='#fff', bg_color='#18161D')
number_label.place(x=350, y=350)

variable = StringVar()
option = ['1', '2', '3']
duration_option = customtkinter.CTkComboBox(
    app, font=font3, text_color='#000', fg_color='#fff',
    dropdown_hover_color='#AA04A7', button_color='#AA04A7',
    button_hover_color='#AA04A7', border_color='#AA04A7',
    width=160, variable=variable, values=option, state='readonly'
)
duration_option.set('1')
duration_option.place(x=490, y=350)

book_button = customtkinter.CTkButton(app, font=font3, text_color='#fff', text='Book tickets',
                                      fg_color='#AA04A7', bg_color='#18161D', cursor='hand2',
                                      corner_radius=15, width=200, command=book)
book_button.place(x=390, y=400)

# TreeView Styling and Setup
style = ttk.Style(app)
style.theme_use('clam')
style.configure('TreeView', font=font2, foreground='#fff', background='#000', fieldbackground='#292933')
style.map('Treeview', background=[('selected', '#AA04A7')])

tree = ttk.Treeview(app, height=8)
tree['columns'] = ('Ticket ID', 'Movie Name', 'Available Tickets', 'Ticket Price')
tree.heading('#0', text='', anchor=tk.CENTER)
tree.heading('Ticket ID', text='Ticket ID', anchor=tk.CENTER)
tree.heading('Movie Name', text='Movie Name', anchor=tk.CENTER)
tree.heading('Available Tickets', text='Available Tickets', anchor=tk.CENTER)
tree.heading('Ticket Price', text='Ticket Price', anchor=tk.CENTER)

tree.column('#0', width=0, stretch=tk.NO)
tree.column('Ticket ID', anchor=tk.CENTER, width=100)
tree.column('Movie Name', anchor=tk.CENTER, width=100)
tree.column('Available Tickets', anchor=tk.CENTER, width=100)
tree.column('Ticket Price', anchor=tk.CENTER, width=100)
tree.place(x=290, y=95)

# Load data
add_to_treeview()

# Run app
app.mainloop()
