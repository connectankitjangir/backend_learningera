# typing/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import TypingPassage
from datetime import timedelta
from typing_tests.models import TypingPassage
import re



def split_passage(passage):
    return re.findall(r'\S+\s*', passage)

def typing_result(request, passage_id):
    passage = get_object_or_404(TypingPassage, id=passage_id)
    given_passage = passage.passage_text
    typed_passage = request.POST.get("typed_text")
    time_select = request.POST.get("time_select")
    total_time = int(time_select) * 60
    print('time_select', time_select)
    try:
        time_remaining = int(request.POST.get("time_remaining"))
    except:
        time_remaining = 0
    print('time_remaining', time_remaining)
    given_passage_words = split_passage(given_passage)
    # given_passage_length = len(given_passage_words)
    typed_passage_words = split_passage(typed_passage)
    
    # Initialize error counts
    # capital_errors = omission_errors = spelling_errors = space_errors = punctuation_errors = transposition_errors = 0
    iterator_given_passage = 0
    last_given_match_index = last_typed_match_index = -1
    matched_word_list = []
    punctuation_errors_list = []
    space_errors_list = []
    capital_errors_list = []
    omission_errors_list = []
    extra_typed_errors_list = []
    transposition_errors_list = []
    spelling_errors_list = []
    missing_words_list = []
    spelling_errors_original_list = []
    swap = False
    original_word_index = 0

    def spelling_omission_errors(last_typed_match_index, last_given_match_index, i, iterator_given_passage):

        for type_index in range(last_typed_match_index + 1, i):
            # spelling_errors += 1
            spelling_errors_list.append(typed_passage_words[type_index])
            print(typed_passage_words[type_index])


        print((iterator_given_passage - last_given_match_index - 1) -(i - last_typed_match_index - 1))
        if  (iterator_given_passage - last_given_match_index - 1) -(i - last_typed_match_index - 1) > 0:
            for given_index in range(last_given_match_index + 1 + (i - last_typed_match_index - 1), iterator_given_passage):
                # omission_errors += 1
                omission_errors_list.append(given_passage_words[given_index])

    for i in range(len(typed_passage_words)):
        if swap:
            swap = False
            last_typed_match_index = i
            last_given_match_index = iterator_given_passage
            continue
        if given_passage_words[min(iterator_given_passage, len(given_passage_words) - 1)] == typed_passage_words[i]:
            matched_word_list.append(typed_passage_words[i])
            spelling_omission_errors(last_typed_match_index, last_given_match_index, i, iterator_given_passage)

            print('last_typed_match_index', last_typed_match_index)
            print('last_given_match_index', last_given_match_index)
            last_typed_match_index = i
            last_given_match_index = iterator_given_passage
            print('last_typed_match_index', last_typed_match_index)
            print('last_given_match_index', last_given_match_index)
            iterator_given_passage += 1
        else:
            omit_words_in_word_list = []
            omit_words_in_word = 0
            for j in range(iterator_given_passage, len(given_passage_words)):
                print('i', i, 'j', j)
                
                if (given_passage_words[j] == typed_passage_words[i]):
                    matched_word_list.append(typed_passage_words[i])
                    
                    spelling_errors_original_list.append(given_passage_words[j])
                    missing_words_list.append(given_passage_words[original_word_index])
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    last_typed_match_index = i
                    last_given_match_index = j
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    iterator_given_passage += 1
                    break
                elif re.sub(r'[^\w\s]', '', given_passage_words[j]) == re.sub(r'[^\w\s]', '', typed_passage_words[i]):
                    # punctuation_errors += 1
                    punctuation_errors_list.append(given_passage_words[j])
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    last_typed_match_index = i
                    last_given_match_index = j
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    iterator_given_passage += 1
                    break
                elif given_passage_words[j].lower() == typed_passage_words[i].lower():
                    # capital_errors += 1
                    capital_errors_list.append(given_passage_words[j])
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    last_typed_match_index = i
                    last_given_match_index = j
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    iterator_given_passage += 1
                    break
                elif given_passage_words[j].strip() == typed_passage_words[i].strip():
                    # space_errors += 1
                    space_errors_list.append(given_passage_words[j])
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    last_typed_match_index = i
                    last_given_match_index = j
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    iterator_given_passage += 1
                    break
                elif (i < len(typed_passage_words) - 1 and j < len(given_passage_words) - 1) and (given_passage_words[j+1] == typed_passage_words[i] and given_passage_words[j] == typed_passage_words[i + 1]):
                    # transposition_errors += 0.5
                    transposition_errors_list.append(typed_passage_words[i])
                    transposition_errors_list.append(typed_passage_words[i + 1])
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    last_typed_match_index = i
                    last_given_match_index = j
                    print('last_typed_match_index', last_typed_match_index)
                    print('last_given_match_index', last_given_match_index)
                    iterator_given_passage += 1
                    swap = True
                    break
                elif j == len(given_passage_words) - 1:
                    # spelling_errors += 1
                    # spelling_errors_list.append(typed_passage_words[i])
                    # spelling_errors_original_list.append(given_passage_words[i])
                    iterator_given_passage -= omit_words_in_word
                    # iterator_given_passage += 1
                    omit_words_in_word = 0
                    # omit_words_in_word_list.clear()
                    break
                else:
                    omit_words_in_word += 1
                    # omit_words_in_word_list.append(given_passage_words[j])
                    iterator_given_passage += 1

            # omission_errors += omit_words_in_word
            # omission_errors_list.append(omit_words_in_word_list)

   
    print('given_passage_words', given_passage_words)
    print('typed_passage_words', typed_passage_words)
    print('matched_word_list', matched_word_list)
    print('capital_errors_list', capital_errors_list)
    print('spelling_errors_list', spelling_errors_list)
    
    print('space_errors_list', space_errors_list)
    print('punctuation_errors_list', punctuation_errors_list)
    print('omission_errors_list', omission_errors_list)
    print('transposition_errors_list', transposition_errors_list)

    data = {
        "capital_errors": capital_errors_list,
        "spelling_errors": spelling_errors_list,
        "space_errors": space_errors_list,
        "punctuation_errors": punctuation_errors_list,
        "transposition_errors": transposition_errors_list,
        "omission_errors": omission_errors_list,
        "matched_word_list": matched_word_list,
        "given_passage_words": given_passage_words,
        "typed_passage_words": typed_passage_words,
        "passage_id": passage_id,
        
    }

    # typing speed count
    typed_passage_length = len(typed_passage_words)
    print('typed_passage_length', typed_passage_length)
    gross_typing_speed = (typed_passage_length) / ((total_time - time_remaining)/60)
    data["gross_typing_speed"] = round(gross_typing_speed, 2)
    total_errors = len(capital_errors_list)/2 + len(spelling_errors_list) + len(space_errors_list)/2 + len(punctuation_errors_list)/2 + len(transposition_errors_list)/4 + len(omission_errors_list)
    error_percentage = (total_errors / typed_passage_length) * 100
    data["error_percentage"] = round(error_percentage, 2)
    net_typing_speed = (typed_passage_length - total_errors) / ((total_time - time_remaining)/60)
    data["net_typing_speed"] = round(net_typing_speed, 2)
    return render(request, "typing_result.html", data)

# given_passage = "The quick brown fox jumps aaa, bbb, ccc, dddd over the lazy dog. "
# typed_passage = "extra are Quick brodwn fox  over, the dog. lazy "

# print(calculate_typing_result(given_passage, typed_passage))


def typing_test(request, passage_id):
    passage = get_object_or_404(TypingPassage, id=passage_id)
    # if request.method == "POST":
    #     typed_text = request.POST.get("typed_text")
    #     result = calculate_typing_result(request, passage.passage_text, typed_text)
        # return JsonResponse(result)

    return render(request, "typing_test.html", {"passage": passage, "duration": 10 * 60})  # 10 minutes in seconds

def typing_home(request):
    passages = TypingPassage.objects.all()
    return render(request, 'typing_home.html', {'passages': passages})