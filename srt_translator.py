import srt
import os
import sys
from google.cloud import translate_v3 as translate
import time
import threading
import getopt


translate_settings = {
    "threaded": False,
    "language": "en",
    "directories": [],
    "srtFiles": []
}


def translate_text(
    text: str = "YOUR_TEXT_TO_TRANSLATE", target_language: str = "TRANSLATION_LANGUAGE"
) -> translate.TranslationServiceClient:
    
    client = translate.TranslationServiceClient()
    project_id = "l9gigatranslator"
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    model_path = f"{parent}/models/general/nmt"

    response = client.translate_text(
        contents = [text],
        target_language_code = target_language,
        parent = parent,
        mime_type = "text/plain",
        #source_language_code = "en",
        model = model_path
    )
    return response


def load_data(srt_file_path):
    srt_file = open(srt_file_path, "r", encoding="utf-8")
    return srt_file.read()


def single_line_text(text: str) -> str:
    split_text = text.split('\n')
    return ' '.join(split_text)


def multi_line_text(text: str):
    result = text
    if len(text) > 35:
        text_words = text.split()
        word_count = len(text_words)
        endl_position = int(word_count / 2)
        first_part = ' '.join(text_words[:endl_position])
        second_part = ' '.join(text_words[endl_position:])
        result = f"{first_part}\n{second_part}"
    return result


def translate_subtitle(subtitle, destination_language):
    if isinstance(subtitle, bytes):
        subtitle = subtitle.decode("utf-8")
    subtitle = single_line_text(subtitle)
    result = translate_text(text = subtitle, target_language = destination_language)
    translated_result = result.translations[0].translated_text
    translated_result = multi_line_text(translated_result)
    print(f"\n\n{subtitle}\n--------------------\n{translated_result}\n\n")
    return translated_result
    

def save_translated_srt(subtitles, file_name):
    srt_file = open(file_name, "a", encoding="utf-16")
    composed_srt = srt.compose(subtitles)
    srt_file.write(composed_srt)


# destination_language -> language code to translate to
def translate_srt_file(srt_file_path, destination_language, translated_srt_path):
    time_start = time.time()
    data = load_data(srt_file_path)
    subtitles = list(srt.parse(data))
    for sub in subtitles:
        # TODO: add delay to avoid getting rate limited by google
        sub.content = translate_subtitle(sub.content, destination_language)
    save_translated_srt(subtitles, translated_srt_path)
    time_end = time.time()
    print(f"\n[TRANSLATED ({time_end - time_start})]: {srt_file_path}\n")


def dir_translate(directories: list[str]):
    for directory in directories:
        try:
            files = os.listdir(directory)
            for file in files:
                if file.endswith(".srt"):
                    translated_srt_path = directory + "\\"+ file[:-4] + "." + translate_settings["language"] + ".srt"
                    if(sys.argv.__contains__("-t")):
                        t = threading.Thread(target = translate_srt_file, args = (directory + "\\" + file, translate_settings["language"], translated_srt_path))
                        t.start()
                    else:
                        translate_srt_file(directory + "\\" + file, translate_settings["language"], translated_srt_path)
        except NotADirectoryError as err:
            print(err)


def srt_translate(srt_files: list[str]):
    for srt_file in srt_files:
        translated_srt_path = srt_file[:-4] + "." + translate_settings["language"] + ".srt"
        if translate_settings["threaded"] == True:
            t = threading.Thread(target = translate_srt_file, args = (srt_file, translate_settings["language"], translated_srt_path))
            t.start()
        else:
            translate_srt_file(srt_file, translate_settings["language"], translated_srt_path)


# TODO: implement BCP-47 language code validation
def validate_language(language: str):
    return True


'''
Example usage:
> python srt_translator.py -t --l=hr --d="D:\Movies\ExampleMovie","D:\Movies\ExampleMovie"
> python srt_translator.py -t --l=hr --srt="D:\Movies\ExampleMovie\subtitle.srt","D:\Movies\ExampleMovie\subtitle2.srt"
'''

if __name__ == "__main__":
    
    try:
        options, arguments = getopt.getopt(
            sys.argv[1:], 
            "tldh", 
            ["threaded", "language=", "directory=", "srt=", "help"]
        )
    except getopt.GetoptError as err:
        print(err)
    
    for option, argument in options:
        if option in ("-t", "--threaded"):
            translate_settings["threaded"] = True
        if option in ("--l", "--language"):
            translate_settings["language"] = argument
        if option in ("--d", "--directory"):
            translate_settings["directories"] = argument.split(',')
        if option in ("--srt", "--subtitle-file"):
            translate_settings["srtFiles"] = argument.split(',')
        if option in ("-h", "--help"):
            print("\nTODO: implement help option")

    if len(translate_settings["directories"]) > 0:
        dir_translate(translate_settings["directories"])

    if len(translate_settings["srtFiles"]) > 0:
        srt_translate(translate_settings["srtFiles"])


############################
    # print(f"\nTranslation started at {time.asctime(time.localtime())}")

    # if(sys.argv.__contains__("-t")):
    #     print(f"\nThreading: ON\n")

    # # Translate every srt file in provided directory
    # if sys.argv[1] == "-d":
    #     directory = sys.argv[4]
    #     destination_language = sys.argv[1]
    #     files = os.listdir(directory)
    #     for file in files:
    #         if file.endswith(".srt"):
    #             translated_srt_path = directory + "\\"+ file[:-4] + "." + destination_language + ".srt"
    #             if(sys.argv.__contains__("-t")):
    #                 t = threading.Thread(target = translate_srt_file, args = (directory + "\\" + file, destination_language, translated_srt_path))
    #                 t.start()
    #                 print(f"\nNew thread started")
    #             else:
    #                 translate_srt_file(directory + "\\" + file, destination_language, translated_srt_path)

    # # Provide multiple paths of srt files as command line arguments
    # else:
    #     srt_files = sys.argv[1:]
    #     destination_language = sys.argv[1]
    #     for srt_file in srt_files:
    #         if srt_file == "-t":
    #             continue
    #         translated_srt_path = srt_file[:-4] + "_-TRANSLATED.srt"
    #         if(sys.argv.__contains__("-t")):
    #             t = threading.Thread(target = translate_srt_file, args = (srt_file, destination_language, translated_srt_path))
    #             t.start()
    #         else:
    #             print(f"\nThreading: OFF\n")
    #             translate_srt_file(srt_file, destination_language, translated_srt_path)
