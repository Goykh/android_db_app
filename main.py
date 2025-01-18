from kivy import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import partial
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import platform

from database_protocol import DatabaseProtocol
from models import Organization, Shop
from services.date import convert_tz_and_format

# from shops import Organisation

Builder.load_file("design.kv")

# Global variables
# have to be used to used data from one screen
# on a different screen

# Input variables:
org_name = ""
shop_name = ""
donation_type = ""
input_amount = ""
# Output variable:
output_org = ""


class StartupScreen(Screen):
    """
    The fist screen you enter when you open the app,
    it has two buttons, one to add data and the other one to read data.
    """

    def to_insert_screen(self):
        self.manager.current = "insert_org_screen"

    def to_output_screen(self):
        self.manager.current = "org_output_screen"

    def to_settings_screen(self) -> None:
        self.manager.current = "settings_screen"


class SettingsScreen(Screen):
    """
    The settings screen.
    You can create a new organization and new shop from here.
    """

    # TODO: Add option to reset all DB values
    def on_pre_enter(self, *args) -> None:
        self.manager.transition.direction = "left"

    def to_add_org_screen(self) -> None:
        self.manager.current = "add_org_screen"

    def to_add_shop_screen(self) -> None:
        self.manager.current = "add_shop_screen"

    def to_delete_org_screen(self) -> None:
        self.manager.current = "delete_org_screen"

    def to_delete_org_shop(self) -> None:
        self.manager.current = "delete_shop_screen"

    def back_button(self) -> None:
        self.manager.current = "startup_screen"
        self.manager.transition.direction = "right"


class AddOrgScreen(Screen):
    """
    Screen to add an organization.
    """

    def on_pre_enter(self, *args) -> None:
        self.manager.transition.direction = "left"

    # TODO: Add option to edit existing orgs/delete them?

    def confirm_org(self) -> None:
        org_name = self.ids.org_name.text
        # validate
        db_conn = DatabaseProtocol()
        if db_conn.check_record_exists(name=org_name, model=Organization):
            popup = Popup(
                title="Nastala chyba!",
                auto_dismiss=True,
                size_hint=(0.6, 0.3),
                pos_hint={"x": 0.2, "top": 0.7},
                content=Label(text="Organizace se zadaným jménem už existuje."),
            )
            popup.open()
        # create record
        db_conn.create_record(Organization, org_name)
        # return to settings screen
        self.back_button()

    def back_button(self):
        self.manager.current = "settings_screen"
        self.manager.transition.direction = "right"


class AddShopScreen(Screen):
    """
    Screen to add a shop.
    """

    def on_pre_enter(self, *args) -> None:
        self.manager.transition.direction = "left"

    def confirm_shop(self) -> None:
        shop_name = self.ids.shop_name.text
        # validate
        db_conn = DatabaseProtocol()
        if db_conn.check_record_exists(name=shop_name, model=Shop):
            popup = Popup(
                title="Nastala chyba!",
                auto_dismiss=True,
                size_hint=(0.6, 0.3),
                pos_hint={"x": 0.2, "top": 0.7},
                content=Label(text="Obchod se zadaným jménem už existuje."),
            )
            popup.open()
        # create record
        db_conn.create_record(Organization, shop_name)
        # return to settings screen
        self.back_button()

    def back_button(self):
        self.manager.current = "settings_screen"
        self.manager.transition.direction = "right"


