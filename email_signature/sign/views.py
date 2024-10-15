from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignatureForm, SignUpForm, LoginForm
from .models import Signature, Company, Banner
from .constants import COUNTRY_PHONE_CODES

def country_select_view(request):
    country_phone_codes = []
    for country_name, phone_code in COUNTRY_PHONE_CODES.items():
        country_phone_codes.append({
            'name': country_name,
            'code': phone_code,
        })
    return render(request, 'country_select.html', {'countries': country_phone_codes})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('signature_list')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


def create_signature(request):
    if request.method == 'POST':
        form = SignatureForm(request.POST, request.FILES)
        if form.is_valid():
            signature = form.save(commit=False)
            signature.user = request.user
            signature.save()
            return redirect('signature_list')
    else:
        form = SignatureForm()
    
    companies = Company.objects.all()
    banners = Banner.objects.all()  
    banner_sets = [banners[i:i + 4] for i in range(0, len(banners), 4)]
    country_phone_codes = [{'name': name, 'code': code} for name, code in COUNTRY_PHONE_CODES.items()]
     
    return render(request, 'create_signature.html', {
        'form': form,
        'countries': country_phone_codes ,
        'companies': companies,
        'banners': banner_sets,  
    })

    
@login_required
def signature_list(request):
    signatures = Signature.objects.filter(user=request.user)
    return render(request, 'signature_list.html', {'signatures': signatures})

@login_required
def delete_signature(request, pk):
    signature = get_object_or_404(Signature, pk=pk, user=request.user)
    if request.method == 'POST':
        signature.delete()
        return redirect('signature_list')
    return render(request, 'confirm_delete.html', {'signature': signature})

# @login_required
# def download_signature(request, pk):
#     # Load your signature
#     signature = Signature.objects.get(pk=pk)

#     # Load the HTML template
#     template = loader.get_template('signature_template.html')
    
#     # Define context based on signature_type
#     if signature.signature_type == 'minimal':
#         context = {
#             'name': signature.name,
#             'surname': signature.surname,
#             'function': signature.function,
#             'mobile': signature.mobile,
#             'country_code': signature.country_code,
#         }
#     elif signature.signature_type == 'detailed':
#         context = {
#             'name': signature.name,
#             'surname': signature.surname,
#             'function': signature.function,
#             'company': signature.company,
#             'company_address': signature.company.address,
#             'country_code': signature.country_code,
#             'mobile': signature.mobile,
#             'phone': signature.phone,
#             'email': signature.email,
#             'signature_type': signature.signature_type,
#             'website': signature.website,
#         }
#     else:
#         context = {
#             'name': signature.name,
#             'surname': signature.surname,
#             'function': signature.function,
#             'company': signature.company,
#             'company_address': signature.company.address,
#             'country_code': signature.country_code,
#             'mobile': signature.mobile,
#             'phone': signature.phone,
#             'email': signature.email,
#             'signature_type': signature.signature_type,
#             'website': signature.website,
#             'banner_image': "http://localhost:8000/" + signature.banner.image.url,
#         }

#     html_content = template.render(context, request)
    
#     # Set up the Chrome driver
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')

#     service = ChromeService(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)

#     # Save the HTML content to a file
#     with open('temp_signature.html', 'w', encoding='utf-8') as f:
#         f.write(html_content)

#     # Open the HTML file in the browser
#     driver.get('file:///' + os.path.abspath('temp_signature.html'))

#     # Find the container element by class name
#     container = driver.find_element(By.CLASS_NAME, 'container')
    
#     # Scroll to the container to ensure it's in view
#     driver.execute_script("arguments[0].scrollIntoView();", container)

#     # Take a screenshot of the container only
#     screenshot = container.screenshot_as_png
#     driver.quit()

#     # Create a response with the image data
#     response = HttpResponse(screenshot, content_type='image/png')
#     response['Content-Disposition'] = 'attachment; filename="signature.png"'
    
#     # Optionally, clean up the temporary file
#     if os.path.exists('temp_signature.html'):
#         os.remove('temp_signature.html')

#     return response

# @login_required
# def upload_banner(request):
    # if request.method == 'POST':
        # form = BannerForm(request.POST, request.FILES)
        # if form.is_valid():
            # form.save()  # Save the banner image
            # return redirect('banner_list')  # Redirect to a page that lists banners or wherever you want
    # else:
        # form = BannerForm()
    
    # return render(request, 'upload_banner.html', {'form': form})

# @login_required
# def banner_list(request):
#     banners = Banner.objects.all()
#     return render(request, 'banner_list.html', {'banners': banners})

# @login_required
# def delete_banner(request, pk):
#     banner = get_object_or_404(Banner, pk=pk)
#     if request.method == 'POST':
#         banner.delete()
#         return redirect('banner_list')  # Redirect to the banner list after deletion
#     return render(request, 'confirm_delete.html', {'banner': banner})
    
