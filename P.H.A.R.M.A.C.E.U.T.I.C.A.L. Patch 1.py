import asyncio
import datetime
from datetime import datetime

#Work on pharmacist print tech's logging records
#Work on self.name syntax in print logging records method in technician class

#Will display the technician interface
def techMenu():
    print()
    print("Please select an option:")
    print("1. Search for a patient")
    print("2. Search for a medication")
    print("3. Place an order on Kinray")
    print("4. Translate sig codes")
    print("5. Logout")

#Will display the pharmacist interface
def docMenu():
    print()
    print("Please select an option:")
    print("1. Search for a patient")
    print("2. Search for a medication")
    print("3. Place an order on Kinray")
    print("4. Translate sig codes")
    print("5. Review Technician Login Records [Pharmacist Only]")
    print("6. Add a pharmacy technician [Pharmacist Only]")
    print("7. Document a Controlled Substance [Pharmacist Only]")
    print("8. Logout")

#Authenticates the login attempt by reviewing the file for the employee name.
def authenticate(id):
    with open(logging_records, "r") as file:
        lines = file.readlines()

    block = False

    for line in lines:
        if line.strip() == "---":
            block = True
            continue
        
        if block:
            if line.strip() == id:
                return True
            
            if line.strip() == "###":
                block = False

    return False

#Will create patient objects from the patients in the database text file
def load_patients(file):
    try:
        with open(file, 'r') as file:
            content = file.read()

        record = content.split('---\n')[1:]
        patients = []

        for record in record:
            if not record.strip().endswith('###'):
                continue

            record = record.strip()[:-3].strip()
            line = record.strip().split('\n')
            name = line[0]
            dob = line[1]

            med_starter = line.index('!!!') + 1
            med_ender = line.index('!!!', med_starter)
            medications = line[med_starter: med_ender]
            address = line[med_ender + 1]
            allergy = line[med_ender + 2]

            patient = Patient(name, dob, medications, address, allergy)
            patients.append(patient)

        return patients

    except FileNotFoundError:
        print(f"Error: File '{file}' couldn't be found.")
        return None
    
    except Exception as e:
        print(f"An error occurred while using the file: {e}")
        return None

#Will create technician and pharmacist objects for every employee in the database file
def load_team(filepath):
    team = []
    try:
        with open(filepath, "r") as file:
            section = file.readlines()
    except FileNotFoundError:
        print("Technician database could not be found.")
        return

    block = False
    session = None
    tech = None
    title = None

    for line in section:
        line_stripped = line.strip()

        if line_stripped == "---":
            block = True
            tech = None
            title = None

        elif block and tech is None:
            tech_name = line_stripped
            tech = {"name": tech_name, "sessions": []}

        elif block and line_stripped.startswith("Role:"):
            title = line_stripped.replace("Role:", "").strip()

        elif block and line_stripped == "Login Times":
            continue

        elif block and line_stripped.startswith("Login:"):
            login_time = line_stripped.replace("Login:", "").strip()
            if login_time:
                session = {"login": login_time, "logout": None}
                tech["sessions"].append(session)

        elif block and line_stripped.startswith("Logout:") and session:
            logout_time = line_stripped.replace("Logout:", "").strip()
            if logout_time:
                session["logout"] = logout_time

        elif block and line_stripped == "###":
            if title == "Pharmacist":
                employee = Pharmacist(tech["name"])

            else:
                employee = Technician(tech["name"])
            
            employee.sessions = tech["sessions"]
            team.append(employee)

            block = False
            tech = None
            session = None

    return team

#Will log employee logins and logouts to P.H.A.R.M.A.C.E.U.T.I.C.A.L.
def log_event(worker, event):
    team = load_team(logging_records)
    employee = next((employee for employee in team if employee.name.lower() == worker.lower()), None)

    if event == "login":
        if not employee.sessions or employee.sessions[-1]["logout"] is not None:
            employee.login()
        else:
            print(f"{employee.name} is already logged in")
    elif event == "logout":
        if employee.sessions and employee.sessions[-1]["logout"] is None:
            employee.logout()
        else:
            print("There is no active session to log out of.")
            return

    with open(logging_records, "w") as file:
        for employee in team:
            file.write("---\n")
            file.write(f"{employee.name}\n")
            file.write(f"Role: {'Pharmacist' if isinstance(employee, Pharmacist) else 'Technician'}\n")
            file.write(("Login Times\n"))

            for session in employee.sessions:
                file.write(f"Login: {session['login']}\n")
                
                if session['logout']:
                    file.write(f"Logout: {session['logout']}\n")

            file.write("###\n")

