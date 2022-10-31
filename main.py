from kivy.app import App

from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from kivy.uix.screenmanager import Screen, ScreenManager

from shops import Organisation

Builder.load_file('design.kv')
# List of shops to generate buttons
SHOP_LIST = ["ALBERT", "BILLA", "D-VÝROBCI", "KAUFLAND", "MAKRO", "PENNY", "TESCO", "DROBNÝ\nDÁRCE", "SBÍRKA\nPOTRAVIN",
             "PBC", "SBÍRKA\nMODLETICE", "NORMA", "JIP", "DM", "ROSSMANN", "LIDL", "COOP", "JINÉ"]


class StartupScreen(Screen):
    # The fist screen you enter when you open the app
    # it has two buttons, one to add data and the other one to read data
    def to_insert_screen(self):
        self.manager.current = "insert_org_screen"

    def to_output_screen(self):
        self.manager.current = "org_output_screen"


class InsertOrgScreen(Screen):
    # Screen where you pick the organisation to add data
    def on_enter(self, *args):
        """
        Method to dynamically generate all the organisations as buttons.
        the on_enter() makes it generate when you enter the screen.
        """
        # calling the db, I picked one org as default, I should change this in the future
        db = Organisation('DCHP')
        # clearing the widgets
        # mainly when you re-enter the screen so the buttons don't generate again
        # on top of the old ones
        self.ids.box.clear_widgets()
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_org_name, valign='center',
                         halign='center', font_size='14')
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        """
        Method to get the name of the organisation as a global variable.
        :param obj: text on the button you pressed
        """
        global org_name
        org_name = obj.text
        self.manager.current = "insert_shop_screen"


class InsertShopScreen(Screen):
    # same screen as before but with shops
    def on_enter(self, *args):
        """
        Method to dynamically generate all the shops as buttons from the SHOP_LIST constant.
        the on_enter() makes it generate when you enter the screen.
        """
        self.ids.box.clear_widgets()
        for i in SHOP_LIST:
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_shop_name, valign='center',
                         halign='center', font_size='14')
            self.ids.box.add_widget(btn)

    def get_shop_name(self, obj):
        """
        Method to get the name of the shop as a global variable.
        :param obj: text on the button you pressed
        """
        global shop_name
        shop_name = obj.text
        self.manager.current = "type_and_amount_screen"


