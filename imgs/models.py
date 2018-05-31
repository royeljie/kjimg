from django.db import models
from django.contrib.auth.models import User, AbstractUser
# from .custom_field import ListField


# Create your models here.
class Menu(models.Model):
    text = models.CharField('菜单名称', max_length=20)
    iconCls = models.CharField('图标样式', max_length=50)
    checked = models.NullBooleanField('是否选中', )
    url = models.CharField('链接', max_length=300, null=True, blank=True)
    parentMenu = models.ForeignKey('Menu', on_delete=models.PROTECT, null=True, blank=True, related_name="children")
    seq = models.PositiveSmallIntegerField('顺序')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name
        ordering = ['seq']


class Org(models.Model):
    code = models.CharField('机构代码', max_length=10, null=False, blank=False, unique=True)
    name = models.CharField('机构名称', max_length=20, null=False, blank=False)
    seq = models.PositiveSmallIntegerField('顺序')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机构"
        verbose_name_plural = verbose_name
        ordering = ['seq']


class UserProfile(AbstractUser):
    fullname = models.CharField(max_length=10, null=False, blank=False, verbose_name="姓名")
    org = models.ForeignKey('Org', on_delete=models.PROTECT, null=True, verbose_name="所属机构")
    date_disabled = models.DateTimeField(verbose_name="停用时间", null=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['org__code', 'fullname']

    def __str__(self):
        return self.fullname


class Account(models.Model):
    code = models.CharField('科目代码', max_length=10, null=False, blank=False, unique=True)
    name = models.CharField('科目名称', max_length=20, null=False, blank=False)

    def __str__(self):
        return self.code + " " + self.name

    class Meta:
        verbose_name = "会计科目"
        verbose_name_plural = verbose_name
        ordering = ['code']


class Certificate(models.Model):
    org = models.ForeignKey('Org', on_delete=models.PROTECT, null=False, default=1)
    bookedDate = models.DateField('记账日期')
    sn = models.CharField('流水号', max_length=15, null=False, blank=False)
    amount = models.DecimalField('金额', max_digits=10, decimal_places=2)
    attachmentNo = models.PositiveSmallIntegerField('附件张数', null=False, blank=False)
    account = models.ForeignKey('Account', on_delete=models.PROTECT, null=False)
    accountDetail = models.CharField('科目明细', max_length=50, null=True, blank=True)
    uploaderName = models.CharField('录入人', max_length=10, null=False, blank=False)
    submitted = models.BooleanField('是否提交', default=False)
    rejected = models.BooleanField('是否退回', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = "会计凭证"
        verbose_name_plural = verbose_name
        ordering = ['-bookedDate', '-sn']
        unique_together = ('org', 'bookedDate', 'sn')


class CertificateImg(models.Model):
    uploadTime = models.DateTimeField('上传时间', auto_now=True)
    img = models.BinaryField('图像数据')
    thumb = models.BinaryField('缩略图')
    certificate = models.ForeignKey('Certificate', on_delete=models.CASCADE, null=False)
    description = models.CharField('影像说明', max_length=200, null=False, blank=True, default='未录入')

    class Meta:
        verbose_name = "凭证影像"
        verbose_name_plural = verbose_name
        ordering = ['uploadTime']


class RejectInfo(models.Model):
    time = models.DateTimeField('退回时间', auto_now=True)
    reason = models.TextField('退回理由', null=False, blank=False)
    handled = models.BooleanField('是否已处理', default=False)
    certificate = models.ForeignKey('Certificate', on_delete=models.CASCADE, null=False)

    verbose_name = "退回信息"
    verbose_name_plural = verbose_name
    ordering = ['time']


class Param(models.Model):
    name = models.CharField('参数名称', max_length=20, null=False, blank=False)
    code = models.CharField('参数代码', max_length=20, null=False, blank=False, unique=True)
    val = models.CharField('参数值', max_length=250, null=False, blank=False)

    verbose_name = "系统参数"
    verbose_name_plural = verbose_name
    ordering = ['code']



