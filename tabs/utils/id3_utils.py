import eyed3
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Extracts the ID3 tag
def extract_id3_metadata(mp3_file):
    audiofile = eyed3.load(mp3_file)
    if not audiofile or not audiofile.tag:
        return {}

    tag = audiofile.tag
    artist = tag.artist or ''
    album = tag.album or ''
    title = tag.title or ''
    track_num = tag.track_num[0] if tag.track_num else 0
    genre = tag.genre.name if tag.genre else ''
    year = tag.getBestDate().year if tag.getBestDate() else None

    artwork_file = None
    if tag.images:
        image = tag.images[0].image_data
        pil_image = Image.open(BytesIO(image))
        buffer = BytesIO()
        pil_image.save(buffer, format='JPEG')
        artwork_file = ContentFile(buffer.getvalue(), name='cover.jpg')

    return {
        'artist': artist,
        'album': album,
        'title': title,
        'track_num': track_num,
        'genre': genre,
        'year': year,
        'artwork_file': artwork_file
    }