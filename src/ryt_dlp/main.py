import tkinter as tk
import tkinter.filedialog as filedialog


class RytDlpGui(tk.Tk):
    def __init__(self):
        self.current_column: dict[tk.Tk | tk.Widget] = {}
        self.current_row: dict[tk.Tk | tk.Widget] = {}

        super().__init__()
        self.title("ryt-dlp")

        self.url = tk.StringVar(self)
        self.media_mode = tk.StringVar(self, "Video")
        self.video_quality = tk.StringVar(self, "720p")
        self.embed_subtitles = tk.BooleanVar(self, False)
        self.embed_thumbnail = tk.BooleanVar(self, True)
        self.embed_metadata = tk.BooleanVar(self, True)

        self.frame_url = tk.Frame(self)
        self.frame_url.grid(row=self._get_row(self), column=0)
        self.label_url = tk.Label(self.frame_url, text="URL:")
        self.label_url.grid(row=0, column=self._get_column(self.frame_url))
        self.entry_url = tk.Entry(self.frame_url, textvariable=self.url)
        self.entry_url.grid(row=0, column=self._get_column(self.frame_url))

        self.label_media_type = tk.Label(self, text="Media Type:")
        self.label_media_type.grid(row=self._get_row(self), column=0)

        self.frame_video_audio = tk.Frame(self)
        self.frame_video_audio.grid(row=self._get_row(self), column=0)
        self.radio_video = tk.Radiobutton(self.frame_video_audio, text="Video", variable=self.media_mode, value="Video")
        self.radio_video.grid(row=0, column=self._get_column(self.frame_video_audio))
        self.radio_audio = tk.Radiobutton(self.frame_video_audio, text="Audio", variable=self.media_mode, value="Audio")
        self.radio_audio.grid(row=0, column=self._get_column(self.frame_video_audio))

        self.label_media_options = tk.Label(self, text="Media Options")
        self.label_media_options.grid(row=self._get_row(self), column=0)

        self.frame_video_options = tk.Frame(self)
        self.frame_video_options.grid(row=self._get_row(self, False), column=0)
        self.label_quality = tk.Label(self.frame_video_options, text="Quality")
        self.label_quality.grid(row=self._get_row(self.frame_video_options, False), column=0)
        self.optionmenu_quality = tk.OptionMenu(self.frame_video_options, self.video_quality, "360p", "420p", "720p", "1080p", "Best")
        self.optionmenu_quality.grid(row=self._get_row(self.frame_video_options), column=1)

        self.frame_audio_options = tk.Frame(self)
        self.frame_audio_options.grid(row=self._get_row(self), column=0)
        self.frame_audio_options.grid_remove()

        self.label_embedding = tk.Label(self, text="Embedding")
        self.label_embedding.grid(row=self._get_row(self), column=0)

        self.frame_embedding = tk.Frame(self)
        self.frame_embedding.grid(row=self._get_row(self), column=0)
        self.checkbutton_subtitles = tk.Checkbutton(self.frame_embedding, text="Subtitles", variable=self.embed_subtitles)
        self.checkbutton_subtitles.grid(row=self._get_row(self.frame_embedding), column=0)
        self.checkbutton_thumbnail = tk.Checkbutton(self.frame_embedding, text="Thumbnail", variable=self.embed_thumbnail)
        self.checkbutton_thumbnail.grid(row=self._get_row(self.frame_embedding), column=0)
        self.checkbutton_metadata = tk.Checkbutton(self.frame_embedding, text="Metadata", variable=self.embed_metadata)
        self.checkbutton_metadata.grid(row=self._get_row(self.frame_embedding), column=0)

        self.mainloop()

    def _get_row(self, parent: tk.Tk | tk.Widget, increment: bool=True) -> int:
        if not parent in self.current_row:
            current = 0
        else:
            current = self.current_row[parent]
        if increment:
            self.current_row[parent] = current + 1
        return current

    def _get_column(self, parent: tk.Tk | tk.Widget, increment: bool=True) -> int:
        if not parent in self.current_column:
            current = 0
        else:
            current = self.current_column[parent]
        
        if increment:
            self.current_column[parent] = current + 1
        return current


if __name__ == "__main__":
    RytDlpGui()
