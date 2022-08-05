import tkinter
import tkinter.messagebox
import customtkinter
from PIL import ImageTk,Image
import serial
import random
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import simpleaudio as sa


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = customtkinter.CTk()
root.geometry("640x480") # Defining the base window size and creating window
#root.attributes('-fullscreen', True)
screen_width = root.winfo_screenwidth() # Grabbing screen size data for sizing needs in the future.
screen_height = root.winfo_screenheight()

image_frame = customtkinter.CTkFrame(root, height = screen_width, width = screen_height)
image_frame.pack() # Starting and sending main frame to screen to write on.

# Loading all images from local storage.
my_img1 = ImageTk.PhotoImage(Image.open("Part 1.png"))
my_img2 = ImageTk.PhotoImage(Image.open("Part 2.png"))
my_img3 = ImageTk.PhotoImage(Image.open("Part 3.png"))
my_img4 = ImageTk.PhotoImage(Image.open("Part 4.png"))
my_img5 = ImageTk.PhotoImage(Image.open("Part 5.png"))

# Texted used for each label, each label is bound to each image by the later functions.
label1 = "Check your surroundings. If the person is in a dangerous area DO NOT attempt to move them. \n Call 9-1-1 immediately."
label2 = "Attempt to wake the person up. Shake or make noise to try to wake them. \n If they do not wake continue to the next slide."
label3 = "Try to place the person of the stretcher. If you cannot try and roll them on. \n Find someone to help you place the person on the stretcher."
label4 = "Attach the wrist module to the right wrist of the person. \n Try to place it along the inside of their arm."
label5 = "Strap the person down if possible to the board. \n If they are securely placed then click next."

audio1 = 'Voice1.wav'
audio2 = 'Voice2.wav'
audio3 = 'Voice3.wav'
audio4 = 'Voice4.wav'
audio5 = 'Voice5.wav'

audio_list = [audio1, audio2, audio3, audio4, audio5]
label_list = [label1, label2, label3, label4, label5]
image_list = [my_img1, my_img2, my_img3, my_img4, my_img5]

my_label = customtkinter.CTkLabel(image_frame, image=my_img1)
my_label.place(relx=0.5, rely = 0.5, anchor = tkinter.CENTER)

my_text = customtkinter.CTkLabel(image_frame, text = label1).place(relx = 0.5, rely = 0.75, anchor = tkinter.CENTER)

def create_analytics():
	line = 0
	image_number = 0
	image_frame.destroy()

	display_frame = customtkinter.CTkFrame(root, height = screen_width, width = screen_height, fg_color = 'black')
	display_frame.pack()

	heart_rate_frame = customtkinter.CTkFrame(display_frame, height = screen_height/2, width = screen_width/2, fg_color= 'red')
	heart_rate_frame.grid(row = 0, column = 0)
	heart_rate_frame.pack_propagate(0)

	heart_rate_label = customtkinter.CTkLabel(heart_rate_frame, text = "Heart Rate Value", text_font = ("Times New Roman", 28), text_color = "black")
	heart_rate_label.pack()

	piston_speed_frame = customtkinter.CTkFrame(display_frame, height = screen_height/2, width = screen_width/2, fg_color= 'green')
	piston_speed_frame.grid(row = 0, column = 1)
	piston_speed_frame.pack_propagate(0)

	piston_speed_label = customtkinter.CTkLabel(piston_speed_frame, text = "Piston Speed (RPM)", text_font = ("Times New Roman", 28), text_color = "black")
	piston_speed_label.pack()

	heart_rate_plot = customtkinter.CTkFrame(display_frame, height = screen_height/2, width = screen_width/2, fg_color= 'white')
	heart_rate_plot.grid(row = 1, column = 0)
	heart_rate_plot.pack_propagate(0)

	heart_rate_plot_label = customtkinter.CTkLabel(heart_rate_plot, text = "Heart Rate Graph", text_font = ("Times New Roman", 28), text_color = "black")
	heart_rate_plot_label.pack()

	piston_force_frame = customtkinter.CTkFrame(display_frame, height = screen_height/2, width = screen_width/2, fg_color= 'purple')
	piston_force_frame.grid(row = 1, column = 1)
	piston_force_frame.pack_propagate(0)

	piston_force_label = customtkinter.CTkLabel(piston_force_frame, text = "Piston Force (lbs-ft)", text_font = ("Times New Roman", 28), text_color = "black")
	piston_force_label.pack()

	heart_val = 0
	heart_rate = customtkinter.CTkLabel(heart_rate_frame, text = heart_val, text_font = ("Times New Roman", 100))
	heart_rate.place(relx=0.5, rely = 0.5, anchor = tkinter.CENTER)

	piston_speed = customtkinter.CTkLabel(piston_speed_frame, text = "0", text_font = ("Times New Roman", 100))
	piston_speed.place(relx = 0.5, rely= 0.5, anchor = tkinter.CENTER)

	xar = []
	yar = []
	xar1 = []
	yar1 = []
	
	force_fig = plt.figure(figsize=(2, 1.5), dpi=100)
	ax2 = force_fig.add_subplot(1, 1, 1)
	ax2.set_ylim(0,200)
	line2, = ax2.plot(xar1, yar1, 'b', marker='o')

	heart_rate_fig = plt.figure(figsize=(2, 1.5), dpi=100)
	ax1 = heart_rate_fig.add_subplot(1, 1, 1)
	ax1.set_ylim(0, 100)
	line, = ax1.plot(xar, yar, 'r', marker='o')

	if __name__ == '__main__':
		ser = serial.Serial('COM4', 9600, timeout=1)
		ser.reset_input_buffer()
	
	global xcount
	global piston_count

	def animate(xcount):
		output = ser.readline().decode('UTF-8').rstrip()
		if output.isdigit():
			print(int(output))
			data = int(output)
			yar.append(data)
			xar.append(xcount)
			line.set_data(xar, yar)
			xcount = xcount + 1
			ax1.set_ylim(0, max(yar))
			ax1.set_xlim(0, xcount)
			heart_rate.set_text(str(data))
			piston_speed.set_text(str(random.randint(100,120)))
			
	def animate_force(piston_count)	:
		xar1.append(piston_count)
		yar1.append(random.randint(0, 200))
		line2.set_data(xar1,yar1)
		ax2.set_xlim(0, piston_count)
		

	heart_rate_canvas = FigureCanvasTkAgg(heart_rate_fig, master=heart_rate_plot) # A tk.DrawingArea.
	heart_rate_canvas.draw()

	force_canvas = FigureCanvasTkAgg(force_fig, master=piston_force_frame)
	force_canvas.draw()

	force_canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
	heart_rate_canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

	heart_rate_update = animation.FuncAnimation(heart_rate_fig, animate, interval = 1000, blit = False)
	force_update = animation.FuncAnimation(force_fig, animate_force, interval = 1000, blit = False)

	force_update._start()
	heart_rate_update._start()

	root.update_idletasks()

