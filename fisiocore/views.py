from django.shortcuts import render


def login(request):
    context = {}
    return render(request, 'fisiocore/login.html', context)


def patients(request):
    context = {}
    return render(request, 'fisiocore/patients.html', context)
    

def patient(request):
    pass
    

def add_patient(request):
    pass
    

def edit_patient(request):
    pass
    
    
def delete_patient(request):
    pass
    
    
def add_consent(request):
    pass


def add_anamnesis(request):
    pass
