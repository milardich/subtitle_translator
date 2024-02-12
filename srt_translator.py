import srt
import os
import sys
from google.cloud import translate_v2 as translate
import time
import threading


def load_data(srt_file_path):
    srt_file = open(srt_file_path, "r", encoding="utf-8")
    return srt_file.read()


def translate_subtitle(subtitle, destination_language):
    translator = translate.Client()
    if isinstance(subtitle, bytes):
        subtitle = subtitle.decode("utf-8")
    result = translator.translate(subtitle, target_language=destination_language, format_= "text")
    translated_result = result["translatedText"]
    print(f"\n\n{subtitle}\n_________________________\n{translated_result}\n\n")
    return result["translatedText"]
    

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


if __name__ == "__main__":
    # test = translate_subtitle("Oh my god, Chechen men are attacking railroad. Why?", "hr")
    # print(test)

    print(f"\nTranslation started at {time.asctime(time.localtime())}")

    if(sys.argv.__contains__("-t")):
        print(f"\nThreading: ON\n")

    # Translate every srt file in provided directory
    if sys.argv[1] == "-d":
        directory = sys.argv[2]
        files = os.listdir(directory)
        for file in files:
            if file.endswith(".srt"):
                translated_srt_path = directory + "\\"+ file[:-4] + "_-TRANSLATED.srt"
                if(sys.argv.__contains__("-t")):
                    t = threading.Thread(target = translate_srt_file, args = (directory + "\\" + file, "hr", translated_srt_path))
                    t.start()
                    print(f"\nNew thread started")
                else:
                    translate_srt_file(directory + "\\" + file, "hr", translated_srt_path)
                #translate_srt_file(directory + "\\" + file, "hr", translated_srt_path)

    # Provide paths of srt files as command line arguments
    else:
        srt_files = sys.argv[1:]
        for srt_file in srt_files:
            if srt_file == "-t":
                continue
            translated_srt_path = srt_file[:-4] + "_-TRANSLATED.srt"
            language = "hr"
            if(sys.argv.__contains__("-t")):
                t = threading.Thread(target = translate_srt_file, args = (srt_file, language, translated_srt_path))
                t.start()
            else:
                print(f"\nThreading: OFF\n")
                translate_srt_file(srt_file, language, translated_srt_path)
            #translate_srt_file(srt_file, language, translated_srt_path)
