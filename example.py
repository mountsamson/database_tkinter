import tkinter
import requests
import json
from tkinter import ttk

#import country list
from country import COUNTRY_LIST

def enter_data():
      # Get data from UI elements
    firstname = first_name_entry.get()
    lastname = last_name_entry.get()
    title = title_combobox.get()
    age = age_spinbox.get()
    nationality = nationality_combobox.get()
    numcourses = numcourses_spinbox.get()
    numsemesters = numsemesters_spinbox.get()
   
    

    # Prepare the data payload
    data = {
        "data": [
            {
                "First Name": firstname,
                "Last Name": lastname,
                "Title": title,
                "Age": age,
                "Nationality": nationality,
                "Number of Courses": numcourses,
                "Number of Semesters": numsemesters,
              
            }
        ]
    }

    # Send the data to the SheetDB API
    response = requests.post("https://sheetdb.io/api/v1/2s24b7asm4g0s", json=data)

    # Print the response for debugging
    print(response.status_code)
    print(response.json())
    

#setting up windows canva
window = tkinter.Tk()
window.title("Data Entry Form - by SamsCo Tech")

frame = tkinter.Frame(window)
frame.pack()



#Saving user information 
user_info_frame = tkinter.LabelFrame(frame, text ="User Information") #this is a label section frame
user_info_frame.grid(row= 0, column= 0, padx=20, pady=10)

#labels
first_name_label = tkinter.Label(user_info_frame, text = "First Name")
first_name_label.grid(row= 0, column= 0)
last_name_label = tkinter.Label(user_info_frame, text = "Last Name")
last_name_label.grid(row= 0, column= 1)

#field form entry
first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

#dropdown box Name Title
title_label = tkinter.Label(user_info_frame, text = "Title")
title_combobox = ttk.Combobox(user_info_frame, values=["Mr", "Mrs", "Miss", "Ms", "Dr"])
title_label.grid(row=0, column =2)
title_combobox.grid(row=1, column=2)

#increment field age
age_label = tkinter.Label(user_info_frame, text="Age")
age_spinbox = tkinter.Spinbox(user_info_frame, from_ =18, to=110)
age_label.grid(row=2, column=0)
age_spinbox.grid(row=3, column=0)

#nationality drop down box
nationality_label = tkinter.Label(user_info_frame, text="Nationality")
nationality_combobox = ttk.Combobox(user_info_frame, values=COUNTRY_LIST)
nationality_label.grid(row=2, column=1)
nationality_combobox.grid(row=3, column=1)

#add padding
for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
    
# Date of Birth entry



#Saving Course Information
course_info= tkinter.LabelFrame(frame)  #this is a label section frame
course_info.grid(row= 1, column=0, sticky="news",padx=20, pady=10)

registered_label = tkinter.Label(course_info, text="Registered Status")
registered_check = tkinter.Checkbutton(course_info, text="Currently Registered")
registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)

numcourses_label = tkinter.Label(course_info, text="Number of Courses")
numcourses_spinbox = tkinter.Spinbox(course_info, from_=0, to="infinity")
numcourses_label.grid(row=0, column=1)
numcourses_spinbox.grid(row=1, column=1)

numsemesters_label = tkinter.Label(course_info, text="Number of Semesters")
numsemesters_spinbox = tkinter.Spinbox(course_info, from_=0, to="infinity")
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox.grid(row=1, column=2)

for widget in course_info.winfo_children():
    widget.grid_configure(padx=10, pady=5)
    
#accept terms
terms_frame = tkinter.LabelFrame(frame, text="Terms and Conditions")
terms_frame.grid(row= 2, column=0, sticky="news", padx=20, pady=10)

terms_check = tkinter.Checkbutton(terms_frame, text="I accept the terms and conditions")
terms_check.grid(row=0, column=0)

terms_frame_2 = tkinter.LabelFrame(frame, text="test")
terms_frame_2.grid(row=3, column=0, sticky="news", padx=20, pady=10)

terms_check = tkinter.Checkbutton(terms_frame, text="test")
terms_check.grid(row=1, column=0)






#Button 
button = tkinter.Button(frame, text="Enter data", command= enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)


window.mainloop()