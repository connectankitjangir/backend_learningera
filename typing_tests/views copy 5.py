# typing/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import TypingPassage
from datetime import timedelta
from typing_tests.models import TypingPassage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TypingPassageSerializer
import re
from tele_bot import send_result

def split_passage(passage):
    return re.findall(r'\S+\s*', passage)

@api_view(['POST'])
def typing_result(request, passage_id):
    passage = get_object_or_404(TypingPassage, id=passage_id)

    given_passage = passage.passage_text
    typed_passage = request.data.get("typed_text")
    total_time = request.data.get("total_time", 0)
    
    given_passage_words = split_passage(given_passage)
    typed_passage_words = split_passage(typed_passage)
    
    # Initialize error tracking lists
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

    display_list = []


    def jumpconfirmation(j, i, given_passage_words, typed_passage_words):
        if (j+2 < len(given_passage_words) and i+2 < len(typed_passage_words) and
            re.sub(r'[^\w\s]', '', given_passage_words[j+1]).lower().strip() == re.sub(r'[^\w\s]', '', typed_passage_words[i+1]).lower().strip() and 
            re.sub(r'[^\w\s]', '', given_passage_words[j+2]).lower().strip() == re.sub(r'[^\w\s]', '', typed_passage_words[i+2]).lower().strip()):
            return True
        return False
        

    def spelling_omission_errors(last_typed_match_index, last_given_match_index, i, iterator_given_passage):
        calculate_index = 0
        for type_index in range(last_typed_match_index + 1, i):
            calculate_index += 1
            spelling_errors_list.append(typed_passage_words[type_index])
            display_list.append(f"{given_passage_words[last_given_match_index + calculate_index]} [{typed_passage_words[type_index]}]")

        if (iterator_given_passage - last_given_match_index - 1) - (i - last_typed_match_index - 1) > 0:
            for given_index in range(last_given_match_index + 1 + (i - last_typed_match_index - 1), iterator_given_passage):
                omission_errors_list.append(given_passage_words[given_index])
                display_list.append(f"[{given_passage_words[given_index]}]")

    # Main comparison loop
    for i in range(len(typed_passage_words)):
        if swap:
            swap = False
            last_typed_match_index = i
            last_given_match_index = iterator_given_passage
            continue
            
        if given_passage_words[min(iterator_given_passage, len(given_passage_words) - 1)] == typed_passage_words[i]:
            matched_word_list.append(typed_passage_words[i])
            spelling_omission_errors(last_typed_match_index, last_given_match_index, i, iterator_given_passage)
            display_list.append(f"{typed_passage_words[i]}")
            last_typed_match_index = i
            last_given_match_index = iterator_given_passage
            iterator_given_passage += 1
        else:
            omit_words_in_word = 0
            for j in range(iterator_given_passage, len(given_passage_words)):
                if (given_passage_words[j] == typed_passage_words[i]):
                    if omit_words_in_word > 0:
                        if jumpconfirmation(j, i, given_passage_words, typed_passage_words)
                            matched_word_list.append(typed_passage_words[i])
                            spelling_errors_original_list.append(given_passage_words[j])
                            missing_words_list.append(given_passage_words[original_word_index])
                            spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                            display_list.append(f"{given_passage_words[j]}")
                            last_typed_match_index = i
                            last_given_match_index = j
                            iterator_given_passage += 1
                            break
                        iterator_given_passage -= omit_words_in_word
                        omit_words_in_word = 0
                        break    

                    matched_word_list.append(typed_passage_words[i])
                    spelling_errors_original_list.append(given_passage_words[j])
                    missing_words_list.append(given_passage_words[original_word_index])
                    display_list.append(f"{given_passage_words[j]} [{typed_passage_words[i]}]")
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    last_typed_match_index = i
                    last_given_match_index = j
                    iterator_given_passage += 1
                    break
                elif re.sub(r'[^\w\s]', '', given_passage_words[j]) == re.sub(r'[^\w\s]', '', typed_passage_words[i]):
                    punctuation_errors_list.append(given_passage_words[j])
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    display_list.append(f"{given_passage_words[j]} [{typed_passage_words[i]}]")
                    last_typed_match_index = i
                    last_given_match_index = j
                    iterator_given_passage += 1
                    break
                elif given_passage_words[j].lower() == typed_passage_words[i].lower():
                    capital_errors_list.append(given_passage_words[j])
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    display_list.append(f"{given_passage_words[j]} [{typed_passage_words[i]}]")
                    last_typed_match_index = i
                    last_given_match_index = j
                    iterator_given_passage += 1
                    break
                elif given_passage_words[j].strip() == typed_passage_words[i].strip():
                    space_errors_list.append(given_passage_words[j])
                    display_list.append(f"{given_passage_words[j]} [{typed_passage_words[i]}]")
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    last_typed_match_index = i
                    last_given_match_index = j
                    iterator_given_passage += 1
                    break
                elif (i < len(typed_passage_words) - 1 and j < len(given_passage_words) - 1) and (given_passage_words[j+1] == typed_passage_words[i] and given_passage_words[j] == typed_passage_words[i + 1]):
                    transposition_errors_list.append(typed_passage_words[i])
                    transposition_errors_list.append(typed_passage_words[i + 1])
                    display_list.append(f"{given_passage_words[j]} {given_passage_words[j+1]} [{typed_passage_words[i]} {typed_passage_words[i+1]}]")
                    spelling_omission_errors(last_typed_match_index, last_given_match_index, i, j)
                    last_typed_match_index = i
                    last_given_match_index = j
                    iterator_given_passage += 1
                    swap = True
                    break
                elif j == len(given_passage_words) - 1:
                    iterator_given_passage -= omit_words_in_word
                    omit_words_in_word = 0
                    break
                else:
                    omit_words_in_word += 1
                    iterator_given_passage += 1

    # Calculate typing metrics
    typed_passage_keystrokes = sum(len(word) for word in typed_passage_words)
    gross_typing_speed = (typed_passage_keystrokes/5) / ((total_time)/60)
    total_errors = (
        len(capital_errors_list)/2 + 
        len(spelling_errors_list) + 
        len(space_errors_list)/2 + 
        len(punctuation_errors_list)/2 + 
        len(transposition_errors_list)/4 + 
        len(omission_errors_list)
    )
    error_keystrokes = (
        sum(len(word) for word in capital_errors_list) * 0.5 +
        sum(len(word) for word in spelling_errors_list) +
        sum(len(word) for word in space_errors_list) * 0.5 +
        sum(len(word) for word in punctuation_errors_list) +
        sum(len(word) for word in transposition_errors_list) * 0.25 +
        sum(len(word) for word in omission_errors_list)
    )
    
    error_percentage = (error_keystrokes / typed_passage_keystrokes) * 100
    net_typing_speed = ((typed_passage_keystrokes - error_keystrokes)/5) /((total_time)/60)


    response_data = {
        # "given_passage_words": given_passage_words,
        "capital_errors": capital_errors_list,
        "spelling_errors": spelling_errors_list,
        "space_errors": space_errors_list,
        "punctuation_errors": punctuation_errors_list,
        "transposition_errors": transposition_errors_list,
        "omission_errors": omission_errors_list,
        "matched_word_list": matched_word_list,
        "typed_passage_words": typed_passage_words,
        "passage_id": passage_id,
        "gross_typing_speed": round(gross_typing_speed, 2),
        "error_percentage": round(error_percentage, 2),
        "net_typing_speed": round(net_typing_speed, 2),
        "total_errors": total_errors,
        'total_time': total_time,
        'display_list': display_list
    }

    # send_result(response_data)

    print('response_data', response_data)

    return Response(response_data)

# given_passage = "The quick brown fox jumps aaa, bbb, ccc, dddd over the lazy dog. "
# typed_passage = "extra are Quick brodwn fox  over, the dog. lazy "

# print(calculate_typing_result(given_passage, typed_passage))

@api_view(['GET'])
def typing_test(request, passage_id):
    passage = get_object_or_404(TypingPassage, id=passage_id)
    serializer = TypingPassageSerializer(passage)
    return Response(serializer.data)


@api_view(['GET'])
def typing_home(request):
    passages = TypingPassage.objects.all().order_by('-order_id')
    serializer = TypingPassageSerializer(passages, many=True)
    return Response(serializer.data)