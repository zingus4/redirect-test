# redirect-test
Скрипт проверяющий правильно ли отрабатывает список редиректов.

Входной файл, по умолчанию redirect.txt
Можно задать с помощию параметра -i
В формате:
Redirect 301 <start_url_relative_address> <finish_url_relative_address>

Входной файл, по умолчанию output.txt
Можно задать с помощию параметра -o
В формате:
Происходит ли редирект; Финальный статус; Совпадает ли конечная ссылка с задуманной; Начальный URL; URL rуда должно перейти; URL где в итоге оказались
Пример:
True, 404, True, <start_url_relative_address>, <expected_finish_url_relative_address>, <finish_url_relative_address>
