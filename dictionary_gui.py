from tkinter import END, VERTICAL, WORD, Button, Entry, Frame, Listbox, Scrollbar, StringVar, Tk
from tkinter.scrolledtext import ScrolledText
# from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Scrollbar 
import requests


class dictionary():
    def __init__(self):
        self.MainScreen()
       

    def list_dict(self,list,text):
        temp={}
        count=0
        for i in list:
            count+=1
            temp.update({f"{text}{count}":i})
        return temp
    def MainScreen(self):
        self.main_screen=Tk()
        self.main_screen.title("Dictionary")
        width=self.main_screen.winfo_screenwidth()//2
        height=self.main_screen.winfo_screenheight()//2
        self.main_screen.geometry(f"{width}x{height}+{width//2}+{height//2}")
        self.main_screen.config(bg="light blue")
        self.main_screen.resizable(0,0)
        self.CreateEntrys()
        self.CreateButtons()
        self.CreateListbox()
        self.CreateTextarea()
        self.main_screen.mainloop()

    def CreateEntrys(self):
        self.user_in=StringVar()
        self.search_box=Entry(self.main_screen,textvariable=self.user_in,font=("Arial",18))
        self.search_box.place(x=50,y=30,width=840,height=50)
    
        self.search_box.bind(f"<KeyRelease>",self.key_bind)

    def update(self,data):
	
        # clear previous data
        self.list_box.delete(0, 'end')

        # put new data
        for item in data:
            self.list_box.insert('end', item)

    def CreateButtons(self):
        Button(self.main_screen,text="Search",command=self.SearchWord).place(x=900,y=30,width=80,height=50)

    def ListboxSelect(self,event):
        selection=self.list_box.curselection()
        text=self.list_box.get(selection)
        self.OnlineSearch(text)
    def key_bind(self,event):
            self.word_list.sort()
            with open(r"word_list.txt","r")as file:
                self.word_list=eval(file.read())
                self.word_list.sort()
                file.close()
            value = event.widget.get()
            
            # get data from l
            if value == '':
                data = self.word_list
            else:
                data = []
                for item in self.word_list:
                    if value.lower() in item.lower():
                        data.append(item)
                        self.list_box.delete(0,END)
                        for i in data:
                            self.list_box.insert(END,i)	
        

    def CreateListbox(self):
        my_frame=Frame(self.main_screen)
        scrollbar=Scrollbar(my_frame,orient=VERTICAL)
        self.list_box=Listbox(my_frame,width=50,height=23,yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.list_box.yview)
        scrollbar.pack(side="right",fill="y")
        my_frame.place(x=30,y=100)  
        self.list_box.pack()
        with open(r"word_list.txt","r")as file:
            self.word_list=eval(file.read())
            self.word_list.sort()
            file.close()
        for i in self.word_list:
            i=i.lower()
            self.list_box.insert(END,i)
        self.list_box.bind("<Double-1>",self.ListboxSelect)
    
    def CreateTextarea(self):
        self.text_area=ScrolledText(self.main_screen,width=75,height=23,wrap=WORD)
        self.text_area.config(state="disabled")
        self.text_area.place(x=360,y=100)

    def SearchWord(self):
        self.text_area.delete("1.0",END)
        in_word=self.user_in.get()
        in_word=in_word.lower()
        if in_word=="":
            pass
        else:
            self.OnlineSearch(in_word)
    def OnlineSearch(self,word):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0",END)
        search=f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        result=requests.get(search)
        rawdata=result.json()
        if 'message' in rawdata:
            self.text_area.insert(END,"We couldn't find definitions for the word you were looking for ")
        else:
            if word in self.word_list:
                pass
            else:
                with open(r"word_list.txt","r")as file:
                    temp=file.read()
                    a=temp.replace("]",f",\"{word}\"]")
                    file.close()
                with open(r"word_list.txt","w")as file:
                    file.write(a)
                    file.close()

            dict_data=self.list_dict(rawdata,"explanation")
            
            self.text_area.insert(END,word)
            for i in dict_data:
                if 'phonetic' in dict_data[i]:
                    self.text_area.insert(END,f"\n{dict_data[i]['phonetic']}")  
                meaning_data=self.list_dict(dict_data[i]['meanings'],"meaning")
                for j in meaning_data:
                    self.text_area.insert(END,f"\n\n\t\t\t{{{meaning_data[j]['partOfSpeech']}}}")
                    definition_data=self.list_dict(meaning_data[j]['definitions'],"definition")
                    count=0
                    self.text_area.insert(END,f"\n\nDefinitions")
                    for k in definition_data:
                        if 'definition' in definition_data[k]:
                            count+=1
                            self.text_area.insert(END,f"\n({count}){definition_data[k]['definition']}")
                        eg='example'
                        if eg in definition_data[k]:
                            self.text_area.insert(END,f"\n eg. {definition_data[k]['example']}")

        self.text_area.config(state='disabled')
        

dictionary()