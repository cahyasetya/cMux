"""Unit tests for main.py functionality."""
import unittest
from unittest.mock import Mock, patch

import main


class TestTmuxFunctions(unittest.TestCase):
    """Test tmux-related functions."""

    @patch('main.subprocess.run')
    def test_is_session_exist_true(self, mock_run):
        """Test is_session_exist returns True when session exists."""
        # Mock successful command execution
        mock_run.return_value = Mock(returncode=0)
        
        result = main.is_session_exist("test_session")
        
        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ['tmux', 'has-session', '-t', 'test_session'],
            capture_output=True,
            check=True
        )

    @patch('main.subprocess.run')
    def test_is_session_exist_false(self, mock_run):
        """Test is_session_exist returns False when session doesn't exist."""
        # Mock command failure (CalledProcessError)
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, ['tmux', 'has-session'])
        
        result = main.is_session_exist("nonexistent_session")
        
        self.assertFalse(result)

    @patch('main.subprocess.run')
    def test_tmux_window_exists_true(self, mock_run):
        """Test tmux_window_exists returns True when window exists."""
        # Mock successful command with window name in output
        mock_run.return_value = Mock(
            returncode=0,
            stdout="window1\nwindow2\ntest_window\n",
            stderr=""
        )
        
        result = main.tmux_window_exists("test_session", "test_window")
        
        self.assertTrue(result)

    @patch('main.subprocess.run')
    def test_tmux_window_exists_false(self, mock_run):
        """Test tmux_window_exists returns False when window doesn't exist."""
        # Mock successful command without target window name
        mock_run.return_value = Mock(
            returncode=0,
            stdout="window1\nwindow2\n",
            stderr=""
        )
        
        result = main.tmux_window_exists("test_session", "nonexistent_window")
        
        self.assertFalse(result)

    @patch('main.subprocess.run')
    def test_create_session(self, mock_run):
        """Test create_session calls tmux with correct arguments."""
        mock_run.return_value = Mock(returncode=0)
        
        with patch('builtins.print'):  # Suppress print output in tests
            main.create_session("test_session")
        
        mock_run.assert_called_once_with(
            ['tmux', 'new-session', '-d', '-s', 'test_session']
        )

    @patch('main.subprocess.run')
    def test_create_window(self, mock_run):
        """Test create_window calls tmux with correct arguments."""
        mock_run.return_value = Mock(returncode=0)
        
        with patch('builtins.print'):  # Suppress print output in tests
            main.create_window("test_session", "test_window")
        
        mock_run.assert_called_once_with(
            ['tmux', 'new-window', '-t', 'test_session', '-n', 'test_window']
        )


if __name__ == '__main__':
    unittest.main()
