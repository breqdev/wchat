from weschat_api import WesChat
import tkinter

window = tkinter.Tk()
window.title("WesChat")

wc = None

def connect():
    global wc, hostEntry
    wc = WesChat(hostEntry.get(), "Ni")

def post(blah=None):
    global wc, postEntry
    wc.post(postEntry.get())
    postEntry.delete(0, tkinter.END)

connectBtn = tkinter.Button(window, text="Connect", command=connect)
postBtn = tkinter.Button(window, text="Post", command=post)
hostEntry = tkinter.Entry(window)
postEntry = tkinter.Entry(window)
msgLabel = tkinter.Text(window, font=("Courier New", 12), wrap=tkinter.WORD)
connectBtn.grid(row=0, column=1, sticky=tkinter.E+tkinter.N)
postBtn.grid(row=2, column=1, sticky=tkinter.E)
hostEntry.grid(row=0, column=0, sticky=tkinter.W+tkinter.E+tkinter.N)
postEntry.bind("<Return>", post)
postEntry.grid(row=2, column=0, sticky=tkinter.W+tkinter.E)
msgLabel.grid(row=1, column=0, columnspan=2, sticky=tkinter.W)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

while True:
    window.update()
    try:
        msgLabel.insert(tkinter.END, wc.get_messages())
    except:
        pass
    msgLabel.see(tkinter.END)
