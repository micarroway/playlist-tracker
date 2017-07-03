from PlaylistTracker.PlaylistTracker import PlaylistTracker
from PlaylistTracker.AppConfig import AppConfig


def main():
    playlist_config = AppConfig.config['playlist']
    playlist_tracker = PlaylistTracker(
        playlist_config['userID'],
        playlist_config['playlistID'],
        playlist_config['allowedMinutes']
    )
    print(playlist_tracker.track_playlist())


if __name__ == '__main__':
    main()
