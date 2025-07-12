from dotenv import load_dotenv
import logging
import os

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RunContext, function_tool
from livekit.plugins import openai, cartesia, deepgram, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from prompts import Prompts
from image_streamer import ImageStreamer
from helpers import User, get_lesson_outline, get_user, get_step_image_path

"""
Główny moduł uruchamiający wirtualnego asystenta (LessonAssistant) w pokoju LiveKit.

Zawiera definicję klasy LessonAssistant, która wspiera dziecko podczas lekcji online
i umożliwia wyświetlanie obrazów kroków rozwiązania. Asystent korzysta z konspektu lekcji,
informacji o użytkowniku oraz strumieniowania obrazu.

Ten projekt ma charakter POC (Proof of Concept), dlatego obsługa błędów oraz część logiki
zostały uproszczone.

Moduł wykorzystuje LiveKit (agent, STT, TTS), OpenAI, Cartesia oraz dodatkowe narzędzia
(np. Deepgram, Silero, wykrywanie mowy).
"""

load_dotenv()

class LessonAssistant(Agent):
    """
    Agent wspierający ucznia podczas lekcji online w pokoju LiveKit.

    Klasa odpowiada za prowadzenie rozmowy na podstawie konspektu lekcji,
    reagowanie na pytania dziecka oraz wyświetlanie obrazów poszczególnych kroków rozwiązania.

    Args:
        lesson_outline (str): Konspekt lekcji, na podstawie którego asystent prowadzi rozmowę.
        user (User): Obiekt zawierający informacje o dziecku (imię, płeć).
        image_streamer (ImageStreamer): Obiekt odpowiedzialny za strumieniowanie obrazu do pokoju.

    Attributes:
        lesson_outline (str): Zapisany konspekt lekcji.
        _image_streamer (ImageStreamer): Streamer do zarządzania obrazami.
        _video_started (bool): Flaga informująca, czy wideo zostało już uruchomione.
    """
        
    def __init__(self, *,
                     
                lesson_outline: str,
                user: User, 
                image_streamer: ImageStreamer                
                )  -> None:
        """
        Inicjalizuje asystenta lekcji.

        Args:
            lesson_outline (str): Konspekt lekcji.
            user (User): Obiekt użytkownika zawierający imię i płeć.
            image_streamer (ImageStreamer): Obiekt odpowiedzialny za strumieniowanie obrazu.
        """    

        self.lesson_outline = lesson_outline
        instructions = Prompts.SYSTEM_MESSAGE.format(
            lesson_outline=lesson_outline,
            child_name=user.name,
            child_gender=user.gender)
        
        super().__init__(instructions=instructions)
        self._video_started = False
        self._image_streamer = image_streamer

    
    async def on_exit(self) -> None:
        """
        Metoda wywoływana przy zamykaniu agenta.

        Zatrzymuje streamer obrazu i wykonuje czyszczenie zasobów przed wyjściem.
        W przypadku błędu loguje informację, ale nie przerywa działania.

        Returns: None
        """        
        logging.debug("Exiting...")
        try:
            await self._image_streamer.stop()
        except Exception as e:
            logging.error("Błąd podczas zatrzymywania streamera: %s", e)

       
        
    @function_tool()
    async def display_solution_image(
        self,
        context: RunContext,
        solution_step_identifier: str,
    ) -> bool:
        """
        Displays the image for the given solution step to the student.

        Args:
            solution_step_identifier (str): The identifier of the step (e.g., '1a', '3b', 'bonus_a') to show to the student. 
                You can also use the special identifier 'game' to show what the finished game looks like.

        Returns:
            bool: True if the image started displaying successfully, False otherwise.
        """

        # Komentarze jest po angielsku, bo jest przekazywany do LLM
        logging.info("Looking for image %s", solution_step_identifier)
        solution_image_path = get_step_image_path(solution_step_identifier)

        if os.path.exists(solution_image_path):
            logging.info("Found image file %s", solution_image_path)

            await self._image_streamer.update_image(solution_image_path)
            if self._video_started:
                await self._image_streamer.stop()
            await self._image_streamer.start()
            self._video_started = True
            return True
        else:
            logging.info("Image for step %s not found", solution_step_identifier)
            return False
    



async def entrypoint(ctx: agents.JobContext):
    """
    Funkcja główna uruchamiająca agenta i konfigurująca sesję w pokoju LiveKit.

    Args:
        ctx (agents.JobContext): Kontekst pracy agenta (np. dostęp do pokoju).
    """

    # Wczytanie danych - docelowo z platformy?
    lesson_outline = get_lesson_outline()
    user = get_user("anna") 

    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="pl"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(model="sonic-multilingual", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02", language="pl"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent = LessonAssistant(
            lesson_outline=lesson_outline,
            user=user, 
            image_streamer=ImageStreamer(ctx.room)),                                                    
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation      
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=Prompts.INITIAL_INSTRUCTIONS
    )


def main():
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

if __name__ == "__main__":
    main()