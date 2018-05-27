import tkinter as tk
import os
import tkinter.font as tkFont

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
   base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

import graphic_interface as g
import cert_check_interface as cc
import destroy_interface as di


def start_this_program(true_if_inv, true_if_cert, parent):
	pass
	if true_if_inv:
		g.run_gui(parent)
		cc.run_gui(parent)
	elif true_if_cert:
		cc.run_gui(parent)
	else:
		di.run_gui(parent)


if __name__ == "__main__":
	# Show button for inventory -> graphic_interface.py
	# Show button for cert check -> cert_chec1_interface.py
	# Show a picture of cerebro
	root = tk.Tk()
	root.iconbitmap(resource_path('img/icon.ico'))
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.geometry("{}x{}+0+0".format(500, 380))
	root.wm_title("Cerebot")
	mainframe = tk.Frame(master=root, background = "#9BE7FF")
	mainframe.pack(side="top", fill="both", expand=True)

	helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')
	
	inv = tk.Button(mainframe, text="Inventory", padx='10', pady='10', font = helv36, borderwidth='5' , background = "#FF4435")
	inv["command"] = lambda: start_this_program(True, False, root)
	inv.pack(side="top")

	cert = tk.Button(mainframe, text="Certification Check", padx='10', pady='10', font = helv36, borderwidth='5', background = "#005EC4")
	cert["command"] = lambda: start_this_program(False, True, root)
	cert.pack(side='top')

	destroy = tk.Button(mainframe, text="Destruction", padx='10', pady='10', font = helv36, borderwidth='5', background = "#004F2E")
	destroy["command"] = lambda: start_this_program(False, False, root)
	destroy.pack(side='top')

	#the_image = tk.PhotoImage(file=resource_path('img/cerebot.gif'))
	#banner = tk.Label(image=the_image)
	#banner.pack(side="top")

	mainframe.mainloop()
