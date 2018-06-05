"""
Django settings for ttxx project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(1,os.path.join(BASE_DIR,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#加密
SECRET_KEY = '7t8g554h&&y)@r=^2t1&23ty@*plp*%qx%my(+30@x1j+2&0h1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tt_cart',
	'tt_goods',
	'tt_order',
	'tt_user',
	'tinymce', #富文本编辑器
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ttxx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
		,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ttxx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ttxx_25',
		'HOST':'localhost',
		'PORT':'3306',
		'USER':'root',
		'PASSWORD':'mysql'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
	os.path.join(BASE_DIR,'static')  #设置静态查找路径
]

AUTH_USER_MODEL ='tt_user.User' ##迁移前需要设置,表示用tt_user的User做模型认证
'''表示身法认证有两个用户类,需要设置AUTH_USER_MODEL ='tt_user.User'指定用户类
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
'''''

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com' #smtp收邮件;pop3发邮件
EMAIL_PORT = 25
#发送邮件的邮箱
EMAIL_HOST_USER = 'bjshanpu@163.com'   #主机:注册邮箱帐号
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'aaa123456'  #授权码
#收件人看到的发件人
EMAIL_FROM = '天天鲜鲜<bjshanpu@163.com>'  #提示信息:名称<发件人邮箱>

# 缓存  #存到redis中
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache", #缓存引擎
        "LOCATION": "redis://127.0.0.1:6379/5",  #缓存服务器
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",  #和数据库交互
        }
    }
}


# Session  #不配置,默认session存到mysql数据库中,现在存到rache中也是redis中
# http://django-redis-chs.readthedocs.io/zh_CN/latest/#session-backend

SESSION_ENGINE = "django.contrib.sessions.backends.cache"  #引擎用cache,不再用mysql的innodb
SESSION_CACHE_ALIAS = "default"  #指定为cache中"default"的配置

LOGIN_URL='/user/login'