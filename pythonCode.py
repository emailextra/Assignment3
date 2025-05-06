import random
import time
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pickle
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")


# Base User class
class User:
    def __init__(self, name, email):
        self.userId = str(random.randint(1000, 9999))
        self.name = name
        self.email = email

    def getUserId(self):
        return self.userId

    def setUserId(self, userId):
        self.userId = userId

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email


class Customer(User):
    def __init__(self, name, email, phone):
        User.__init__(self, name, email)
        self.phone = phone
        self.bookings = []

    def getPhone(self):
        return self.phone

    def setPhone(self, phone):
        self.phone = phone

    def addBooking(self, booking):
        self.bookings.append(booking)

    def getBookings(self):
        return self.bookings

    def setBookings(self, bookings):
        self.bookings = bookings

    def removeBooking(self, booking_id):
        for i, booking in enumerate(self.bookings):
            if booking.getBookingId() == booking_id:
                del self.bookings[i]
                return True
        return False


class Admin(User):
    def __init__(self, name, email):
        User.__init__(self, name, email)

    def createEvent(self, name, date, venue, total_seats):
        return Event(name, date, venue, total_seats)

    def manageEvents(self):
        # Implementation for managing events
        pass

    def generateReports(self):
        # Implementation for generating reports
        pass

    def setDiscount(self, event, discount_percentage):
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100")

        for ticket in event.getTickets():
            if not ticket.isBooked():
                original_price = ticket.getPrice()
                discounted_price = original_price * (1 - discount_percentage / 100)
                ticket.setPrice(discounted_price)


class Account:
    def __init__(self, username, password, user):
        self.username = username
        self.password = password
        self.user = user

    def getUsername(self):
        return self.username

    def setUsername(self, username):
        self.username = username

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user

    def authenticate(self, username, password):
        return self.username == username and self.password == password

    def updatePassword(self, old_password, new_password):
        if self.password == old_password:
            self.password = new_password
            return True
        return False


class Event:
    def __init__(self, name, date, venue, total_seats):
        self.eventId = "E" + str(random.randint(100, 999))
        self.name = name
        self.date = date
        self.venue = venue
        self.totalSeats = total_seats
        self.availableSeats = total_seats
        self.tickets = []
        self.ticketTypes = {
            "Single Day": {"price": 150.0, "features": "Access to race day only"},
            "Weekend": {"price": 300.0, "features": "Access to qualifying and race day"},
            "VIP": {"price": 500.0, "features": "Premium seating, paddock access, and refreshments"}
        }

    def getEventId(self):
        return self.eventId

    def setEventId(self, eventId):
        self.eventId = eventId

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getDate(self):
        return self.date

    def setDate(self, date):
        self.date = date

    def getVenue(self):
        return self.venue

    def setVenue(self, venue):
        self.venue = venue

    def getTotalSeats(self):
        return self.totalSeats

    def setTotalSeats(self, totalSeats):
        self.totalSeats = totalSeats

    def getAvailableSeats(self):
        return self.availableSeats

    def setAvailableSeats(self, availableSeats):
        self.availableSeats = availableSeats

    def getTickets(self):
        return self.tickets

    def setTickets(self, tickets):
        self.tickets = tickets

    def getTicketTypes(self):
        return self.ticketTypes

    def setTicketTypes(self, ticketTypes):
        self.ticketTypes = ticketTypes

    def createTicket(self, seat_number, price, ticket_type="Single Day"):
        ticket = Ticket(self, seat_number, price, ticket_type)
        self.tickets.append(ticket)
        return ticket

    def updateAvailableSeats(self):
        booked = 0
        for ticket in self.tickets:
            if ticket.isBooked():
                booked = booked + 1
        self.availableSeats = self.totalSeats - booked


