from ryt_dlp.media_mode import MediaMode

from os import path
from typing import Self


class CommandBuilder:
    def __init__(self):
        self._command: list[str] = ["yt-dlp"]
        self._directory = ""
        self._template = ""
        self._media_mode: MediaMode = MediaMode.VIDEO

    def build(self, url: str) -> list[str]:
        full_dir = path.join(self._directory, self._template)
        self._with_option("o", full_dir)
        self._command.append(url)
        return self._command
    
    def with_video_quality(self, height: str, fps: str) -> Self:
        if self._media_mode == MediaMode.AUDIO:
            raise RuntimeError("Unable to specify video quality while extracting audio")
        
        if height == "Best" and fps == "Best":
            return self._with_option("f", "bestvideo+bestaudio/best")
        elif fps == "Best":
            return self._with_option("f", f"bestvideo[height<={height[:-1]}]+bestaudio/best")
        else:
            return self._with_option("f", f"bestvideo[height<={height[:-1]}][fps<={fps}]+bestaudio/best") 

    def with_video_format(self, format: str) -> Self:
        if self._media_mode == MediaMode.AUDIO:
            raise RuntimeError("Unable to specify video format while extracting audio")
        
        return self._with_option("merge-output-format", format)
    
    def with_sponsorblock(self, **kwargs: bool):
        if self._media_mode == MediaMode.AUDIO:
            raise RuntimeError("Unable to use SponsorBlock while extracting audio")
        
        block = [to_block for to_block in kwargs if kwargs[to_block] == True]

        if len(block) > 0:
            return self._with_option("sponsorblock-remove", ",".join(block))
        else:
            return self
        
    def extract_audio(self):
        self._media_mode = MediaMode.AUDIO
        return self._with_flag("x")
    
    def with_audio_quality(self, quality: int):
        if self._media_mode != MediaMode.AUDIO:
            raise RuntimeError("Unable to specify audio quality when not extracting audio")
        
        return self._with_option("audio-quality", str(quality))
    
    def with_audio_format(self, format: str):
        if self._media_mode != MediaMode.AUDIO:
            raise RuntimeError("Unable to specify audio format when not extracting audio")
        
        return self._with_option("audio-format", format)
    
    def embed_subtitles(self):
        if self._media_mode != MediaMode.VIDEO:
            raise RuntimeError("Unable to embed subtitles when not downloading video")
        
        return self._with_flag("embed-subs")
    
    def embed_thumbnail(self):
        return self._with_flag("embed-thumbnail")
    
    def embed_metadata(self):
        return self._with_flag("embed-metadata")
    
    def with_output_directory(self, directory: str):
        self._directory = directory
        return self
    
    def with_file_name_template(self, template: str):
        self._template = template
        return self
    
    def with_min_sleep(self, min_sleep: int):
        return self._with_option("sleep-interval", str(min_sleep))
    
    def with_max_sleep(self, max_sleep: int):
        return self._with_option("max-sleep-interval", str(max_sleep))
    
    def with_rate_limit(self, rate_limit: str):
        if rate_limit == "":
            return self
        return self._with_option("r", rate_limit)
    
    def with_js_runtime(self, runtime: str, path: str=""):
        if runtime == "None":
            return self
        
        option = runtime + (f":{path}" if len(path) > 0 else "")
        self._with_option("remote-components", "ejs:github")
        return self._with_option("js-runtimes", option)
    
    def with_browser_cookies(self, browser: str):
        return self._with_option("cookies-from-browser", browser)
    
    def _with_flag(self, flag: str) -> Self:
        if len(flag) == 1:
            self._command.append(f"-{flag}")
        else:
            self._command.append(f"--{flag}")
        return self
    
    def _with_option(self, flag: str, option: str) -> Self:
        self._with_flag(flag)
        self._command.append(option)
        return self
