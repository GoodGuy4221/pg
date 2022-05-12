from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class Transaction(models.Model):
    LONG = 'L'
    SHORT = 'S'
    TYPES_TRANSACTION = (
        (LONG, 'покупка'),
        (SHORT, 'продажа'),
    )
    STOCK = 'S'
    BOND = 'B'
    CURRENCY = 'C'
    TOOLS_TYPE = (
        (STOCK, 'акция'),
        (BOND, 'облигация'),
        (CURRENCY, 'валюта'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name_asset = models.CharField(_('Название'), max_length=64, db_index=True, blank=True)
    ticker = models.CharField(_('Тикер'), max_length=64, db_index=True)
    purchase_price = models.PositiveIntegerField(_('Цена покупки в рублях за 1 ед.'))
    sale_price = models.PositiveIntegerField(_('Цена продажи в рублях за 1 ед.'))
    quantity = models.PositiveIntegerField(_('Количество единиц'))
    type_transaction = models.CharField(_('Тип сделки'), max_length=1, choices=TYPES_TRANSACTION, default=LONG)
    tool_type = models.CharField(_('Тип инструмента'), max_length=1, choices=TOOLS_TYPE, default=STOCK)
    tax = models.PositiveSmallIntegerField(_('Процент налога на прибыль'), default=13)
    broker_exchange_commission_percentage = models.PositiveSmallIntegerField(_('Комиссия брокера и биржи процент'),
                                                                             default=0.06)
    description = models.TextField(_('Описание сделки'), blank=True)
    created_at = models.DateTimeField(_('Дата создания записи'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('Дата редактирования записи'), auto_now=True)
    is_active = models.BooleanField(_('Активна'), default=True)

    # total_purchase_price = models.PositiveIntegerField(_('общая цена покупки'), null=True, blank=True),
    # full_sale_price = models.PositiveIntegerField(_('общая цена продажи'), null=True, blank=True)
    # deal_positive = models.BooleanField(_('сделка закрылась в плюс'), null=True, blank=True)
    # percent = models.PositiveSmallIntegerField(_('Процент'), null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'сделка'
        verbose_name_plural = 'сделки'

    def delete(self, using=None, keep_parents=False):
        pass

    def __str__(self):
        return f'{self.user.user_name}|{self.ticker}'

    @property
    def get_fill_purchase_price(self):
        """
        Возвращает общую цену покупки
        """
        return self.purchase_price * self.quantity

    @property
    def get_full_sale_price(self):
        """
        Возвращает общую цену продажи
        """
        return self.sale_price * self.quantity

    @property
    def get_deal_made_profit(self):
        """
        Возвращает флаг закрыта сделка в прибыль
        """
        if self.type_transaction == 'L':
            return True if self.get_fill_purchase_price < self.get_full_sale_price else False
        elif self.type_transaction == 'S':
            return True if self.get_fill_purchase_price > self.get_full_sale_price else False

    @property
    def get_percentage(self):
        """
        Возвращает процент разницы от суммы покупки и продажи
        """
        margin = abs(self.get_full_sale_price - self.get_fill_purchase_price)
        ratio = self.get_fill_purchase_price / margin
        result = 100 / ratio
        return result

    @property
    def get_dirty_profit_deal(self):
        """
        Возвращает грязную прибыль от сделки (без учета налогов и комиссий)
        """
        if self.get_deal_made_profit and self.type_transaction == 'L':
            return self.get_full_sale_price - self.get_fill_purchase_price
        elif self.get_deal_made_profit and self.type_transaction == 'S':
            return self.get_fill_purchase_price - self.get_full_sale_price
        return 0

    @property
    def get_tax_amount(self):
        """
        Возвращает сумму налога на прибыль в рублях
        """
        if self.get_deal_made_profit:
            return (self.get_dirty_profit_deal / 100) * self.tax
        return 0

    @property
    def get_commission_amount_purchase(self):
        """
        Возвращает размер комиссии при покупке
        """
        return (self.get_fill_purchase_price / 100) * self.broker_exchange_commission_percentage

    @property
    def get_commission_amount_sale(self):
        """
        Возвращает размер комиссии при продаже
        """
        return (self.get_full_sale_price / 100) * self.broker_exchange_commission_percentage

    @property
    def get_clean_profit(self):
        """
        Возвращает размер чистой прибыли от сделки
        """
        if self.get_deal_made_profit:
            tax = self.get_commission_amount_purchase + self.get_commission_amount_sale
            result = self.get_dirty_profit_deal - tax - self.get_tax_amount
            return result
        return 0
