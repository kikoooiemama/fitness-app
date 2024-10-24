# Fitness App

## Правила регистрации

- У нас есть 3 типа пользователя: Администратор, Тренер, Клиент -> 3 вида личных кабинетов
- Клиент регистрируется самостоятельно и попадает в приложение автоматически.
- Тренер регистрируется самостоятельно и верифицируется Администратором.
- Администратор может быть зарегистрирован только другим пользоватеелем с правами Администратора.

## Правила записи на тренировку
- Клиент открывает вкладу "Запись", выбирает тренера, выбирает время и тип тренировки (если их несколько).
- Если к тренеру записался клиент, тогда он должен подтвердить эту запись (верифицировать).
- Если тренер провел тренировку, то он отмечает в приложении, что тренировка проведена (это означает, что клиент ее оплатил).
- Неверифицованные тренером тренировки не должны попадать в БД.

## Разработка 

#### 1. Регистрация/Вход

- [x] Окно входа
- [x] Окно регистрации

#### 2. Личный кабинет администратора

- [x] Заявки от тренеров
- [x] Учет сотрудников
- [x] Учет клиентов
- [x] Генерация отчетов
- [x] Прайс-лист

#### 3. Личный кабинет тренера

- [ ] Панель с расписанием
- [ ] Панель с отчетами

#### 4. Личный кабинет клиента

- [ ] Панель с текущими занятиями
- [ ] Панель с записью к тренеру

---
