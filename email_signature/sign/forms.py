from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Signature, Company, Banner
from django.core.exceptions import ValidationError
import re

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    
class SignatureForm(forms.ModelForm):
    SIGNATURE_TYPE_CHOICES = [
        ('minimal', 'Minimal'),
        ('detailed', 'Detailed'),
        ('detailed_with_banner', 'Detailed with Banner'),
    ]

    signature_type = forms.ChoiceField(
        choices=SIGNATURE_TYPE_CHOICES,
        label='Signature Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    banner = forms.ModelChoiceField(
        queryset=Banner.objects.all(),
        required=False,
        label='Select Banner',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Signature
        fields = [
            'name', 
            'surname', 
            'function', 
            'company', 
            'country_code', 
            'mobile', 
            'phone', 
            'email', 
            'website',
            'signature_type',
            'banner',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your surname'}),
            'function': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your function'}),
            'country_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your country code'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter your website'}),
        }

    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        empty_label='Select Company',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_to_keep = self.fields.keys()

        
        if self.instance:
            if self.instance.signature_type == 'minimal':
                fields_to_keep = ['name', 'surname', 'function', 'country_code', 'mobile']
            elif self.instance.signature_type == 'detailed':
                fields_to_keep = ['name', 'surname', 'function', 'company', 'country_code', 'mobile', 'phone', 'email', 'website']
            elif self.instance.signature_type == 'detailed_with_banner':
                fields_to_keep = self.fields.keys()

        
        for field_name in list(self.fields.keys()):
            if field_name not in fields_to_keep:
                self.fields.pop(field_name)

    def get_max_length_for_country_code(self, country_code):
        if country_code is None:
            return 0  # Return 0 if country_code is None

        country_code_length_map = {
        '93': 9,  # Afghanistan
        '355': 8, # Albania
        '213': 9, # Algeria
        '376': 6, # Andorra
        '244': 9, # Angola
        '1-268': 7, # Antigua and Barbuda
        '54': 10,  # Argentina
        '374': 8,  # Armenia
        '61': 9,   # Australia
        '43': 10,  # Austria
        '994': 9,  # Azerbaijan
        '1-242': 7,# Bahamas
        '973': 8,  # Bahrain
        '880': 10, # Bangladesh
        '1-246': 7,# Barbados
        '375': 9,  # Belarus
        '32': 9,   # Belgium
        '501': 7,  # Belize
        '229': 8,  # Benin
        '975': 8,  # Bhutan
        '591': 8,  # Bolivia
        '387': 8,  # Bosnia and Herzegovina
        '267': 7,  # Botswana
        '55': 11,  # Brazil
        '673': 7,  # Brunei
        '359': 9,  # Bulgaria
        '226': 8,  # Burkina Faso
        '257': 6,  # Burundi
        '238': 7,  # Cabo Verde
        '855': 8,  # Cambodia
        '237': 9,  # Cameroon
        '1': 10,   # Canada
        '236': 7,  # Central African Republic
        '235': 8,  # Chad
        '56': 9,   # Chile
        '86': 11,  # China
        '57': 10,  # Colombia
        '269': 7,  # Comoros
        '242': 9,  # Congo, Republic of the
        '243': 9,  # Congo, Democratic Republic of the
        '506': 8,  # Costa Rica
        '385': 9,  # Croatia
        '53': 8,   # Cuba
        '357': 8,  # Cyprus
        '420': 9,  # Czech Republic
        '45': 8,   # Denmark
        '253': 6,  # Djibouti
        '1-767': 7,# Dominica
        '1-809': 7,# Dominican Republic
        '593': 9,  # Ecuador
        '20': 9,   # Egypt
        '503': 8,  # El Salvador
        '240': 9,  # Equatorial Guinea
        '291': 8,  # Eritrea
        '372': 7,  # Estonia
        '268': 7,  # Eswatini
        '251': 10, # Ethiopia
        '679': 7,  # Fiji
        '358': 10, # Finland
        '33': 10,  # France
        '241': 7,  # Gabon
        '220': 7,  # Gambia
        '995': 9,  # Georgia
        '49': 11,  # Germany
        '233': 9,  # Ghana
        '30': 10,  # Greece
        '1-473': 7,# Grenada
        '502': 8,  # Guatemala
        '224': 9,  # Guinea
        '245': 7,  # Guinea-Bissau
        '592': 7,  # Guyana
        '509': 8,  # Haiti
        '504': 8,  # Honduras
        '36': 9,   # Hungary
        '354': 7,  # Iceland
        '91': 10,  # India
        '62': 10,  # Indonesia
        '98': 10,  # Iran
        '964': 9,  # Iraq
        '353': 9,  # Ireland
        '972': 9,  # Israel
        '39': 10,  # Italy
        '1-876': 7,# Jamaica
        '81': 11,  # Japan
        '962': 9,  # Jordan
        '7': 10,   # Kazakhstan
        '254': 10, # Kenya
        '686': 7,  # Kiribati
        '850': 9,  # Korea, North
        '82': 10,  # Korea, South
        '965': 8,  # Kuwait
        '996': 9,  # Kyrgyzstan
        '856': 8,  # Laos
        '371': 8,  # Latvia
        '961': 8,  # Lebanon
        '266': 8,  # Lesotho
        '231': 8,  # Liberia
        '218': 9,  # Libya
        '423': 7,  # Liechtenstein
        '370': 9,  # Lithuania
        '352': 8,  # Luxembourg
        '261': 9,  # Madagascar
        '265': 8,  # Malawi
        '60': 10,  # Malaysia
        '960': 7,  # Maldives
        '223': 8,  # Mali
        '356': 8,  # Malta
        '692': 7,  # Marshall Islands
        '222': 8,  # Mauritania
        '230': 8,  # Mauritius
        '52': 10,  # Mexico
        '691': 7,  # Micronesia
        '373': 8,  # Moldova
        '377': 8,  # Monaco
        '976': 8,  # Mongolia
        '382': 8,  # Montenegro
        '212': 9,  # Morocco
        '258': 9,  # Mozambique
        '95': 9,   # Myanmar
        '264': 9,  # Namibia
        '674': 7,  # Nauru
        '977': 10, # Nepal
        '31': 9,   # Netherlands
        '64': 8,   # New Zealand
        '505': 8,  # Nicaragua
        '227': 8,  # Niger
        '234': 10, # Nigeria
        '389': 8,  # North Macedonia
        '47': 8,   # Norway
        '968': 8,  # Oman
        '92': 10,  # Pakistan
        '680': 7,  # Palau
        '970': 9,  # Palestine
        '507': 8,  # Panama
        '675': 7,  # Papua New Guinea
        '595': 10, # Paraguay
        '51': 9,   # Peru
        '63': 10,  # Philippines
        '48': 9,   # Poland
        '351': 9,  # Portugal
        '974': 8,  # Qatar
        '40': 10,  # Romania
        '7': 10,   # Russia
        '250': 9,  # Rwanda
        '1-869': 7,# Saint Kitts and Nevis
        '1-758': 7,# Saint Lucia
        '1-784': 7,# Saint Vincent and the Grenadines
        '685': 7,  # Samoa
        '378': 8,  # San Marino
        '239': 7,  # Sao Tome and Principe
        '966': 9,  # Saudi Arabia
        '221': 9,  # Senegal
        '381': 9,  # Serbia
        '248': 7,  # Seychelles
        '232': 8,  # Sierra Leone
        '65': 8,   # Singapore
        '421': 9,  # Slovakia
        '386': 8,  # Slovenia
        '677': 7,  # Solomon Islands
        '252': 8,  # Somalia
        '27': 10,  # South Africa
        '211': 8,  # South Sudan
        '34': 9,   # Spain
        '94': 10,  # Sri Lanka
        '249': 9,  # Sudan
        '597': 8,  # Suriname
        '46': 8,   # Sweden
        '41': 9,   # Switzerland
        '963': 9,  # Syria
        '886': 9,  # Taiwan
        '992': 9,  # Tajikistan
        '255': 10, # Tanzania
        '66': 9,   # Thailand
        '228': 8,  # Togo
        '676': 7,  # Tonga
        '1-868': 7,# Trinidad and Tobago
        '216': 8,  # Tunisia
        '90': 10,  # Turkey
        '993': 9,  # Turkmenistan
        '688': 7,  # Tuvalu
        '256': 9,  # Uganda
        '380': 9,  # Ukraine
        '971': 9,  # United Arab Emirates
        '44': 10,  # United Kingdom
        '1': 10,   # United States
        '598': 8,  # Uruguay
        '998': 9,  # Uzbekistan
        '678': 7,  # Vanuatu
        '39': 10,  # Vatican City
        '58': 10,  # Venezuela
        '84': 9,   # Vietnam
        '967': 9,  # Yemen
        '260': 9,  # Zambia
        '263': 9,  # Zimbabwe
    }
        return country_code_length_map.get(country_code.lstrip('+'), 0)
    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        mobile = cleaned_data.get('mobile')
        phone = cleaned_data.get('phone')

        max_length = self.get_max_length_for_country_code(country_code)

        if country_code is None or country_code == '':
            self.add_error('country_code', 'Please select a country code.')

        if mobile:
            mobile_cleaned = mobile.replace('-', '')
            if not re.match(r'^[\d-]+$', mobile):  # Check for numeric only
                self.add_error('mobile', 'Mobile number must contain only digits.')
            
            elif len(mobile_cleaned) != max_length:
                self.add_error('mobile', f'Mobile number must be exactly {max_length} digits for country code {country_code}.')

        if phone:
            phone_cleaned = phone.replace('-', '')
            if not re.match(r'^[\d-]+$', phone):  # Check for numeric only
                self.add_error('phone', 'Phone number must contain only digits.')
                
            if len(phone_cleaned) != max_length:
                self.add_error('phone', f'Phone number must be exactly {max_length} digits for country code {country_code}.')

        return cleaned_data



class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image']