#Will search the patient registrar for patients based on either name or date of birth
def search_patient(search):
    with open(patient_records, "r") as file:
        section = file.read()

    patients = section.split("---\n")
    for sections in patients:
        if not sections.strip() or not sections.strip().endswith("###"):
            continue

        line = [line.strip() for line in sections.strip().split("\n")]  

        name = line[0]
        dob = line[1]
        meds_start = line.index("!!!") + 1
        meds_end = len(line) - 3
        medications = []

        for i in range(meds_start, len(line)):
            if line[i] == "!!!":
                meds_end = i
                break
            medications.append(line[i])

        address = line[meds_end + 1]
        allergies = line[meds_end + 2].replace("Allergy:", "").strip()

        if search.lower() == name.lower() or search == dob:
            return Patient(name, dob, medications, address, allergies)
        
    print(f"{search} could not be found.")
    return None

#Will lookup details about a medication  
def med_search(file):
    print()
    print("What medication would you like to look up?")
    
    med = input()
    
    if not med:
        print("No input was found. Please try again.")
        return 

    else:
        while True:
            try:
                with open(file, 'r') as file:
                    content = file.read()

                    # Split the file into sections using '---'
                    blocks = content.split('---\n')
                    
                    for block in blocks:
                        if not block.strip():
                            continue 

                        # End marker is '###'
                        if not block.strip().endswith('###'):
                            continue  

                        line = block.strip().split('\n')
                        if len(line) < 3:
                            continue 

                        med_name = line[0].strip() 

                        if med.lower() == med_name.lower():
                            print(f"Name: {med_name}\nUse: {' '.join(line[1:-1])}")
                            return

                    print(f"The medication '{med}' wasn't found.")
                    return

            except FileNotFoundError:
                print(f"Error: File '{file}' couldn't be found.")
                return None
            
            except Exception as e:
                print(f"An error occurred while using the file: {e}")
                return None

#Technician class implemented for basic pharmacy responsibilities (Role-Based Access Control)
class Technician:
    def __init__(self, name):
        self.name = name
        self.sessions = []

    #Logs a login
    def login(self):
        time = datetime.now().strftime("%B %d, %Y %I:%M %p")
        self.sessions.append({"login": time, "logout": None})

    #Logs a logoff
    def logout(self):
        time = datetime.now().strftime("%B %d, %Y %I:%M %p")
        if self.sessions and self.sessions[-1]["logout"] is None:
            self.sessions[-1]["logout"] = time

#Pharmacist class inherits the basic technician permissions while also expanding upon them to perform pharmacist-only duties (Role-Based Access Control)              
class Pharmacist(Technician):
    def __init__(self, name):
        super().__init__(name)
        self.MD = True

    #Adds an employee to the team database
    def add_employee():
        print()
        print("Enter the name of the technician you want to add to the registrar")
        name = input()

        print(f"Is {name} a technician or a pharmacist?")
        role = input()

        if not(role.lower() == "technician" or role == "pharmacist"):
            print("You did not select either option. Registration has failed.")
            return

        try:
            with open(logging_records, "r") as file:
                section = file.readlines()
        except FileNotFoundError:
            print("The technician registrar could not be found.")
            return

        block = False

        for line in section:
            if line.strip() == "---":
                block = True
                continue
            
            if block:
                if line.strip().lower() == name.lower():
                    print(f"'{name}' is already registered.")
                    return
                
                if line.strip() == "###":
                    block = False

        with open(logging_records, "a") as file:
            file.write("---\n")
            file.write(f"{name}\n")

            if role.lower() == "pharmacist":
                file.write("Role: Pharmacist")
            else:
                file.write("Role: Technician")
            file.write("Login Times:\n")
            file.write("###\n")

        print(f"{name} has been added to the registrar.")

    #Prints the logs for a specific technician
    def printLogins():
        print()
        team = load_team(logging_records)

        if not team:
            print("No employees could be found")

        print("Pharmacy employees:")

        for index, employee in enumerate(team, 1):
            role = "Pharmacist" if isinstance(employee, Pharmacist) else "Technician"
            print(f"{index}. {employee.name} ({role})")
       
        print("Which employee are you trying to access login times for?")
        select = int(input())
        if select < 1 or select > len(team):
            print("You did not properly select a technician. Printing of loggings has failed.")
            return
        
        employee = team[select - 1]

        if not employee.sessions:
            print(f"{employee.name} doesn't have any logging records.")

        else:
            print(f"\nThese are the logs of events for the technician {employee.name}")
            print("-" * 20)

            for i,session in enumerate(employee.sessions, 1):
                print(f"Session {i}:")
                print(f"Login: {session['login']}")
                print(f"Logout: {session['logout'] if session['logout'] else 'Still logged in'}")
                print()

