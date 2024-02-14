## About this project
#### This python script translates subtitles to a desired language. Translation is performed using the Google Cloud Translation API, so please ensure you adhere to the [rate limits](https://cloud.google.com/translate/quotas).

#

### Setup
- [Google cloud console setup](https://cloud.google.com/translate/docs/setup)
- [Install gcloud CLI](https://cloud.google.com/translate/docs/authentication)
- after gcloud setup is complete and you are successfully logged in, enter this command: <br>
`gcloud auth application-default login`
([https://cloud.google.com/docs/authentication/gcloud#gcloud-credentials](https://cloud.google.com/docs/authentication/gcloud#gcloud-credentials))
- Setup should be done now.
- For more information, visit [Google Translation documentation](https://cloud.google.com/translate/docs)
<br>

#

### Example usage
- `python.exe srt_translator.py -t --l=hr --d="D:\ExampleDirectory","D:\ExampleDirectory"`
- Scans directories for .srt files, loops through each file, and translates the subtitles.

<br>

- `python.exe srt_translator.py -t --l=hr --srt="D:\ExampleDirectory\sub1.srt","D:\ExampleDirectory\sub2.srt"`
- Loops through provided .srt files and translates the subtitles

<br>

- After the translation is complete, a new .srt file is created in the same directory with the translated content.


#### Flags:
`--d` or `--directory`: specifies directories to scan and translate (use `,` as separator for multiple directories) <br>
`--t` or `--threaded`: runs multiple threads for faster execution <br>
`--l` or `--language`: specifies translation language in BCP-47 language code (eg. `--l:en` for English) <br>
`--srt` or `--subtitle-file`: specifies subtitle files to translate (use `,` as separator for multiple .srt files)<br>

<br>

#

### TODO:
- ### Validate language code
- ### Implement `--help` command
