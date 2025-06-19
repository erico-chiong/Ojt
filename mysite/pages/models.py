from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Memorandum(models.Model):
    memo_no = models.CharField(max_length=10, primary_key=True)
    memo_date = models.DateField()
    memo_to = models.CharField(max_length=100, blank=True, null=True)
    memo_to_pos = models.CharField(max_length=100, blank=True, null=True)
    memo_thru = models.CharField(max_length=100, blank=True, null=True)
    memo_thru_pos = models.CharField(max_length=100, blank=True, null=True)
    memo_from = models.CharField(max_length=100, blank=True, null=True)
    memo_from_pos = models.CharField(max_length=100, blank=True, null=True)
    memo_subject = models.CharField(max_length=255, blank=True, null=True)
    memo_content = models.TextField(blank=True, null=True)
    memo_recomm_by = models.CharField(max_length=50, blank=True, null=True)
    memo_approved_by = models.CharField(max_length=50, blank=True, null=True)
    memo_file = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.memo_no

class TravelOrder(models.Model):
    to_no = models.CharField(max_length=10)
    series_of = models.CharField(max_length=4)
    date_issued = models.DateTimeField()
    place = models.CharField(max_length=200)
    inclusive_dates = models.CharField(max_length=30, blank=True, null=True)
    mode_trans = models.CharField(max_length=100, blank=True, null=True)
    purpose = models.CharField(max_length=500, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    approved_by = models.CharField(max_length=100, default="MA. CARLA A. OCHOTORENA, RN., Ph.D.")
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = (('to_no', 'series_of'),)

    def __str__(self):
        return f"{self.to_no}-{self.series_of}"

class SpecialOrder(models.Model):
    so_no = models.CharField(max_length=10, primary_key=True)
    so_date = models.DateField(blank=True, null=True)
    so_subject = models.CharField(max_length=255, blank=True, null=True)
    so_content = models.TextField(blank=True, null=True)
    so_for = models.IntegerField(blank=True, null=True)
    so_signedby = models.CharField(max_length=100, blank=True, null=True)
    so_file = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.so_no

class CommunicationLetter(models.Model):
    letter_no = models.AutoField(primary_key=True)
    letter_to = models.CharField(max_length=100, blank=True, null=True)
    letter_from = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    received_by = models.CharField(max_length=100, blank=True, null=True)
    received_date = models.DateTimeField(blank=True, null=True)
    letter_notedby = models.CharField(max_length=100, blank=True, null=True)
    letter_recom_approval = models.CharField(max_length=100, blank=True, null=True)
    letter_approved_by = models.CharField(max_length=100, blank=True, null=True)
    letter_file = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.letter_no)

class MOAU(models.Model):
    moau_no = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    approved_date = models.DateField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    notarized_by = models.CharField(max_length=255, blank=True, null=True)
    notarized_date = models.DateField(blank=True, null=True)
    moau_file = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.moau_no)

class MOAUParties(models.Model):
    moauparties_id = models.AutoField(primary_key=True)
    moau_no = models.ForeignKey(MOAU, on_delete=models.CASCADE)
    agency = models.CharField(max_length=255)
    represented_by = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    referred_to_as = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = (('moau_no', 'agency'),)

    def __str__(self):
        return f"{self.agency} ({self.moau_no})"

class MOAUSignatories(models.Model):
    mousgn_id = models.AutoField(primary_key=True)
    moau_no = models.ForeignKey(MOAU, on_delete=models.CASCADE)
    signed_by = models.CharField(max_length=50)
    position = models.CharField(max_length=50, blank=True, null=True)
    agency = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = (('moau_no', 'signed_by'),)

    def __str__(self):
        return f"{self.signed_by} ({self.moau_no})"
