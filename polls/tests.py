from django.test import TestCase


# Create your tests here.
class BasicTestCase(TestCase):
    """
    Basic test case to ensure the test suite runs successfully.
    No actual unit tests are required yet per the assignment.
    """

    def test_basic(self):
        """A simple test that always passes."""
        self.assertEqual(1 + 1, 2)

    def test_django_setup(self):
        """Test that Django is properly configured."""
        from django.conf import settings

        self.assertTrue(settings.configured)
