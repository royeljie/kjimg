"""kjimg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views as imgs_views

app_name = 'imgs'

urlpatterns = [
    # url('account/list', imgs_views.listAccount, name='listAccount'),
    url('cert-img/thumb', imgs_views.viewThumb, name='viewThumb'),
    url('cert-img/view', imgs_views.viewImg, name='viewImg'),
    url('cert-img/upload', imgs_views.uploadImg, name='uploadImg'),
    url('cert-img/del', imgs_views.delCertificateImg, name="delCertificateImg"),
    url('cert-img/list', imgs_views.listCertificateImg, name='listCertificateImg'),
    url('cert-img/test', imgs_views.adminCertImg, name='adminCertImg'),
    url('cert-img', imgs_views.adminCertificateImg, name='adminCertificateImg'),
    url('certificate/countRejected', imgs_views.countRejectedCertificate, name='countRejectedCertificate'),
    url('certificate/reject', imgs_views.rejectCertificate, name='rejectCertificate'),
    url('certificate/submit', imgs_views.submitCertificate, name='submitCertificate'),
    url('certificate/del', imgs_views.delCertificate, name='delCertificate'),
    url('certificate/update', imgs_views.updateCertificate, name='updateCertificate'),
    url('certificate/save', imgs_views.saveCertificate, name='saveCertificate'),
    url('certificate/page', imgs_views.pageCertificate, name='pageCertificate'),
    url('certificate/mytodo', imgs_views.myTodoCertificate, name='myTodoCertificate'),
    url('certificate/mysubmitted', imgs_views.mySubmittedCertificate, name='mySubmittedCertificate'),
    url('certificate', imgs_views.adminCertificate, name='adminCertificate'),
    url('sys/param/update', imgs_views.updateParam, name='updateParam'),
    url('sys/param/page', imgs_views.pageParam, name='pageParam'),
    url('sys/param', imgs_views.adminParam, name='adminParam'),
    # url('sys/account/import', imgs_views.importAccount, name='importAccount'),
    # url('sys/account/save', imgs_views.saveAccount, name='saveAccount'),
    # url('sys/account/update', imgs_views.updateAccount, name='updateAccount'),
    # url('sys/account/del', imgs_views.delAccount, name='delAccount'),
    # url('sys/account/page', imgs_views.pageAccount, name='pageAccount'),
    # url('sys/account', imgs_views.adminAccount, name='adminAccount'),
    url('sys/org/del', imgs_views.delOrg, name='delOrg'),
    url('sys/org/update', imgs_views.updateOrg, name='updateOrg'),
    url('sys/org/save', imgs_views.saveOrg, name='saveOrg'),
    url('sys/org/page', imgs_views.pageOrg, name='pageOrg'),
    url('sys/org', imgs_views.adminOrg, name='adminOrg'),
    url('sys/user/reset', imgs_views.resetUser, name='resetUser'),
    url('sys/user/save', imgs_views.saveUser, name='saveUser'),
    url('sys/user/update', imgs_views.updateUser, name='updateUser'),
    url('sys/user/del', imgs_views.delUser, name='delUser'),
    url('sys/user/page', imgs_views.pageUser, name='pageUser'),
    url('sys/user', imgs_views.adminUser, name='adminUser'),
    url('org/listSub', imgs_views.listSubOrg, name='listSubOrg'),
    url('org/listSubAndSelf', imgs_views.listSubAndSelfOrg, name='listSubAndSelfOrg'),
    url('role/list', imgs_views.listRoles, name='listRoles'),
    url('menu/all', imgs_views.listMenus, name='listMenus'),
    url('admin', admin.site.urls),
    url('login', auth_views.login, {"template_name": "login.html"}, name='login'),
    url('logout', auth_views.logout_then_login, name='logout'),
    url('changePwd', imgs_views.changePwd, name='changePwd'),
    url('', imgs_views.main, name='main'),
]
