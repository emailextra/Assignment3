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