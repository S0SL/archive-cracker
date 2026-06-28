from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from threading import Thread
import sys
import os

from core.cracker import ArchiveCracker
from core.generator import PasswordGenerator
from core.history import HistoryManager
from core.translations import translator

FONT = 'Chinese'  


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cracker = ArchiveCracker()
        self.generator = PasswordGenerator()
        self.history = HistoryManager()
        self.is_paused = False
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        t = translator.t
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text=t('app_title'), size_hint_y=0.1, font_size=24, font_name=FONT)
        layout.add_widget(title)
        
        archive_layout = BoxLayout(size_hint_y=0.08)
        archive_layout.add_widget(Label(text=t('archive'), size_hint_x=0.2, font_name=FONT))
        self.archive_input = TextInput(hint_text=t('hint_archive'), readonly=True, size_hint_x=0.6, font_name=FONT)
        archive_layout.add_widget(self.archive_input)
        archive_btn = Button(text=t('browse'), size_hint_x=0.2, font_name=FONT)
        archive_btn.bind(on_press=self.select_archive)
        archive_layout.add_widget(archive_btn)
        layout.add_widget(archive_layout)
        
        wordlist_layout = BoxLayout(size_hint_y=0.08)
        wordlist_layout.add_widget(Label(text=t('wordlist'), size_hint_x=0.2, font_name=FONT))
        self.wordlist_input = TextInput(hint_text=t('hint_wordlist'), readonly=True, size_hint_x=0.6, font_name=FONT)
        wordlist_layout.add_widget(self.wordlist_input)
        wordlist_btn = Button(text=t('browse'), size_hint_x=0.2, font_name=FONT)
        wordlist_btn.bind(on_press=self.select_wordlist)
        wordlist_layout.add_widget(wordlist_btn)
        layout.add_widget(wordlist_layout)
        
        settings_layout = BoxLayout(size_hint_y=0.08)
        settings_layout.add_widget(Label(text=t('threads'), size_hint_x=0.2, font_name=FONT))
        self.threads_input = TextInput(text='4', size_hint_x=0.3, font_name=FONT)
        settings_layout.add_widget(self.threads_input)
        settings_layout.add_widget(Label(text=t('format'), size_hint_x=0.2, font_name=FONT))
        self.format_input = TextInput(text=t('auto'), size_hint_x=0.3, font_name=FONT)
        settings_layout.add_widget(self.format_input)
        layout.add_widget(settings_layout)
        
        btn_layout = BoxLayout(size_hint_y=0.1)
        self.start_btn = Button(text=t('start'), background_color=(0, 1, 0, 1), font_name=FONT)
        self.start_btn.bind(on_press=self.start_crack)
        btn_layout.add_widget(self.start_btn)
        
        self.pause_btn = Button(text=t('pause'), disabled=True, font_name=FONT)
        self.pause_btn.bind(on_press=self.pause_crack)
        btn_layout.add_widget(self.pause_btn)
        
        self.stop_btn = Button(text=t('stop'), background_color=(1, 0, 0, 1), disabled=True, font_name=FONT)
        self.stop_btn.bind(on_press=self.stop_crack)
        btn_layout.add_widget(self.stop_btn)
        layout.add_widget(btn_layout)
        
        progress_layout = BoxLayout(orientation='vertical', size_hint_y=0.15)
        
        progress_info = BoxLayout(size_hint_y=0.4)
        self.progress_bar = ProgressBar(max=100, value=0)
        progress_info.add_widget(self.progress_bar)
        self.progress_label = Label(text='0%', size_hint_x=0.15, font_name=FONT)
        progress_info.add_widget(self.progress_label)
        progress_layout.add_widget(progress_info)
        
        self.status_label = Label(text=t('ready'), size_hint_y=0.3, font_name=FONT)
        progress_layout.add_widget(self.status_label)
        self.detail_label = Label(text='', size_hint_y=0.3, font_name=FONT)
        progress_layout.add_widget(self.detail_label)
        layout.add_widget(progress_layout)
        
        nav_layout = BoxLayout(size_hint_y=0.1)
        history_btn = Button(text=t('history'), font_name=FONT)
        history_btn.bind(on_press=self.show_history)
        nav_layout.add_widget(history_btn)
        
        generate_btn = Button(text=t('generate'), font_name=FONT)
        generate_btn.bind(on_press=self.show_generator)
        nav_layout.add_widget(generate_btn)
        
        settings_btn = Button(text=t('settings'), font_name=FONT)
        settings_btn.bind(on_press=self.show_settings)
        nav_layout.add_widget(settings_btn)
        layout.add_widget(nav_layout)
        
        self.add_widget(layout)
    
    def refresh_language(self):
        self.build_ui()
    
    def select_archive(self, *args):
        content = FileChooserIconView()
        content.bind(on_submit=self.on_archive_selected)
        popup = Popup(title=translator.t('select_archive'), content=content, size_hint=(0.9, 0.9))
        self._popup = popup
        popup.open()
    
    def on_archive_selected(self, instance, selection, *args):
        if selection:
            self.archive_input.text = selection[0]
        self._popup.dismiss()
    
    def select_wordlist(self, *args):
        content = FileChooserIconView()
        content.bind(on_submit=self.on_wordlist_selected)
        popup = Popup(title=translator.t('select_wordlist'), content=content, size_hint=(0.9, 0.9))
        self._popup = popup
        popup.open()
    
    def on_wordlist_selected(self, instance, selection, *args):
        if selection:
            self.wordlist_input.text = selection[0]
        self._popup.dismiss()
    
    def start_crack(self, *args):
        archive = self.archive_input.text
        wordlist = self.wordlist_input.text
        
        if not archive or not wordlist:
            self.status_label.text = translator.t('please_select')
            return
        
        try:
            threads = int(self.threads_input.text)
        except:
            threads = 4
        
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.pause_btn.disabled = False
        self.is_paused = False
        
        def callback(event, data):
            Clock.schedule_once(lambda dt: self.update_ui(event, data))
        
        def run():
            self.cracker.crack(archive, wordlist, threads, callback)
            Clock.schedule_once(lambda dt: self.crack_complete())
        
        Thread(target=run, daemon=True).start()
    
    def update_ui(self, event, data):
        t = translator.t
        if event == 'start':
            self.status_label.text = f"{t('starting')} {data['total']} {t('passwords')}"
            self.progress_bar.max = data['total']
            self.progress_label.text = '0%'
        elif event == 'progress':
            self.progress_bar.value = data['current']
            percent = int(data['current'] / data['total'] * 100)
            self.progress_label.text = f"{percent}%"
            self.detail_label.text = f"{t('testing')} {data['password']} | {t('speed')} {data['speed']:.1f}{t('per_sec')}"
        elif event == 'found':
            self.progress_label.text = '100%'
            self.status_label.text = f"{t('password_found')} {data['password']}"
            self.history.add_archive(self.archive_input.text, data['password'])
            self.history.add_password(data['password'], self.archive_input.text)
        elif event == 'not_found':
            self.status_label.text = f"{t('not_found')} {data['tested']} {t('attempts')}"
        elif event == 'stopped':
            self.status_label.text = f"{t('stopped')} {data['tested']} {t('attempts')}"
        elif event == 'error':
            self.status_label.text = f"{t('error')} {data}"
    
    def crack_complete(self):
        t = translator.t
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.pause_btn.disabled = True
        self.pause_btn.text = t('pause')
        self.progress_bar.value = 0
        self.progress_label.text = '0%'
    
    def pause_crack(self, *args):
        t = translator.t
        if self.is_paused:
            self.cracker.resume()
            self.pause_btn.text = t('pause')
            self.is_paused = False
        else:
            self.cracker.pause()
            self.pause_btn.text = t('resume')
            self.is_paused = True
    
    def stop_crack(self, *args):
        self.cracker.stop()
    
    def show_history(self, *args):
        self.manager.current = 'history'
    
    def show_generator(self, *args):
        self.manager.current = 'generator'
    
    def show_settings(self, *args):
        self.manager.current = 'settings'


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = HistoryManager()
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        t = translator.t
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text=t('history'), size_hint_y=0.1, font_size=24, font_name=FONT)
        layout.add_widget(title)
        
        header = BoxLayout(size_hint_y=0.05)
        header.add_widget(Label(text=t('archive'), size_hint_x=0.4, font_name=FONT))
        header.add_widget(Label(text=t('password'), size_hint_x=0.3, font_name=FONT))
        header.add_widget(Label(text=t('time'), size_hint_x=0.3, font_name=FONT))
        layout.add_widget(header)
        
        scroll = ScrollView()
        self.history_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        scroll.add_widget(self.history_list)
        layout.add_widget(scroll)
        
        btn_layout = BoxLayout(size_hint_y=0.1)
        clear_btn = Button(text=t('clear_history'), background_color=(1, 0, 0, 0.5), font_name=FONT)
        clear_btn.bind(on_press=self.clear_history)
        btn_layout.add_widget(clear_btn)
        
        back_btn = Button(text=t('back'), font_name=FONT)
        back_btn.bind(on_press=self.go_back)
        btn_layout.add_widget(back_btn)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
        self.bind(on_enter=self.refresh_history)
    
    def refresh_language(self):
        self.build_ui()
        self.refresh_history()
    
    def refresh_history(self, *args):
        self.history_list.clear_widgets()
        
        archives = self.history.get_recent_archives()
        for archive in archives:
            item = BoxLayout(size_hint_y=None, height=40)
            item.add_widget(Label(text=archive['filename'], size_hint_x=0.4, font_name=FONT))
            if archive.get('password'):
                item.add_widget(Label(text=archive['password'], size_hint_x=0.3, font_name=FONT))
            else:
                item.add_widget(Label(text=translator.t('not_found_text'), size_hint_x=0.3, font_name=FONT))
            time_str = archive.get('timestamp', '')[:16].replace('T', ' ')
            item.add_widget(Label(text=time_str, size_hint_x=0.3, font_name=FONT))
            self.history_list.add_widget(item)
    
    def clear_history(self, *args):
        self.history.clear()
        self.refresh_history()
    
    def go_back(self, *args):
        self.manager.current = 'main'


class GeneratorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generator = PasswordGenerator()
        self.charset_state = {'lower': True, 'upper': True, 'digit': True, 'symbol': False}
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        t = translator.t
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text=t('generate'), size_hint_y=0.1, font_size=24, font_name=FONT)
        layout.add_widget(title)
        
        charset_layout = GridLayout(cols=2, size_hint_y=0.2)
        self.lower_check = Button(text=t('lowercase'), background_color=(0, 1, 0, 0.5), font_name=FONT)
        self.lower_check.bind(on_press=lambda x: self.toggle_charset('lower'))
        charset_layout.add_widget(self.lower_check)
        
        self.upper_check = Button(text=t('uppercase'), background_color=(0, 1, 0, 0.5), font_name=FONT)
        self.upper_check.bind(on_press=lambda x: self.toggle_charset('upper'))
        charset_layout.add_widget(self.upper_check)
        
        self.digit_check = Button(text=t('digits'), background_color=(0, 1, 0, 0.5), font_name=FONT)
        self.digit_check.bind(on_press=lambda x: self.toggle_charset('digit'))
        charset_layout.add_widget(self.digit_check)
        
        self.symbol_check = Button(text=t('symbols'), background_color=(0.5, 0.5, 0.5, 1), font_name=FONT)
        self.symbol_check.bind(on_press=lambda x: self.toggle_charset('symbol'))
        charset_layout.add_widget(self.symbol_check)
        layout.add_widget(charset_layout)
        
        custom_layout = BoxLayout(size_hint_y=0.08)
        custom_layout.add_widget(Label(text=t('custom'), size_hint_x=0.2, font_name=FONT))
        self.custom_input = TextInput(hint_text=t('hint_custom'), size_hint_x=0.8, font_name=FONT)
        custom_layout.add_widget(self.custom_input)
        layout.add_widget(custom_layout)
        
        length_layout = BoxLayout(size_hint_y=0.08)
        length_layout.add_widget(Label(text=t('min_length'), size_hint_x=0.2, font_name=FONT))
        self.min_length = TextInput(text='6', size_hint_x=0.3, font_name=FONT)
        length_layout.add_widget(self.min_length)
        length_layout.add_widget(Label(text=t('max_length'), size_hint_x=0.2, font_name=FONT))
        self.max_length = TextInput(text='12', size_hint_x=0.3, font_name=FONT)
        length_layout.add_widget(self.max_length)
        layout.add_widget(length_layout)
        
        count_layout = BoxLayout(size_hint_y=0.08)
        count_layout.add_widget(Label(text=t('count'), size_hint_x=0.2, font_name=FONT))
        self.count_input = TextInput(text='1000', size_hint_x=0.3, font_name=FONT)
        count_layout.add_widget(self.count_input)
        layout.add_widget(count_layout)
        
        btn_layout = BoxLayout(size_hint_y=0.1)
        generate_btn = Button(text=t('generate_btn'), background_color=(0, 1, 0, 1), font_name=FONT)
        generate_btn.bind(on_press=self.generate)
        btn_layout.add_widget(generate_btn)
        
        save_btn = Button(text=t('save_to_file'), font_name=FONT)
        save_btn.bind(on_press=self.save_to_file)
        btn_layout.add_widget(save_btn)
        layout.add_widget(btn_layout)
        
        scroll = ScrollView()
        self.preview = TextInput(readonly=True, size_hint_y=0.3, font_name=FONT)
        scroll.add_widget(self.preview)
        layout.add_widget(scroll)
        
        back_btn = Button(text=t('back'), size_hint_y=0.08, font_name=FONT)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def refresh_language(self):
        self.build_ui()
    
    def toggle_charset(self, key):
        self.charset_state[key] = not self.charset_state[key]
        btn = getattr(self, f'{key}_check')
        btn.background_color = (0, 1, 0, 0.5) if self.charset_state[key] else (0.5, 0.5, 0.5, 1)
    
    def generate(self, *args):
        self.generator.set_charset(
            lowercase=self.charset_state['lower'],
            uppercase=self.charset_state['upper'],
            digits=self.charset_state['digit'],
            symbols=self.charset_state['symbol'],
            custom=self.custom_input.text
        )
        
        try:
            min_len = int(self.min_length.text)
            max_len = int(self.max_length.text)
            count = int(self.count_input.text)
        except:
            min_len, max_len, count = 6, 12, 1000
        
        self.generator.set_length(min_len, max_len)
        passwords = self.generator.generate_random(count)
        self.preview.text = '\n'.join(passwords[:100])
    
    def save_to_file(self, *args):
        t = translator.t
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=t('filename')))
        filename_input = TextInput(text='generated_passwords.txt', font_name=FONT)
        content.add_widget(filename_input)
        
        btn_layout = BoxLayout()
        save_btn = Button(text=t('save'), font_name=FONT)
        cancel_btn = Button(text=t('cancel'), font_name=FONT)
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title=t('save_passwords'), content=content, size_hint=(0.8, 0.5))
        
        def save(*args):
            self.generator.generate_random(1000, filename_input.text)
            popup.dismiss()
        
        save_btn.bind(on_press=save)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, *args):
        self.manager.current = 'main'


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        t = translator.t
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text=t('settings'), size_hint_y=0.1, font_size=24, font_name=FONT)
        layout.add_widget(title)
        
        settings_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.5)
        
        settings_layout.add_widget(Label(text=t('language'), font_name=FONT))
        lang_layout = BoxLayout(size_hint_x=0.5)
        self.en_btn = Button(
            text='English',
            font_name=FONT,
            background_color=(0, 1, 0, 1) if translator.lang == 'en' else (0.5, 0.5, 0.5, 1)
        )
        self.en_btn.bind(on_press=lambda x: self.on_lang_change('en'))
        lang_layout.add_widget(self.en_btn)
        self.zh_btn = Button(
            text='中文',
            font_name=FONT,
            background_color=(0, 1, 0, 1) if translator.lang == 'zh' else (0.5, 0.5, 0.5, 1)
        )
        self.zh_btn.bind(on_press=lambda x: self.on_lang_change('zh'))
        lang_layout.add_widget(self.zh_btn)
        settings_layout.add_widget(lang_layout)
        
        settings_layout.add_widget(Label(text=t('default_threads'), font_name=FONT))
        self.threads_input = TextInput(text='4', size_hint_x=0.5, font_name=FONT)
        settings_layout.add_widget(self.threads_input)
        
        settings_layout.add_widget(Label(text=t('timeout'), font_name=FONT))
        self.timeout_input = TextInput(text='10', size_hint_x=0.5, font_name=FONT)
        settings_layout.add_widget(self.timeout_input)
        
        settings_layout.add_widget(Label(text=t('auto_detect'), font_name=FONT))
        self.auto_detect = Button(text=t('enabled'), size_hint_x=0.5, background_color=(0, 1, 0, 0.5), font_name=FONT)
        self.auto_detect.bind(on_press=self.toggle_auto_detect)
        settings_layout.add_widget(self.auto_detect)
        
        layout.add_widget(settings_layout)
        
        btn_layout = BoxLayout(size_hint_y=0.15)
        save_btn = Button(text=t('save'), background_color=(0, 1, 0, 1), font_name=FONT)
        save_btn.bind(on_press=self.save_settings)
        btn_layout.add_widget(save_btn)
        
        reset_btn = Button(text=t('reset'), font_name=FONT)
        reset_btn.bind(on_press=self.reset_settings)
        btn_layout.add_widget(reset_btn)
        layout.add_widget(btn_layout)
        
        back_btn = Button(text=t('back'), size_hint_y=0.1, font_name=FONT)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def refresh_language(self):
        self.build_ui()
    
    def on_lang_change(self, lang):
        translator.set_lang(lang)
        self.manager.get_screen('main').refresh_language()
        self.manager.get_screen('history').refresh_language()
        self.manager.get_screen('generator').refresh_language()
        self.build_ui()
    
    def toggle_auto_detect(self, *args):
        t = translator.t
        if self.auto_detect.text == t('enabled'):
            self.auto_detect.text = t('disabled')
            self.auto_detect.background_color = (1, 0, 0, 0.5)
        else:
            self.auto_detect.text = t('enabled')
            self.auto_detect.background_color = (0, 1, 0, 0.5)
    
    def save_settings(self, *args):
        pass
    
    def reset_settings(self, *args):
        self.threads_input.text = '4'
        self.timeout_input.text = '10'
    
    def go_back(self, *args):
        self.manager.current = 'main'


class ArchiveCrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(GeneratorScreen(name='generator'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm


if __name__ == '__main__':
    ArchiveCrackerApp().run()
