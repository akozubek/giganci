from dotenv import load_dotenv
from dataclasses import dataclass
import asyncio

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
from sending_images import start_video

load_dotenv()

@dataclass
class User:
    name: str
    gender: str


class Assistant(Agent):
    def __init__(self, lesson_outline, start_video_callback) -> None:
        user = get_user("anna")

        self.lesson_outline = lesson_outline
        instructions = Prompts.SYSTEM_MESSAGE.format(
            lesson_outline=lesson_outline,
            child_name=user.name,
            child_gender=user.gender)
        super().__init__(instructions=instructions)
        self.start_video_callback = start_video_callback
        self.video_started = False
        self._video_track = None
        self._video_task = None

    
    async def on_exit(self) -> None:
        # TODO: dodać cleanup
        logging.debug("Exiting...")
       

    async def on_user_turn_completed(
        self, turn_ctx: llm.ChatContext, new_message: llm.ChatMessage
    ) -> None:
        logging.debug("User turn completed...")
        logging.debug("%s %s",turn_ctx, new_message)


    
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

        self.video_started = True
        # strt video callback
        asyncio.create_task(self._async_llm_node())
        return super().llm_node(chat_ctx, tools, model_settings)
    
        

    async def _async_llm_node(self):
        self._video_track, self._video_task = await self.start_video_callback()
    



def get_lesson_outline():
    with open('./data/skrypt-dla-ucznia-4o.md', 'r') as f:
        contents = f.read()
        return contents
    
def get_user(user):
    import yaml
    users = {}

    with open('./example_users.yaml', 'r') as f:
        data = yaml.safe_load(f)
        for key, value in data.items():
            user = User(**value)
            users[key] = user
        return users[user]
    



async def entrypoint(ctx: agents.JobContext):
    lesson_outline = get_lesson_outline() 

    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="pl"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(model="sonic-multilingual", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02", language="pl"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent = Assistant(lesson_outline=lesson_outline, 
                          start_video_callback=lambda: asyncio.create_task(start_video(ctx.room))),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter            
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
