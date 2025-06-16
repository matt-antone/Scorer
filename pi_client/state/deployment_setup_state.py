from typing import List, Dict, Optional

class DeploymentSetupState:
    """
    Pure logic class for deployment setup state and validation.
    This class is independent of Kivy and UI code.
    """
    def __init__(self, players: Optional[List[str]] = None, roles: Optional[List[str]] = None,
                 deployment_sequence: Optional[List[str]] = None, rolls: Optional[Dict[str, int]] = None,
                 p1_deployment: Optional[Dict[str, int]] = None, p2_deployment: Optional[Dict[str, int]] = None,
                 attacker_name: Optional[str] = None, defender_name: Optional[str] = None,
                 roll_validation: Optional[Dict[str, bool]] = None):
        self.players = players or []
        self.roles = roles or []
        self.deployment_sequence = deployment_sequence or []
        self.rolls = rolls or {}
        self.p1_deployment = p1_deployment or {}
        self.p2_deployment = p2_deployment or {}
        self.attacker_name = attacker_name
        self.defender_name = defender_name
        self.roll_validation = roll_validation or {}

    def validate_players(self) -> bool:
        return isinstance(self.players, list) and len(self.players) == 2 and all(isinstance(p, str) for p in self.players)

    def validate_roles(self) -> bool:
        valid_roles = {'attacker', 'defender'}
        return (
            isinstance(self.roles, list) and
            len(self.roles) == 2 and
            set(self.roles) == valid_roles
        )

    def validate_deployment_sequence(self) -> bool:
        return (
            isinstance(self.deployment_sequence, list) and
            set(self.deployment_sequence) == set(self.players)
        )

    def validate_rolls(self) -> bool:
        if not isinstance(self.rolls, dict):
            return False
        for player in self.players:
            if player not in self.rolls:
                return False
            roll = self.rolls[player]
            if not isinstance(roll, int) or not (1 <= roll <= 6):
                return False
        return True

    def validate_deployments(self) -> bool:
        valid_units = {'infantry', 'artillery', 'cavalry'}
        for deployment in [self.p1_deployment, self.p2_deployment]:
            if not isinstance(deployment, dict):
                return False
            for unit, count in deployment.items():
                if unit not in valid_units or not isinstance(count, int) or count < 0:
                    return False
        return True

    def validate_player_names(self) -> bool:
        return (
            self.attacker_name in self.players and
            self.defender_name in self.players and
            self.attacker_name != self.defender_name
        )

    def validate_roll_validation(self) -> bool:
        if not isinstance(self.roll_validation, dict):
            return False
        for player in self.players:
            if player not in self.roll_validation or not isinstance(self.roll_validation[player], bool):
                return False
        return True

    def validate_state(self) -> bool:
        return all([
            self.validate_players(),
            self.validate_roles(),
            self.validate_deployment_sequence(),
            self.validate_rolls(),
            self.validate_deployments(),
            self.validate_player_names(),
            self.validate_roll_validation(),
        ]) 