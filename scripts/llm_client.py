"""
Multi-provider LLM client for AgenticSDLC
Supports OpenAI (GPT-4), Anthropic (Claude), and Google (Gemini)
"""
import os
from typing import Optional, Dict, Any
from enum import Enum


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE_OPENAI = "azure-openai"


class LLMClient:
    """Unified interface for multiple LLM providers"""

    def __init__(
        self,
        provider: str,
        model: str,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize LLM client

        Args:
            provider: One of 'openai', 'anthropic', 'google', 'azure-openai'
            model: Model identifier (e.g., 'gpt-4', 'claude-3-5-sonnet-20241022', 'gemini-pro')
            api_key: API key (if not provided, will use environment variables)
            **kwargs: Provider-specific configuration (e.g., azure_endpoint, azure_deployment)
        """
        self.provider = LLMProvider(provider.lower())
        self.model = model
        self.kwargs = kwargs

        # Initialize the appropriate client
        if self.provider == LLMProvider.OPENAI:
            self._init_openai(api_key)
        elif self.provider == LLMProvider.ANTHROPIC:
            self._init_anthropic(api_key)
        elif self.provider == LLMProvider.GOOGLE:
            self._init_google(api_key)
        elif self.provider == LLMProvider.AZURE_OPENAI:
            self._init_azure_openai(api_key, **kwargs)

    def _init_openai(self, api_key: Optional[str]):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")

        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def _init_anthropic(self, api_key: Optional[str]):
        """Initialize Anthropic client"""
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")

        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    def _init_google(self, api_key: Optional[str]):
        """Initialize Google Generative AI client"""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")

        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.client = genai

    def _init_azure_openai(self, api_key: Optional[str], **kwargs):
        """Initialize Azure OpenAI client"""
        try:
            from openai import AzureOpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")

        azure_endpoint = kwargs.get("azure_endpoint") or os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = kwargs.get("api_version", "2024-02-15-preview")

        self.client = AzureOpenAI(
            api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint,
            api_version=api_version
        )
        self.azure_deployment = kwargs.get("azure_deployment", self.model)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> str:
        """
        Generate completion from the LLM

        Args:
            prompt: User prompt/input
            system_prompt: System prompt (if supported)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters

        Returns:
            Generated text response
        """
        if self.provider == LLMProvider.OPENAI:
            return self._generate_openai(prompt, system_prompt, temperature, max_tokens, **kwargs)
        elif self.provider == LLMProvider.ANTHROPIC:
            return self._generate_anthropic(prompt, system_prompt, temperature, max_tokens, **kwargs)
        elif self.provider == LLMProvider.GOOGLE:
            return self._generate_google(prompt, system_prompt, temperature, max_tokens, **kwargs)
        elif self.provider == LLMProvider.AZURE_OPENAI:
            return self._generate_azure_openai(prompt, system_prompt, temperature, max_tokens, **kwargs)

    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using OpenAI API"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Some models use max_completion_tokens instead of max_tokens
        # O1 models and gpt-5.x models don't support temperature parameter
        api_params = {
            "model": self.model,
            "messages": messages,
        }

        # Models that use max_completion_tokens (o1, gpt-5.x)
        if self.model.startswith("o1") or self.model.startswith("gpt-5"):
            # These models use max_completion_tokens and may not support temperature
            api_params["max_completion_tokens"] = max_tokens
            # Only add temperature if the model supports it (check kwargs or model-specific logic)
            # For gpt-5.4-mini, we'll skip temperature to avoid errors
        else:
            # Standard models support both temperature and max_tokens
            api_params["temperature"] = temperature
            api_params["max_tokens"] = max_tokens

        # Add any additional kwargs
        api_params.update(kwargs)

        response = self.client.chat.completions.create(**api_params)
        return response.choices[0].message.content

    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using Anthropic API"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return message.content[0].text

    def _generate_google(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using Google Generative AI API"""
        model = self.client.GenerativeModel(self.model)

        # Combine system prompt with user prompt for Google
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        generation_config.update(kwargs)

        response = model.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        return response.text

    def _generate_azure_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using Azure OpenAI API"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Handle different parameter requirements for O1 and GPT-5 models
        api_params = {
            "model": self.azure_deployment,
            "messages": messages,
        }

        if self.model.startswith("o1") or self.model.startswith("gpt-5"):
            # O1 and GPT-5 models use max_completion_tokens and don't support temperature
            api_params["max_completion_tokens"] = max_tokens
        else:
            # Standard models
            api_params["temperature"] = temperature
            api_params["max_tokens"] = max_tokens

        api_params.update(kwargs)

        response = self.client.chat.completions.create(**api_params)
        return response.choices[0].message.content


def create_llm_client_from_config(agent_config: Dict[str, Any]) -> LLMClient:
    """
    Create LLM client from agent configuration

    Expected config format in agent.yaml:
        model: gpt-4  # or claude-3-5-sonnet-20241022, gemini-pro, etc.
        provider: openai  # optional, will auto-detect from model name if not provided
        temperature: 0.7  # optional
        max_tokens: 4096  # optional

    For Azure OpenAI, add:
        azure_endpoint: https://your-resource.openai.azure.com
        azure_deployment: your-deployment-name

    Args:
        agent_config: Agent configuration dictionary

    Returns:
        Configured LLMClient instance
    """
    model = agent_config.get("model", "gpt-4")
    provider = agent_config.get("provider")

    # Auto-detect provider from model name if not specified
    if not provider:
        model_lower = model.lower()
        if "gpt" in model_lower or "o1" in model_lower or "o3" in model_lower:
            provider = "openai"
        elif "claude" in model_lower:
            provider = "anthropic"
        elif "gemini" in model_lower:
            provider = "google"
        else:
            provider = "openai"  # default

    # Get provider-specific kwargs
    kwargs = {}
    if provider == "azure-openai":
        kwargs["azure_endpoint"] = agent_config.get("azure_endpoint")
        kwargs["azure_deployment"] = agent_config.get("azure_deployment")
        kwargs["api_version"] = agent_config.get("api_version")

    return LLMClient(
        provider=provider,
        model=model,
        **kwargs
    )