class DeleteOrgScreen(Screen):
    def on_pre_enter(self, *args):
        self.manager.transition.direction = "left"
        # clearing the widgets
        self.ids.box_delete_org.clear_widgets()
        # reset scrollview to the top
        self.ids.scroll_org_delete.scroll_y = 1
        db_conn = DatabaseProtocol()
        for org in db_conn.get_all_records(Organization):
            btn = Button(
                text=str(org.name),
                size_hint_y=None,
                height=dp(70),
                on_release=self.delete_org,
                valign="center",
                halign="center",
                font_size=sp(14),
            )
            self.ids.box_delete_org.add_widget(btn)

    def delete_org(self, obj: Button):
        """
        Attempts to find the org record in the DB.
        Opens a different popup depending on the result.
        :param obj: text on the button you pressed
        """
        org_name = obj.text
        db_conn = DatabaseProtocol()
        org = db_conn.get_record_by_name(Organization, org_name)
        error_popup = Popup(
            title="Nastala chyba!",
            auto_dismiss=True,
            size_hint=(0.6, 0.3),
            pos_hint={"x": 0.2, "top": 0.7},
            content=Label(text="Něco se pokazilo..."),
        )
        if not org:
            error_popup.content = Label(text="Zadaná organizace neexistuje.")
            error_popup.open()
            return
        if len(org) != 1:
            error_popup.content = Label(text="Bylo nalezeno více než jedna organizace se stejným jménem.")
            error_popup.open()
            return
        confirm_btn = Button(text="Ano!")
        deny_btn = Button(text="Ne!")
        grid = GridLayout(cols=2, size_hint=(1, 0.5))
        grid.add_widget(confirm_btn)
        grid.add_widget(deny_btn)

        popup = Popup(
            title=f"Opravdu chcete smazat {org_name}?",
            auto_dismiss=True,
            size_hint=(0.6, 0.3),
            pos_hint={"x": 0.2, "top": 0.7},
            content=grid,
        )
        confirm_btn.bind(on_press=partial(self.delete_org_confirm, popup, org[0]))
        deny_btn.bind(on_press=popup.dismiss)

        popup.open()

    def delete_org_confirm(self, popup: Popup, org: Organization, *args) -> None:
        """
        Processes the deletion of the organization in the DB.
        If unsuccessful, opens a popup.
        Refreshes the screen to reload the buttons
        :param popup: the confirmation popup of the deletion
        :param org: the given org to delete
        :return: None
        """
        db_conn = DatabaseProtocol()
        res = db_conn.delete_record(Organization, org.id)
        popup.dismiss()

        if not res:
            error_popup = Popup(
                title="Nastala chyba!",
                auto_dismiss=True,
                size_hint=(0.6, 0.3),
                pos_hint={"x": 0.2, "top": 0.7},
                content=Label(text="Nepovedlo se smazat organizaci..."),
            )
            error_popup.open()
        self.on_pre_enter()

    def back_button(self):
        self.manager.current = "settings_screen"
        self.manager.transition.direction = "right"


class DeleteShopScreen(Screen):
    def on_pre_enter(self, *args):
        self.manager.transition.direction = "left"
        # clearing the widgets
        self.ids.box_delete_shop.clear_widgets()
        # reset scrollview to the top
        self.ids.scroll_shop_delete.scroll_y = 1
        db_conn = DatabaseProtocol()
        for shop in db_conn.get_all_records(Shop):
            btn = Button(
                text=str(shop.name),
                size_hint_y=None,
                height=dp(70),
                on_release=self.delete_shop,
                valign="center",
                halign="center",
                font_size=sp(14),
            )
            self.ids.box_delete_shop.add_widget(btn)

    def delete_shop(self, obj: Button):
        """
        Attempts to find the shop record in the DB.
        Opens a different popup depending on the result.
        :param obj: text on the button you pressed
        """
        shop_name = obj.text
        db_conn = DatabaseProtocol()
        shop = db_conn.get_record_by_name(Shop, shop_name)
        error_popup = Popup(
            title="Nastala chyba!",
            auto_dismiss=True,
            size_hint=(0.6, 0.3),
            pos_hint={"x": 0.2, "top": 0.7},
            content=Label(text="Něco se pokazilo..."),
        )
        if not shop:
            error_popup.content = Label(text="Zadaný obchod neexistuje.")
            error_popup.open()
            return
        if len(shop) != 1:
            error_popup.content = Label(text="Bylo nalezeno více než jeden obchod se stejným jménem.")
            error_popup.open()
            return
        confirm_btn = Button(text="Ano!")
        deny_btn = Button(text="Ne!")
        grid = GridLayout(cols=2, size_hint=(1, 0.5))
        grid.add_widget(confirm_btn)
        grid.add_widget(deny_btn)

        popup = Popup(
            title=f"Opravdu chcete smazat {shop_name}?",
            auto_dismiss=True,
            size_hint=(0.6, 0.3),
            pos_hint={"x": 0.2, "top": 0.7},
            content=grid,
        )
        confirm_btn.bind(on_press=partial(self.delete_shop_confirm, popup, shop[0]))
        deny_btn.bind(on_press=popup.dismiss)

        popup.open()

    def delete_shop_confirm(self, popup: Popup, shop: Shop, *args) -> None:
        """
        Processes the deletion of the shop in the DB.
        If unsuccessful, opens a popup.
        Refreshes the screen to reload the buttons
        :param popup: the confirmation popup of the deletion
        :param shop: the given shop to delete
        :return: None
        """
        db_conn = DatabaseProtocol()
        res = db_conn.delete_record(Shop, shop.id)
        popup.dismiss()

        if not res:
            error_popup = Popup(
                title="Nastala chyba!",
                auto_dismiss=True,
                size_hint=(0.6, 0.3),
                pos_hint={"x": 0.2, "top": 0.7},
                content=Label(text="Nepovedlo se smazat obchod..."),
            )
            error_popup.open()
        self.on_pre_enter()

    def back_button(self):
        self.manager.current = "settings_screen"
        self.manager.transition.direction = "right"


