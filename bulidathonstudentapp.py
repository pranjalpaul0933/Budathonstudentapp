from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
import json, os

# -------------------- File setup --------------------
DATA_DIR = "rc_data"
os.makedirs(DATA_DIR, exist_ok=True)
CRED_FILE = os.path.join(DATA_DIR, "teachers.json")
STUD_FILE = os.path.join(DATA_DIR, "students.json")

if not os.path.exists(CRED_FILE):
    with open(CRED_FILE, "w") as f:
        json.dump({}, f)
if not os.path.exists(STUD_FILE):
    with open(STUD_FILE, "w") as f:
        json.dump([], f)

# -------------------- KV Layout --------------------
KV = '''
ScreenManager:
    LoginScreen:
    SignupScreen:
    HomeScreen:

<LoginScreen>:
    name: "login"
    MDFloatLayout:
        md_bg_color: 0.95,0.95,0.95,1
        MDLabel:
            text: "Teacher Login"
            halign: "center"
            pos_hint: {"center_y": 0.9}
            font_style: "H4"
        MDTextField:
            id: username
            hint_text: "Username"
            pos_hint: {"center_x": 0.5, "center_y": 0.65}
            size_hint_x: 0.8
        MDTextField:
            id: password
            hint_text: "Password"
            pos_hint: {"center_x": 0.5, "center_y": 0.52}
            size_hint_x: 0.8
            password: True
        MDFillRoundFlatIconButton:
            text: "Login  "
            pos_hint: {"center_x": 0.5, "center_y": 0.38}
            md_bg_color: 0,0.6,0.9,1
            on_release: app.login(username.text, password.text)
        MDFlatButton:
            text: "No Account? Signup"
            pos_hint: {"center_x": 0.5, "center_y": 0.28}
            on_release: app.change_screen("signup")

<SignupScreen>:
    name: "signup"
    MDFloatLayout:
        md_bg_color: 0.95,0.95,0.95,1
        MDLabel:
            text: "Teacher Signup"
            halign: "center"
            pos_hint: {"center_y": 0.9}
            font_style: "H4"
        MDTextField:
            id: username
            hint_text: "New Username"
            pos_hint: {"center_x": 0.5, "center_y": 0.65}
            size_hint_x: 0.8
        MDTextField:
            id: password
            hint_text: "New Password"
            pos_hint: {"center_x": 0.5, "center_y": 0.52}
            size_hint_x: 0.8
            password: True
        MDFillRoundFlatIconButton:
            text: "Create Account"
            pos_hint: {"center_x": 0.5, "center_y": 0.38}
            md_bg_color: 0,0.8,0.4,1
            on_release: app.signup(username.text, password.text)
        MDFlatButton:
            text: "Back to Login"
            pos_hint: {"center_x": 0.5, "center_y": 0.28}
            on_release: app.change_screen("login")

<HomeScreen>:
    name: "home"
    MDFloatLayout:
        md_bg_color: 0.95,0.95,1,1
        MDLabel:
            text: "Teacher Smart Dashboard"
            halign: "center"
            pos_hint: {"center_y":0.98}
            font_style: "H5"
        MDBoxLayout:
            id: dashboard
            orientation: "vertical"
            adaptive_height: True
            size_hint_y: None
            pos_hint: {"center_x": 0.5, "top": 0.95}
        BoxLayout:
            id: content_area
            orientation: "vertical"
            size_hint: 1,0.7
            pos_hint: {"x":0, "y":0.05}
            padding: dp(5)
'''

# -------------------- Screens --------------------
class LoginScreen(Screen): pass
class SignupScreen(Screen): pass
class HomeScreen(Screen): pass

