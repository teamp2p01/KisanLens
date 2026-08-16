import io

from PIL import Image

# Vision models don't need a full-resolution phone photo: 1600px on the long
# edge keeps leaf detail while making requests smaller and faster over a
# hackathon-venue wifi connection.
MAX_DIMENSION = 1600
MAX_IMAGE_BYTES = 8 * 1024 * 1024


def validate_image(image: Image.Image):
    width, height = image.size
    if width < 240 or height < 240:
        return False, "Please upload a larger image (at least 240\u00d7240 pixels)."
    return True, "OK"


def image_to_jpeg_bytes(image: Image.Image, quality: int = 88) -> bytes:
    """Convert an image to compact JPEG bytes ready to send to a vision API.

    Downscales large photos and, in the rare case that isn't enough,
    progressively lowers JPEG quality until the result fits under
    MAX_IMAGE_BYTES.
    """
    rgb_image = image.convert("RGB")

    if max(rgb_image.size) > MAX_DIMENSION:
        rgb_image = rgb_image.copy()
        rgb_image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)

    data = b""
    for attempt_quality in (quality, 70, 55, 40):
        buffer = io.BytesIO()
        rgb_image.save(buffer, format="JPEG", quality=attempt_quality, optimize=True)
        data = buffer.getvalue()
        if len(data) <= MAX_IMAGE_BYTES:
            return data

    return data  # smallest attempt tried, even if still over the limit