class InsertOrgScreen(Screen):
    """
    Screen where you pick the organisation to add data.
    """

    def on_pre_enter(self, *args):
        """
        Method to dynamically generate all the organisations as buttons.
        the on_enter() makes it generate when you enter the screen.
        """
        self.manager.transition.direction = "left"
        # clearing the widgets
        # mainly when you re-enter the screen so the buttons don't generate again
        # on top of the old ones
        self.ids.box.clear_widgets()
        # reset scrollview to the top
        self.ids.scroll_org.scroll_y = 1
        db_conn = DatabaseProtocol()
        for org in db_conn.get_all_records(Organization):
            btn = Button(
                text=str(org.name),
                size_hint_y=None,
                height=dp(70),
                on_release=self.get_org_name,
                valign="center",
                halign="center",
                font_size=sp(14),
            )
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
        self.manager.current = "startup_screen"
        self.manager.transition.direction = "right"


class InsertShopScreen(Screen):
    """
    Same screen as before but with shops.
    """

    def on_pre_enter(self, *args):
        """
        Method to dynamically generate all the shops as buttons from the shops in the DB.
        The on_enter() makes it generate when you enter the screen.
        """
        global org_name
        self.manager.transition.direction = "left"
        self.ids.box.clear_widgets()
        # reset scrollview to the top
        self.ids.scroll_shop.scroll_y = 1
        self.ids.shop_label.text = org_name
        db_conn = DatabaseProtocol()
        for shop in db_conn.get_all_records(Shop):
            btn = Button(
                text=str(shop.name),
                size_hint_y=None,
                height=dp(70),
                on_release=self.get_shop_name,
                valign="center",
                halign="center",
                font_size=sp(14),
            )
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
        self.manager.get_screen("type_and_amount_screen").ids.calculator_input.text = ""
        self.manager.current = "type_and_amount_screen"

    def back_button(self):
        self.manager.current = "insert_org_screen"
        self.manager.transition.direction = "right"


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
        self.manager.transition.direction = "left"
        self.ids.type_amount_label.text = f"{org_name} - {shop_name}"
        global donation_type
        donation_type = ""
        self.ids.type_a.state = "normal"
        self.ids.type_b.state = "normal"
        self.ids.type_c.state = "normal"
        self.ids.type_m.state = "normal"

    @staticmethod
    def get_type(input_type):
        """
        Method to get the type of food as a global variable.
        :param input_type: text on the button you pressed
        """
        global donation_type
        donation_type = input_type

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
        if previous_number in ["0", "+", "-", "*"]:
            # adds input to text area
            self.ids.calculator_input.text = f"{pressed_button}"
        else:
            # adds input to text area
            self.ids.calculator_input.text += f"{pressed_button}"

    def math_operation(self, pressed_button):
        """
        Method when a math operation button is pressed (+, - or *).
        Checks if the input area isn't already ending with one of the signs.
        If yes, it replaces it.
        :param pressed_button:  value of the pressed button
        """
        # previous input in the text input area
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith("+") or previous_number.endswith("-") or previous_number.endswith("*"):
            self.ids.calculator_input.text = previous_number[:-1] + f"{pressed_button}"
        else:
            self.ids.calculator_input.text += f"{pressed_button}"

    def decimal_click(self):
        """
        Method for the decimal button.
        Checks if it's already in the input text
        or the text is ending with any other math operator.
        If yes, it replaces it.
        """
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith("."):
            pass
        elif (
            previous_number.endswith("+")
            or previous_number.endswith("-")
            or previous_number.endswith("*")
            or self.ids.calculator_input.text == ""
        ):
            self.ids.calculator_input.text += "0."
        else:
            self.ids.calculator_input.text += "."

    def equals(self):
        """
        Gets called when the '=' button is pressed.
        Uses the eval built in to calculate the result.
        If the input text area is ending with a math operator (+, -, *)
        It does the eval without it.
        """
        previous_number = self.ids.calculator_input.text
        if previous_number.endswith("+") or previous_number.endswith("-") or previous_number.endswith("*"):
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
        if input_amount == "":
            popup = Popup(
                title="Nastala chyba!",
                auto_dismiss=True,
                size_hint=(0.6, 0.3),
                pos_hint={"x": 0.2, "top": 0.7},
                content=Label(text="Zadání není správné! Můžete zadat jenom čísla"),
            )
            popup.open()
        # checks if any index in the input amount is a letter
        for i in input_amount:
            if i.isalpha():
                popup = Popup(
                    title="Nastala chyba!",
                    auto_dismiss=True,
                    size_hint=(0.6, 0.3),
                    pos_hint={"x": 0.2, "top": 0.7},
                    content=Label(text="Zadání není správné! Můžete zadat jenom čísla."),
                )
                popup.open()

        # checks if food type has been selected, if not. Creates popup
        if donation_type in ["a", "b", "c", "m"]:
            self.manager.current = "success_screen"
        else:
            popup = Popup(
                title="Nastala chyba!",
                auto_dismiss=True,
                size_hint=(0.6, 0.3),
                pos_hint={"x": 0.2, "top": 0.7},
                content=Label(text="Nevybrali jste typ!!!"),
            )
            popup.open()

    def back_button(self):
        self.manager.current = "insert_shop_screen"
        self.manager.transition.direction = "right"


