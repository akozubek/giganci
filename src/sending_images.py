import asyncio
from livekit import rtc

async def start_video(room):
    WIDTH, HEIGHT = 1280, 720
    FPS = 5
    IMAGE_PATH = "obraz.png"

    source = rtc.VideoSource(WIDTH, HEIGHT)
    video_track = rtc.LocalVideoTrack.create_video_track("agent-image", source)

    from PIL import Image
    img = Image.open(IMAGE_PATH).convert("RGB")
    
    img.thumbnail((WIDTH, HEIGHT), Image.LANCZOS)
    # Tworzymy czarne tło
    background = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    # Wyliczamy przesunięcie, żeby wyśrodkować
    x_offset = (WIDTH - img.width) // 2
    y_offset = (HEIGHT - img.height) // 2

    # Wklejamy na tło
    background.paste(img, (x_offset, y_offset))
    background.save("DEBUG_OUTPUT.png")


    frame_bytes = background.tobytes()


    await room.local_participant.publish_track(video_track)

    async def send_frames():
        while True:
            frame = rtc.VideoFrame(WIDTH, HEIGHT, rtc.VideoBufferType.RGB24, frame_bytes)
            source.capture_frame(frame)

    
            await asyncio.sleep(1 / FPS)

    video_task = asyncio.create_task(send_frames())
    return video_track, video_task

async def stop_video(room, video_task, video_track):
    if video_task:
        video_task.cancel()
    await room.local_participant.unpublish_track(video_track)
