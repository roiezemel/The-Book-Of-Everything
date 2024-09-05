from tkinter import *
from PIL import ImageTk, Image
from reform import *
from tkinter import ttk
import re


CHAPTER_SIZE = 10 ** 12  # in pages
PART_SIZE = (10 ** 12) * CHAPTER_SIZE  # in chapters


def right():
    global curr_page
    curr_page += 1
    show_page()


def left():
    global curr_page
    if curr_page == 0:
        return
    curr_page -= 1
    show_page()


def clear_new_lines():
    global e1
    val = e1.get()
    e1.delete(0, END)
    e1.insert(0, val.replace('\n', ''))


def search():
    global curr_page, e1
    clear_new_lines()
    manager.define_chars(var1.get(), var2.get(), var3.get(), var4.get())
    val = e1.get()
    if len(val) == 0:
        manager.clear_search_result()
        return
    if not all([c in manager.CHARS for c in e1.get()]):
        if var3.get() and not any([var1.get(), var2.get(), var4.get()]) \
                and (special_search := special_number_search(e1.get())) != -1:
            val = special_search
        else:
            e1.delete(0, END)
            e1.insert(0, "Invalid input!")
            return

    pre_search_page = pre_search(val)
    curr_page = pre_search_page if pre_search_page != -1 else manager.get_page_number(val)
    show_page()


def special_number_search(search_val):
    lval = search_val.lower()
    if lval == 'pi':
        with open('PI.txt', 'r') as file:
            return file.read()
    elif lval == 'sqrt(2)' or lval == 'sqrt 2' or lval == 'square root of 2':
        with open('sqrt2.txt', 'r') as file:
            return file.read()
    return -1


def on_search_enter(val):
    search()


def page_no_update(value):
    global curr_page, page_no_value
    val = page_no_value.get().replace(',', '')
    if not all([c.isdigit() for c in val]):
        val = '1'
    curr_page = int(val)
    page_no_value.set(format_number(page_no_value.get()))
    show_page()


def show_page():
    global page, curr_page, page_no, e1, page_start_offset
    if curr_page and not any([var1.get(), var2.get(), var3.get(), var4.get()]):
        page.configure(state="normal")
        page.delete(0.0, "end")
        page.configure(state="disabled")
        page_no_value.set(format_number(str(curr_page)))
        return
    if curr_page == 0:
        show_checks()
    else:
        manager.define_chars(var1.get(), var2.get(), var3.get(), var4.get())
        hide_checks()

    if len(e1.get()) == 0:
        manager.clear_search_result()

    part = curr_page // PART_SIZE
    pages_in_part = (curr_page - part * PART_SIZE)
    chapter = pages_in_part // CHAPTER_SIZE
    page_no = pages_in_part - chapter * CHAPTER_SIZE

    page.configure(state="normal")
    page.delete(0.0, "end")
    if curr_page:
        heading = f"The Book of Everything\n" +  \
                    f"{format_scientific_notation(part)}" \
                    f" ｜ {format_scientific_notation(chapter)}" + \
                    f" ｜ {format_number(str(page_no))}\n\n"
        page_start_offset = len(heading)
        content = heading + get_current_page()

        page.insert(0.0, content, 'center')
    else:
        first_page()
    bold_it()
    page.configure(state="disabled")
    page_no_value.set(format_number(str(curr_page)))


def format_scientific_notation(n):
    if len(str(n)) < 9:
        return format_number(str(n))
    sc = str(n)[0] + "." + str(n)[1:3]
    exps = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    return sc + "x10" + ''.join([exps[int(c)] for c in str(len(str(n)) - 1)])


def first_page():
    global page
    page.tag_configure("heading1", font=("David", 18, 'bold'), justify=CENTER)
    page.insert(0.0, f"\n\n\n{book_primary_title}", 'heading1')

    lines = len(book_secondary_title.split('\n'))
    page.tag_configure("heading2", font=("David", 14), justify=CENTER)
    page.insert('end', f"{book_secondary_title}", 'heading2')

    page.insert('end', (10 - lines) * '\n' + "\r", 'heading2')
    if book_primary_title != "The Book of Nothing":
        page.image_create('end', image=img)

    page.tag_configure("heading3", font=("David", 16), justify=CENTER)
    page.insert('end', (10 if book_primary_title != "The Book of Nothing" else 16 - lines) * "\n" + "By\nThis computer", 'heading3')


def get_current_page():
    global curr_page
    return manager.get_page_by_number(curr_page)


def format_number(n_str):
    if len(n_str) < 4:
        return n_str
    new_str = ""
    for i in range(len(n_str)):
        if i and i % 3 == 0 and n_str[- i - 1] != ',':
            new_str += ','
        new_str += n_str[- i - 1]
    return new_str[::-1]


