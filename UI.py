import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from con_sql import *

root = tb.Window(themename="cerculean")
colors = root.style.colors
root.geometry("1000x500")

navbar = tb.Frame(root)
navbar.place(x=10, y=0)

main = None
table = None
row_id = None
entry_widgets = []

def create_navbar():
    for key in navbar_items.keys():
        button = tb.Button(navbar, text=key, width=20, bootstyle="primary")
        button.pack(fill="x", pady=5)  

        def on_click(e, k=key):
            navbar_items[k]()

        button.bind("<Button-1>", on_click)
    return navbar

def load_client(): 
    destroy_main()
    global table
    global main
    df = get_db()
    if df.empty:
        print("No data found to display.")
        return
    
    headers = list(df.columns)
    rows = df.values.tolist()

    main = tb.Frame(root, style=PRIMARY )
    main.pack(padx=(170,10), pady=(0,10), fill=BOTH, expand=TRUE)
    table = Tableview(main, coldata=headers, rowdata=rows, bootstyle=PRIMARY,
                    pagesize=10, height=10, searchable= True,
                    paginated=True, autofit=True, stripecolor=(colors.light, None))

    table.autofit_columns()
    style = tb.Style()
    style.configure("custom.Treeview.Heading", font=("Tahoma", 10), background=colors.primary, foreground="white", bordercolor="white",
                    relief=SOLID)
    style.configure("custom.Treeview", highlightthickness=0, bd=0, font=("Tahoma", 9))
    style.map("custom.Treeview", background=[("selected", style.colors.primary )], foreground=[("selected", "#000000")])

    table.configure(style="custom.Treeview")
    table.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
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
    # print(data)
    global main
    destroy_main()
    main = tb.Frame(root, style=INFO)
    main.pack(padx=(170,10), pady=(0,10), fill=BOTH, expand=TRUE)

    style = tb.Style()
    primary_color = style.colors.primary
    style.configure("Custom.TFrame", background="gray", foreground="white")
    style.configure("Custom.TLabel", background=primary_color, foreground="white")

    frame1 = tb.Frame(main, style="Custom.TLabel")
    frame1.pack(padx=(10,5), pady=(10,0), anchor="w")

    for i, (key, value) in enumerate(data.items()):
        label = tb.Label(frame1, text=key.replace('_', ' ').title() + ":", font=("Arial", 12, "bold"), style="Custom.TLabel")
        label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
    
        value_label = tb.Label(frame1, text=str(value), font=("Arial", 12),style="Custom.TLabel")
        value_label.grid(row=i, column=1, sticky='w', padx=5, pady=2)

    btn_frame = tb.Frame(main)
    btn_frame.pack(padx=10, pady=10, anchor="w")

    back = tb.Button(btn_frame, text="Back",  bootstyle=INFO)
    back.grid(row=0, column=0, padx=5, pady=5)
    back.bind("<Button-1>", lambda e: load_client())
    edit = tb.Button(btn_frame, text="Edit",  bootstyle=INFO)
    edit.grid(row=0, column=1, padx=5, pady=5)
    edit.bind("<Button-1>", lambda e: edit_form(data))  

def edit_form(data):
    global main
    # print(data)
    destroy_main()

    main = tb.Frame(root, style=INFO)
    main.pack(padx=(170, 10), pady=(0, 10), fill=BOTH, expand=True)

    scrollable_frame = ScrolledFrame(main, autohide=True, style=INFO)
    scrollable_frame.place(x=0, y=0, relwidth=1, relheight=1)

    in_sframe = tb.Frame(scrollable_frame, style=WARNING)
    in_sframe.pack(fill=BOTH, expand=True, padx=5, pady=5)

    style = tb.Style()
    primary_color = style.colors.primary
    style.configure("Custom.TFrame", background="gray")
    style.configure("Custom.TLabel", background=primary_color, foreground="white")
    style.configure("Custom.TEntry", font=("Arial", 10))

    # Store entry fields
    entries = {}

    def check_changes(*args):
        for key, entry in entries.items():
            if entry.get() != str(data[key]):  # Check if entry is modified
                save.config(state="normal")  # Enable Save button
                return
        save.config(state="disabled")  # Disable Save button if no changes

    for i, (key, value) in enumerate(data.items()):
        label = tb.Label(in_sframe, text=key.replace('_', ' ').title() + ":", 
                         font=("Arial", 12, "bold"), style="Custom.TLabel")
        label.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        entry = tb.Entry(in_sframe, font=("Arial", 10), style="Custom.TEntry")
        entry.insert(0, str(value))  # Set the existing value
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)

        entry.bind("<KeyRelease>", check_changes)  # Detect changes in entry field
        entries[key] = entry

    
    def n_data():
        """Extracts updated values and prints them."""
        new_data = {key: entry.get() for key, entry in entries.items()}
        print(new_data)  # Now this will print the latest values
        # client_form(new_data)  # Call next function with updated data
        return new_data
    
    btn_frame = tb.Frame(in_sframe, style=PRIMARY)
    btn_frame.grid(row=len(data), column=0, columnspan=2, pady=10, sticky="w")

    save = tb.Button(btn_frame, text="Save", bootstyle=INFO, state=DISABLED)
    save.pack(side=LEFT, padx=5)
    save.bind("<Button-1>", lambda e: [update_info(n_data()),client_form(n_data())])

    cancel = tb.Button(btn_frame, text="Cancel", bootstyle=INFO)
    cancel.pack(side=LEFT, padx=5)
    cancel.bind("<Button-1>", lambda e: client_form(data))

    return entries

# def save_changes():


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

navbar_items = {"Client": load_client, "Sales": load_sales, "Expenses":load_exp, "Inventory":load_inv,"Settings":load_settings}

create_navbar()

root.mainloop()

