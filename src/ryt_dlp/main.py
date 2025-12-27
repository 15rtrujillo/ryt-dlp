from ryt_dlp.constants import *
from ryt_dlp.media_mode import MediaMode

import tkinter as tk
import tkinter.filedialog as filedialog


class RytDlpGui(tk.Tk):
    def __init__(self):
        self.current_row = 0

        super().__init__()
        self.title("ryt-dlp")

        self.url = tk.StringVar(self)
        self.media_mode = tk.IntVar(self, MediaMode.VIDEO)
        self.video_quality = tk.StringVar(self, VIDEO_QUALITY_DEFAULT)
        self.video_format = tk.StringVar(self, VIDEO_FORMAT_DEFAULT)
        self.audio_quality = tk.StringVar(self, AUDIO_QUALITY_DEFAULT)
        self.audio_format = tk.StringVar(self, AUDIO_FORMAT_DEFAULT)

        self.block_sponsor = tk.BooleanVar(self, True)
        self.block_selfpromo = tk.BooleanVar(self, True)
        self.block_interaction = tk.BooleanVar(self, True)
        self.block_intro = tk.BooleanVar(self, False)
        self.block_outro = tk.BooleanVar(self, False)
        self.block_preview = tk.BooleanVar(self, False)
        self.block_filler = tk.BooleanVar(self, False)
        self.block_hook = tk.BooleanVar(self, False)
        self.block_music_offtopic = tk.BooleanVar(self, False)

        self.embed_subtitles = tk.BooleanVar(self, False)
        self.embed_thumbnail = tk.BooleanVar(self, True)
        self.embed_metadata = tk.BooleanVar(self, True)

        self.frame_url = tk.Frame(self)
        self.frame_url.grid(row=self._get_row(), column=0)
        self.label_url = tk.Label(self.frame_url, text="URL:")
        self.label_url.grid(row=0, column=0)
        self.entry_url = tk.Entry(self.frame_url, textvariable=self.url)
        self.entry_url.grid(row=0, column=1)

        self._create_frame_video_audio()

        self._create_frame_video_options()
        # self.frame_video_options.grid_remove()

        self._create_frame_audio_options()
        self.frame_audio_options.grid_remove()

        self._create_frame_embedding()

        self.mainloop()

    def _get_row(self, increment: bool=True) -> int:
        current = self.current_row
        if increment:
            self.current_row += 1
        return current
    
    def _create_frame_video_audio(self):
        self.frame_video_audio = tk.Frame(self)
        self.frame_video_audio.grid(row=self._get_row(), column=0)

        self.label_media_type = tk.Label(self.frame_video_audio, text="Media Type:")
        self.label_media_type.grid(row=0, column=0, columnspan=2)

        self.radio_video = tk.Radiobutton(self.frame_video_audio, text="Video", variable=self.media_mode, value=MediaMode.VIDEO)
        self.radio_video.grid(row=1, column=0)

        self.radio_audio = tk.Radiobutton(self.frame_video_audio, text="Audio", variable=self.media_mode, value=MediaMode.AUDIO)
        self.radio_audio.grid(row=1, column=1)

    def _create_frame_video_options(self):
        self.frame_video_options = tk.Frame(self)
        self.frame_video_options.grid(row=self._get_row(False), column=0)

        self.label_video_options = tk.Label(self.frame_video_options, text="Video Options")
        self.label_video_options.grid(row=0, column=0, columnspan=2)

        self.label_quality = tk.Label(self.frame_video_options, text="Quality")
        self.label_quality.grid(row=1, column=0)

        self.optionmenu_quality = tk.OptionMenu(self.frame_video_options, self.video_quality, self.video_quality.get(), *VIDEO_QUALITY)
        self.optionmenu_quality.grid(row=1, column=1)

        self.label_video_format = tk.Label(self.frame_video_options, text="Output Format:")
        self.label_video_format.grid(row=2, column=0)

        self.optionmenu_video_format = tk.OptionMenu(self.frame_video_options, self.video_format, self.video_format.get(), *VIDEO_FORMAT)
        self.optionmenu_video_format.grid(row=2, column=1)
        
        self._create_frame_sponsorblock()

    def _create_frame_sponsorblock(self):
        self.frame_sponsorblock = tk.Frame(self.frame_video_options)
        self.frame_sponsorblock.grid(row=3, column=0, columnspan=2)

        self.label_sponserblock = tk.Label(self.frame_sponsorblock, text="SponsorBlock - Remove Segments")
        self.label_sponserblock.grid(row=0, column=0, columnspan=3)

        self.checkbutton_sponsor = tk.Checkbutton(self.frame_sponsorblock, text="Sponsor", variable=self.block_sponsor)
        self.checkbutton_sponsor.grid(row=1, column=0)

        self.checkbutton_selfpromo = tk.Checkbutton(self.frame_sponsorblock, text="Self Promotion", variable=self.block_selfpromo)
        self.checkbutton_selfpromo.grid(row=2, column=0)

        self.checkbutton_interaction = tk.Checkbutton(self.frame_sponsorblock, text="Interaction Reminder", variable=self.block_interaction)
        self.checkbutton_interaction.grid(row=3, column=0)

        self.checkbutton_intro = tk.Checkbutton(self.frame_sponsorblock, text="Intro Animation", variable=self.block_intro)
        self.checkbutton_intro.grid(row=1, column=1)

        self.checkbutton_outro = tk.Checkbutton(self.frame_sponsorblock, text="Endcards/Credits", variable=self.block_outro)
        self.checkbutton_outro.grid(row=2, column=1)

        self.checkbutton_preview = tk.Checkbutton(self.frame_sponsorblock, text="Preview/Recap", variable=self.block_preview)
        self.checkbutton_preview.grid(row=3, column=1)

        self.checkbutton_hook = tk.Checkbutton(self.frame_sponsorblock, text="Hook/Greeting", variable=self.block_hook)
        self.checkbutton_hook.grid(row=1, column=2)

        self.checkbutton_filler = tk.Checkbutton(self.frame_sponsorblock, text="Tangents/Jokes", variable=self.block_filler)
        self.checkbutton_filler.grid(row=2, column=2)

        self.checkbutton_music_offtopic = tk.Checkbutton(self.frame_sponsorblock, text="Non-Music Section", variable=self.block_music_offtopic)
        self.checkbutton_music_offtopic.grid(row=3, column=2)

    def _create_frame_audio_options(self):
        self.frame_audio_options = tk.Frame(self)
        self.frame_audio_options.grid(row=self._get_row(), column=0)

        self.label_audio_options = tk.Label(self.frame_audio_options, text="Audio Options")
        self.label_audio_options.grid(row=0, column=0, columnspan=2)

        self.label_audio_quality = tk.Label(self.frame_audio_options, text="Audio Quality:")
        self.label_audio_quality.grid(row=1, column=0)

        self.optionmenu_audio_quality = tk.OptionMenu(self.frame_audio_options, self.audio_quality, self.audio_quality.get(), *AUDIO_QUALITY)
        self.optionmenu_audio_quality.grid(row=1, column=1)

        self.label_audio_format = tk.Label(self.frame_audio_options, text="Audio Format:")
        self.label_audio_format.grid(row=2, column=0)

        self.optionmenu_audio_format = tk.OptionMenu(self.frame_audio_options, self.audio_format, self.audio_format.get(), *AUDIO_FORMAT)
        self.optionmenu_audio_format.grid(row=2, column=1)

    def _create_frame_embedding(self):
        self.frame_embedding = tk.Frame(self)
        self.frame_embedding.grid(row=self._get_row(), column=0)

        self.label_embedding = tk.Label(self.frame_embedding, text="Embedding")
        self.label_embedding.grid(row=0, column=0, columnspan=3)

        self.checkbutton_subtitles = tk.Checkbutton(self.frame_embedding, text="Subtitles", variable=self.embed_subtitles)
        self.checkbutton_subtitles.grid(row=1, column=0)

        self.checkbutton_thumbnail = tk.Checkbutton(self.frame_embedding, text="Thumbnail", variable=self.embed_thumbnail)
        self.checkbutton_thumbnail.grid(row=1, column=1)

        self.checkbutton_metadata = tk.Checkbutton(self.frame_embedding, text="Metadata", variable=self.embed_metadata)
        self.checkbutton_metadata.grid(row=1, column=2)


if __name__ == "__main__":
    RytDlpGui()