def on_check_change():
    global book_primary_title, book_secondary_title
    primary_title = "The Book of Everything"
    title = ""
    if var1.get():
        title += "\n" if len(title) == 0 else "\nand "
        title += "in English"
    if var2.get():
        title += "\n" if len(title) == 0 else "\nand "
        title += "in Hebrew"
    if var3.get():
        title += "\n" if len(title) == 0 else "\nand "
        title += "about Numbers"
    if var4.get():
        title += "\n" if len(title) == 0 else "\nand "
        title += "with Special Characters"

    if len(title) == 0:
        book_primary_title = "The Book of Nothing"
        book_secondary_title = ""
        show_page()
        return
    book_primary_title = primary_title
    book_secondary_title = title
    show_page()


def bold_it():
    global page, e1
    page.tag_configure("bold", background="yellow")
    if manager.search_result['start_page'] \
            and manager.search_result['start_page'] <= curr_page <= manager.search_result['end_page']:
        start = 0
        end = 0
        if curr_page == manager.search_result['start_page']:
            start = manager.search_result['start_index']
            if curr_page == manager.search_result['end_page']:
                end = manager.search_result['end_index']
            else:
                end = 'end'
        elif curr_page == manager.search_result['end_page']:
            end = manager.search_result['end_index']
        else:
            end = 'end'

        page.tag_add('bold',
                        f"1.0 + {start + page_start_offset} chars",
                        f"1.0 + {end + page_start_offset} chars" if end != 'end' else end)

    for m in re.finditer(re.escape(e1.get()), page.get(0.0, 'end')):
        page.tag_add('bold', f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")


def pre_search(val):
    max_pages = 500 if len(val) < 4 else 30
    for i in range(1, max_pages + 1):
        if val in manager.get_page_by_number(i):
            return i
    return -1


def hide_checks():
    check_frame.grid_forget()


def show_checks():
    check_frame.grid(row=1, column=0, sticky=N)


manager = Manager()
book_primary_title = "The Book of Everything"
book_secondary_title = "\nin English"
curr_page = 0
page_start_offset = 0

master = Tk()
# master.configure(bg='white')
master.title("The Book of Everything")
Label(master, text='Search anything: ').grid(row=0, padx=10, pady=50)
ttk.Button(master, text='Search', width=15, command=search).grid(row=0, column=2, padx=10)


e1 = ttk.Entry(master, width=100)
e1.bind('<Return>', on_search_enter)
e1.grid(row=0, column=1)

check_frame = Frame(master)
# check_frame.grid(row=1, column=0, sticky=N)

settings_label = Label(check_frame, text="Book settings:")
settings_label.grid(row=0, column=0, sticky=W)

var1 = IntVar()
var1.set(1)
check1 = ttk.Checkbutton(check_frame, text="English", variable=var1, command=on_check_change)
check1.grid(row=1, column=0, sticky=W)

var2 = IntVar()
check2 = ttk.Checkbutton(check_frame, text="Hebrew", variable=var2, command=on_check_change)
check2.grid(row=2, column=0, sticky=W)

var3 = IntVar()
check3 = ttk.Checkbutton(check_frame, text="Numbers", variable=var3, command=on_check_change)
check3.grid(row=3, column=0, sticky=W)

var4 = IntVar()
check4 = ttk.Checkbutton(check_frame, text="Other characters", variable=var4, command=on_check_change)
check4.grid(row=4, column=0, sticky=W)


page = Text(master, width=62, height=37, borderwidth=10, wrap=CHAR, pady=30)
page.configure(font=("David", 12))
page.tag_configure('center', justify=CENTER)
page.configure(inactiveselectbackground=page.cget("selectbackground"))
page.grid(row=1, column=1, pady=(0, 20))


img = ImageTk.PhotoImage(Image.open("The book of everything logo.png").resize((120, 120)))
# label = Label(master, image=img)
# label.grid(row=1, column=2, sticky=NE, padx=(0, 30))


page_no_value = StringVar()
page_no = ttk.Entry(master, textvariable=page_no_value, justify=CENTER)
page_no.bind('<Return>', page_no_update)
page_no.grid(row=2, column=1, pady=(0, 20))


nav_frame = Frame(master)
nav_frame.grid(row=3, column=1, pady=(0, 10))
ttk.Button(nav_frame, text="ᐊ", width=5, command=left).grid(row=0, column=0, sticky=W)
ttk.Button(nav_frame, text="ᐅ", width=5, command=right).grid(row=0, column=1, sticky=E)

show_page()

mainloop()
