import kivy.uix.screenmanager as kv_screenmanager
import kivy.uix.anchorlayout as kv_anchorlayout
import kivy.uix.boxlayout as kv_boxlayout
import kivy.uix.label as kv_label
import kivy.uix.button as kv_button

class StoryScreen(kv_screenmanager.Screen):
    initialized = False
    widgets = {}
    story = None

    def on_pre_enter(self):
        if not self.initialized:
            self.initialized = False # for now everything is regenerated everytime
            self.widgets["title_layout"] = kv_anchorlayout.AnchorLayout(anchor_x = "center", anchor_y = "top")
            self.widgets["title_layout"].add_widget(Label(text=self.story.get_title(), size_hint = (0.1,0.1)))
            
            self.widgets["exit_layout"] = kv_anchorlayout.AnchorLayout(anchor_x = "left", anchor_y = "bottom")
            self.widgets["exit_layout"].add_widget(kv_button.Button(
                background_normal = 'images/arrow_left.png',
                background_down = 'images/arrow_left.png',
                size_hint = (.2, .1),
                border = [1,1,1,1],
                on_press = lambda i: self.goto_newgame()))

            self.widgets["center_layout"] = kv_anchorlayout.AnchorLayout(anchor_x = "center", anchor_y = "center")
            self.widgets["center_layout"].add_widget(kv_boxlayout.BoxLayout(orientation = 'vertical', size_hint = (0.5, 0.7)))
            self.widgets["center_layout"].children[0].add_widget(kv_label.Label(text = self.story.get_summary()))
            self.widgets["center_layout"].children[0].add_widget(kv_button.Button(
                text = "Begin Story",
                on_press = lambda i: self.run_chapter(self.story.get_first_chapter())))

        for name,widget in self.widgets.items():
            self.add_widget(widget)

    def on_leave(self):
        self.clear_widgets()

    def goto_newgame(self):
        self.manager.current = "newgame"

    def run_chapter(self, chapter):
        self.clear_widgets()
        self.widgets["title_layout"].children[0].text=chapter.get_title()
        
        self.widgets["center_layout"] = kv_anchorlayout.AnchorLayout(anchor_x = "center", anchor_y = "center")
        self.widgets["center_layout"].add_widget(Label(text=chapter.get_summary()))
        
        self.widgets["bottom_layout"] = kv_anchorlayout.AnchorLayout(anchor_x = "center", anchor_y = "bottom")
        self.widgets["bottom_layout"].add_widget(kv_button.Button(
            text = "Begin Chapter",
            size_hint = (.2, .1),
            on_press = lambda i: self.run_paragraph(chapter.get_first_paragraph())))
        
        for name,widget in self.widgets.items():
            self.add_widget(widget)
    
    def run_paragraph(self, paragraph):
        self.clear_widgets()
        self.widgets = {}
        
        self.widgets["center_layout"] = kv_anchorlayout.AnchorLayout(anchor_x = "center", anchor_y = "center", size_hint = (0.9,0.9))
        self.widgets["center_layout"].add_widget(kv_label.Label(
            text_size = (400,400),
            text = paragraph.get_text(),
            halign = "center",
            valign = "center"))
        
        self.widgets["choices_layout"] = kv_anchorlayout.AnchorLayout(anchor_x = "center", anchor_y = "bottom")
        self.widgets["choices_layout"].add_widget(kv_boxlayout.BoxLayout(orientation='vertical', size_hint = (0.5, 0.2)))
        
        for choice in paragraph.get_choices():
            self.widgets["choices_layout"].children[0].add_widget(kv_button.Button(
                text = choice.get_text(),
                on_press = lambda i: self.run_paragraph(choice.get_paragraph())
                ))
        
        for name,widget in self.widgets.items():
            self.add_widget(widget)
    
    
   

