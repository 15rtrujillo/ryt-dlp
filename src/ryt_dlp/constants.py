AUDIO_FORMAT_DEFAULT = "mp3"
AUDIO_FORMATS = ["aac", "alac", "flac", "m4a", "opus", "vorbis", "wav"]
AUDIO_QUALITY_DEFAULT = "Best"
AUDIO_QUALITIES = ["High", "Medium", "Low"]
AUDIO_QUALITY_LABEL_TO_VALUE = {
    "Best": 0,
    "High": 2,
    "Medium": 5,
    "Low": 9
}

VIDEO_FORMAT_DEFAULT = "mp4"
VIDEO_FORMATS = ["avi", "flv", "mkv", "mov", "webm"]
VIDEO_QUALITY_DEFAULT = "720p"
VIDEO_QUALITIES = ["360p", "480p", "1080p", "Best"]

JS_RUNTIME_DEFAULT = "None"
JS_RUNTIMES = ["node", "deno", "quickjs", "bun"]

BROWSER_DEFAULT = "firefox"
BROWSERS = ["brave", "chrome", "chromium", "edge", "opera", "safari", "vivaldi", "whale"]
