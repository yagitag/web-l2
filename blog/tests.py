from django.test import TestCase

from blog.models import Post

class MyTest(TestCase):
  def test_post(self):
    print("Name", Post.__name__)
    print(Post._meta.get_all_field_names())
