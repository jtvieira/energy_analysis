from django.shortcuts import render
from .utils.analysis import number_one, number_two, number_three, number_four, number_five, number_six, number_seven
# Create your views here.
def index(request):
    one = number_one()
    two = number_two()
    fig3 = number_three()
    fig4 = number_four()
    fig5 = number_five()
    fig6 = number_six()
    fig7 = number_seven()
    return render(request, "index.html", context={'one': one,
                                                  'two': two,
                                                  'fig3': fig3,
                                                  'fig4': fig4,
                                                  'fig5': fig5,
                                                  'fig6': fig6,
                                                  'fig7': fig7})
