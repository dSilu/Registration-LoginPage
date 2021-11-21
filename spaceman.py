"""
Before Running the program,
Connect to your mongodb cluster.
"""


# Libraries used
from tkinter import *
from tkinter import font
import pymongo
import re
from PIL import ImageTk, Image
import tkinter.messagebox as msg
import time
from tkinter import ttk
import webbrowser



# Connect to the database
client = pymongo.MongoClient("mongodb+srv://<User Name>:<Password>@<cluster Name>.zwgfj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test

db = client.get_database('<DataBase Name>')
mycol = db.collection_name # write collection name here


# Minimized window
def minimized_window():
    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    root.geometry(f'{width}x{height}+{x_cord}+{y_cord}')


# Page navigation
def change_to_signin():
    signin_frame.pack(fill='both',expand=True)
    login_frame.forget()
    home_frame.forget()
    work_frame.forget()
    reset_frame.forget()

def change_to_login():
    login_frame.pack(fill='both',expand=1)
    signin_frame.forget()
    home_frame.forget()
    work_frame.forget()
    reset_frame.forget()
    
def change_to_home():
    home_frame.pack(fill='both', expand=True)
    signin_frame.forget()
    login_frame.forget()
    work_frame.forget()
    reset_frame.forget()

def change_to_reset():
    reset_frame.pack(fill='both', expand=True)
    signin_frame.forget()
    login_frame.forget()
    work_frame.forget()
    home_frame.forget()


def login_center():
    check = 0
    warn = ''
    b = ''
    a = ''

    my_query = {'_id':username_enter.get()}
    for x in mycol.find(my_query):
        a = x['Passcode'] # password
        b = x['_id'] # user name
    
    entered_password = pas_enter.get()
    
    if username_enter.get() == '' and entered_password == '':
        warn = 'Enter user credentials'
    else:
        check += 1

    if username_enter.get() == b and entered_password==a:
        check += 1
    else:
        warn = 'Semms you are new here. Register to continue'
    
    if check == 2:
        try:
            work_frame.pack(fill='both', expand=True)
            login_frame.forget()
            signin_frame.forget()
            home_frame.forget()
            
        except Exception as ep:
            msg.showerror('Something went wrong. Try again')
    else:
        msg.showerror('Error', warn)

    username_enter.delete(0, END)
    pas_enter.delete(0, END)



def validator():
    #msg.showinfo('Validating informations')
    check_counter = 0
    warn = ''

    mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    pas_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,16}$"
    c_reg = re.compile(pas_regex) # compile regex

    f_name = snfn_entry.get()
    l_name = snfn_entry.get()
    email_id = snmail_entry.get()
    u_name = snun_entry.get()
    pwd = snpas_entry.get()
    
    if f_name == '':
        warn = "First Name can't be empty"
    else:
        check_counter +=1
    
    if l_name == '':
        warn = "Last Name can't be empty"
    else:
        check_counter += 1
    
    if email_id == '':
        warn = "Email ID can't be empty"
    else:
        check_counter += 1
    
    if u_name == '':
        warn = "User name can't be empty"
    else:
        check_counter += 1
    
    res = re.search(c_reg, pwd)
    if res:
        check_counter += 1
    else:
        warn = 'Password must be in between 5-16 letter long\nMust have at least \n* One uppercase and lowercase letter\n* A special character\n* A digit'
    
    
    myquery1 = {'_id':u_name}

    if myquery1 in mycol.find():
        warn = 'User name already exists'
    else:
        check_counter += 1
    
    if (re.fullmatch(mail_regex, email_id)):
        check_counter += 1
    else:
        warn = 'Invalid Email'
    
    myquery2 = {'Email ID':email_id}

    if myquery2 in mycol.find():
        warn = 'Email ID already exist, Please login'
    else:
        check_counter += 1
    
    processing_time()

    if check_counter == 8:
        try:
            user_data = {'_id':u_name, 'First Name':f_name, 'Last Name':l_name, 'Email ID':email_id, 'Passcode':pwd}
            mycol.insert_one(user_data)
            msg.showinfo('Info', 'Welcome on board!')
            login_frame.pack(fill='both', expand=True)
            signin_frame.forget()
            work_frame.forget()
            home_frame.forget()
        except Exception as ep:
            msg.showerror('Try another Mail ID or User Name')
    else:
        msg.showerror('Error', warn)
    
    snfn_entry.delete(0, END)
    snlsn_entry.delete(0, END)
    snmail_entry.delete(0, END)
    snun_entry.delete(0, END)
    snpas_entry.delete(0, END)


