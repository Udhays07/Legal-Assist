"""
Interactive script to setup LLM provider for your RAG system.

Supports:
1. Ollama (local) - Good if you have GPU
2. Groq (cloud) - Fast and free, recommended for CPU-only systems
3. Ollama on Google Colab - Use Colab's free GPU
"""

import os
from pathlib import Path


def update_env_file(updates: dict):
    """Update .env file with new values."""
    env_path = Path(__file__).parent / ".env"
    
    # Read existing .env
    if env_path.exists():
        with open(env_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Update or add new values
    env_dict = {}
    for line in lines:
        if '=' in line and not line.strip().startswith('#'):
            key = line.split('=')[0].strip()
            env_dict[key] = line
    
    # Apply updates
    for key, value in updates.items():
        env_dict[key] = f"{key}={value}\n"
    
    # Write back
    with open(env_path, 'w') as f:
        # Write non-LLM lines first
        for line in lines:
            if '=' in line and not line.strip().startswith('#'):
                key = line.split('=')[0].strip()
                if key not in updates and key not in ['LLM_PROVIDER', 'LLM_MODEL', 'LLM_BASE_URL', 'GROQ_API_KEY', 'LLM_TEMPERATURE', 'LLM_MAX_TOKENS']:
                    f.write(line)
            elif not any(x in line for x in ['LLM', 'GROQ']):
                f.write(line)
        
        # Write LLM configuration section
        f.write("\n# LLM Configuration\n")
        for key, value in updates.items():
            f.write(f"{key}={value}\n")
    
    print(f"✓ Updated {env_path}")


def setup_ollama_local():
    """Setup local Ollama."""
    print("\n" + "="*60)
    print("OLLAMA LOCAL SETUP")
    print("="*60)
    print("\nMake sure Ollama is installed and running:")
    print("1. Install: https://ollama.com/download")
    print("2. Run: ollama serve")
    print("3. Pull model: ollama pull llama3")
    
    base_url = input("\nOllama URL [http://localhost:11434]: ").strip() or "http://localhost:11434"
    model = input("Model name [llama3]: ").strip() or "llama3"
    
    updates = {
        "LLM_PROVIDER": "ollama",
        "LLM_BASE_URL": base_url,
        "LLM_MODEL": model,
        "LLM_TEMPERATURE": "0.7",
        "LLM_MAX_TOKENS": "2000"
    }
    
    update_env_file(updates)
    print("\n✓ Ollama configured!")


def setup_groq():
    """Setup Groq API."""
    print("\n" + "="*60)
    print("GROQ API SETUP")
    print("="*60)
    print("\nGroq provides fast, free LLM inference.")
    print("\nSteps:")
    print("1. Go to https://console.groq.com")
    print("2. Sign up for free")
    print("3. Create an API key")
    print("4. Copy the key (starts with gsk_)")
    
    api_key = input("\nEnter your Groq API key: ").strip()
    
    if not api_key:
        print("✗ API key required!")
        return
    
    print("\nAvailable models:")
    print("1. llama3-70b-8192 (recommended, fast)")
    print("2. llama3-8b-8192 (faster, smaller)")
    print("3. mixtral-8x7b-32768")
    
    model_choice = input("\nChoose model [1]: ").strip() or "1"
    
    models = {
        "1": "llama3-70b-8192",
        "2": "llama3-8b-8192",
        "3": "mixtral-8x7b-32768"
    }
    
    model = models.get(model_choice, "llama3-70b-8192")
    
    updates = {
        "LLM_PROVIDER": "groq",
        "GROQ_API_KEY": api_key,
        "LLM_MODEL": model,
        "LLM_TEMPERATURE": "0.7",
        "LLM_MAX_TOKENS": "2000"
    }
    
    update_env_file(updates)
    
    print("\n✓ Groq configured!")
    print("\nInstall Groq SDK:")
    print("  pip install groq")


def setup_ollama_colab():
    """Setup Ollama on Google Colab."""
    print("\n" + "="*60)
    print("OLLAMA ON GOOGLE COLAB")
    print("="*60)
    print("\nSteps:")
    print("1. Open ollama_colab_setup.ipynb in Google Colab")
    print("2. Run all cells")
    print("3. Get ngrok auth token from https://dashboard.ngrok.com")
    print("4. Copy the public URL from Colab")
    print("5. Come back here and enter the URL")
    
    print("\nPress Enter when you have the ngrok URL...")
    input()
    
    ngrok_url = input("Enter ngrok URL (e.g., https://xxxx.ngrok-free.app): ").strip()
    
    if not ngrok_url:
        print("✗ URL required!")
        return
    
    updates = {
        "LLM_PROVIDER": "ollama",
        "LLM_BASE_URL": ngrok_url,
        "LLM_MODEL": "llama3",
        "LLM_TEMPERATURE": "0.7",
        "LLM_MAX_TOKENS": "2000"
    }
    
    update_env_file(updates)
    print("\n✓ Ollama Colab configured!")


def main():
    """Main setup menu."""
    print("\n" + "="*60)
    print("LLM PROVIDER SETUP")
    print("="*60)
    print("\nChoose your LLM provider:")
    print("\n1. Groq API (Recommended for CPU-only systems)")
    print("   - Fast and free")
    print("   - No local setup needed")
    print("   - Responses in 1-2 seconds")
    print("\n2. Ollama Local")
    print("   - Good if you have GPU")
    print("   - Slower on CPU")
    print("   - Completely private")
    print("\n3. Ollama on Google Colab")
    print("   - Use Colab's free GPU")
    print("   - Requires ngrok setup")
    print("   - Session expires after ~12 hours")
    
    choice = input("\nEnter choice [1]: ").strip() or "1"
    
    if choice == "1":
        setup_groq()
    elif choice == "2":
        setup_ollama_local()
    elif choice == "3":
        setup_ollama_colab()
    else:
        print("Invalid choice!")
        return
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n1. Test your setup:")
    print("   python test_rag_system.py")
    print("\n2. Start your backend:")
    print("   uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
