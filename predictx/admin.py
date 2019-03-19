from django.contrib import admin
from  .models import Stock
# Register your models here.

#order in admin login
class StockAdmin(admin.ModelAdmin):
    fields = ["stock_title",
              "stock_name"]

admin.site.register(Stock, StockAdmin)