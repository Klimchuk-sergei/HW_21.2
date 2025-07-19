import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        Обрабатывает GET-запросы.
        На любой GET-запрос возвращает содержимое файла contacts.html
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        try:
            # Читаем файл в бинарном режиме 'rb'
            with open('templates/contacts.html', 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found: templates/contacts.html")
            self.wfile.write(b"404 - contacts.html not found")

    def do_POST(self):
        """
        Обрабатывает POST-запросы.
        Считывает данные из формы и выводит их в консоль.
        """
        # Получаем длину тела запроса
        content_length = int(self.headers['Content-Length'])
        # Считываем тело запроса (данные формы)
        post_data_bytes = self.rfile.read(content_length)

        # Декодируем байты в строку
        post_data_str = post_data_bytes.decode('utf-8')

        # Парсим URL-encoded строку в словарь.
        # parse_qs удобен, но возвращает значения в виде списков.
        parsed_data = urllib.parse.parse_qs(post_data_str)

        print("--- Получены данные из формы ---")
        for key, value in parsed_data.items():
            # Берем первое значение из списка
            print(f"  {key}: {value[0]}")
        print("---------------------------------")

        # Отправляем простой ответ пользователю
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        response_message = """
            <html>
            <head><title>Спасибо!</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body class="d-flex justify-content-center align-items-center vh-100">
                <div class="text-center">
                    <h1>Спасибо, ваше сообщение получено!</h1>
                    <a href="/" class="btn btn-primary mt-3">Вернуться</a>
                </div>
            </body>
            </html>
        """
        self.wfile.write(response_message.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    """Запускает HTTP сервер."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен http://localhost:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()