# -------------------- App Class --------------------
class ReportCardMDApp(MDApp):
    def build(self):
        self.title = "Report Card System"
        self.theme_cls.primary_palette = "Blue"
        self.subject_inputs = []
        return Builder.load_string(KV)

    # -------------------- Dialog --------------------
    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    # -------------------- Screen Change --------------------
    def change_screen(self, name):
        self.root.current = name

    # -------------------- Login / Signup --------------------
    def login(self, user, pwd):
        with open(CRED_FILE) as f:
            creds = json.load(f)
    
        if user in creds and creds[user] == pwd:
            # Store the current teacher name
            self.current_teacher = user
    
            # Create or use a separate file for each teacher's students
            self.student_file = os.path.join(DATA_DIR, f"students_{user}.json")
    
            # Create empty file if doesn't exist
            if not os.path.exists(self.student_file):
                with open(self.student_file, "w") as f:
                    json.dump([], f)
    
            # Proceed to home screen
            self.change_screen("home")
            self.show_dashboard()
    
        else:
            self.show_dialog("Login Failed", "Invalid username or password")
    
    
    def signup(self, user, pwd):
        if not user or not pwd:
            self.show_dialog("Error", "Fields cannot be empty!")
            return
    
        with open(CRED_FILE) as f:
            creds = json.load(f)
    
        if user in creds:
            self.show_dialog("Error", "User already exists!")
        else:
            creds[user] = pwd
            with open(CRED_FILE, "w") as f:
                json.dump(creds, f)
    
            # Create separate student file for new teacher
            student_file = os.path.join(DATA_DIR, f"students_{user}.json")
            if not os.path.exists(student_file):
                with open(student_file, "w") as f:
                    json.dump([], f)
    
            self.show_dialog("Success", "Account created! Now login.")
            self.change_screen("login")
    # -------------------- Dashboard --------------------
    from kivymd.uix.button import MDFillRoundFlatIconButton
    from kivymd.uix.button import MDFillRoundFlatIconButton
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.boxlayout import BoxLayout
    from kivymd.uix.label import MDLabel
    from kivy.metrics import dp
    
    def show_dashboard(self):
        home = self.root.get_screen("home")
        content = home.ids.content_area
        dashboard = home.ids.dashboard
        dashboard.opacity = 1
        dashboard.disabled = False
        dashboard.size_hint_y = 0.25
        dashboard.height = dp(200)
        content.clear_widgets()
        
        
        dashboard = home.ids.dashboard  
        dashboard.opacity = 1  
        dashboard.disabled = False  
        dashboard.clear_widgets()  
        
        # -------------------- Main Layout --------------------  
        main_layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(30), size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})  
        
        # -------------------- Grid Layout for Buttons --------------------  
        grid = GridLayout(
            cols=2,
            spacing=[dp(30), dp(60)],
            padding=[dp(0), dp(10), dp(20), dp(10)],
            size_hint=(1, 1),  
        )
        grid.bind(minimum_height=grid.setter("height"))  
        
        # -------------------- Buttons with Icons --------------------  
        buttons = [  
            ("Add Student", "account-plus", self.add_student_ui),  
            ("Display Students", "account-multiple", self.display_students),  
            ("Search Student", "magnify", self.search_student),  
            ("Update Student", "account-edit", self.update_student_ui),  
            ("Delete Student", "delete", self.delete_student),  
            ("Rank List", "format-list-numbered", self.rank_list),  
            ("AI Insights", "robot-excited", self.ai_insights),
("Prediction Mode", "chart-line", self.prediction_mode),
            ("Emotional AI", "heart-pulse", self.emotional_dashboard),
            ("AI Mentor", "robot", self.ai_mentor_mode),
            ("Career Map", "compass", self.dream_path_visualizer),
             ("GK Questions", "lightbulb-question-outline", self.gk_quiz_mode),
            ("Topper", "star", self.show_topper),  
            ("Class Stats", "chart-bar", self.class_stats),  
            ("New Login", "login", lambda: self.change_screen("login")),  
           ("Logout", "logout", lambda x=None: self.close_app())
        ]  
        
        for text, icon, func in buttons:  
            btn = MDFillRoundFlatIconButton(  
                text=text,  
                icon=icon,  
                on_release=lambda x, f=func: f(),  
                size_hint=(1, None),  
                md_bg_color=(  
                    (0.3, 0.8, 0.3, 1)  
                    if text == "New Login"  
                    else (1, 0.3, 0.3, 1) if text == "Logout"  
                    else (0.2, 0.6, 1, 1)  
                ),  
            )  
            grid.add_widget(btn)  
        
        main_layout.add_widget(grid)  
        dashboard.add_widget(main_layout)
        
    def close_app(self):
        import sys
        from kivy.app import App
    
        print("Logging out — closing app completely...")
        App.get_running_app().stop()  
        sys.exit(0)                   # Exit Python process
        
        
    # -------------------- Add Student --------------------
    def add_student_ui(self):
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        dashboard.opacity = 0
        dashboard.disabled = True
        dashboard.size_hint_y = None
        dashboard.height = 0
        content.clear_widgets()

        main_layout = BoxLayout(orientation='vertical', spacing=dp(2), padding=dp(2))
        scroll = ScrollView(size_hint=(1, 5))
        self.grid = GridLayout(cols=2, spacing=dp(5), padding=dp(5), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.student_fields = {}
        fields = ["Name", "Class", "Roll Number", "Father's Name", "Mother's Name",
                  "Blood Group", "Phone Number", "Address", "Extra Criteria", "Number of Subjects"]

        for f in fields:
            self.grid.add_widget(MDLabel(text=f))
            txt = TextInput(multiline=False, size_hint_y=None, height=dp(50))
            self.grid.add_widget(txt)
            self.student_fields[f] = txt

        scroll.add_widget(self.grid)
        main_layout.add_widget(scroll)

        btn_layout = GridLayout(cols=2, size_hint=(1, 0.45), spacing=dp(80), pos_hint={"center_x": 0.5},padding=dp(9))
        gen_btn = MDFillRoundFlatIconButton(text="Generate Subjects", md_bg_color=(0,0.6,0.9,1))
        gen_btn.bind(on_release=lambda x: self.generate_subject_fields())
        back_btn = MDFillRoundFlatIconButton(text="Back to Dashboard", md_bg_color=(1,0,0,1))
        back_btn.bind(on_release=lambda x: self.show_dashboard())
        btn_layout.add_widget(gen_btn)
        btn_layout.add_widget(back_btn)
        main_layout.add_widget(btn_layout)

        content.add_widget(main_layout)

    def generate_subject_fields(self):
        try:
            n = int(self.student_fields["Number of Subjects"].text)
            if n <= 0:
                self.show_dialog("Error","Enter valid number of subjects")
                return
        except:
            self.show_dialog("Error","Enter valid number of subjects")
            return

        if hasattr(self, "subject_inputs") and self.subject_inputs:
            for w1, w2 in self.subject_inputs:
                self.grid.remove_widget(w1)
                self.grid.remove_widget(w2)
        self.subject_inputs = []

        for i in range(1, n+1):
            sub_label = MDLabel(text=f"Subject {i}")
            sub_input = TextInput(multiline=False, size_hint_y=None, height=dp(40))
            mark_label = MDLabel(text=f"Marks {i}")
            mark_input = TextInput(multiline=False, input_filter="int", size_hint_y=None, height=dp(40))
            self.grid.add_widget(sub_label)
            self.grid.add_widget(sub_input)
            self.grid.add_widget(mark_label)
            self.grid.add_widget(mark_input)
            self.subject_inputs.append((sub_input, mark_input))

        content = self.root.get_screen("home").ids.content_area
        if hasattr(self, "save_btn"):
            content.remove_widget(self.save_btn)
        self.save_btn = MDFillRoundFlatIconButton(text="Save Student", md_bg_color=(0,0.7,0.3,1), size_hint=(0.5, None), padding=dp(1), pos_hint={"center_x": 0.5}, height=dp(30))
        self.save_btn.bind(on_release=lambda x: self.save_student())
        content.add_widget(self.save_btn)

    def save_student(self):
        student = {k:v.text for k,v in self.student_fields.items() if k!="Number of Subjects"}
        student["subjects"] = [sub.text for sub, mark in self.subject_inputs]
        student["marks"] = [int(mark.text) if mark.text.isdigit() else 0 for sub, mark in self.subject_inputs]

        with open(self.student_file) as f:
            data = json.load(f)
        data.append(student)
        with open(self.student_file, "w") as f:
            json.dump(data, f, indent=2)

        self.show_dialog("Success", f"Student '{student['Name']}' saved successfully!")
        self.show_dashboard()

            #-------------------- Display Students --------------------
    
    def display_students(self):  
        home = self.root.get_screen("home")  
        dashboard = home.ids.dashboard  
        content = home.ids.content_area  
    
        dashboard.opacity = 0  
        dashboard.disabled = True  
        content.clear_widgets()  
    
        with open(self.student_file) as f:
            data = json.load(f) 
    
        if not data:  
            self.show_dialog("Info","No students found!")  
            self.show_dashboard()  
            return  
    
        scroll_vert = ScrollView(size_hint=(1,0.1))  
        outer_grid = GridLayout(cols=1, spacing=dp(15), padding=dp(10), size_hint_y=None)  
        outer_grid.bind(minimum_height=outer_grid.setter('height'))  
    
        for s in data:  
            card = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10), spacing=dp(5))  
            card.height = dp(80 + 40*len(s.get("subjects",[])))  
    
            # Basic Info  
            info_grid = GridLayout(cols=2, size_hint_y=None, height=dp(80))  
            info_grid.add_widget(MDLabel(text=f"[b]Name:[/b] {s.get('Name','')}", markup=True))  
            info_grid.add_widget(MDLabel(text=f"[b]Class:[/b] {s.get('Class','')}", markup=True))  
            info_grid.add_widget(MDLabel(text=f"[b]Roll:[/b] {s.get('Roll Number','')}", markup=True))  
            info_grid.add_widget(MDLabel(text=f"[b]Phone:[/b] {s.get('Phone Number','')}", markup=True))  
            info_grid.add_widget(MDLabel(text=f"[b]Father:[/b] {s.get("Father's Name",'')}", markup=True))  
            info_grid.add_widget(MDLabel(text=f"[b]Mother:[/b] {s.get("Mother's Name",'')}", markup=True))  
            info_grid.add_widget(MDLabel(text=f"[b]Blood Group:[/b] {s.get('Blood Group','')}", markup=True))  
            info_grid.add_widget(MDLabel(text=f"[b]Address:[/b] {s.get('Address','')}", markup=True))  
            card.add_widget(info_grid)  
    
            # Subjects + Marks 
            scroll_h = ScrollView(size_hint=(1,None), size=(dp(300), dp(40 + 30*len(s.get("subjects",[])))), do_scroll_x=True, do_scroll_y=False)  
            subj_grid = GridLayout(cols=len(s.get("subjects",[]))*2, size_hint_x=None, height=dp(40))  
            subj_grid.bind(minimum_width=subj_grid.setter('width'))  
    
            for sub, mark in zip(s.get("subjects",[]), s.get("marks",[])):  
                lbl_sub = MDLabel(text=f"[b]{sub}[/b]", markup=True, size_hint_x=None, width=dp(120))  
                lbl_mark = MDLabel(text=str(mark), size_hint_x=None, width=dp(60))  
                subj_grid.add_widget(lbl_sub)  
                subj_grid.add_widget(lbl_mark)  
    
            scroll_h.add_widget(subj_grid)  
            card.add_widget(scroll_h)  
            outer_grid.add_widget(card)  
    
        scroll_vert.add_widget(outer_grid)  
        content.add_widget(scroll_vert)  
    
        back_btn = MDFillRoundFlatIconButton(text="Back to Dashboard", size_hint=(0.5,None), pos_hint={"center_x": 0.5},height=dp(50), md_bg_color=(1,0,0,1))  
        back_btn.bind(on_release=lambda x: self.show_dashboard())  
        content.add_widget(back_btn)


            
    # ---------- Update Student ----------
    def update_student_ui(self):
        home=self.root.get_screen("home")
        dashboard=home.ids.dashboard
        content=home.ids.content_area
        dashboard.opacity=0
        dashboard.disabled=True
        content.clear_widgets()
        layout = BoxLayout(
        orientation='vertical',
        spacing=dp(15),
        padding=dp(10),
        height = dp(7000),
        size_hint_y=None
)
        layout.height = dp(600)  
        roll_label=MDLabel(text="Enter Roll Number to Update")
        self.roll_input=TextInput(multiline=False,size_hint_y=None,height=dp(600))
        search_btn=MDFillRoundFlatIconButton(text="Search  ",md_bg_color=(0,0.6,0.9,1), padding=dp(10))
        search_btn.bind(on_release=lambda x:self.search_student_for_update())
        back_btn=MDFillRoundFlatIconButton(text="Back  ",md_bg_color=(1,0,0,1), padding=dp(10))
        back_btn.bind(on_release=lambda x:self.show_dashboard())
        layout.add_widget(roll_label)
        layout.add_widget(self.roll_input)
        btn_layout=GridLayout(cols=2,size_hint=(1,None),height=dp(70),spacing=dp(190), padding=dp(40))
        btn_layout.add_widget(search_btn)
        btn_layout.add_widget(back_btn)
        layout.add_widget(btn_layout)
        content.add_widget(layout)
        
          # -------------------- Search Student --------------------

    def search_student_for_update(self):
        roll=self.roll_input.text.strip()
        if not roll:
            self.show_dialog("Error","Enter Roll Number")
            return
        with open(self.student_file) as f:
            data=json.load(f)
        student=None
        for s in data:
            if s.get("Roll Number")==roll:
                student=s
                break
        if not student:
            self.show_dialog("Error","Student not found")
            return
        # Show update UI
        home=self.root.get_screen("home")
        content=home.ids.content_area
        content.clear_widgets()
        main_layout=BoxLayout(orientation='vertical',spacing=dp(10),padding=dp(10))
        scroll=ScrollView(size_hint=(1,0.85))
        self.grid=GridLayout(cols=2,spacing=dp(10),padding=dp(10),size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.student_fields={}
        for k,v in student.items():
            if k in ["subjects","marks"]: continue
            self.grid.add_widget(MDLabel(text=k))
            txt=TextInput(multiline=False,size_hint_y=None,height=dp(40))
            txt.text=str(v)
            self.grid.add_widget(txt)
            self.student_fields[k]=txt
        scroll.add_widget(self.grid)
        main_layout.add_widget(scroll)
        # Subjects
        self.subject_inputs=[]
        for sub,mark in zip(student.get("subjects",[]),student.get("marks",[])):
            sub_label=MDLabel(text="Subject")
            sub_input=TextInput(multiline=False,size_hint_y=None,height=dp(40))
            sub_input.text=sub
            mark_label=MDLabel(text="Marks")
            mark_input=TextInput(multiline=False,input_filter="int",size_hint_y=None,height=dp(40))
            mark_input.text=str(mark)
            self.grid.add_widget(sub_label)
            self.grid.add_widget(sub_input)
            self.grid.add_widget(mark_label)
            self.grid.add_widget(mark_input)
            self.subject_inputs.append((sub_input,mark_input))
        save_btn=MDFillRoundFlatIconButton(text="Save Updates",md_bg_color=(0,0.7,0.3,1),size_hint=(1,None),height=dp(50))
        save_btn.bind(on_release=lambda x:self.save_updated_student(roll))
        main_layout.add_widget(save_btn)
        content.add_widget(main_layout)

    def save_updated_student(self,roll):
        with open(self.student_file) as f:
            data = json.load(f)
        for i,s in enumerate(data):
            if s.get("Roll Number")==roll:
                for k,v in self.student_fields.items():
                    s[k]=v.text
                s["subjects"]=[sub.text for sub,mark in self.subject_inputs]
                s["marks"]=[int(mark.text) if mark.text.isdigit() else 0 for sub,mark in self.subject_inputs]
                data[i]=s
                break
        with open(self.student_file, "w") as f:
            json.dump(data,f,indent=2)
        self.show_dialog("Success","Student updated successfully!")
        self.show_dashboard()



      # -------------------- AI Insights --------------------
    def ai_insights(self):
        import json, os, statistics
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.boxlayout import BoxLayout
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDFillRoundFlatIconButton
        from kivy.metrics import dp
    
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
        #Load Data 
        if not os.path.exists(self.student_file):
            self.show_dialog("Error", "No student data available.")
            self.show_dashboard()
            return
    
        with open(self.student_file) as f:
            students = json.load(f)
    
        if not students:
            self.show_dialog("Info", "No student records found.")
            self.show_dashboard()
            return
    
        # Analytics 
        avgs = []
        toppers = []
        subject_stats = {}
    
        for s in students:
            marks = s.get("marks", [])
            subs = s.get("subjects", [])
            if not marks:
                continue
            avg = sum(marks)/len(marks)
            avgs.append(avg)
            toppers.append((s.get("Name"), avg))
            for sub, m in zip(subs, marks):
                subject_stats.setdefault(sub, []).append(m)
    
        class_avg = round(sum(avgs)/len(avgs), 2)
        topper = max(toppers, key=lambda x: x[1])
        weakest = min(toppers, key=lambda x: x[1])
    
        # Subject averages
        subj_avg_text = ""
        for sub, marks in subject_stats.items():
            subj_avg_text += f"{sub}: {round(sum(marks)/len(marks),1)}%   "
    
        # Mood analysis
        if class_avg >= 85:
            mood = "Excellent performance! Keep up the consistency."
        elif class_avg >= 70:
            mood = "Good class average — steady progress."
        elif class_avg >= 50:
            mood = "Needs improvement — focus on weaker topics."
        else:
            mood = "Class struggling — consider revision sessions."
    
        # Layout 
        from kivy.uix.scrollview import ScrollView
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.metrics import dp
        from kivymd.uix.label import MDLabel
        from kivymd.uix.card import MDCard
        from kivymd.uix.button import MDFillRoundFlatIconButton
        
        scroll = ScrollView(size_hint=(1, 1))  
        
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(18),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))
        
        # Title 
        layout.add_widget(MDLabel(
            text="[b]💡 AI Insights — Class Performance Analyzer[/b]",
            markup=True,
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(60)
        ))
        
        #  Card 
        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            radius=[20, 20, 20, 20],
            size_hint_y=None,
            md_bg_color=(1, 1, 1, 1),
            elevation=3
        )
        card.bind(minimum_height=card.setter("height"))
        
    
        info_texts = [
            f"Class Average: [b]{class_avg}%[/b]",
            f"Topper: [b]{topper[0]}[/b] — {round(topper[1],1)}%",
            f"Weakest: [b]{weakest[0]}[/b] — {round(weakest[1],1)}%",
            f"Subject Averages:\n{subj_avg_text}",
            f"Insight: {mood}",
        ]
        
        for t in info_texts:
            lbl = MDLabel(
                text=t,
                markup=True,
                halign="left",
                size_hint_y=None,
                height=dp(40)
            )
            card.add_widget(lbl)
        
        layout.add_widget(card)
        
        #Back Button 
        layout.add_widget(MDFillRoundFlatIconButton(
            text="Back to Dashboard",
            icon="arrow-left",
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 0, 0, 1),
            on_release=lambda x: self.show_dashboard()
        ))
        
        scroll.add_widget(layout)
        content.add_widget(scroll)
    
    
      # -------------------- AI Prediction--------------------

    def prediction_mode(self):
        import json, os, statistics
        from kivy.uix.scrollview import ScrollView
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDFillRoundFlatIconButton
        from kivy.metrics import dp
    
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
        if not os.path.exists(self.student_file):
            self.show_dialog("Error", "No student data available.")
            self.show_dashboard()
            return
    
        with open(self.student_file, "r") as f:
            students = json.load(f)
    
        if not students:
            self.show_dialog("Info", "No student records found.")
            self.show_dashboard()
            return
    
        scroll = ScrollView(size_hint=(1, 1))
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))
    
        layout.add_widget(MDLabel(
            text="[b]AI Performance Prediction Mode[/b]",
            markup=True,
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(60)
        ))
    
        for s in students:
            name = s.get("Name", "Unknown")
            marks = s.get("marks", [])
            if not marks:
                continue
    
            current_avg = sum(marks) / len(marks)
    
            # Simple prediction logic
            if current_avg >= 85:
                predicted_avg = min(current_avg + 1.0, 100)
                trend = "Improving"
            elif current_avg >= 60:
                predicted_avg = current_avg + 0.5
                trend = "Stable"
            else:
                predicted_avg = current_avg + 2.0
                trend = "Needs Improvement"
    
            card = MDCard(
                orientation="vertical",
                padding=dp(15),
                spacing=dp(10),
                radius=[20, 20, 20, 20],
                size_hint=(0.9, None),
                pos_hint={"center_x": 0.5},
                md_bg_color=(1, 1, 1, 1),
                elevation=3
            )
            card.bind(minimum_height=card.setter("height"))
    
            card.add_widget(MDLabel(
                text=f"[b]{name}[/b]",
                markup=True,
                halign="center",
                size_hint_y=None,
                height=dp(35)
            ))
            card.add_widget(MDLabel(
                text=f"Current Average: [b]{round(current_avg, 1)}%[/b]",
                markup=True,
                halign="left",
                size_hint_y=None,
                height=dp(30)
            ))
            card.add_widget(MDLabel(
                text=f"Predicted Next Average: [b]{round(predicted_avg, 1)}%[/b]",
                markup=True,
                halign="left",
                size_hint_y=None,
                height=dp(30)
            ))
            card.add_widget(MDLabel(
                text=f"Trend: [b]{trend}[/b]",
                markup=True,
                halign="left",
                size_hint_y=None,
                height=dp(30)
            ))
    
            layout.add_widget(card)
    
        layout.add_widget(MDFillRoundFlatIconButton(
            text="Back to Dashboard",
            icon="arrow-left",
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 0, 0, 1),
            on_release=lambda x: self.show_dashboard()
        ))
    
        scroll.add_widget(layout)
        content.add_widget(scroll)
        
            
