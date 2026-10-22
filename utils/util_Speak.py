import asyncio
import io
import edge_tts


def speak(text):
    async def get_audio_bytes():
        communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")

        audio_stream = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
        
        audio_stream.seek(0)
        return audio_stream.read()

    audio_bytes = asyncio.run(get_audio_bytes())

    return audio_bytes
