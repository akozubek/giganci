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
from sending_images import start_video

load_dotenv()



class Assistant(Agent):
    def __init__(self, lesson_outline, start_video_callback) -> None:
        self.lesson_outline = lesson_outline
        instructions = Prompts.SYSTEM_MESSAGE.format(lesson_outline=lesson_outline)
        super().__init__(instructions=instructions)
        self.start_video_callback = start_video_callback
        self.video_started = False
        self._video_track = None
        self._video_task = None

    async def on_enter(self) -> None:
        logging.debug("Entering...")

    async def on_exit(self) -> None:
        logging.debug("Exiting...")
        self.session._forward_video_task

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

        self.video_started = True
        self._video_track, self._video_task = self.start_video_callback()
        return super().llm_node(chat_ctx, tools, model_settings)
    



def get_lesson_outline():
    with open('./data/skrypt-dla-ucznia-4o.md', 'r') as f:
        contents = f.read()
        return contents
    



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

from livekit import rtc
from livekit.agents import JobContext
import asyncio

async def f(ctx):
    WIDTH = 640
    HEIGHT = 480

    source = rtc.VideoSource(WIDTH, HEIGHT)
    track = rtc.LocalVideoTrack.create_video_track("example-track", source)
    options = rtc.TrackPublishOptions(
        # since the agent is a participant, our video I/O is its "camera"
        source=rtc.TrackSource.SOURCE_CAMERA,
        simulcast=True,
        # when modifying encoding options, max_framerate and max_bitrate must both be set
        video_encoding=rtc.VideoEncoding(
            max_framerate=30,
            max_bitrate=3_000_000,
        ),
        video_codec=rtc.VideoCodec.H264,
    )
    publication = await ctx.agent.publish_track(track, options)

    # this color is encoded as ARGB. when passed to VideoFrame it gets re-encoded.
    COLOR = [255, 255, 0, 0]; # FFFF0000 RED

    async def _draw_color():
        argb_frame = bytearray(WIDTH * HEIGHT * 4)
        while True:
            await asyncio.sleep(0.1) # 10 fps
            argb_frame[:] = COLOR * WIDTH * HEIGHT
            frame = rtc.VideoFrame(WIDTH, HEIGHT, rtc.VideoBufferType.RGBA, argb_frame)

            # send this frame to the track
            source.capture_frame(frame)

    return _draw_color


def main():
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

if __name__ == "__main__":
    main()