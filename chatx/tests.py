from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from django.test import TestCase
from django.test import Client


class ChatxTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_chatx_works(self):
        response = self.client.get('/chat/')
        self.assertEqual(200, response.status_code)
        
    def test_view_roomname_chatx(self):
        response = self.client.get('/chat/skater')
        print(response)

class ChatxTestTrue(ChannelsLiveServerTestCase):
    server_static = True
    
    @classmethod
    def setUpClass(cls):
        drive_exec_path="/home/ubuntu/workspace/download/chromedriver"
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        chrome_options.binary_location = '/usr/bin/X11/chromium-browser'
        super().setUpClass()
        try:
            cls.driver = webdriver.Chrome(
                executable_path=drive_exec_path,
                chrome_options=chrome_options
                )
        except:
            super().tearDownClass()
            raise
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
        
    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        try:
            self._enter_chat_room('room_1')

            self._open_new_window()
            self._enter_chat_room('room_1')

            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value,
                'Message was not received by window 1 from window 1')
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value,
                'Message was not received by window 2 from window 1')
        finally:
            self._close_all_new_windows()
    
    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        try:
            self._enter_chat_room('room_1')

            self._open_new_window()
            self._enter_chat_room('room_2')

            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value,
                'Message was not received by window 1 from window 1')

            self._switch_to_window(1)
            self._post_message('world')
            WebDriverWait(self.driver, 2).until(lambda _:
                'world' in self._chat_log_value,
                'Message was not received by window 2 from window 2')
            self.assertTrue('hello' not in self._chat_log_value,
                'Message was improperly received by window 2 from window 1')
        finally:
            self._close_all_new_windows()
            
    # === Utility ===

    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + '/chat/')
        ActionChains(self.driver).send_keys(room_name + '\n').perform()
        WebDriverWait(self.driver, 2).until(lambda _:
            room_name in self.driver.current_url)

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(self.driver.window_handles[0])

    def _switch_to_window(self, window_index):
        self.driver.switch_to_window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message + '\n').perform()

    @property
    def _chat_log_value(self):
        return self.driver.find_element_by_css_selector('#chat-log')\
                .get_property('value')
        
        
        