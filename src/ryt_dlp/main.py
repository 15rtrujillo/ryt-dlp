from ryt_dlp.command_builder import CommandBuilder
from ryt_dlp.constants import *
from ryt_dlp.download_manager import DownloadManager
from ryt_dlp.media_mode import MediaMode

import tkinter as tk
import tkinter.filedialog as filedialog


class RytDlpGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ryt-dlp")

        self.url = tk.StringVar(self)
        self.media_mode = tk.IntVar(self, MediaMode.VIDEO)
        self.video_quality = tk.StringVar(self, VIDEO_QUALITY_DEFAULT)
        self.video_format = tk.StringVar(self, VIDEO_FORMAT_DEFAULT)
        self.video_fps = tk.StringVar(self, VIDEO_FPS_DEFAULT)
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

        self.directory = tk.StringVar(self)
        self.file_name_template = tk.StringVar(self, "%(title)s.%(ext)s")

        self.advanced_options = tk.BooleanVar(self, False)
        self.min_sleep = tk.StringVar(self, "5")
        self.max_sleep = tk.StringVar(self, "0")
        self.rate_limit = tk.StringVar(self)
        self.js_runtime = tk.StringVar(self, JS_RUNTIME_DEFAULT)
        self.js_runtime_path = tk.StringVar(self)
        self.use_cookies = tk.BooleanVar(self, False)
        self.browser = tk.StringVar(self, BROWSER_DEFAULT)

        self.media_mode.trace_add("write", self._media_mode_changed)
        self.video_format.trace_add("write", self._embed_subs_changed)
        self.advanced_options.trace_add("write", self._advanced_options_changed)
        self.use_cookies.trace_add("write", self._use_cookies_changed)

        self.validate_command_spinbox = (self.register(self._validate_spinbox), '%P')

        self.frame_column1 = tk.Frame(self)
        self.frame_column1.grid(row=0, column=0)

        self._create_frame_url(self.frame_column1, 0, 0)

        self._create_frame_video_audio(self.frame_column1, 1, 0)

        self._create_frame_video_options(self.frame_column1, 2, 0)

        self._create_frame_audio_options(self.frame_column1, 2, 0)
        self.frame_audio_options.grid_remove()

        self._create_frame_embedding(self.frame_column1, 3, 0)

        self.frame_column2 = tk.Frame(self)
        self.frame_column2.grid(row=0, column=1)

        self._create_frame_download_options(self.frame_column2, 0, 0)
        self.frame_advanced_options.grid_remove()
        self.optionmenu_browser.grid_remove()

        self.button_download = tk.Button(self, text="Download", command=self._button_download_clicked)
        self.button_download.grid(row=1, column=0, columnspan=2)

        self._create_frame_output(self, 2, 0)

        self.mainloop()
    
    def _validate_spinbox(self, text: str) -> bool:
        if text == "":
            return True
        return text.isdigit() and 0 <= int(text) <= 3600
    
    def _create_frame_url(self, parent, row: int, column: int):
        self.frame_url = tk.Frame(parent)
        self.frame_url.grid(row=row, column=column)
        self.label_url = tk.Label(self.frame_url, text="URL:")
        self.label_url.grid(row=0, column=0)
        self.entry_url = tk.Entry(self.frame_url, textvariable=self.url)
        self.entry_url.grid(row=0, column=1)
    
    def _create_frame_video_audio(self, parent, row: int, column: int):
        self.frame_video_audio = tk.LabelFrame(parent, text="Media Type")
        self.frame_video_audio.grid(row=row, column=column)

        self.radio_video = tk.Radiobutton(self.frame_video_audio, text="Video", variable=self.media_mode, value=MediaMode.VIDEO)
        self.radio_video.grid(row=0, column=0)

        self.radio_audio = tk.Radiobutton(self.frame_video_audio, text="Audio", variable=self.media_mode, value=MediaMode.AUDIO)
        self.radio_audio.grid(row=0, column=1)

    def _create_frame_video_options(self, parent, row: int, column: int):
        self.frame_video_options = tk.LabelFrame(parent, text="Video Options")
        self.frame_video_options.grid(row=row, column=column)

        self.label_video_format = tk.Label(self.frame_video_options, text="Output Format:")
        self.label_video_format.grid(row=0, column=0)

        self.optionmenu_video_format = tk.OptionMenu(self.frame_video_options, self.video_format, self.video_format.get(), *VIDEO_FORMATS)
        self.optionmenu_video_format.grid(row=0, column=1)

        self.label_quality = tk.Label(self.frame_video_options, text="Quality")
        self.label_quality.grid(row=1, column=0)

        self.optionmenu_quality = tk.OptionMenu(self.frame_video_options, self.video_quality, self.video_quality.get(), *VIDEO_QUALITIES)
        self.optionmenu_quality.grid(row=1, column=1)

        self.label_fps = tk.Label(self.frame_video_options, text="FPS:")
        self.label_fps.grid(row=2, column=0)

        self.optionmenu_fps = tk.OptionMenu(self.frame_video_options, self.video_fps, self.video_fps.get(), *VIDEO_FPSES)
        self.optionmenu_fps.grid(row=2, column=1)
        
        self._create_frame_sponsorblock(self.frame_video_options, 3, 0)

    def _create_frame_sponsorblock(self, parent, row: int, column: int):
        self.frame_sponsorblock = tk.LabelFrame(parent, text="SponsorBlock - Remove Segments")
        self.frame_sponsorblock.grid(row=row, column=column, columnspan=2)

        self.checkbutton_sponsor = tk.Checkbutton(self.frame_sponsorblock, text="Sponsor", variable=self.block_sponsor)
        self.checkbutton_sponsor.grid(row=0, column=0)

        self.checkbutton_selfpromo = tk.Checkbutton(self.frame_sponsorblock, text="Self Promotion", variable=self.block_selfpromo)
        self.checkbutton_selfpromo.grid(row=1, column=0)

        self.checkbutton_interaction = tk.Checkbutton(self.frame_sponsorblock, text="Interaction Reminder", variable=self.block_interaction)
        self.checkbutton_interaction.grid(row=2, column=0)

        self.checkbutton_intro = tk.Checkbutton(self.frame_sponsorblock, text="Intro Animation", variable=self.block_intro)
        self.checkbutton_intro.grid(row=0, column=1)

        self.checkbutton_outro = tk.Checkbutton(self.frame_sponsorblock, text="Endcards/Credits", variable=self.block_outro)
        self.checkbutton_outro.grid(row=1, column=1)

        self.checkbutton_preview = tk.Checkbutton(self.frame_sponsorblock, text="Preview/Recap", variable=self.block_preview)
        self.checkbutton_preview.grid(row=2, column=1)

        self.checkbutton_hook = tk.Checkbutton(self.frame_sponsorblock, text="Hook/Greeting", variable=self.block_hook)
        self.checkbutton_hook.grid(row=0, column=2)

        self.checkbutton_filler = tk.Checkbutton(self.frame_sponsorblock, text="Tangents/Jokes", variable=self.block_filler)
        self.checkbutton_filler.grid(row=1, column=2)

        self.checkbutton_music_offtopic = tk.Checkbutton(self.frame_sponsorblock, text="Non-Music Section", variable=self.block_music_offtopic)
        self.checkbutton_music_offtopic.grid(row=2, column=2)

    def _create_frame_audio_options(self, parent, row: int, column: int):
        self.frame_audio_options = tk.LabelFrame(parent, text="Audio Options")
        self.frame_audio_options.grid(row=row, column=column)

        self.label_audio_format = tk.Label(self.frame_audio_options, text="Output Format:")
        self.label_audio_format.grid(row=0, column=0)

        self.optionmenu_audio_format = tk.OptionMenu(self.frame_audio_options, self.audio_format, self.audio_format.get(), *AUDIO_FORMATS)
        self.optionmenu_audio_format.grid(row=0, column=1)

        self.label_audio_quality = tk.Label(self.frame_audio_options, text="Quality:")
        self.label_audio_quality.grid(row=1, column=0)

        self.optionmenu_audio_quality = tk.OptionMenu(self.frame_audio_options, self.audio_quality, self.audio_quality.get(), *AUDIO_QUALITIES)
        self.optionmenu_audio_quality.grid(row=1, column=1)

    def _create_frame_embedding(self, parent, row: int, column: int):
        self.frame_embedding = tk.LabelFrame(parent, text="Embedding")
        self.frame_embedding.grid(row=row, column=column)

        self.checkbutton_subtitles = tk.Checkbutton(self.frame_embedding, text="Subtitles", variable=self.embed_subtitles)
        self.checkbutton_subtitles.grid(row=0, column=0)

        self.checkbutton_thumbnail = tk.Checkbutton(self.frame_embedding, text="Thumbnail", variable=self.embed_thumbnail)
        self.checkbutton_thumbnail.grid(row=0, column=1)

        self.checkbutton_metadata = tk.Checkbutton(self.frame_embedding, text="Metadata", variable=self.embed_metadata)
        self.checkbutton_metadata.grid(row=0, column=2)

    def _create_frame_download_options(self, parent, row: int, column: int):
        self.frame_download_options = tk.LabelFrame(parent, text="Download Options")
        self.frame_download_options.grid(row=row, column=column)

        self.frame_directory = tk.Frame(self.frame_download_options)
        self.frame_directory.grid(row=0, column=0)

        self.label_directory = tk.Label(self.frame_directory, text="Download Directory:")
        self.label_directory.grid(row=0, column=0)

        self.entry_directory = tk.Entry(self.frame_directory, textvariable=self.directory)
        self.entry_directory.grid(row=0, column=1)

        self.button_browse_directory = tk.Button(self.frame_directory, text="Browse", command=self._button_browse_directory_clicked)
        self.button_browse_directory.grid(row=0, column=2)

        self.frame_file_name_template = tk.Frame(self.frame_download_options)
        self.frame_file_name_template.grid(row=1, column=0)

        self.label_file_name_template = tk.Label(self.frame_file_name_template, text="File Name Template:")
        self.label_file_name_template.grid(row=0, column=0)

        self.entry_file_name_template = tk.Entry(self.frame_file_name_template, textvariable=self.file_name_template)
        self.entry_file_name_template.grid(row=0, column=1)

        self.checkbutton_advanced_options = tk.Checkbutton(self.frame_download_options, text="Advanced Options", variable=self.advanced_options)
        self.checkbutton_advanced_options.grid(row=2, column=0)

        self._create_frame_advanced_options(self.frame_download_options, 3, 0)

    def _create_frame_advanced_options(self, parent, row: int, column: int):
        self.frame_advanced_options = tk.LabelFrame(parent, text="Advanced Options")
        self.frame_advanced_options.grid(row=row, column=column)

        self.frame_sleep = tk.Frame(self.frame_advanced_options)
        self.frame_sleep.grid(row=0, column=0)

        self.label_sleep_interval = tk.Label(self.frame_sleep, text="Sleep (Min/Max):")
        self.label_sleep_interval.grid(row=0, column=0)

        self.spinbox_sleep_min = tk.Spinbox(self.frame_sleep, from_=0, to=3600, textvariable=self.min_sleep, validate="key", validatecommand=self.validate_command_spinbox, width=5)
        self.spinbox_sleep_min.grid(row=0, column=1)

        self.label_sleep_to = tk.Label(self.frame_sleep, text="to")
        self.label_sleep_to.grid(row=0, column=2)

        self.spinbox_sleep_max = tk.Spinbox(self.frame_sleep, from_=0, to=3600, textvariable=self.max_sleep, validate="key", validatecommand=self.validate_command_spinbox, width=5)
        self.spinbox_sleep_max.grid(row=0, column=3)

        self.frame_rate_limit = tk.Frame(self.frame_advanced_options)
        self.frame_rate_limit.grid(row=1, column=0)

        self.label_rate_limit = tk.Label(self.frame_rate_limit, text="Rate Limit (bytes/s):")
        self.label_rate_limit.grid(row=0, column=0)

        self.entry_rate_limit = tk.Entry(self.frame_rate_limit, textvariable=self.rate_limit, width=10)
        self.entry_rate_limit.grid(row=0, column=1)

        self.frame_js_runtime = tk.LabelFrame(self.frame_advanced_options, text="JavaScript Runtime")
        self.frame_js_runtime.grid(row=2, column=0)

        self.label_js_runtime = tk.Label(self.frame_js_runtime, text="Runtime:")
        self.label_js_runtime.grid(row=0, column=0)

        self.optionmenu_js_runtime = tk.OptionMenu(self.frame_js_runtime, self.js_runtime, self.js_runtime.get(), *JS_RUNTIMES)
        self.optionmenu_js_runtime.grid(row=0, column=1)

        self.label_js_runtime_path = tk.Label(self.frame_js_runtime, text="Path:")
        self.label_js_runtime_path.grid(row=1, column=0)

        self.entry_js_runtime_path = tk.Entry(self.frame_js_runtime, textvariable=self.js_runtime_path)
        self.entry_js_runtime_path.grid(row=1, column=1)

        self.frame_cookies = tk.Frame(self.frame_advanced_options)
        self.frame_cookies.grid(row=3, column=0)

        self.checkbutton_cookies = tk.Checkbutton(self.frame_cookies, text="Use cookies for auth", variable=self.use_cookies)
        self.checkbutton_cookies.grid(row=0, column=0)

        self.optionmenu_browser = tk.OptionMenu(self.frame_cookies, self.browser, self.browser.get(), *BROWSERS)
        self.optionmenu_browser.grid(row=0, column=1)

    def _create_frame_output(self, parent, row: int, column: int):
        self.frame_output = tk.LabelFrame(parent, text="Output Console")
        self.frame_output.grid(row=row, column=column, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.text_output = tk.Text(self.frame_output, height=10, width=80, state="disabled", wrap="word")
        self.text_output.grid(row=0, column=0, sticky="nsew")

        # 3. Create the Scrollbar
        self.scrollbar_output = tk.Scrollbar(self.frame_output, orient="vertical", command=self.text_output.yview)
        self.scrollbar_output.grid(row=0, column=1, sticky="ns")

        self.text_output.configure(yscrollcommand=self.scrollbar_output.set)

        self.frame_output.grid_columnconfigure(0, weight=1)
        self.frame_output.grid_rowconfigure(0, weight=1)

    def _media_mode_changed(self, *_):
        if self.media_mode.get() == MediaMode.VIDEO:
            self.frame_video_options.grid()
            if self.video_format.get() in VIDEO_FORMAT_ALLOWS_SUBS:
                self.checkbutton_subtitles.grid()
            self.frame_audio_options.grid_remove()
        elif self.media_mode.get() == MediaMode.AUDIO:
            self.frame_video_options.grid_remove()
            self.checkbutton_subtitles.grid_remove()
            self.frame_audio_options.grid()

    def _advanced_options_changed(self, *_):
        if self.advanced_options.get():
            self.frame_advanced_options.grid()
        else:
            self.frame_advanced_options.grid_remove()

    def _use_cookies_changed(self, *_):
        if self.use_cookies.get():
            self.optionmenu_browser.grid()
            self.checkbutton_cookies.configure(text="Use cookies from")
        else:
            self.optionmenu_browser.grid_remove()
            self.checkbutton_cookies.configure(text="Use cookies for auth")

    def _embed_subs_changed(self, *_):
        if self.video_format.get() in VIDEO_FORMAT_ALLOWS_SUBS:
            self.checkbutton_subtitles.grid()
        else:
            self.checkbutton_subtitles.grid_remove()

    def _button_browse_directory_clicked(self):
        dir = filedialog.askdirectory()
        self.directory.set(dir)

    def _button_download_clicked(self):
        self.button_download.configure(state=tk.DISABLED)
        self.text_output.configure(state=tk.NORMAL)
        self.text_output.delete(1.0, tk.END)
        self.text_output.configure(state=tk.DISABLED)

        builder = CommandBuilder()
        if self.media_mode.get() == MediaMode.VIDEO:
            sponsorblock = {
                "sponsor": self.block_sponsor.get(),
                "selfpromo": self.block_selfpromo.get(),
                "interaction": self.block_interaction.get(),
                "intro": self.block_intro.get(),
                "outro": self.block_outro.get(),
                "filler": self.block_filler.get(),
                "hook": self.block_hook.get(),
                "music_offtopic": self.block_music_offtopic.get()
            }
            
            builder = (builder.with_video_format(self.video_format.get())
                       .with_video_quality(self.video_quality.get(), self.video_fps.get())
                       .with_sponsorblock(**sponsorblock))
            
            if  self.video_format.get() in VIDEO_FORMAT_ALLOWS_SUBS and self.embed_subtitles.get():
                builder.embed_subtitles()
        else:
            builder = (builder.extract_audio()
                       .with_audio_format(self.audio_format.get())
                       .with_audio_quality(AUDIO_QUALITY_LABEL_TO_VALUE[self.audio_quality.get()]))
        
        if self.embed_metadata.get():
            builder.embed_metadata()
        if self.embed_thumbnail.get():
            builder.embed_thumbnail()

        builder = (builder.with_output_directory(self.directory.get())
                   .with_file_name_template(self.file_name_template.get()))
        
        if self.advanced_options.get():
            if self.min_sleep.get().isdigit() and self.min_sleep.get() != "" and int(self.min_sleep.get()) > 0:
                builder.with_min_sleep(int(self.min_sleep.get()))

            if self.max_sleep.get().isdigit() and self.max_sleep.get() != "" and int(self.max_sleep.get()) > 0:
                builder.with_max_sleep(int(self.max_sleep.get()))

            builder = (builder.with_rate_limit(self.rate_limit.get())
                       .with_js_runtime(self.js_runtime.get(), self.js_runtime_path.get()))
            
            if self.use_cookies.get():
                builder.with_browser_cookies(self.browser.get())

        command_list = builder.build(self.url.get())
        download = DownloadManager(command_list, self._update_output, self._download_complete)
        download.start()

    def _update_output(self, line: str):
        self.after(0, self._text_output_safe_insert, line)

    def _download_complete(self):
        self.button_download.configure(state=tk.ACTIVE)
        self._text_output_safe_insert("Done!")

    def _text_output_safe_insert(self, line):
        self.text_output.configure(state=tk.NORMAL)
        self.text_output.insert(tk.END, line)
        self.text_output.see(tk.END)
        self.text_output.configure(state=tk.DISABLED)


if __name__ == "__main__":
    RytDlpGui()
