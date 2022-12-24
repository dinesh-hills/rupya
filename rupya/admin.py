from django.contrib import admin
from .models import Transaction, Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['tag', 'balance', 'id']
    readonly_fields = ['balance', 'id']
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['from_wallet', 'to_wallet', 'amount', 'transaction_type', 'transacted_at']
    readonly_fields = [f.name for f in Transaction._meta.fields]