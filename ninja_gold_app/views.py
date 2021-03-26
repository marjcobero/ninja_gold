from django.shortcuts import render, redirect
import random
from datetime import datetime

# Create your views here.
GOLD = {
    "farm": (5,10,15,18),
    "cave": (0,3,5,7,9),
    "house": (1,2,3,4,5),
    "casino": (0,10,20,40,50),
}

def index(request):
    if not "gold" in request.session or "activities" not in request.session:
        request.session['gold'] = 0
        request.session['activities'] = []
    return render(request, 'index.html')

def reset(request):
    request.session.clear()
    return redirect('/')

def process_gold(request):
    if request.method == 'GET':
        return redirect('/')

    building_name = request.POST['building']
    building = GOLD[building_name]
    building_name_upper = building_name[0].upper() + building_name[1:]
    
    get_gold = random.randint(building[0], building[1])
    now_formatted = datetime.now().strftime("%m/%d/%Y %I:%M%p")
    result = 'earn'
    
    message = f"Earned {get_gold} from the {building_name_upper}! ({now_formatted})"
    
    if building_name == 'casino':
        if random.randint(0,1) > 0:
            message = f"Entered a {building_name_upper} and lost {get_gold} golds... Ouch... ({now_formatted})"
            get_gold = get_gold * -1
            result = 'lose'
    request.session['gold'] += get_gold
    request.session['activities'].append({"message": message, "result": result})
    return redirect('/')