class Ticket:
    def __init__(self, event, seat_number, price, ticket_type="Single Day"):
        self.ticketId = "T" + str(random.randint(1000, 9999))
        self.event = event
        self.price = price
        self.seatNumber = seat_number
        self.booked = False
        self.ticketType = ticket_type
        self.purchaseDate = None

    def getTicketId(self):
        return self.ticketId

    def setTicketId(self, ticketId):
        self.ticketId = ticketId

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getSeatNumber(self):
        return self.seatNumber

    def setSeatNumber(self, seatNumber):
        self.seatNumber = seatNumber

    def isBooked(self):
        return self.booked

    def setBooked(self, booked):
        self.booked = booked

    def getEvent(self):
        return self.event

    def setEvent(self, event):
        self.event = event

    def getTicketType(self):
        return self.ticketType

    def setTicketType(self, ticketType):
        self.ticketType = ticketType

    def getPurchaseDate(self):
        return self.purchaseDate

    def setPurchaseDate(self, purchaseDate):
        self.purchaseDate = purchaseDate

    def bookTicket(self):
        if not self.booked:
            self.booked = True
            self.purchaseDate = time.strftime("%Y-%m-%d")
            self.event.updateAvailableSeats()
            return True
        return False


class Booking:
    def __init__(self, customer):
        self.bookingId = "B" + str(random.randint(1000, 9999))
        self.bookingDate = time.strftime("%Y-%m-%d")
        self.status = "Pending"
        self.tickets = []
        self.customer = customer
        self.payment = None

    def getBookingId(self):
        return self.bookingId

    def setBookingId(self, bookingId):
        self.bookingId = bookingId

    def getBookingDate(self):
        return self.bookingDate

    def setBookingDate(self, bookingDate):
        self.bookingDate = bookingDate

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getTickets(self):
        return self.tickets

    def setTickets(self, tickets):
        self.tickets = tickets

    def getCustomer(self):
        return self.customer

    def setCustomer(self, customer):
        self.customer = customer

    def getPayment(self):
        return self.payment

    def setPayment(self, payment):
        self.payment = payment

    def addTicket(self, ticket):
        if ticket.bookTicket():
            self.tickets.append(ticket)

    def removeTicket(self, ticket):
        if ticket in self.tickets:
            self.tickets.remove(ticket)
            ticket.setBooked(False)
            ticket.getEvent().updateAvailableSeats()

    def calculateTotal(self):
        total = 0
        for ticket in self.tickets:
            total = total + ticket.getPrice()
        return total

    def confirmBooking(self):
        if len(self.tickets) > 0 and self.payment and self.payment.getStatus() == "Completed":
            self.status = "Confirmed"
            return True
        return False


class Payment:
    def __init__(self, amount):
        self.paymentId = "P" + str(random.randint(1000, 9999))
        self.amount = amount
        self.paymentDate = None
        self.status = "Pending"
        self.paymentMethod = None
        self.cardNumber = None

    def getPaymentId(self):
        return self.paymentId

    def setPaymentId(self, paymentId):
        self.paymentId = paymentId

    def getAmount(self):
        return self.amount

    def setAmount(self, amount):
        self.amount = amount

    def getPaymentDate(self):
        return self.paymentDate

    def setPaymentDate(self, paymentDate):
        self.paymentDate = paymentDate

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getPaymentMethod(self):
        return self.paymentMethod

    def setPaymentMethod(self, paymentMethod):
        self.paymentMethod = paymentMethod

    def getCardNumber(self):
        return self.cardNumber

    def setCardNumber(self, cardNumber):
        self.cardNumber = cardNumber

    def processPayment(self, payment_method, card_number):
        try:
            # Validate card number (simplified)
            if len(card_number) < 13 or len(card_number) > 19:
                raise ValueError("Invalid card number length")

            if not card_number.isdigit():
                raise ValueError("Card number must contain only digits")

            self.paymentMethod = payment_method
            self.cardNumber = card_number[-4:]  # Store only last 4 digits for security
            self.paymentDate = time.strftime("%Y-%m-%d")
            self.status = "Completed"
            return True
        except ValueError as e:
            messagebox.showerror("Payment Error", str(e))
            return False

    def refund(self):
        try:
            if self.status != "Completed":
                raise ValueError("Cannot refund a payment that is not completed")
            self.status = "Refunded"
            return True
        except ValueError as e:
            messagebox.showerror("Refund Error", str(e))
            return False