def reset_setting():
    a = ''
    check = 0
    warn = ''

    mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    pas_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,16}$"
    c_reg = re.compile(pas_regex) # compile password regex

    user_info1 = ExistingUserName.get()
    user_info2 = ExistingEmailID.get()
    newps_info = NewPassEnter.get()

    if user_info1 == '':
        warn = 'Please enter your registered User Name'
    else:
        check += 1
    
    if user_info2 == '':
        warn = 'Please entery your registered Email ID'
    else:
        check += 1

    if (re.fullmatch(mail_regex, user_info2)):
        check += 1
    else:
        warn = 'Invalid Email'

    res = re.search(c_reg, newps_info)
    if res:
        check += 1
    else:
        warn = 'Password must be in between 5-16 letter long\nMust have at least \n* One uppercase and lowercase letter\n* A special character\n* A digit'

    my_query = {'_id':user_info1}
    for data in mycol.find(my_query):
        a = data['Email ID']

    if user_info2 == a:
        check += 1
    else:
        warn = 'Please enter your registerd email ID'
    

    if check == 5:
        try:
            mycol.update_one(my_query,{'$set':{'Passcode':newps_info}})
            msg.showinfo('Info', 'Reset operation successful!')
            login_frame.pack(fill='both', expand=True)
            reset_frame.forget()
        except Exception as ep:
            msg.showerror('Error',ep)
    else:
        msg.showerror('Error', warn)

    ExistingUserName.delete(0, END)
    ExistingEmailID.delete(0, END)
    NewPassEnter.delete(0, END)

# time to process
def processing_time():
    global progress

    progress = ttk.Progressbar(signin_frame, orient=HORIZONTAL, length=200, mode='determinate')
    progress.place(x=(width/3)-70, y=310)
    my_progress()
    progress.after(1000, progress.destroy())


def my_progress():
    global progress
    for x in range(5):
        progress['value'] += 20
        signin_frame.update_idletasks()
        time.sleep(1)

def callback(url):
    webbrowser.open_new(url)


root = Tk()
root.title('Just checking')
# root.config(bg='blue')


# screen size
width, height = 500, 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
minimized_window()


# frames
login_frame = Frame(root, relief=SOLID,bg='white')
signin_frame = Frame(root, relief=SOLID, bg='White')
home_frame = Frame(root, relief=SOLID ,bg='white')
work_frame = Frame(root, relief=SOLID, bg='white')
reset_frame = Frame(root, relief=SOLID, bg='white')


# variables
myvar1 = StringVar()
myvar2 = StringVar()
myvar3 = StringVar()
myvar4 = StringVar()
myvar5 = StringVar()
myvar6 = StringVar()
myvar7 = StringVar()
myvar8 = StringVar()
myvar9 = StringVar()
myvar10 = StringVar()


# Page labels
Label(
    home_frame,
    text='Hello, World!', 
    bg='#033e3e', 
    width=width, 
    height='2', 
    fg='white', 
    font='Monospace 20 bold'
).pack(pady=5)

Label(
    login_frame,
    text= 'Login Center',
    bg= '#033e3e',
    width= width,
    height=2,
    fg='White',
    font='Monospace 20 bold'
).pack(pady=5)

