import datetime
import json

#Variables
password = ''
id = ''
key = ''
logoff = False
license = '02 082702'
cart = []
key = False
exit = False
checkout = ""

registrar = ["Bryan", "Josh", "Sandy", "Katherine"]
eScripts = {
    "Amanda Bayer": "Omeprazole - 40 MG",
    "Brandi Jones": "Loratadine - 5 MG",
    "Jennifer Dune": "Alprazolam - 1.5 MG",
    "Martin Cole": "Cyanocobalamin - 1 ct.",
    "Randy Roger": "Tamsulosin - 0.4 MG",
    "Wendy Williams": "Vitamin D3 - 50,000 IU"
}
CONTROLLED = ["Alprazolam - 10 MG Tablets", "Buprenorphine - 4MG/1MG", "Lorazepam 1 - MG Tablets", "Pregabalin - 75 MG Capsules", "Zolpidem - 5 MG Tablets"]

#Array containing wholesaler inventory
inventory = ["Atorvastatin 20 MG Tablets" , "Amoxicillin 500 MG Capsules", "Escitalopram 10 MG Tablets", "Guaifenesin 100 MG/5 ML ", "Hydrochlortiazide 12.5 MG Tablets", 
             "Icosapent 1 G Capsules" , "Kerendia 10 MG Tablets", "Lorazepam 1 MG Tablets", "Metoprolol 25 MG Tablets", "Nifedipine ER 90 MG Tablets", 
             "Omeprazole DR 40 MG Capsules", "Quetiapine 300 MG Tablets", "Risperidone 0.5 MG Tablets", "Sertraline 50 MG Tablets", "Tramadol 25 MG Tablets", 
             "Ubrevly 50 MG Tablets", "Vilazodone 10 MG Tablets", "Wegovy 2.4 MG/0.75 ML", "Xigduo 5MG/1000MG Tablets", "Yasmin 21ct.", "Zolpidem 5 MG Tablets"]

#Entry prompt
print("'Welcome to Winpharm. Please enter the password:")
password = input()
password.lower()

while not (password == 'pharmaceutical'):
    print('This is not the correct password. Please input the correct password:')
    passcode = input()
    passcode.lower()

#Registrar entry prompt
print("Access Granted. Please state your name for recorded entry with the first initial capitalized.")
print("Example: 'Samantha'")
id = input()

#More security measures
while (id not in registrar):
    print("We're sorry. The selected name is not a current member of our pharmacy. Please try again.")
    print("Example: 'Samantha'")
    id = input()

print("Access granted. Welcome " + id + ".")

