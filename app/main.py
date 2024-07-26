from http import HTTPStatus
from flask import Flask, request, jsonify, Response
from pytube import Playlist, YouTube
import requests
from sys import stderr

app = Flask(__name__)

@app.get('/test')
def test_endpoint():
    return Response('Server works', status=HTTPStatus.OK, mimetype='text/plain')

@app.get('/playlist')
def get_playlist_urls():
    playlist_url = request.args.get('url')
    playlist = Playlist(playlist_url)
    videos: list[YouTube] = playlist.videos
    result = list(
        map(
            lambda v: v.watch_url,
            videos
        )
    )
    return jsonify({
        "name": playlist.title,
        "urls": result
    })

@app.get('/thumbnail')
def get_thumbnail_url():
    video_url = request.args.get('url')
    yt = YouTube(video_url)
    resp = requests.get(yt.thumbnail_url, stream=True)
    thumbnail = resp.content
    return Response(thumbnail, headers={
        'Content-Type': 'image/jpg'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)