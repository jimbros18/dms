import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.widgets import DateEntry
from datetime import datetime

from con_sql import *

root = tb.Window(themename="cerculean")
colors = root.style.colors
root.geometry("1065x550")

navbar = None
main = None
table = None
row_id = None
entry_widgets = []

fields = ['First Name', 'Middle Name', 'Last Name', 'Nickname', 'birthdate', 'deathdate',
          'Address', 'age', 'Religion', 'Coffin', 'Amount', 'Gov. Assistance',
          'Mortuary Plan', 'Mortuary Plan Amount', 'Accessories']

def login():
        admin = "king"
        admin_pass = "admin"

        def login_success():
            if username_entry.get() == admin and password_entry.get() == admin_pass:
                frame.destroy()
                create_navbar()
                print("log-in successfull")
            else:
                print("wrong credentials")

        frame = tb.Labelframe(root, padding=20, text="Log-in",  style=INFO)
        frame.pack(pady=(50,0))
        frame.bind("<Return>", lambda e:login_success())

        title_label = tb.Label(frame, text="User Login", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        tb.Label(frame, text="Username:", font=("Arial", 12)).pack(anchor="w")
        username_entry = tb.Entry(frame, bootstyle=INFO)
        username_entry.pack(fill=X, pady=5)

        tb.Label(frame, text="Password:", font=("Arial", 12)).pack(anchor="w")
        password_entry = tb.Entry(frame, show="*", bootstyle=INFO)
        password_entry.pack(fill=X, pady=5)
        # password_entry.bind("<Return>", lambda e:login_success())

        button_frame = tb.Frame(frame)
        button_frame.pack(pady=10, fill=X)

        login_button = tb.Button(button_frame, text="Login", bootstyle=SUCCESS, width=10)
        login_button.pack(side=LEFT, padx=5)
        login_button.bind("<Button-1>", lambda e:login_success())
        login_button.bind("<Return>", lambda e:login_success())

        cancel_button = tb.Button(button_frame, text="Cancel", bootstyle=DANGER, width=10, command=root.quit)
        cancel_button.pack(side=RIGHT, padx=5)

        signup_label = tb.Label(frame, text="Don't have an account? Sign Up", font=("Arial", 10, "underline"), 
                                cursor="hand2", bootstyle=PRIMARY)
        signup_label.pack(pady=5)
        signup_label.bind("<Button-1>", lambda e:print("sign up"))

def log_out():
    global main, navbar
    if main is not None:
        main.destroy()
    if navbar is not None:
        navbar.destroy()
    main = None
    navbar = None
    login() 

def create_navbar():
    global navbar
    navbar = tb.Frame(root)
    navbar.place(x=10, y=0)

    for key in navbar_items.keys():
        button = tb.Button(navbar, text=key, width=20, bootstyle="primary")
        button.pack(fill="x", pady=5)  

        def on_click(e, k=key):
            navbar_items[k]()

        button.bind("<Button-1>", on_click)
    return navbar

def load_client_table(): 
    destroy_main()
    global table
    global main
    df = get_db()
    if df.empty:
        print("No data found to display.")
        return
    sel_headers = ['id','first_name', 'middle_name', 'last_name', 'address', 'coffin', 'amount', 'gov_ass', 'accessories']
    # headers = list(df[sel_headers])
    headers = sel_headers
    # rows = df.values.tolist()
    rows = df[sel_headers].values.tolist()


    main = tb.Frame(root, style=PRIMARY )
    main.pack(padx=(170,10), pady=(0,10), fill=BOTH, expand=TRUE)
    
    btn_1 = tb.Button(main,  text="Add Client", style=WARNING)
    btn_1.place(x=10, y=10)
    btn_1.bind("<Button-1>", lambda e:add_client(fields))

    table = Tableview(main, coldata=headers, rowdata=rows, bootstyle=PRIMARY,
                    pagesize=20, height=20, searchable= True,
                    paginated=True, autofit=True, stripecolor=(colors.light, None))

    table.autofit_columns()
    style = tb.Style()
    style.configure("custom.Treeview.Heading", font=("Tahoma", 10), background=colors.primary, foreground="white", bordercolor="white",
                    relief=SOLID)
    style.configure("custom.Treeview", highlightthickness=0, bd=0, font=("Tahoma", 9))
    style.map("custom.Treeview", background=[("selected", style.colors.primary )], foreground=[("selected", "#000000")])

    table.configure(style="custom.Treeview")
    # table.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    table.place(x=10, y=50)
    table.view.bind("<Double-1>", lambda e: get_row())

def get_row():
    global main
    global table
    global row_id
    global row_data
    row = table.get_rows(selected=True)
    row_id = row[0].values[0]
    row_data = row[0].values
    # print(f'id: {row_id}, row: {row_data}')
    client_form(data = get_client_id(row_id))

def client_form(data):
    global main
    destroy_main()
    main = tb.Frame(root, style=PRIMARY)
    main.pack(padx=(170,10), pady=(0,10), fill=BOTH, expand=TRUE)

    style = tb.Style()
    style.configure("Custom.TLabel", background="#225384", foreground="white")

    info_label = tb.Label(main, text="Personal Info", width=20, foreground="white", background="#4bb1ea", font=("Calibri",15,"bold"))
    info_label.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsew")

    frame1 = tb.Frame(main, style=INFO)
    frame1.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

    for i, (key, value) in enumerate(data.items()):
        label = tb.Label(frame1, text=key.replace('_', ' ').title() + ":", font=("Arial", 12, "bold"), style="Custom.TLabel")
        label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
    
        value_label = tb.Label(frame1, text=str(value), font=("Arial", 12),style="Custom.TLabel")
        value_label.grid(row=i, column=1, sticky='w', padx=5, pady=2)

    btn_frame = tb.Frame(main, width=200, style=PRIMARY)
    btn_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

    back = tb.Button(btn_frame, text="Back", width=15, style=INFO)
    back.grid(row=0, column=0, padx=(10,20), pady=5, sticky="we")
    back.bind("<Button-1>", lambda e: load_client_table())

    edit = tb.Button(btn_frame, text="Edit", width=15,  style=INFO)
    edit.grid(row=0, column=1, padx=(20,10), pady=5, sticky="we")
    edit.bind("<Button-1>", lambda e: edit_form(data))

    v_bar1 = tb.Frame(main, style=PRIMARY)
    v_bar1.grid(row=0, column=1, rowspan=3, sticky="nsew")

    acc_label = tb.Label(v_bar1, text="Accessories",  foreground="white", background="#4bb1ea", font=("Calibri",15,"bold"))
    acc_label.grid(row=0, column=0,  pady=(10,0), sticky="nsew")

    acc_frame = tb.Frame(v_bar1, style=INFO, height=200, width=300)
    acc_frame.grid(row=1, column=0,  pady=(0,10), sticky="nsew")

    pay_label = tb.Label(v_bar1, text="Payments", width=20, foreground="white", background="#4bb1ea", font=("Calibri",15,"bold"))
    pay_label.grid(row=2, column=0, pady=(10,0), sticky="nsew")

    pay_frame = tb.Frame(v_bar1, style=INFO, height=240)
    pay_frame.grid(row=3, column=0, pady=(0,10), sticky="nsew")

    v_bar2 = tb.Frame(main, style=PRIMARY)
    v_bar2.grid(row=0, column=2, rowspan=3, padx=10, sticky="nsew")

    date_label = tb.Label(v_bar2, text="Date", foreground="white", background="#4bb1ea", font=("Calibri",15,"bold"))
    date_label.grid(row=0, column=0, pady=(10,0), sticky="nsew")

    date_frame = tb.Frame(v_bar2, style=INFO, height=200, width=300,)
    date_frame.grid(row=1, column=0, pady=(0,10), sticky="nsew")

    trans_label = tb.Label(v_bar2, text="Transaction History", width=20, foreground="white", background="#4bb1ea", font=("Calibri",15,"bold"))
    trans_label.grid(row=2, column=0,pady=(10,0), sticky="nsew")

    trans_frame = tb.Frame(v_bar2, style=INFO, height=240)
    trans_frame.grid(row=3, column=0, pady=(0,10), sticky="nsew")

def edit_form(data):
    print(data)
    global main
    destroy_main()

    main = tb.Frame(root, style=PRIMARY)
    main.pack(padx=(170, 10), pady=(0, 10), fill=BOTH, expand=True)

    scrollable_frame = ScrolledFrame(main, autohide=True, style=PRIMARY)
    scrollable_frame.place(x=0, y=0, relwidth=1, relheight=1)

    in_sframe = tb.Frame(scrollable_frame, style=PRIMARY)
    in_sframe.pack(fill=BOTH, expand=True, padx=0, pady=0)

    style = tb.Style()
    style.configure("Custom.TLabel", background="#225384", foreground="white")

    info_label = tb.Label(in_sframe, text="Personal Info", width=20, foreground="white", background="#4bb1ea", font=("Calibri", 15, "bold"))
    info_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

    frame1 = tb.Frame(in_sframe, style=INFO)
    frame1.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

    entries = {}

    def check_changes(*args):
        for key, entry in entries.items():
            if isinstance(entry, DateEntry) and entry.entry.get() != str(data[key]):
                print(f"Change detected in {key}: {entry.entry.get()} != {data[key]}")
                save.config(state="normal")
                return
            elif isinstance(entry, tb.Label) and entry.cget() != str(data[key]):
                print(f"Change detected in {key}: {entry.cget()} != {data[key]}")
                save.config(state="normal")
                return
            elif isinstance(entry, tb.Entry) and entry.get() != str(data[key]):
                save.config(state="normal")
                print(f"Change detected in {key}: {entry.get()} != {data[key]}")
                return  
        save.config(state="disabled") 
        print("No changes detected")

    for i, (key, value) in enumerate(data.items()):
        label = tb.Label(frame1, text=key.replace('_', ' ').title() + ":", font=("Arial", 12, "bold"), style="Custom.TLabel")
        label.grid(row=i, column=0, sticky='w', padx=5, pady=2)

        entry = tb.Entry(frame1, font=("Arial", 12), width=30)
        entry.insert(0, str(value))

        if key in ['birthdate', 'deathdate']:
            date_str = value
            date = datetime.strptime(date_str, "%m/%d/%Y")
            entry = DateEntry(frame1, bootstyle=PRIMARY)
            entry.entry.delete(0, tb.END)
            entry.entry.insert(0, date.strftime("%m/%d/%Y"))
        elif key in 'age':
            entry = tb.Label(frame1, text=value, font=('Arial', 12), width=31, foreground="white", background="#225384")
        else:
            entry = tb.Entry(frame1, font=('Arial', 12), width=30)
            entry.insert(0,str(value))

        entry.grid(row=i, column=1, sticky='w', padx=5, pady=2)
        entries[key] = entry 
        entry.bind("<KeyRelease>", check_changes)
    
    def n_data():
        """Extracts updated values and prints them."""
        data = []
        for key, entry in entries.items():
            if isinstance(entry, DateEntry):  # Check if the entry is a DateEntry widget
                value = entry.entry.get()  # Use the entry attribute to get the date
            elif isinstance(entry, tb.Label):
                value = entry.cget("text")
            else:
                value = entry.get()  # Use the standard get() method for other widgets
            data.append(value)
        return data
    
    def save_changes(event=None):
        """Executes saving only if the save button is enabled."""
        if save.instate(["!disabled"]):  # Check if save is enabled
            new_values = n_data()  # Extract new values
            print("Saving data:", new_values)  # Debugging print statement
            update_info(new_values)  # Save the updated info
            client_form(new_values)  # Load updated data into form
        else:
            print("Save button is disabled")

    btn_frame = tb.Frame(in_sframe, width=200, style=PRIMARY)
    btn_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

    save = tb.Button(btn_frame, text="Save", bootstyle=INFO, state=DISABLED)
    save.pack(side=LEFT, padx=5)
    save.bind("<Button-1>", save_changes)

    cancel = tb.Button(btn_frame, text="Cancel", bootstyle=INFO)
    cancel.pack(side=LEFT, padx=5)
    cancel.bind("<Button-1>", lambda e: client_form(data))

    v_bar1 = tb.Frame(in_sframe, style=PRIMARY)
    v_bar1.grid(row=0, column=1, rowspan=3, sticky="nsew")

    acc_label = tb.Label(v_bar1, text="Accessories", foreground="white", background="#4bb1ea", font=("Calibri", 15, "bold"))
    acc_label.grid(row=0, column=0, pady=(10, 0), sticky="nsew")

    acc_frame = tb.Frame(v_bar1, style=INFO, height=200, width=300)
    acc_frame.grid(row=1, column=0, pady=(0, 10), sticky="nsew")

    pay_label = tb.Label(v_bar1, text="Payments", width=20, foreground="white", background="#4bb1ea", font=("Calibri", 15, "bold"))
    pay_label.grid(row=2, column=0, pady=(10, 0), sticky="nsew")

    pay_frame = tb.Frame(v_bar1, style=INFO, height=240)
    pay_frame.grid(row=3, column=0, pady=(0, 10), sticky="nsew")

    v_bar2 = tb.Frame(in_sframe, style=PRIMARY)
    v_bar2.grid(row=0, column=2, rowspan=3, padx=10, sticky="nsew")

    date_label = tb.Label(v_bar2, text="Date", foreground="white", background="#4bb1ea", font=("Calibri", 15, "bold"))
    date_label.grid(row=0, column=0, pady=(10, 0), sticky="nsew")

    date_frame = tb.Frame(v_bar2, style=INFO, height=200, width=300)
    date_frame.grid(row=1, column=0, pady=(0, 10), sticky="nsew")

    trans_label = tb.Label(v_bar2, text="Transaction History", width=20, foreground="white", background="#4bb1ea", font=("Calibri", 15, "bold"))
    trans_label.grid(row=2, column=0, pady=(10, 0), sticky="nsew")

    trans_frame = tb.Frame(v_bar2, style=INFO, height=240)
    trans_frame.grid(row=3, column=0, pady=(0, 10), sticky="nsew")

    return entries

def add_client(fields):
    global main
    destroy_main()

    main = tb.Frame(root, style='primary')
    main.pack(padx=(170, 10), pady=(0, 10), fill='both', expand=True)

    scrollable_frame = ScrolledFrame(main, autohide=True, style='primary')
    scrollable_frame.place(x=0, y=0, relwidth=1, relheight=1)

    in_sframe = tb.Frame(scrollable_frame, style='primary')
    in_sframe.pack(fill='both', expand=True)

    info_label = tb.Label(in_sframe, text='Personal Info', width=20, foreground='white',
                          background='#4bb1ea', font=('Calibri', 15, 'bold'))
    info_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='nsew')

    frame1 = tb.Frame(in_sframe, style='info')
    frame1.grid(row=1, column=0, padx=10, pady=0, sticky='nsew')

    entries = {}

    def check_changes(*args):
        for entry in entries.values():
            if isinstance(entry, DateEntry): 
                value = entry.entry.get().strip()
            if isinstance(entry, tb.Label): 
                value = entry.cget("text")
            else:
                value = entry.get().strip()
            if value:  # If any input is not empty
                save.config(state='normal')
                return
        save.config(state='disabled')  # Disable button if all fields are empty

    def calculate_age(b_day, d_date, age_today ,event=None):
        """Calculate age based on the selected bdate_str."""
        bdate_str = b_day.entry.get().strip()
        ddate_str = d_date.entry.get().strip()
        if bdate_str:
            try:
                b_date = datetime.strptime(bdate_str, "%m/%d/%Y")
                d_date = datetime.strptime(ddate_str, "%m/%d/%Y")
                age = d_date.year - b_date.year - ((d_date.month, d_date.day) < (b_date.month, b_date.day))
                age_today.config(text=str(age))
            except ValueError:
                print(f"Invalid date format: {bdate_str}")
        else:
            print("No bdate_str selected.")

    for i, field in enumerate(fields):
        label = tb.Label(frame1, text=field.replace('_', ' ').title() + ':', 
                        font=('Arial', 12, 'bold'), foreground="white", background="#225384")
        label.grid(row=i, column=0, sticky='w', padx=5, pady=2)

        if field in ['birthdate', 'deathdate']:
            entry = DateEntry(frame1, bootstyle=PRIMARY)
        elif field == 'age':
            entry = tb.Label(frame1, font=('Arial', 12), width=31, foreground="white", background="#225384")
        else:
            entry = tb.Entry(frame1, font=('Arial', 12), width=30)

        entry.grid(row=i, column=1, sticky='w', padx=5, pady=2)
        entries[field] = entry 
        entry.bind("<KeyRelease>", check_changes)

    if "deathdate" in entries:
        entries["deathdate"].bind("<FocusOut>", lambda event: calculate_age(entries["birthdate"], entries["deathdate"], entries["age"]))
    else:
        print("Warning: 'birthdate' or 'age' field not found in entries.")

    def n_data():
        """Extracts values from all entries, handling DateEntry widgets."""
        data = []
        for fields, entry in entries.items():
            if isinstance(entry, DateEntry):  # Check if the entry is a DateEntry widget
                value = entry.entry.get()  # Use the entry attribute to get the date
            elif isinstance(entry, tb.Label):
                value = entry.cget("text")
            else:
                value = entry.get()  # Use the standard get() method for other widgets
            data.append(value)
        return data

    btn_frame = tb.Frame(in_sframe, width=200, style='primary')
    btn_frame.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')

    save = tb.Button(btn_frame, text='Save', bootstyle='info', state='disabled')
    save.pack(side='left', padx=5)
    save.bind("<Button-1>", lambda e: [print(n_data()), save_to_db(n_data()), load_client_table()])
    # save.bind("<Button-1>", lambda e: print(n_data()))


    cancel = tb.Button(btn_frame, text='Cancel', bootstyle='info')
    cancel.pack(side='left', padx=5)
    cancel.bind("<Button-1>", lambda e:load_client_table())

    return entries

def load_sales():
    destroy_main()
    global main
    main = tb.Frame(root, bootstyle=PRIMARY)
    main.grid(row=0, column=1, sticky="nw", padx=5, pady=10)

def load_exp():
    destroy_main()
    global main
    main = tb.Frame(root, bootstyle=SECONDARY)
    main.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

def load_inv():
    destroy_main()
    global main
    main = tb.Frame(root, bootstyle=INFO)
    main.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

def load_settings():
    destroy_main()
    global main
    main = tb.Frame(root, bootstyle=PRIMARY)
    main.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

def destroy_main():
    global main
    if main is not None:
        main.destroy()
        main = None

navbar_items = {"Client": load_client_table, "Sales": load_sales, "Expenses":load_exp, "Inventory":load_inv,"Settings":load_settings, "Log-out": log_out}

login()

root.mainloop()