#Patient class for pharmacy patients
class Patient:
    def __init__(self, name, dob, medications, address, allergy):
        self.name = name
        self.dob = dob
        self.medications = medications
        self.address = address
        self.allergy = allergy

    #Will print patient information [Patient Personal Information]
    def printPPI(self):
        print()
        meds = "\n".join(self.medications)
        print (f"Name: {self.name}\n"
                f"Date of Birth: {self.dob}\n"
                f"Medications: {meds}\n"
                f"Address: {self.address}\n"
                f"Allergy: {self.allergy}\n")
        print()

    #Adds a medication to the patient's medication list
    def add_Medication(self):
        while not (choice.lower() == "no"):
            print("What medication would you like to add? Please use the format: Drug - Dosage")
            input = input()
            self.medications.append(input)
            self.medications.sort()
            print(input + " has been added to " + self.name + "'s medication list.")
            print("Would you like to add another medication?")

            choice = input()

            while not (choice.lower() == "yes" or choice.lower() == "no"):
                print("You did not respond properly. Please respond with 'yes' or 'no' to proceed.")
                print("Would you like to add another medication?")

                choice = input()

            if choice.lower() == "yes":
                continue
    
    def scanPrescription(self):
        print("Please insert your physical prescription. Input DONE when the prescription is inserted.")
        confirm = input()

        asyncio.run(scan())

        while not (confirm.upper() == "DONE"):
            print("Scan has failed. Please try again. Press any key to continue.")
            confirm = input()

            print("Please scan your physical prescription. Input DONE when the prescription is scanned.")
            confirm = input()

            asyncio.run(scan())
        
        print("Prescription has been successfully scanned.")
        print("What is the medication? Please use the format: Drug - Dosage")
        confirm = input()

#Simulates the scanning of a prescription
async def scan():
    print("Scanning", end = " ")
    await asyncio.sleep(0.5)
    print(".", end = "")
    await asyncio.sleep(0.5)
    print(" .", end = "")
    await asyncio.sleep(0.5)
    print(" .")
    await asyncio.sleep(0.5)

#Variables
id = ''
key = ''
logoff = False
license = '02 082702'
cart = []
exit = False
MD = False
patient_records = "patients.txt"
logging_records = "logs.txt"
formulary = "pharmaceuticals.txt"
active_tech = None
sig_codes = {
    " T " : " TABLET(S) ",
    " C " : " CAPSULE(S) ",
    " AC " : " BEFORE MEALS ",
    " PC " : " AFTER MEALS ",
    "APP " : "APPLY ",
    "UTD" : "AS DIRECTED",
    " STAT " : " AT ONCE ",
    "TK" : "TAKE",
    " Q " : " EVERY ",
    " H " : " HOUR ",
    " D " : " DAY ",
    " N " : " NIGHT ",
    "QD" : "EVERY DAY",
    "BID" : "TWICE A DAY",
    "TID" : "THREE TIMES A DAY",
    "QID" : "FOUR TIMES A DAY",
    "QAM" : "EVERY MORNING",
    "QPM" : "EVERY EVENING",
    "QHS" : "EVERY NIGHT AT BEDTIME",
    "PRN" : "AS NEEDED",
    "WF" : "WITH FOOD",
    " PO " : " ORALLY ",
    " AA " : " TO THE AFFECTED AREA ",
    " AU " : " IN EACH EAR ",
    " AL " : " IN THE LEFT EAR ",
    " AD " : " IN THE RIGHT EAR ",
    " OU " : " IN EACH EYE ",
    " OS " : " IN THE LEFT EYE ",
    " OD " : " IN THE RIGHT EYE ",
    " IEN " : " IN EACH NOSTRIL ",
    " INJ " : " INJECT",
    "INH" : "INHALE",
    " SC " : " SUBCUTANEOUSLY ",
    " R " : " RECTALLY ",
    " V " : " VAGINALLY "
}
CONTROLLED = ["Alprazolam - 10 MG Tablets", "Buprenorphine - 4MG/1MG", "Lorazepam 1 - MG Tablets", "Pregabalin - 75 MG Capsules", "Zolpidem - 5 MG Tablets"]

