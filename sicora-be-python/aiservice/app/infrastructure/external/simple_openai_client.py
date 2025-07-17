"""
Simple OpenAI Client Mock for Testing Integration
Cliente simulado de OpenAI para probar la integración sin dependencias externas
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class SimpleOpenAIClient:
    """
    Cliente simulado de OpenAI para pruebas de integración.
    Retorna respuestas predefinidas sin hacer llamadas reales a la API.
    """
    
    def __init__(self, api_key: Optional[str] = None, organization: Optional[str] = None):
        self.api_key = api_key
        self.organization = organization
        self.default_model = "gpt-4"
        
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Simula una respuesta de chat completion de OpenAI.
        """
        logger.info(f"Mock ChatCompletion request with {len(messages)} messages")
        
        # Simular delay de API
        await asyncio.sleep(0.1)
        
        # Obtener el último mensaje del usuario
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        # Generar respuesta basada en el contexto
        if "reglamento" in user_message.lower() or "norma" in user_message.lower():
            response_content = """Basándome en el reglamento del aprendiz SENA, puedo informarte que el reglamento establece las normas y procedimientos que deben seguir los aprendices durante su formación. 

Para una consulta específica sobre el reglamento, te recomiendo revisar:
- Los deberes y derechos del aprendiz
- Las normas de convivencia
- Los procedimientos disciplinarios
- Las condiciones de permanencia en el programa

¿Hay algún aspecto específico del reglamento sobre el que necesites información?"""
        else:
            response_content = f"""Entiendo tu consulta: "{user_message[:100]}..."

Como asistente del sistema SICORA, estoy aquí para ayudarte con información sobre:
- Reglamento del aprendiz SENA
- Normas y procedimientos académicos
- Consultas sobre formación profesional

¿Podrías ser más específico sobre lo que necesitas saber?"""
        
        return {
            "id": f"chatcmpl-mock-{hash(user_message) % 100000}",
            "object": "chat.completion",
            "created": int(asyncio.get_event_loop().time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_content
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": sum(len(msg.get("content", "").split()) for msg in messages),
                "completion_tokens": len(response_content.split()),
                "total_tokens": sum(len(msg.get("content", "").split()) for msg in messages) + len(response_content.split())
            }
        }
    
    async def create_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """
        Simula la creación de embeddings.
        """
        logger.info(f"Mock embedding creation for text length: {len(text)}")
        
        # Simular delay de API
        await asyncio.sleep(0.05)
        
        # Generar embedding simulado (vector de 1536 dimensiones con valores aleatorios)
        import random
        random.seed(hash(text) % 1000000)  # Seed basado en el texto para consistencia
        embedding = [random.uniform(-1, 1) for _ in range(1536)]
        
        return embedding
    
    def is_available(self) -> bool:
        """
        Verifica si el cliente está disponible.
        """
        return True  # Siempre disponible en modo mock
    
    async def test_connection(self) -> bool:
        """
        Prueba la conexión (siempre exitosa en modo mock).
        """
        logger.info("Testing mock OpenAI connection")
        await asyncio.sleep(0.05)
        return True
