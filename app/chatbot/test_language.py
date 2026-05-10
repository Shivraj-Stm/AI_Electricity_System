from language_utils import detect_language, to_english, from_english

print(detect_language("मेरा बिल दिखाओ"))
print(to_english("मेरा बिल दिखाओ", "hi"))
print(from_english("Here is your bill", "hi"))
