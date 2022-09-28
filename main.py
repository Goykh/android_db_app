from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from shops import Organisation

Builder.load_file('design.kv')


class StartupScreen(Screen):
    def to_insert_screen(self):
        self.manager.current = "insert_screen"

    def to_output_screen(self):
        self.manager.current = "output_screen"


class InsertScreen(Screen):
    def on_enter(self, *args):
        db = Organisation("dchp")
        for i in db.org_list():
            btn = Button(text=str(i), size_hint_y=None, height=50)
            self.ids.box.add_widget(btn)


    # def confirm(self):
    #     org = self.ids.org_name.text
    #     shop = self.ids.shop_name.text
    #     typ = self.ids.type.text
    #     amount = self.ids.amount.text
    #     organisation = Organisation(org)
    #     organisation.insert(org, shop, typ, amount)
    #     self.manager.current = "success_screen"

    def show_amount(self):
        org = self.ids.org_name.text
        shop = self.ids.shop_name.text
        typ = self.ids.type.text
        organisation = Organisation(org)
        organisation.get_type_amount(org, shop, typ)


class OutputScreen(Screen):
    def show_amount(self):
        org = self.ids.out_org_name.text
        shop = self.ids.out_shop_name.text
        typ = self.ids.out_type.text
        organisation = Organisation(org)
        amount = organisation.get_type_amount(org, shop, typ)
        if amount[0]:
            self.ids.out_org.text = f"Možství pro organizaci {org.capitalize()} " \
                                    f"z obchodu {shop.capitalize()} typu {amount[0]}kg."
        else:
            self.ids.out_org.text = f"Nebyl nalezen žádný záznam."

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