#Array containing wholesaler inventory
inventory = ["Atorvastatin 20 MG Tablets" , "Amoxicillin 500 MG Capsules", "Escitalopram 10 MG Tablets", "Guaifenesin 100 MG/5 ML ", "Hydrochlortiazide 12.5 MG Tablets", 
             "Icosapent 1 G Capsules" , "Kerendia 10 MG Tablets", "Lorazepam 1 MG Tablets", "Metoprolol 25 MG Tablets", "Nifedipine ER 90 MG Tablets", 
             "Omeprazole DR 40 MG Capsules", "Quetiapine 300 MG Tablets", "Risperidone 0.5 MG Tablets", "Sertraline 50 MG Tablets", "Tramadol 25 MG Tablets", 
             "Ubrevly 50 MG Tablets", "Vilazodone 10 MG Tablets", "Wegovy 2.4 MG/0.75 ML", "Xigduo 5MG/1000MG Tablets", "Yasmin 21ct.", "Zolpidem 5 MG Tablets"]

patients = load_patients(patient_records)
employees = load_team(logging_records)

#Security Prompt
print("'Welcome to Winpharm. Please enter the password:")
passcode = input()


while not (passcode == 'pharmaceutical'):
    print('This is not the correct password. Please input the correct password:')
    passcode = input()
    passcode.lower()

print("Please state your name for recorded entry with the first initial capitalized for entry.")
print("Example: 'Samantha'")
id = input()

if authenticate(id) == True:
    log_event(id, "login")
    print(f"{id} has been successfully logged in.")

else:
    print("Technician could not be found. The program will now close.")

user = next((worker for worker in employees if worker.name.lower() == id.lower()), None)
 
