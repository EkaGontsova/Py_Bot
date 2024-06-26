**Название:** Тренажер английских слов

**Описание:**
Бот, который помогает изучать английские слова по карточкам.

**Возможности:**
* Выбор случайной пары слов из базы данных.
* Добавление новых слов в базу данных.
* Удаление слов из базы данных.
* Проверка правильности перевода.

**Использование:**
1. Запустите бота, отправив команду `/start`.
2. Выберите перевод для предложенного русского слова.
3. Если ответ верный, появится возможность перейти к следующей карточке.
4. Если ответ неверный, бот выдаст ошибку и предложит попробовать еще раз.
5. Для добавления нового слова отправьте команду `/add_word`.
6. Для удаления слова отправьте команду `/delete_word`.

**Команды:**

* `/start`: Запустить бота.
* `/add_word`: Добавить новое слово в базу данных.
* `/delete_word`: Удалить слово из базы данных.
* `/next`: Перейти к следующей карточке.

**Пример использования:**

```
Пользователь: /start
Бот: Hello! Let's study English!
Бот: Выберите перевод:
Бот: 🇷🇺 Лес
Бот: 1. Forest
Бот: 2. River
Бот: 3. Mountain
Бот: 4. Sun

Пользователь: 1
Бот: Это правильный ответ! 👍
Бот: Forest -> Лес
Бот: Дальше ⏭
```