Label(
    signin_frame,
    text='Registration Hall',
    width= width,
    bg='#033e3e',
    height='2',
    font='Monospace 20 bold',
    fg='white'
).pack(pady=5)

Label(
    reset_frame,
    text='Account Recovery',
    width= width,
    height=2,
    bg='#033e3e',
    fg='white',
    font='Monospace 20 bold'
).pack(pady=5)

Label(
    work_frame,
    text='Work Station',
    width= width,
    bg='#033e3e',
    fg='white',
    font='Monospace 20 bold'
).pack(pady=5)


# Home Page
home_img = ImageTk.PhotoImage(Image.open('astronaut.png').resize((150, 150), Image.ANTIALIAS))
Label(home_frame, image=home_img).pack(pady=5)

Label(
    home_frame, 
    text='From another Galaxy?',
    font='Georgia 12',
    bg='white'
).place(x=(width/6)-5, y=275)

Button(
    home_frame,
    text='Sign Up',
    relief=RAISED,
    bg= '#045f5f',
    fg='white',
    activeforeground='black',
    activebackground='white',
    bd=2,
    font='Georgia 11',
    width=6,
    cursor='hand2',
    command=change_to_signin
).place(x=(width/2)+80, y=270)

Label(
    home_frame,
    text='Remember something?',
    font='Georgia 12',
    bg='white'
).place(x=(width/6)-5,y=328)

Button(
    home_frame,
    text='Login',
    font='Georgia 11',
    activebackground='white',
    activeforeground='black',
    bd='2',
    bg='#c34a2c',
    fg='white',
    width= 6,
    cursor='hand2',
    command=change_to_login
).place(x=(width/2)+80,y=321)



# Login Page
Label(
    login_frame,
    text = 'User Name',
    bg= 'white',
    font='Georgia, 11',
).place(x=(width/5)-55, y=100)

Label(
    login_frame, 
    text='Password',
    bg='white',
    font='Georgia 11'
).place(x= (width/5)-55, y=145)

username_enter = Entry(
    login_frame,
    textvariable=myvar1,
    bd=2,
    width=30,
    justify=CENTER,
)
username_enter.place(x=(width/2)-95, y=95)

pas_enter = Entry(
    login_frame,
    textvariable=myvar2,
    bd=2,
    width=30,
    show='*',
    justify=CENTER)
pas_enter.place(x=(width/2)-95, y= 140)

login_button = Button(
    login_frame,
    text='Login',
    relief=RAISED,
    bg= '#c34a2c',
    activebackground='white',
    activeforeground='blue',
    bd=2,
    font='Georgia 12',
    fg='white',
    width=6,
    cursor='hand2',
    command=login_center
)
login_button.place(x=(width/2)+92, y=195)



# forget password
Label(
    login_frame,
    text='Forget Password?',
    font='Georgia 12',
    bg= 'white'
).place(x=(width/2)-145, y=310)

Button(
    login_frame,
    text='Reset',
    relief=RAISED,
    bd=1,
    font='Georgia 12',
    width=5,
    bg = '#5e5a80',
    fg='white',
    activebackground='white',
    activeforeground='blue',
    cursor='hand2',
    command=change_to_reset
).place(x=(width/2)+20, y=300)


# Registration Page
Label(signin_frame, text='First Name', bg='white', font='Georgia 11').place(x=25, y=95)
Label(signin_frame, text='Second Name', bg='white', font='Georgia 11').place(x=25, y=135)
Label(signin_frame, text='Email ID', bg='white', font='Georgia 11').place(x=25, y=175)
Label(signin_frame, text='User Name', bg='white', font='Georgia 11').place(x=25, y=215)
Label(signin_frame, text='Password', bg='white', font='Georgia 11').place(x=25, y=255)

