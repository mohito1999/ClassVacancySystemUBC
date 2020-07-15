import tkinter as tk
from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import time
#from twisted.internet.task import LoopingCall
#from twisted.internet import reactor
import threading


class App(tk.Frame):
    def __init__(self, title, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title
        

        self.class_id = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(self, text="Enter your class URL here", background='#002145', fg="white", font='Helvetica 12 bold').grid(column=0, row=0)
        tk.Entry(self, textvariable=self.class_id, highlightbackground='#002145').grid(column = 1, row=0)
        tk.Label(self, text="Enter your email address here", background='#002145', fg="white", font='Helvetica 12 bold').grid(column=0, row=1)
        tk.Entry(self, textvariable=self.email, highlightbackground='#002145').grid(column = 1, row=1)
        tk.Label(self, text="Enter your password here", background='#002145', fg="white", font='Helvetica 12 bold').grid(column=0, row=2)
        tk.Entry(self, textvariable=self.password, show="*", highlightbackground='#002145').grid(column = 1, row=2)
        #tk.Label(self, text="Please keep this window open for regular checks.\nClose window when you have registered in desired class.").grid(column=0, row=4)

        tk.Button(self, text="Initialize Details", command=self.enter_var, background='#002145', highlightbackground='#002145').grid(column=0, row=3)
        tk.Button(self, text="Begin Monitoring Class", command=self.interval, background='#002145', highlightbackground='#002145').grid(column=1, row=3)
        

    def enter_var(self):
        self.class_entry = self.class_id.get()
        self.email_entry = self.email.get()
        self.password_entry = self.password.get()

        
    
    def send_email(self):
        while True:
            url = requests.get(self.class_entry)
            html_str = url.text
            full_not = BeautifulSoup(html_str, 'html.parser')
            tr_tag = full_not.find_all('tr')
            tr_tags = []
            for tag in tr_tag:
                tr_tags.append(tag.get_text())
            for i in range(len(tr_tags)):
                if "Total Seats Remaining" in tr_tags[i]:
                    rel_str = tr_tags[i]
            for i in range(len(rel_str)):
                if rel_str[i] == ':' and rel_str[i + 1] == "0":
                    seats_remaining = 0
                elif rel_str[i] == ':' and int(rel_str[i + 1]) > 0:
                    seats_remaining = 1
            fromaddr = self.email_entry
            toaddr = self.email_entry
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "A Seat Has Opened Up!"
            body = "Go To " + self.class_entry
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, self.password_entry)
            text = msg.as_string()
            if seats_remaining == 1:
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
            time.sleep(60)
            continue
        

    def interval(self):
        t = threading.Thread(target=self.send_email)
        t.daemon = True #ends thread when there are no other non-thread scripts active. Allows for red close button to terminate program.
        t.start()
        
            

root = tk.Tk()
app = App(title = "Class Vacancy System", master=root)
app.configure(background='#002145')
app.master.title("Class Vacancy System")
app.mainloop()
root.quit()