class SuccessScreen(Screen):
    """
    You get a list of donations made in the session.
    Generates 3 buttons to edit, add again or go back menu.
    """

    @classmethod
    def _process_donation(self) -> None:
        """
        Processes the donation in the db.
        Finds all the necessary records.
        Opens popups if errors happen.
        :return: None
        """
        db_conn = DatabaseProtocol()
        org = db_conn.get_record_by_name(Organization, org_name)
        shop = db_conn.get_record_by_name(Shop, shop_name)
        try:
            float(input_amount)
        except ValueError:
            Logger.exception("PB_APP: Invalid input amount...")
            popup = Popup(
                title="Nastala chyba!",
                auto_dismiss=True,
                size_hint=(0.6, 0.3),
                pos_hint={"x": 0.2, "top": 0.7},
                content=Label(text="Neplatná hodnota množství!"),
            )
            popup.open()
            return

        res = db_conn.make_donation(org, shop, donation_type, input_amount)
        if not res:
            popup = Popup(
                title="Nastala chyba!",
                auto_dismiss=True,
                size_hint=(0.6, 0.3),
                pos_hint={"x": 0.2, "top": 0.7},
                content=Label(text="Nepovedlo se provést operaci..."),
            )
            popup.open()

    def on_pre_enter(self, *args):
        """
        On enter generates a label with the data you just added.
        For now, it stacks for every entry you did in the current session.
        """
        # declaring the self.label, so I can access it in a function below
        self.manager.transition.direction = "left"
        self.ids.scroll_success.scroll_y = 1
        self.label = Label(
            text=f"{org_name} - {shop_name} -  {donation_type.upper()} - {input_amount}kg",
            color=(0, 0, 0, 1),
            font_size=sp(20),
            size_hint_y=None,
            height=dp(70),
        )
        self.label.bind()
        self.ids.query_output.add_widget(self.label)

    def return_to_calculator(self):
        """
        Returns to the previous screen if you see a mistake in the newest label.
        Also deletes the newest label.
        """
        self.ids.query_output.remove_widget(self.label)
        self.manager.current = "type_and_amount_screen"
        self.manager.transition.direction = "right"

    def return_to_org_screen(self):
        """
        Returns to the screen where you pick a shop from the list
        so, you can add more data to one organisation.
        """
        self._process_donation()
        self.manager.current = "insert_shop_screen"
        self.manager.transition.direction = "right"

    def return_to_menu(self):
        """
        Returns to the startup_screen.
        """
        self._process_donation()
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
        self.manager.transition.direction = "left"
        self.ids.box.clear_widgets()
        # reset scrollview to the top
        self.ids.scroll_out_org.scroll_y = 1
        db_conn = DatabaseProtocol()
        for org in db_conn.get_all_records(Organization):
            btn = Button(
                text=str(org.name),
                size_hint_y=None,
                height=dp(70),
                on_release=self.get_org_name,
                valign="center",
                halign="center",
                font_size=sp(14),
            )
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
        self.manager.current = "startup_screen"
        self.manager.transition.direction = "right"


