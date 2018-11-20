import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods

from PIL import Image
from pymysql import Date

from imgs.forms import *
from imgs.models import *

import io

DEFAULT_PASSWORD = '123456'


def loginSystem(request):
    return render(request, 'login.html')


# Create your views here.
@login_required
def logoutSystem(request):
    logout(request)
    return HttpResponseRedirect('/kjimg/login')


@login_required
def main(request):
    today = Date.today().strftime('%Y年%m月%d日')
    return render(request, 'main.html', {'today': today})


@login_required
def listMenus(request):
    currentUser = request.user
    role = currentUser.role

    rootMenus = Menu.objects.filter(parentMenu=None).filter(roles__contains=role)
    menus = []
    for menu in rootMenus:
        menus.append(formMenuTree(menu, request))
    return JsonResponse(menus, safe=False)


def formMenuTree(menu, request):
    currentUser = request.user
    role = currentUser.role

    jsonObj = {"id": menu.id, "text": menu.text, "iconCls": menu.iconCls}
    if menu.url != None:
        jsonObj["url"] = menu.url
    subMenus = Menu.objects.filter(parentMenu=menu)
    children = []
    if subMenus.count() > 0:
        jsonObj["state"] = "open"
        for subMenu in subMenus:
            if subMenu.roles.find(role) != -1:
                print(subMenu.text.find('下级'))
                if subMenu.text.find('下级') != -1:
                    if hasSubOrg(currentUser):
                        children.append(formMenuTree(subMenu, request))
                else:
                    children.append(formMenuTree(subMenu, request))
        jsonObj["children"] = children
    return jsonObj


@staff_member_required
def adminUser(request):
    return render(request, 'adminUser.html')


@staff_member_required
@require_http_methods(["GET"])
def pageUser(request):
    currentUser = request.user

    userList = []
    page = int(request.GET.get('page', 1))
    rows = int(request.GET.get('rows', 20))
    users = UserProfile.objects.filter(org__code__startswith=currentUser.org.code)
    paginator = Paginator(users, rows)
    try:
        showUsers = paginator.page(page)
    except PageNotAnInteger:
        showUsers = paginator.page(1)
    except EmptyPage:
        showUsers = paginator.page(paginator.num_pages)
    for user in showUsers:
        date_joined = user.date_joined.strftime('%Y-%m-%d %H:%I:%S')
        userObj = {"id": user.id, "username": user.username, "fullname": user.fullname,
                   "roleName": user.get_role_display(), "roleId": user.role, "is_active": user.is_active,
                   "active": user.is_active and '启用' or '停用', "date_joined": date_joined, "orgId": user.org.id,
                   "orgName": user.org.name}
        userList.append(userObj)
    pageObj = {"total": len(users), "rows": userList}
    return JsonResponse(pageObj, safe=False)


@staff_member_required
@require_http_methods(["POST"])
@transaction.atomic
def saveUser(request):
    instance = UserProfile(is_staff=True, is_superuser=False)
    form = UserForm(request.POST, instance=instance)
    if form.is_valid():
        try:
            user = form.save()
            user.set_password(DEFAULT_PASSWORD)
            user.save()
        except:
            return JsonResponse({"rst": False, "msg": "用户信息保存失败！"}, safe=False, content_type='text/html')
        return JsonResponse({"rst": True, "msg": "用户信息保存成功！"}, safe=False, content_type='text/html')


@staff_member_required
@require_http_methods(["POST"])
def updateUser(request):
    form = UserForm(request.POST)
    id = form.data['id']
    user = UserProfile.objects.get(pk=id)
    # user.username = form.data['username']
    user.fullname = form.data['fullname']
    user.is_active = form.data['is_active']
    user.org = Org.objects.get(id=form.data['org'])
    user.role = form.data['role']
    try:
        user.save()
        return JsonResponse({"rst": True, "msg": "用户信息更新成功！"}, safe=False, content_type='text/html')
    except Exception as e:
        raise e
        return JsonResponse({"rst": False, "msg": "用户信息更新失败！"}, safe=False, content_type='text/html')


