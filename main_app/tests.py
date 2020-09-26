from django.test import TestCase

from .models import Topic

# Create your tests here.

class TopicModelTests(TestCase):
    def test_text_field_with_valid_length(self):
        topic = Topic(text='This is valid topic')

        self.assertEqual(topic.text, 'This is valid topic')
