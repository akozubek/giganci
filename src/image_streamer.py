import asyncio
from typing import Optional

from PIL import Image
from livekit.rtc import VideoSource, LocalVideoTrack, VideoFrame, VideoBufferType, Room


class ImageStreamer:
    """
    Klasa odpowiada za wyświetlanie wybranego pliku graficznego w strumieniu wideo pokoju.
    """

    def __init__(self, room: Room, width=1280, height=720, fps=5):
        """
        Inicjalizuje obiekt ImageStreamer.

        Args:
            room (Room): Pokój, w których wyświetlamy wideo. 
            width (int): Szerokość obrazu w pikselach.
            height (int): Wysokość obrazu w pikselach.
            fps (int): Liczba klatek na sekundę w strumieniu wideo.
        """

        self.width = width
        self.height = height
        self.fps = fps
        self.room = room

        self._lock = asyncio.Lock()
        self._frame_bytes = None
        self._task = None
        self._video_track: Optional[LocalVideoTrack] = None

    def _resize_and_center_image(self, image_path):
        """
        Otwiera obraz z podanej ścieżki, zmienia jego rozmiar tak, aby pasował
        do rozmiaru wideo ustawionego w streamerze, i wyśrodkowuje go na czarnym tle.

        Args:
            image_path (str): Ścieżka do pliku graficznego.

        Returns:
            Image: Obiekt PIL.Image z przygotowanym obrazem.
        """

        img = Image.open(image_path).convert("RGB")
        img.thumbnail((self.width, self.height), Image.LANCZOS) #type: ignore
        prepared_image = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        x_offset = (self.width - img.width) // 2
        y_offset = (self.height - img.height) // 2
        prepared_image.paste(img, (x_offset, y_offset))
        return prepared_image

    async def update_image(self, image_path):
        """
        Aktualizuje obraz, który będzie wysyłany w strumieniu wideo.

        Args:
            image_path (str): Ścieżka do nowego pliku graficznego.
        """
        prepared_image = self._resize_and_center_image(image_path=image_path)

        async with self._lock:
            self._frame_bytes = prepared_image.tobytes()

    async def start(self):
        """
        Rozpoczyna wysyłanie obrazu jako strumienia wideo do pokoju.

        Tworzy nowy track video track, publikuje go do pokoju i uruchamia asynchroniczną pętlę, 
        która cyklicznie wysyła klatki przygotowane na podstawie aktualnego obrazu.

        Tworzony track ma wymiary ustawione w streamerze i działa z zadanym FPS.

        Raises:
            Exception: Jeśli nie uda się utworzyć ani opublikować toru wideo.
         """

        source = VideoSource(self.width, self.height)
        self._video_track = LocalVideoTrack.create_video_track("agent-image", source)

        await self.room.local_participant.publish_track(self._video_track)

        async def send_frames():
            while True:
                async with self._lock:
                    if self._frame_bytes is not None:
                        frame = VideoFrame(self.width, self.height, VideoBufferType.RGB24, self._frame_bytes)
                        source.capture_frame(frame)
                await asyncio.sleep(1 / self.fps)

        self._task = asyncio.create_task(send_frames())
        

    async def stop(self):
        """
        Zatrzymuje strumień wideo i odłącza tor wideo od pokoju.

        Anuluje działającą pętlę wysyłającą klatki oraz unpublikuje tor wideo,
        dzięki czemu przestaje być widoczny dla uczestników pokoju.
        """

        if self._task:
            self._task.cancel()
        if self._video_track:
            await self.room.local_participant.unpublish_track(self._video_track.sid)

