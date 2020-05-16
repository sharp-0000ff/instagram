from django.test import TestCase, Client
from instagram_profile import models
from instagram_profile import views
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

# Create your tests here.


class PhotographyCreateViewTestCase(TestCase):

    def setUp(self):
        super(PhotographyCreateViewTestCase, self).setUp()
        self.client = Client()
        self.user = models.User.objects.create_user(username='root',  password='root')
        self.user.save()
        self.image = SimpleUploadedFile(name='test_image.jpg',
                                        content=open(r'E:\django\project\media\unknown.jpeg', 'rb').read(),
                                        content_type='image/jpeg')

    def test_redirect_if_not_logged_in(self):
        response = self.client.post('/create/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='root')
        response = self.client.get(reverse('instagram_profile:create_photography_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photographs/create_photography.html')

    def test_photography_created_return_302(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/create/', {'photo': self.image, 'description': 'test_photo'})
        self.assertEqual(response.status_code, 302)

    def test_created_one_photography(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/create/', {'photo': self.image, 'description': 'test_photo'})
        photo = models.Photography.objects.get()
        self.assertEqual(photo.description, 'test_photo')

    def test_get_absolute_url(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/create/', {'photo': self.image, 'description': 'test_photo'})
        photo = models.Photography.objects.get(pk=1)
        self.assertEqual(photo.get_absolute_url(), '/1/')


class PhotographyDetailViewTestCase(TestCase):

    def setUp(self):
        super(PhotographyDetailViewTestCase, self).setUp()
        self.client = Client()
        self.user = models.User.objects.create_user(username='root',  password='root')
        self.user.save()
        self.image = SimpleUploadedFile(name='test_image.jpg',
                                        content=open(r'E:\django\project\media\unknown.jpeg', 'rb').read(),
                                        content_type='image/jpeg')
        self.new_photo = models.Photography.objects.create(pk=1,
                                                           photo=self.image,
                                                           description='test',
                                                           user_id=self.user.pk)
        self.new_photo.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.post('/1/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/1/')
        self.assertEqual(response.status_code, 200)

    def test_comment_created_return_302(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/1/', {'name': 'name',
                                            'body': 'body',
                                            'publish': '2020-01-01',
                                            'email': 'email@email.com'})
        self.assertEqual(response.status_code, 302)

    def test_created_one_comment(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/1/', {'name': 'name',
                                            'body': 'body',
                                            'publish': '2020-01-01',
                                            'email': 'email@email.com'})
        comment = models.Comment.objects.get()
        self.assertEqual(comment.body, 'body')

    def test_for_invalid_comment_if_logged_in(self):
        self.client.login(username='root', password='root')
        response = self.client.post('/1/', {'name': 'name',
                                            'body': 'body',
                                            'publish': '2020-01-01',
                                            'email': 'email@email.com'})
        comment = models.Comment.objects.get()
        self.assertFalse(comment.pk == 2)


class PhotographyDeleteViewTestCase(TestCase):

    def setUp(self):
        super(PhotographyDeleteViewTestCase, self).setUp()
        self.client = Client()
        self.user = models.User.objects.create_user(username='root',  password='root')
        self.user.save()
        self.image = SimpleUploadedFile(name='test_image.jpg',
                                        content=open(r'E:\django\project\media\unknown.jpeg', 'rb').read(),
                                        content_type='image/jpeg')
        self.new_photo = models.Photography.objects.create(pk=1,
                                                           photo=self.image,
                                                           description='test',
                                                           user_id=self.user.pk)
        self.new_photo.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.post('/1/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/1/')
        self.assertEqual(response.status_code, 200)

    # def test_photography_deleted_return_302(self):
    #     self.client.login(username='root', password='root')
    #     response = self.client.post('/1/', {})
    #     self.assertEqual(response.status_code, 302)


class PasswordChangeViewTestCase(TestCase):

    def setUp(self):
        super(PasswordChangeViewTestCase, self).setUp()
        self.client = Client()
        self.user = models.User.objects.create_user(username='root',  password='root')
        self.user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.post('/password_change/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='root', password='root')
        response = self.client.get('/password_change/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='root')
        response = self.client.get(reverse('instagram_profile:password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change.html')

    def test_password_change(self):
        response = self.client.post('/registration/', {'username': 'user', 'password1': 'pass', 'password2': 'pass'})
        self.client.login(username='user', password='pass')
        response = self.client.post('/password_change/', {'old_password': 'pass',
                                                          'new_password1': 'fghjvbnm',
                                                          'new_password2': 'fghjvbnm'})
        self.assertEqual(response.status_code, 302)

    def test_one_password_change(self):
        response = self.client.post('/registration/', {'username': 'user', 'password1': 'pass', 'password2': 'pass'})
        self.client.login(username='user', password='pass')
        response = self.client.post('/password_change/', {'old_password': 'pass',
                                                          'new_password1': 'fghjvbnm',
                                                          'new_password2': 'fghjvbnm'})
        new_password = models.User.objects.get(pk=2)
        self.assertEqual(new_password.username, 'user')
        self.assertTrue(new_password.check_password('fghjvbnm'))


class RegistrationViewTestCase(TestCase):

    def setUp(self):
        super(RegistrationViewTestCase, self).setUp()
        self.client = Client()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/registration/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('instagram_profile:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_user_registration_return_200(self):
        response = self.client.post('/registration/', {'username': 'user', 'password1': 'pass', 'password2': 'pass'})
        self.assertEqual(response.status_code, 200)

    def test_created_one_user(self):
        response = self.client.post('/registration/', {'username': 'user', 'password1': 'pass', 'password2': 'pass'})
        user = models.User.objects.get()
        self.assertEqual(user.username, 'user')


class EditProfileViewTestCase(TestCase):

    def setUp(self):
        super(EditProfileViewTestCase, self).setUp()
        self.client = Client()
        self.user = models.User.objects.create_user(username='root',  password='root')
        self.user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.post('/edit_profile/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.post('/registration/', {'username': 'user', 'password1': 'pass', 'password2': 'pass'})
        self.client.login(username='user', password='pass')
        response = self.client.get('/edit_profile/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.post('/registration/', {'username': 'user', 'password1': 'pass', 'password2': 'pass'})
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('instagram_profile:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/edit_profile.html')

    def test_edit_profile(self):
        response = self.client.post('/registration/', {'username': 'user', 'password1': 'pass', 'password2': 'pass'})
        self.client.login(username='user', password='pass')
        response = self.client.post('/edit_profile/', {'username': 'username',
                                                       'First_name': 'first_name',
                                                       'last_name': 'last_name',
                                                       'email': 'email@email.com',
                                                       'gender': 'gender',
                                                       'birthday': '1995-10-28'})
        self.assertEqual(response.status_code, 302)

    def test_edit_one_profile(self):
        response = self.client.post('/registration/', {'username': 'user', 'password1': 'pass', 'password2': 'pass'})
        self.client.login(username='user', password='pass')
        response = self.client.post('/edit_profile/', {'username': 'username',
                                                       'First_name': 'first_name',
                                                       'last_name': 'last_name',
                                                       'email': 'email@email.com',
                                                       'gender': 'gender',
                                                       'birthday': '1995-10-28'})
        user = models.Profile.objects.get()
        self.assertEqual(user.gender, 'gender')


class ViewProfileViewTestCase(TestCase):

    def setUp(self):
        super(ViewProfileViewTestCase, self).setUp()
        self.client = Client()
        self.user = models.User.objects.create_user(username='root',  password='root')
        self.user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.post('')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='root', password='root')
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='root', password='root')
        response = self.client.get(reverse('instagram_profile:view_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile.html')