class TypeAndAmountScreen(Screen):
    # screen with 4 buttons to pick the food type
    # and a calculator layout below it to add the amount
    def on_pre_enter(self, *args):
        # THIS SHOULD RESET THE COLOURS OF THE BUTTONS
        # WHEN YOU RE-ENTER THE SCREEN
        # BUT IT DOES NOT WORK YET
        self.ids.calculator_input.text = ''
        self.ids.type_a.background_normal = 'atlas://data/images/defaulttheme/button'
        self.ids.type_b.background_normal = 'atlas://data/images/defaulttheme/button'
        self.ids.type_c.background_normal = 'atlas://data/images/defaulttheme/button'
        self.ids.type_m.background_normal = 'atlas://data/images/defaulttheme/button'

    def get_type(self, input_type):
        """
        Method to get the type of food as a global variable.
        :param obj: text on the button you pressed
        """
        global food_type
        food_type = input_type
        self.change_color()

    def change_color(self):
        """
        Changes the colour of the clicked button to green
        and back to grey when you click a different button.
        I know that this is ugly AF and I need to rewrite this.
        """
        # 3 120 32 rgb for clicked button
        # this part looks like crap, but I haven't figured out how to do it better...
        if food_type == 'a':
            self.ids.type_a.background_normal = ''
            self.ids.type_b.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_c.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_m.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_a.background_color = (3 / 255, 120 / 255, 32 / 255, 1)
            self.ids.type_b.background_color = (1, 1, 1, 1)
            self.ids.type_c.background_color = (1, 1, 1, 1)
            self.ids.type_m.background_color = (1, 1, 1, 1)
        elif food_type == 'b':
            self.ids.type_b.background_normal = ''
            self.ids.type_a.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_c.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_m.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_b.background_color = (3 / 255, 120 / 255, 32 / 255, 1)
            self.ids.type_a.background_color = (1, 1, 1, 1)
            self.ids.type_c.background_color = (1, 1, 1, 1)
            self.ids.type_m.background_color = (1, 1, 1, 1)
        elif food_type == 'c':
            self.ids.type_c.background_normal = ''
            self.ids.type_a.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_b.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_m.background_normal = 'atlas://data/images/defaulttheme/button'
            self.ids.type_c.background_color = (3 / 255, 120 / 255, 32 / 255, 1)
            self.ids.type_a.background_color = (1, 1, 1, 1)
            self.ids.type_b.background_color = (1, 1, 1, 1)
            self.ids.type_m.background_color = (1, 1, 1, 1)
        elif food_type == 'm':
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
        """
        Method for when you press the C button on the calculator.
        Clears the text input area and shows the hint_text.
        """
        self.ids.calculator_input.text = ''

    # method to press buttons
    def button_press(self, pressed_button):
        """
        Method gets called when a number button on the calculator is pressed.
        Text is then added to the text input area.
        :param pressed_button: value of the pressed button
        """
        # variable that is the previous input in the input area
        previous_number = self.ids.calculator_input.text
        # checks if there is a number (it shouldn't be, but better to be safe)
        if previous_number in ['0', '+', '-', '*']:
            # adds input to text area
            self.ids.calculator_input.text = f'{pressed_button}'
        else:
            # adds input to text area
            self.ids.calculator_input.text += f'{pressed_button}'

    def math_operation(self, pressed_button):
        """
        Method when a math operation button is pressed (+, - or *).
        Checks if the input area isn't already ending with one of the signs.
        If yes, it replaces it.
        :param pressed_button:  value of the pressed button
        """
        # previous input in the text input area
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith('+') or previous_number.endswith('-') or previous_number.endswith('*'):
            self.ids.calculator_input.text = previous_number[:-1] + f'{pressed_button}'
        else:
            self.ids.calculator_input.text += f'{pressed_button}'

    def decimal_click(self):
        """
        Method for the decimal button.
        Checks if it's already in the input text
        or the text is ending with any other math operator.
        If yes, it replaces it.
        """
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith('.'):
            pass
        elif previous_number.endswith('+') or previous_number.endswith('-') or previous_number.endswith(
                '*') or self.ids.calculator_input.text == '':
            self.ids.calculator_input.text += '0.'
        else:
            self.ids.calculator_input.text += '.'

    def equals(self):
        """
        Gets called when the '=' button is pressed.
        Uses the eval built in to calculate the result.
        If the input text area is ending with a math operator (+, -, *)
        It does the eval without it.
        """
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith('+') or previous_number.endswith('-') or previous_number.endswith('*'):
            evaluation = eval(previous_number[:-1])
        else:
            evaluation = eval(previous_number)
        self.ids.calculator_input.text = str(evaluation)

    def confirm(self):
        # this is not done yet
        """
        Gets called when the confirm button is pressed.
        Creates global variable with the amount.
        Looks for possible errors.
        If error is found, it generates a popup window
        to tell the user what was wrong.
        """
        global input_amount
        input_amount = self.ids.calculator_input.text
        # checks if input amount is empty
        if input_amount == '':
            popup = Popup(
                title='Nastala chyba!',
                auto_dismiss=True,
                size_hint=(.6, .3),
                pos_hint={'x': .2, 'top': .7},
                content=Label(text='Zadání není správné! Můžete zadat jenom čísla'))
            popup.open()
        # checks if any index in the input amount is a letter
        for i in input_amount:
            if i.isalpha():
                popup = Popup(
                    title='Nastala chyba!',
                    auto_dismiss=True,
                    size_hint=(.6, .3),
                    pos_hint={'x': .2, 'top': .7},
                    content=Label(text='Zadání není správné! Můžete zadat jenom čísla.'))
                popup.open()

        # checks if food type has been selected, if not. Creates popup
        if food_type in ['a', 'b', 'c', 'm']:
            self.manager.current = "success_screen"
        else:
            popup = Popup(
                title='Nastala chyba!',
                auto_dismiss=True,
                size_hint=(.6, .3),
                pos_hint={'x': .2, 'top': .7},
                content=Label(text='Nevybrali jste typ!!!'))
            popup.open()


