# Plan Implementacji Usługi Rozmów Telefonicznych ElevenLabs

## Cel
Utworzenie usługi przyjmującej informacje o użytkowniku i chargebacku, wykonującej rozmowę telefoniczną przez ElevenLabs Agent, i zwracającej transkrypt rozmowy.

## Obecna Struktura Projektu

### Istniejący Kod
- `backend/main.py` - FastAPI application z podstawowymi endpointami
- `backend/elevenlabs/service.py` - testowa implementacja z `DefaultAudioInterface`
- Konfiguracja przez environment variables (`AGENT_ID`, `ELEVENLABS_API_KEY`)

### Obecne Wykorzystanie ElevenLabs
- Użycie `DefaultAudioInterface` - interface audio lokalny (mikrofon/głośniki)
- `ConversationInitiationData` z dynamic variables (obecnie tylko `product_name`)
- Callbacks do przechwytywania transkryptów (`callback_user_transcript`, `callback_agent_response`)

## Wymagania

### Input
```python
{
  "user_info": {
    "first_name": str,
    "last_name": str,
    "phone_number": str
  },
  "chargeback_info": {
    "product_name": str,
    "reason": str
  }
}
```

### Output
```python
{
  "conversation_id": str,
  "transcript": [
    {
      "speaker": "agent" | "user",
      "text": str,
      "timestamp": float
    }
  ],
  "status": "completed" | "failed",
  "duration_seconds": float
}
```

## Architektura Rozwiązania

### Struktura Modułów

```
backend/
├── conversation/           # Główna logika biznesowa rozmów
│   ├── __init__.py
│   ├── models.py          # Modele Pydantic (Request/Response)
│   ├── service.py         # ConversationService - orchestracja
│   └── controller.py      # FastAPI endpoints/routing
├── elevenlabs/            # Warstwa integracji z ElevenLabs SDK
│   ├── __init__.py
│   ├── client.py          # Wrapper dla ElevenLabs API
│   └── transcript_manager.py  # Zbieranie transkryptów z callbacków
└── main.py
```

### 1. Modele Danych (`conversation/models.py`)

```python
class UserInfo(BaseModel)
class ChargebackInfo(BaseModel)
class ConversationRequest(BaseModel)  # Input API
class TranscriptEntry(BaseModel)
class ConversationResponse(BaseModel)  # Output API
```

**Odpowiedzialność**: Definicje typów, walidacja danych wejściowych/wyjściowych

### 2. ElevenLabs Client (`elevenlabs/client.py`)

Wrapper wokół ElevenLabs SDK:
- Inicjalizacja klienta ElevenLabs
- Konfiguracja `Conversation` z callbackami
- Metoda `start_conversation(dynamic_variables: dict) -> str` (conversation_id)
- Obsługa `DefaultAudioInterface`
- Czysta integracja SDK bez logiki biznesowej

### 3. Transcript Manager (`elevenlabs/transcript_manager.py`)

Odpowiedzialność:
- Zbieranie transkryptów z callbacków ElevenLabs
- Synchronizacja (thread-safe) zapisywania wpisów
- Timestamping każdej wypowiedzi
- Zwracanie pełnego transkryptu jako `List[TranscriptEntry]`

### 4. Conversation Service (`conversation/service.py`)

**Główna logika biznesowa**:
- Przyjmuje `ConversationRequest` (user_info + chargeback_info)
- Mapuje dane do `dynamic_variables` dla agenta
- Wywołuje `ElevenLabsClient` do wykonania rozmowy
- Pobiera transkrypt z `TranscriptManager`
- Zwraca `ConversationResponse` z pełnymi danymi
- Obsługa błędów i timeoutów
- Logika async/sync bridging (thread pool executor)

### 5. Controller (`conversation/controller.py`)

**FastAPI routing layer**:
- Endpoint: `POST /api/conversation/start`
- Walidacja request body przez Pydantic
- Dependency injection dla `ConversationService`
- Mapowanie wyjątków na HTTP status codes
- Zwracanie `ConversationResponse`

**Flow**:
1. Request → Walidacja (Pydantic)
2. Controller → Service
3. Service → ElevenLabs Client + Transcript Manager
4. Service ← Transkrypt
5. Controller ← ConversationResponse
6. Response → User

### 6. Kwestia Połączenia Telefonicznego

**Problem**: `DefaultAudioInterface` używa lokalnego audio (mikrofon/głośniki), nie telefonu.

**Możliwe podejścia**:
1. **Na razie**: Pozostawić `DefaultAudioInterface` (zgodnie z wymaganiem "na razie telefon nie jest istotny")
2. **Przyszłość**: Integracja z ElevenLabs Phone API lub WebSocket dla połączeń PSTN

**Decyzja dla MVP**: Użyć `DefaultAudioInterface` - rozmowa będzie przez komputer, nie telefon. Numer telefonu będzie zapisywany w metadanych, ale nie używany do wykonania połączenia.

## Plan Implementacji

### Krok 1: Utworzenie Modeli Danych
**Lokalizacja**: `backend/conversation/models.py`
- Utworzyć katalog `backend/conversation/`
- Utworzyć `backend/conversation/__init__.py`
- Utworzyć `backend/conversation/models.py` z modelami:
  - `UserInfo` - imię, nazwisko, telefon
  - `ChargebackInfo` - product_name, reason
  - `ConversationRequest` - user_info + chargeback_info
  - `TranscriptEntry` - speaker, text, timestamp
  - `ConversationResponse` - conversation_id, transcript, status, duration
- Dodać walidację (phone number format, non-empty strings)

