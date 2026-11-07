class NetworkException(Exception):
    """Собственное исключение для ошибок в сети."""
    pass


class Data:
    """Класс для представления пакета данных"""
    def __init__(self, data: str, ip: int) -> None:
        if not isinstance(data, str):
            raise TypeError("Данные пакета должны быть строкой")
        if not isinstance(ip, int):
            raise TypeError("IP-адрес должен быть целым числом")
            
        self.data: str = data  # данные (строка)
        self.ip: int = ip      # адрес назначения

class Log:
    """Класс для отдельной записи лога с порядковым номером сообщения"""
    _counter = 0

    def __init__(self, message: str) -> None:
        if not isinstance(message, str):
                    raise TypeError("Cообщение должно быть строкой")
        Log._counter += 1
        self.order = Log._counter  # порядковый номер
        self.message: str = message

    def __str__(self) -> str:
        return f"[{self.order}] {self.message}"


class NetworkMonitor:
    """Класс, работающий с заметками для мониторинга сетевого трафика, работающий с объектами типа Log"""
    def __init__(self) -> None:
        self.logs = []

    def add_record(self, log_entry: Log) -> None:
        """Добавление объекта Log в журнал"""
        self.logs.append(log_entry)

    def print_logs(self) -> None:
        """Вывод всех записей журнала"""
        print("--- Журнал сетевых событий ---")
        for log in self.logs:
            print(log)
        print("------------------------------")


class Server:
    """Класс для представления сервера"""
    _ip_counter: int = 0

    def __init__(self) -> None:
        Server._ip_counter += 1
        self.buffer: list[Data] = []  # список принятых пакетов данных
        self.ip: int = self._ip_counter
        self.link = None  # роутер, к которому подключён данный сервер

    def send_data(self, data: Data) -> None:
        """Отправка пакета данных на роутер"""
        if self.link is not None:
            self.link.buffer.append(data)
        else:
            raise NetworkException(f"Ошибка: Сервер {self.ip} не подключён к роутеру")
        
    def get_data(self) -> list[Data]:
        """Возвращает список принятых пакетов и очищает буфер"""
        buf = self.buffer.copy()
        self.buffer.clear()
        return buf

    def get_ip(self) -> int:
        return self.ip


class Router:
    """Класс для представления роутера"""
    def __init__(self) -> None:
        self.buffer = []       # список пакетов данных, принятых от серверов
        self.links = {}        # словарь {ip: server} подключенных серверов

    def link(self, server: Server) -> None:
        """Присоединение сервера к роутеру"""
        if server.get_ip() not in self.links:
            self.links.update({server.get_ip(): server})
            server.link = self
        else:
            raise NetworkException(f"Ошибка: Сервер с IP {server.get_ip()} уже подключён к роутеру")

    def unlink(self, server: Server) -> None:
        """Отключение сервера от роутера"""
        if server.get_ip() in self.links:
            self.links.pop(server.get_ip())
            server.link = None
        else:
            raise NetworkException(f"Ошибка: Сервер с IP {server.get_ip()} не был подключён к роутеру")

    def send_data(self) -> None:
        """Отправка всех пакетов из буфера роутера соответствующим серверам"""
        for data in self.buffer:
            if data.ip in self.links:
                self.links[data.ip].buffer.append(data)
            else:
                raise NetworkException(f"Ошибка доставки: Сервер с IP {data.ip} не найден в сети")
        self.buffer.clear()