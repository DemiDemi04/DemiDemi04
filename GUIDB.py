import tkinter as tk
from tkinter import ttk
import mysql.connector

# Function to display the data in the table
def display_data():
    # Clear previous data in the table
    for row in tree.get_children():
        tree.delete(row)

    conn = mysql.connector.connect(user='root', password='Darian123123', host='localhost', database='matched_faces')
    c = conn.cursor()
    c.execute('SELECT face_id, timestamp FROM faces')
    rows = c.fetchall()
    for row in rows:
    
        tree.insert('', 'end', values=(row[0], row[1], True))
    
    conn.close()
 
root = tk.Tk()
root.title('Database Table Viewer')

#display the table
tree = ttk.Treeview(root, columns=('face_id', 'timestamp', 'Checkbox' ,), show='headings')
tree.heading('face_id', text='ID' )
tree.heading('timestamp', text='Timestamp')
tree.heading('Checkbox', text='Checkbox')
tree.pack(padx=10, pady=10)


# Call the display_data function to display the data
display_data()

root.geometry('600x300')
root.configure(bg = '#9772F9')

# Run the Tkinter main loop
root.mainloop()