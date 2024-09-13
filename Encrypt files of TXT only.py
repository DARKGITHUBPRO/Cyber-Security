from tkinter import Menu
import os
from tkinter import Tk, Label, Button, filedialog, messagebox, Frame
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
#=========================================================================

# اختيــــار صيغ الملف

filetypes = [
("Text files", ".txt"),
("all files", "."),
("all files","*.*"),
("python files","*.py")
]

#=========================================================================

# برمــجـــة دوال القائــمه
def New_File () :
  new_file = filedialog.askopenfile(title="اختر ملف" , initialdir="/",filetypes=[("text Files",".txt"),("All Files","*.*")])
  messagebox.showwarning("فقدان البيانات","لم يتم التعريف علي الملف!")

#=========================================================================
#=========================================================================


# توليد وحفظ المفتاح
def generate_key():
    key = get_random_bytes(16)  # AES-128
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)

# قراءة المفتاح من الملف
def load_key():
    if not os.path.exists('filekey.key'):
        generate_key()
    with open('filekey.key', 'rb') as filekey:
        return filekey.read()

# تشفير الملف
def encrypt_file(file_path):
    key = load_key()
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        original = file.read()
    ciphertext, tag = cipher.encrypt_and_digest(original)
    with open(file_path, 'wb') as encrypted_file:
        for x in (cipher.nonce, tag, ciphertext):
            encrypted_file.write(x)
    messagebox.showinfo("Success", "File Encrypted Successfully!")

# فك تشفير الملف
def decrypt_file(file_path):
    try:
        key = load_key()
        with open(file_path, 'rb') as enc_file:
            nonce, tag, ciphertext = [enc_file.read(x) for x in (16, 16, -1)]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        with open(file_path, 'wb') as dec_file:
            dec_file.write(decrypted)
        messagebox.showinfo("Success", "File Decrypted Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during decryption: {str(e)}")

# واجهة المستخدم الرسومية
def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=filetypes)
    label_file_explorer.configure(text="File Opened: " + filename)
    return filename

def encrypt_action():
    file_path = browse_files()
    Encrypt = messagebox.askokcancel("تشفير الملف...!", "هل انت متــأكد من تشفيــر الملف!!؟",
    icon="warning", detail="كن حذراً قبل اي شئ",parent=window)
    if Encrypt:
            if file_path:
                encrypt_file(file_path)
                label_file_explorer.configure(text="File Encrypted: " + file_path)
    else:
        messagebox.showinfo("هناك خطأ", "لم يتم تشفير الملف")

def decrypt_action():
    file_path = browse_files()
    if file_path:
        decrypt_file(file_path)
        label_file_explorer.configure(text="File Decrypted: " + file_path)

# إعداد نافذه tkinter
window = Tk()
window.title('File Encryption/Decryption')
window.geometry("600x300")
window.config(background="#f0f0f0")

# إعداد الإطارات لتنسيق الأزرار
frame_top = Frame(window, bg="#f0f0f0")
frame_middle = Frame(window, bg="#f0f0f0")
frame_bottom = Frame(window, bg="#f0f0f0")

label_file_explorer = Label(frame_top, text="File Explorer using Tkinter", width=100, height=4, fg="blue", bg="#f0f0f0", font=('Helvetica', 14, 'bold'))
#=========================================================
button_encrypt = Button(frame_middle, text="Encrypt File", command=encrypt_action, bg="red", fg="white", font=('Helvetica', 12, 'bold'))
button_encrypt.place(x=250,y=20)
#=========================================================
#=========================================================
button_decrypt = Button(frame_middle, text="Decrypt File", command=decrypt_action, bg="green", fg="white", font=('Helvetica', 12, 'bold'))
button_decrypt.place(x=250,y=20,width=50)
#=========================================================
#=========================================================
#button_exit = Button(frame_bottom, text="Exit", command=window.quit, bg="grey", fg="white", font=('Helvetica', 12, 'bold'),width=20)
#button_exit.place(x=250,y=10)

# ترتيب الإطارات والأزرار
frame_top.pack(pady=10)
frame_middle.pack(pady=10)
frame_bottom.pack(pady=10)

label_file_explorer.pack()
button_encrypt.pack(side="left", padx=20)
button_decrypt.pack(side="right", padx=20)
#button_exit.pack()
# Menu create
menu =  Menu(window)
window.config(menu=menu)
# file menu
files = Menu(menu,tearoff=False,font=("",10,"bold"))
files.config()
menu.add_cascade(label="Control Options",menu=files)

files.add_cascade(label="New" , command=New_File)

files.add_cascade(label="Open")

files.add_separator()
files.add_cascade(label="Save")

files.add_separator()
files.add_checkbutton(label="Auto Save")
files.add_separator()

files.add_cascade(label="Connect With Us")

files.add_separator()
files.add_cascade(label="Arabic Language")
files.add_cascade(label="English Language")
files.add_separator()

# root.bind("<Tab-DR>",())


files.add_command(label="About Program                                     Ctrl+P")

files.add_separator()

files.add_cascade(label="Exit",command=exit)




window.mainloop()

# Developer :: Mohammed Alaa Mohammed
# Info about This :: This Project under Developer