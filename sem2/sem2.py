def func(value: float) -> str:
    """
    Выводит в виде строки данные о состоянии датчика и коровы, значения показаний датчика и температуры

    Args:
        float value: значение датчика (диапазон 4-20мА)
    
    Returns:
        string: данные о состоянии датчика и коровы, значения показаний датчика и температуры
    
    Raises:
        TypeError: неверный тип value
        ValueError: значение value отрицательное
    """
    if type(value) != float:
            raise TypeError("Неверный тип значения датчика")
    if value < 0:
          raise ValueError("Отрицательное значение датчика")
    
    temperature = (value - 4) * (75)/(20 - 4) #вычисляет температуру по формуле
    #cостояние дотчика
    res = f"Получен сигнал датчика {value}mA"

    if (0 <= value <= 3.9) or (value > 20.1):
        return res + ", датчик неисправен"
    res += f", датчик исправен, температура {round(temperature,1)} градусов"
    #cостояние коровы
    if 37.5 <= temperature <= 39:
          return res + ", у коровы всё норм"
    if 35 <= temperature <= 37.4:
          return res + ', корова замёрзла, требуется обогрев'
    if 39.1 <= temperature <= 39.5:
          return res + ", корова перегрелась, требуется охлаждение"
    if temperature <= 34.9:
          return res + ", требуется внимание(датчик свалился или корове плохо)"
    if temperature >= 39.6:
          return res + ", корове плохо, вызывайте ветеринара"
