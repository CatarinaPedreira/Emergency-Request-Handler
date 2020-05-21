def check_if_comma(string):
    while "," not in string:
        string = input("Invalid input. Please insert the values separated by a comma: ")
    return string.split(",")


def sanitize_location(area, num, val):
    s = "Invalid input. Please insert positive " + str(val) + " value smaller or equal than " + str(num) + ": "
    num += 1
    while not area.isdigit() or not -1 < int(area) < num:
        area = input(s)
    return int(area)


def sanitize_type(string):
    if string == "1":
        value = "Life-threatening"
    elif string == "2":
        value = "Non life-threatening"
    else:
        string = input("Invalid input. Please insert 1 or 2: ")
        value = sanitize_type(string)
    return value


def sanitize_integer_input(arg):
    while not arg.isnumeric() or arg == "0" or arg == "":
        arg = input("Invalid input. Please insert a positive integer value: ")
    return int(arg)


def sanitize_gravity(arg):
    arg = sanitize_integer_input(arg)
    if not 1 <= arg <= 10:
        arg = input("Invalid input. Please insert an integer between 1 and 10: ")
        arg = sanitize_gravity(arg)
    return arg


def sanitize_vehicle_type(string):
    if len(string) > 5:
        string = check_if_comma(string)
    else:
        string = [string]
    for s in string:
        if s != "SBV" and s != "VMER" and s != "SIV":
            string = input("Invalid input. Please insert one or more of these types SBV,VMER,SIV: ")
            string = sanitize_vehicle_type(string)
            break
    return string


def setup(width, height):
    location = []
    print("-------------------Insert new Medical Emergency-------------------")
    location_x = input("Location width: ")
    location.append(sanitize_location(location_x, width, "width"))
    location_y = input("Location height: ")
    location.append(sanitize_location(location_y, height, "height"))
    location = tuple(location)
    emergency_type = input("Type of emergency insert 1 or 2 (1-Life-threatening or 2-Non life-threatening): ")
    emergency_type = sanitize_type(emergency_type)
    n_patients = input("Number of patients: ")
    n_patients = sanitize_integer_input(n_patients)
    gravity = input("Gravity (from 1 to 10): ")
    gravity = sanitize_gravity(gravity)
    vehicle_type = input("Insert one or more of these types SBV,VMER,SIV: ")
    vehicle_type = sanitize_vehicle_type(vehicle_type)
    s = "Type: " + str(emergency_type) + "\nLocation: " + str(location) + "\nPatients: " + str(n_patients) + "\nGravity: " + str(gravity) + "\nType of vehicles: " + str(vehicle_type)
    f = open("temp.txt", "w")
    f.write(s)
    f.close()