class TextOutputScreen(Screen):
    """
    Screen that outputs the data for an org.
    """

    def on_pre_enter(self):
        """
        Builds a list of all donations for the selected organization.
        """
        # clears widgets on screen
        self.manager.transition.direction = "left"
        self.ids.output_grid.clear_widgets()
        db_conn = DatabaseProtocol()
        org = db_conn.get_record_by_name(Organization, output_org)
        donations = db_conn.get_organization_donations(org.id)
        for donation in donations:
            lb1 = Label(text=str(donation[0]), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb2 = Label(text=str(donation[1]), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb3 = Label(text=f"{str(donation[2])}", color=(0, 0, 0, 1), markup=True, font_size=sp(15))
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

    @staticmethod
    def extract_data_to_xlsx():
        if platform == "android":
            db_conn = DatabaseProtocol()
            db_conn.to_xlsx_file()

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
        Gets all the detailed donations of the selected org.
        """
        # clears widgets on screen
        self.manager.transition.direction = "left"
        self.ids.detailed_grid.clear_widgets()
        db_conn = DatabaseProtocol()
        org = db_conn.get_record_by_name(Organization, output_org)
        donations = db_conn.get_detailed_organization_donations(org.id)
        for donation in donations:
            date = convert_tz_and_format(donation.create_date)
            lb1 = Label(text=str(donation.shop_id.name), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb2 = Label(text=str(donation.type), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
            lb3 = Label(text=str(f"{donation.type.amount}kg"), color=(0, 0, 0, 1), markup=True, font_size=sp(15))
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

    # TODO: Rework the whole deletion part!!!
    def delete_data(self):
        grid = GridLayout(cols=2, size_hint=(1, 0.5))

        confirm_button = Button(text="Ano!")
        deny_button = Button(text="Ne!")

        grid.add_widget(confirm_button)
        grid.add_widget(deny_button)

        popup = Popup(
            title="Opravdu chcete vymazat celou tabulku?",
            auto_dismiss=True,
            size_hint=(0.6, 0.3),
            pos_hint={"x": 0.2, "top": 0.7},
            content=grid,
        )

        confirm_button.bind(on_press=self.delete_confirm)
        confirm_button.bind(on_press=popup.dismiss)
        deny_button.bind(on_press=popup.dismiss)
        popup.open()

    def delete_confirm(self, button):
        # TODO: Rework the whole deletion
        #  org = Organisation(output_org)
        #  org.delete_data_in_table(output_org)
        self.manager.current = "org_output_screen"
        self.manager.transition.direction = "right"


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
