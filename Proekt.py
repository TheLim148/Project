from tkinter import *
from tkinter import ttk
import pickle

class RecipeBook:
    def __init__(self, master):
        self.master = master
        root.title("Recipe Book")
        root.geometry("500x800")

        self.recipe_texts = []
        self.recipe_names = []
        self.current_recipe = 0
        self.pages = 0
        
        try:
            with open("recipes.pickle", "rb") as file:
                self.recipe_texts = pickle.load(file)
        except FileNotFoundError:
            pass
        
        try:
            with open("recipes.pickle", "rb") as file:
                names = pickle.load(file)
                for name in names:
                    lines = name.split("\n")
                    self.recipe_names.append(lines[0])
        except FileNotFoundError:
            pass

        #Фреймы
        root.iconbitmap(default = "Undertale.ico")
        
        frame = Frame(root, height = 800, width = 500, bg = "black")
        frame.place(relx = 0.5, rely = 0.5, relheight = 1, relwidth = 1, anchor = "center")

        frame1 = Frame(root, height = 790, width = 790, bg = "white")
        frame1.place(relx = 0.5, rely = 0.5, relheight = 0.97, relwidth = 0.97, anchor = "center")

        frame2 = Frame(root, height = 780, width = 780, bg = "black")
        frame2.place(relx = 0.5, rely = 0.5, relheight = 0.95, relwidth = 0.95, anchor = "center")

        #Поле для ввода и отображения рецептов
        self.editor = Text(bg = "black", fg = "white", font = "undertale_battle_font 14 normal roman")
        self.editor.place(relx = 0.1, rely = 0.1, relheight = 0.8, relwidth = 0.8)

        #Кнопка сохранения
        self.save_button = ttk.Button(text = "Save", command = self.save_recipe)
        self.save_button.place(relx = 0.5, rely = 0.95, anchor = "s")

        #Кнопка следующего рецепта
        self.next_button = ttk.Button(text = "Next", command = self.next_recipe)
        self.next_button.place(relx = 0.8, rely = 0.95, anchor = "s")
        
        #Кнопка предыдущего рецепта
        self.prev_button = ttk.Button(text = "Prev", command = self.prev_recipe)
        self.prev_button.place(relx = 0.2, rely = 0.95, anchor = "s")

        #Отображение страниц
        self.label = Label(text = self.pages, bg = "black", fg = "white", font = "undertale_battle_font")
        self.label.place(relx = 0.93, rely = 0.05)

        #Отображение всех доступных рецептов
        self.combobox = ttk.Combobox(values = self.recipe_names, state="readonly")
        self.combobox.place(relx = 0.24, rely = 0.05, anchor = "n")
        self.combobox.bind("<<ComboboxSelected>>", self.selected)

    def selected(self, event):
        selection = self.combobox.get()
        for text in self.recipe_texts:
            lines = text.split("\n")
            if lines[0] == selection:
                print("Выбранный рецепт -", text)
                self.editor.delete(1.0, END)
                self.editor.insert(1.0, text)

    def save_recipe(self):
        recipe_text = self.editor.get(1.0, END)
        self.recipe_texts.append(recipe_text)
        with open("recipes.pickle", "wb") as file:
            pickle.dump(self.recipe_texts, file)
        
        try:
            with open("recipes.pickle", "rb") as file:
                names = pickle.load(file)
                for name in names:
                    lines = name.split("\n")
                    self.recipe_names.append(lines[0])
        except FileNotFoundError:
            pass
        
        self.combobox = ttk.Combobox(values = self.recipe_names, state="readonly")
        self.combobox.place(relx = 0.24, rely = 0.05, anchor = "n")
        self.combobox.bind("<<ComboboxSelected>>", self.selected)

    def show_recipe(self):
        self.editor.delete(1.0, END)
        self.editor.insert(INSERT, self.recipe_texts[self.current_recipe])

    def next_recipe(self):
        self.current_recipe = (self.current_recipe + 1) % len(self.recipe_texts)
        self.label["text"] = f"{self.current_recipe+1}"
        self.show_recipe()

    def prev_recipe(self):
        self.current_recipe = (self.current_recipe - 1) % len(self.recipe_texts)
        self.label["text"] = f"{self.current_recipe+1}"
        self.show_recipe()
        
        
if __name__ == "__main__":
    root = Tk()
    app = RecipeBook(root)
    root.mainloop()
