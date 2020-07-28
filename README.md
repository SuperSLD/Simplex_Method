# Simplex_Method
---
Симплекс метод для курсовой работы на python.

Однофазный симплекс метод. С поиском опорного базисного решения перебором возможных базисных переменных методом перебора(в будущем может быть будет исправлено).

В будущем возможно появятся реализации на других языках.

### Пример использования
Поиск максимального оптимального значения задачи линейного программирования.
Код из файла **test**:
```python
from LPP import LPP

lpp = LPP()

lpp.add_W(["6.5", "0", "-7.5", "23.5", "-5", 0])

lpp.add_limit(["1", "3", "1", "4", "-1", "12"])
lpp.add_limit(["2", "0", "-1", "12", "-1", "14"])
lpp.add_limit(["1", "2", "0", "3", "-1", "6"])

lpp.simplex_method(max=True)

print("Оптимальное значение " + str(lpp.get_optimal_value()))
```

Вывод программы:
```
Оптимальное значение 50/7
```
