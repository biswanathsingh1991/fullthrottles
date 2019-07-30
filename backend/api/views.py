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
#   word = serializers.CharField(max_length=500)
#   count = serializers.Inter

class SearchWord(GenericAPIView):

    def check_start(self, word, strng):
        '''
        Function for check if word is starting from start retrun 0 if true and 1 if false.
        and if dataframe cell had unexpected value return 1
        '''
        try:
            if re.search(r"^(%s)" % word, strng, re.IGNORECASE):  # regx for matching at front
                return 0
            else:
                return 1
        except Exception as e:  # execption for any abnormal entry on dataframe
            print(e)
            return 1

    def check_whole(self, word, strng):
        '''
        Function for check if word contain in recorderd string 0 if true and 1 if false.
        and if dataframe cell had unexpected value return 1.
        '''
        try:
            # regx for matching at any position
            if re.search(r"(%s)" % word, strng, re.IGNORECASE):
                return 0
            else:
                return 1
        except Exception as e:  # exception for any abnormal entry on database
            print(e)
            return 1

    def create_new_df(self, word, col):
        '''
        create a new dataframe with three new column 
        word_len : column hold the length of the data sets words,
        word_start: column store o and 1 depending on if the word send on querystring matches at the start,
        check_word:columnn store o and 1 depending on if the word send on query string matches at any position,
        '''
        return pd.Series({"word_len": len(str(col['word'])),
                          "word_start": self.check_start(word, col['word']),
                          "check_word": self.check_whole(word, col['word'])
                          })

    def create_json(self, word):
        print(os.getcwd())
        main = pd.read_table('api/word_search.tsv',
                             names=["word", "count"])  # read the data set
        new_df = main.apply(lambda col: self.create_new_df(
            word, col), axis=1, result_type='expand')
        # return a new data set with three new column word_len, word_start, check_word
        result = pd.concat([main, new_df], axis=1, sort=False)
        result.sort_values(by=['word_start', 'word_len', "count", "check_word"], ascending=[
                           True, True, False, True], inplace=True)  # sort the dataframe as requirement
        # slice the sorted dataframe from top and take the row wich are releted with requested word
        final_result = result.loc[result['check_word'] == 0]
        # take the top 25 result of data frame
        return final_result if len(final_result) < 26 else final_result.iloc[:25]

    def get(self, request, *args, **kwargs):
        word = request.GET.get("search")  # grad the querystring
        # res = self.create_json(word)
        respon = []
        # itrate over the top 25 row
        for index, row in self.create_json(word).iterrows():
            # create a dict containg word and wordcount key and append it to a list
            respon.append({"word": row["word"], "count": row["count"]})
        # drf http response data is a list containing top 25 result , response status 200
        return Response(data=respon, status=status.HTTP_200_OK)
