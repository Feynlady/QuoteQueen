from Session import Session
import tkinter as tk
import tkinter.font as tkfont

'''
    This is the Main Class (our View). Right now, it is rather bland.
    It instantiates a session (our controller). It then listens for the users input and passes this input to the session to compute a reply.
    Connectable to a GUI if anyone wants to do that...
'''
#TODO: BETTER GUI?


class quote_main(object):
    def __init__(self):
        session = Session()
        self.convoGUI(session)


    def convo (self, session):
        print("START")
        print('[QUOTE QUEEN]:', session.current.getPrompt())

        inp = ""
        while inp != "end":
            inp = input('[User]: ')
            print('[QUOTE QUEEN]:', session.reply(inp))

    def convoGUI(self, session):

        def displayInput(conv):
            inp = inputWin.get()
            if inp == "end":
                win.quit()
            conv.insert(tk.INSERT, '[USER]: ', 'username')
            conv.insert(tk.INSERT, inp + "\n", 'userinput')
            reply = session.reply(inp)
            print(type(reply))
            print(reply)
            if type(reply) is tuple:
                quote = reply[0]
                author = reply[2]
                conv_disp.insert('end', "[QUOTE QUEEN]: " + "\n", 'qqname')
                conv_disp.insert('end', "\t" + quote + "\n", 'quote')
                conv_disp.insert('end', "~ " + author + "\n\n", 'author')
            else:
                conv_disp.insert(tk.INSERT, "[QUOTE QUEEN]: " + reply + "\n")
            conv_disp.see(tk.END)

            inputWin.delete(0, "end")

        # main GUI window
        win = tk.Tk()
        win.geometry("700x400")
        win.title('QuoteQueen')

        # conversation display
        conv_disp = tk.Text(win, height=10, width=70)
        conv_disp.configure(font=("Helvetica", 12, "normal"))
        print(tkfont.families())


        conv_disp.pack(fill=tk.BOTH, expand= True, padx=10, pady=5)
        conv_disp.tag_add('quote', '1.0', '1.end')
        conv_disp.tag_config('quote', font='helvetica 12 italic', foreground="blue")  # Set font, size and style
        conv_disp.tag_add('author', '2.0', '2.end')
        conv_disp.tag_config('author', font='helvetica 10 normal', justify='center')
        conv_disp.tag_add('username', '3.0', '3.end')
        conv_disp.tag_config('username', font='helvetica 12 bold', foreground="gray")
        conv_disp.tag_add('userinput', '4.0', '4.end')
        conv_disp.tag_config('userinput', font='helvetica 12 normal', foreground="gray")
        conv_disp.tag_add('qqname', '5.0', '5.end')
        conv_disp.tag_config('qqname', font='helvetica 12 bold')


        # input window
        inp = tk.StringVar()
        inputWin = tk.Entry(win, textvariable=inp, width=10)
        inputWin.configure(font=("Helvetica", 10, "normal"))

        inputWin.pack(fill=tk.BOTH, expand = True, padx=10, pady=5)
        inputWin.bind('<Return>', (lambda event: displayInput(conv_disp)))

        #start conversation
        conv_disp.insert(tk.INSERT, '[QUOTE QUEEN]: ', 'qqname')
        conv_disp.insert(tk.INSERT, session.current.getPrompt() + "\n")

        #update GUI
        win.mainloop()

if __name__ == "__main__":
    qm = quote_main()
