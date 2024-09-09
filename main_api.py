import datetime
import geocoder
import qrcode
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("server_private_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def validate_user_faculty(username, password):
    try:
        # Query Firestore to check if the username exists and the password matches
        user_ref = db.collection("user_faculty").where("username", "==", username).limit(1)
        user_docs = user_ref.stream()
        
        for doc in user_docs:
            user_data = doc.to_dict()
            if user_data["password"] == password:
                return True
    except Exception as e:
        print("An error occurred:", e)
        print("Contact Admin Section")
    
    return False

def validate_user_admin(username, password):
    try:
        # Query Firestore to check if the username exists and the password matches
        user_ref = db.collection("user_admin").where("username", "==", username).limit(1)
        user_docs = user_ref.stream()
        
        for doc in user_docs:
            user_data = doc.to_dict()
            if user_data["password"] == password:
                return True
    except Exception as e:
        print("An error occurred:", e)
        print("Contact Admin Section")
    
    return False

def change_password_faculty():
    username = input("Enter your username: ")
    try:
        # Query Firestore to get the user document
        user_ref = db.collection("user_faculty").where("username", "==", username).limit(1)
        user_docs = user_ref.stream()
        
        user_found = False  # Flag to track if the user is found
        
        for doc in user_docs:
            user_data = doc.to_dict()
            user_found = True
            old_password = input("Enter your old password: ")
            # Check if the old password matches the one stored in the database
            if user_data["password"] == old_password:
                new_password = input("Enter your new password: ")
                confirm_password = input("Confirm your new password: ")
                # Check if the new password and confirm password match
                if new_password == confirm_password:
                    # Update the password in the database
                    db.collection("user_faculty").document(doc.id).update({"password": new_password})
                    print("Password changed successfully.")
                    return True
                else:
                    print("New password and confirm password do not match.")
                    return False
            else:
                print("Incorrect old password.")
                return False
        
        # If the loop ends without returning, it means the username was found but the old password was incorrect
        if user_found:
            print("Incorrect old password.")
        else:
            print("Username not found.")
        
        return False
    
    except Exception as e:
        print("An error occurred:", e)
        print("Contact Admin Section")
        return False

def get_date_time():
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H-%M-%S")
    return current_date, current_time

def get_location():
    g = geocoder.ip('me')
    return g.latlng 

def generate_and_save_qr_code(course_code, date, time, location, user_name):
    # Combine information into a single string
    qr_data = f"course_code:{course_code},date:{date},time:{time},Location:{location[0]}&{location[1]},user_name:{user_name}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    filename = f"qr_code.png"

    qr_image.save(filename, overwrite=True)
    print(f"QR code saved as {filename}")

    # Convert username to lowercase for case-insensitivity
    user_name_lower = user_name.lower()

    user_collection = db.collection(user_name_lower)
    user_collection_document = user_collection.document("classes")
    # Check if the classes document exists
    if not user_collection_document.get().exists:
        # Create the classes document
        user_collection_document.set({})
    class_document = user_collection_document.collection(course_code).document(date)  
    # Check if the class document for today exists
    if not class_document.get().exists:
        # Create the class document for today
        class_document.set({})
    attendance_collection = class_document.collection("attendance")   
    # Check if the teacher document already exists
    teacher_doc = attendance_collection.document("teacher")
    if not teacher_doc.get().exists:
        # Create the teacher document with the information
        doc_data = {
            "user_name": user_name,
            "course_code": course_code,
            "date": date,
            "time": time,
            "location": {
                "latitude": location[0],
                "longitude": location[1]
            }
        }
        teacher_doc.set(doc_data)
    print(f"Data written to Firestore for user {user_name} for class {course_code} on {date}.")

def display_courses(user_name):
    course=[]
    # Convert username to lowercase for case-insensitivity
    user_name_lower = user_name.lower()
    user_collection = db.collection(user_name_lower)
    user_classes_document = user_collection.document("classes")

    # Check if the user's classes document exists
    classes_snapshot = user_classes_document.get()
    if not classes_snapshot.exists:
        print("No classes found for this user.")
        return

    class_ids = list(user_classes_document.collections())  # Convert generator to list

    # Display class names
    for index, class_ref in enumerate(class_ids):
        #print(f"{index + 1}. {class_ref.id}")
        course.append(class_ref.id)
    return course

    #class_choice = input("Enter the name of the class: ").strip()  # Remove leading/trailing whitespace

    print("Input class choice:", repr(class_choice))  # Debug print

    # Check if the input class name matches any of the available class names (case-insensitive)
def display_dates(class_choice, user_name):
    user_name_lower = user_name.lower()
    user_collection = db.collection(user_name_lower)
    user_classes_document = user_collection.document("classes")
    class_ids = list(user_classes_document.collections())  # Convert generator to list

    dates = []
    selected_class_ref = None
    for class_ref in class_ids:
        print("Comparing:", (class_ref.id).lower(), class_choice.lower())  # Debug print
        if (class_ref.id).lower() == class_choice.lower():
            selected_class_ref = class_ref
            break

    if selected_class_ref is None:
        print("Invalid class name.")
        return

    print("Selected class:", selected_class_ref.id)  # Debug print'''

    #Display available dates
    print("Available dates:")
    date_ids = [doc.id for doc in selected_class_ref.stream()]
    for index, date_id in enumerate(date_ids):
        print(f"{index + 1}. {date_id}")
        dates.append(date_id)
    print(dates)
    return dates

def display_attendance(class_choice, date_choice, user_name ):
    table_data = []
    user_name_lower = user_name.lower()
    user_collection = db.collection(user_name_lower)
    user_classes_document = user_collection.document("classes")
    class_ids = list(user_classes_document.collections()) 
    for class_ref in class_ids:
        if (class_ref.id).lower() == class_choice.lower():
            selected_class_ref = class_ref
            break
    attendance_collection = selected_class_ref.document(date_choice).collection("attendance")
    for doc in attendance_collection.stream():
        data = doc.to_dict()
        table_data.append([data['user_name'], data['date'], data['time']])
    print(table_data)
    return table_data

def add_manual_attendance(user_name):
    # Convert username to lowercase for case-insensitivity
    user_name_lower = user_name.lower()
    # Get the current date and time
    current_date, current_time = get_date_time()
    # Access the user's collection
    user_collection = db.collection(user_name_lower)
    user_classes_document = user_collection.document("classes")
    # Check if the user's classes document exists
    classes_snapshot = user_classes_document.get()
    if not classes_snapshot.exists:
        print("No classes found for this user.")
        return
    # Prompt for class choice
    print("Select a class:")
    class_ids = list(user_classes_document.collections())  # Convert generator to list
    # Display class names
    for index, class_ref in enumerate(class_ids):
        print(f"{index + 1}. {class_ref.id}")
    class_choice = input("Enter the name of the class: ").strip()  # Remove leading/trailing whitespace
    # Check if the input class name matches any of the available class names (case-insensitive)
    selected_class_ref = None
    for class_ref in class_ids:
        if class_ref.id.lower() == class_choice.lower():
            selected_class_ref = class_ref
            break
    if selected_class_ref is None:
        print("Invalid class name.")
        return

    today_date = current_date
    attendance_collection = selected_class_ref.document(today_date).collection("attendance")
    student_name = input("Enter the student's name: ")
    roll_number = input("Enter the student's roll number: ")
    # Check if the document for the student already exists
    student_doc_ref = attendance_collection.document(roll_number)
    if student_doc_ref.get().exists:
        print("Attendance for this student already exists.")
        return
    # Create the document with the student's information
    student_data = {
        "course_code": selected_class_ref.id,
        "user_name": student_name,
        "roll_number": roll_number,
        "date": current_date,
        "time": current_time
    }
    student_doc_ref.set(student_data)
    print("Manual attendance added successfully.")

def display_total_attendance(user_name, class_choice):
    # Convert username to lowercase for case-insensitivity
    user_name_lower = user_name.lower()
    user_collection = db.collection(user_name_lower)
    user_classes_document = user_collection.document("classes")
    # Check if the user's classes document exists
    classes_snapshot = user_classes_document.get()
    if not classes_snapshot.exists:
        print("No classes found for this user.")
        return
    print("Select a class:")
    class_ids = list(user_classes_document.collections())  # Convert generator to list

    # Display class names
    for index, class_ref in enumerate(class_ids):
        print(f"{index + 1}. {class_ref.id}")
    #class_choice = input("Enter the name of the class: ").strip()  # Remove leading/trailing whitespace
    # Check if the input class name matches any of the available class names (case-insensitive)
    selected_class_ref = None
    for class_ref in class_ids:
        if class_ref.id.lower() == class_choice.lower():
            selected_class_ref = class_ref
            break
    if selected_class_ref is None:
        print("Invalid class name.")
        return

    # Get all dates for the selected class
    date_ids = [doc.id for doc in selected_class_ref.stream()]
    # Dictionary to store attendance counts for each student
    attendance_counts = {}

    # Iterate over each date and count attendance for each student
    for date_id in date_ids:
        attendance_collection = selected_class_ref.document(date_id).collection("attendance")
        for doc in attendance_collection.stream():
            data = doc.to_dict()
            student_name = data["user_name"]
            if student_name in attendance_counts:
                attendance_counts[student_name] += 1
            else:
                attendance_counts[student_name] = 1
    # Display total attendance for each student
    print("\nTotal Attendance:")
    print("{:<20} {:<20}".format("Name", "Total Attendance"))
    for student, count in attendance_counts.items():
        print("{:<20} {:<20}".format(student, count))
    print(attendance_counts)
    return attendance_counts

def display_student_users():
    user_student_collection = db.collection("user_student")
    print("Users in user_student collection:")
    docs = user_student_collection.stream()
    student = []
    count = 0
    for doc in docs:
        name = doc.to_dict().get("name")
        if name:
            print(f"{count+1}. {name}")
            student.append(name)
            count += 1
    if count == 0:
        print("No users found.")
    print(student)
    return student
def delete_student_user(user_name):
    user_student_collection = db.collection("user_student")
    display_student_users()
    query = user_student_collection.where("name", "==", user_name)
    docs = query.stream()
    found = False
    for doc in docs:
        found = True
        print(f"User to delete: {doc.id}")
        doc.reference.delete()
    if not found:
        return -1
def add_faculty_user(name, username, password):
    #put it in try block..
    user_faculty_collection = db.collection("user_faculty")
    user_faculty_collection.add({
        "name": name,
        "username": username,
        "password": password
    })

def display_faculty_users():
    user_faculty_collection = db.collection("user_faculty")
    print("Users in user_faculty collection:")
    docs = user_faculty_collection.stream()
    count = 0
    L = []
    for doc in docs:
        username = doc.to_dict().get("username")
        if username:
            print(f"{count+1}. {username}")
            L.append(username)
            count += 1
    if count == 0:
        print("No users found.")
    return L

def delete_faculty(username):
    user_faculty_collection = db.collection("user_faculty")
    query = user_faculty_collection.where("username", "==", username)
    docs = query.stream()
    found = False
    for doc in docs:
        found = True
        doc.reference.delete()
    if not found:
        return -1

def add_admin_user(name, username, password):
    # Check if username already exists
    user_admin_collection = db.collection("user_admin")
    query = user_admin_collection.where("username", "==", username)
    existing_users = [doc.to_dict()["username"] for doc in query.stream()]
    if existing_users:
        return -1
    user_admin_collection.add({
        "name": name,
        "username": username,
        "password": password
    })
    print("Admin user added successfully.")
def display_admin_users():
    user_admin_collection = db.collection("user_admin")
    print("Users in user_admin collection:")
    docs = user_admin_collection.stream()
    count = 0
    for doc in docs:
        name = doc.to_dict().get("name")
        if name:
            print(f"{count+1}. {name}")
            count += 1
    if count == 0:
        print("No users found.")
def delete_admin_user(user_name, password):
    user_admin_collection = db.collection("user_admin")
    display_admin_users()
    query = user_admin_collection.where("name", "==", user_name)
    docs = query.stream()
    found = False
    for doc in docs:
        found = True
        stored_password = doc.to_dict().get("password")
        if stored_password == password:
            print(f"Admin user to delete: {doc.id}")
                # Delete the document
            doc.reference.delete()
            print("Admin user deleted successfully.")
        else:
            print("Incorrect password.")
            return -1
    if not found:
        print("Admin user not found.")
        return -2

def delete_collection(collection_ref, batch_size=500):
    docs = collection_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        subcollections = doc.reference.collections()
        for subcollection in subcollections:
            delete_collection(subcollection, batch_size)
        doc.reference.delete()
        deleted += 1
    if deleted >= batch_size:
        return delete_collection(collection_ref, batch_size)

def delete_collection_except(doc_ref, exclude_doc_id, batch_size=500):
    docs = doc_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        if doc.id == exclude_doc_id:
            continue 
        # Delete subcollections recursively
        subcollections = doc.reference.collections()
        for subcollection in subcollections:
            delete_collection(subcollection, batch_size)
        doc.reference.delete()
        deleted += 1
    if deleted >= batch_size:
        return delete_collection_except(doc_ref, exclude_doc_id, batch_size)
def clear_user_student():
    user_student_collection = db.collection("user_student")
    delete_collection_except(user_student_collection, "temp_dont_delete")
    print("user_student collection cleared successfully except for temp_dont_delete.")

def clear_data():
    # Get all collections
    collections = db.collections()
    for collection in collections:
        collection_id = collection.id
        if collection_id in ["user_faculty", "user_admin", "user_student"]:
            continue  
        delete_collection(collection)
        print(f"{collection_id} collection cleared successfully.")
    clear_user_student()
    print("Data cleared successfully except for user_faculty, user_admin, and user_student (except temp_dont_delete).")

def main_menu():
    user_name = input("Enter your name: ")
    while True:
        print("1. Generate QR Code")
        print("2. Display Attendance")
        print("3. Add Attendance Manually")
        print("4. Total Attendance")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            course_code = input("Enter the course code: ").upper()  # Automatically capitalize input
            date, time = get_date_time()
            location = get_location()
            generate_and_save_qr_code(course_code, date, time, location, user_name)
        elif choice == "2":
            print(display_attendance(user_name))
        elif choice == "3":
            add_manual_attendance(user_name)
        elif choice == "4":
            display_total_attendance(user_name)
        elif choice == "5":
            print("GoodBye!")
            break
        else:
            print("Invalid choice. Please try again.")
#main_menu()

#display_dates('ADBB', 'sahil')
#display_attendance('POP', '2024-02-22', 'sahil')

#display_faculty_users()