#P.H.A.R.M.A.C.E.U.T.I.C.A.L. Entry
while (6 < 7):
    is_pharm = isinstance(user, Pharmacist)

    if not is_pharm:
        #Technician Login
        techMenu()

        key = input()

        #Searches for a patient based off name or date of birth
        if (key == '1'):
            print("What patient would you like to look up?")
            search = input()
            pt = search_patient(search)

            if not pt:
                break

            print(f"What would you like to do for {pt.name}?")
            print("Patient Menu:")
            print("1. Retrieve personal information")
            print("2. Type a physical prescription")

            choice = input()

            if not (choice.lower() == "retrieve personal information" or choice == '1' or choice.lower() == "type a medication" or choice == '2'):
                print("You did not select a valid option. Closing patient tab.")
                print()

            elif (choice.lower() == "retrieve personal information" or choice == '1'):
                pt.printPPI()

            elif (choice.lower() == "type a medication" or choice == '2'):
                pt.scanPrescription()

        #Searches for a medication to describe what it's taken for
        elif (key == '2'):
                meds = med_search(formulary)

        #Opens the Kinray Interface
        elif (key == '3'):
            while not(exit == True):
                print()
                print("Welcome to Kinray " + id + ".")
                print('Please enter a command:')
                print('1. [spacebar] to add an item to your cart')
                print('2. "-" or "Delete Item" to delete an item from your cart')
                print('3. "Reset" or "Restart" to empty cart and start over')
                print('4. "Checkout" to purchase items')
                print('5. "Quit" to close Kinray Inc.')

                key = input()

                #Adds item to the cart
                if (key == " " or key == "1"):
                    print('Please select your product:')

                    for i,item in enumerate(inventory, 1):
                        print(i, item)

                    option = int(input())
                    option = option - 1

                    while (option < 0 or option >= 22):
                        print('You have inputted an invalid selection. Please select your product:')

                        for i,item in enumerate(inventory, 1):
                            print(i, item)
                            option = int(input())

                    cart.append(inventory[option])
                    cart.sort()

                    print("Shopping Cart:")

                    for (i,item) in enumerate(cart):
                        print(i + 1, item)

                    print()
                
                #Subtracts an item from the shopping cart
                elif (key == "-" or key == "delete item" or key == "2"):

                    #Will print if shopping cart is empty
                    if not (cart):
                        print("Your shopping cart is empty. There is nothing to subtract.")

                    else:
                        print("Please select an item to delete:")
                        print()
                        print("Shopping Cart:")

                        for (i,item) in enumerate(cart):
                            print(i + 1, item)

                        item = int(input())
                        item = item - 1
                        cartsize = len(cart)


                        while (item > cartsize):
                            print("Your input is invalid. Please select an item to delete:")
                            for (i,item) in enumerate(cart):
                                print(i + 1, item)

                        #Subtracts the item from the input that the user desires
                        cart.pop(item)

                        if not (cart):
                            print("Your shopping cart is empty.")

                        else:
                            print("Shopping Cart:")
                            for (i,item) in enumerate(cart):
                                print(i + 1, item)

                    print()
                
                #Reset option
                elif (key == "reset" or key == "restart" or key == "3"):
                    #Clears the cart
                    cart.clear()
                    print("You have selected the Reset option. Your cart has been emptied.")
                    print()

                #Checkout option
                elif (key == "checkout" or key == '4'):
                    print()
                    print("Shopping Cart:")
                    for (i,item) in enumerate(cart):
                            print(i + 1, item)
                    
                    print()
                    print('Enter "Y" or "Yes" to confirm:')
                    input = input()

                    #Will document the invoice on the host computer
                    if (input.upper() == "Y" or input.upper() == "YES"):
                        print('Thank you for choosing Kinray. Your invoice is listed below:')
                        print()
                        instance = datetime.datetime.now()

                        for (i,item) in enumerate(cart):
                            print(i + 1, item)

                        invoice = open("Kinray Invoice " + instance.strftime("%B") + " " + instance.strftime("%d") + "," + instance.strftime("%Y"), "w")
                        invoice.write("---Kinray Invoice---" + "\n")
                        invoice.write("\n")
                        invoice.write("Date: " + instance.strftime("%B") + " " + instance.strftime("%d") + "," + instance.strftime("%Y") + "\n")
                        invoice.write("Time of purchase: " + instance.strftime("%I") + ":" + instance.strftime("%M") + " " + instance.strftime("%p") + "\n")
                        invoice.write("\n")

                        for (i,item) in enumerate(cart):
                            invoice.write(item + "\n")
                        
                        invoice.write("\n")
                        invoice.write("---Items Purchased---\n")
                        invoice.write("This Kinray Order was placed by: " + id + "\n")
                        invoice.write("Kinray Inc. © 2025")

                        invoice.close()

                        #Exits the interface
                        break

                    else:
                        continue

                #Quit option
                elif (key == "quit" or key == '5'):
                    #Exits Kinray and returns to the pharmacy interface
                    key == True
                    break

                else:
                    print("You did not select a proper option. Please try again.")
                    
        
        #Translate sig codes option
        elif (key == '4'):
            print("This is the sig code translator. It will take in any text with sig codes and translate it, removing any abbreviations into regular text.")
            print("Would you like to use this program more than once? Y / N")
            
            text = input()
            
            if (text.upper() == "Y" or text.upper() == "YES"):
                print("The sig code translator will continue to run. To end the program, input the word QUIT")

                while not(text == "QUIT"):
                    print()
                    print("Please submit your text that you need translated:")
                    text = input()

                    for word, words in sig_codes.items():
                        text = text.replace(word, words)

                    if (text == "QUIT"):
                        print()

                    else:
                        print("Here are the revised directions:")
                        print(text)
            else:
                print()
                print("Please submit your text that you need translated:")
                text = input()

                for word, words in sig_codes.items():
                    text = text.replace(word, words)

                print()
                print("Here are the revised directions:")
                print(text)

        #Logout option
        elif (key == '5'):
            log_event(id, 'logout')
            print(f"{id} has been successfully logged out.")
            break

        else:
            print("You did not select a proper option. Please try again.")
            print()

    #Pharmacist Login
    else:
        docMenu()

        key = input()

        #Searches for a patient based off name or date of birth
        if (key == '1'):
            print("What patient would you like to look up?")
            search = input()
            pt = search_patient(search)

            print(f"What would you like to do for {pt.name}?")
            print("Patient Menu:")
            print("1. Retrieve personal information")
            print("2. Type a physical prescription")

            choice = input()

            if not (choice.lower() == "retrieve personal information" or choice == '1' or choice.lower() == "type a medication" or choice == '2'):
                print("You did not select a valid option. Closing patient tab.")
                print()

            elif (choice.lower() == "retrieve personal information" or choice == '1'):
                pt.printPPI()

            elif (choice.lower() == "type a medication" or choice == '2'):
                pt.scanPrescription()

        #Searches for a medication to describe what it's taken for
        elif (key == '2'):
                meds = med_search(formulary)

        #Opens the Kinray Interface
        elif (key == '3'):
            while not(exit == True):
                print()
                print("Welcome to Kinray " + id + ".")
                print('Please enter a command:')
                print('1. [spacebar] to add an item to your cart')
                print('2. "-" or "Delete Item" to delete an item from your cart')
                print('3. "Reset" or "Restart" to empty cart and start over')
                print('4. "Checkout" to purchase items')
                print('5. "Quit" to close Kinray Inc.')

                key = input()

                #Adds item to the cart
                if (key == " " or key == "1"):
                    print('Please select your product:')

                    for i,item in enumerate(inventory, 1):
                        print(i, item)

                    option = int(input())
                    option = option - 1

                    while (option < 0 or option >= 22):
                        print('You have inputted an invalid selection. Please select your product:')

                        for i,item in enumerate(inventory, 1):
                            print(i, item)
                            option = int(input())

                    cart.append(inventory[option])
                    cart.sort()

                    print("Shopping Cart:")

                    for (i,item) in enumerate(cart):
                        print(i + 1, item)

                    print()
                
                #Subtracts an item from the shopping cart
                elif (key == "-" or key == "delete item" or key == "2"):

                    #Will print if shopping cart is empty
                    if not (cart):
                        print("Your shopping cart is empty. There is nothing to subtract.")

                    else:
                        print("Please select an item to delete:")
                        print()
                        print("Shopping Cart:")

                        for (i,item) in enumerate(cart):
                            print(i + 1, item)

                        item = int(input())
                        item = item - 1
                        cartsize = len(cart)


                        while (item > cartsize):
                            print("Your input is invalid. Please select an item to delete:")
                            for (i,item) in enumerate(cart):
                                print(i + 1, item)

                        #Subtracts the item from the input that the user desires
                        cart.pop(item)

                        if not (cart):
                            print("Your shopping cart is empty.")

                        else:
                            print("Shopping Cart:")
                            for (i,item) in enumerate(cart):
                                print(i + 1, item)

                    print()
                
                #Reset option
                elif (key == "reset" or key == "restart" or key == "3"):
                    #Clears the cart
                    cart.clear()
                    print("You have selected the Reset option. Your cart has been emptied.")
                    print()

                #Checkout option
                elif (key == "checkout" or key == '4'):
                    print()
                    print("Shopping Cart:")
                    for (i,item) in enumerate(cart):
                            print(i + 1, item)
                    
                    print()
                    print('Enter "Y" or "Yes" to confirm:')
                    input = input()

                    #Will document the invoice on the host computer
                    if (input.upper() == "Y" or input.upper() == "YES"):
                        print('Thank you for choosing Kinray. Your invoice is listed below:')
                        print()
                        instance = datetime.datetime.now()

                        for (i,item) in enumerate(cart):
                            print(i + 1, item)

                        invoice = open("Kinray Invoice " + instance.strftime("%B") + " " + instance.strftime("%d") + "," + instance.strftime("%Y"), "w")
                        invoice.write("---Kinray Invoice---" + "\n")
                        invoice.write("\n")
                        invoice.write("Date: " + instance.strftime("%B") + " " + instance.strftime("%d") + "," + instance.strftime("%Y") + "\n")
                        invoice.write("Time of purchase: " + instance.strftime("%I") + ":" + instance.strftime("%M") + " " + instance.strftime("%p") + "\n")
                        invoice.write("\n")

                        for (i,item) in enumerate(cart):
                            invoice.write(item + "\n")
                        
                        invoice.write("\n")
                        invoice.write("---Items Purchased---\n")
                        invoice.write("This Kinray Order was placed by: " + id + "\n")
                        invoice.write("Kinray Inc. © 2025")

                        invoice.close()

                        #Exits the interface
                        break

                    else:
                        continue

                #Quit option
                elif (key == "quit" or key == '5'):
                    #Exits Kinray and returns to the pharmacy interface
                    key == True
                    break

                else:
                    print("You did not select a proper option. Please try again.")
                    
        
        #Translate sig codes option
        elif (key == '4'):
            print("This is the sig code translator. It will take in any text with sig codes and translate it, removing any abbreviations into regular text.")
            print("Would you like to use this program more than once? Y / N")
            
            text = input()
            
            if (text.upper() == "Y" or text.upper() == "YES"):
                print("The sig code translator will continue to run. To end the program, input the word QUIT")

                while not(text == "QUIT"):
                    print()
                    print("Please submit your text that you need translated:")
                    text = input()

                    for word, words in sig_codes.items():
                        text = text.replace(word, words)

                    if (text == "QUIT"):
                        print()

                    else:
                        print("Here are the revised directions:")
                        print(text)
            else:
                print()
                print("Please submit your text that you need translated:")
                text = input()

                for word, words in sig_codes.items():
                    text = text.replace(word, words)

                print()
                print("Here are the revised directions:")
                print(text)

        #Review technician login times option
        elif (key == '5'):
            Pharmacist.printLogins()

        #Adds a technician to the database with security measures
        elif (key == '6'):
            Pharmacist.add_employee()

        #Documents a controlled substance
        elif (key == '7'):
            if (MD == True):
                print("You are attempting to document a controlled substance. This is a pharmacist only option.")
                print('Please enter your licensing number using this format (00 123456):')
                license = input()

                i = 3

                while not (license == "02 082702"):

                    i = i-1

                    if (i == 0):
                        print("YOU HAVE EXCEEDED THE MAXIMUM NUMBER OF ATTEMPTS! NATIONAL AUTHORITIES WILL BE TRACKING THE IP ADDRESS!")
                        print("&$#&*(@&(#$(@&#@!&($*&)(!@&$(*&(#&(@&($&@#&$(@&#$(&@)($#@(*^*&&#*^*^*^*&^$&*#*#$)")
                        break
                        
                    attempts = str(i)
                    print("You have not input a license number. You have " + attempts + " more attempts:")
                    license = input()
                    int(i)

                confirm = ''

                #Adds an item to the list of available controlled medications
                while not (confirm == 'y' or confirm == 'Y' or confirm == 'yes' or confirm == 'YES'):
                    print('Welcome Bryan. Please enter the name of the controlled medication and the dosage. Enter "0" to go back.')
                    C2 = input()

                    if (C2 == '0'):
                        break

                    print('You are submitting the controlled substance -' + C2 + '-. Is this correct? Enter "Y" or "yes" to confirm.')
                    confirm = input()
                    confirm.lower()

                    CONTROLLED.append(C2)
                    CONTROLLED.sort()

                    print()
                    print('Successfully added ' + C2 + ' to the controlled substance records.')
                    print()

                    print('Controlled Medicine Records:')
                    
                    for x in range(len(CONTROLLED)):
                        print (CONTROLLED[x])

        #Logout option
        elif (key == '8'):
            log_event(id, 'logout')
            print(f"{id} has been successfully logged out.")
            break

        else:
            print("You did not select a proper option. Please try again.")
            print()