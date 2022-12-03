from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import sp, dp
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from shops import Organisation

Builder.load_file('design.kv')

# List of shops to generate buttons
SHOP_LIST = ["ALBERT", "BILLA", "D-VÝROBCI", "KAUFLAND", "MAKRO", "PENNY", "TESCO", "DROBNÝ\nDÁRCE", "SBÍRKA\nPOTRAVIN",
             "PBC", "SBÍRKA\nMODLETICE", "NORMA", "JIP", "DM", "ROSSMANN", "LIDL", "COOP", "JINÉ"]

# Global variables
# have to be used to used data from one screen
# on a different screen

# Input variables:
org_name = ''
shop_name = ''
food_type = ''
input_amount = ''
# Output variable:
output_org = ''


class StartupScreen(Screen):
    """
    The fist screen you enter when you open the app,
    it has two buttons, one to add data and the other one to read data.
    """

    def to_insert_screen(self):
        self.manager.current = "insert_org_screen"

    def to_output_screen(self):
        self.manager.current = "org_output_screen"


class InsertOrgScreen(Screen):
    """
    Screen where you pick the organisation to add data.
    """

    def on_pre_enter(self, *args):
        """
        Method to dynamically generate all the organisations as buttons.
        the on_enter() makes it generate when you enter the screen.
        """
        self.manager.transition.direction = 'left'
        # calling the db, I picked one org as default, I should change this in the future
        db = Organisation('DCHP')
        # clearing the widgets
        # mainly when you re-enter the screen so the buttons don't generate again
        # on top of the old ones
        self.ids.box.clear_widgets()
        # reset scrollview to the top
        self.ids.scroll_org.scroll_y = 1
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=dp(50), on_release=self.get_org_name, valign='center',
                         halign='center', font_size=sp(14))
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        """
        Method to get the name of the organisation as a global variable.
        :param obj: text on the button you pressed
        """
        global org_name
        org_name = obj.text
        self.manager.current = "insert_shop_screen"

    def back_button(self):
        self.manager.current = 'startup_screen'
        self.manager.transition.direction = 'right'


class InsertShopScreen(Screen):
    """
    Same screen as before but with shops.
    """

    def on_pre_enter(self, *args):
        """
        Method to dynamically generate all the shops as buttons from the SHOP_LIST constant.
        the on_enter() makes it generate when you enter the screen.
        """
        self.manager.transition.direction = 'left'
        self.ids.box.clear_widgets()
        # reset scrollview to the top
        self.ids.scroll_shop.scroll_y = 1
        for i in SHOP_LIST:
            btn = Button(text=str(i), size_hint_y=None, height=dp(50), on_release=self.get_shop_name, valign='center',
                         halign='center', font_size=sp(14))
            self.ids.box.add_widget(btn)

    def get_shop_name(self, obj):
        """
        Method to get the name of the shop as a global variable.
        :param obj: text on the button you pressed
        """
        global shop_name
        shop_name = obj.text
        # Setting the text input on the calculator on the next screen here
        # so when you come back to repair it from the screen after that
        # the number will stay
        self.manager.get_screen('type_and_amount_screen').ids.calculator_input.text = ''
        self.manager.current = "type_and_amount_screen"

    def back_button(self):
        self.manager.current = 'insert_org_screen'
        self.manager.transition.direction = 'right'


class TypeAndAmountScreen(Screen):
    """
    Screen with 4 buttons to pick the food type
    and a calculator layout below it to add the amount.
    """

    def on_pre_enter(self, *args):
        """
        Clears the screen before entering it.
        Resets anything that has been set before.
        """
        self.manager.transition.direction = 'left'
        global food_type
        food_type = ''
        self.ids.type_a.state = 'normal'
        self.ids.type_b.state = 'normal'
        self.ids.type_c.state = 'normal'
        self.ids.type_m.state = 'normal'

    @staticmethod
    def get_type(input_type):
        """
        Method to get the type of food as a global variable.
        :param input_type: text on the button you pressed
        """
        global food_type
        food_type = input_type

    # Calculator functions!!!
    def delete_last_number(self):
        """
        Method for when you press the << button on the calculator.
        Deletes the last character in the input box.
        """
        self.ids.calculator_input.text = self.ids.calculator_input.text[:-1]

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
            previous_number = self.ids.calculator_input.text[:-1]
        try:
            evaluation = eval(previous_number)
            self.ids.calculator_input.text = str(evaluation)
        except Exception:
            self.ids.calculator_input.text = "Chyba, zadali jste neplatný znak!"

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

    def back_button(self):
        self.manager.current = 'insert_shop_screen'
        self.manager.transition.direction = 'right'