def forward(image_number):
	global my_label
	global button_forward
	global button_back
	
	if  image_number == len(image_list) + 1:
		answer = tkinter.messagebox.askyesno(message = "Are you and the patient ready to start the system?")
		if (answer == True):
			create_analytics()
		else:
			back(4)

	else:
		my_label.destroy()
		my_label = customtkinter.CTkLabel(image_frame, image=image_list[image_number - 1])
		my_label.place(relx=0.5, rely = 0.5, anchor = tkinter.CENTER)

		button_forward = customtkinter.CTkButton(image_frame, text=">>", height = screen_height, width = (screen_width/10), text_font = ("Times New Roman", 25), command=lambda: forward(image_number+1))
		button_back = customtkinter.CTkButton(image_frame, text="<<", height = screen_height, width = (screen_width/10), text_font = ("Times New Roman", 25), command=lambda: back(image_number-1))

		my_text = customtkinter.CTkLabel(image_frame, text = label_list[image_number - 1])
		my_text.place(relx=0.5, rely = 0.75, anchor = tkinter.CENTER)

		my_audio = sa.WaveObject.from_wave_file(audio_list[image_number - 1])
		my_audio.play()
		#if forward.has_been_called or back.has_been_called:
			#my_audio.stop()

		button_forward.place(relx = (5/6), rely = 0)
		button_back.place(relx = 0, rely = 0)

		forward.has_been_called = True
		pass
forward.has_been_called = False

def back(image_number):
	global my_label
	global button_forward
	global button_back

	my_label.destroy()
	my_label = customtkinter.CTkLabel(image_frame, image=image_list[image_number-1])
	my_label.place(relx=0.5, rely = 0.5, anchor = tkinter.CENTER)

	button_forward = customtkinter.CTkButton(image_frame, text=">>", height = screen_width, width = (screen_width/10), text_font = ("Times New Roman", 25), command=lambda: forward(image_number+1))
	button_back = customtkinter.CTkButton(image_frame, text="<<", height = screen_width, width = (screen_width/10), text_font = ("Times New Roman", 25), command=lambda: back(image_number-1))

	my_text = customtkinter.CTkLabel(image_frame, text = label_list[image_number - 1])
	my_text.place(relx=0.5, rely = 0.75, anchor = tkinter.CENTER)
	
	my_audio = sa.WaveObject.from_wave_file(audio_list[image_number - 1])
	my_audio.play()
	#if forward.has_been_called or back.has_been_called:
			#sa.stop()

	if image_number == 1:
		button_back = customtkinter.CTkButton(image_frame, text="<<", state= tkinter.DISABLED, text_font = ("Times New Roman", 25))

	button_forward.place(relx = (5/6), rely = 0)
	button_back.place(relx = 0, rely = 0)
	back.has_been_called = True
	pass
back.has_been_called = False
	

button_back = customtkinter.CTkButton(image_frame, text="<<", height = screen_height, width = (screen_width/10), text_font = ("Times New Roman", 25), command=back, state= tkinter.DISABLED)
button_exit = customtkinter.CTkButton(image_frame, text="Exit Program", command=root.quit)
button_forward = customtkinter.CTkButton(image_frame, text=">>", height = screen_height, width = (screen_width/10), text_font = ("Times New Roman", 25), command=lambda: forward(2))

button_back.place(relx = 0, rely = 0)
button_exit.place(relx = 0.5, rely = 0.90)
button_forward.place(relx = (5/6), rely = 0)

my_audio = sa.WaveObject.from_wave_file(audio1)
my_audio.play()
#if forward.has_been_called:
	#my_audio.stop()

root.mainloop()