### Krok 2: Implementacja TranscriptManager
**Lokalizacja**: `backend/elevenlabs/transcript_manager.py`
- Utworzyć `backend/elevenlabs/__init__.py` (jeśli nie istnieje)
- Utworzyć `backend/elevenlabs/transcript_manager.py`
- Klasa `TranscriptManager`:
  - Thread-safe przechowywanie listy wpisów transkryptu
  - Metody: `add_user_message()`, `add_agent_message()`, `get_transcript()`
  - Timestamping relatywny od początku rozmowy
  - Zwracanie `List[TranscriptEntry]`

### Krok 3: Implementacja ElevenLabs Client
**Lokalizacja**: `backend/elevenlabs/client.py`
- Refaktoryzacja `backend/elevenlabs/service.py` → `client.py`
- Klasa `ElevenLabsClient`:
  - Constructor: przyjmuje `api_key`, `agent_id`, `transcript_manager`
  - Metoda: `start_conversation(dynamic_variables: dict) -> str`
  - Konfiguracja `Conversation` z callbackami
  - Callbacks integrują się z `TranscriptManager`
  - Obsługa `DefaultAudioInterface`
  - Return conversation_id po zakończeniu

### Krok 4: Implementacja Conversation Service
**Lokalizacja**: `backend/conversation/service.py`
- Utworzyć `backend/conversation/service.py`
- Klasa `ConversationService`:
  - Constructor: dependency injection dla `ElevenLabsClient`
  - Metoda: `async def start_conversation(request: ConversationRequest) -> ConversationResponse`
  - Mapowanie request → dynamic_variables
  - Wywołanie `ElevenLabsClient.start_conversation()`
  - Thread pool executor dla async/sync bridging
  - Pobieranie transkryptu z `TranscriptManager`
  - Kalkulacja duration
  - Zwracanie `ConversationResponse`
  - Error handling

### Krok 5: Utworzenie Controller (API Endpoint)
**Lokalizacja**: `backend/conversation/controller.py`
- Utworzyć `backend/conversation/controller.py`
- FastAPI router z endpointem `POST /api/conversation/start`
- Dependency injection dla `ConversationService`
- Request/response handling
- HTTP error mapping (400, 500, etc.)

### Krok 6: Aktualizacja Main Application
**Lokalizacja**: `backend/main.py`
- Import routera z `conversation.controller`
- Rejestracja routera: `app.include_router(conversation_router)`
- Dodanie example request/response w API docs
- Aktualizacja root endpoint z informacją o nowym API

### Krok 7: Testowanie
- Test manualny przez FastAPI docs (`/docs`)
- Weryfikacja zbierania transkryptu
- Sprawdzenie poprawności dynamic variables przekazywanych do agenta
- Test concurrent conversations (jeśli wymagane)

## Struktura Katalogów (Po Implementacji)

```
backend/
├── conversation/              # Moduł logiki biznesowej rozmów
│   ├── __init__.py
│   ├── models.py             # Modele Pydantic
│   ├── service.py            # ConversationService - orchestracja
│   └── controller.py         # FastAPI router/endpoints
├── elevenlabs/               # Moduł integracji z ElevenLabs SDK
│   ├── __init__.py
│   ├── client.py             # ElevenLabsClient (wrapper SDK)
│   └── transcript_manager.py # Zbieranie transkryptów
├── lineage/
│   └── conversation-service-plan.md
└── main.py                   # FastAPI app z rejestracją routerów
```

## Uwagi Implementacyjne

### Dynamic Variables dla ElevenLabs Agent
Obecny kod używa tylko `product_name`. Rozszerzenie:
```python
dynamic_variables = {
    "first_name": user_info.first_name,
    "last_name": user_info.last_name,
    "phone_number": user_info.phone_number,
    "product_name": chargeback_info.product_name,
    "chargeback_reason": chargeback_info.reason
}
```

**Ważne**: Agent prompt musi być skonfigurowany w ElevenLabs dashboard do używania tych zmiennych.

### Threading i Async
- ElevenLabs SDK używa synchronicznego API (`conversation.wait_for_session_end()`)
- FastAPI używa async
- Rozwiązanie: uruchomić synchroniczny kod w thread pool executor

```python
loop = asyncio.get_event_loop()
conversation_id = await loop.run_in_executor(
    None,
    conversation.wait_for_session_end
)
```

### Error Handling
Potencjalne błędy:
- Brak/nieprawidłowy API key
- Agent ID nie istnieje
- Timeout rozmowy
- Audio interface failure

Wszystkie powinny być obsłużone i zwracać odpowiednie HTTP status codes.

### Timestamping
Callbacks ElevenLabs nie dostarczają timestampów. Rozwiązanie:
- Zapisywać `time.time()` przy każdym wywołaniu callbacku
- Timestamp relatywny: od początku rozmowy (pierwszy callback = 0.0)

## Pytania do Rozważenia

1. **Max długość rozmowy**: Czy powinien być timeout? (np. 5 minut max)
2. **Concurrent conversations**: Czy API powinno obsługiwać wiele równoczesnych rozmów?
3. **Storage**: Czy zapisywać transkrypty do bazy danych, czy tylko zwracać?
4. **Phone number validation**: Jaki format numerów telefonu akceptować? (międzynarodowy, lokalny?)

## Następne Kroki (Po MVP)

1. **Integracja z prawdziwym telefonem** - ElevenLabs Phone API
2. **Persistence** - Zapisywanie transkryptów w bazie danych
3. **Webhook callbacks** - Powiadomienie po zakończeniu rozmowy
4. **Analytics** - Metryki rozmów (duration, success rate)
5. **Retry logic** - Automatyczne ponowienie przy błędach