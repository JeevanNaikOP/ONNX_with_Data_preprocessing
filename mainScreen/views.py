from django.shortcuts import render,redirect
from .forms import FraudDetectionForm
import sweetify
import os
import json
import requests
from .models import scoringDataBase

# Create your views here.
def index(request):
    form = FraudDetectionForm()
    
    return render(request,'index.html',{'form': form})

def result(request):
    sweetify.DEFAULT_OPTS = {
    'showConfirmButton': True,
    'timer': 2500,
    'allowOutsideClick': True,
    'confirmButtonText': 'OK',
}
    header = {
            'Content-Type': 'application/json',
            'Control': 'no-cache',
        }
    
    json_data = {
            'username' : os.getenv("USERNAME"),
            'password' : os.getenv("PASSWORD"),   
                      }
    response = requests.post('https://192.86.32.113:9888/auth/generateToken', json=json_data, headers=header,verify=False)

    token = json.loads(response.text)['token']

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    
    choose = request.POST.get('input')

    print(choose)
    if choose != '':
        choose = int(choose)
        i = scoringDataBase.objects.get(Id=choose)

        user = i.User
        amount = i.Amount
        usechip = i.Use_chip
        card = i.Card
        merchantName = i.Merchant_name
        errors = i.Errors
        merchntState = i.Merchant_state
        merchantCity = i.Merchant_city
        zip = i.Zip

        form = FraudDetectionForm()
        return render(request,'index.html',{'form': form, 'user_profile':user, 'amount': amount,'useChip':str(usechip), 'card': card,
                                            'merchantName':merchantName,'errors':errors,'merchantState':merchntState,
                                            'merchantCity':merchantCity, 'zip':zip})
    else:
        user = request.POST.get('input1')
        amount = request.POST.get('input2')
        usechip = request.POST.get('input3')
        card = request.POST.get('input4')
        merchantName = request.POST.get('input5')
        errors = request.POST.get('input6')
        merchntState = request.POST.get('input7')
        merchantCity = request.POST.get('input8')
        zip = request.POST.get('input9')
        form = FraudDetectionForm()
    
    payload_scoring = [{"Amount_num":amount,"Card":card,"Errors?":errors,"Merchant City":merchantCity,"Merchant Name":merchantName,"Merchant State":merchntState,"Use Chip":usechip,"User":user,"Zip":zip}]

    response_scoring = requests.post('http://192.86.32.113:6001/iml/v2/scoring/online/bbf9ef27-c1a5-4f49-ba04-239b2f041257', json=payload_scoring, headers=header,verify=False)

    json_out = (json.loads(response_scoring.text))

    payload_scoring = []
    payload_scoring.append(json_out[0]['minMaxScaler(Amount_num)'])
    payload_scoring.append(json_out[0]['minMaxScaler(Card)'])
    payload_scoring.append(json_out[0]['minMaxScaler(User)'])
    payload_scoring.append(json_out[0]['mms-ce(Errors?)'])
    payload_scoring.append(json_out[0]['mms-ce(Merchant City)'])
    payload_scoring.append(json_out[0]['mms-ce(Merchant Name)'])
    payload_scoring.append(json_out[0]['mms-ce(Merchant State)'])
    payload_scoring.append(json_out[0]['mms-ce(Use Chip)'])
    payload_scoring.append(json_out[0]['mms-ce(Zip)'])

    payload_scoring = [{"dense_16_input": payload_scoring}]

    response_scoring = requests.post('http://192.86.32.113:6001/iml/v2/scoring/online/116eed64-1544-4cee-9238-9d2bc0a76efd', json=payload_scoring, headers=header,verify=False)

    json_out = (json.loads(response_scoring.text))    

    try:
        isFraud = json_out[0]['dense_19']['data']
    
        myDatabase = scoringDataBase(User=user,Amount=amount,Use_chip=usechip,Card =card ,Merchant_name=merchantName,Errors=errors,
                            Merchant_state=merchntState,Merchant_city=merchantCity,Zip=zip,IsFraud=isFraud)
        myDatabase.save()
    
    except:
        sweetify.error(request, 'This transaction is fraud',persistent='Ok')
        return render(request,'index.html',{'form': form})

    print(json_out)
    if isFraud[0] == 1.0:
        sweetify.error(request, 'This transaction is fraud',persistent='Ok')
    else:
        sweetify.success(request, 'This transaction is not fraud',  persistent='Ok')
    # return redirect('/')
    return render(request,'index.html',{'form': form})

def showTables(request):
    myDatabase = scoringDataBase.objects.all()
    context = {
        "myDatabase": myDatabase
    }
    return render(request, 'mydatabase.html', context)
