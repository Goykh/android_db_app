from kivy.app import App
from kivy.graphics import Line
from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.uix.screenmanager import Screen, ScreenManager

from shops import Organisation

Builder.load_file('design.kv')
SHOP_LIST = ["ALBERT", "BILLA", "D-VÝROBCI", "KAUFLAND", "MAKRO", "PENNY", "TESCO", "DROBNÝ\nDÁRCE", "SBÍRKA\nPOTRAVIN",
             "PBC", "SBÍRKA\nMODLETICE", "NORMA", "JIP", "DM", "ROSSMANN", "LIDL", "COOP", "JINÉ"]


class StartupScreen(Screen):
    def to_insert_screen(self):
        self.manager.current = "insert_org_screen"

    def to_output_screen(self):
        self.manager.current = "org_output_screen"


class InsertOrgScreen(Screen):
    def on_enter(self, *args):
        db = Organisation('DCHP')
        self.ids.box.clear_widgets()
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_org_name, valign='center',
                         halign='center', font_size='14')
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        print(obj.text)
        global org_name
        org_name = obj.text
        self.manager.current = "insert_shop_screen"


class InsertShopScreen(Screen):
    def on_enter(self, *args):
        self.ids.box.clear_widgets()
        for i in SHOP_LIST:
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_shop_name, valign='center',
                         halign='center', font_size='14')
            self.ids.box.add_widget(btn)

    def get_shop_name(self, obj):
        print(obj.text)
        global shop_name
        shop_name = obj.text
        self.manager.current = "type_and_amount_screen"


class TypeAndAmountScreen(Screen):

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
        global input_amount
        input_amount = self.ids.amount.text
        organisation = Organisation(org_name)
        organisation.insert(org_name, shop_name, type, input_amount)
        self.manager.current = "success_screen"


class OrgOutputScreen(Screen):
    def on_enter(self, *args):
        self.ids.box.clear_widgets()
        db = Organisation('DCHP')
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_org_name, valign='center',
                         halign='center', font_size='14')
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        global output_org
        output_org = obj.text
        self.manager.current = "text_output_screen"


class TextOutputScreen(Screen):
    def on_enter(self):
        self.ids.output_grid.clear_widgets()
        org = Organisation(output_org)
        amount = org.get_type_amount(output_org)
        for i in amount:
            lb1 = Label(text=str(i[0]), color=(0, 0, 0, 1), markup=True, font_size='14')
            lb2 = Label(text=str(i[1]), color=(0, 0, 0, 1), markup=True, font_size='14')
            lb3 = Label(text=str(i[2]), color=(0, 0, 0, 1), markup=True, font_size='14')
            self.ids.output_grid.add_widget(lb1)
            self.ids.output_grid.add_widget(lb2)
            self.ids.output_grid.add_widget(lb3)

            # I WANT TO ADD A LINE IN BETWEEN THE ROWS, NEED TO FIGURE OUT HOW
            # line = Line(points=[], cap='none', width=2)
            # self.ids.output_grid.add_widget(line)

    def return_to_previous_screen(self):
        self.manager.transition.direction = "left"
        self.manager.current = "org_output_screen"

    def return_to_menu(self):
        self.manager.transition.direction = "left"
        self.manager.current = "startup_screen"

class RootWidget(ScreenManager):
    pass


class SuccessScreen(Screen):
    def on_enter(self, *args):
        label = Label(
            text=f'{org_name} - {shop_name} -  {type.upper()} - {input_amount}kg',
            color=(0, 0, 0, 1))
        self.ids.success_grid.add_widget(label)

    def return_to_menu(self):
        self.manager.transition.direction = "left"
        self.manager.current = "startup_screen"


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
