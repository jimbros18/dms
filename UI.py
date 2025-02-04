import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from con_sql import get_data

root = tb.Window(themename="cerculean")
colors = root.style.colors
root.geometry("1290x450")

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
    df = get_data()
    if df.empty:
        print("No data found to display.")
        return

    headers = list(df.columns)
    rows = df.values.tolist()

    # main = tb.Frame(root)
    # main.grid(row=0, column=1, padx=5, pady=5)
    # width = root.winfo_width()
    main = tb.Frame(root, style=PRIMARY )
    main.place(x=170, y=0, relwidth=1, relheight=1)
    table = Tableview(main, coldata=headers, rowdata=rows, bootstyle=PRIMARY,
                    pagesize=10, height=10, searchable= True,
                    paginated=True, autofit=True, stripecolor=(colors.light, None))
    # table.pack()
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
    print(f'id: {row_id}, row: {row_data}')

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

