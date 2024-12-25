import mutagen
from mutagen.id3 import APIC, ID3
from mutagen.easyid3 import EasyID3
import mutagen.id3
import requests
import os

def set_other_fields(audio_file, title_name, artist_name, album_name):
    try:
        audio = EasyID3(audio_file)
    except mutagen.id3._util.ID3NoHeaderError:
        audio = mutagen.File(filething=audio_file)
        audio.add_tags()
    except Exception:
        write_bad_albums(title_name)
        return
    audio['title'] = title_name
    audio['artist'] = artist_name
    audio['album'] = album_name
    audio.save()

def set_album_cover(audio_file, image_url):
    try:
        file = ID3(audio_file)
    except mutagen.id3._util.ID3NoHeaderError:
        file = mutagen.File(audio_file, easy=True)
        file.add_tags()
    except Exception:
        write_bad_albums(audio_file)
        return
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)

    with open('image_name.jpg', 'rb') as albumart:
        file.add(APIC(
            encoding=3,
            mime='image/jpeg',
            type=3, desc=u'Cover',
            data=albumart.read()
        ))

    file.save(v2_version=3)
    os.remove('image_name.jpg')

def write_bad_albums(album_name):
    with open("metadata_failed.txt", "a") as f:
        f.write('\n' + album_name)