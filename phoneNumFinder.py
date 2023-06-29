from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import phonenumbers
from phonenumbers import carrier, geocoder, timezone


class PhoneNumberInfoApp(App):
    def build(self):
        self.title = 'Phone Number Information'
        layout = BoxLayout(orientation='vertical', spacing=10)
        HB = BoxLayout(orientation='horizontal', spacing=10)

        label = Label(text='Enter Phone number with country code\n(+xx xxxxxxxxx):', font_size=70,
                      color=(0.0, 0.65, 0.95, 1.0))
        self.phone_input = TextInput(hint_text='Enter the phone number', font_size=70,
                                     foreground_color=(0.0, 0.0, 0.0, 1.0), background_color=(1.0, 1.0, 1.0, 1.0))
        button = Button(text='GET INFO', background_normal='', background_color=(0.0, 0.65, 0.95, 1.0), font_size=70)
        button.bind(on_press=self.get_phone_number_info)

        HB.add_widget(label)
        HB.add_widget(self.phone_input)
        layout.add_widget(HB)

        VB = BoxLayout(orientation='vertical', spacing=10)
        clear_button = Button(text='CLEAR', background_normal='', background_color=(0.0, 0.65, 0.95, 1.0),font_size=70)
        clear_button.bind(on_press=self.clear_input)
        VB.add_widget(button)
        VB.add_widget(clear_button)
        layout.add_widget(VB)

        self.info_output = TextInput(readonly=True, multiline=True, hint_text='Your info will be shown here',
                                      foreground_color=(0.0, 0.0, 0.0, 1.0), background_color=(1.0, 1.0, 1.0, 1.0), font_size=40)
        scrollview = ScrollView()
        scrollview.add_widget(self.info_output)
        layout.add_widget(scrollview)

        return layout

    def get_phone_number_info(self, instance):
        phone_number = self.phone_input.text.strip()
        
        if not phone_number:
            self.show_popup("Input Error", "Please enter a phone number.")
            return
        
        if not phone_number.startswith("+"):
            self.show_popup("Input Error", "Phone number must start with '+' symbol.")
            return
        
        try:
            parsed_number = phonenumbers.parse(phone_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            self.show_popup("Input Error", "Invalid phone number format.")
            return

        if not parsed_number.country_code:
            self.show_popup("Input Error", "Invalid phone number format.")
            return

        if len(phone_number) > 15:
            self.show_popup("Input Error", "Phone number exceeds maximum length.")
            return

        if phonenumbers.is_valid_number(parsed_number):
            info_text = "Phone Number belongs to region: {}\n".format(
                ", ".join(timezone.time_zones_for_number(parsed_number)))
            info_text += "Service Provider: {}\n".format(carrier.name_for_number(parsed_number, "en"))
            info_text += "Phone number belongs to country: {}\n".format(geocoder.description_for_number(parsed_number,
                                                                                                        "en"))
            info_text += "Formatted phone number: {}\n".format(
                phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
            info_text += "National number: {}\n".format(
                phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL))
            info_text += "E.164 format: {}\n".format(
                phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164))
            info_text += "RFC3966 format: {}\n".format(
                phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.RFC3966))
            info_text += "Normalized phone number: {}\n".format(phonenumbers.normalize_digits_only(str(parsed_number)))
            info_text += "Is a possible number: {}\n".format(phonenumbers.is_possible_number(parsed_number))
            info_text += "Country code: {}\n".format(parsed_number.country_code)
            info_text += "National number: {}\n".format(parsed_number.national_number)
            info_text += "Extension: {}\n".format(parsed_number.extension)

            self.info_output.text = info_text
        else:
            self.show_popup("Invalid Phone Number", "Please enter a valid mobile number")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message, color=(1,1,1,1)))

        button = Button(text='OK', size_hint_y=None, height=40, background_normal='',
                    background_color=(0.0, 0.65, 0.95, 1.0))
        content.add_widget(button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 300))
        button.bind(on_press=popup.dismiss)

        popup.open()


    def clear_input(self, instance):
        self.phone_input.text = ''
        self.info_output.text = ''


if __name__ == '__main__':
    PhoneNumberInfoApp().run()