class SuccessScreen(Screen):
    """
    You get a list of transactions made in the session.
    Generates 3 buttons to edit, add again or go back menu.
    """

    def on_pre_enter(self, *args):
        """
        On enter generates a label with the data you just added.
        For now, it stacks for every entry you did in the current session.
        """
        # declaring the self.label, so I can access it in a function below
        self.manager.transition.direction = 'left'
        self.label = Label(
            text=f'{org_name} - {shop_name} -  {food_type.upper()} - {input_amount}kg',
            color=(0, 0, 0, 1), font_size=sp(20))
        self.ids.query_output.add_widget(self.label)

    def return_to_calculator(self):
        """
        Returns to the previous screen if you see a mistake in the newest label.
        Also deletes the newest label.
        """
        self.ids.query_output.remove_widget(self.label)
        self.manager.current = 'type_and_amount_screen'
        self.manager.transition.direction = "right"

    def return_to_org_screen(self):
        """
        Returns to the screen where you pick a shop from the list
        so, you can add more data to one organisation.
        Also makes the SQL query to add all the data to the database.
        """
        organisation = Organisation(org_name)
        organisation.insert(org_name, shop_name, food_type, input_amount)
        self.manager.current = "insert_shop_screen"
        self.manager.transition.direction = "right"

    def return_to_menu(self):
        """
        Returns to the startup_screen.
        Also makes the SQL query to add all the data to the database.
        """
        organisation = Organisation(org_name)
        organisation.insert(org_name, shop_name, food_type, input_amount)
        self.manager.current = "startup_screen"
        self.manager.transition.direction = "right"


class OrgOutputScreen(Screen):
    """
    Screen to pick orgs to the output screen.
    Basically a copy of the InsertOrgScreen.
    """

    def on_pre_enter(self, *args):
        """
        Method to dynamically generate all the organisations as buttons.
        the on_enter() makes it generate when you enter the screen.
        """
        self.manager.transition.direction = 'left'
        self.ids.box.clear_widgets()
        # reset scrollview to the top
        self.ids.scroll_out_org.scroll_y = 1
        db = Organisation('DCHP')
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=dp(50), on_release=self.get_org_name, valign='center',
                         halign='center', font_size=sp(14))
            self.ids.box.add_widget(btn)

    def get_org_name(self, obj):
        """
        Method to get the name of the organisation as a global variable.
        :param obj: text on the button you pressed
        """
        global output_org
        output_org = obj.text
        self.manager.current = "text_output_screen"

    def back_button(self):
        self.manager.current = 'startup_screen'
        self.manager.transition.direction = 'right'


class TextOutputScreen(Screen):
    """
    Screen that outputs the data for an org.
    """

    def on_pre_enter(self):
        """
        On entering generates labels with the data from the .get_type_amount() method
        from shops.py
        """
        # clears widgets on screen
        self.manager.transition.direction = 'left'
        self.ids.output_grid.clear_widgets()
        org = Organisation(output_org)
        amount = org.get_type_amount(output_org)
        for i in amount:
            lb1 = Label(text=str(i[0]), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb2 = Label(text=str(i[1]), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb3 = Label(text=f'{str(i[2])}', color=(0, 0, 0, 1), markup=True, font_size=sp(15))
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
        self.manager.current = "org_output_screen"
        self.manager.transition.direction = "right"

    def extract_data_to_xlsx(self):
        org = Organisation(output_org)
        org.to_xlsx_file(output_org)

    def return_to_menu(self):
        """
        Returns to main screen
        """
        self.manager.current = "startup_screen"
        self.manager.transition.direction = "right"

    def to_detailed_output(self):
        self.manager.current = "detailed_output_screen"


class DetailedOutputScreen(Screen):
    """
    Shows detailed data.
    Each row in the DB table, so basically every query done.
    Has a method to delete all data in table.
    Will add a method to delete only one row in the future.
    """

    def on_pre_enter(self):
        """

        """
        # clears widgets on screen
        self.manager.transition.direction = 'left'
        self.ids.detailed_grid.clear_widgets()
        org = Organisation(output_org)
        data = org.get_all_table_data(output_org)
        for i in data:
            reversed_date = i[4][:10]  # YYYY-MM-DD format
            date = f"{reversed_date[8:]}-{reversed_date[5:7]}-{reversed_date[:4]}"  # DD-MM-YYYY format
            lb1 = Label(text=str(i[1]), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb2 = Label(text=str(i[2]), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb3 = Label(text=str(f'{i[3]}kg'), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb4 = Label(text=str(date), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            self.ids.detailed_grid.add_widget(lb1)
            self.ids.detailed_grid.add_widget(lb2)
            self.ids.detailed_grid.add_widget(lb3)
            self.ids.detailed_grid.add_widget(lb4)

    def return_to_previous_screen(self):
        """
        Return to previous screen to see first output screen
        """
        self.manager.current = "text_output_screen"
        self.manager.transition.direction = "right"

    def return_to_menu(self):
        """
        Returns to main screen
        """
        self.manager.current = "startup_screen"
        self.manager.transition.direction = "right"

    def delete_data(self):
        grid = GridLayout(cols=2, size_hint=(1, .5))

        confirm_button = Button(text='Ano!')
        deny_button = Button(text='Ne!')

        grid.add_widget(confirm_button)
        grid.add_widget(deny_button)

        popup = Popup(
            title='Opravdu chcete vymazat celou tabulku?',
            auto_dismiss=True,
            size_hint=(.6, .3),
            pos_hint={'x': .2, 'top': .7},
            content=grid)

        confirm_button.bind(on_press=self.delete_confirm)
        confirm_button.bind(on_press=popup.dismiss)
        deny_button.bind(on_press=popup.dismiss)
        popup.open()

    def delete_confirm(self, button):
        org = Organisation(output_org)
        org.delete_data_in_table(output_org)
        self.manager.current = "org_output_screen"
        self.manager.transition.direction = "right"


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
