import tkinter
board = tkinter.Tk()
canvas = tkinter.Canvas(board, width=500, height=500)
canvas.pack()
canvas.create_rectangle(50, 25, 150, 75, fill="red")
board.mainloop()

