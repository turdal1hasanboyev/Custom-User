from django.db import models
import re ### telefon raqami validatsiyasi uchun
from django.contrib.auth.models import AbstractUser, UserManager ### manager va abstract modellar


### Custom User Manager
class CustomUserManager(UserManager):
        def create_user(self, email, phone_number, password, **extra_fields): ### oddiy userda keladigan fieldlar ### hohlagan fieldni None qilub olib kelish va is None bilan tekshirib hato chiqarish mumkin
            if not email:
                raise ValueError("Email kiritilishi shart!")
            if not phone_number:
                raise ValueError("Telefon raqami kiritilishi shart!")
            if not re.match(r'^\+?[0-9]{10,15}$', phone_number): ### tel raqam validatsiyasi
                raise ValueError("Telefon raqami noto'g'ri formatda! Masalan: +998901234567")
            if not password:
                raise ValueError("Parol kiritilishi shart!")
            
            # bu yerda barcha kerakli fieldlar tekshirib olindi
            ### hohlagan fieldga None qiymatida kelishiga ruhsat berib lekin uni is None qilib tekshirib olish mumkin
            ### majburiy bolsa if not bilan None bolsa is None bilan tekshiriladi
            
            email = self.normalize_email(email) #### email validatsiya va optimizatsiya qilib tekshirib olindi
            user = self.model(email=email, phone_number=phone_number, **extra_fields) ## user yaratildi
            user.set_password(password) ### password heshlandi
            user.save(using=self._db) ### bazaga saqlandi user
            return user ### qaytarildi
        
        def create_superuser(self, email, phone_number, password, **extra_fields): ### super userda keladigan fieldlar hohlagan fildni None qilib olib kelish mumkin yani shunday kelishiga ruxsat berish mumkin lekin uni if <field_name> is None: qilib tekshirish kerak boladi
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)

            ### is_active va is_superuser fieldlari True holatga keltirilmoqda
            # bu usul biroz kop kod yozish talab qiladi va uni ustiga bularni huddi pastdagi kabi tekshirib olish kerak
            '''
            shunday qilib
            if extra_fields.get('is_staff') is not True:
                raise ValueError("Superuser uchun is_staff=True bo'lishi shart!")
            if extra_fields.get('is_superuser') is not True:
                raise ValueError("Superuser uchun is_superuser=True bo'lishi shart!")
            '''

            '''
            if 'is_staff' not in extra_fields:
                extra_fields['is_staff'] = True
            if 'is_superuser' not in extra_fields:
                extra_fields['is_superuser'] = True
            
            bunday tekshirib va biratola yozib ketish ham mumkin
            '''

            ### lekin boshqa tezroq kam kod yozish usullari ham bor
            ### update orqali bir qator kod orqali yozsa ham boladi

            '''
            extra_fields.update({'is_staff': True, 'is_superuser': True})
            '''
            ### bunday usulda yozishda tekshirib olish yoki tekshirmaslik ixtiyoriy tekshirib olgan va xato chiqargan maqul(agar biron bir xato bolsa)

            if extra_fields.get('is_staff') is not True:
                raise ValueError("Superuser uchun is_staff=True bo'lishi shart!")
            if extra_fields.get('is_superuser') is not True:
                raise ValueError("Superuser uchun is_superuser=True bo'lishi shart!")
            if not email:
                raise ValueError("Superuser uchun email kiritilishi shart!")
            if not phone_number:
                raise ValueError("Superuser uchun telefon raqami kiritilishi shart!")
            if not re.match(r'^\+?[0-9]{10,15}$', phone_number): ### phone_number validatsiyasi
                raise ValueError("Telefon raqami noto'g'ri formatda! Masalan: +998901234567")
            if not password:
                raise ValueError("Superuser uchun parol kiritilishi shart!")
            
            ### value error yoki type error bilan tekshirish 
            ### if not yoki is None bilan vaziyatga qarab tekshirish
            
            ### barcha fieldlar tekshirib olindi

            ### har doim ham barcha fieldlarni tekshiraverish ham kerak emas bu kop kod yozishni talab qiladi va vaqtni oladi
            
            user = self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)
            return user
        
            '''
            user = create_user(...)
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)
            return user
            '''

            ### bunday usulda ham yozsa boladi bunda oldin oddiy user yaratib olinadi va uning is_staff va is_superuser fieldlari update qilinadi yani True qilib keyin user bazaga saqlanadi
            ### bu usul birmuncha qulayroq hech qanday muammoni keltirib chiqarmaydi ancha yaxshi usullardan biri qaytib tekshirish ham umuman kerak emas


class CustomUser(AbstractUser):
    GENDER = (
        ('Male', ('Male')),
        ('Female', ('Female')),
    )
    username = None ### username ni inkor(faolsizlantirish ya'ni kerak bo'lmasa) etish istalgan fieldni shu yo'l bilan faolsizlantirsa boladi
    email = models.EmailField(unique=True, db_index=True, max_length=225, null=True, blank=True) #### agar email kerak bolsa ayniqsa superuser yaratishda shu tartibda update qilish kerak eng asosiysi unique=True qilsih kerak 
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="Images/", null=True, blank=True, default='img/default.png')
    video = models.FileField(upload_to="Videos/", null=True, blank=True)
    phone_number = models.CharField(max_length=225, null=True, blank=True, unique=True)
    adress = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=225, choices=GENDER, null=True, blank=True)

    ### oddiy fieldlar

    objects = CustomUserManager() #### menegerdan obyekt olish har bir field unga ham otishi uchun

    USERNAME_FIELD = 'email' ### asosiy field default holatda username boladi bu orqali adminka boshqariladi desa ham boladi qaysi asosiy fild bolishini
    REQUIRED_FIELDS = ['phone_number'] ### toldirilishi kerak bolgan field majburiy boladi adminkada bu yerda yozilgan field soraladi desa ham boladi bu yerda yozilgan fieldni create_user va create_superuser da None qilish mumkin emas 

    '''
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    default holatdagi fieldlar

    default holatda bu ham UserManagerdan obyekt oladi
    '''

    def __str__(self):
        if self.get_full_name():
            return f"{self.id}-{self.get_full_name()}"
        if self.email:
            return f"{self.id}-{self.email}"
        return f"{self.id}-{self.phone_number}"
    ### str qaytarish usuli django strukturasi bo'yicha