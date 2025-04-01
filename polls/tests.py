from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        # opts.add_argument("--headless") # si quieres modo sin interfaz
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Creamos superusuario en la BD de test
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_admin(self):
        # Ir a la pantalla de login del admin
        self.selenium.get(f'{self.live_server_url}/admin/login/')
        # Login
        self.selenium.find_element(By.NAME, "username").send_keys('isard')
        self.selenium.find_element(By.NAME, "password").send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        # Comprobar que hemos entrado
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

# Create your tests here.