class SuccessScreen(Screen):
    # TODO: 2 new buttons:
    # 1. button: go back to edit the input on the screen before if input was wrong
    # 2. button: go back to InsertShopScreen to pick another shop for the same org
    # make the sql query (.insert()) on this button or the return_to_menu button
    #
    # organisation = Organisation(org_name)
    # organisation.insert(org_name, shop_name, type, input_amount)

    # Confirmation screen
    # You get a list of transactions made in the session.
    # Generates 3 buttons to edit, add again or go back menu.
    def on_enter(self, *args):
        """
        On enter generates a label with the data you just added.
        For now it stacks for every entry you did in the current session.
        """
        # declaring the self.label so I can access it in a function below
        self.label = Label(
            text=f'{org_name} - {shop_name} -  {food_type.upper()} - {input_amount}kg',
            color=(0, 0, 0, 1))
        self.ids.query_output.add_widget(self.label)

    def return_to_calculator(self):
        """
        Returns to the previous screen if you see a mistake in the newest label.
        Also deletes the newest label.
        """
        self.ids.query_output.remove_widget(self.label)
        self.manager.transition.direction = "left"
        self.manager.current = 'type_and_amount_screen'

    def return_to_org_screen(self):
        """
        Returns to the screen where you pick a shop from the list
        so you can add more data to one organisation.
        Also makes the SQL query to add all the data to the database.
        """
        organisation = Organisation(org_name)
        organisation.insert(org_name, shop_name, food_type, input_amount)
        self.manager.transition.direction = "left"
        self.manager.current = "insert_shop_screen"

    def return_to_menu(self):
        """
        Returns to the startup_screen.
        Also makes the SQL query to add all the data to the database.
        """
        organisation = Organisation(org_name)
        organisation.insert(org_name, shop_name, food_type, input_amount)
        self.manager.transition.direction = "left"
        self.manager.current = "startup_screen"


class OrgOutputScreen(Screen):
    # Screen to pick orgs to the output screen
    # basically a copy of the InsertOrgScreen
    def on_enter(self, *args):
        """
        Method to dynamically generate all the organisations as buttons.
        the on_enter() makes it generate when you enter the screen.
        """
        self.ids.box.clear_widgets()
        db = Organisation('DCHP')
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=50, on_release=self.get_org_name, valign='center',
                         halign='center', font_size='14')
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        """
        Method to get the name of the organisation as a global variable.
        :param obj: text on the button you pressed
        """
        global output_org
        output_org = obj.text
        self.manager.current = "text_output_screen"


class TextOutputScreen(Screen):
    # Screen that outputs the data for a org.
    def on_pre_enter(self):
        """
        On entering generates labels with the data from the .get_type_amount() method
        from shops.py
        """
        # clears widgets on screen
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
        """
        Return to previous screen to see data from a different org
        """
        self.manager.transition.direction = "left"
        self.manager.current = "org_output_screen"

    def return_to_menu(self):
        """
        Returns to main screen
        """
        self.manager.transition.direction = "left"
        self.manager.current = "startup_screen"

    def to_detailed_output(self):
        self.manager.current = "detailed_output_screen"


class DetailedOutputScreen(Screen):
    def on_pre_enter(self):
        """

        """
        # clears widgets on screen
        self.ids.detailed_grid.clear_widgets()
        org = Organisation(output_org)
        data = org.get_all_table_data(output_org)
        for i in data:
            reversed_date = i[4][:10]  # YYYY-MM-DD format
            date = f"{reversed_date[8:]}-{reversed_date[5:7]}-{reversed_date[:4]}"  # DD-MM-YYYY format
            lb1 = Label(text=str(i[1]), color=(0, 0, 0, 1), markup=True, font_size='14')
            lb2 = Label(text=str(i[2]), color=(0, 0, 0, 1), markup=True, font_size='14')
            lb3 = Label(text=str(i[3]), color=(0, 0, 0, 1), markup=True, font_size='14')
            lb4 = Label(text=str(date), color=(0, 0, 0, 1), markup=True, font_size='14')
            self.ids.detailed_grid.add_widget(lb1)
            self.ids.detailed_grid.add_widget(lb2)
            self.ids.detailed_grid.add_widget(lb3)
            self.ids.detailed_grid.add_widget(lb4)


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