@staff_member_required
@require_http_methods(["GET"])
def delUser(request):
    id = request.GET['id']
    try:
        UserProfile.objects.get(pk=id).delete()
        return JsonResponse({"rst": True, "msg": "用户信息删除成功！"}, safe=False)
    except:
        return JsonResponse({"rst": False, "msg": "用户信息删除失败！"}, safe=False)


@staff_member_required
@require_http_methods(["GET"])
def disableUser(request):
    id = request.GET['id']
    try:
        user = UserProfile.objects.get(pk=id)
        user.is_active = False
        user.date_disabled = Date
        user.save()
        return JsonResponse({"rst": True, "msg": "用户信息删除成功！"}, safe=False)
    except:
        return JsonResponse({"rst": False, "msg": "用户信息删除失败！"}, safe=False)


@staff_member_required
@require_http_methods(["GET"])
def resetUser(request):
    id = request.GET['id']
    try:
        user = UserProfile.objects.get(pk=id)
        user.set_password(DEFAULT_PASSWORD)
        user.save()
        return JsonResponse({"rst": True, "msg": "用户密码重置成功！"}, safe=False)
    except:
        return JsonResponse({"rst": False, "msg": "用户密码重置失败！"}, safe=False)


@sensitive_post_parameters()
@login_required
@require_http_methods(["POST"])
def changePwd(request, password_change_form=PasswordChangeForm):
    form = password_change_form(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(request, form.user)
        return JsonResponse({"rst": True, "msg": "用户密码修改成功！"}, safe=False)
    else:
        msg = '用户密码修改失败'
        if form.has_error(field='old_password', code='password_incorrect'):
            msg += '，旧密码输入错误'
        if form.has_error(field='new_password2', code='password_mismatch'):
            msg += '，两次密码输入不一致'
        elif form.has_error(field='new_password2'):
            msg += '，新密码应至少8位，且包含字母和数字'
        return JsonResponse({"rst": False, "msg": msg}, safe=False)


@login_required
@require_http_methods(["GET"])
def myTodoCertificate(request):
    return render(request, 'adminCertificate.html', {"scope": 'todo'})


@login_required
@require_http_methods(["GET"])
def mySubmittedCertificate(request):
    return render(request, 'adminCertificate.html', {"scope": 'submitted'})


@login_required
@require_http_methods(["GET"])
def adminCertificate(request):
    return render(request, 'adminCertificate.html', {"scope": 'belonged'})


@login_required
@require_http_methods(["POST"])
def pageCertificate(request):
    currentUser = request.user
    scope = request.POST.get('scope', 'todo')

    certList = []
    page = int(request.POST.get('page', 1))
    rows = int(request.POST.get('rows', 20))
    if currentUser.org is None:
        certs = {}
    elif scope == 'todo':
        certs = Certificate.objects.filter(org__code=currentUser.org.code).filter(submitted=False)
    elif scope == 'submitted':
        certs = Certificate.objects.filter(org__code=currentUser.org.code).filter(submitted=True)
    elif scope == 'belonged':
        certs = Certificate.objects.filter(org__code__startswith=currentUser.org.code).exclude(
            org__code=currentUser.org.code).filter(submitted=True)
    elif scope == 'all':
        certs = Certificate.objects.all()
    else:
        certs = {}

    orgId = request.POST.get('orgId', None)
    # accountCode = request.POST.get('accountCode', None)
    # detail = request.POST.get('detail', None)
    now_time = datetime.datetime.now()
    first_day = datetime.datetime(now_time.year, now_time.month, 1, 0, 0, 0)
    last_day = datetime.datetime(now_time.year, now_time.month + 1, 1, 0, 0, 0)
    beginDate = request.POST.get('beginDate', None)
    endDate = request.POST.get('endDate', None)
    beginAmount = request.POST.get('beginAmount', None)
    endAmount = request.POST.get('endAmount', None)
    if orgId is not None and orgId != '':
        certs = certs.filter(org_id=orgId)
    # if accountCode is not None and accountCode != '':
    #     certs = certs.filter(accountCode=accountCode)
    # if detail is not None and detail != '':
    #     certs = certs.filter(accountDetail__contains=detail)
    if beginDate is not None and beginDate != '':
        certs = certs.filter(bookedDate__gte=beginDate)
    if endDate is not None and endDate != '':
        certs = certs.filter(bookedDate__lte=endDate)
    # if beginAmount is not None and beginAmount != '':
    #     certs = certs.filter(amount__gte=beginAmount)
    # if endAmount is not None and endAmount != '':
    #     certs = certs.filter(amount__lte=endAmount)

    paginator = Paginator(certs, rows)
    try:
        showCerts = paginator.page(page)
    except PageNotAnInteger:
        showCerts = paginator.page(1)
    except EmptyPage:
        showCerts = paginator.page(paginator.num_pages)
    for cert in showCerts:
        rejectInfoList = RejectInfo.objects.filter(certificate_id=cert.id).filter(handled=False)
        rejectMsg = ''
        for info in rejectInfoList:
            rejectMsg += '' + info.time.strftime("%Y-%m-%d %H:%I:%S") + '&nbsp;' + info.reason + '<br>'
        if len(rejectMsg) != 0:
            certObj = {"id": cert.id, "orgName": cert.org.name, "bookedYearMonth": cert.bookedDate.strftime("%Y-%m"),
                       "bookedDate": cert.bookedDate, "sn": cert.sn, "attachmentNo": cert.attachmentNo,
                       "rejectMsg": rejectMsg,
                       "uploaderName": cert.uploaderName, "submitted": cert.submitted, "rejected": cert.rejected}
        else:
            certObj = {"id": cert.id, "orgName": cert.org.name, "bookedYearMonth": cert.bookedDate.strftime("%Y-%m"),
                       "bookedDate": cert.bookedDate, "sn": cert.sn, "attachmentNo": cert.attachmentNo,
                       "uploaderName": cert.uploaderName, "submitted": cert.submitted, "rejected": cert.rejected}
        certList.append(certObj)
    pageObj = {"total": len(certs), "rows": certList}
    return JsonResponse(pageObj, safe=False)


@login_required
@require_http_methods(["GET"])
def countRejectedCertificate(request):
    currentUser = request.user
    org = currentUser.org

    rejectInfos = RejectInfo.objects.filter(certificate__org=org, handled=False)
    count = rejectInfos.count()
    return JsonResponse({"rst": True, "count": count}, safe=False, content_type='text/html')


@login_required
@require_http_methods(["POST"])
def saveCertificate(request):
    currentUser = request.user
    bookedDate = request.POST['bookedYearMonth'] + '-01'

    cert = Certificate(org=currentUser.org, attachmentNo=0, uploaderName=currentUser.fullname, bookedDate=bookedDate)
    form = CertificateForm(request.POST, instance=cert)
    if form.is_valid():
        try:
            instance = form.save()
        except IntegrityError as e:
            return JsonResponse({"rst": False, "msg": "账务信息保存失败，一个月之内凭证号不能重复！"}, safe=False, content_type='text/html')
        except:
            return JsonResponse({"rst": False, "msg": "账务信息保存失败！"}, safe=False, content_type='text/html')
        return JsonResponse({"rst": True, "msg": "账务信息保存成功！", "certId": instance.id}, safe=False,
                            content_type='text/html')
    else:
        return JsonResponse({"rst": False, "msg": "账务信息保存失败！"}, safe=False, content_type='text/html')


@login_required
@require_http_methods(["POST"])
def updateCertificate(request):
    form = CertificateForm(request.POST)
    bookedDate = request.POST['bookedYearMonth'] + '-01'
    print(bookedDate)

    try:
        Certificate.objects.filter(id=form.data['id']).update(bookedDate=bookedDate, sn=form.data['sn'])
        return JsonResponse({"rst": True, "msg": "账务信息更新成功！"}, safe=False, content_type='text/html')
    except IntegrityError as e:
        return JsonResponse({"rst": False, "msg": "账务信息更新失败，一个月之内凭证号不能重复！"}, safe=False, content_type='text/html')
    except:
        return JsonResponse({"rst": False, "msg": "账务信息更新失败！"}, safe=False, content_type='text/html')


@login_required
@require_http_methods(["GET"])
@transaction.atomic
def delCertificate(request):
    idList = request.GET.getlist('ids')
    try:
        for id in idList:
            Certificate.objects.filter(pk=id).delete()
        return JsonResponse({"rst": True, "msg": "账务信息删除成功！"}, safe=False)
    except:
        return JsonResponse({"rst": False, "msg": "账务信息删除失败！"}, safe=False)


# @login_required
# @require_http_methods(["POST"])
# @transaction.atomic
# def importCertificate(request):
#     try:
#         fileObj = request.FILES.get("certificateFile")
#
#         xls = xlrd.open_workbook(file_contents=fileObj.read())
#         sheet = xls.sheets()[0]
#         for i in range(sheet.nrows):
#             code = str(int(sheet.row_values(i)[0]))
#             name = sheet.row_values(i)[1]
#             Account.objects.get_or_create(code=code, name=name)
#
#     except Exception as e:
#         raise e
#         return JsonResponse({"rst": False, "msg": "批量导入账务信息失败！"}, safe=False, content_type='text/html')
#     return JsonResponse({"rst": True, "msg": "批量导入账务信息成功！"}, safe=False, content_type='text/html')


@login_required
@require_http_methods(["GET"])
@transaction.atomic
def submitCertificate(request):
    idList = request.GET.getlist('ids')
    try:
        for id in idList:
            cert = Certificate.objects.get(pk=id)
            cert.submitted = True
            cert.rejected = False
            cert.save()
            RejectInfo.objects.filter(certificate_id=id).filter(handled=False).update(handled=True)
        return JsonResponse({"rst": True, "msg": "账务信息提交成功！"}, safe=False)
    except:
        return JsonResponse({"rst": False, "msg": "账务信息提交失败！"}, safe=False)


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def rejectCertificate(request):
    form = RejectInfoForm(request.POST)
    if form.is_valid():
        try:
            rejectInfo = form.save()
            cert = rejectInfo.certificate
            cert.submitted = False
            cert.rejected = True
            cert.save()
        except Exception as e:
            print(e.__traceback__)
            return JsonResponse({"rst": False, "msg": "账务信息退回失败！"}, safe=False, content_type='text/html')
        return JsonResponse({"rst": True, "msg": "账务信息退回成功！"}, safe=False, content_type='text/html')
    else:
        return JsonResponse({"rst": False, "msg": "账务信息退回失败！"}, safe=False, content_type='text/html')


@login_required
def adminCertificateImg(request):
    certId = request.GET.get("certId")
    cert = Certificate.objects.get(id=certId)
    if cert.submitted:
        canDelete = False
    else:
        canDelete = True
    return render(request, 'adminCertificateImg.html', {'certId': certId, 'canDelete': canDelete})


@login_required
def adminCertImg(request):
    certId = request.GET.get("certId")
    cert = Certificate.objects.get(id=certId)
    if cert.submitted:
        canDelete = False
    else:
        canDelete = True
    imgs = CertificateImg.objects.filter(certificate_id=certId).only('uploadTime', 'description')
    return render(request, 'adminCertImg.html', {'certId': certId, 'canDelete': canDelete, 'imgs': imgs})


@login_required
@require_http_methods(["GET"])
def listCertificateImg(request):
    currentUser = request.user
    certId = request.GET.get("certId")

    imgList = []
    page = int(request.GET.get('page', 1))
    rows = int(request.GET.get('rows', 20))
    if currentUser.org is None:
        imgs = {}
    else:
        imgs = CertificateImg.objects.filter(certificate_id=certId).only('uploadTime')

    paginator = Paginator(imgs, rows)

    try:
        showImgs = paginator.page(page)
    except PageNotAnInteger:
        showImgs = paginator.page(1)
    except EmptyPage:
        showImgs = paginator.page(paginator.num_pages)
    for img in showImgs:
        timeStr = img.uploadTime.strftime('%Y-%m-%d %H:%I:%S')
        imgObj = {"id": img.id, "uploadTime": timeStr, "description": img.description}
        imgList.append(imgObj)
    pageObj = {"total": len(imgs), "rows": imgList}
    return JsonResponse(pageObj, safe=False)


@login_required
@require_http_methods(["GET"])
@transaction.atomic
def delCertificateImg(request):
    id = str(request.GET.get('id')).replace('img_', '')
    currentUser = request.user
    try:
        img = CertificateImg.objects.get(pk=id)
    except:
        return JsonResponse({"rst": False, "msg": "影像文件不存在！"}, safe=False)

    if currentUser.role == 'user' and currentUser.org.id == img.certificate.org.id and img.certificate.submitted is False:
        try:
            img.certificate.attachmentNo = img.certificate.attachmentNo - 1
            img.certificate.save()
            img.delete()

            return JsonResponse({"rst": True, "msg": "影像文件删除成功！"}, safe=False)
        except:
            return JsonResponse({"rst": False, "msg": "影像文件删除失败！"}, safe=False)
    else:
        return JsonResponse({"rst": False, "msg": "影像文件删除失败，无权限！"}, safe=False)


@login_required
@require_http_methods(["GET"])
@transaction.atomic
def changeCertificateImgOrder(request):
    action = request.GET.get('action')
    currentUser = request.user
    try:
        id = str(request.GET.get('id')).replace('img_', '')
        img = CertificateImg.objects.get(pk=id)
        if currentUser.role == 'user' and currentUser.org.id == img.certificate.org.id and img.certificate.submitted is False:
            if action == 'toFirst':
                firstImg = CertificateImg.objects.filter(certificate_id=img.certificate.id).order_by(
                    'uploadTime').first()
                if img.id == firstImg.id:
                    return JsonResponse({"rst": False, "msg": "该影像已经在第一位了！"}, safe=False)
                else:
                    newUploadTime = firstImg.uploadTime - datetime.timedelta(minutes=1)
                    CertificateImg.objects.filter(id=id).update(uploadTime=newUploadTime)
                    return JsonResponse({"rst": True, "msg": "该影像排序成功！"}, safe=False)
            elif action == 'toLast':
                lastImg = CertificateImg.objects.filter(certificate_id=img.certificate.id).order_by(
                    '-uploadTime').first()
                if img.id == lastImg.id:
                    return JsonResponse({"rst": False, "msg": "该影像已经在最后一位了！"}, safe=False)
                else:
                    newUploadTime = lastImg.uploadTime + datetime.timedelta(minutes=1)
                    CertificateImg.objects.filter(id=id).update(uploadTime=newUploadTime)
                    return JsonResponse({"rst": True, "msg": "该影像排序成功！"}, safe=False)
            else:
                return JsonResponse({"rst": False, "msg": "未指定排序方法！"}, safe=False)
        else:
            return JsonResponse({"rst": False, "msg": "影像文件排序失败，无权限！"}, safe=False)
    except Exception as e:
        raise e
        return JsonResponse({"rst": False, "msg": "影像文件不存在！"}, safe=False)


@login_required
@require_http_methods(["POST"])
@transaction.atomic
def uploadImg(request):
    certId = request.POST.get("certId")
    try:
        cert = Certificate.objects.get(id=certId)
        fileObj = request.FILES.get("img")
        description = request.POST['description']

        # 产生缩略图
        thumb = Image.open(fileObj)

        output1 = io.BytesIO()
        thumb.save(output1, format='JPEG')

        thumbHeight = int(thumb.size[1] * 200 / thumb.size[0])
        size = (200, thumbHeight)
        thumb.thumbnail(size)
        output2 = io.BytesIO()
        thumb.save(output2, format='JPEG')

        img = CertificateImg(img=output1.getvalue(), thumb=output2.getvalue(), certificate_id=certId,
                             description=description)
        img.save()
        attachmentNo = cert.attachmentNo + 1
        Certificate.objects.filter(id=cert.id).update(attachmentNo=attachmentNo)
    except OSError:
        return JsonResponse({"rst": False, "msg": "图片格式不正确，请上传JPG格式文件！"}, safe=False, content_type='text/html')
    except Exception as e:
        return JsonResponse({"rst": False, "msg": "凭证影像保存失败！"}, safe=False, content_type='text/html')
    return JsonResponse({"rst": True, "msg": "凭证影像保存成功！", "certId": certId}, safe=False, content_type='text/html')


@login_required
@require_http_methods(["GET"])
def viewThumb(request):
    imgId = request.GET.get("imgId")
    try:
        certImg = CertificateImg.objects.get(id=imgId)
        return HttpResponse(certImg.thumb, content_type="image/jpeg")

    except ObjectDoesNotExist:
        noimgUrl = "imgs/static/images/noimg.jpeg"
        imageData = open(noimgUrl, "rb").read()
        return HttpResponse(imageData, content_type="image/jpeg")


@login_required
@require_http_methods(["GET"])
def viewImg(request):
    imgId = request.GET.get("imgId")
    try:
        certImg = CertificateImg.objects.get(id=imgId)
        imageData = certImg.img
        return HttpResponse(imageData, content_type="image/jpeg")

    except ObjectDoesNotExist:
        noimgUrl = "imgs/static/images/noimg.jpeg"
        imageData = open(noimgUrl, "rb").read()
        return HttpResponse(imageData, content_type="image/jpeg")


@login_required
@require_http_methods(["GET"])
def listSubOrg(request):
    currentUser = request.user

    orgList = []
    orgs = Org.objects.filter(code__startswith=currentUser.org.code).exclude(code=currentUser.org.code)
    for org in orgs:
        orgList.append({"id": org.id, "code": org.code, "name": org.name})
    return JsonResponse(orgList, safe=False)


@login_required
@require_http_methods(["GET"])
def listSubAndSelfOrg(request):
    currentUser = request.user

    orgList = []
    orgs = Org.objects.filter(code__startswith=currentUser.org.code)
    for org in orgs:
        orgList.append({"id": org.id, "code": org.code, "name": org.name})
    return JsonResponse(orgList, safe=False)


@staff_member_required
@require_http_methods(["GET"])
def adminOrg(request):
    currentUser = request.user

    return render(request, 'adminOrg.html', {"orgCode": currentUser.org.code})


@staff_member_required
@require_http_methods(["GET"])
def pageOrg(request):
    currentUser = request.user

    orgList = []
    page = int(request.GET.get('page', 1))
    rows = int(request.GET.get('rows', 20))
    orgs = Org.objects.filter(code__startswith=currentUser.org.code)  # .exclude(code=currentUser.org.code)
    paginator = Paginator(orgs, rows)
    try:
        showOrgs = paginator.page(page)
    except PageNotAnInteger:
        showOrgs = paginator.page(1)
    except EmptyPage:
        showOrgs = paginator.page(paginator.num_pages)
    for org in showOrgs:
        selfCode = org.code.replace(currentUser.org.code, '')
        orgObj = {"id": org.id, "code": org.code, "selfCode": selfCode, "name": org.name}
        orgList.append(orgObj)
    pageObj = {"total": len(orgs), "rows": orgList}
    return JsonResponse(pageObj, safe=False)


@staff_member_required
@require_http_methods(["POST"])
def saveOrg(request):
    currentUser = request.user

    code = currentUser.org.code + request.POST['selfCode']
    org = Org(code=code)
    form = OrgForm(request.POST, instance=org)
    if form.is_valid():
        try:
            form.save()
        except IntegrityError:
            return JsonResponse({"rst": False, "msg": "机构信息保存失败，机构代码不能重复！"}, safe=False, content_type='text/html')
        except Exception:
            return JsonResponse({"rst": False, "msg": "机构信息保存失败！"}, safe=False, content_type='text/html')
        return JsonResponse({"rst": True, "msg": "机构信息保存成功！"}, safe=False, content_type='text/html')
    else:
        return JsonResponse({"rst": False, "msg": "机构信息保存失败，机构代码可能重复！"}, safe=False, content_type='text/html')


@staff_member_required
@require_http_methods(["POST"])
def updateOrg(request):
    currentUser = request.user

    form = OrgForm(request.POST)
    orgId = form.data['id']
    orgName = form.data['name']
    orgCode = currentUser.org.code + form.data['selfCode']
    try:
        org = Org.objects.get(pk=orgId)
        org.name = orgName
        org.code = orgCode
        org.save()
        return JsonResponse({"rst": True, "msg": "机构信息更新成功！"}, safe=False, content_type='text/html')
    except IntegrityError:
        return JsonResponse({"rst": False, "msg": "机构信息更新失败，机构代码不能重复！"}, safe=False, content_type='text/html')
    except Exception as e:
        return JsonResponse({"rst": False, "msg": "机构信息更新失败！"}, safe=False, content_type='text/html')


@staff_member_required
@require_http_methods(["GET"])
def delOrg(request):
    currentUser = request.user

    orgId = request.GET['id']
    org = Org.objects.get(pk=orgId)
    if org.code.startswith(currentUser.org.code) and org.code != currentUser.org.code:
        try:
            org.delete()
            return JsonResponse({"rst": True, "msg": "机构信息删除成功！"}, safe=False)
        except:
            return JsonResponse({"rst": False, "msg": "机构信息删除失败！"}, safe=False)
    else:
        return JsonResponse({"rst": False, "msg": "机构信息删除失败，无权限！"}, safe=False)


def hasSubOrg(currentUser):
    org = currentUser.org
    subOrgs = Org.objects.filter(code__startswith=org.code).exclude(code=org.code)
    if len(subOrgs) > 0:
        return True
    else:
        return False


def hasParentOrg(currentUser):
    org = currentUser.org
    parentOrg = Org.objects.filter(code__search='')


# @staff_member_required
# @require_http_methods(["GET"])
# def adminAccount(request):
#     return render(request, 'adminAccount.html')
#
#
# @staff_member_required
# @require_http_methods(["GET"])
# def pageAccount(request):
#     accountList = []
#     page = int(request.GET.get('page', 1))
#     rows = int(request.GET.get('rows', 20))
#     accounts = Account.objects.all()
#     paginator = Paginator(accounts, rows)
#     try:
#         showAccounts = paginator.page(page)
#     except PageNotAnInteger:
#         showAccounts = paginator.page(1)
#     except EmptyPage:
#         showAccounts = paginator.page(paginator.num_pages)
#     for account in showAccounts:
#         accountObj = {"id": account.id, "code": account.code, "name": account.name}
#         accountList.append(accountObj)
#     pageObj = {"total": len(accounts), "rows": accountList}
#     return JsonResponse(pageObj, safe=False)
#
#
# @staff_member_required
# @require_http_methods(["POST"])
# def saveAccount(request):
#     form = AccountForm(request.POST)
#     if form.is_valid():
#         try:
#             form.save()
#         except Exception as e:
#             print(e.__traceback__)
#             return JsonResponse({"rst": False, "msg": "会计科目保存失败！"}, safe=False, content_type='text/html')
#         return JsonResponse({"rst": True, "msg": "会计科目保存成功！"}, safe=False, content_type='text/html')
#     else:
#         return JsonResponse({"rst": False, "msg": "会计科目保存失败，科目代码可能重复！"}, safe=False, content_type='text/html')
#
#
# @staff_member_required
# @require_http_methods(["POST"])
# def updateAccount(request):
#     form = AccountForm(request.POST)
#     accountId = form.data['id']
#     accountName = form.data['name']
#     try:
#         Account.objects.filter(id=accountId).update(name=accountName)
#         return JsonResponse({"rst": True, "msg": "会计科目更新成功！"}, safe=False, content_type='text/html')
#     except Exception:
#         return JsonResponse({"rst": False, "msg": "会计科目更新失败！"}, safe=False, content_type='text/html')
#
#
# @staff_member_required
# @require_http_methods(["GET"])
# def delAccount(request):
#     accountId = request.GET['id']
#     account = Account.objects.get(pk=accountId)
#     try:
#         account.delete()
#         return JsonResponse({"rst": True, "msg": "会计科目删除成功！"}, safe=False)
#     except:
#         return JsonResponse({"rst": False, "msg": "会计科目删除失败！"}, safe=False)
#
#
# @staff_member_required
# @require_http_methods(["POST"])
# @transaction.atomic
# def importAccount(request):
#     try:
#         fileObj = request.FILES.get("accountFile")
#
#         xls = xlrd.open_workbook(file_contents=fileObj.read())
#         sheet = xls.sheets()[0]
#         for i in range(sheet.nrows):
#             code = str(int(sheet.row_values(i)[0]))
#             name = sheet.row_values(i)[1]
#             Account.objects.get_or_create(code=code, name=name)
#
#     except Exception:
#         return JsonResponse({"rst": False, "msg": "批量导入会计科目失败！"}, safe=False, content_type='text/html')
#     return JsonResponse({"rst": True, "msg": "批量导入会计科目成功！"}, safe=False, content_type='text/html')
#
#
# @login_required
# @require_http_methods(["GET"])
# def listAccount(request):
#     accountList = []
#     accounts = Account.objects.all()
#     for account in accounts:
#         accountList.append({"id": account.id, "code": account.code, "name": account.name,
#                             "fullname": account.code + ' ' + account.name})
#     return JsonResponse(accountList, safe=False)


@staff_member_required
@require_http_methods(["GET"])
def adminParam(request):
    return render(request, 'adminParam.html')


@staff_member_required
@require_http_methods(["GET"])
def pageParam(request):
    paramList = []
    page = int(request.GET.get('page', 1))
    rows = int(request.GET.get('rows', 20))
    params = Param.objects.all()
    paginator = Paginator(params, rows)
    try:
        showParams = paginator.page(page)
    except PageNotAnInteger:
        showParams = paginator.page(1)
    except EmptyPage:
        showParams = paginator.page(paginator.num_pages)
    for param in showParams:
        paramObj = {"id": param.id, "name": param.name, "code": param.code, "val": param.val}
        paramList.append(paramObj)
    pageObj = {"total": len(params), "rows": paramList}
    return JsonResponse(pageObj, safe=False)


@staff_member_required
@require_http_methods(["POST"])
def updateParam(request):
    form = ParamForm(request.POST)
    paramId = form.data['id']
    paramVal = form.data['val']
    try:
        Param.objects.filter(id=paramId).update(val=paramVal)
        return JsonResponse({"rst": True, "msg": "系统参数更新成功！"}, safe=False, content_type='text/html')
    except Exception:
        return JsonResponse({"rst": False, "msg": "系统参数更新失败！"}, safe=False, content_type='text/html')


@staff_member_required
@require_http_methods(["GET"])
def listRoles(request):
    roleList = []
    for role in UserProfile.ROLES:
        roleList.append({"id": role[0], "name": role[1]})
    return JsonResponse(roleList, safe=False)
