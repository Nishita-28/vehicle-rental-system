# FINAL CODE
import re
import mysql.connector
import random

from designs import *

printbanner()

mydb = mysql.connector.connect(host="localhost", user="root", password="YOUR_PASSWORD")

if mydb.is_connected() == True:

    # Creating database if it doesn't exist
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Free2Move;")
    mycursor.execute("USE Free2Move;")


    def create_tables():
        # Creating table if it doesn't exist
        mycursor.execute("CREATE TABLE IF NOT EXISTS User(u_id INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(255),Phone_Number VARCHAR(255) UNIQUE,email VARCHAR(255))")

        mycursor.execute("CREATE TABLE IF NOT EXISTS Vehicles(v_id INT AUTO_INCREMENT PRIMARY KEY,Vehicle_Type VARCHAR(255),Vehicle_Model VARCHAR(255),Rate Float)")
        mycursor.execute("Select * from vehicles;")
        d5 = mycursor.fetchall()
        if d5 == []:
            vt = ["Car", "Bike", "Scooter"]
            for a in vt:
                if a == "Car":
                    cmodel = ["Maruti Swift Dzire", "Ford Ecosport"]
                    for b in range(len(cmodel)):
                        ccost = [2400.0, 2880.0]
                        mycursor.execute('''INSERT INTO Vehicles(Vehicle_Type,Vehicle_Model,Rate) 
                        VALUES('{}','{}',{})'''.format(a, cmodel[b], ccost[b]))
                elif a == "Bike":
                    bmodel = ["Honda", "Royal Enfield"]
                    for c in range(len(bmodel)):
                        bcost = [480.0, 552.0]
                        mycursor.execute('''INSERT INTO Vehicles(Vehicle_Type,Vehicle_Model,Rate) 
                        VALUES('{}','{}',{})'''.format(a, bmodel[c], bcost[c]))
                elif a == "Scooter":
                    smodel = ["Honda Activa", "Honda Dio"]
                    for d in range(len(smodel)):
                        scost = [360.0, 400.0]
                        mycursor.execute('''INSERT INTO Vehicles(Vehicle_Type,Vehicle_Model,Rate) 
                                        VALUES('{}','{}',{})'''.format(a, smodel[d], scost[d]))

        mydb.commit()

        mycursor.execute('''
                                CREATE TABLE IF NOT EXISTS `Bookings` (
                                    u_id INT AUTO_INCREMENT PRIMARY KEY,
                                    User_Name varchar(225),
                                    ph_num varchar(225),
                                    V_Type varchar(225),
                                    V_Model varchar(225),
                                    Amount Float,
                                    PickUp_Date Date,
                                    DropOff_Date Date,
                                    Payment_Method varchar(225)
                                )
                            ''')
        mydb.commit()

    create_tables()
    book = ""


    # admin/user login
    while True:
        book=""
        log = int(input('''
1. Admin
2. User
3. Exit
Please enter your option:'''))
        if log == 1:
            p_w = input("Please enter password:")
            if p_w == "Admin@123":
                m1 = int(input('''
1. Display Table User
2. Display Table Vehicle
3. Display Table User_Booking
Please enter your option:'''))
                if m1 == 1:
                    mycursor.execute("Select * from User;")
                    d1 = mycursor.fetchall()
                    for i in d1:
                        print(i)
                elif m1 == 2:
                    mycursor.execute("Select * from Vehicles;")
                    d2 = mycursor.fetchall()
                    for i in d2:
                        print(i)
                elif m1 == 3:
                    mycursor.execute("Select * from User_Bookings;")
                    d3 = mycursor.fetchall()
                    for i in d3:
                        print(i)
            else:
                print("Wrong password")
        elif log == 2:
            client_details = {}
            client_details["phone_number"] = input("Enter your phone number: ")


            # Function to validate phone number
            def validate_phone_number(phone_number):
                pattern = r'^[6-9]\d{9}$'
                return re.match(pattern, phone_number) is not None


            while True:
                # Validating phone number
                if validate_phone_number(client_details["phone_number"]):
                    break
                else:
                    print("Invalid phone number. Please try again.")
                    client_details["phone_number"] = input("Enter your phone number: ")

            mycursor.execute(
                "Select * from User where phone_number = {}".format(client_details["phone_number"]))
            d4 = mycursor.fetchone()
            if d4 == None:
                book = "Yes"
                print("Please register")
                while True:
                    client_details["name"] = input("Enter your name: ")
                    if len(client_details["name"]) == 0:
                        print("Please enter a valid name.")
                    else:
                        break

                client_details["email"] = input("Enter your email address: ")


                def validate_email(email):
                    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                    return re.match(pattern, email) is not None

                    # Loop to handle email input until it is valid


                while True:
                    # Validating email address
                    if validate_email(client_details["email"]):
                        break
                    else:
                        print("Invalid email address. Please try again.")
                        client_details["email"] = input("Enter your email address: ")

                mycursor.execute('''INSERT INTO User(Name,Phone_Number,email) 
                VALUES('{}','{}','{}')'''.format(client_details["name"],
                                                 client_details["phone_number"], client_details["email"]))
                mydb.commit()


            else:
                while True:
                    k1 = int(input('''
1. View previous booking
2. Book new
3. Exit
Please enter your option(1/2/3)'''))
                    if k1 == 1:
                        book = "No"
                        mycursor.execute(
                            "Select * from User where phone_number = {}".format(client_details["phone_number"])
                        )
                        p_book = mycursor.fetchall()
                        print(p_book)
                    elif k1 == 2:
                        book = "Yes"
                        mycursor.execute(
                        "Select name from User where phone_number = {}".format(client_details["phone_number"]))
                        client_details["name"] = mycursor.fetchone()[0]
                        print(client_details["name"])
                        mycursor.execute(
                        "Select email from Client_records where phone_number = {}".format(client_details["phone_number"]))
                        client_details["email"] = mycursor.fetchone()[0]
                        print(client_details["email"])
                        break
                    elif k1 == 3:
                        break
                    else:
                        print("Wrong option")
        elif log == 3:
            break
        else:
            print("Wrong option")
        if book == "Yes":
            print('''
Pickup location:
1.Bangalore:#20, 100 ft road, Indiranagar
2.Mumbai:#52, Lokhandwala Market, Andheri West
3.New Delhi:#5, Sarojini Market
4.Chennai:#10, Anna Salai''')

            # Validate pickup location
            pickup_locations = {
                "1": "Bangalore:#20, 100 ft road, Indiranagar",
                "2": "Mumbai:#52, Lokhandwala Market, Andheri West",
                "3": "New Delhi:#5, Sarojini Market",
                "4": "Chennai:#10, Anna Salai"
            }

            pickup_location_choice = input("Enter your pick-up location choice (1-4): ")
            while pickup_location_choice not in pickup_locations:
                print("Invalid pick-up location choice. Please try again.")
                pickup_location_choice = input("Enter your pick-up location choice (1-4): ")

            client_details["pickup_location"] = pickup_locations[pickup_location_choice]
            pickup_location = client_details["pickup_location"]

            print('''
Dropoff location:
1.Bangalore:#20, 100 ft road, Indiranagar
2.Mumbai:#52, Lokhandwala Market, Andheri West
3.New Delhi:#5, Sarojini Market
4.Chennai:#10, Anna Salai''')

            # Validate dropoff location
            dropoff_locations = {
                "1": "Bangalore:#20, 100 ft road, Indiranagar",
                "2": "Mumbai:#52, Lokhandwala Market, Andheri West",
                "3": "New Delhi:#5, Sarojini Market",
                "4": "Chennai:#10, Anna Salai"
            }

            dropoff_location_choice = input("Enter your drop-off location choice (1-4): ")
            while dropoff_location_choice not in dropoff_locations:
                print("Invalid drop-off location choice. Please try again.")
                dropoff_location_choice = input("Enter your drop-off location choice (1-4): ")

            client_details["dropoff_location"] = dropoff_locations[dropoff_location_choice]


            # Generating license
            def generate_license_plate_number(pickup_location):
                if pickup_location == "Bangalore:#20, 100 ft road, Indiranagar":
                    return "KA" + str(random.randint(10, 99)) + "AB" + str(random.randint(1000, 9999))
                elif pickup_location == "Mumbai:#52, Lokhandwala Market, Andheri West":
                    return "MH" + str(random.randint(10, 99)) + "CD" + str(random.randint(1000, 9999))
                elif pickup_location == "New Delhi:#5, Sarojini Market":
                    return "DL" + str(random.randint(10, 99)) + "EF" + str(random.randint(1000, 9999))
                elif pickup_location == "Chennai:#10, Anna Salai":
                    return "TN" + str(random.randint(10, 99)) + "GH" + str(random.randint(1000, 9999))


            license_plate = generate_license_plate_number(client_details["pickup_location"])
            if license_plate is None:
                print("Invalid pickup location!")

            client_details["pickup_date"] = input("Enter pick up date(yyyy-mm-dd):")
            client_details["dropoff_date"] = input("Enter drop off date(yyyy-mm-dd):")
            mycursor.execute(
                "SELECT DATEDIFF('{}','{}')".format(client_details["dropoff_date"], client_details["pickup_date"]))
            rental_days = int(mycursor.fetchone()[0])

            # Accepting vehicle details
            vehicle_details = {}

            # Accepting vehicle type
            print("Vehicle Types:")
            print("1. Car")
            print("2. Bike")
            print("3. Scooter")
            vehicle_type_choice = input("Enter your vehicle type choice (1-3): ")
            vehicle_types = {
                "1": "car",
                "2": "bike",
                "3": "scooter"
            }

            while vehicle_type_choice not in vehicle_types:
                print("Invalid vehicle type choice. Please try again.")
                print("Vehicle Types:")
                print("1. Car")
                print("2. Bike")
                print("3. Scooter")
                vehicle_type_choice = input("Enter your vehicle type choice (1-3): ")

            client_details["vehicle_types"] = vehicle_types[vehicle_type_choice]

            # For Car
            if client_details["vehicle_types"] == "car":
                print("Car Models:")
                print("1. Maruti Swift Dzire (2400 INR per day)")
                print("2. Ford Ecosport (2880 INR per day)")
                car_model_choice = input("Enter your car model choice (1-2): ")
                car_models = {
                    '1': {"model": "Maruti Swift Dzire", "daily_rental_rate": 2400},
                    '2': {"model": "Ford Ecosport", "daily_rental_rate": 2880}
                }
                while car_model_choice not in car_models:
                    print("Invalid car model choice. Please try again.")
                    print("Car Models:")
                    print("1. Maruti Swift Dzire (2400 INR per day)")
                    print("2. Ford Ecosport (2880 INR per day)")
                    car_model_choice = input("Enter your car model choice (1-2): ")

                vehicle_details = car_models[car_model_choice]

                # Calculating amount
                if car_model_choice == '1':
                    final_amount = rental_days * 2400
                elif car_model_choice == '2':
                    final_amount = rental_days * 2880

            # For Bike
            elif client_details["vehicle_types"] == "bike":
                print("Bike Models:")
                print("1. Honda (480 INR per day)")
                print("2. Royal Enfield (552 INR per day)")
                bike_model_choice = input("Enter your bike model choice (1-2): ")
                bike_models = {
                    "1": {"model": "Honda", "daily_rental_rate": 480},
                    "2": {"model": "Royal Enfield", "daily_rental_rate": 552}
                }
                while bike_model_choice not in bike_models:
                    print("Invalid bike model choice. Please try again.")
                    print("Bike Models:")
                    print("1. Honda (480 INR per day)")
                    print("2. Royal Enfield (552 INR per day)")
                    bike_model_choice = input("Enter your bike model choice (1-2): ")

                vehicle_details = bike_models[bike_model_choice]

                # Calculating amount
                if bike_model_choice == '1':
                    final_amount = rental_days * 480
                elif bike_model_choice == '2':
                    final_amount = rental_days * 552

            # For Scooter
            elif client_details["vehicle_types"] == "scooter":
                print("Scooter Models:")
                print("1. Honda Activa (360 INR per day)")
                print("2. Honda Dio (400 INR per day)")
                scooter_model_choice = input("Enter your scooter model choice (1-2): ")
                scooter_models = {
                    "1": {"model": "Honda Activa", "daily_rental_rate": 360},
                    "2": {"model": "Honda Dio", "daily_rental_rate": 400}
                }
                while scooter_model_choice not in scooter_models:
                    print("Invalid scooter model choice. Please try again.")
                    print("Scooter Models:")
                    print("1. Honda Activa (360 INR per day)")
                    print("2. Honda Dio (400 INR per day)")
                    scooter_model_choice = input("Enter your scooter model choice (1-2): ")

                vehicle_details = scooter_models[scooter_model_choice]

                # Calculating amount
                if scooter_model_choice == '1':
                    final_amount = rental_days * 360
                elif scooter_model_choice == '2':
                    final_amount = rental_days * 400

            if final_amount is None:
                print("Invalid vehicle type!")

            while True:
                k2 = int(input('''
Payment methods:
1. Credit Card
2. Debit Card
3. Cash (payment while returning vehicle)
Please enter one of the options(1/2/3):'''))
                if k2 == 1:
                    client_details["payment_method"] = "Credit card"
                    break
                elif k2 == 2:
                    client_details["payment_method"] = "Debit card"
                    break
                elif k2 == 3:
                    client_details["payment_method"] = "Cash"
                    break
                else:
                    print("Wrong option")

            import smtplib
            from email.mime.text import MIMEText


            def send_email(client_details, vehicle_details, final_amount, rental_days):
                sender_email = "xfree.2.movex@gmail.com"
                receiver_email = client_details["email"]
                subject = "Vehicle Rental Details"

                vehicle_type = client_details.get("vehicle_types", "N/A")
                license_plate = vehicle_details.get("license_plate", "N/A")
                pickup_location = client_details.get("pickup_location", "N/A")

                message = f"""
                Dear {client_details["name"]},

                Thank you for choosing Free2Move for your vehicle rental needs. Here are your rental details:

                Client Details:
                Name: {client_details["name"]}
                Phone Number: {client_details["phone_number"]}
                Email: {client_details["email"]}

                Vehicle Details:
                Type: {vehicle_type}
                License Plate Number: {license_plate}
                Model: {vehicle_details.get("model", "N/A")}
                Daily Rental Rate: {vehicle_details.get("daily_rental_rate", "N/A")}

                Pick-up Location: {pickup_location}
                Drop-off Location: {client_details.get("dropoff_location", "N/A")}
                Pick-up date: {client_details["pickup_date"]}
                Drop-off date: {client_details["dropoff_date"]}
                Rental Duration: {rental_days} day/s
                Payment Method: {client_details["payment_method"]}
                Final Amount: {final_amount} INR

                Thank you for your business! 

                Regards,
                Free2Move Team.
                """

                msg = MIMEText(message)
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = receiver_email

                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(sender_email, "npwo szcc idpy oxjo")
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                except Exception as e:
                    print(f"Failed to send the email. Error: {e}")
                    return False

                return True


            if send_email(client_details, vehicle_details, final_amount, rental_days):
                print("We have sent you an email with your details. Please check your inbox.")
            else:
                print("Failed to send the email. Please try again.")

            mycursor.execute("INSERT INTO Bookings(User_Name,ph_num,V_Type,V_Model,Amount,PickUp_Date,DropOff_Date,Payment_Method)VALUES('{}','{}','{}','{}',{},'{}','{}','{}')".format(client_details["name"], client_details["phone_number"],client_details.get("vehicle_types", "N/A"), vehicle_details.get("model", "N/A"),final_amount, client_details["pickup_date"], client_details["pickup_date"],client_details["payment_method"]))
            mydb.commit()

mydb.close()

