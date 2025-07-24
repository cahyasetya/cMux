"""Tests for SSH auto-reconnection functionality."""
import unittest
from unittest.mock import Mock, patch

import main


class TestSSHFunctionality(unittest.TestCase):
    """Test SSH detection and retry functionality."""

    def test_is_ssh_command_detects_ssh(self):
        """Test that SSH commands are properly detected."""
        ssh_commands = [
            "ssh user@host",
            "ssh -p 2222 user@host",
            "ssh -o ServerAliveInterval=60 user@host.com",
            "ssh   user@host",  # Extra spaces
        ]
        
        for cmd in ssh_commands:
            with self.subTest(cmd=cmd):
                self.assertTrue(main.is_ssh_command(cmd))

    def test_is_ssh_command_rejects_non_ssh(self):
        """Test that non-SSH commands are not detected as SSH."""
        non_ssh_commands = [
            "ls -la",
            "grep ssh file.txt",
            "rsync -av user@host:/path .",
            "scp file user@host:/tmp",
            "  ssh",  # Just ssh without arguments
            "",
        ]
        
        for cmd in non_ssh_commands:
            with self.subTest(cmd=cmd):
                self.assertFalse(main.is_ssh_command(cmd))

    def test_extract_ssh_connection_simple(self):
        """Test extracting connection details from simple SSH commands."""
        test_cases = [
            ("ssh user@host", "user@host"),
            ("ssh user@server.com", "user@server.com"),
            ("ssh admin@192.168.1.100", "admin@192.168.1.100"),
            ("ssh myserver", "myserver"),
        ]
        
        for cmd, expected in test_cases:
            with self.subTest(cmd=cmd):
                result = main.extract_ssh_connection(cmd)
                self.assertEqual(result, expected)

    def test_extract_ssh_connection_with_options(self):
        """Test extracting connection details from SSH commands with options."""
        test_cases = [
            ("ssh -p 2222 user@host", "user@host"),
            ("ssh -o ServerAliveInterval=60 user@server.com", "user@server.com"),
            ("ssh -i ~/.ssh/key -p 2222 admin@host.local", "admin@host.local"),
            ("ssh -L 8080:localhost:80 user@proxy.com", "user@proxy.com"),
        ]
        
        for cmd, expected in test_cases:
            with self.subTest(cmd=cmd):
                result = main.extract_ssh_connection(cmd)
                self.assertEqual(result, expected)

    def test_extract_ssh_connection_invalid(self):
        """Test that invalid commands return None."""
        invalid_commands = [
            "ls -la",
            "ssh",  # No target
            "ssh -p",  # Incomplete
            "",
        ]
        
        for cmd in invalid_commands:
            with self.subTest(cmd=cmd):
                result = main.extract_ssh_connection(cmd)
                self.assertIsNone(result)

    @patch('main.subprocess.run')
    @patch('main.time.sleep')
    def test_send_keys_with_retry_ssh_success_first_try(self, mock_sleep, mock_run):
        """Test SSH command succeeds on first attempt."""
        # Mock successful command execution
        mock_run.return_value = Mock(returncode=0, stderr="")
        
        with patch('builtins.print'):  # Suppress print output
            main.send_keys_with_retry("session", "window", "ssh user@host")
        
        # Should only be called once (no retries)
        self.assertEqual(mock_run.call_count, 1)
        mock_sleep.assert_not_called()

    @patch('main.subprocess.run')
    @patch('main.time.sleep')
    def test_send_keys_with_retry_ssh_fails_then_succeeds(self, mock_sleep, mock_run):
        """Test SSH command fails first, succeeds on retry."""
        # First call fails, second succeeds
        mock_run.side_effect = [
            Mock(returncode=1, stderr="Connection failed"),  # First attempt fails
            Mock(returncode=0, stderr=""),  # Ctrl+C cleanup
            Mock(returncode=0, stderr=""),  # Second attempt succeeds
        ]
        
        with patch('builtins.print'):  # Suppress print output
            main.send_keys_with_retry("session", "window", "ssh user@host", max_retries=1)
        
        # Should be called 3 times: fail, cleanup, succeed
        self.assertEqual(mock_run.call_count, 3)
        mock_sleep.assert_called()

    @patch('main.subprocess.run')
    @patch('main.time.sleep')
    def test_send_keys_with_retry_non_ssh_no_retry(self, mock_sleep, mock_run):
        """Test that non-SSH commands don't retry on failure."""
        # Mock command failure
        mock_run.return_value = Mock(returncode=1, stderr="Command failed")
        
        with patch('builtins.print'):  # Suppress print output
            main.send_keys_with_retry("session", "window", "ls -la")
        
        # Should only be called once (no retries for non-SSH)
        self.assertEqual(mock_run.call_count, 1)
        mock_sleep.assert_not_called()


if __name__ == '__main__':
    unittest.main()
