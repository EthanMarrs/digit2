"""test_views.py: runs tests on the views for digit."""
import pytest
from core.models import (Grade,
                         Subject,
                         Question,
                         Comment,
                         Option,
                         Topic,
                         Block,
                         Syllabus,
                         StateException,
                         CorrectOptionExistsError,
                         )
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class BlockViewTests(TestCase):
    """
    Test all Block views.
    """
    def setUp(self):
        grade_test = Grade.objects.create(name="Grade Example")
        syllabus_test = Syllabus.objects.create(grade=grade_test)
        Topic.objects.create(name="Financial Mathematics",
                             description="Topic that involves sinking funds "
                                         "and loan calculations",
                             syllabus=syllabus_test, week_start=1,
                             duration=3)

    def test_get_blocks(self):
        """
        Test that blocks are listed.
        """
        response = self.client.get('/blocks/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Financial Mathematics")
        self.assertQuerysetEqual(
            [response.context['object']],
            ['<Block: Financial Mathematics Block 1>']
        )

    def test_post_block_update(self):
        """
        Test updating block description.
        """
        data = {"text": "yep!"}
        response = self.client.post('/blocks/1/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Block.objects.first().description, "yep!")
