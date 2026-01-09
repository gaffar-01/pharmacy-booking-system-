import sqlite3
import hashlib

def hash_password(old_password):
    return hashlib.sha256(old_password.encode()).hexdigest() #ENCODES Password into hex digest 
def hash_answer(answer):
    return hashlib.sha256(answer.encode()).hexdigest()


#account login fucntions 

def create_account(email,password,name,role,answer):
    #role checking
    if role not in ("Patient", "Staff",):
        return False, "invalid role"
    #check if user entered all details correctly
    if not name or not email or not password or not answer:
        return False, "all fields required"
    #email error checking 
    if '@' not in email or '.' not in email:
        return False, "invalid email procedure"
    #exception handling if problems with database
    hashed_password = hash_password(password) #calls hash password algorithm to encode password
    hashed_answer = hash_answer(answer)
    try:
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()

        #check if email is in use 
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,)) 
        if cursor.fetchone():
            conn.close()
            return False, "Email already registered."
        #inserts user details into database
        cursor.execute("""
                INSERT INTO users(email,password,name,role,answer)
                VALUES(?,?,?,?,?)
        """, (email,hashed_password,name,role,hashed_answer))

        conn.commit()
        conn.close()
        return True, "account created"
    except sqlite3.Error as e: #checks for error in database
        return False, f"Database error: {str(e)}"

def login(email, password):
    if not email or not password:
        return False, "fill all fields"
    if '@' not in email or '.' not in email:
        return False, "invalid email procedure" #validation
    
    #exception handling if problems with database
    hashed_password = hash_password(password) #calls hash password algorithm to encode password
    
    try:
        
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, name, role
            FROM users
            WHERE email = ? AND password = ?
        """, (email,hashed_password)) #queries database using the arguments to check if email and password is correct

        user = cursor.fetchone() #only need one record 
        conn.close()
        return user
    
    except sqlite3.Error as e: #checks for error in database
        return False, f"Database error: {str(e)}"

def forgot_password(email,new_password,answer):
    if not email or not new_password or not answer:
        return False, "please fill in both email and password and answer" #validation
    
    hashed_answer = hash_answer(answer)
    try:
        conn  = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,)) # queries database for given email 
        valid_user = cursor.fetchone() #only need one record 
        
        if not valid_user:
            conn.close()
            return False, "email is not in data base" #validation 
        hashed_password = hash_password(new_password) #calls hash password algorithm to encode password
        
        cursor.execute("""
                SELECT answer 
                FROM users
                WHERE email = ?
           """, (email,))
        security = cursor.fetchone()
       
        if security[0] != hashed_answer:
            return False, "security answer is incorrect"
            
        cursor.execute("""
            UPDATE users 
            SET password = ?, answer = ?
            WHERE email = ? 
                
        """, (hashed_password,hashed_answer,email)) # updates database with new user details 

        conn.commit()
        conn.close()
        return True, "new password is active"
    except sqlite3.Error as F:#exception handling to handle database error 
        return False, f"error: {str(F)}"
    

def get_services():
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM SERVICES 
    """          )
    services = cursor.fetchall() #collects all records from services  

    conn.close()
    return services

def get_available_slots(date):
    all_slots = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
                 "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", 
                 "15:00", "15:30", "16:00", "16:30"] #1d array for all slots (30 mins)
    
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT time 
        FROM appointments 
        WHERE date = ? 
        AND status = 'Booked' 
    """, (date,)) #sql query to database to find the time of all booked appointments 
    
    booked = cursor.fetchall() #all records/slots that are booked 
    booked_times = [slot[0] for slot in booked]  #only takes the time 
    
    conn.close()
    #compares each slot rom all slots to booked times using linear search - onlu returns available 
    available = [slot for slot in all_slots if slot not in booked_times]
    return available

def book_appointment(user_id, service_id, date, time):
    if user_id == "" or service_id == "" or date == "" or time == "" :
        return False, "all fields are needed" #data handling to  check all fields are correct
    
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM appointments
        WHERE date = ?
        AND time = ? 
        AND status == 'Booked'
    """, (date,time))
    result = cursor.fetchone()

    if result:
        conn.close()
        return False, "time slot not available" #checks database to see if required slot is booked
    else:
        cursor.execute("""
             INSERT INTO appointments(user_id,service_id,date,time,status)
             VALUES(?,?,?,?,'Booked')
        """, (user_id,service_id,date,time)) #inserts details into appointment table iff not booked 

        conn.commit()
        conn.close()
        return True, "Appointment booked"
    

def upcoming_appointments(user_id):
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM appointments
        WHERE user_id = ? 
        AND status = 'Booked'
     """, (user_id,)) 
    appointments = cursor.fetchall() #fetches all appointments that are upcoming and booked status 
    conn.close()
    return appointments #the appointments outputted on the view upcoming interface 

def attended_appointments():
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
           UPDATE appointments
           SET status = 'Attended'
           WHERE date < DATE('now')
           AND status = 'Booked'
        """ )
    conn.commit()
    conn.close()



def cancel_appointment(appointment_id):
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
            UPDATE appointments
            SET status = 'Cancelled'
            WHERE appointment_id = ?
    """, (appointment_id,)) # updates appoitnment in appointment table to cancelled 
    conn.commit()
    conn.close()
    return True, "cancelled"

def previous_appointments(user_id):
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor() 

    cursor.execute("""
        SELECT * FROM appointments
        WHERE user_id = ?
        AND (status = 'Cancelled' OR status = 'Attended') 
    """, (user_id,))
    #query database or either cancelled appointments or those that are past current date 
    appointments = cursor.fetchall()#gets all appointments 
    conn.close()
    return appointments #appointments data shown on interface 

#pharmacist dashboard functions 

def add_service(service_name):
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor() 

    cursor.execute("""
            INSERT INTO services(service_name)
             VALUES(?)
    """, (service_name,)) #inserts service name entry into database service table 
    conn.commit()
    conn.close()
    return True, "service added succesfully"

def get_services():
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT service_id, service_name
        FROM services
    """           )
    services = cursor.fetchall()
    conn.close()
    return services

def delete_service(service_id):
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM services WHERE service_id = ?
        """, (service_id,))
    conn.commit()
    conn.close()
    return True, "service removed"


def staff_cancel(appointment_id):
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
            UPDATE appointments
            SET status = 'Cancelled'
            WHERE appointment_id = ?
    """, (appointment_id,))
    conn.commit()
    conn.close()
    return True, "appointment cancelled successfully"

def all_appointments():
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT appointments.appointment_id, users.name, services.service_name, 
               appointments.date, appointments.time, appointments.status
        FROM appointments
        JOIN users ON appointments.user_id = users.user_id
        JOIN services ON appointments.service_id = services.service_id
        WHERE appointments.status = 'Booked' 
        ORDER BY appointments.date, appointments.time
    """) #cross table referencing - gets user name and service name from other tables 
    appointments = cursor.fetchall() 
    conn.close()
    return appointments #appointment data shown on interface 


create_account('faizal@a.com','password','Faizal','Staff','jibs')








                   

        