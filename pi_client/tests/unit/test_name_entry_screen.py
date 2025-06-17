import unittest
from unittest.mock import Mock, patch
from pi_client.state.name_entry_state import NameEntryState

class TestNameEntryState(unittest.TestCase):
    """State-only tests for name entry logic and validation."""
    
    def setUp(self):
        self.state = NameEntryState()
        self.state.p1_name = ''
        self.state.p2_name = ''
        self.state.player_names = ['', '']
        self.state.qr_code = ''
        self.state.qr_code_valid = False
        self.state.qr_code_error = ''
        self.state.name_validation = True

    def test_initial_state(self):
        """Test initial state properties."""
        self.assertEqual(self.state.p1_name, '')
        self.assertEqual(self.state.p2_name, '')
        self.assertEqual(self.state.player_names, ['', ''])
        self.assertFalse(self.state.qr_code_valid)
        self.assertEqual(self.state.qr_code_error, '')
        self.assertTrue(self.state.name_validation)

    def test_validate_name(self):
        """Test name validation logic."""
        # Valid names
        self.assertTrue(self.state.validate_name('Alice'))
        self.assertTrue(self.state.validate_name('Bob Smith'))
        self.assertTrue(self.state.validate_name('Player123'))
        self.assertTrue(self.state.validate_name('A' * 20))  # Max length
        
        # Invalid names
        self.assertFalse(self.state.validate_name(''))  # Empty
        self.assertFalse(self.state.validate_name('A'))  # Too short
        self.assertFalse(self.state.validate_name('A' * 21))  # Too long
        self.assertFalse(self.state.validate_name('Invalid!'))  # Special chars
        self.assertFalse(self.state.validate_name('Invalid@'))  # Special chars

    def test_validate_inputs(self):
        """Test input validation logic."""
        # Valid inputs
        self.state.p1_name = 'Alice'
        self.state.p2_name = 'Bob'
        self.assertTrue(self.state.validate_inputs())
        
        # Invalid inputs - empty names
        self.state.p2_name = ''
        self.assertFalse(self.state.validate_inputs())
        
        # Invalid inputs - duplicate names
        self.state.p2_name = 'Alice'
        self.assertFalse(self.state.validate_inputs())
        
        # Invalid inputs - invalid names
        self.state.p2_name = 'Invalid!'
        self.assertFalse(self.state.validate_inputs())

    def test_update_player_names(self):
        """Test updating player names."""
        self.state.update_player_names('Alice', 'Bob')
        self.assertEqual(self.state.p1_name, 'Alice')
        self.assertEqual(self.state.p2_name, 'Bob')
        self.assertEqual(self.state.player_names, ['Alice', 'Bob'])

    def test_generate_qr_code(self):
        """Test QR code generation logic."""
        # Valid QR code generation
        self.assertTrue(self.state.generate_qr_code('Alice'))
        self.assertTrue(self.state.qr_code_valid)
        self.assertEqual(self.state.qr_code_error, '')
        
        # Invalid QR code generation
        self.assertFalse(self.state.generate_qr_code('Invalid!'))
        self.assertFalse(self.state.qr_code_valid)
        self.assertNotEqual(self.state.qr_code_error, '')

    def test_handle_qr_code_error(self):
        """Test QR code error handling."""
        self.state.handle_qr_code_error()
        self.assertFalse(self.state.qr_code_valid)
        self.assertEqual(self.state.qr_code_error, "Failed to generate QR code")

    def test_state_validation(self):
        """Test state validation."""
        # Valid state
        self.assertTrue(self.state.validate_state())
        
        # Invalid state - invalid names
        self.state.p1_name = 'Invalid!'
        self.assertFalse(self.state.validate_state())

    def test_get_state_dict(self):
        """Test state serialization."""
        state_dict = self.state.get_state_dict()
        expected_keys = ['p1_name', 'p2_name', 'player_names', 'qr_code', 
                        'qr_code_valid', 'qr_code_error', 'name_validation']
        for key in expected_keys:
            self.assertIn(key, state_dict)

    def test_update_from_dict(self):
        """Test state deserialization."""
        new_state = {
            'p1_name': 'Alice',
            'p2_name': 'Bob',
            'player_names': ['Alice', 'Bob'],
            'qr_code': 'test_qr',
            'qr_code_valid': True,
            'qr_code_error': '',
            'name_validation': True
        }
        self.state.update_from_dict(new_state)
        self.assertEqual(self.state.p1_name, 'Alice')
        self.assertEqual(self.state.p2_name, 'Bob')
        self.assertEqual(self.state.player_names, ['Alice', 'Bob'])
        self.assertEqual(self.state.qr_code, 'test_qr')
        self.assertTrue(self.state.qr_code_valid)

    def test_reset_state(self):
        """Test state reset functionality."""
        self.state.p1_name = 'Alice'
        self.state.p2_name = 'Bob'
        self.state.qr_code_valid = True
        
        self.state.reset_state()
        
        self.assertEqual(self.state.p1_name, '')
        self.assertEqual(self.state.p2_name, '')
        self.assertEqual(self.state.player_names, ['', ''])
        self.assertFalse(self.state.qr_code_valid)
        self.assertEqual(self.state.qr_code_error, '')

if __name__ == '__main__':
    unittest.main() 