class Order:
    def __init__(self, booking, payment):
        self.orderId = "O" + str(random.randint(1000, 9999))
        self.booking = booking
        self.payment = payment
        self.orderDate = time.strftime("%Y-%m-%d")
        self.status = "Processed"

    def getOrderId(self):
        return self.orderId

    def setOrderId(self, orderId):
        self.orderId = orderId

    def getBooking(self):
        return self.booking

    def setBooking(self, booking):
        self.booking = booking

    def getPayment(self):
        return self.payment

    def setPayment(self, payment):
        self.payment = payment

    def getOrderDate(self):
        return self.orderDate

    def setOrderDate(self, orderDate):
        self.orderDate = orderDate

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status


# Data Manager for handling file operations
class DataManager:
    def __init__(self):
        self.accounts_file = "data/accounts.pkl"
        self.events_file = "data/events.pkl"
        self.orders_file = "data/orders.pkl"

    def save_accounts(self, accounts):
        try:
            with open(self.accounts_file, "wb") as file:
                pickle.dump(accounts, file)
        except Exception as e:
            messagebox.showerror("Error", "Failed to save accounts: " + str(e))

    def load_accounts(self):
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, "rb") as file:
                    return pickle.load(file)
            return []
        except Exception as e:
            messagebox.showerror("Error", "Failed to load accounts: " + str(e))
            return []

    def save_events(self, events):
        try:
            with open(self.events_file, "wb") as file:
                pickle.dump(events, file)
        except Exception as e:
            messagebox.showerror("Error", "Failed to save events: " + str(e))

    def load_events(self):
        try:
            if os.path.exists(self.events_file):
                with open(self.events_file, "rb") as file:
                    return pickle.load(file)
            return []
        except Exception as e:
            messagebox.showerror("Error", "Failed to load events: " + str(e))
            return []

    def save_orders(self, orders):
        try:
            with open(self.orders_file, "wb") as file:
                pickle.dump(orders, file)
        except Exception as e:
            messagebox.showerror("Error", "Failed to save orders: " + str(e))

    def load_orders(self):
        try:
            if os.path.exists(self.orders_file):
                with open(self.orders_file, "rb") as file:
                    return pickle.load(file)
            return []
        except Exception as e:
            messagebox.showerror("Error", "Failed to load orders: " + str(e))
            return []


