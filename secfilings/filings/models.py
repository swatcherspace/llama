from django.db import models

class Filing(models.Model):
    cik = models.CharField(max_length=20)
    company = models.CharField(max_length=255)
    filing_type = models.CharField(max_length=50)
    filing_date = models.DateField()
    period_of_report = models.DateField()
    sic = models.CharField(max_length=10)
    state_of_inc = models.CharField(max_length=2)
    state_location = models.CharField(max_length=100)
    fiscal_year_end = models.CharField(max_length=4)
    filing_html_index = models.URLField()
    htm_filing_link = models.URLField()
    complete_text_filing_link = models.URLField()
    filename = models.CharField(max_length=255)
    
    # Fields for items (item_1 to item_10, add as needed)
    item_1 = models.TextField(blank=True, null=True)
    item_2 = models.TextField(blank=True, null=True)
    item_3 = models.TextField(blank=True, null=True)
    item_4 = models.TextField(blank=True, null=True)
    item_5 = models.TextField(blank=True, null=True)
    item_6 = models.TextField(blank=True, null=True)
    item_7 = models.TextField(blank=True, null=True)
    item_8 = models.TextField(blank=True, null=True)
    item_9 = models.TextField(blank=True, null=True)
    item_10 = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company