# -------------------- Emotional AI Dashboard --------------------
    
    def emotional_dashboard(self):
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
        import os, json
        from kivy.uix.scrollview import ScrollView
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDFillRoundFlatIconButton
        from kivy.metrics import dp
        from functools import partial  # to fix button binding issue
    
        if not os.path.exists(self.student_file):
            self.show_dialog("Error", "No student data file found.")
            self.show_dashboard()
            return
    
        with open(self.student_file) as f:
            data = json.load(f)
    
        if not data:
            self.show_dialog("Info", "No students found!")
            self.show_dashboard()
            return
    
        # Simple heuristics for emotional state
        def student_state(s):
            marks = s.get("marks", [])
            if not marks:
                return "no-data"
            avg = sum(marks) / len(marks)
            if len(marks) >= 2:
                last, prev = marks[-1], marks[-2]
                change = last - prev
            else:
                change = 0
            variance = (max(marks) - min(marks)) if marks else 0
            if change <= -20:
                return "stressed"
            if variance >= 30:
                return "inconsistent"
            if avg >= 80 or change >= 10:
                return "motivated"
            return "stable"
    
        # Aggregate class-level counts
        counts = {"stressed": 0, "inconsistent": 0, "motivated": 0, "stable": 0, "no-data": 0}
        student_flags = []
        for s in data:
            st = student_state(s)
            counts[st] = counts.get(st, 0) + 1
            student_flags.append((s.get("Name", "Unknown"), st, s))
    
        # Layout
        scroll = ScrollView(size_hint=(1, 1))
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(18),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))
    
        # Summary card
        summary = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            radius=[16, 16, 16, 16],
            size_hint=(0.95, None),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 1, 1, 1),
            elevation=3
        )
        summary.bind(minimum_height=summary.setter("height"))
        summary.add_widget(MDLabel(
            text="[b]Emotional AI - Class Summary[/b]",
            halign="center",
            markup=True,
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        ))
        summary.add_widget(MDLabel(
            text=(
                f"Motivated: {counts['motivated']}    "
                f"Stable: {counts['stable']}    "
                f"Inconsistent: {counts['inconsistent']}    "
                f"Stressed: {counts['stressed']}"
            ),
            halign="center",
            size_hint_y=None,
            height=dp(40)
        ))
        layout.add_widget(summary)
    
        # Student cards
        for name, flag, s in student_flags:
            card = MDCard(
                orientation="vertical",
                padding=dp(15),
                spacing=dp(8),
                radius=[16, 16, 16, 16],
                size_hint=(0.95, None),
                pos_hint={"center_x": 0.5},
                md_bg_color=(1, 1, 1, 1),
                elevation=2
            )
            card.bind(minimum_height=card.setter("height"))
    
            # ---- Student State Logic ----
            if flag == "stressed":
                title = f"{name} — Possible Stress"
                advice = "Check recent tests, consider counseling or focused revision plan."
            elif flag == "inconsistent":
                title = f"{name} — Inconsistent Performance"
                advice = "Recommend consistent practice and short daily quizzes."
            elif flag == "motivated":
                title = f"{name} — Motivated / Improving"
                advice = "Provide challenge problems and encourage peer tutoring."
            elif flag == "stable":
                title = f"{name} — Stable"
                advice = "Maintain current routine; give periodic feedback."
            else:
                title = f"{name} — No Data"
                advice = "No marks available to analyze."
    
            card.add_widget(MDLabel(
                text=f"[b]{title}[/b]",
                markup=True,
                halign="left",
                size_hint_y=None,
                height=dp(30)
            ))
    
            subjects = s.get("subjects", [])
            marks = s.get("marks", [])
            if subjects and marks:
                subj_marks = sorted(zip(subjects, marks), key=lambda x: x[1], reverse=True)
                top3 = ", ".join([f"{sub}({m})" for sub, m in subj_marks[:3]])
                card.add_widget(MDLabel(
                    text=f"Top subjects: {top3}",
                    halign="left",
                    size_hint_y=None,
                    height=dp(28)
                ))
    
            card.add_widget(MDLabel(
                text=f"Action: {advice}",
                halign="left",
                size_hint_y=None,
                height=dp(28)
            ))
    
            # Buttons (fixed with partial binding)
            btns = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(10),
                size_hint_y=None,
                height=dp(45),
                padding=[0, dp(4), 0, 0]
            )
            plan_btn = MDFillRoundFlatIconButton(
                text="Create Plan",
                icon="file-document",
                on_release=partial(self._create_quick_plan, s)  
            )
            note_btn = MDFillRoundFlatIconButton(
                text="Teacher Note",
                icon="pencil",
                on_release=partial(self._quick_teacher_note, s)  
            )
            btns.add_widget(plan_btn)
            btns.add_widget(note_btn)
            card.add_widget(btns)
    
            layout.add_widget(card)
    
        # Back Button 
        layout.add_widget(MDFillRoundFlatIconButton(
            text="Back to Dashboard",
            icon="arrow-left",
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 0, 0, 1),
            on_release=lambda x: self.show_dashboard()
        ))
    
        scroll.add_widget(layout)
        content.add_widget(scroll)
        
        
    def _create_quick_plan(self, student, *args):
        """Teacher-facing quick plan generator"""
        name = student.get("Name", "Unknown")
        subjects = student.get("subjects", [])
        marks = student.get("marks", [])
        weak = [sub for sub, m in zip(subjects, marks) if m < 50]

        plan = ""
        if weak:
            plan = f"Suggested 7-day plan for {name}:\n"
            for sub in weak:
                plan += f"• {sub}: 20-30 min practice, 5 questions daily\n"
        else:
            plan = f"{name} is doing fine. Suggest weekly revision & challenge problems."

        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        dialog = MDDialog(
            title=f"Quick Plan — {name}",
            text=plan,
            size_hint=(0.85, None),
            buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

    def _quick_teacher_note(self, student, *args):
        """Teacher can note quick observation (dialog)"""
        name = student.get("Name", "Unknown")
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        dialog = MDDialog(
            title=f"Teacher Note — {name}",
            text=f"Add your private note for {name} (to implement saving later).",
            size_hint=(0.85, None),
            buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()
    # -------------------- GK Quiz --------------------
    def gk_quiz_mode(self):
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDFillRoundFlatButton
        from kivymd.uix.dialog import MDDialog
        from kivy.metrics import dp
        import random
    
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
     
        self.gk_questions = [
    # --- Indian History ---
            {"question": "Who was the first Emperor of the Maurya Dynasty?", "options": ["Ashoka", "Chandragupta Maurya", "Bindusara", "Harsha"], "answer": "Chandragupta Maurya"},
            {"question": "Who was known as the Iron Man of India?", "options": ["Bhagat Singh", "Sardar Vallabhbhai Patel", "Subhas Chandra Bose", "Lal Bahadur Shastri"], "answer": "Sardar Vallabhbhai Patel"},
            {"question": "When did India get independence from British rule?", "options": ["1942", "1947", "1950", "1930"], "answer": "1947"},
            {"question": "Who was the first Mughal emperor of India?", "options": ["Akbar", "Babur", "Humayun", "Aurangzeb"], "answer": "Babur"},
            {"question": "Who founded the Gupta Empire?", "options": ["Samudragupta", "Chandragupta I", "Vikramaditya", "Skandagupta"], "answer": "Chandragupta I"},
            {"question": "Who gave the slogan 'Quit India'?", "options": ["Bal Gangadhar Tilak", "Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose"], "answer": "Mahatma Gandhi"},
            {"question": "Who was the founder of the Indian National Congress?", "options": ["A.O. Hume", "Dadabhai Naoroji", "W.C. Banerjee", "Gopal Krishna Gokhale"], "answer": "A.O. Hume"},
            {"question": "The Battle of Plassey was fought in which year?", "options": ["1757", "1857", "1764", "1707"], "answer": "1757"},
            {"question": "Who was known as the ‘Napoleon of India’?", "options": ["Samudragupta", "Ashoka", "Chandragupta Maurya", "Raja Raja Chola"], "answer": "Samudragupta"},
            {"question": "Who was the last Governor-General of independent India?", "options": ["C. Rajagopalachari", "Lord Mountbatten", "Lord Wavell", "Rajendra Prasad"], "answer": "C. Rajagopalachari"},
        
            # --- Geography of India ---
            {"question": "Which is the largest state in India by area?", "options": ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan", "Maharashtra"], "answer": "Rajasthan"},
            {"question": "Which river is known as the Ganga of the South?", "options": ["Godavari", "Krishna", "Kaveri", "Narmada"], "answer": "Godavari"},
            {"question": "Which is the smallest state in India by area?", "options": ["Goa", "Sikkim", "Tripura", "Manipur"], "answer": "Goa"},
            {"question": "What is the southernmost point of India called?", "options": ["Cape Comorin", "Indira Point", "Rameswaram", "Kanyakumari"], "answer": "Indira Point"},
            {"question": "Which Indian city is known as the 'City of Lakes'?", "options": ["Udaipur", "Bhopal", "Srinagar", "Jaipur"], "answer": "Udaipur"},
            {"question": "Which is the highest peak in India?", "options": ["Mount Everest", "K2 (Godwin Austen)", "Kanchenjunga", "Nanda Devi"], "answer": "Kanchenjunga"},
            {"question": "The Sundarbans are famous for which animal?", "options": ["Elephant", "Tiger", "Lion", "Leopard"], "answer": "Tiger"},
            {"question": "Which plateau is known as the 'Deccan Plateau'?", "options": ["Malwa", "Chota Nagpur", "Southern Plateau", "Peninsular Plateau"], "answer": "Peninsular Plateau"},
            {"question": "Which state is known as the 'Land of Five Rivers'?", "options": ["Punjab", "Haryana", "Bihar", "Gujarat"], "answer": "Punjab"},
            {"question": "Which river flows through the Valley of Flowers?", "options": ["Alaknanda", "Mandakini", "Pindar", "Pushpawati"], "answer": "Pushpawati"},
        
            # --- Indian Polity ---
            {"question": "Who is known as the Father of the Indian Constitution?", "options": ["Mahatma Gandhi", "B.R. Ambedkar", "Rajendra Prasad", "Jawaharlal Nehru"], "answer": "B.R. Ambedkar"},
            {"question": "In which year was the Indian Constitution adopted?", "options": ["1947", "1948", "1949", "1950"], "answer": "1949"},
            {"question": "Who was the first President of India?", "options": ["Rajendra Prasad", "S. Radhakrishnan", "Zakir Hussain", "V.V. Giri"], "answer": "Rajendra Prasad"},
            {"question": "Who was the first Prime Minister of India?", "options": ["Lal Bahadur Shastri", "Indira Gandhi", "Jawaharlal Nehru", "Rajiv Gandhi"], "answer": "Jawaharlal Nehru"},
            {"question": "How many fundamental rights are there in the Indian Constitution?", "options": ["5", "6", "7", "8"], "answer": "6"},
            {"question": "Which Article guarantees the Right to Equality?", "options": ["Article 14", "Article 19", "Article 21", "Article 32"], "answer": "Article 14"},
            {"question": "The President of India is elected for a term of how many years?", "options": ["4 years", "5 years", "6 years", "7 years"], "answer": "5 years"},
            {"question": "Who appoints the Chief Justice of India?", "options": ["President", "Prime Minister", "Parliament", "Supreme Court"], "answer": "President"},
            {"question": "Which part of the Indian Constitution deals with Fundamental Duties?", "options": ["Part III", "Part IV", "Part IVA", "Part V"], "answer": "Part IVA"},
            {"question": "Which article of the Indian Constitution is related to the Emergency provisions?", "options": ["Article 352", "Article 356", "Article 360", "All of these"], "answer": "All of these"},
        
            # --- Indian Economy ---
            {"question": "Which is the currency of India?", "options": ["Rupee", "Dollar", "Yen", "Pound"], "answer": "Rupee"},
            {"question": "Which is the central bank of India?", "options": ["SBI", "RBI", "ICICI", "NABARD"], "answer": "RBI"},
            {"question": "When was GST implemented in India?", "options": ["2014", "2016", "2017", "2019"], "answer": "2017"},
            {"question": "Which is the largest sector in India’s GDP?", "options": ["Agriculture", "Industry", "Service", "Mining"], "answer": "Service"},
            {"question": "Which organization publishes the Economic Survey of India?", "options": ["Finance Ministry", "RBI", "NITI Aayog", "Planning Commission"], "answer": "Finance Ministry"},
            {"question": "What is the full form of GDP?", "options": ["Gross Domestic Product", "Global Domestic Power", "Gross Departmental Plan", "General Development Policy"], "answer": "Gross Domestic Product"},
            {"question": "Which scheme aims to provide employment in rural India?", "options": ["PMGSY", "MNREGA", "PMJDY", "UDAY"], "answer": "MNREGA"},
            {"question": "Which is India’s first digital payment bank?", "options": ["Paytm Payments Bank", "Airtel Payments Bank", "India Post Payments Bank", "Jio Payments Bank"], "answer": "Airtel Payments Bank"},
            {"question": "Which tax replaced most indirect taxes in India?", "options": ["VAT", "Excise", "GST", "Customs"], "answer": "GST"},
            {"question": "What is the name of India’s first AI Mission?", "options": ["AI Bharat", "IndiaAI Mission", "SmartAI", "AI Revolution"], "answer": "IndiaAI Mission"},
        
            # --- Science and Technology ---
            {"question": "Who is known as the Missile Man of India?", "options": ["A.P.J. Abdul Kalam", "Homi Bhabha", "Vikram Sarabhai", "C.V. Raman"], "answer": "A.P.J. Abdul Kalam"},
            {"question": "What does ISRO stand for?", "options": ["Indian Space Research Organisation", "International Space Research Organisation", "Indian Science Research Office", "Institute for Space Research Organization"], "answer": "Indian Space Research Organisation"},
            {"question": "Which was India’s first satellite?", "options": ["Aryabhata", "Bhaskara", "Rohini", "INSAT-1A"], "answer": "Aryabhata"},
            {"question": "Who discovered the Raman Effect?", "options": ["C.V. Raman", "Homi Bhabha", "J.C. Bose", "S. Chandrasekhar"], "answer": "C.V. Raman"},
            {"question": "Where is ISRO’s headquarters located?", "options": ["Bengaluru", "Hyderabad", "Delhi", "Mumbai"], "answer": "Bengaluru"},
            {"question": "What is the full form of DRDO?", "options": ["Defence Research and Development Organisation", "Department of Research and Defence Office", "Development of Research and Defence Organisation", "Directorate of Research for Defence Operations"], "answer": "Defence Research and Development Organisation"},
            {"question": "Who is known as the Father of Indian Space Program?", "options": ["Vikram Sarabhai", "A.P.J. Abdul Kalam", "C.V. Raman", "S. Chandrasekhar"], "answer": "Vikram Sarabhai"},
            {"question": "Which Indian mission discovered water on the Moon?", "options": ["Chandrayaan-1", "Chandrayaan-2", "Mangalyaan", "Aditya L1"], "answer": "Chandrayaan-1"},
            {"question": "Which mission made India the first Asian country to reach Mars?", "options": ["Chandrayaan", "Mangalyaan", "Vikram", "Aditya L1"], "answer": "Mangalyaan"},
            {"question": "Which Indian supercomputer is among the fastest in the world?", "options": ["PARAM Siddhi-AI", "Pratyush", "Mihir", "All of these"], "answer": "All of these"},
        
            # --- Indian Culture & Sports ---
            {"question": "Bharatanatyam is a classical dance from which state?", "options": ["Kerala", "Tamil Nadu", "Odisha", "Karnataka"], "answer": "Tamil Nadu"},
            {"question": "Who was the first Indian to win an individual Olympic gold medal?", "options": ["Milkha Singh", "Abhinav Bindra", "P.T. Usha", "Leander Paes"], "answer": "Abhinav Bindra"},
            {"question": "Where is the Sun Temple located?", "options": ["Konark", "Khajuraho", "Madurai", "Amritsar"], "answer": "Konark"},
            {"question": "Which city is known as the 'Pink City'?", "options": ["Udaipur", "Jodhpur", "Jaipur", "Bikaner"], "answer": "Jaipur"},
            {"question": "Which festival is known as the 'Festival of Lights'?", "options": ["Holi", "Diwali", "Navratri", "Eid"], "answer": "Diwali"},
            {"question": "What is the national animal of India?", "options": ["Lion", "Elephant", "Tiger", "Peacock"], "answer": "Tiger"},
            {"question": "Who is known as the 'Flying Sikh'?", "options": ["Milkha Singh", "P.T. Usha", "Kapil Dev", "Dhyan Chand"], "answer": "Milkha Singh"},
            {"question": "Where is the Gateway of India located?", "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"], "answer": "Mumbai"},
            {"question": "Which sport is associated with the term 'LBW'?", "options": ["Football", "Hockey", "Cricket", "Tennis"], "answer": "Cricket"},
            {"question": "Which Indian won the Nobel Peace Prize in 2014?", "options": ["Malala Yousafzai", "Kailash Satyarthi", "A.P.J. Abdul Kalam", "Mother Teresa"], "answer": "Kailash Satyarthi"},
            {"question": "Which is the largest state in India by area?",
             "options": ["Maharashtra", "Rajasthan", "Uttar Pradesh", "Madhya Pradesh"],
             "answer": "Rajasthan"},
            
            {"question": "Who is known as the Missile Man of India?",
             "options": ["Dr. A.P.J. Abdul Kalam", "Vikram Sarabhai", "Homi Bhabha", "C.V. Raman"],
             "answer": "Dr. A.P.J. Abdul Kalam"},
            
            {"question": "Which Indian river is known as the 'Sorrow of Bihar'?",
             "options": ["Ganga", "Kosi", "Yamuna", "Brahmaputra"],
             "answer": "Kosi"},
            
            {"question": "Which city is known as the Silicon Valley of India?",
             "options": ["Pune", "Hyderabad", "Bengaluru", "Chennai"],
             "answer": "Bengaluru"},
            
            {"question": "Who was the first Indian woman to go to space?",
             "options": ["Kalpana Chawla", "Sunita Williams", "Indira Gandhi", "Kiran Bedi"],
             "answer": "Kalpana Chawla"},
            
            {"question": "Which Indian state has the longest coastline?",
             "options": ["Gujarat", "Tamil Nadu", "Andhra Pradesh", "Maharashtra"],
             "answer": "Gujarat"},
            
            {"question": "Who was the first Prime Minister of India?",
             "options": ["Sardar Vallabhbhai Patel", "Mahatma Gandhi", "Jawaharlal Nehru", "Dr. Rajendra Prasad"],
             "answer": "Jawaharlal Nehru"},
            
            {"question": "Which is the national fruit of India?",
             "options": ["Banana", "Mango", "Apple", "Litchi"],
             "answer": "Mango"},
            
            {"question": "Which Indian state is known as the 'Land of Five Rivers'?",
             "options": ["Punjab", "Haryana", "Uttar Pradesh", "Rajasthan"],
             "answer": "Punjab"},
            
            {"question": "Who is known as the Father of the Indian Constitution?",
             "options": ["Dr. B.R. Ambedkar", "Mahatma Gandhi", "Jawaharlal Nehru", "Rajendra Prasad"],
             "answer": "Dr. B.R. Ambedkar"},
        
            {"question": "Which country gifted the Statue of Liberty to the USA?",
             "options": ["France", "Germany", "Canada", "Spain"],
             "answer": "France"},
            
            {"question": "Which planet is known as the Blue Planet?",
             "options": ["Mars", "Earth", "Venus", "Jupiter"],
             "answer": "Earth"},
            
            {"question": "Which country has the largest population in the world (as of 2025)?",
             "options": ["China", "India", "USA", "Indonesia"],
             "answer": "India"},
            
            {"question": "Who is the current UN Secretary-General (as of 2025)?",
             "options": ["Ban Ki-moon", "Antonio Guterres", "Kofi Annan", "Tedros Ghebreyesus"],
             "answer": "Antonio Guterres"},
            
            {"question": "Which continent is known as the Dark Continent?",
             "options": ["Africa", "Asia", "Europe", "South America"],
             "answer": "Africa"},
            
            {"question": "Which is the smallest ocean in the world?",
             "options": ["Indian Ocean", "Arctic Ocean", "Atlantic Ocean", "Pacific Ocean"],
             "answer": "Arctic Ocean"},
            
            {"question": "Which is the longest river in the world?",
             "options": ["Amazon", "Nile", "Yangtze", "Mississippi"],
             "answer": "Nile"},
            
            {"question": "Who discovered Penicillin?",
             "options": ["Alexander Fleming", "Marie Curie", "Isaac Newton", "Albert Einstein"],
             "answer": "Alexander Fleming"},
            
            {"question": "Who is the current President of India (as of 2025)?",
             "options": ["Ram Nath Kovind", "Droupadi Murmu", "Narendra Modi", "Pratibha Patil"],
             "answer": "Droupadi Murmu"},
            
            {"question": "Which city hosted the G20 Summit 2023?",
             "options": ["New Delhi", "Mumbai", "Rome", "Tokyo"],
             "answer": "New Delhi"},
            
            {"question": "Which Indian mission successfully landed on the Moon's south pole?",
             "options": ["Chandrayaan-1", "Chandrayaan-2", "Chandrayaan-3", "Mangalyaan"],
             "answer": "Chandrayaan-3"},
            
            {"question": "Which Indian company became the first to cross $200 billion market value?",
             "options": ["Infosys", "Reliance Industries", "TCS", "Adani Group"],
             "answer": "Reliance Industries"},
            
            {"question": "Who won the ICC Men’s Cricket World Cup 2023?",
             "options": ["India", "Australia", "England", "New Zealand"],
             "answer": "Australia"},
            
            {"question": "Which state launched the 'Mukhyamantri Ladli Behna Yojana'?",
             "options": ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan", "Bihar"],
             "answer": "Madhya Pradesh"},
            
            {"question": "Which Indian cricketer scored the most runs in ODI World Cup 2023?",
             "options": ["Virat Kohli", "Rohit Sharma", "Shreyas Iyer", "KL Rahul"],
             "answer": "Virat Kohli"},
        
            {"question": "What is the national currency of Japan?",
             "options": ["Yen", "Won", "Ringgit", "Baht"],
             "answer": "Yen"},
            
            {"question": "Which country is known as the Land of the Rising Sun?",
             "options": ["Japan", "China", "Thailand", "South Korea"],
             "answer": "Japan"},
            
            {"question": "Who was the first woman Prime Minister of India?",
             "options": ["Indira Gandhi", "Sonia Gandhi", "Pratibha Patil", "Sarojini Naidu"],
             "answer": "Indira Gandhi"},
            
            {"question": "In which year did India gain independence?",
             "options": ["1942", "1945", "1947", "1950"],
             "answer": "1947"},
            
            {"question": "Which planet is the hottest in the Solar System?",
             "options": ["Mercury", "Venus", "Mars", "Jupiter"],
             "answer": "Venus"},
            
            {"question": "Which festival is known as the Festival of Lights?",
             "options": ["Holi", "Diwali", "Navratri", "Onam"],
             "answer": "Diwali"},
            
            {"question": "Who invented the telephone?",
             "options": ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "James Watt"],
             "answer": "Alexander Graham Bell"},
            
            {"question": "Which Indian state has 'Hornbill Festival'?",
             "options": ["Nagaland", "Mizoram", "Assam", "Sikkim"],
             "answer": "Nagaland"},
            
            {"question": "Which country recently joined BRICS in 2024?",
             "options": ["Saudi Arabia", "Pakistan", "Turkey", "Vietnam"],
             "answer": "Saudi Arabia"},
            
            {"question": "Who is the CEO of Tesla?",
             "options": ["Elon Musk", "Jeff Bezos", "Tim Cook", "Sundar Pichai"],
             "answer": "Elon Musk"},
            
            {"question": "Which Indian city is known as the City of Joy?",
             "options": ["Mumbai", "Kolkata", "Varanasi", "Jaipur"],
             "answer": "Kolkata"},
        
            {"question": "Who was the first Indian to win a Nobel Prize?",
             "options": ["Rabindranath Tagore", "C.V. Raman", "Mother Teresa", "Amartya Sen"],
             "answer": "Rabindranath Tagore"},
        
            {"question": "Which Indian state is the largest producer of tea?",
             "options": ["Assam", "West Bengal", "Kerala", "Tamil Nadu"],
             "answer": "Assam"},
        
            {"question": "Which Indian festival marks the New Year in Punjab?",
             "options": ["Baisakhi", "Lohri", "Pongal", "Onam"],
             "answer": "Baisakhi"},
        
            {"question": "Who is the current Prime Minister of the United Kingdom (as of 2025)?",
             "options": ["Rishi Sunak", "Boris Johnson", "Keir Starmer", "Liz Truss"],
             "answer": "Rishi Sunak"},
        
            {"question": "Which country won the FIFA World Cup 2022?",
             "options": ["Argentina", "France", "Brazil", "Croatia"],
             "answer": "Argentina"},
        
            {"question": "Which is the largest desert in the world?",
             "options": ["Sahara", "Gobi", "Arabian", "Kalahari"],
             "answer": "Sahara"},
        
            {"question": "Which is the national animal of India?",
             "options": ["Elephant", "Tiger", "Lion", "Peacock"],
             "answer": "Tiger"},
        
            {"question": "Which Indian city is famous for Charminar?",
             "options": ["Hyderabad", "Lucknow", "Delhi", "Agra"],
             "answer": "Hyderabad"},
        
            {"question": "Which state is known as 'God’s Own Country'?",
             "options": ["Kerala", "Goa", "Tamil Nadu", "Himachal Pradesh"],
             "answer": "Kerala"},
            {"question": "Which element has the chemical symbol 'O'?",
             "options": ["Gold", "Oxygen", "Osmium", "Oganesson"],
             "answer": "Oxygen"},
        
            {"question": "Who was the first President of India?",
             "options": ["Rajendra Prasad", "Jawaharlal Nehru", "Sardar Patel", "Mahatma Gandhi"],
             "answer": "Rajendra Prasad"},
        
            {"question": "Which state is known as the 'Spice Garden of India'?",
             "options": ["Kerala", "Goa", "Karnataka", "Assam"],
             "answer": "Kerala"},
        
            {"question": "Which Indian monument is also known as 'Symbol of Love'?",
             "options": ["Qutub Minar", "Taj Mahal", "Red Fort", "Charminar"],
             "answer": "Taj Mahal"},
        
            {"question": "Which is the smallest state in India by area?",
             "options": ["Goa", "Sikkim", "Tripura", "Manipur"],
             "answer": "Goa"},
        
            {"question": "Which Mughal Emperor built the Red Fort in Delhi?",
             "options": ["Akbar", "Shah Jahan", "Aurangzeb", "Babur"],
             "answer": "Shah Jahan"},
        
            {"question": "In which year was the Indian Space Research Organisation (ISRO) founded?",
             "options": ["1962", "1969", "1972", "1980"],
             "answer": "1969"},
        
            {"question": "What is the capital of Canada?",
             "options": ["Toronto", "Ottawa", "Vancouver", "Montreal"],
             "answer": "Ottawa"},
        
            {"question": "Which Indian cricketer is known as the 'Little Master'?",
             "options": ["Sunil Gavaskar", "Sachin Tendulkar", "Kapil Dev", "Rahul Dravid"],
             "answer": "Sunil Gavaskar"},
        
            {"question": "Which is the largest island in the world?",
             "options": ["Greenland", "Madagascar", "Borneo", "Sumatra"],
             "answer": "Greenland"},
        
            {"question": "Which country hosted the 2024 Summer Olympics?",
             "options": ["Paris", "Tokyo", "Los Angeles", "London"],
             "answer": "Paris"},
        
            {"question": "Which Indian river flows eastward into the Bay of Bengal?",
             "options": ["Narmada", "Godavari", "Tapi", "Sutlej"],
             "answer": "Godavari"},
        
            {"question": "Who invented the light bulb?",
             "options": ["Thomas Edison", "Nikola Tesla", "Michael Faraday", "Isaac Newton"],
             "answer": "Thomas Edison"},
        
            {"question": "Which Indian freedom fighter gave the slogan 'Inquilab Zindabad'?",
             "options": ["Bhagat Singh", "Subhas Chandra Bose", "Mahatma Gandhi", "Bal Gangadhar Tilak"],
             "answer": "Bhagat Singh"},
        
            {"question": "Which Indian state has 'Kohima' as its capital?",
             "options": ["Manipur", "Nagaland", "Mizoram", "Meghalaya"],
             "answer": "Nagaland"},
        
            {"question": "Which metal is liquid at room temperature?",
             "options": ["Mercury", "Silver", "Copper", "Aluminium"],
             "answer": "Mercury"},
        
            {"question": "Who was the first Indian to win an Olympic individual gold medal?",
             "options": ["Abhinav Bindra", "Neeraj Chopra", "Milkha Singh", "PV Sindhu"],
             "answer": "Abhinav Bindra"},
        
            {"question": "Which is the highest civilian award in India?",
             "options": ["Padma Bhushan", "Padma Vibhushan", "Bharat Ratna", "Gallantry Award"],
             "answer": "Bharat Ratna"},
        
            {"question": "Which planet has the most moons?",
             "options": ["Saturn", "Jupiter", "Mars", "Uranus"],
             "answer": "Saturn"},
        
            {"question": "Who discovered gravity?",
             "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Copernicus"],
             "answer": "Isaac Newton"},
        
            {"question": "What is the capital of Australia?",
             "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
             "answer": "Canberra"},
        
            {"question": "Which Indian city is known as the 'Pink City'?",
             "options": ["Udaipur", "Jaipur", "Jodhpur", "Bhopal"],
             "answer": "Jaipur"},
        
            {"question": "Who is the current Chief Justice of India (as of 2025)?",
             "options": ["D.Y. Chandrachud", "U.U. Lalit", "N.V. Ramana", "Ranjan Gogoi"],
             "answer": "D.Y. Chandrachud"},
        
            {"question": "Which country recently became the 5th largest economy in the world?",
             "options": ["India", "UK", "Germany", "France"],
             "answer": "India"},
        
            {"question": "Which gas is essential for photosynthesis?",
             "options": ["Carbon Dioxide", "Oxygen", "Nitrogen", "Hydrogen"],
             "answer": "Carbon Dioxide"},
        
            {"question": "Which animal is known as the Ship of the Desert?",
             "options": ["Camel", "Horse", "Elephant", "Donkey"],
             "answer": "Camel"},
        
            {"question": "Which is the longest wall in the world?",
             "options": ["Great Wall of China", "Berlin Wall", "Hadrian’s Wall", "Western Wall"],
             "answer": "Great Wall of China"},
        
            {"question": "Who is the founder of Microsoft?",
             "options": ["Steve Jobs", "Bill Gates", "Larry Page", "Mark Zuckerberg"],
             "answer": "Bill Gates"},
        
            {"question": "Which is the largest planet in our Solar System?",
             "options": ["Earth", "Jupiter", "Saturn", "Neptune"],
             "answer": "Jupiter"},
        
            {"question": "What is the capital of Russia?",
             "options": ["St. Petersburg", "Moscow", "Kazan", "Novgorod"],
             "answer": "Moscow"},
        
            {"question": "Which country won the ICC T20 World Cup 2024?",
             "options": ["India", "England", "Australia", "West Indies"],
             "answer": "India"},
        
            {"question": "Who was known as the Iron Man of India?",
             "options": ["Sardar Vallabhbhai Patel", "Bhagat Singh", "Subhas Chandra Bose", "Lal Bahadur Shastri"],
             "answer": "Sardar Vallabhbhai Patel"},
        
            {"question": "Which Indian festival celebrates the victory of good over evil?",
             "options": ["Holi", "Diwali", "Navratri", "Eid"],
             "answer": "Diwali"},
        
            {"question": "Which Indian state is famous for backwaters?",
             "options": ["Kerala", "Goa", "Odisha", "Andhra Pradesh"],
             "answer": "Kerala"},
        
            {"question": "Who is the founder of Facebook?",
             "options": ["Mark Zuckerberg", "Elon Musk", "Jeff Bezos", "Bill Gates"],
             "answer": "Mark Zuckerberg"},
        
            {"question": "Which is the national bird of India?",
             "options": ["Peacock", "Sparrow", "Parrot", "Eagle"],
             "answer": "Peacock"},
        
            {"question": "Who wrote the Indian national anthem?",
             "options": ["Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Subramania Bharati"],
             "answer": "Rabindranath Tagore"},
        
            {"question": "Which Indian state is known for its dance form 'Kathakali'?",
             "options": ["Kerala", "Tamil Nadu", "Odisha", "Karnataka"],
             "answer": "Kerala"},
        
            {"question": "Which is the largest continent on Earth?",
             "options": ["Asia", "Africa", "Europe", "North America"],
             "answer": "Asia"},
        
            {"question": "Which Indian company developed the UPI payment system?",
             "options": ["RBI", "NPCI", "Paytm", "Google Pay"],
             "answer": "NPCI"},
        
            {"question": "Which Indian city is called the City of Lakes?",
             "options": ["Udaipur", "Bhopal", "Srinagar", "Hyderabad"],
             "answer": "Udaipur"},
            {"question": "Who is the current Prime Minister of the United Kingdom (2025)?",
             "options": ["Rishi Sunak", "Keir Starmer", "Boris Johnson", "Theresa May"],
             "answer": "Keir Starmer"},
        
            {"question": "Which Indian city hosted the G20 Summit in 2023?",
             "options": ["New Delhi", "Mumbai", "Hyderabad", "Bangalore"],
             "answer": "New Delhi"},
        
            {"question": "Which country won the FIFA World Cup 2022?",
             "options": ["France", "Argentina", "Brazil", "Croatia"],
             "answer": "Argentina"},
        
            {"question": "Which Indian was awarded the 2024 Bharat Ratna?",
             "options": ["L.K. Advani", "MS Swaminathan", "Narendra Modi", "Amitabh Bachchan"],
             "answer": "MS Swaminathan"},
        
            {"question": "Which is the fastest train in India as of 2025?",
             "options": ["Vande Bharat Express", "Rajdhani Express", "Tejas Express", "Duronto Express"],
             "answer": "Vande Bharat Express"},
        
            {"question": "Which Indian space mission landed on the Moon’s south pole?",
             "options": ["Chandrayaan-3", "Chandrayaan-2", "Mangalyaan", "Aditya-L1"],
             "answer": "Chandrayaan-3"},
        
            {"question": "Who is the current President of India (2025)?",
             "options": ["Droupadi Murmu", "Ram Nath Kovind", "Venkaiah Naidu", "Pratibha Patil"],
             "answer": "Droupadi Murmu"},
        
            {"question": "Which Indian film won the Oscar for Best Original Song?",
             "options": ["RRR", "Lagaan", "Slumdog Millionaire", "Jawan"],
             "answer": "RRR"},
        
            {"question": "Which Indian cricketer won the ICC Cricketer of the Year 2023?",
             "options": ["Virat Kohli", "Shubman Gill", "Rohit Sharma", "Ravindra Jadeja"],
             "answer": "Shubman Gill"},
        
            {"question": "Which city is known as the Silicon Valley of India?",
             "options": ["Hyderabad", "Bangalore", "Chennai", "Pune"],
             "answer": "Bangalore"},
        
            {"question": "Which Indian scientist is known as the Missile Man of India?",
             "options": ["APJ Abdul Kalam", "Vikram Sarabhai", "C.V. Raman", "Homi Bhabha"],
             "answer": "APJ Abdul Kalam"},
        
            {"question": "Which planet is known as the 'Morning Star'?",
             "options": ["Venus", "Mars", "Mercury", "Neptune"],
             "answer": "Venus"},
        
            {"question": "Who was the first woman Prime Minister of India?",
             "options": ["Indira Gandhi", "Sonia Gandhi", "Pratibha Patil", "Sarojini Naidu"],
             "answer": "Indira Gandhi"},
        
            {"question": "Which Indian city is known as the 'City of Joy'?",
             "options": ["Kolkata", "Delhi", "Mumbai", "Chennai"],
             "answer": "Kolkata"},
        
            {"question": "Who discovered penicillin?",
             "options": ["Alexander Fleming", "Louis Pasteur", "Marie Curie", "Charles Darwin"],
             "answer": "Alexander Fleming"},
        
            {"question": "Which Indian river is known as 'Dakshin Ganga'?",
             "options": ["Godavari", "Krishna", "Cauvery", "Narmada"],
             "answer": "Godavari"},
        
            {"question": "Which is the largest democracy in the world?",
             "options": ["USA", "India", "China", "Russia"],
             "answer": "India"},
        
            {"question": "Who invented the telephone?",
             "options": ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "James Watt"],
             "answer": "Alexander Graham Bell"},
        
            {"question": "Which is the highest mountain peak in the world?",
             "options": ["K2", "Mount Everest", "Kangchenjunga", "Annapurna"],
             "answer": "Mount Everest"},
        
            {"question": "Who is known as the Father of the Nation in India?",
             "options": ["Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "Subhas Chandra Bose"],
             "answer": "Mahatma Gandhi"},
        
            {"question": "What is the national flower of India?",
             "options": ["Rose", "Lotus", "Sunflower", "Jasmine"],
             "answer": "Lotus"},
        
            {"question": "Which is the currency of Japan?",
             "options": ["Yen", "Won", "Dollar", "Peso"],
             "answer": "Yen"},
        
            {"question": "Which is the largest ocean on Earth?",
             "options": ["Indian Ocean", "Pacific Ocean", "Atlantic Ocean", "Arctic Ocean"],
             "answer": "Pacific Ocean"},
        
            {"question": "Which Indian won the Nobel Prize in Economics in 1998?",
             "options": ["Amartya Sen", "C.V. Raman", "Venkatraman Ramakrishnan", "Kailash Satyarthi"],
             "answer": "Amartya Sen"},
        
            {"question": "Who is known as the 'Flying Sikh' of India?",
             "options": ["Milkha Singh", "P.T. Usha", "Neeraj Chopra", "Abhinav Bindra"],
             "answer": "Milkha Singh"},
        
            {"question": "Which is the national sport of India (de jure)?",
             "options": ["Cricket", "Hockey", "Kabaddi", "Football"],
             "answer": "None (No official national sport)"},
        
            {"question": "Which country is known as the 'Land of the Rising Sun'?",
             "options": ["China", "Japan", "South Korea", "Thailand"],
             "answer": "Japan"},
        
            {"question": "Which is the cleanest city in India (2024 survey)?",
             "options": ["Indore", "Surat", "Bhopal", "Mysuru"],
             "answer": "Indore"},
        
            {"question": "Which country launched the world’s first reusable rocket?",
             "options": ["USA", "Russia", "China", "India"],
             "answer": "USA"},
        
            {"question": "Who is the current UN Secretary-General?",
             "options": ["António Guterres", "Ban Ki-moon", "Kofi Annan", "Jens Stoltenberg"],
             "answer": "António Guterres"},
        
            {"question": "Which Indian city is called the 'Manchester of India'?",
             "options": ["Ahmedabad", "Surat", "Mumbai", "Kanpur"],
             "answer": "Ahmedabad"},
        
            {"question": "Which element has the chemical symbol 'Na'?",
             "options": ["Nitrogen", "Sodium", "Nickel", "Neon"],
             "answer": "Sodium"},
        
            {"question": "Which festival marks the Sikh New Year?",
             "options": ["Baisakhi", "Lohri", "Guru Nanak Jayanti", "Diwali"],
             "answer": "Baisakhi"},
        
            {"question": "Which Indian state produces the most tea?",
             "options": ["Assam", "West Bengal", "Kerala", "Tamil Nadu"],
             "answer": "Assam"},
        
            {"question": "Which is the smallest country in the world?",
             "options": ["Vatican City", "Monaco", "Nauru", "Malta"],
             "answer": "Vatican City"},
        
            {"question": "Which country invented paper?",
             "options": ["China", "India", "Egypt", "Greece"],
             "answer": "China"},
        
            {"question": "Which Indian was recently appointed as World Bank Chief Economist (2024)?",
             "options": ["Indermit Gill", "Kaushik Basu", "Raghuram Rajan", "Arvind Subramanian"],
             "answer": "Indermit Gill"},
        
            {"question": "Who is the CEO of Tesla?",
             "options": ["Elon Musk", "Tim Cook", "Jeff Bezos", "Larry Page"],
             "answer": "Elon Musk"},
        
            {"question": "Which Indian sportsperson won gold in javelin at the Tokyo Olympics 2021?",
             "options": ["Neeraj Chopra", "Bajrang Punia", "PV Sindhu", "Lovlina Borgohain"],
             "answer": "Neeraj Chopra"},
        
            {"question": "What is the national animal of India?",
             "options": ["Lion", "Tiger", "Elephant", "Leopard"],
             "answer": "Tiger"},
        
            {"question": "Which Indian state is known as the 'Land of Five Rivers'?",
             "options": ["Punjab", "Haryana", "Uttar Pradesh", "Bihar"],
             "answer": "Punjab"},
        
            {"question": "Which was the first satellite launched by India?",
             "options": ["Aryabhata", "Bhaskara", "Rohini", "INSAT-1A"],
             "answer": "Aryabhata"},
        ]
        
        
        
    
        
        while len(self.gk_questions) < 700:
            q = random.choice(self.gk_questions)
            self.gk_questions.append(q)
    
        random.shuffle(self.gk_questions)
    
        self.current_question = 0
        self.score = 0
    
        def show_question(index):
            content.clear_widgets()
            if index >= len(self.gk_questions):
                show_result()
                return
    
            qdata = self.gk_questions[index]
    
            layout = MDBoxLayout(orientation="vertical", spacing=dp(18), padding=dp(20))
            layout.add_widget(MDLabel(
                text=f"[b]Question {index+1} of {len(self.gk_questions)}[/b]",
                markup=True,
                halign="center",
                font_style="H6"
            ))
            layout.add_widget(MDLabel(
                text=qdata["question"],
                halign="center",
                theme_text_color="Primary",
                font_style="H5"
            ))
    
            # Option buttons
            for opt in qdata["options"]:
                btn = MDFillRoundFlatButton(
                    text=opt,
                    size_hint=(0.8, None),
                    height=dp(48),
                    pos_hint={"center_x": 0.5},
                    on_release=lambda x, o=opt: check_answer(o)
                )
                layout.add_widget(btn)
    
            # Navigation buttons (Back / Next)
            nav_box = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(250), padding=[0, dp(100), 0, 0])
            back_btn = MDFillRoundFlatButton(
                text="Back",
                icon="arrow-left",
                on_release=lambda x: prev_question(),
                md_bg_color=(1, 0.3, 0.3, 1)
            )
            next_btn = MDFillRoundFlatButton(
                text="Next",
                on_release=lambda x: next_question(),
                md_bg_color=(0.3, 0.8, 0.3, 1)
            )
            nav_box.add_widget(back_btn)
            nav_box.add_widget(next_btn)
            layout.add_widget(nav_box)
    
            # Back button 
            dash_btn = MDFillRoundFlatButton(
                text="Back to Dashboard",
                size_hint=(0.7, None),
                height=dp(50),
                pos_hint={"center_x": 0.5},
                md_bg_color=(1, 0, 0, 1),
                on_release=lambda x: self.show_dashboard()
            )
            layout.add_widget(dash_btn)
    
            content.add_widget(layout)
    
        def check_answer(selected_option):
            correct = self.gk_questions[self.current_question]["answer"]
            if selected_option == correct:
                self.score += 1
                msg = f"Correct! Your score: {self.score}"
            else:
                msg = f"Wrong! Correct answer: [b]{correct}[/b]"
    
            dialog = MDDialog(
                title="Answer Result",
                text=msg,
                size_hint=(0.8, None),
                buttons=[
                    MDFillRoundFlatButton(
                        text="Close",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
    
        def next_question():
            if self.current_question < len(self.gk_questions) - 1:
                self.current_question += 1
                show_question(self.current_question)
            else:
                show_result()
    
        def prev_question():
            if self.current_question > 0:
                self.current_question -= 1
                show_question(self.current_question)
    
        def show_result():
            content.clear_widgets()
            layout = MDBoxLayout(orientation="vertical", spacing=dp(20), padding=dp(30))
            layout.add_widget(MDLabel(
                text=f"[b]Quiz Completed![/b]",
                markup=True,
                halign="center",
                font_style="H4"
            ))
            layout.add_widget(MDLabel(
                text=f"Your final score: {self.score} / {len(self.gk_questions)}",
                halign="center",
                font_style="H5"
            ))
    
            btn = MDFillRoundFlatButton(
                text="Back to Dashboard",
                size_hint=(0.6, None),
                height=dp(50),
                pos_hint={"center_x": 0.5},
                md_bg_color=(1, 0, 0, 1),
                on_release=lambda x: self.show_dashboard()
            )
            layout.add_widget(btn)
            content.add_widget(layout)
    
        # Start quiz
        show_question(self.current_question)

    # -------------------- AI Mentor Mode (Teacher-Facing) --------------------
    def ai_mentor_mode(self):
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
        import os, json
        from kivy.uix.scrollview import ScrollView
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDFillRoundFlatIconButton
        from kivy.metrics import dp
    
        # --------------- Check File ---------------
        if not os.path.exists(self.student_file):
            self.show_dialog("Error", "No student data file found.")
            self.show_dashboard()
            return
    
        with open(self.student_file) as f:
            data = json.load(f)
        if not data:
            self.show_dialog("Info", "No students found!")
            self.show_dashboard()
            return
    
        # --------------- Layout ---------------
        scroll = ScrollView(size_hint=(1, 1))
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(18),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))
    
        # --------------- Title Card ---------------
        card = MDCard(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            radius=[20, 20, 20, 20],
            size_hint=(0.9, None),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 1, 1, 1),
            elevation=3
        )
        card.bind(minimum_height=card.setter("height"))
    
        card.add_widget(MDLabel(
            text="[b]AI Mentor — Teacher Mode[/b]",
            markup=True,
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height=dp(35)
        ))
    
        card.add_widget(MDLabel(
            text="Click a student below to get coaching notes and a 7-day homework plan.",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(45)
        ))
    
        layout.add_widget(card)
    
        # --------------- Student Buttons ---------------
        for s in data:
            name = s.get("Name", "Unknown")
            total = sum(s.get("marks", [])) if s.get("marks") else 0
            btn = MDFillRoundFlatIconButton(
                text=f"{name} — Total {total}",
                icon="account",
                size_hint=(0.85, None),
                height=dp(48),
                pos_hint={"center_x": 0.5},
                on_release=lambda x, st=s: self._mentor_for_student(st)
            )
            layout.add_widget(btn)
    
        scroll.add_widget(layout)
        content.add_widget(scroll)
    
        # --------------- Back Button ---------------
        back_btn = MDFillRoundFlatIconButton(
            text="Back to Dashboard",
            icon="arrow-left",
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 0, 0, 1),
            on_release=lambda x: self.show_dashboard()
        )
        content.add_widget(back_btn)
    
    
    def _mentor_for_student(self, s):
     
        name = s.get("Name","Unknown")
        subjects = s.get("subjects", [])
        marks = s.get("marks", [])
        avg = round(sum(marks)/len(marks),2) if marks else 0

        # Coaching rules 
        notes = []
        plan = []
        if avg >= 85:
            notes.append("Excellent overall. Assign extension/challenge problems.")
        elif avg >= 60:
            notes.append("Good. Focus on accuracy & time management.")
        else:
            notes.append("Remedial plan recommended. Short daily practice sessions.")

        # subject-wise tips
        for sub, m in zip(subjects, marks):
            if m >= 85:
                notes.append(f"{sub}: Strong — give advanced worksheets.")
            elif m >= 60:
                notes.append(f"{sub}: Average — assign timed practice.")
            else:
                notes.append(f"{sub}: Weak — give micro-lessons (15 min) + 5 daily Qs.")
                plan.append(f"{sub}: 15 min theory + 5 practice q/day")

        # build text
        text = f"Teacher Notes for {name} (Avg: {avg}):\n" + "\n".join(f"• {n}" for n in notes)
        if plan:
            text += "\n\n7-day Quick Homework Plan:\n" + "\n".join(f"Day {i+1}: {p}" for i,p in enumerate(plan*7))
        else:
            text += "\n\n7-day Plan: Weekly revision + 10 min daily practice."



        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.uix.scrollview import ScrollView
        from kivy.metrics import dp
        from kivy.core.window import Window
        
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))  # Full size but constrained by parent
        box = MDBoxLayout(orientation="vertical", padding=dp(10), size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        
        label = MDLabel(
            text=text,
            markup=True,
            halign="left",
            theme_text_color="Primary",
            size_hint_y=None,
        )
        label.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        box.add_widget(label)
        scroll.add_widget(box)
        
        dialog = MDDialog(
            title=f"Mentor Notes — {name}",
            type="custom",
            content_cls=scroll,
            size_hint=(0.9, None),  # ✅ Important — fix overall height of dialog
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()


    
   
      
   # -------------------- Dream Path Visualizer (Career Map) --------------------
    def dream_path_visualizer(self):
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
        import os, json
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.boxlayout import BoxLayout
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDFillRoundFlatIconButton
        from kivy.metrics import dp
    
        if not os.path.exists(self.student_file):
            self.show_dialog("Error", "No student data file found.")
            self.show_dashboard()
            return
    
        with open(self.student_file) as f:
            data = json.load(f)
        if not data:
            self.show_dialog("Info", "No students found!")
            self.show_dashboard()
            return
    
        
        def suggest_career(s):
            subjects = s.get("subjects", [])
            marks = s.get("marks", [])
            if not subjects or not marks:
                return ["Data insufficient"]
            best_idx = max(range(len(marks)), key=lambda i: marks[i])
            best_sub = subjects[best_idx].lower()
    
            if any(k in best_sub for k in ["math","physics","chem","science","computer"]):
                return ["Engineering / Computer Science / Research"]
            if any(k in best_sub for k in ["commerce","account","business","economics"]):
                return ["Commerce / Business / CA"]
            if any(k in best_sub for k in ["history","civics","geography","political"]):
                return ["Law / Civil Services / Humanities"]
            if any(k in best_sub for k in ["art","drawing","design","music","dance","english","literature"]):
                return ["Design / Creative Arts / Media"]
            return ["General Sciences / Explore electives"]
    
        # ---------------- Layout ----------------
        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation="vertical", spacing=dp(16), padding=dp(16), size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
    
        # Title Card
        title_card = MDCard(orientation="vertical", padding=dp(14), radius=[16]*4, md_bg_color=(1,1,1,1), elevation=3, size_hint_y=None)
        title_card.add_widget(MDLabel(
            text="[b]Dream Path Visualizer — Teacher Mode[/b]\nClick a student to view suggested career paths.",
            markup=True,
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(10)
        ))
        layout.add_widget(title_card)
    
        # Student Cards
        for s in data:
            name = s.get("Name", "Unknown")
            careers = suggest_career(s)
    
            card = MDCard(
                orientation="vertical",
                padding=dp(14),
                spacing=dp(10),
                radius=[16]*4,
                size_hint=(0.9, None),
                pos_hint={"center_x": 0.5},
                md_bg_color=(1, 1, 1, 1),
                elevation=3
            )
            card.bind(minimum_height=card.setter("height"))
    
            # Name Label
            card.add_widget(MDLabel(
                text=f"[b]{name}[/b]",
                markup=True,
                halign="left",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(28)
            ))
    
            # Suggested Career
            card.add_widget(MDLabel(
                text="Suggested: " + ", ".join(careers),
                halign="left",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(30)
            ))
    
            # Button
            more_btn = MDFillRoundFlatIconButton(
                text="Show Details",
                icon="eye",
                size_hint=(0.6, None),
                height=dp(45),
                pos_hint={"center_x": 0.5},
                md_bg_color=(0,0.6,0.9,1),
                on_release=lambda x, st=s: self._career_details(st)
            )
            card.add_widget(more_btn)
    
            layout.add_widget(card)
    
        scroll.add_widget(layout)
        content.add_widget(scroll)
    
        # Back button
        back_btn = MDFillRoundFlatIconButton(
            text="Back to Dashboard",
            icon="arrow-left",
            size_hint=(0.6, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 0, 0, 1),
            on_release=lambda x: self.show_dashboard()
        )
        content.add_widget(back_btn)
        
          # -------------------- Career --------------------
    
    def _career_details(self, s):
        name = s.get("Name", "Unknown")
        subjects = s.get("subjects", [])
        marks = s.get("marks", [])
        careers = []
        tips = ""
    
        if subjects and marks:
            best_idx = max(range(len(marks)), key=lambda i: marks[i])
            best_sub = subjects[best_idx].lower()
            if any(k in best_sub for k in ["math","physics","chem","science","computer"]):
                careers = ["Engineering (CS, EE, ME)", "Research / Data Science", "BSc + MSc"]
                tips = "Encourage coding, advanced math problem-solving, and science projects."
            elif any(k in best_sub for k in ["commerce","account","business","economics"]):
                careers = ["Commerce (B.Com, BBA)", "CA / CS", "Business Analytics"]
                tips = "Focus on numerical aptitude, business projects, and internships."
            elif any(k in best_sub for k in ["history","civics","geography","political"]):
                careers = ["Law", "Civil Services", "Social Sciences"]
                tips = "Encourage essay writing, debates, and current affairs."
            else:
                careers = ["Design / Media / General electives"]
                tips = "Provide creative assignments and portfolio guidance."
        else:
            careers = ["Data insufficient"]
            tips = "Collect more subject marks to give better guidance."
    
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        from kivy.uix.scrollview import ScrollView
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivy.metrics import dp
    
        text = (
            f"[b]Name:[/b] {name}\n\n"
            f"[b]Suggested Career Paths:[/b]\n• " + "\n• ".join(careers) +
            f"\n\n[b]Teacher Tips:[/b]\n{tips}"
        )
    
        # Scrollable content for dialog
        scroll = ScrollView(size_hint=(1, None), height=dp(300))
        box = MDBoxLayout(orientation="vertical", padding=dp(10), size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
    
        label = MDLabel(
            text=text,
            markup=True,
            halign="left",
            theme_text_color="Primary",
            size_hint_y=None,
        )
        label.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        box.add_widget(label)
        scroll.add_widget(box)
    
        # Proper MDDialog
        d = MDDialog(
            title=f"Career Details — {name}",
            type="custom",
            content_cls=scroll,
            size_hint=(0.9, None),
            buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: d.dismiss())],
        )
        d.open()

    # -------------------- Rank List --------------------
    def rank_list(self):
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area

        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()

        with open(self.student_file) as f:
            data = json.load(f)

        if not data:
            self.show_dialog("Info", "No students found!")
            self.show_dashboard()
            return

        for s in data:
            s['total_marks'] = sum(s.get('marks', []))

        data.sort(key=lambda x: x['total_marks'], reverse=True)

        scroll_vert = ScrollView(size_hint=(1, 0.9))
        outer_grid = GridLayout(cols=1, spacing=dp(15), padding=dp(15), size_hint_y=None)
        outer_grid.bind(minimum_height=outer_grid.setter('height'))

        header = GridLayout(cols=4, padding=dp(15),  size_hint_y=None, height=dp(80))
        header.add_widget(MDLabel(text="[b]Rank[/b]", markup=True))
        header.add_widget(MDLabel(text="[b]Name[/b]", markup=True))
        header.add_widget(MDLabel(text="[b]Roll[/b]", markup=True))
        header.add_widget(MDLabel(text="[b]Total Marks[/b]", markup=True))
        outer_grid.add_widget(header)

        for idx, s in enumerate(data, start=1):
            row = GridLayout(cols=4, size_hint_y=None, height=dp(40))
            row.add_widget(MDLabel(text=str(idx)))
            row.add_widget(MDLabel(text=s.get("Name","")))
            row.add_widget(MDLabel(text=s.get("Roll Number","")))
            row.add_widget(MDLabel(text=str(s.get("total_marks",0))))
            outer_grid.add_widget(row)

        scroll_vert.add_widget(outer_grid)
        content.add_widget(scroll_vert)

        back_btn = MDFillRoundFlatIconButton(text="Back to Dashboard  ", size_hint=(0.5,None), pos_hint={"center_x": 0.5},height=dp(50), md_bg_color=(1,0,0,1))
        back_btn.bind(on_release=lambda x: self.show_dashboard())
        content.add_widget(back_btn)
        
 
    # -------------------- Delete Student --------------------
    def delete_student(self):
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area

        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()

        layout = BoxLayout(orientation='vertical', spacing=dp(650), padding=dp(10))
        label = MDLabel(text="Enter Roll Number to Delete")
        self.delete_roll_input = TextInput(multiline=False, size_hint_y=None, height=dp(40))
        search_btn = MDFillRoundFlatIconButton(text="Delete  ", md_bg_color=(0,0.6,0.9,1))
        back_btn = MDFillRoundFlatIconButton(text="Back  ", md_bg_color=(1,0,0,1))
        layout.add_widget(label)
        layout.add_widget(self.delete_roll_input)

        btn_layout = GridLayout(cols=2, size_hint=(1.5,None), height=dp(50), spacing=dp(220), padding=dp(7))
        btn_layout.add_widget(search_btn)
        btn_layout.add_widget(back_btn)
        layout.add_widget(btn_layout)
        content.add_widget(layout)

        search_btn.bind(on_release=lambda x: self.delete_student_by_roll())
        back_btn.bind(on_release=lambda x: self.show_dashboard())

    def delete_student_by_roll(self):
        roll = self.delete_roll_input.text.strip()
        if not roll:
            self.show_dialog("Error", "Enter Roll Number")
            return
        with open(self.student_file) as f:
            data = json.load(f)
        new_data = [s for s in data if s.get("Roll Number") != roll]
        if len(new_data) == len(data):
            self.show_dialog("Error", "Student not found")
            return
        with open(self.student_file,"w") as f:
            json.dump(new_data,f,indent=2)
        self.show_dialog("Success", f"Student with Roll '{roll}' deleted!")
        self.show_dashboard()
        
            
# -------------------- Search Student --------------------
    def search_student(self):
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        
        # Hide dashboard buttons
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=700,
            padding=[20, 20, 20, 20]
        )
    
        # Title
        label = MDLabel(
            text="Search Student",
            halign="center",
            theme_text_color="Primary",
            font_style="H5"
        )
        layout.add_widget(label)
    
        # Search input
        self.search_field = MDTextField(
            hint_text="Enter Roll Number or Name",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.search_field)
    
        # Buttons
        btn_box = MDBoxLayout(spacing=560, padding=7, size_hint_y=None, height=dp(48))
        search_btn = MDFillRoundFlatIconButton(
            text="Search  ",
            md_bg_color=(0.2, 0.6, 1, 1),
            on_release=lambda x: self.perform_search()
        )
        back_btn = MDFillRoundFlatIconButton(
            text="Back  ",
            md_bg_color=(1, 0, 0, 1),
            on_release=lambda x: self.show_dashboard()
        )
        btn_box.add_widget(search_btn)
        btn_box.add_widget(back_btn)
        layout.add_widget(btn_box)
    
        content.add_widget(layout)
    
    
    def perform_search(self):
        query = self.search_field.text.strip().lower()
        if not query:
            self.show_dialog("Error", "Please enter a roll number or name to search.")
            return
    
        results = []
        if os.path.exists(self.student_file):
            with open(self.student_file, "r") as f:
                students = json.load(f)  
                for s in students:      
                    # Safe key access
                    name = s.get("Name") or s.get("name", "")
                    roll = s.get("Roll Number") or s.get("roll", "")
                    if query in name.lower() or query == roll.lower():
                        results.append(s)
    
        home = self.root.get_screen("home")
        content = home.ids.content_area
        content.clear_widgets()
    
        if not results:
          
            self.show_dialog("No result found", "No student matched your query. Please try again.")
            # Return to search page
            self.search_student()
            return
    
        # Prepare table rows with calculated Average and Grade
        row_data = []
        for s in results:
            marks = s.get("marks", [])
            avg = sum(marks)/len(marks) if marks else 0
            if avg >= 90: grade = "A+"
            elif avg >= 75: grade = "A"
            elif avg >= 60: grade = "B"
            elif avg >= 50: grade = "C"
            else: grade = "F"
    
            roll = s.get("Roll Number") or s.get("roll", "")
            name = s.get("Name") or s.get("name", "")
            row_data.append((
                roll,                   # Roll
                name,                   # Name
                ", ".join(map(str, marks)),  # Marks list
                f"{avg:.2f}",           # Average
                grade                   # Grade
            ))
    
        # Table
        table = MDDataTable(
            size_hint=(1, 0.8),
            use_pagination=True,
            column_data=[
                ("Roll", dp(30)),
                ("Name", dp(50)),
                ("Marks", dp(60)),
                ("Average", dp(30)),
                ("Grade", dp(30)),
            ],
            row_data=row_data
        )
    
        # Back button
        back_btn = MDFillRoundFlatIconButton(
            text="Back",
            md_bg_color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=dp(50),
            on_release=lambda x: self.search_student()  # go back to search page
        )
    
        content.add_widget(table)
        content.add_widget(back_btn)
        
       # -------------------- Show Topper Student --------------------
    def show_topper(self):
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
    
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
        # Load data
        if not os.path.exists(self.student_file):
            self.show_dialog("Error", "No student data found.")
            self.show_dashboard()
            return
    
        with open(self.student_file) as f:
            data = json.load(f)
    
        if not data:
            self.show_dialog("Info", "No students found!")
            self.show_dashboard()
            return
    
        # Find topper
        topper = None
        top_total = 0
        for s in data:
            marks = s.get("marks", [])
            total = sum(marks) if all(isinstance(m, (int, float)) for m in marks) else 0
            if total > top_total:
                top_total = total
                topper = s
    
        if not topper:
            self.show_dialog("Info", "No valid marks found.")
            self.show_dashboard()
            return
    
        # Display topper info
        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(2), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
    
        card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(100),
            radius=[20, 20, 20, 20],
            elevation=2,
            size_hint_y=None,
        )
        card.bind(minimum_height=card.setter('height'))
    
        card.add_widget(MDLabel(
            text="[b]Topper of the Class[/b]",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0.84, 0, 1),
            font_style="H5",
            markup=True
        ))
    
        info = f"""
    [b]Name:[/b] {topper.get('Name','')}
    [b]Class:[/b] {topper.get('Class','')}
    [b]Roll:[/b] {topper.get('Roll Number','')}
    [b]Total Marks:[/b] {top_total}
    [b]Average:[/b] {round(top_total/len(topper.get('marks',[])), 2) if topper.get('marks') else 0}
    """
        card.add_widget(MDLabel(text=info, markup=True))
    
        subjects = topper.get("subjects", [])
        marks = topper.get("marks", [])
        total = topper.get("total",[])
        if subjects:
            grid = GridLayout(cols=2, spacing=dp(25), padding=dp(20), size_hint_y=None)
            grid.bind(minimum_height=grid.setter('height'))
            grid.add_widget(MDLabel(text="[b]Subject[/b]", markup=True))
            grid.add_widget(MDLabel(text="[b]Marks[/b]", markup=True))
            for sub, mark in zip(subjects, marks):
                grid.add_widget(MDLabel(text=sub))
                grid.add_widget(MDLabel(text=str(mark)))
            card.add_widget(grid)
    
        layout.add_widget(card)
        scroll.add_widget(layout)
        content.add_widget(scroll)
    
        back_btn = MDFillRoundFlatIconButton(
            text="Back to Dashboard  ",
            size_hint=(0.5, None),
            pos_hint={"center_x": 0.5},
            height=dp(50),
            md_bg_color=(1, 0, 0, 1)
        )
        back_btn.bind(on_release=lambda x: self.show_dashboard())
        content.add_widget(back_btn)
        
           # -------------------- Class Statistics (with Graphs) --------------------

    def class_stats(self):
        import matplotlib.pyplot as plt
        import io
        from kivy.core.image import Image as CoreImage
        from kivy.uix.image import Image
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.widget import Widget
        from kivy.metrics import dp
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDFillRoundFlatIconButton, MDFlatButton
        from kivymd.uix.dialog import MDDialog
        import os
        import json
    
        home = self.root.get_screen("home")
        dashboard = home.ids.dashboard
        content = home.ids.content_area
        dashboard.opacity = 0
        dashboard.disabled = True
        content.clear_widgets()
    
        # ---------------- Load Data ----------------
        if not os.path.exists(self.student_file):
            self.show_dialog("Error", "No student data file found.")
            self.show_dashboard()
            return
    
        with open(self.student_file) as f:
            data = json.load(f)
        if not data:
            self.show_dialog("Info", "No students found!")
            self.show_dashboard()
            return
    
        # ---------------- Compute Stats ----------------
        total_students = len(data)
        total_marks_list = [sum(s.get("marks", [])) for s in data if s.get("marks")]
        overall_avg = round(sum(total_marks_list) / total_students, 2) if total_students else 0
        highest = max(total_marks_list) if total_marks_list else 0
        lowest = min(total_marks_list) if total_marks_list else 0
    
        median = 0
        if total_marks_list:
            sorted_marks = sorted(total_marks_list)
            mid = len(sorted_marks) // 2
            median = sorted_marks[mid] if len(sorted_marks) % 2 != 0 else (sorted_marks[mid - 1] + sorted_marks[mid]) / 2
    
        # ---------------- Top / Bottom 3 Students ----------------
        students_with_marks = [(s.get("Name", ""), sum(s.get("marks", []))) for s in data if s.get("marks")]
        sorted_students = sorted(students_with_marks, key=lambda x: x[1], reverse=True)
        top3 = sorted_students[:3]
        bottom3 = sorted_students[-3:]
    
        # ---------------- Grade Distribution ----------------
        grade_count = {"A+": 0, "A": 0, "B": 0, "C": 0, "F": 0}
        for s in data:
            marks = s.get("marks", [])
            if not marks:
                continue
            avg = sum(marks) / len(marks)
            if avg >= 90:
                grade = "A+"
            elif avg >= 75:
                grade = "A"
            elif avg >= 60:
                grade = "B"
            elif avg >= 50:
                grade = "C"
            else:
                grade = "F"
            grade_count[grade] += 1
    
        # ---------------- Per Subject Average ----------------
        subject_totals, subject_counts = {}, {}
        subject_topper, subject_weak = {}, {}
        for s in data:
            for sub, mark in zip(s.get("subjects", []), s.get("marks", [])):
                if sub:
                    subject_totals[sub] = subject_totals.get(sub, 0) + mark
                    subject_counts[sub] = subject_counts.get(sub, 0) + 1
                    if sub not in subject_topper or mark > subject_topper[sub][1]:
                        subject_topper[sub] = (s.get("Name", ""), mark)
                    if sub not in subject_weak or mark < subject_weak[sub][1]:
                        subject_weak[sub] = (s.get("Name", ""), mark)
        subject_avg = {sub: round(subject_totals[sub] / subject_counts[sub], 2) for sub in subject_totals}
    
        # ---------------- Alerts ----------------
        alerts = []
        for s in data:
            marks = s.get("marks", [])
            avg = sum(marks) / len(marks) if marks else 0
            if avg < 40:
                alerts.append(f"{s.get('Name')} is scoring low overall")
            low_subjects = [sub for sub, mark in zip(s.get("subjects", []), marks) if mark < 35]
            if low_subjects:
                alerts.append(f"{s.get('Name')} is weak in: {', '.join(low_subjects)}")
    
        # ---------------- Layout ----------------
        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))
    
        # ---------------- Utility Functions ----------------
        def make_card(title, content_widgets, height=None):
            card = MDCard(
                orientation="vertical",
                padding=dp(20),
                spacing=dp(10),
                radius=[20] * 4,
                size_hint_y=None,
                md_bg_color=(1, 1, 1, 1),
                height=height or dp(450)
            )
            card.add_widget(MDLabel(
                text=title,
                halign="center",
                markup=True,
                font_style="H6"
            ))
            for w in content_widgets:
                card.add_widget(w)
            return card
    
        def show_student_details(name):
            student_data = next((s for s in data if s.get("Name") == name), None)
            if not student_data:
                return
            details = f"Name: {student_data.get('Name')}\n"
            subjects = student_data.get("subjects", [])
            marks = student_data.get("marks", [])
            for sub, mark in zip(subjects, marks):
                details += f"{sub}: {mark}\n"
            total = sum(marks)
            avg = round(total / len(marks), 2) if marks else 0
            details += f"Total Marks: {total}\nAverage: {avg}"
    
            dialog = MDDialog(
                title=f"{name} Details",
                text=details,
                size_hint=(0.8, None),
                height=dp(400),
                buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
    
        # ---- Summary Card ----
        summary_text = f"""
    [b]Total Students: [/b] {total_students}
    [b]Average Total Marks: [/b] {overall_avg}
    [b]Highest Marks: [/b] {highest}
    [b]Lowest Marks: [/b] {lowest}
    [b]Median Marks: [/b] {median}
    """
        summary_label = MDLabel(
            text=summary_text,
            markup=True,
            halign="left",
            size_hint_y=None,
            text_size=(dp(500), None),
            adaptive_height=True
        )
        layout.add_widget(make_card("[b]Class Statistics Summary[/b]", [summary_label]))
    
        # ---- Top/Bottom 3 Students ----
        tb_widgets = [MDLabel(text="[b]Top 3:[/b]", markup=True, halign="left", size_hint_y=None)]
        for name, marks in top3:
            btn = MDFlatButton(
                text=f"{name}: {marks}",
                size_hint_y=None,
                text_color=(0, 0, 1, 1),
                on_release=lambda x, n=name: show_student_details(n)
            )
            tb_widgets.append(btn)
        tb_widgets.append(MDLabel(text="[b]Bottom 3:[/b]", markup=True, halign="left", size_hint_y=None))
        for name, marks in bottom3:
            btn = MDFlatButton(
                text=f"{name}: {marks}",
                size_hint_y=None,
                text_color=(0, 0, 1, 1),
                on_release=lambda x, n=name: show_student_details(n)
            )
            tb_widgets.append(btn)
        layout.add_widget(make_card("[b]Top & Bottom 3 Students[/b]", tb_widgets))
    
        # ---- Grade Distribution ----
        g_widgets = [MDLabel(text=f"{g}: {c}", halign="left", size_hint_y=None) for g, c in grade_count.items()]
        layout.add_widget(make_card("[b]Grade Distribution[/b]", g_widgets))
    
        # ---- Subject Averages ----
        sub_widgets = []
        if subject_avg:
            for sub, avg in subject_avg.items():
                t_name, t_mark = subject_topper[sub]
                w_name, w_mark = subject_weak[sub]
                sub_widgets.append(MDLabel(
                    text=f"{sub}: Avg={avg}, Topper={t_name}({t_mark}), Weak={w_name}({w_mark})",
                    halign="left",
                    size_hint_y=None,
                    text_size=(dp(500), None),
                    adaptive_height=True
                ))
        else:
            sub_widgets.append(MDLabel(
                text="No subjects available",
                halign="left",
                size_hint_y=None,
                text_size=(dp(500), None),
                adaptive_height=True
            ))
    
        # Card auto-resizes based on content
        subject_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(30),
            radius=[20]*4,
            size_hint_y=None
        )
        subject_card.bind(minimum_height=subject_card.setter("height"))
        subject_card.add_widget(MDLabel(
            text="[b]Subject Averages & Performance[/b]",
            halign="center",
            markup=True,
            font_style="H6"
        ))
        for w in sub_widgets:
            subject_card.add_widget(w)
        layout.add_widget(subject_card)
        
        # ---- Full Class List (Clickable) ----
        from kivymd.uix.button import MDFlatButton
        from kivymd.uix.dialog import MDDialog
        
        # ---- Clickable Student List ----
        student_widgets = [MDLabel(text="[b]All Students:[/b]", markup=True, halign="left", size_hint_y=None)]
        
        def show_student_details_popup(student):
            # Prepare student details text
            marks_text = "\n".join(f"{sub}: {mark}" for sub, mark in zip(student.get("subjects", []), student.get("marks", [])))
            avg = round(sum(student.get("marks", []))/len(student.get("marks", [])),2) if student.get("marks") else 0
            text = f"Name: {student.get('Name')}\nTotal Marks: {sum(student.get('marks', []))}\nAverage: {avg}\n\nMarks:\n{marks_text}"
            
            # Show popup
            MDDialog(
    title="Student Details",
    text=text,
    size_hint=(0.8, None),
    radius=[20, 20, 20, 20],
    md_bg_color=(1,1,1,1),  # popup background (white)
    overlay_color=(0,0,0,0.5) # fully transparent overlay
).open()
        for s in data:
            name = s.get("Name", "Unknown")
            total_marks = sum(s.get("marks", [])) if s.get("marks") else 0
            # Use transparent button
            btn = MDFlatButton(
                text=f"{name}: {total_marks}",
                text_color=(0,0,0,1),  # black text
                on_release=lambda x, stu=s: show_student_details_popup(stu),
                size_hint_y=None
            )
            student_widgets.append(btn)
        
        layout.add_widget(make_card("[b]All Students[/b]", student_widgets, height=None))
    
        # ---- Charts ----
        from kivy.clock import Clock
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import numpy as np
        import io
        from kivy.core.image import Image as CoreImage
        from kivy.uix.image import Image
        from kivy.metrics import dp
        from kivymd.uix.label import MDLabel
        from matplotlib.patches import FancyBboxPatch
        import matplotlib.pyplot as plt
        import numpy as np
        import io
        from kivy.core.image import Image as CoreImage
        from kivy.uix.image import Image
        from kivy.metrics import dp
        from kivymd.uix.label import MDLabel
        
        if subject_avg:
            subs = list(subject_avg.keys())
            avgs = list(subject_avg.values())
        
            fig, ax = plt.subplots(figsize=(10, 10))
            fig.patch.set_facecolor("white")  # <-- yeh add karo
            from matplotlib.ticker import MultipleLocator

