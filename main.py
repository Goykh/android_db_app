from kivy.app import App
from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.label import Label
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
    def on_enter(self, *args):
        db = Organisation('DCHP')
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_org_name)
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        print(obj.text)
        global org_name
        org_name = obj.text
        self.manager.current = "insert_shop_screen"


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
    def get_type(self, input_type):
        global type
        if input_type == "a":
            type = "a"
        elif input_type == "b":
            type = "b"
        elif input_type == "c":
            type = "c"
        elif input_type == "m":
            type = "c"

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

#THIS DOESN'T WORK YET !!!
class TextOutputScreen(Screen):
    def show_amount(self):
        org = Organisation(output_org)
        amount = org.get_type_amount(output_org)
        l = Label(text=f'[color=ff3333]{amount}[/color]', markup=True)
        self.ids.box.add_widget(l)
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
