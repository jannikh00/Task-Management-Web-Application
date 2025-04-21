from django.test import TestCase
from .models import Task

# Define a test case class for Task model
class TaskModelTest(TestCase):

    # This method will test whether a Task instance is created correctly
    def test_task_creation(self):
        # Create a task with a title and due date
        task = Task.objects.create(title="Test Task", due_date="2025-12-12")

        # Check if the title was saved correctly
        self.assertEqual(task.title, "Test Task")

        # Check if the default status is False (i.e., not completed)
        self.assertFalse(task.status)

    # Test that a task with status=True is saved correctly
    def test_completed_task_status(self):
        # Create a task marked as completed (status=True)
        task = Task.objects.create(title="Completed Task", due_date="2025-11-11", status=True)
        
        # Check that the status is saved as True
        self.assertTrue(task.status)

    # Test that the __str__ method returns the task title
    def test_task_string_representation(self):
        # Create a task with a specific title
        task = Task.objects.create(title="Title Test", due_date="2025-11-01")
        
        # Check that str(task) returns the title
        self.assertEqual(str(task), "Title Test")

    # Test that creating a Task without a title raises an error
    def test_missing_title_raises_error(self):
        # Create a Task instance with no title, only a due date
        task = Task(due_date="2025-10-10")  # Not saved to the database yet

        # Expect an exception to be raised when validation is triggered
        with self.assertRaises(Exception):
            # Run full model validation (checks for required fields, formats, etc.)
            task.full_clean()
            # This line will not be reached if full_clean() raises an error
            task.save()