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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from imgs import views as imgs_views

urlpatterns = [
    url('admin/', admin.site.urls),
    url('kjimg/', include('imgs.urls', namespace='imgs')),
    # url('kjimg/account/list', imgs_views.listAccount, name='listAccount'),
    # url('kjimg/cert-img/thumb', imgs_views.viewThumb, name='viewThumb'),
    # url('kjimg/cert-img/view', imgs_views.viewImg, name='viewImg'),
    # url('kjimg/cert-img/upload', imgs_views.uploadImg, name='uploadImg'),
    # url('kjimg/cert-img/del', imgs_views.delCertificateImg, name="delCertificateImg"),
    # url('kjimg/cert-img/list', imgs_views.listCertificateImg, name='listCertificateImg'),
    # url('kjimg/cert-img', imgs_views.adminCertificateImg, name='adminCertificateImg'),
    # url('kjimg/certificate/reject', imgs_views.rejectCertificate, name='rejectCertificate'),
    # url('kjimg/certificate/submit', imgs_views.submitCertificate, name='submitCertificate'),
    # url('kjimg/certificate/del', imgs_views.delCertificate, name='delCertificate'),
    # url('kjimg/certificate/update', imgs_views.updateCertificate, name='updateCertificate'),
    # url('kjimg/certificate/save', imgs_views.saveCertificate, name='saveCertificate'),
    # url('kjimg/certificate/page', imgs_views.pageCertificate, name='pageCertificate'),
    # url('kjimg/certificate/mytodo', imgs_views.myTodoCertificate, name='myTodoCertificate'),
    # url('kjimg/certificate/mysubmitted', imgs_views.mySubmittedCertificate, name='mySubmittedCertificate'),
    # url('kjimg/certificate', imgs_views.adminCertificate, name='adminCertificate'),
    # url('kjimg/sys/account/import', imgs_views.importAccount, name='importAccount'),
    # url('kjimg/sys/account/save', imgs_views.saveAccount, name='saveAccount'),
    # url('kjimg/sys/account/update', imgs_views.updateAccount, name='updateAccount'),
    # url('kjimg/sys/account/del', imgs_views.delAccount, name='delAccount'),
    # url('kjimg/sys/account/page', imgs_views.pageAccount, name='pageAccount'),
    # url('kjimg/sys/account', imgs_views.adminAccount, name='adminAccount'),
    # url('kjimg/sys/org/del', imgs_views.delOrg, name='delOrg'),
    # url('kjimg/sys/org/update', imgs_views.updateOrg, name='updateOrg'),
    # url('kjimg/sys/org/save', imgs_views.saveOrg, name='saveOrg'),
    # url('kjimg/sys/org/page', imgs_views.pageOrg, name='pageOrg'),
    # url('kjimg/sys/org', imgs_views.adminOrg, name='adminOrg'),
    # url('kjimg/sys/user/reset', imgs_views.resetUser, name='resetUser'),
    # url('kjimg/sys/user/save', imgs_views.saveUser, name='saveUser'),
    # url('kjimg/sys/user/update', imgs_views.updateUser, name='updateUser'),
    # url('kjimg/sys/user/del', imgs_views.delUser, name='delUser'),
    # url('kjimg/sys/user/page', imgs_views.pageUser, name='pageUser'),
    # url('kjimg/sys/user', imgs_views.adminUser, name='adminUser'),
    # url('kjimg/org/listSub', imgs_views.listSubOrg, name='listSubOrg'),
    # url('kjimg/org/listSubAndSelf', imgs_views.listSubAndSelfOrg, name='listSubAndSelfOrg'),
    # url('kjimg/menu/all', imgs_views.listMenus, name='listMenus'),
    # url('kjimg/admin', admin.site.urls),
    # url('kjimg/login', imgs_views.loginSystem, name='login'),
    # url('kjimg/logout', imgs_views.logoutSystem, name='logout'),
    # url('kjimg', imgs_views.main, name='main'),
]
