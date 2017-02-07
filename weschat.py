from weschat_api import WesChat
import tkinter

window = tkinter.Tk()
window.title("WesChat")

wc = None

def connect():
    global wc, hostEntry, passEntry
    wc = WesChat(hostEntry.get(), passEntry.get())

def post(blah=None):
    global wc, postEntry
    wc.post(postEntry.get())
    postEntry.delete(0, tkinter.END)

connectBtn = tkinter.Button(window, text="Connect", command=connect,
                            font=("Courier New", 12))
postBtn = tkinter.Button(window, text="Post", command=post,
                         font=("Courier New", 12))

hostLabel = tkinter.Label(window, text="Server IP:", font=("Courier New", 12))
passLabel = tkinter.Label(window, text="Password:", font=("Courier New", 12))

hostEntry = tkinter.Entry(window, font=("Courier New", 12))
passEntry = tkinter.Entry(window, font=("Courier New", 12), show="*")
postEntry = tkinter.Entry(window, font=("Courier New", 12))

msgLabel = tkinter.Text(window, font=("Courier New", 12), wrap=tkinter.WORD)

connectBtn.grid(row=0, column=2, sticky=tkinter.E+tkinter.N)
postBtn.grid(row=3, column=2, sticky=tkinter.E, rowspan=2)

hostLabel.grid(row=0, column=0, sticky=tkinter.W+tkinter.N)
passLabel.grid(row=1, column=0, sticky=tkinter.W)

hostEntry.grid(row=0, column=1, sticky=tkinter.W+tkinter.E+tkinter.N)
passEntry.grid(row=1, column=1, sticky=tkinter.W+tkinter.E+tkinter.N)
postEntry.bind("<Return>", post)
postEntry.grid(row=3, column=0, columnspan=2, sticky=tkinter.W+tkinter.E)

msgLabel.grid(row=2, column=0, columnspan=3, sticky=tkinter.W)

window.rowconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

while True:
    window.update()
    try:
        msgLabel.insert(tkinter.END, wc.get_messages())
    except:
        pass
    msgLabel.see(tkinter.END)
