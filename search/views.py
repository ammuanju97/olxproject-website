from django.shortcuts import render

class MySearchView(SearchView):
    template_name = 'search_result.html'