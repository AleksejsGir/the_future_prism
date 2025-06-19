# Copyright 2024-2025 Aleksejs Giruckis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# apps/analytics/models.py
from django.db import models
from django.conf import settings
from apps.news.models import News

class Like(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='likes',
        help_text="Новость, к которой поставлен лайк"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        help_text="Пользователь, поставивший лайк"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время постановки лайка")

    class Meta:
        unique_together = ('news', 'user')  # каждый пользователь может лайкнуть новость только один раз
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} лайкнул {self.news}"
