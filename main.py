from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen, ScreenManager
from shops import Organisation

Builder.load_file('design.kv')
SHOP_LIST = ["ALBERT", "BILLA", "D-VÝROBCI", "KAUFLAND", "MAKRO", "PENNY", "TESCO", "DROBNÝ DÁRCE", "SBÍRKA POTRAVIN",
             "PBC", "SBÍRKA MODLETICE", "NORMA", "JIP", "DM", "ROSSMANN", "LIDL", "COOP", "JINÉ"]


class StartupScreen(Screen):
    def to_insert_screen(self):
        self.manager.current = "insert_org_screen"

    def to_output_screen(self):
        self.manager.current = "org_output_screen"


class InsertOrgScreen(Screen):
    def on_pre_enter(self, *args):
        db = Organisation('DCHP')

        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_org_name)
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        print(obj.text)
        global org_name
        org_name = obj.text
        self.manager.current = "insert_shop_screen"

    # def on_leave(self, *args):
    #     self.ids.grid.clear_widgets()


class InsertShopScreen(Screen):
    def on_enter(self, *args):
        for i in SHOP_LIST:
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_shop_name)
            self.ids.box.add_widget(btn)

    def get_shop_name(self, obj):
        print(obj.text)
        global shop_name
        shop_name = obj.text
        self.manager.current = "type_and_amount_screen"


class TypeAndAmountScreen(Screen):
    # def on_enter(self, *args):
    #     btn_a = Button(text="A - Sbírka potravin", ids='type_a', size_hint=(.5, .5), on_press=self.change_color)
    #     btn_b = Button(text="B - Čerstvé potraviny", ids='type_b', size_hint=(.5, .5), on_press=self.change_color)
    #     btn_c = Button(text="C - Trvanlivé potraviny a nápoje", ids='type_c', size_hint=(.5, .5),
    #                    on_press=self.change_color)
    #     btn_m = Button(text="M - Materialní a drogérie", ids='type_a', size_hint=(.5, .5), on_press=self.change_color)
    #     btn_a.bind(on_press=lambda x: self.get_type('a'))
    #     btn_b.bind(on_press=lambda x: self.get_type('b'))
    #     btn_c.bind(on_press=lambda x: self.get_type('c'))
    #     btn_m.bind(on_press=lambda x: self.get_type('m'))
    #     self.ids.grid.add_widget(btn_a)
    #     self.ids.grid.add_widget(btn_b)
    #     self.ids.grid.add_widget(btn_c)
    #     self.ids.grid.add_widget(btn_m)

    def get_type(self, input_type):
        global type
        type = input_type
        self.change_color()

    def change_color(self):
        # 3 120 32 rgb for clicked button
        # this part looks like crap, but I haven't figured out how to do it better...
        if type == 'a':
            self.ids.type_a.background_normal = ''
            self.ids.type_b.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_c.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_m.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_a.background_color = (3 / 255, 120 / 255, 32 / 255, 1)
            self.ids.type_b.background_color = (1, 1, 1, 1)
            self.ids.type_c.background_color = (1, 1, 1, 1)
            self.ids.type_m.background_color = (1, 1, 1, 1)
        elif type == 'b':
            self.ids.type_b.background_normal = ''
            self.ids.type_a.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_c.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_m.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_b.background_color = (3 / 255, 120 / 255, 32 / 255, 1)
            self.ids.type_a.background_color = (1, 1, 1, 1)
            self.ids.type_c.background_color = (1, 1, 1, 1)
            self.ids.type_m.background_color = (1, 1, 1, 1)
        elif type == 'c':
            self.ids.type_c.background_normal = ''
            self.ids.type_a.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_b.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_m.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_c.background_color = (3 / 255, 120 / 255, 32 / 255, 1)
            self.ids.type_a.background_color = (1, 1, 1, 1)
            self.ids.type_b.background_color = (1, 1, 1, 1)
            self.ids.type_m.background_color = (1, 1, 1, 1)
        elif type == 'm':
            self.ids.type_m.background_normal = ''
            self.ids.type_a.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_b.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_c.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_m.background_color = (3 / 255, 120 / 255, 32 / 255, 1)
            self.ids.type_a.background_color = (1, 1, 1, 1)
            self.ids.type_b.background_color = (1, 1, 1, 1)
            self.ids.type_c.background_color = (1, 1, 1, 1)

    def confirm(self):
        amount = self.ids.amount.text
        organisation = Organisation(org_name)
        organisation.insert(org_name, shop_name, type, amount)
        self.manager.current = "success_screen"


class OrgOutputScreen(Screen):
    def on_enter(self, *args):
        db = Organisation('DCHP')
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_org_name)
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        print(obj.text)
        global output_org
        output_org = obj.text
        self.manager.current = "text_output_screen"


# THIS DOESN'T WORK YET !!!
class TextOutputScreen(Screen):
    def on_enter(self):
        org = Organisation(output_org)
        amount = org.get_type_amount(output_org)
        self.ids.content_text.text = str(amount)

    def return_to_menu(self):
        self.manager.transition.direction = "left"
        self.manager.current = "startup_screen"


class RootWidget(ScreenManager):
    pass


class SuccessScreen(Screen):
    def return_to_menu(self):
        self.manager.transition.direction = "left"
        self.manager.current = "startup_screen"


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
