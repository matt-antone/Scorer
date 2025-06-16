import unittest
from pi_client.state.deployment_setup_state import DeploymentSetupState

class TestDeploymentSetupState(unittest.TestCase):
    """Test cases for DeploymentSetupState (pure logic, no Kivy)."""

    def setUp(self):
        self.state = DeploymentSetupState(
            players=['Player1', 'Player2'],
            roles=['attacker', 'defender'],
            deployment_sequence=['Player1', 'Player2'],
            rolls={'Player1': 6, 'Player2': 4},
            p1_deployment={'infantry': 3, 'artillery': 2, 'cavalry': 1},
            p2_deployment={'infantry': 2, 'artillery': 2, 'cavalry': 2},
            attacker_name='Player1',
            defender_name='Player2',
            roll_validation={'Player1': True, 'Player2': True}
        )

    def test_validate_players(self):
        self.assertTrue(self.state.validate_players())
        self.state.players = ['Player1']
        self.assertFalse(self.state.validate_players())
        self.state.players = ['Player1', 2]
        self.assertFalse(self.state.validate_players())

    def test_validate_roles(self):
        self.assertTrue(self.state.validate_roles())
        self.state.roles = ['attacker']
        self.assertFalse(self.state.validate_roles())
        self.state.roles = ['attacker', 'invalid']
        self.assertFalse(self.state.validate_roles())

    def test_validate_deployment_sequence(self):
        self.assertTrue(self.state.validate_deployment_sequence())
        self.state.deployment_sequence = ['Player2', 'Player1']
        self.assertTrue(self.state.validate_deployment_sequence())
        self.state.deployment_sequence = ['Player1']
        self.assertFalse(self.state.validate_deployment_sequence())

    def test_validate_rolls(self):
        self.assertTrue(self.state.validate_rolls())
        self.state.rolls = {'Player1': 6}
        self.assertFalse(self.state.validate_rolls())
        self.state.rolls = {'Player1': 7, 'Player2': 4}
        self.assertFalse(self.state.validate_rolls())
        self.state.rolls = {'Player1': 6, 'Player2': 0}
        self.assertFalse(self.state.validate_rolls())

    def test_validate_deployments(self):
        self.assertTrue(self.state.validate_deployments())
        self.state.p1_deployment = {'invalid_unit': 3}
        self.assertFalse(self.state.validate_deployments())
        self.state.p1_deployment = {'infantry': -1}
        self.assertFalse(self.state.validate_deployments())

    def test_validate_player_names(self):
        self.assertTrue(self.state.validate_player_names())
        self.state.attacker_name = 'InvalidPlayer'
        self.assertFalse(self.state.validate_player_names())
        self.state.attacker_name = 'Player1'
        self.state.defender_name = 'Player1'
        self.assertFalse(self.state.validate_player_names())

    def test_validate_roll_validation(self):
        self.assertTrue(self.state.validate_roll_validation())
        self.state.roll_validation = {'Player1': True}
        self.assertFalse(self.state.validate_roll_validation())
        self.state.roll_validation = {'Player1': 1, 'Player2': True}
        self.assertFalse(self.state.validate_roll_validation())

    def test_validate_state(self):
        self.assertTrue(self.state.validate_state())
        self.state.players = ['Player1']
        self.assertFalse(self.state.validate_state())
        self.state.players = ['Player1', 'Player2']
        self.state.roles = ['attacker']
        self.assertFalse(self.state.validate_state())

if __name__ == '__main__':
    unittest.main() 