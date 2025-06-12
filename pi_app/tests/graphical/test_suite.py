"""
Test suite for running all graphical tests.
"""
import pytest
from pi_app.tests.graphical.test_splash_screen import TestSplashScreen
from pi_app.tests.graphical.test_resume_game_screen import TestResumeGameScreen
from pi_app.tests.graphical.test_name_entry_screen import TestNameEntryScreen
from pi_app.tests.graphical.test_deployment_setup_screen import TestDeploymentSetupScreen
from pi_app.tests.graphical.test_initiative_screen import TestInitiativeScreen
from pi_app.tests.graphical.test_scoreboard_screen import TestScoreboardScreen
from pi_app.tests.graphical.test_game_over_screen import TestGameOverScreen
from pi_app.tests.graphical.test_settings_screen import TestSettingsScreen

def test_suite():
    """Run all graphical tests in sequence."""
    # Create test instances
    splash_tests = TestSplashScreen()
    resume_tests = TestResumeGameScreen()
    name_entry_tests = TestNameEntryScreen()
    deployment_tests = TestDeploymentSetupScreen()
    initiative_tests = TestInitiativeScreen()
    scoreboard_tests = TestScoreboardScreen()
    game_over_tests = TestGameOverScreen()
    settings_tests = TestSettingsScreen()
    
    # Run tests in sequence
    try:
        # Splash Screen tests
        splash_tests.setUp()
        splash_tests.test_initial_state()
        splash_tests.test_screen_transition()
        splash_tests.tearDown()
        
        # Resume Game Screen tests
        resume_tests.setUp()
        resume_tests.test_initial_state()
        resume_tests.test_resume_button()
        resume_tests.test_new_game_button()
        resume_tests.tearDown()
        
        # Name Entry Screen tests
        name_entry_tests.setUp()
        name_entry_tests.test_initial_state()
        name_entry_tests.test_name_validation()
        name_entry_tests.test_continue_button()
        name_entry_tests.tearDown()
        
        # Deployment Setup Screen tests
        deployment_tests.setUp()
        deployment_tests.test_initial_state()
        deployment_tests.test_deployment_selection()
        deployment_tests.test_continue_button()
        deployment_tests.tearDown()
        
        # Initiative Screen tests
        initiative_tests.setUp()
        initiative_tests.test_initial_state()
        initiative_tests.test_roll_die_player1()
        initiative_tests.test_roll_die_player2()
        initiative_tests.test_continue_button()
        initiative_tests.tearDown()
        
        # Scoreboard Screen tests
        scoreboard_tests.setUp()
        scoreboard_tests.test_initial_state()
        scoreboard_tests.test_update_scores()
        scoreboard_tests.test_open_score_popup()
        scoreboard_tests.test_concede_game()
        scoreboard_tests.tearDown()
        
        # Game Over Screen tests
        game_over_tests.setUp()
        game_over_tests.test_initial_state()
        game_over_tests.test_new_game_button()
        game_over_tests.tearDown()
        
        # Settings Screen tests
        settings_tests.setUp()
        settings_tests.test_initial_state()
        settings_tests.test_display_rotation()
        settings_tests.test_screensaver_timeout()
        settings_tests.test_back_button()
        settings_tests.tearDown()
        
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False 