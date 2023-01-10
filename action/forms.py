from django import forms

from action.models import Treatment, TreatmentProcess, Consulting
from manager.models import Employee, Customer, Service


class ConsultingForm(forms.ModelForm):
    customer = \
        forms.ModelChoiceField(
            Customer.objects.all(),
            label='Khách Hàng:',
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    consultor = \
        forms.ModelChoiceField(
            Employee.objects.all(),
            label='Tư vấn :',
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    date = \
        forms.DateField(
            label='Ngày:',
            widget=forms.DateInput(
                attrs={'type': 'date', 'format': '%d %m %Y'},
                format='%Y-%m-%d',
            )
            # widget=DatePickerInput()
        )
    request = \
        forms.CharField(
            label='Yêu cầu của K/H:',
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Request'})
        )
    medicalhistory = \
        forms.CharField(
            label='Tiền sử bệnh lý:',
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medical history'})
        )
    health = \
        forms.CharField(
            label='Sức khỏe hiện tại:',
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Health'})
        )

    class Meta:
        model = Consulting
        fields = '__all__'


class ConsultingFilterForm(forms.Form):
    mobile: forms.CharField()


class TreatmentForm(forms.ModelForm):
    service = \
        forms.ModelChoiceField(
            Service.objects.all(),
            label='Dịch vụ:',
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    customer = \
        forms.ModelChoiceField(
            Customer.objects.all(),
            label='Khách Hàng:',
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    date_apply = \
        forms.DateField(
            label='Ngày mua:',
            widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
            # widget=DatePickerInput()
        )
    date_end = \
        forms.DateField(
            required=False,
            label='Ngày hết hạn:',
            widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
            # widget=DatePickerInput()
        )
    consultant = \
        forms.ModelChoiceField(
            Employee.objects.all(),
            label='Tư vấn viên:',
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    expert = \
        forms.ModelChoiceField(
            Employee.objects.filter(department=3),
            label='Chuyên viên:',
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    doctor = \
        forms.ModelChoiceField(
            Employee.objects.filter(department=3),
            label='Bác sĩ:',
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    note = \
        forms.CharField(
            label='Ghi chú:',
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'})
        )

    class Meta:
        model = Treatment
        fields = ('service', 'customer', 'consultant', 'expert', 'doctor', 'date_apply', 'date_end', 'note')


class TreatmentFilterForm(forms.Form):
    mobile: forms.CharField()


class TreatmentAppendForm(forms.ModelForm):
    """
    tag = \
      forms.IntegerField(
        label='Yêu cầu nhập đúng con số ở trên:',
        widget=forms.NumberInput()
      )
    """
    date = \
        forms.DateField(
            label='Ngày cập nhật:',
            widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
            # widget=DatePickerInput()
        )
    status = \
        forms.CharField(
            label='Tình trạng:',
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Warranty'})
        )
    thumb = \
        forms.ImageField(
            required=False,
            label='Hình ảnh:',
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )

    class Meta:
        model = TreatmentProcess
        fields = ('date', 'status', 'thumb')


class TreatmentProcessForm(forms.ModelForm):
    date = \
        forms.DateField(
            label='Ngày:',
            widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
            # widget=DatePickerInput()
        )
    status = \
        forms.CharField(
            label='Tình trạng:',
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Warranty'})
        )
    tmp_thumb = \
        forms.ImageField(
            required=False,
            label='Thêm ảnh:',
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )

    class Meta:
        model = TreatmentProcess
        fields = ('date', 'status', 'tmp_thumb')