while not (logoff == True):
    #Mainframe
    print()
    print("Please select an option:")
    print("1. View Electronic Scripts")
    print("2. Add an eScript")
    print("3. Add a pharmacy technician [Pharmacist Only]")
    print("4. Document a Controlled Substance [Pharmacist Only]")
    print("5. Place an order on Kinray")
    print("6. Logout")

    key = input()

    #Will print the dictionary
    if (key == '1'):
            print("--eScripts--")
            print()
            print(json.dumps(eScripts, indent = 4))

    #Will add an item and print the dictionary 
    elif (key == '2'):
            patient = ''
            prescription = ''

            print("Enter the patient name:")
            patient = input()

            print("Enter the patient's prescription in the following format: Medication - Dosage")
            print("Example: Calcium Tablets - 667 MG")
            prescription = input()

            eScripts[patient] = prescription

            print("--eScripts--")
            print()
            print(json.dumps(eScripts, indent = 4))

    #Adding an option to the tuple featuring a security measure with grave consequences for intruders
    elif (key == '3'):
            print("You are attempting to add a technician to the database. This is a pharmacist only option.")
            print('Please enter your licensing number using this format (00 123456):')
            license = input()

            i = 3

            while not (license == "02 082702"):

                i = i-1

                #Anti social engineering measure
                if (i == 0):
                    print("YOU HAVE EXCEEDED THE MAXIMUM NUMBER OF ATTEMPTS! NATIONAL AUTHORITIES WILL BE TRACKING THE IP ADDRESS!")
                    print("&$#&*(@&(#$(@&#@!&($*&)(!@&$(*&(#&(@&($&@#&$(@&#$(&@)($#@(*^*&&#*^*^*^*&^$&*#*#$)")
                    break
                
                attempts = str(i)
                print("You have not input a license number. You have " + attempts + " more attempts:")
                license = input()
                int(i)

            confirm = ''

            #Prompt for non-intruders that will add to the tuple
            while not (confirm == 'y' or confirm == 'Y' or confirm == 'yes' or confirm == 'YES'):
                print('Welcome Bryan. Please enter the name of the registering pharmacy technician. Enter "0" to go back.')
                technician = input()

                if (technician == '0'):
                    break

                print('You are submitting the name -' + technician + '-. Is this correct? Enter "Y" or "yes" to confirm.')
                confirm = input()
                confirm.lower()

                registrar.append(technician)

                print()
                print('Successfully added ' + technician + ' to the registrar.')

                print('Pharmacy registrar:')
                print(registrar)

    #Will add to the list with security system 
    elif (key == '4'):
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

        #Prompt that will add item to list 
        while not (confirm == 'y' or confirm == 'Y' or confirm == 'yes' or confirm == 'YES'):
            print('Welcome Bryan. Please enter the name of the controlled medication. Enter "0" to go back.')
            C2 = input()

            if (C2 == '0'):
                break

            print('You are submitting the controlled substance -' + C2 + '-. Is this correct? Enter "Y" or "yes" to confirm.')
            confirm = input()
            confirm.lower()

            CONTROLLED.append(C2)

            print()
            print('Successfully added ' + C2 + ' to the controlled substance records.')
            print()

            print('Controlled Medicine Records:')
            
            for x in range(len(CONTROLLED)):
                print (CONTROLLED[x])

    elif (key == '5'):
        #Introduction
        print('Welcome to Kinray Inc. Please select your product:')

        #Prints the inventory
        for i,item in enumerate(inventory, 1):
            print(i, item)

        #Fixes the index of choice for the user 
        option = int(input())
        option = option - 1

        #Forces the user to pick within the length of the inventory size
        while (option < 0 or option >= 22):
            print('You have inputted an invalid selection. Please select your product:')

            for i,item in enumerate(inventory, 1):
                print(i, item)
            option = int(input())

        #Adds item to shopping cart
        cart.append(inventory[option])

        print("Shopping Cart:")

        for (i,item) in enumerate(cart):
                print(i + 1, item)

        print()

        #Loop with commands for shopping cart, checking out, and quitting
        while not(key == True or exit == True):
            print('Please enter a command:')
            print('1. [spacebar] to add an item to your cart')
            print('2. "-" or "Delete Item" to delete an item from your cart')
            print('3. "Reset" or "Restart" to empty cart and start over')
            print('4. "Checkout" to purchase items')
            print('5. "Quit" to close Kinray Inc.')

            key = input()
            key.lower()

            #Alphabetizes the array
            cart.sort()

            #Add command
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
            
            #Subtract command
            elif (key == "-" or key == "delete item" or key == "2"):
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
                        for (i,item) in enumerate(cart):
                            print(i + 1, item)

                print()
            
            #Reset command
            elif (key == "reset" or key == "restart" or key == "3"):
                #Clears the cart
                cart.clear()
                print("You have selected the Reset option. Your cart has been emptied.")
                print()

            #Checkout command
            elif (key == "checkout" or key == '4'):
                print()
                print("Shopping Cart:")
                for (i,item) in enumerate(cart):
                        print(i + 1, item)
                
                print()
                print('Enter "Y" or "Yes" to confirm:')
                checkout = input()

                if (checkout == "Y" or checkout == "Yes"): 
                    #Exits the loop
                    break
                else:
                    continue

            #Quit option
            elif (key == "quit" or key == '5'):
                #Quit condition to avoid printing a checkout specific message
                key == True
                break
            else:
                print("You have not input any of the listed commands. Please try again.")

        print()

        if key == True:
            print("Thank you for choosing Kinray Inc. Until next time!")

        else:       
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
            invoice.write("Kinray Inc. © 2024")

            invoice.close()

    #Logout option
    elif (key == '6'):
        print("Thank you " + id + ". You are now logged out.")
        logoff = True

    #Prompt for out of bounds input
    while not(key == '1' or key == '2' or key == '3' or key == '4' or key == '5' or key == '6'):
        print("You have not selected a valid option.")
        print()
        print("Please select an option:")
        print("1. View Electronic Scripts")
        print("2. Add an eScript")
        print("3. Add a pharmacy technician [Pharmacist Only]")
        print("4. Document a Controlled Substance [Pharmacist Only]")
        print("5. Place an order on Kinray")
        print("6. Logout")

        key = input()

        #Will print the dictionary
        if (key == '1'):
                print("--eScripts--")
                print()
                print(json.dumps(eScripts, indent = 4))

        #Will add an item and print the dictionary 
        elif (key == '2'):
                patient = ''
                prescription = ''

                print("Enter the patient name:")
                patient = input()

                print("Enter the patient's prescription in the following format: Medication - Dosage")
                print("Example: Calcium Tablets - 667 MG")
                prescription = input()

                eScripts[patient] = prescription

                print("--eScripts--")
                print()
                print(json.dumps(eScripts, indent = 4))

        #Adding an option to the tuple featuring a security measure with grave consequences for intruders
        elif (key == '3'):
                print("You are attempting to add a technician to the database. This is a pharmacist only option.")
                print('Please enter your licensing number using this format (00 123456):')
                license = input()

                i = 3

                while not (license == "02 082702"):

                    i = i-1

                    #Anti social engineering measure
                    if (i == 0):
                        print("YOU HAVE EXCEEDED THE MAXIMUM NUMBER OF ATTEMPTS! NATIONAL AUTHORITIES WILL BE TRACKING THE IP ADDRESS!")
                        print("&$#&*(@&(#$(@&#@!&($*&)(!@&$(*&(#&(@&($&@#&$(@&#$(&@)($#@(*^*&&#*^*^*^*&^$&*#*#$)")
                        break
                    
                    attempts = str(i)
                    print("You have not input a license number. You have " + attempts + " more attempts:")
                    license = input()
                    int(i)

                confirm = ''

                #Prompt for non-intruders that will add to the tuple
                while not (confirm == 'y' or confirm == 'Y' or confirm == 'yes' or confirm == 'YES'):
                    print('Welcome Bryan. Please enter the name of the registering pharmacy technician. Enter "0" to go back.')
                    technician = input()

                    if (technician == '0'):
                        break

                    print('You are submitting the name -' + technician + '-. Is this correct? Enter "Y" or "yes" to confirm.')
                    confirm = input()
                    confirm.lower()

                    eScript_refreshed = registrar + (technician)

                    print()
                    print('Successfully added ' + technician + ' to the registrar.')

                    print('Pharmacy registrar:')
                    print(eScript_refreshed)

        #Will add to the list with security system 
        elif (key == '4'):
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

            #Prompt that will add item to list 
            while not (confirm == 'y' or confirm == 'Y' or confirm == 'yes' or confirm == 'YES'):
                print('Welcome Bryan. Please enter the name of the controlled medication. Enter "0" to go back.')
                C2 = input()

                if (C2 == '0'):
                    break

                print('You are submitting the controlled substance -' + C2 + '-. Is this correct? Enter "Y" or "yes" to confirm.')
                confirm = input()
                confirm.lower()

                CONTROLLED.append(C2)

                print()
                print('Successfully added ' + C2 + ' to the controlled substance records.')
                print()

                print('Controlled Medicine Records:')
                
                for x in range(len(CONTROLLED)):
                    print (CONTROLLED[x])

        elif (key == '5'):
            #Introduction
            print('Welcome to Kinray Inc. Please select your product:')

            #Prints the inventory
            for i,item in enumerate(inventory, 1):
                print(i, item)

            #Fixes the index of choice for the user 
            option = int(input())
            option = option - 1

            #Forces the user to pick within the length of the inventory size
            while (option < 0 or option >= 22):
                print('You have inputted an invalid selection. Please select your product:')

                for i,item in enumerate(inventory, 1):
                    print(i, item)
                option = int(input())

            #Adds item to shopping cart
            cart.append(inventory[option])

            print("Shopping Cart:")

            for (i,item) in enumerate(cart):
                    print(i + 1, item)

            print()

            #Loop with commands for shopping cart, checking out, and quitting
            while not(key == True or exit == True):
                print('Please enter a command:')
                print('1. [spacebar] to add an item to your cart')
                print('2. "-" or "Delete Item" to delete an item from your cart')
                print('3. "Reset" or "Restart" to empty cart and start over')
                print('4. "Checkout" to purchase items')
                print('5. "Quit" to close Kinray Inc.')

                key = input()
                key.lower()

                #Alphabetizes the array
                cart.sort()

                #Add command
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
                
                #Subtract command
                elif (key == "-" or key == "delete item" or key == "2"):
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
                            for (i,item) in enumerate(cart):
                                print(i + 1, item)

                    print()
                
                #Reset command
                elif (key == "reset" or key == "restart" or key == "3"):
                    #Clears the cart
                    cart.clear()
                    print("You have selected the Reset option. Your cart has been emptied.")
                    print()

                #Checkout command
                elif (key == "checkout" or key == '4'):
                    print()
                    print("Shopping Cart:")
                    for (i,item) in enumerate(cart):
                            print(i + 1, item)
                    
                    print()
                    print('Enter "Y" or "Yes" to confirm:')
                    checkout = input()

                    if (checkout == "Y" or checkout == "Yes"): 
                        #Exits the loop
                        break
                    else:
                        continue

                #Quit option
                elif (key == "quit" or key == '5'):
                    #Quit condition to avoid printing a checkout specific message
                    key == True
                    break
                else:
                    print("You have not input any of the listed commands. Please try again.")

            print()

            if key == True:
                print("Thank you for choosing Kinray Inc. Until next time!")

            else:       
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
                invoice.write("Kinray Inc. © 2024")

                invoice.close()

        #Logout option
        elif (key == '6'):
            print("Thank you " + id + ". You are now logged out.")
            logoff = True
