# typing/views.py
from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
from .models import TypingPassage
# from datetime import timedelta
from typing_tests.models import TypingPassage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TypingPassageSerializer
import re
# from tele_bot import send_result
import difflib
# import re
def clean_word(word):
    """Remove punctuation and lowercase for easier comparison."""
    return re.sub(r'[^\w]', '', word).lower()
# def split_passage(passage):
#     return re.findall(r'\S+\s*', passage)

@api_view(['POST'])
def typing_result(request, passage_id):
    passage = get_object_or_404(TypingPassage, id=passage_id)

    given_passage = passage.passage_text
    typed_passage = request.data.get("typed_text", "")
    total_time = float(request.data.get("total_time", 0))
    
    # Tokenize passages
    given_passage_words = re.findall(r'\w+|[^\w\s]', given_passage)
    typed_passage_words = re.findall(r'\w+|[^\w\s]', typed_passage)
    
    # Determine up to where the user attempted
    attempt_boundary = len(typed_passage_words)
    
    # Initialize error tracking
    matched_word_list = []
    punctuation_errors_list = []
    space_errors_list = []
    extra_typed_errors_list = []
    capital_errors_list = []
    omission_errors_list = []
    spelling_errors_list = []
    display_list = []
    
    matcher = difflib.SequenceMatcher(None, given_passage_words, typed_passage_words)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for idx in range(i1, i2):
                matched_word_list.append(given_passage_words[idx])
                display_list.append(f"{given_passage_words[idx]}")
        
        elif tag == 'delete':
            for idx in range(i1, i2):
                if idx < attempt_boundary:
                    omission_errors_list.append(given_passage_words[idx])
                    display_list.append(f"[{given_passage_words[idx]}]")
                else:
                    # display_list.append(f"{given_passage_words[idx]}")
                    pass

        elif tag == 'insert':
            for idx in range(j1, j2):
                extra_typed_errors_list.append(typed_passage_words[idx])
                display_list.append(f"[+{typed_passage_words[idx]}]")
        
        elif tag == 'replace':
            for ori_idx, typ_idx in zip(range(i1, i2), range(j1, j2)):
                if ori_idx < len(given_passage_words) and typ_idx < len(typed_passage_words):
                    ori = given_passage_words[ori_idx]
                    typ = typed_passage_words[typ_idx]

                    if clean_word(ori) == clean_word(typ):
                        if ori.lower() == typ.lower() and ori != typ:
                            capital_errors_list.append(ori)
                            display_list.append(f"{ori} [{typ}]")
                        else:
                            punctuation_errors_list.append(ori)
                            display_list.append(f"{ori} [{typ}]")
                    else:
                        spelling_errors_list.append(typ)
                        display_list.append(f"{ori} [{typ}]")
            
            if i2 - i1 > j2 - j1:
                for idx in range(i1 + (j2 - j1), i2):
                    if idx < attempt_boundary:
                        omission_errors_list.append(given_passage_words[idx])
                        display_list.append(f"[{given_passage_words[idx]}]")
                    else:
                        # display_list.append(f"{given_passage_words[idx]}")
                        pass
            elif j2 - j1 > i2 - i1:
                for idx in range(j1 + (i2 - i1), j2):
                    space_errors_list.append(typed_passage_words[idx])
                    display_list.append(f"[+{typed_passage_words[idx]}]")

    # Typing speed calculations
    typed_passage_keystrokes = sum(len(word) for word in typed_passage_words)
    gross_typing_speed = (typed_passage_keystrokes/5) / (total_time/60) if total_time > 0 else 0

    error_keystrokes = (
        sum(len(word) for word in capital_errors_list) * 0.5 +
        sum(len(word) for word in spelling_errors_list) +
        sum(len(word) for word in extra_typed_errors_list) +
        sum(len(word) for word in space_errors_list) * 0.5 +
        sum(len(word) for word in punctuation_errors_list) * 0.5 +
        sum(len(word) for word in omission_errors_list)
    )

    total_errors = (
        len(capital_errors_list) * 0.5 +
        len(spelling_errors_list) +
        len(extra_typed_errors_list) +
        len(space_errors_list) * 0.5 +
        len(punctuation_errors_list) * 0.5 +
        len(omission_errors_list)
    )

    error_percentage = (error_keystrokes / typed_passage_keystrokes) * 100 if typed_passage_keystrokes > 0 else 0
    net_typing_speed = ((typed_passage_keystrokes - error_keystrokes) / 5) / (total_time/60) if total_time > 0 else 0

    response_data = {
        "capital_errors": capital_errors_list,
        "spelling_errors": spelling_errors_list,
        "extra_typed_errors": extra_typed_errors_list,
        "space_errors": space_errors_list,
        "punctuation_errors": punctuation_errors_list,
        "omission_errors": omission_errors_list,
        # "matched_word_list": matched_word_list,
        # "typed_passage_words": typed_passage_words,
        # "passage_id": passage_id,
        "gross_typing_speed": round(gross_typing_speed, 2),
        "error_percentage": round(error_percentage, 2),
        "net_typing_speed": round(net_typing_speed, 2),
        "total_errors": total_errors,
        # "total_time": total_time,
        "display_list": display_list,
        "attempted_percentage": round((attempt_boundary / len(given_passage_words)) * 100, 2) if given_passage_words else 0
    }

    # You can enable telegram sending if you want
    # send_result(response_data)

    # print('response_data', response_data)
    return Response(response_data)

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