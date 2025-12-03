# ElevenLabs Wrapper

Python wrapper dla ElevenLabs Conversational AI z obsługą konfiguracji agenta.

## Komponenty

### Agent

Klasa `Agent` reprezentuje konfigurację agenta z wszystkimi opcjami customizacji:

```python
from elevenlabs_wrapper import Agent

# Podstawowa konfiguracja
agent = Agent(
    agent_id="your_agent_id",
    dynamic_variables={
        "product_name": "Shrek",
        "first_name": "Janek",
    }
)

# Opcjonalne: Ustaw pierwszą wiadomość
agent.set_first_message("Hello! How can I help you today?")

# Opcjonalne: Ustaw język
agent.set_language("pl")

# Opcjonalne: Zmień prompt
agent.set_prompt(
    prompt="You are a helpful assistant...",
    llm="gpt-4",
    temperature=0.7
)
```

### ElevenLabsClient

Klient dla lokalnych konwersacji przez mikrofon/głośniki:

```python
from elevenlabs_wrapper import ElevenLabsClient, Agent

# Utwórz agenta
agent = Agent(
    agent_id="your_agent_id",
    dynamic_variables={"name": "User"}
)

# Utwórz klienta
client = ElevenLabsClient()

# Rozpocznij konwersację (blokuje do końca rozmowy)
conversation_id = client.start_conversation(agent)
```

### PhoneCaller

Klient do wykonywania połączeń telefonicznych przez Twilio:

```python
from elevenlabs_wrapper import PhoneCaller, Agent

# Utwórz agenta
agent = Agent(
    agent_id="your_agent_id",
    dynamic_variables={"customer_name": "John"}
)

# Utwórz phone caller
caller = PhoneCaller()

# Wykonaj połączenie
response = caller.make_call(
    agent=agent,
    to_number="+1234567890"
)

print(f"Call SID: {response.call_sid}")
print(f"Conversation ID: {response.conversation_id}")
```

### TranscriptManager

Manager do śledzenia transkrypcji rozmów:

```python
from elevenlabs_wrapper import TranscriptManager

manager = TranscriptManager()

# Dodaj wiadomości
manager.add_user_message("Hello!")
manager.add_agent_message("Hi! How can I help?")

# Pobierz transkrypcję
transcript = manager.get_transcript()
for message in transcript:
    print(f"{message.speaker}: {message.text}")
```

## Zmienne środowiskowe

Utwórz plik `.env` z następującymi zmiennymi:

```bash
# Wymagane
ELEVENLABS_API_KEY=your_api_key_here
AGENT_ID=your_agent_id_here

# Dla połączeń telefonicznych
AGENT_PHONE_NUMBER_ID=your_phone_number_id_here

# Opcjonalne dla testów
TEST_PHONE_NUMBER=+1234567890
```

## Przykłady użycia

### Lokalna konwersacja

```bash
cd backend
python test_elevenlabs.py
```

Skrypt uruchomi konwersację przez mikrofon/głośniki. Mów do mikrofonu, naciśnij Ctrl+C aby zakończyć.

### Połączenie telefoniczne

```bash
cd backend
python test_phone_call.py
```

Skrypt wykona połączenie telefoniczne do podanego numeru.

## API Reference

### Agent

**Parametry konstruktora:**
- `agent_id` (str) - ID agenta z ElevenLabs
- `user_id` (Optional[str]) - ID użytkownika
- `dynamic_variables` (Dict[str, Any]) - Zmienne dynamiczne dla personalizacji
- `agent_override` (Optional[AgentConfigOverride]) - Override konfiguracji agenta
- `phone_number_id` (Optional[str]) - ID numeru telefonu dla połączeń

**Metody:**
- `add_dynamic_variable(key, value)` - Dodaj zmienną dynamiczną
- `set_first_message(message)` - Ustaw pierwszą wiadomość agenta
- `set_language(language)` - Ustaw język (np. "pl", "en")
- `set_prompt(prompt, llm, temperature, max_tokens)` - Zmień prompt i parametry LLM
- `to_conversation_config()` - Konwertuj do formatu dla lokalnej konwersacji
- `to_phone_call_config()` - Konwertuj do formatu dla połączenia telefonicznego

### ElevenLabsClient

**Parametry konstruktora:**
- `api_key` (Optional[str]) - Klucz API (domyślnie z env)
- `transcript_manager` (Optional[TranscriptManager]) - Manager transkrypcji

**Metody:**
- `start_conversation(agent)` - Rozpocznij lokalną konwersację (blokuje)

### PhoneCaller

**Parametry konstruktora:**
- `api_key` (Optional[str]) - Klucz API (domyślnie z env)
- `phone_number_id` (Optional[str]) - ID numeru telefonu (domyślnie z env)

**Metody:**
- `make_call(agent, to_number)` - Wykonaj połączenie synchroniczne
- `make_call_async(agent, to_number)` - Wykonaj połączenie asynchroniczne

## Architektura

```
Agent (konfiguracja)
    |
    ├──> ElevenLabsClient (lokalne konwersacje)
    |         |
    |         └──> Conversation API
    |
    └──> PhoneCaller (połączenia telefoniczne)
              |
              └──> Twilio Outbound Call API
```

Klasa `Agent` enkapsuluje wszystkie opcje customizacji i może być użyta zarówno dla lokalnych konwersacji jak i połączeń telefonicznych.