# y-axis grid lines aur ticks har 10 units pe
            ax.yaxis.set_major_locator(MultipleLocator(10))
            ax.yaxis.grid(True, linestyle='--', alpha=0.5)

# rest of your plotting code...
        
            # Pop-up colors and shadow effect
            colors = ['#4CAF50' if v == max(avgs) else '#F44336' if v == min(avgs) else '#2196F3' for v in avgs]
        
            # Shadow: slightly offset, darker color behind bars
            for i, (sub, val) in enumerate(zip(subs, avgs)):
                ax.bar(i + 0.05, val, color='grey', alpha=0.3, width=0.5)  # shadow
            bars = ax.bar(np.arange(len(subs)), avgs, color=colors, width=0.5, edgecolor='black')
        
            # Labels
            ax.set_xticks(np.arange(len(subs)))
            ax.set_xticklabels(subs, rotation=25, ha='right')
            ax.set_ylabel("Average Marks")
            
        
            # Annotate values
            for i, v in enumerate(avgs):
                ax.text(i, v + 0.3, str(v), ha='center', va='bottom', fontweight='bold', color='black')
        
            # Optional: subtle grid
            ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        
            # Save to buffer
            buf = io.BytesIO()
            plt.tight_layout()
            fig.savefig(buf, format='png', dpi=150)
            buf.seek(0)
            plt.close(fig)
        
            # Convert to Kivy image
            img = CoreImage(buf, ext="png").texture
            img_widget = Image(texture=img, size_hint_y=None, height=dp(350))
            layout.add_widget(MDLabel(text="[b]Subject Average[/b]", halign="center", markup=True))
            layout.add_widget(img_widget)

        
        #pie
            import matplotlib.pyplot as plt
            import numpy as np
            import io
            from kivy.core.image import Image as CoreImage
            from kivy.uix.image import Image
            from kivy.metrics import dp
            
            grades = list(grade_count.keys())
            values = list(grade_count.values())
            
            if any(values):
                fig, ax = plt.subplots(figsize=(10, 10))
            
                total_students = sum(values)
            
                
                cmap = plt.get_cmap("Pastel1")
                colors = [cmap(i / len(values)) for i in range(len(values))]
            
              
                explode = [0.1 if v == max(values) else 0.02 for v in values]
            
                wedges, texts, autotexts = ax.pie(
                    values,
                    labels=grades,
                    autopct=lambda pct: f"{pct:.1f}%",
                    startangle=90,
                    colors=colors,
                    explode=explode,
                    shadow=True,
                    wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.45}
                )
            
                # Center text with total
                ax.text(0, 0, f"Total\n{total_students}", ha='center', va='center',
                        fontsize=25, fontweight='bold', color='dimgray')
            
                # Style percentages nicely
                for autotext in autotexts:
                    autotext.set_color('black')
                    autotext.set_fontsize(22)
                    autotext.set_fontweight('bold')
            
                
            
                # Save to buffer
                buf = io.BytesIO()
                plt.tight_layout()
                fig.savefig(buf, format='png', dpi=300)
                buf.seek(0)
                plt.close(fig)
            
                # Convert to Kivy image
                img = CoreImage(buf, ext="png").texture
                img_widget = Image(texture=img, size_hint_y=None, height=dp(300))
                layout.add_widget(MDLabel(text="[b]Grade Distribution Chart[/b]", halign="center", markup=True))
                layout.add_widget(img_widget)
        # ---- Alerts ----
        if alerts:
            alert_widgets = []
            for a in alerts:
                btn = MDFlatButton(
                    text=a,
                    size_hint_y=None,
                    text_color=(1, 0, 0, 1),
                    on_release=lambda x, msg=a: self.show_dialog("Alert Detail", msg)
                )
                alert_widgets.append(btn)
            layout.add_widget(make_card("[b]Alerts & Insights[/b]", alert_widgets))
    
        layout.add_widget(Widget(size_hint_y=None, height=dp(50)))  
        scroll.add_widget(layout)
        content.add_widget(scroll)
    
       # ---- Back Button ----
        back_btn = MDFillRoundFlatIconButton(
            text="Back to Dashboard",
            size_hint=(0.5, None),       # Width 50% of parent
            height=dp(50),
            pos_hint={"center_x": 0.5},   # Center horizontally
            md_bg_color=(1, 0, 0, 1),
            on_release=lambda x: self.show_dashboard()
        )
        content.add_widget(back_btn)
        
       
  
    
   

ReportCardMDApp().run()