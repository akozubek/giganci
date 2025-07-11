from dotenv import load_dotenv

from livekit import agents, rtc
from typing import Any
from livekit.agents import AgentSession, Agent, RoomInputOptions, llm, ModelSettings, stt
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.agents.llm import FunctionTool, RawFunctionTool

from collections.abc import AsyncGenerator, AsyncIterable, Coroutine, Generator

import logging
from prompts import Prompts

load_dotenv()



class Assistant(Agent):
    def __init__(self, lesson_outline) -> None:
        self.lesson_outline = lesson_outline
        instructions = Prompts.SYSTEM_MESSAGE.format(lesson_outline=lesson_outline)
        super().__init__(instructions=instructions)

    async def on_enter(self) -> None:
        logging.debug("Entering...")

    async def on_exit(self) -> None:
        logging.debug("Exiting...")

    async def on_user_turn_completed(
        self, turn_ctx: llm.ChatContext, new_message: llm.ChatMessage
    ) -> None:
        logging.debug("User turn completed...")
        logging.debug("%s %s",turn_ctx, new_message)

    def stt_node(
        self, audio: AsyncIterable[rtc.AudioFrame], model_settings: ModelSettings
    ) -> (
        AsyncIterable[stt.SpeechEvent | str]
        | Coroutine[Any, Any, AsyncIterable[stt.SpeechEvent | str]]
        | Coroutine[Any, Any, None]
    ):
        logging.debug("STT node")
        return super().stt_node( audio, model_settings)
    
    def llm_node(
        self,
        chat_ctx: llm.ChatContext,
        tools: list[FunctionTool | RawFunctionTool],
        model_settings: ModelSettings,
    ) -> (
        AsyncIterable[llm.ChatChunk | str]
        | Coroutine[Any, Any, AsyncIterable[llm.ChatChunk | str]]
        | Coroutine[Any, Any, str]
        | Coroutine[Any, Any, llm.ChatChunk]
        | Coroutine[Any, Any, None]
    ):
        logging.debug("LLM node")
        logging.debug("%s %s %s", chat_ctx.to_dict(), tools, model_settings)
        return super().llm_node(chat_ctx, tools, model_settings)
    
    def transcription_node(
        self, text: AsyncIterable[str], model_settings: ModelSettings
    ) -> AsyncIterable[str] | Coroutine[Any, Any, AsyncIterable[str]] | Coroutine[Any, Any, None]:

        logging.debug("Transcription node")
        return super().transcription_node(text, model_settings)

    def tts_node(
        self, text: AsyncIterable[str], model_settings: ModelSettings
    ) -> (
        AsyncGenerator[rtc.AudioFrame, None]
        | Coroutine[Any, Any, AsyncIterable[rtc.AudioFrame]]
        | Coroutine[Any, Any, None]
    ):
        logging.debug("TTS node")
        logging.debug("text: %s, model_settings: %s", text, model_settings)
        return super().tts_node(text, model_settings)


def get_lesson_outline():
    with open('./data/konspekt_extracted.txt', 'r') as f:
        contents = f.read()
        return contents

async def entrypoint(ctx: agents.JobContext):
    lesson_outline = get_lesson_outline() 

    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="pl"),
        llm=openai.LLM(model="gpt-4o"),
        tts=cartesia.TTS(model="sonic-multilingual", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02", language="pl"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(lesson_outline),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
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