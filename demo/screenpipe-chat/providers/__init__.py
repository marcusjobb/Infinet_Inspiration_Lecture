from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .oneminai_provider import OneMinAIProvider
from .openrouter_provider import OpenRouterProvider

PROVIDERS = {
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "1minai": OneMinAIProvider,
    "openrouter": OpenRouterProvider,
}
