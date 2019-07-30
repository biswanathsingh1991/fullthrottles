from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import pandas as pd
import os
import re
from rest_framework import status
from rest_framework import serializers

# Create your views here.


# class WordSerializer(serializers.Serializer):
# 	word = serializers.CharField(max_length=500)
# 	count = serializers.Inter

class SearchWord(GenericAPIView):

    def check_start(self, word, strng):
        try:
            if re.search(r"^(%s)" % word, strng, re.IGNORECASE):
                return 0
            else:
                return 1
        except Exception as e:
            print(e)
            return 1

    def check_whole(self, word, strng):
        try:
            if re.search(r"(%s)" % word, strng, re.IGNORECASE):
                return 0
            else:
                return 1
        except Exception as e:
            print(e)
            return 1

    def create_new_df(self, word, col):
        return pd.Series({"word_len": len(str(col['word'])),
                          "word_start": self.check_start(word, col['word']),
                          "check_word": self.check_whole(word, col['word'])
                          })

    def create_json(self, word):
        print(os.getcwd())
        main = pd.read_table('api/word_search.tsv', names=["word", "count"])
        new_df = main.apply(lambda col: self.create_new_df(
            word, col), axis=1, result_type='expand')
        result = pd.concat([main, new_df], axis=1, sort=False)
        result.sort_values(by=['word_start', 'word_len', "count", "check_word"], ascending=[
                           True, True, False, True], inplace=True)
        final_result = result.loc[result['check_word'] == 0]
        return final_result if len(final_result) < 26 else final_result.iloc[:25]

    def get(self, request, *args, **kwargs):
        word = request.GET.get("search")
        # res = self.create_json(word)
        respon = []
        for index, row in self.create_json(word).iterrows():
            respon.append({"word": row["word"], "count": row["count"]})
        return Response(data=respon, status=status.HTTP_200_OK)
