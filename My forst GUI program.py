from customtkinter import *

window = CTk()
window.title("My first Calculator")
window.geometry("400x500")

my_entry = CTkEntry(window, width=200, height=40, border_width=2, corner_radius=10)
my_entry.pack(pady=20)

my_entry.pack(pady=20)
button_frame = CTkFrame(window)
button_frame.pack(pady=20)

button_list = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, '+', '_', '*', '/', 'c', '=']
for i, value in enumerate(button_list):
    CTkButton(button_frame, text=value, width=50, height=50, command=lambda v=value: button_click(v)).grid(row=i//4, column=i%4, padx=5, pady=5)

def button_click(action):
    if action == '=':
        try:
            ans = eval(my_entry.get())
            my_entry.delete(0, 'end')
            my_entry.insert(0, str(ans))
        except:
            my_entry.delete(0, "end")
            my_entry.insert(0, "ERROR")
    elif action == 'c':
        my_entry.delete(0,'end')
    else:
        my_entry.insert('end', str(action))

window.bind('<Return>', lambda event: button_click('='))
window.mainloop()

