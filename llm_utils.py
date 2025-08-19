"""
LLM Utilities for flask-datta-able-base
Simple utilities for working with LLM APIs
"""

from typing import Dict, Any
from config import get_env, get_config


class LLMClient:
    """
    Simple LLM client for API key management and configuration
    """

    def __init__(self):
        # Load API keys and models from environment
        self.openai_key = get_env('OPENAI_API_KEY')
        self.openai_model = get_env('OPENAI_MODEL', 'gpt-4o-mini')

        self.anthropic_key = get_env('ANTHROPIC_API_KEY')
        self.anthropic_model = get_env('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')

        # Load default provider from config
        self.default_provider = get_config('llm.default_provider', 'openai')

    def check_api_keys(self) -> Dict[str, bool]:
        """Check which API keys are available"""
        return {
            'openai': bool(self.openai_key),
            'anthropic': bool(self.anthropic_key),
        }

    def get_openai_config(self) -> Dict[str, Any]:
        """Get OpenAI configuration"""
        return {
            'api_key_available': bool(self.openai_key),
            'model': self.openai_model,
            'api_key_preview': f"{self.openai_key[:20]}..." if self.openai_key else None
        }

    def get_anthropic_config(self) -> Dict[str, Any]:
        """Get Anthropic configuration"""
        return {
            'api_key_available': bool(self.anthropic_key),
            'model': self.anthropic_model,
            'api_key_preview': f"{self.anthropic_key[:20]}..." if self.anthropic_key else None
        }

    def get_available_providers(self) -> list:
        """Get list of available LLM providers"""
        providers = []
        if self.openai_key:
            providers.append('openai')
        if self.anthropic_key:
            providers.append('anthropic')
        return providers


def get_llm_client() -> LLMClient:
    """Get configured LLM client"""
    return LLMClient()


def check_llm_setup() -> Dict[str, Any]:
    """Check LLM setup and return status"""
    client = LLMClient()

    return {
        'default_provider': client.default_provider,
        'available_providers': client.get_available_providers(),
        'api_keys_available': client.check_api_keys(),
        'openai': client.get_openai_config(),
        'anthropic': client.get_anthropic_config(),
    }


if __name__ == "__main__":
    print("🧪 Testing LLM Configuration...")
    setup = check_llm_setup()

    print(f"\n⚙️  Default Provider: {setup['default_provider']}")
    print(f"🔌 Available Providers: {setup['available_providers']}")

    print("\n🔑 API Keys:")
    for provider, available in setup['api_keys_available'].items():
        status = "✅" if available else "❌"
        if available:
            config_key = f"{provider}"
            model = setup[config_key]['model']
            print(f"  {status} {provider.upper()} - Model: {model}")
        else:
            print(f"  {status} {provider.upper()}")