# Main GUI Application
class TicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket Booking System")
        self.root.geometry("800x600")
        self.data_manager = DataManager()
        self.accounts = self.data_manager.load_accounts()
        self.events = self.data_manager.load_events()
        self.orders = self.data_manager.load_orders()
        self.current_user = None

        # Welcome Frame
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(fill="both", expand=True)
        self.show_welcome_screen()

    def show_welcome_screen(self):
        for widget in self.welcome_frame.winfo_children():
            widget.destroy()

        tk.Label(self.welcome_frame, text="Welcome to Ticket Booking System", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.welcome_frame, text="Login", width=20, command=self.show_login_screen).pack(pady=10)
        tk.Button(self.welcome_frame, text="Create Account", width=20, command=self.show_account_creation_screen).pack(
            pady=10)

    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.welcome_frame, text="Login", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.welcome_frame, text="Username").pack()
        username_entry = tk.Entry(self.welcome_frame)
        username_entry.pack()

        tk.Label(self.welcome_frame, text="Password").pack()
        password_entry = tk.Entry(self.welcome_frame, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            for account in self.accounts:
                if account.authenticate(username, password):
                    self.current_user = account.getUser()
                    if isinstance(self.current_user, Admin):
                        self.show_admin_dashboard()
                    elif isinstance(self.current_user, Customer):
                        self.show_customer_dashboard()
                    return
            messagebox.showerror("Login Failed", "Invalid username or password")

        tk.Button(self.welcome_frame, text="Login", command=login).pack(pady=10)
        tk.Button(self.welcome_frame, text="Back", command=self.show_welcome_screen).pack(pady=10)

    def show_account_creation_screen(self):
        self.clear_screen()
        tk.Label(self.welcome_frame, text="Create Account", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.welcome_frame, text="Name").pack()
        name_entry = tk.Entry(self.welcome_frame)
        name_entry.pack()

        tk.Label(self.welcome_frame, text="Email").pack()
        email_entry = tk.Entry(self.welcome_frame)
        email_entry.pack()

        tk.Label(self.welcome_frame, text="Phone").pack()
        phone_entry = tk.Entry(self.welcome_frame)
        phone_entry.pack()

        tk.Label(self.welcome_frame, text="Username").pack()
        username_entry = tk.Entry(self.welcome_frame)
        username_entry.pack()

        tk.Label(self.welcome_frame, text="Password").pack()
        password_entry = tk.Entry(self.welcome_frame, show="*")
        password_entry.pack()

        def create_account():
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not name or not email or not phone or not username or not password:
                messagebox.showerror("Error", "All fields are required")
                return

            # Create a new customer and account
            customer = Customer(name, email, phone)
            new_account = Account(username, password, customer)

            # Check if username is unique
            for account in self.accounts:
                if account.getUsername() == username:
                    messagebox.showerror("Error", "Username already exists")
                    return

            self.accounts.append(new_account)
            self.data_manager.save_accounts(self.accounts)
            messagebox.showinfo("Success", "Account created successfully")
            self.show_welcome_screen()

        tk.Button(self.welcome_frame, text="Create Account", command=create_account).pack(pady=10)
        tk.Button(self.welcome_frame, text="Back", command=self.show_welcome_screen).pack(pady=10)

    def show_customer_dashboard(self):
        self.clear_screen()
        tk.Label(self.welcome_frame, text=f"Welcome, {self.current_user.getName()}", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.welcome_frame, text="View Events", width=20, command=self.show_event_list).pack(pady=10)
        tk.Button(self.welcome_frame, text="View Bookings", width=20, command=self.show_booking_list).pack(pady=10)
        tk.Button(self.welcome_frame, text="Logout", width=20, command=self.logout).pack(pady=10)

    def show_admin_dashboard(self):
        self.clear_screen()
        tk.Label(self.welcome_frame, text="Admin Dashboard", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.welcome_frame, text="Manage Events", width=20, command=self.manage_events).pack(pady=10)
        tk.Button(self.welcome_frame, text="View Reports", width=20, command=self.show_reports).pack(pady=10)
        tk.Button(self.welcome_frame, text="Logout", width=20, command=self.logout).pack(pady=10)

    def show_event_list(self):
        self.clear_screen()
        tk.Label(self.welcome_frame, text="Available Events", font=("Arial", 18)).pack(pady=20)

        for event in self.events:
            event_frame = tk.Frame(self.welcome_frame, relief="ridge", borderwidth=1)
            event_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(event_frame, text=f"Event: {event.getName()}").pack(anchor="w")
            tk.Label(event_frame, text=f"Date: {event.getDate()}").pack(anchor="w")
            tk.Label(event_frame, text=f"Venue: {event.getVenue()}").pack(anchor="w")
            tk.Label(event_frame, text=f"Available Seats: {event.getAvailableSeats()}").pack(anchor="w")

            tk.Button(event_frame, text="Book Tickets", command=lambda e=event: self.book_tickets(e)).pack(anchor="e",
                                                                                                           pady=5)

        tk.Button(self.welcome_frame, text="Back", command=self.show_customer_dashboard).pack(pady=10)

    def book_tickets(self, event):
        self.clear_screen()
        tk.Label(self.welcome_frame, text=f"Book Tickets for {event.getName()}", font=("Arial", 18)).pack(pady=20)

        ticket_types = event.getTicketTypes()
        ticket_selections = {}

        for ticket_type, details in ticket_types.items():
            frame = tk.Frame(self.welcome_frame)
            frame.pack(pady=5)

            tk.Label(frame, text=f"{ticket_type} - ${details['price']}").pack(side="left", padx=10)
            tk.Label(frame, text=details["features"]).pack(side="left", padx=10)
            quantity_var = tk.IntVar(value=0)
            ticket_selections[ticket_type] = quantity_var

            tk.Spinbox(frame, from_=0, to=event.getAvailableSeats(), textvariable=quantity_var, width=5).pack(
                side="right")

        def confirm_booking():
            total_tickets = 0
            selected_tickets = []
            for ticket_type, quantity_var in ticket_selections.items():
                quantity = quantity_var.get()
                if quantity > 0:
                    total_tickets += quantity
                    for _ in range(quantity):
                        ticket = event.createTicket(seat_number=random.randint(1, 1000),
                                                    price=ticket_types[ticket_type]["price"],
                                                    ticket_type=ticket_type)
                        selected_tickets.append(ticket)

            if total_tickets == 0:
                messagebox.showerror("Error", "Please select at least one ticket")
                return

                # Create booking and proceed to payment
            booking = Booking(self.current_user)
            for ticket in selected_tickets:
                booking.addTicket(ticket)

            self.current_user.addBooking(booking)
            self.data_manager.save_events(self.events)
            self.show_payment_screen(booking)

        tk.Button(self.welcome_frame, text="Confirm Booking", command=confirm_booking).pack(pady=10)
        tk.Button(self.welcome_frame, text="Back", command=self.show_event_list).pack(pady=10)

    def show_payment_screen(self, booking):
        self.clear_screen()
        tk.Label(self.welcome_frame, text="Payment", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.welcome_frame, text=f"Total Amount: ${booking.calculateTotal()}").pack(pady=10)

        tk.Label(self.welcome_frame, text="Payment Method").pack()
        payment_method_var = tk.StringVar(value="Credit/Debit Card")
        tk.Radiobutton(self.welcome_frame, text="Credit/Debit Card", variable=payment_method_var,
                       value="Credit/Debit Card").pack()
        tk.Radiobutton(self.welcome_frame, text="PayPal", variable=payment_method_var, value="PayPal").pack()

        tk.Label(self.welcome_frame, text="Card Number").pack()
        card_number_entry = tk.Entry(self.welcome_frame)
        card_number_entry.pack()

        def process_payment():
            payment_method = payment_method_var.get()
            card_number = card_number_entry.get()

            if not card_number:
                messagebox.showerror("Error", "Card number is required")
                return

            payment = Payment(booking.calculateTotal())
            if payment.processPayment(payment_method, card_number):
                booking.setPayment(payment)
                if booking.confirmBooking():
                    self.orders.append(Order(booking, payment))
                    self.data_manager.save_orders(self.orders)
                    messagebox.showinfo("Success", "Payment successful and booking confirmed!")
                    self.show_customer_dashboard()
                else:
                    messagebox.showerror("Error", "Booking confirmation failed")
            else:
                messagebox.showerror("Error", "Payment processing failed")

        tk.Button(self.welcome_frame, text="Pay Now", command=process_payment).pack(pady=10)
        tk.Button(self.welcome_frame, text="Back",
                  command=lambda: self.book_tickets(booking.getTickets()[0].getEvent())).pack(pady=10)

    def show_booking_list(self):
        self.clear_screen()
        tk.Label(self.welcome_frame, text="Your Bookings", font=("Arial", 18)).pack(pady=20)

        if len(self.current_user.getBookings()) == 0:
            tk.Label(self.welcome_frame, text="No bookings found").pack(pady=10)
        else:
            for booking in self.current_user.getBookings():
                booking_frame = tk.Frame(self.welcome_frame, relief="ridge", borderwidth=1)
                booking_frame.pack(fill="x", padx=10, pady=5)

                tk.Label(booking_frame, text=f"Booking ID: {booking.getBookingId()}").pack(anchor="w")
                tk.Label(booking_frame, text=f"Booking Date: {booking.getBookingDate()}").pack(anchor="w")
                tk.Label(booking_frame, text=f"Status: {booking.getStatus()}").pack(anchor="w")
                tk.Label(booking_frame, text=f"Total Tickets: {len(booking.getTickets())}").pack(anchor="w")

                def show_ticket_details(booking_obj=booking):
                    self.clear_screen()
                    tk.Label(self.welcome_frame, text=f"Tickets for Booking ID: {booking_obj.getBookingId()}",
                             font=("Arial", 18)).pack(pady=20)

                    for ticket in booking_obj.getTickets():
                        ticket_frame = tk.Frame(self.welcome_frame, relief="ridge", borderwidth=1)
                        ticket_frame.pack(fill="x", padx=10, pady=5)

                        tk.Label(ticket_frame, text=f"Ticket ID: {ticket.getTicketId()}").pack(anchor="w")
                        tk.Label(ticket_frame, text=f"Type: {ticket.getTicketType()}").pack(anchor="w")
                        tk.Label(ticket_frame, text=f"Price: ${ticket.getPrice()}").pack(anchor="w")
                        tk.Label(ticket_frame, text=f"Seat Number: {ticket.getSeatNumber()}").pack(anchor="w")
                        tk.Label(ticket_frame, text=f"Purchase Date: {ticket.getPurchaseDate()}").pack(anchor="w")

                    tk.Button(self.welcome_frame, text="Back", command=self.show_booking_list).pack(pady=10)

                tk.Button(booking_frame, text="View Tickets", command=show_ticket_details).pack(anchor="e", pady=5)

            tk.Button(self.welcome_frame, text="Back", command=self.show_customer_dashboard).pack(pady=10)

    def manage_events(self):
        self.clear_screen()
        tk.Label(self.welcome_frame, text="Manage Events", font=("Arial", 18)).pack(pady=20)

        for event in self.events:
            event_frame = tk.Frame(self.welcome_frame, relief="ridge", borderwidth=1)
            event_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(event_frame, text=f"Event: {event.getName()}").pack(anchor="w")
            tk.Label(event_frame, text=f"Date: {event.getDate()}").pack(anchor="w")
            tk.Label(event_frame, text=f"Venue: {event.getVenue()}").pack(anchor="w")
            tk.Label(event_frame, text=f"Available Seats: {event.getAvailableSeats()}").pack(anchor="w")

            def update_discount(event_obj=event):
                discount = simpledialog.askinteger("Set Discount", "Enter discount percentage (0-100):")
                if discount is not None:
                    try:
                        Admin(self.current_user.getName(), self.current_user.getEmail()).setDiscount(event_obj,
                                                                                                             discount)
                        self.data_manager.save_events(self.events)
                        messagebox.showinfo("Success", f"Discount of {discount}% applied successfully!")
                        self.manage_events()
                    except ValueError as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(event_frame, text="Set Discount", command=update_discount).pack(anchor="e", pady=5)
            tk.Button(self.welcome_frame, text="Back", command=self.show_admin_dashboard).pack(pady=10)

    def show_reports(self):
        self.clear_screen()
        tk.Label(self.welcome_frame, text="Ticket Sales Report", font=("Arial", 18)).pack(pady=20)

        sales_data = {}
        for order in self.orders:
            order_date = order.getOrderDate()
            if order_date not in sales_data:
                sales_data[order_date] = 0
            sales_data[order_date] += len(order.getBooking().getTickets())

        if not sales_data:
            tk.Label(self.welcome_frame, text="No sales data available.").pack(pady=10)
        else:
            fig, ax = plt.subplots()
            ax.bar(sales_data.keys(), sales_data.values())
            ax.set_title("Ticket Sales by Date")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Tickets Sold")

            canvas = FigureCanvasTkAgg(fig, self.welcome_frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)

        tk.Button(self.welcome_frame, text="Back", command=self.show_admin_dashboard).pack(pady=10)

    def logout(self):
        self.current_user = None
        self.show_welcome_screen()

    def clear_screen(self):
        for widget in self.welcome_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingApp(root)
    root.mainloop()