import re

from rest_framework import serializers


class URLValidator:

    def __init__(self, url):
        self.url = url

    def __call__(self, value):
        reg = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$',)
        tmp_url = dict(value).get(self.url)
        if not bool(reg.match(tmp_url)):
            raise serializers.ValidationError('Данная ссылка не является ссылкой на Youtube')
