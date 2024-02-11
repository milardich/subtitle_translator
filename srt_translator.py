from googletrans import Translator, constants
import srt

# init the Google API translator
translator = Translator()

############### example: #############################
# translation = translator.translate("We have to cook, Jesse!", dest="hr")
# print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")


def load_data(srt_file_path):
    srt_file = open(srt_file_path, "r")
    return srt_file.read()


def translate_subtitle(subtitle, destination_language):
    translation = translator.translate(subtitle.content, dest = destination_language)
    return translation.text
    

def save_translated_srt(subtitles, file_name):
    srt_file = open(file_name, "a")
    composed_srt = srt.compose(subtitles)
    srt_file.write(composed_srt)


# destination_language -> language code to translate to
def translate_srt_file(srt_file_path, destination_language, translated_srt_path):
    data = load_data(srt_file_path)
    subtitles = list(srt.parse(data))
    for sub in subtitles:
        # TODO: add delay to avoid getting rate limited by google
        sub.content = translate_subtitle(sub, destination_language)
    save_translated_srt(subtitles, translated_srt_path)


if __name__ == "__main__":
    srt_file_path = "D:\\Downloads\\bb_srt_test.srt"
    language = "hr"
    translated_srt_path = "D:\\Downloads\\bb_srt_test-TRANSLATED.srt"
    translate_srt_file(srt_file_path, language, translated_srt_path)

    