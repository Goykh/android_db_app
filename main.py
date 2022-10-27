from kivy.app import App

from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

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
        global shop_name
        shop_name = obj.text
        self.manager.current = "type_and_amount_screen"


class TypeAndAmountScreen(Screen):

    def on_pre_enter(self, *args):
        global type
        type = ''
        self.ids.calculator_input.text = ''
        self.ids.type_a.background_normal = 'atlas://data/images/defaulttheme/button'
        self.ids.type_b.background_normal = 'atlas://data/images/defaulttheme/button'
        self.ids.type_c.background_normal = 'atlas://data/images/defaulttheme/button'
        self.ids.type_m.background_normal = 'atlas://data/images/defaulttheme/button'

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

    # Calculator functions!
    def clear(self):
        self.ids.calculator_input.text = ''

    # method to press buttons
    def button_press(self, button):
        # variable that is the previous input in the input area
        previous_number = self.ids.calculator_input.text
        # checks if there is a number (it shouldn't be, but better to be safe)
        if previous_number in ['0', '+', '-', '*']:
            self.ids.calculator_input.text = f'{button}'
        else:
            self.ids.calculator_input.text += f'{button}'

    def math_operation(self, pressed_button):
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith('+') or previous_number.endswith('-') or previous_number.endswith('*'):
            self.ids.calculator_input.text = previous_number[:-1] + f'{pressed_button}'
        else:
            self.ids.calculator_input.text += f'{pressed_button}'

    def decimal_click(self):
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith('.'):
            pass
        elif previous_number.endswith('+') or previous_number.endswith('-') or previous_number.endswith(
                '*') or self.ids.calculator_input.text == '':
            self.ids.calculator_input.text += '0.'
        else:
            self.ids.calculator_input.text += '.'

    def equals(self):
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith('+') or previous_number.endswith('-') or previous_number.endswith('*'):
            evaluation = eval(previous_number[:-1])
        else:
            evaluation = eval(previous_number)
        self.ids.calculator_input.text = str(evaluation)

    def confirm(self):
        # this needs work on too
        global input_amount
        input_amount = self.ids.calculator_input.text
        if input_amount == '':
            popup = Popup(
                title='Nastala chyba!',
                auto_dismiss=True,
                size_hint=(.6, .3),
                pos_hint={'x': .2, 'top': .7},
                content=Label(text='Zadání není správné! Můžete zadat jenom čísla'))
            popup.open()
        elif input_amount.isdigit() is False:
            for i in input_amount:
                if i.isalpha():
                    popup = Popup(
                        title='Nastala chyba!',
                        auto_dismiss=True,
                        size_hint=(.6, .3),
                        pos_hint={'x': .2, 'top': .7},
                        content=Label(text='Zadání není správné! Můžete zadat jenom čísla.'))
                    popup.open()
                else:
                    continue
        else:
            if type in ['a', 'b', 'c', 'm']:
                self.manager.current = "success_screen"
            else:
                popup = Popup(
                    title='Nastala chyba!',
                    auto_dismiss=True,
                    size_hint=(.6, .3),
                    pos_hint={'x': .2, 'top': .7},
                    content=Label(text='Nevybrali jste typ!!!'))
                popup.open()


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
    # TODO: 2 new buttons:
    # 1. button: go back to edit the input on the screen before if input was wrong
    # 2. button: go back to InsertShopScreen to pick another shop for the same org
    # make the sql query (.insert()) on this button or the return_to_menu button
    #
    # organisation = Organisation(org_name)
    # organisation.insert(org_name, shop_name, type, input_amount)

    def on_enter(self, *args):
        label = Label(
            text=f'{org_name} - {shop_name} -  {type.upper()} - {input_amount}kg',
            color=(0, 0, 0, 1))
        self.ids.query_output.add_widget(label)

    def return_to_calculator(self):
        self.manager.transition.direction = "left"
        self.manager.current = 'type_and_amount_screen'

    def return_to_org_screen(self):
        organisation = Organisation(org_name)
        organisation.insert(org_name, shop_name, type, input_amount)
        self.manager.transition.direction = "left"
        self.manager.current = "insert_shop_screen"

    def return_to_menu(self):
        organisation = Organisation(org_name)
        organisation.insert(org_name, shop_name, type, input_amount)
        self.manager.transition.direction = "left"
        self.manager.current = "startup_screen"


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