snfn_entry = Entry(signin_frame, textvariable=myvar3, bd=2, width=30, justify=CENTER)
snlsn_entry = Entry(signin_frame, textvariable=myvar4, bd=2, width=30, justify=CENTER)
snmail_entry = Entry(signin_frame, textvariable=myvar5, bd=2, width=30, justify=CENTER)
snun_entry = Entry(signin_frame, textvariable=myvar6, bd=2, width=30, justify=CENTER)
snpas_entry = Entry(signin_frame, textvariable=myvar7, bd=2, width=30, show='*', justify=CENTER)

sn_fname_var = StringVar()
sn_lname_var = StringVar()
sn_email_var = StringVar()
sn_username_var = StringVar()
sn_password_var = StringVar()

snfn_entry.place(x=(width/3)-20, y=92)
snlsn_entry.place(x=(width/3)-20, y=132)
snmail_entry.place(x=(width/3)-20, y=172)
snun_entry.place(x=(width/3)-20, y=212)
snpas_entry.place(x=(width/3)-20, y=252)

Button(
    signin_frame,
    bd=2,
    width=7,
    text='Register',
    fg='white',
    bg='#045f5f',
    font='Georgia 11',
    activeforeground='blue',
    activebackground='white',
    cursor='hand2',
    command=validator
).place(x=(width/2)+80,y=295)



# Password reset Page
Label(reset_frame, text='User name',font='Georgia 11', bg='white').place(x=25, y=95)
Label(reset_frame, text='Email ID', font='Georgia 11', bg='white').place(x=25, y=135)
Label(reset_frame, text='New Password', font='Georgia 11', bg='white').place(x=25, y=175)

ExistingUserName= Entry(
    reset_frame,
    textvariable=myvar8,
    bd=2,
    width=30,
    justify=CENTER
)
ExistingUserName.place(x=(width/2)-100, y=92)

ExistingEmailID = Entry(
    reset_frame,
    textvariable=myvar9,
    bd=2,
    width=30,
    justify=CENTER)
ExistingEmailID.place(x=(width)/2-100, y=132)

NewPassEnter = Entry(
    reset_frame,
    textvariable=myvar10,
    bd=2,
    width=30,
    show='*',
    justify=CENTER
)
NewPassEnter.place(x=(width/2)-100, y=172)

Button(
    reset_frame, 
    text='Reset', 
    fg='white', 
    bg='#5e5a80', 
    width=6, 
    bd=2,
    activebackground='white',
    activeforeground='blue',
    relief=RAISED,
    font='Georgia 11',
    cursor='hand2', 
    command=reset_setting
).place(x=(width)/2, y= 220)


#work Station
Label(
    work_frame,
    text='To listen a song',
    bg='white',
    font='Georgia 12'
).pack(pady=50)

url = 'https://youtu.be/D7xOZVBAWtw'
link = Label(
    work_frame,
    text='Click Here',
    bg='white',
    fg='blue',
    font='Georgia 12',
    cursor='hand2'
)
link.pack()
link.bind('<Button-1>', lambda x: callback(url))

# Home buttons
home_icon = PhotoImage(file='icons8-home-24.png')
home_btn_1= Button(
    signin_frame,
    image= home_icon,
    bd='3',
    background='white',
    activeforeground='white',
    command=change_to_home
)

home_btn_2 = Button(
    login_frame,
    image= home_icon,
    bd='3',
    background='white',
    activeforeground='white',
    command=change_to_home
)

home_btn_3 = Button(
    work_frame,
    image= home_icon,
    bd='3',
    background='white',
    activeforeground='white',
    command=change_to_home
)

home_btn_4 = Button(
    reset_frame,
    image=home_icon,
    background='white',
    activeforeground='white',
    command=change_to_home
)

home_btn_1.pack(side=BOTTOM)
home_btn_2.pack(side=BOTTOM)
home_btn_3.pack(side=BOTTOM)
home_btn_4.pack(side=BOTTOM)



home_frame.pack(fill='both', expand=1)

root.mainloop()
