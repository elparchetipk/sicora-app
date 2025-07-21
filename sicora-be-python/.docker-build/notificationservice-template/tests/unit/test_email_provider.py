"""
Tests unitarios para EmailProvider
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.infrastructure.providers.email_provider import EmailProvider

@pytest.mark.asyncio
async def test_send_email_success():
    """Test envío exitoso de email."""
    provider = EmailProvider()

    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = await provider.send_notification(
            "test@example.com",
            "Test Subject",
            "Test Body"
        )

        assert result is True
        mock_server.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_send_email_failure():
    """Test fallo en envío de email."""
    provider = EmailProvider()

    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp.side_effect = Exception("SMTP Error")

        result = await provider.send_notification(
            "test@example.com",
            "Test Subject",
            "Test Body"
        )

        assert result is False
