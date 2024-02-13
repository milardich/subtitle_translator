## About this project
#### This python script translates subtitles to a desired language. Translation is done by using Google Cloud Translation API so make sure you stay within the [rate limits](https://cloud.google.com/translate/quotas).

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
`python.exe srt_translator.py -d "D:\ExampleDirectory" -t`
- Scans the directory for .srt files, loops through each file, and translates the subtitles.
<br>

`python.exe srt_translator.py "D:\ExampleDirectory\example_subtitles1.srt" "D:\ExampleDirectory\example_subtitles2.srt" -t`
- Loops through provided .srt files and translates the subtitles

- After the translation is complete, a new .srt file is created in the same directory with the translated content.
- `"D:\ExampleDirectory\example_subtitles1_-TRANSLATED.srt"` 


#### Flags:
`-d`: specifies directory <br>
`-t`: runs multiple threads for faster execution

<br>

#

### TODO:
- ### Specify destination language as command line argument (language to translate to)
    - Currently, it only translates en -> hr
